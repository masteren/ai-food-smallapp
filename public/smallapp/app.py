import hashlib
import json
import os
import random
import re
from datetime import date, datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from db import (
    add_cooking_log,
    add_recognition_log,
    create_user,
    fetch_pantry_items,
    fetch_recipe_by_id,
    fetch_recipes,
    fetch_recipes_with_ingredients,
    fetch_recognition_logs,
    fetch_cooking_log_count,
    fetch_expiry_alerts,
    fetch_cooking_logs_range,
    fetch_recently_used_recipes,
    get_user_by_id,
    get_user_by_username,
    init_db,
    seed_data,
    search_recipes,
    upsert_pantry_item,
    update_pantry_item,
    update_recipe,
    delete_pantry_item,
)
from services.openai_vision import (
    MissingAPIKeyError,
    NonJsonResponseError,
    OpenAIVisionError,
    VisionTimeoutError,
    recognize_ingredients_from_bytes,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")


DEMO_IMAGE_GROUPS: Tuple[Tuple[str, str], ...] = (
    ("fridge", "fridege"),
    ("cart", "cart"),
    ("table", "table"),
)
DEMO_IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
DEMO_CACHE_VERSION = "v2-ja"


with app.app_context():
    init_db()
  #  seed_data()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth"))
        return view(*args, **kwargs)

    return wrapped


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


def _is_strong_password(password: str) -> bool:
    if len(password) < 10:
        return False
    has_upper = re.search(r"[A-Z]", password) is not None
    has_lower = re.search(r"[a-z]", password) is not None
    has_digit = re.search(r"\d", password) is not None
    has_symbol = re.search(r"[^A-Za-z0-9]", password) is not None
    return has_upper and has_lower and has_digit and has_symbol


def _build_demo_catalog() -> List[Dict[str, List[str]]]:
    base_dir = Path(app.root_path) / "static"
    catalog: List[Dict[str, List[str]]] = []
    for key, rel_path in DEMO_IMAGE_GROUPS:
        dir_path = base_dir / rel_path
        images: List[str] = []
        if dir_path.exists():
            files = [
                path
                for path in dir_path.iterdir()
                if path.is_file() and path.suffix.lower() in DEMO_IMAGE_EXTS
            ]
            for path in sorted(files):
                images.append(url_for("static", filename=f"{rel_path}/{path.name}"))
        catalog.append({"key": key, "images": images})
    return catalog


def _demo_cache_path(image_bytes: bytes) -> Path:
    digest = hashlib.sha256(f"{DEMO_CACHE_VERSION}:".encode("utf-8") + image_bytes).hexdigest()
    cache_dir = Path(app.root_path) / "static" / "demo_cache"
    return cache_dir / f"{digest}.json"


def _sha256_digest(image_bytes: bytes) -> str:
    return hashlib.sha256(image_bytes).hexdigest()


def _current_week_monday_to_sunday(today: Optional[date] = None) -> List[str]:
    base_day = today or date.today()
    monday = base_day - timedelta(days=base_day.weekday())
    return [(monday + timedelta(days=offset)).isoformat() for offset in range(7)]


def _estimate_recipe_minutes(ingredients: List[Dict[str, object]], steps: List[str]) -> int:
    step_count = max(1, len(steps))
    ingredient_count = max(1, len(ingredients))
    step_text = " ".join(steps)

    # Simple heuristic for demo UI: step count + ingredient count + heavy cooking keywords.
    minutes = 4 + step_count * 3 + ingredient_count
    heavy_keywords = ("煮込", "揚げ", "焼き", "蒸し", "オーブン", "下ごしらえ")
    if any(k in step_text for k in heavy_keywords):
        minutes += 4
    return max(5, min(60, minutes))


def _recipe_level_stars(ingredients: List[Dict[str, object]], steps: List[str]) -> str:
    complexity = len(steps) * 2 + len(ingredients)
    step_text = " ".join(steps)
    advanced_keywords = ("包む", "衣", "二度", "煮込", "揚げ")
    if any(k in step_text for k in advanced_keywords):
        complexity += 2

    if complexity <= 8:
        return "★☆☆"
    if complexity <= 14:
        return "★★☆"
    return "★★★"


def _ingredient_note(name: str, unit: str, quantity: object) -> str:
    unit = _unit_to_japanese(unit)
    notes = {
        "鶏肉": "筋や余分な脂を落とすと仕上がりが軽い。",
        "鶏もも肉": "一口大に切ると火入れが均一になる。",
        "鶏むね肉": "加熱しすぎると固くなるので注意。",
        "豚肉": "臭みが気になる場合は酒を少量加える。",
        "牛肉": "強火で短時間に焼くと旨みを残しやすい。",
        "鶏卵": "溶きすぎず、半熟で止めると食感が良い。",
        "卵": "溶きすぎず、半熟で止めると食感が良い。",
        "玉ねぎ": "薄切りにすると甘みが出やすい。",
        "長ねぎ": "青い部分は仕上げに加えると香りが立つ。",
        "ネギ": "青い部分は仕上げに加えると香りが立つ。",
        "にんにく": "焦げやすいので弱火で香りを引き出す。",
        "ニンニク": "焦げやすいので弱火で香りを引き出す。",
        "豆腐": "水切りすると味がぼやけにくい。",
        "トマト": "酸味が強い場合は少量の砂糖で調整。",
        "じゃがいも": "煮崩れ防止に大きめに切る。",
        "ジャガイモ": "煮崩れ防止に大きめに切る。",
        "ブロッコリー": "食感を残すなら加熱は短めに。",
        "キノコ": "水分が出るので強火で一気に炒める。",
        "チーズ": "火を止めてから加えると分離しにくい。",
        "牛乳": "沸騰させず温めると分離を防げる。",
        "米": "炊きたてより少し冷ましたご飯が扱いやすい。",
        "米飯": "炊きたてより少し冷ましたご飯が扱いやすい。",
    }
    trimmed_name = name.strip()
    if trimmed_name in notes:
        return notes[trimmed_name]

    if unit == "g":
        return "下味を先につけると味が入りやすい。"
    if unit in ("個", "枚"):
        return "使う直前に準備すると風味を保ちやすい。"
    if unit in ("ml", "cc"):
        return "少しずつ加えて濃さを調整。"

    try:
        amount = float(quantity)
    except (TypeError, ValueError):
        amount = 0.0
    if amount >= 300:
        return "加熱ムラを避けるため数回に分けて調理。"
    return "お好みで量を微調整してOK。"


def _unit_to_japanese(unit: str) -> str:
    normalized = str(unit or "").strip()
    mapping = {
        "汤匙": "大さじ",
        "湯匙": "大さじ",
        "碗": "杯",
        "个": "個",
        "個": "個",
        "克": "g",
        "公克": "g",
        "毫升": "ml",
        "公升": "L",
        "匙": "さじ",
    }
    return mapping.get(normalized, normalized)


def _enrich_ingredients_with_notes(ingredients: List[Dict[str, object]]) -> List[Dict[str, object]]:
    enriched: List[Dict[str, object]] = []
    for item in ingredients:
        if not isinstance(item, dict):
            continue
        ingredient = dict(item)
        existing_note = str(ingredient.get("note", "")).strip()
        name = str(ingredient.get("name", "")).strip()
        unit = _unit_to_japanese(str(ingredient.get("unit", "")).strip())
        ingredient["unit"] = unit
        if existing_note:
            ingredient["note"] = existing_note
        else:
            ingredient["note"] = _ingredient_note(name, unit, ingredient.get("quantity"))
        enriched.append(ingredient)
    return enriched


def _recipe_edit_form_from_data(
    recipe: Dict[str, object],
    ingredients: List[Dict[str, object]],
    steps: List[str],
    nutrition: Dict[str, object],
) -> Dict[str, str]:
    ingredient_lines: List[str] = []
    for ing in ingredients:
        name = str(ing.get("name", "")).strip()
        quantity = str(ing.get("quantity", "")).strip()
        unit = str(ing.get("unit", "")).strip()
        note = str(ing.get("note", "") or "").strip()
        if not (name or quantity or unit or note):
            continue
        parts = [name, quantity, unit]
        if note:
            parts.append(note)
        ingredient_lines.append(" | ".join(parts))

    return {
        "title": str(recipe.get("title", "") or ""),
        "description": str(recipe.get("description", "") or ""),
        "ingredients_text": "\n".join(ingredient_lines),
        "steps_text": "\n".join(str(s) for s in steps if str(s).strip()),
        "nutrition_kcal": str(nutrition.get("kcal", "") or ""),
        "nutrition_protein": str(nutrition.get("protein", "") or ""),
        "nutrition_fat": str(nutrition.get("fat", "") or ""),
        "nutrition_carb": str(nutrition.get("carb", "") or ""),
        "nutrition_veg_score": str(nutrition.get("veg_score", "") or ""),
    }


def _parse_recipe_ingredients_text(text: str) -> List[Dict[str, object]]:
    ingredients: List[Dict[str, object]] = []
    for idx, raw_line in enumerate((text or "").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            raise ValueError(f"材料 {idx}行目は「食材名 | 量 | 単位」の形式で入力してください。")
        name, quantity, unit = parts[0], parts[1], parts[2]
        note = parts[3] if len(parts) >= 4 else ""
        if not name or not quantity or not unit:
            raise ValueError(f"材料 {idx}行目の食材名・量・単位は必須です。")
        item: Dict[str, object] = {
            "name": name,
            "quantity": quantity,
            "unit": unit,
        }
        if note:
            item["note"] = note
        ingredients.append(item)
    if not ingredients:
        raise ValueError("材料を1行以上入力してください。")
    return ingredients


def _parse_recipe_steps_text(text: str) -> List[str]:
    steps = [line.strip() for line in (text or "").splitlines() if line.strip()]
    if not steps:
        raise ValueError("手順を1行以上入力してください。")
    return steps


def _parse_nutrition_number(label: str, raw_value: str) -> float:
    value = (raw_value or "").strip()
    if not value:
        raise ValueError(f"{label}を入力してください。")
    try:
        number = float(value)
    except ValueError as exc:
        raise ValueError(f"{label}は数値で入力してください。") from exc
    if number < 0:
        raise ValueError(f"{label}は0以上で入力してください。")
    return int(number) if number.is_integer() else number


def _build_recipe_detail_context(
    recipe_id: int,
    *,
    edit_mode: bool = False,
    edit_error: str = "",
    edit_success: str = "",
    edit_form: Optional[Dict[str, str]] = None,
) -> Optional[Dict[str, object]]:
    recipe = fetch_recipe_by_id(recipe_id)
    if not recipe:
        return None

    user_id = session["user_id"]
    pantry_items = fetch_pantry_items(user_id)
    pantry_names = {item["name"] for item in pantry_items}

    raw_ingredients = json.loads(recipe["ingredients_json"])
    ingredients = _enrich_ingredients_with_notes(raw_ingredients)
    matched_ingredients = [ing for ing in ingredients if ing["name"] in pantry_names]
    match_rate = int((len(matched_ingredients) / len(ingredients) * 100) if ingredients else 0)

    raw_steps = json.loads(recipe["steps_json"])
    steps = raw_steps if isinstance(raw_steps, list) else []
    steps = [str(step) for step in steps]

    nutrition_data = json.loads(recipe["nutrition_json"])
    if not isinstance(nutrition_data, dict):
        nutrition_data = {}

    if edit_form is None:
        edit_form = _recipe_edit_form_from_data(recipe, ingredients, steps, nutrition_data)

    return {
        "recipe": recipe,
        "ingredients": ingredients,
        "steps": steps,
        "nutrition": nutrition_data,
        "match_rate": match_rate,
        "matched_count": len(matched_ingredients),
        "total_ingredients": len(ingredients),
        "user": current_user(),
        "edit_mode": edit_mode,
        "edit_error": edit_error,
        "edit_success": edit_success,
        "edit_form": edit_form,
    }


def _normalize_recipe_filters(selected_filter: str, selected_goal: str) -> Tuple[str, str]:
    normalized_filter = (selected_filter or "").strip()
    normalized_goal = (selected_goal or "").strip()
    if normalized_filter not in {"", "quick"}:
        normalized_filter = ""
    if normalized_goal not in {"", "low_fat"}:
        normalized_goal = ""
    return normalized_filter, normalized_goal


def _build_ranked_recipes(user_id: int, selected_filter: str = "", selected_goal: str = "") -> List[Dict[str, object]]:
    pantry_items = fetch_pantry_items(user_id)
    pantry_names = {item["name"] for item in pantry_items}
    recipes_data: List[Dict[str, object]] = []

    for recipe in fetch_recipes_with_ingredients():
        ingredients = recipe.get("ingredients") or []
        if not ingredients:
            ingredients = json.loads(recipe["ingredients_json"])

        required = [ing for ing in ingredients if ing.get("role") == "required"]
        if not required:
            required = ingredients
        required_names = {ing["name"] for ing in required}
        matched_required = [ing for ing in required if ing["name"] in pantry_names]

        total_required = max(1, len(required_names))
        match_rate = len(matched_required) / total_required
        missing_required = total_required - len(matched_required)

        if match_rate < 0.6 and missing_required > 2:
            continue

        nutrition = json.loads(recipe["nutrition_json"])
        steps = json.loads(recipe.get("steps_json", "[]"))
        if not isinstance(steps, list):
            steps = []
        step_texts = [str(s) for s in steps]
        cook_minutes = _estimate_recipe_minutes(ingredients, step_texts)
        cook_time = f"{cook_minutes}分"
        level_stars = _recipe_level_stars(ingredients, step_texts)

        if selected_filter == "quick" and cook_minutes > 15:
            continue

        health_score = 0
        if nutrition.get("protein", 0) >= 30:
            health_score += 10
        if nutrition.get("veg_score", 0) >= 2:
            health_score += 10
        if nutrition.get("kcal", 0) <= 500:
            health_score += 10
        if nutrition.get("fat", 0) <= 15:
            health_score += 10
        if nutrition.get("carb", 0) >= 70:
            health_score -= 10
        health_score = max(0, min(40, health_score))

        if selected_goal == "low_fat" and nutrition.get("fat", 0) > 15:
            continue

        match_score = max(0, min(60, int(match_rate * 60) - missing_required * 8))
        total_score = match_score + health_score

        if total_score >= 90:
            grade = "SSS"
        elif total_score >= 80:
            grade = "SS"
        elif total_score >= 70:
            grade = "S"
        elif total_score >= 60:
            grade = "A"
        elif total_score >= 50:
            grade = "B"
        else:
            grade = "C"

        recipes_data.append(
            {
                **recipe,
                "match_count": len(matched_required),
                "match_items": matched_required,
                "match_rate": int(match_rate * 100),
                "missing_required": missing_required,
                "health_score": health_score,
                "total_score": total_score,
                "grade": grade,
                "score": grade,
                "time": cook_time,
                "lvl": level_stars,
            }
        )

    recipes_data.sort(key=lambda r: r["total_score"], reverse=True)
    return recipes_data[:15]


def _build_search_results(query: str) -> List[Dict[str, object]]:
    if not query:
        return []

    results = search_recipes(query)
    for recipe in results:
        try:
            ingredients = json.loads(recipe.get("ingredients_json", "[]"))
            recipe["ingredients"] = ingredients
        except (json.JSONDecodeError, TypeError):
            recipe["ingredients"] = []
    return results


def _build_recently_used_data(user_id: int, limit: int = 50) -> List[Dict[str, object]]:
    recipes = fetch_recently_used_recipes(user_id, limit=limit)
    recipes_data = []
    for recipe in recipes:
        try:
            ingredients = json.loads(recipe.get("ingredients_json", "[]"))
        except (json.JSONDecodeError, TypeError):
            ingredients = []
        recipes_data.append(
            {
                "id": recipe["id"],
                "title": recipe["title"],
                "description": recipe["description"],
                "ingredients": ingredients,
                "last_cooked_date": recipe["last_cooked_date"],
            }
        )
    return recipes_data


def _build_dashboard_data(user_id: int) -> Dict[str, object]:
    recognition_count = len(fetch_recognition_logs(user_id, limit=100))
    recipe_count = fetch_cooking_log_count(user_id)
    expiry_alerts = fetch_expiry_alerts(user_id)
    recognition_logs = fetch_recognition_logs(user_id, limit=3)
    recent_recipes_raw = fetch_recently_used_recipes(user_id, limit=3)
    recent_recipes = [
        {
            "id": recipe["id"],
            "title": recipe["title"],
            "cooked_at_date": recipe.get("last_cooked_date"),
        }
        for recipe in recent_recipes_raw
    ]
    return {
        "recognition_count": recognition_count,
        "recipe_count": recipe_count,
        "expiry_alert_count": len(expiry_alerts),
        "recognition_logs": recognition_logs,
        "recent_recipes": recent_recipes,
    }


def _is_mobile_client() -> bool:
    # Prefer Client Hints when available, fallback to User-Agent keyword matching.
    ch_mobile = (request.headers.get("Sec-CH-UA-Mobile") or "").strip()
    if ch_mobile == "?1":
        return True
    if ch_mobile == "?0":
        return False

    ua = (request.headers.get("User-Agent") or "").lower()
    mobile_keywords = (
        "iphone",
        "android",
        "mobile",
        "ipad",
        "ipod",
        "windows phone",
        "blackberry",
        "opera mini",
    )
    return any(keyword in ua for keyword in mobile_keywords)


def _read_demo_cache(path: Path) -> Optional[List[Dict[str, object]]]:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    ingredients = payload.get("ingredients")
    if isinstance(ingredients, list):
        return ingredients
    return None


def _write_demo_cache(path: Path, ingredients: List[Dict[str, object]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "ingredients": ingredients,
            "cached_at": datetime.now().isoformat(),
        }
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except OSError:
        return


def _format_recognize_items(ingredients: List[Dict[str, object]]) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    for item in ingredients:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        name_ja = str(item.get("name_ja", "")).strip() or name
        confidence_value = item.get("confidence")
        try:
            confidence = float(confidence_value) if confidence_value is not None else 0.0
        except (TypeError, ValueError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))
        items.append(
            {
                "name": name,
                "name_ja": name_ja,
                "confidence": confidence,
            }
        )
    return items


def mobile_login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("mobile_login"))
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def inject_alert_count():
    """Inject alert count into all templates."""
    user_id = session.get("user_id")
    alert_count = 0
    stats_ingredients = 0
    if user_id:
        expiry_alerts = fetch_expiry_alerts(user_id)
        alert_count = len(expiry_alerts)
        stats_ingredients = len(fetch_pantry_items(user_id))
    style_path = Path(app.root_path) / "static" / "style.css"
    mobile_style_path = Path(app.root_path) / "static" / "mobile.css"
    mobile_scan_path = Path(app.root_path) / "static" / "mobile_scan.js"
    try:
        asset_v = str(int(style_path.stat().st_mtime))
        mobile_asset_v = str(
            max(
                int(style_path.stat().st_mtime),
                int(mobile_style_path.stat().st_mtime),
                int(mobile_scan_path.stat().st_mtime),
            )
        )
    except OSError:
        asset_v = "1"
        mobile_asset_v = "1"
    return dict(
        alert_count=alert_count,
        stats_ingredients=stats_ingredients,
        ingredient_note=_ingredient_note,
        asset_v=asset_v,
        mobile_asset_v=mobile_asset_v,
    )


@app.get("/")
def start():
    if _is_mobile_client():
        return redirect(url_for("mobile_root"))
    return render_template("start.html")


@app.get("/home")
@login_required
def home():
    # Get overview stats for home page
    user_id = session.get("user_id")

    pantry_count = 0
    expiry_alert_count = 0
    recipe_count = 0
    avg_protein = 0
    home_recommendations = []

    if user_id:
        # Get stats only if user is logged in
        pantry_items = fetch_pantry_items(user_id)
        pantry_count = len(pantry_items)

        expiry_alerts = fetch_expiry_alerts(user_id)
        expiry_alert_count = len(expiry_alerts)

        recipes_data = fetch_recipes()
        recipes_by_title = {str(recipe.get("title", "")): recipe for recipe in recipes_data}
        pantry_names = {item["name"] for item in pantry_items}
        recipe_count = sum(1 for recipe in recipes_data
                          if any(ing["name"] in pantry_names
                                for ing in json.loads(recipe["ingredients_json"])))

        # Keep homepage labels stable when available, but gracefully fallback
        # to existing recipes in the current dataset so the section never goes empty.
        preferred_items = [
            {"title": "鶏むね肉の塩レモン", "minutes": "15分", "difficulty": "★☆☆"},
            {"title": "卵と野菜のスープ", "minutes": "10分", "difficulty": "★☆☆"},
            {"title": "ツナ豆腐ボウル", "minutes": "7分", "difficulty": "★☆☆"},
        ]
        for item in preferred_items:
            recipe = recipes_by_title.get(item["title"])
            if not recipe:
                continue
            home_recommendations.append(
                {
                    "id": recipe["id"],
                    "title": item["title"],
                    "minutes": item["minutes"],
                    "difficulty": item["difficulty"],
                }
            )

        if not home_recommendations:
            fallback_minutes = ["15分", "10分", "7分"]
            for idx, recipe in enumerate(recipes_data[:3]):
                home_recommendations.append(
                    {
                        "id": recipe["id"],
                        "title": str(recipe.get("title", "")),
                        "minutes": fallback_minutes[idx] if idx < len(fallback_minutes) else "10分",
                        "difficulty": "★☆☆",
                    }
                )

        # Calculate average protein for the week
        labels = _current_week_monday_to_sunday()

        logs = fetch_cooking_logs_range(user_id, labels[0], labels[-1])
        recipes_map = {recipe["id"]: recipe for recipe in recipes_data}

        total_protein = 0
        for log in logs:
            recipe = recipes_map.get(log["recipe_id"])
            if recipe:
                nutrition = json.loads(recipe["nutrition_json"])
                total_protein += nutrition.get("protein", 0)

        avg_protein = int(total_protein / 7) if total_protein > 0 else 0

    return render_template(
        "home.html",
        user=current_user(),
        pantry_count=pantry_count,
        expiry_alert_count=expiry_alert_count,
        recipe_count=recipe_count,
        avg_protein=avg_protein,
        home_recommendations=home_recommendations,
    )


@app.get("/auth")
def auth():
    return render_template("auth.html", error=None)


@app.get("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")


@app.post("/register")
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        return render_template("auth.html", error="ユーザー名とパスワードを入力してください")

    if get_user_by_username(username):
        return render_template("auth.html", error="ユーザー名は既に使われています")

    if not _is_strong_password(password):
        return render_template(
            "auth.html",
            error="パスワードは10文字以上で、英大文字・英小文字・数字・記号を含めてください",
        )

    password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    user_id = create_user(username, password_hash)
    session["user_id"] = user_id
    return redirect(url_for("dashboard"))


@app.post("/login")
def login():
    username = request.form.get("login_username", request.form.get("username", "")).strip()
    password = request.form.get("login_password", request.form.get("password", "")).strip()

    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("auth.html", error="ログインに失敗しました")

    session["user_id"] = user["id"]
    return redirect(url_for("dashboard"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.get("/m")
def mobile_root():
    next_url = url_for("mobile_home") if "user_id" in session else url_for("mobile_login")
    return render_template("start.html", next_url=next_url)


@app.get("/m/login")
def mobile_login():
    if "user_id" in session:
        return redirect(url_for("mobile_home"))
    return render_template("mobile/login.html", error=None)


@app.post("/m/login")
def mobile_login_post():
    username = request.form.get("login_username", request.form.get("username", "")).strip()
    password = request.form.get("login_password", request.form.get("password", "")).strip()

    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("mobile/login.html", error="ログインに失敗しました")

    session["user_id"] = user["id"]
    return redirect(url_for("mobile_home"))


@app.post("/api/mobile/login")
def api_mobile_login():
    payload = request.get_json(silent=True) or {}

    username = str(payload.get("username", "")).strip()
    password = str(payload.get("password", "")).strip()

    if not username:
        username = request.form.get("login_username", request.form.get("username", "")).strip()
    if not password:
        password = request.form.get("login_password", request.form.get("password", "")).strip()

    if not username or not password:
        return jsonify({"ok": False, "error": "missing_credentials"}), 400

    user = get_user_by_username(username)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"ok": False, "error": "invalid_credentials"}), 401

    session["user_id"] = user["id"]
    return jsonify(
        {
            "ok": True,
            "user": {
                "id": user["id"],
                "username": user["username"],
            },
        }
    )


@app.post("/api/mobile/logout")
def api_mobile_logout():
    session.clear()
    return jsonify({"ok": True})


@app.post("/m/logout")
def mobile_logout():
    session.clear()
    return redirect(url_for("mobile_login"))


@app.get("/m/home")
@mobile_login_required
def mobile_home():
    demo_catalog = _build_demo_catalog()
    return render_template("mobile/scan.html", user=current_user(), demo_catalog=demo_catalog)


@app.get("/m/scan")
@mobile_login_required
def mobile_scan():
    demo_catalog = _build_demo_catalog()
    return render_template("mobile/scan.html", user=current_user(), demo_catalog=demo_catalog)


@app.get("/m/pantry")
@mobile_login_required
def mobile_pantry():
    items = fetch_pantry_items(session["user_id"])
    return render_template("mobile/pantry.html", user=current_user(), items=items)


@app.post("/m/pantry/add")
@mobile_login_required
def mobile_pantry_add():
    name = request.form.get("name", "").strip()
    quantity_raw = request.form.get("quantity", "").strip()
    unit = request.form.get("unit", "").strip() or "個"
    if name and quantity_raw.isdigit():
        upsert_pantry_item(
            session["user_id"],
            name,
            int(quantity_raw),
            unit,
            date.today().isoformat(),
        )
    return redirect(url_for("mobile_pantry"))


@app.post("/m/pantry/delete/<int:item_id>")
@mobile_login_required
def mobile_pantry_delete(item_id: int):
    delete_pantry_item(session["user_id"], item_id)
    return redirect(url_for("mobile_pantry"))


@app.get("/m/dashboard")
@mobile_login_required
def mobile_dashboard():
    user_id = session["user_id"]
    return render_template(
        "mobile/dashboard.html",
        user=current_user(),
        mobile_active="dashboard",
        **_build_dashboard_data(user_id),
    )


@app.get("/m/recipes")
@mobile_login_required
def mobile_recipes():
    selected_filter, selected_goal = _normalize_recipe_filters(
        request.args.get("filter", ""),
        request.args.get("goal", ""),
    )
    recipes_data = _build_ranked_recipes(session["user_id"], selected_filter, selected_goal)
    return render_template(
        "mobile/recipes.html",
        user=current_user(),
        mobile_active="recipes",
        recipes=recipes_data,
        selected_filter=selected_filter,
        selected_goal=selected_goal,
    )


@app.get("/m/search")
@mobile_login_required
def mobile_search():
    query = request.args.get("q", "").strip()
    results = _build_search_results(query)
    return render_template(
        "mobile/search.html",
        user=current_user(),
        mobile_active="search",
        query=query,
        results=results,
    )


@app.get("/m/recently-used")
@app.get("/m/recently_used")
@mobile_login_required
def mobile_recently_used():
    recipes_data = _build_recently_used_data(session["user_id"], limit=50)
    return render_template(
        "mobile/recently_used.html",
        user=current_user(),
        mobile_active="recently_used",
        recipes=recipes_data,
    )


@app.get("/m/recipes/<int:recipe_id>")
@mobile_login_required
def mobile_recipe_detail(recipe_id: int):
    context = _build_recipe_detail_context(
        recipe_id,
        edit_mode=request.args.get("edit") == "1",
        edit_success="レシピを更新しました。" if request.args.get("saved") == "1" else "",
    )
    if not context:
        return redirect(url_for("mobile_recipes"))
    context["mobile_active"] = "recipes"
    return render_template("mobile/recipe_detail.html", **context)


@app.post("/m/recipes/<int:recipe_id>/edit")
@mobile_login_required
def mobile_recipe_edit(recipe_id: int):
    recipe = fetch_recipe_by_id(recipe_id)
    if not recipe:
        return redirect(url_for("mobile_recipes"))

    form_values = {
        "ingredients_text": request.form.get("ingredients_text", "").strip(),
        "steps_text": request.form.get("steps_text", "").strip(),
    }

    try:
        ingredients = _parse_recipe_ingredients_text(form_values["ingredients_text"])
        steps = _parse_recipe_steps_text(form_values["steps_text"])
        title = str(recipe.get("title", "") or "")
        description = str(recipe.get("description", "") or "")
        nutrition_json = recipe.get("nutrition_json", "{}")
        if not isinstance(nutrition_json, str):
            nutrition_json = json.dumps(nutrition_json, ensure_ascii=False)

        update_recipe(
            recipe_id,
            title,
            description,
            json.dumps(steps, ensure_ascii=False),
            json.dumps(ingredients, ensure_ascii=False),
            nutrition_json,
        )
    except ValueError as exc:
        context = _build_recipe_detail_context(
            recipe_id,
            edit_mode=True,
            edit_error=str(exc),
            edit_form=form_values,
        )
        if not context:
            return redirect(url_for("mobile_recipes"))
        context["mobile_active"] = "recipes"
        return render_template("mobile/recipe_detail.html", **context)

    return redirect(url_for("mobile_recipe_detail", recipe_id=recipe_id, saved=1, edit=1))


@app.post("/m/recipes/<int:recipe_id>/cook")
@mobile_login_required
def mobile_recipe_cook(recipe_id: int):
    add_cooking_log(session["user_id"], recipe_id, date.today().isoformat())
    return redirect(url_for("mobile_recipe_detail", recipe_id=recipe_id))


@app.get("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]
    return render_template(
        "dashboard.html",
        user=current_user(),
        **_build_dashboard_data(user_id),
    )


def _mock_recognize(filename: str) -> List[Dict[str, str]]:
    pool = ["鶏むね肉", "卵", "ブロッコリー", "牛乳", "ご飯", "豆腐", "トマト", "玉ねぎ"]
    matches = []
    name = filename.lower()
    keyword_map = {
        "chicken": "鶏むね肉",
        "egg": "卵",
        "broccoli": "ブロッコリー",
        "milk": "牛乳",
        "rice": "ご飯",
        "tofu": "豆腐",
        "tomato": "トマト",
        "onion": "玉ねぎ",
    }
    for key, value in keyword_map.items():
        if key in name and value not in matches:
            matches.append(value)

    if not matches:
        matches = random.sample(pool, random.randint(3, 6))

    results = []
    for item in matches:
        results.append({
            "name": item,
            "quantity": random.randint(1, 3),
            "unit": "個" if item in ["卵", "トマト"] else "枚" if item == "鶏むね肉" else "株" if item == "ブロッコリー" else "本" if item == "牛乳" else "杯" if item == "ご飯" else "丁" if item == "豆腐" else "個",
        })
    return results


@app.get("/recognize")
@login_required
def recognize():
    return redirect(url_for("vision"))


@app.post("/recognize")
@login_required
def recognize_post():
    file = request.files.get("image")
    if not file:
        return redirect(url_for("recognize"))

    results = _mock_recognize(file.filename or "")
    session["recognize_items"] = results
    session.modified = True
    return redirect(url_for("recognize"))


@app.post("/recognize/update/<int:item_index>")
@login_required
def recognize_update(item_index: int):
    items = session.get("recognize_items", [])
    if 0 <= item_index < len(items):
        name = request.form.get("name", "").strip()
        quantity = request.form.get("quantity", "1").strip()
        unit = request.form.get("unit", "").strip()
        if name and quantity.isdigit() and unit:
            items[item_index] = {
                "name": name,
                "quantity": int(quantity),
                "unit": unit,
            }
            session["recognize_items"] = items
            session.modified = True
    return redirect(url_for("recognize"))


@app.post("/recognize/delete/<int:item_index>")
@login_required
def recognize_delete(item_index: int):
    items = session.get("recognize_items", [])
    if 0 <= item_index < len(items):
        items.pop(item_index)
        session["recognize_items"] = items
        session.modified = True
    return redirect(url_for("recognize"))


@app.post("/recognize/save")
@login_required
def recognize_save():
    items = session.get("recognize_items", [])
    user_id = session["user_id"]
    for item in items:
        upsert_pantry_item(
            user_id,
            item["name"],
            int(item["quantity"]),
            item["unit"],
            date.today().isoformat(),
        )
    if items:
        add_recognition_log(user_id, datetime.now().isoformat(), len(items))
    session["recognize_items"] = []
    session.modified = True
    return redirect(url_for("pantry"))


@app.get("/pantry")
@login_required
def pantry():
    user_id = session["user_id"]
    items = fetch_pantry_items(user_id)
    expiry_alerts = fetch_expiry_alerts(user_id)
    return render_template("pantry.html", items=items, expiry_alert_count=len(expiry_alerts), user=current_user())


@app.post("/pantry/add")
@login_required
def pantry_add():
    name = request.form.get("name", "").strip()
    quantity_raw = request.form.get("quantity", "").strip()
    unit = request.form.get("unit", "").strip()
    expiry_date = request.form.get("expiry_date", "").strip()
    expiry_value = expiry_date or None
    if name and quantity_raw.isdigit() and unit:
        upsert_pantry_item(
            session["user_id"],
            name,
            int(quantity_raw),
            unit,
            expiry_value,
        )
    return redirect(url_for("pantry"))


@app.get("/vision")
@login_required
def vision():
    demo_catalog = _build_demo_catalog()
    return render_template("vision.html", user=current_user(), demo_catalog=demo_catalog)


@app.post("/api/recognize")
@login_required
def api_recognize():
    file = request.files.get("image")
    if not file:
        return jsonify({"ok": False, "error": "missing_image"}), 400

    image_bytes = file.read()
    if not image_bytes:
        return jsonify({"ok": False, "error": "empty_image"}), 400

    digest = _sha256_digest(image_bytes)
    cache_path = _demo_cache_path(image_bytes)
    cached_ingredients = _read_demo_cache(cache_path)
    if cached_ingredients is not None:
        return jsonify(
            {
                "ok": True,
                "sha256": digest,
                "items": _format_recognize_items(cached_ingredients),
            }
        )

    mime_type = file.mimetype or "image/jpeg"
    try:
        ingredients = recognize_ingredients_from_bytes(image_bytes, mime_type)
    except MissingAPIKeyError as exc:
        mock_items = _mock_recognize(file.filename or "")
        return jsonify(
            {
                "ok": True,
                "sha256": digest,
                "items": _format_recognize_items(mock_items),
                "mock": True,
            }
        )
    except VisionTimeoutError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 504
    except NonJsonResponseError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502
    except OpenAIVisionError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502
    except Exception:
        return jsonify({"ok": False, "error": "unknown_error"}), 500

    if ingredients:
        _write_demo_cache(cache_path, ingredients)

    return jsonify(
        {
            "ok": True,
            "sha256": digest,
            "items": _format_recognize_items(ingredients),
        }
    )


@app.post("/api/mobile/pantry/save")
@mobile_login_required
def api_mobile_pantry_save():
    payload = request.get_json(silent=True) or {}
    items = payload.get("items", [])
    if not isinstance(items, list):
        return jsonify({"ok": False, "error": "invalid_payload"}), 400

    user_id = session["user_id"]
    saved = 0
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name_ja") or item.get("name") or "").strip()
        if not name:
            continue
        upsert_pantry_item(
            user_id,
            name,
            1,
            "個",
            date.today().isoformat(),
        )
        saved += 1

    if saved > 0:
        add_recognition_log(user_id, datetime.now().isoformat(), saved)
    return jsonify({"ok": True, "saved": saved})


@app.get("/api/mobile/pantry")
def api_mobile_pantry():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"ok": False, "error": "unauthorized"}), 401

    items = fetch_pantry_items(user_id)
    return jsonify({"ok": True, "items": items})


@app.post("/api/vision/ingredients")
@login_required
def vision_ingredients():
    file = request.files.get("image")
    if not file:
        return jsonify({"error": "missing_image"}), 400

    image_bytes = file.read()
    if not image_bytes:
        return jsonify({"error": "empty_image"}), 400

    mime_type = file.mimetype or "image/jpeg"
    prefer_cache = request.headers.get("X-Demo-Image") == "1"
    cache_path = _demo_cache_path(image_bytes)
    cached_ingredients = _read_demo_cache(cache_path)

    if prefer_cache and cached_ingredients is not None:
        response = jsonify({"ingredients": cached_ingredients})
        response.headers["X-Cache-Status"] = "Cached"
        return response

    try:
        ingredients = recognize_ingredients_from_bytes(image_bytes, mime_type)
    except MissingAPIKeyError as exc:
        if cached_ingredients is not None:
            response = jsonify({"ingredients": cached_ingredients})
            response.headers["X-Cache-Status"] = "Cached"
            response.headers["X-Cache-Fallback"] = "1"
            return response
        return jsonify({"error": "missing_api_key", "detail": str(exc)}), 500
    except VisionTimeoutError as exc:
        if cached_ingredients is not None:
            response = jsonify({"ingredients": cached_ingredients})
            response.headers["X-Cache-Status"] = "Cached"
            response.headers["X-Cache-Fallback"] = "1"
            return response
        return jsonify({"error": "timeout", "detail": str(exc)}), 504
    except NonJsonResponseError as exc:
        if cached_ingredients is not None:
            response = jsonify({"ingredients": cached_ingredients})
            response.headers["X-Cache-Status"] = "Cached"
            response.headers["X-Cache-Fallback"] = "1"
            return response
        return jsonify({"error": "non_json_response", "detail": str(exc)}), 502
    except OpenAIVisionError as exc:
        if cached_ingredients is not None:
            response = jsonify({"ingredients": cached_ingredients})
            response.headers["X-Cache-Status"] = "Cached"
            response.headers["X-Cache-Fallback"] = "1"
            return response
        return jsonify({"error": "vision_error", "detail": str(exc)}), 502
    except Exception:
        if cached_ingredients is not None:
            response = jsonify({"ingredients": cached_ingredients})
            response.headers["X-Cache-Status"] = "Cached"
            response.headers["X-Cache-Fallback"] = "1"
            return response
        return jsonify({"error": "unknown_error"}), 500

    if ingredients:
        _write_demo_cache(cache_path, ingredients)

    response = jsonify({"ingredients": ingredients})
    response.headers["X-Cache-Status"] = "Live"
    return response


@app.post("/api/vision/save")
@login_required
def vision_save():
    payload = request.get_json(silent=True) or {}
    items = payload.get("ingredients", [])
    if not isinstance(items, list):
        return jsonify({"error": "invalid_payload"}), 400

    user_id = session["user_id"]
    saved = 0
    today_str = date.today().isoformat()
    for item in items:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        quantity_raw = item.get("quantity", 1)
        try:
            quantity = int(float(quantity_raw))
        except (TypeError, ValueError):
            quantity = 1
        unit = str(item.get("unit", "個")).strip() or "個"
        expiry_date = str(item.get("expiry_date", "")).strip() or today_str
        upsert_pantry_item(user_id, name, quantity, unit, expiry_date)
        saved += 1

    return jsonify({"saved": saved})


@app.post("/pantry/update/<int:item_id>")
@login_required
def pantry_update(item_id: int):
    name = request.form.get("name", "").strip()
    quantity_raw = request.form.get("quantity", "").strip()
    unit = request.form.get("unit", "").strip()
    expiry_date = request.form.get("expiry_date", "").strip()
    expiry_value = expiry_date or None
    if name and quantity_raw.isdigit() and unit:
        update_pantry_item(
            session["user_id"],
            item_id,
            name,
            int(quantity_raw),
            unit,
            expiry_value,
        )
    return redirect(url_for("pantry"))


@app.get("/pantry/delete/<int:item_id>")
@login_required
def pantry_delete(item_id: int):
    delete_pantry_item(session["user_id"], item_id)
    return redirect(url_for("pantry"))


@app.get("/recipes")
@login_required
def recipes():
    selected_filter, selected_goal = _normalize_recipe_filters(
        request.args.get("filter", ""),
        request.args.get("goal", ""),
    )
    recipes_data = _build_ranked_recipes(session["user_id"], selected_filter, selected_goal)
    return render_template(
        "recipes.html",
        recipes=recipes_data,
        user=current_user(),
        selected_filter=selected_filter,
        selected_goal=selected_goal,
    )


@app.get("/search")
@login_required
def search():
    query = request.args.get("q", "").strip()
    results = _build_search_results(query)
    return render_template(
        "search.html",
        query=query,
        results=results,
        user=current_user(),
    )


@app.get("/recently-used")
@app.get("/recently_used")
@login_required
def recently_used():
    """Display recently used recipes efficiently."""
    recipes_data = _build_recently_used_data(session["user_id"], limit=50)
    return render_template(
        "recently_used.html",
        recipes=recipes_data,
        user=current_user(),
    )


@app.get("/recipes/<int:recipe_id>")
@login_required
def recipe_detail(recipe_id: int):
    context = _build_recipe_detail_context(
        recipe_id,
        edit_mode=request.args.get("edit") == "1",
        edit_success="レシピを更新しました。" if request.args.get("saved") == "1" else "",
    )
    if not context:
        return redirect(url_for("recipes"))
    return render_template("recipe_detail.html", **context)


@app.post("/recipes/<int:recipe_id>/edit")
@login_required
def recipe_edit(recipe_id: int):
    recipe = fetch_recipe_by_id(recipe_id)
    if not recipe:
        return redirect(url_for("recipes"))

    form_values = {
        "ingredients_text": request.form.get("ingredients_text", "").strip(),
        "steps_text": request.form.get("steps_text", "").strip(),
    }

    try:
        ingredients = _parse_recipe_ingredients_text(form_values["ingredients_text"])
        steps = _parse_recipe_steps_text(form_values["steps_text"])
        title = str(recipe.get("title", "") or "")
        description = str(recipe.get("description", "") or "")
        nutrition_json = recipe.get("nutrition_json", "{}")
        if not isinstance(nutrition_json, str):
            nutrition_json = json.dumps(nutrition_json, ensure_ascii=False)

        update_recipe(
            recipe_id,
            title,
            description,
            json.dumps(steps, ensure_ascii=False),
            json.dumps(ingredients, ensure_ascii=False),
            nutrition_json,
        )
    except ValueError as exc:
        context = _build_recipe_detail_context(
            recipe_id,
            edit_mode=True,
            edit_error=str(exc),
            edit_form=form_values,
        )
        if not context:
            return redirect(url_for("recipes"))
        return render_template("recipe_detail.html", **context)

    return redirect(url_for("recipe_detail", recipe_id=recipe_id, saved=1, edit=1))


@app.post("/recipes/<int:recipe_id>/cook")
@login_required
def recipe_cook(recipe_id: int):
    add_cooking_log(session["user_id"], recipe_id, date.today().isoformat())
    return redirect(url_for("recipe_detail", recipe_id=recipe_id))


def _nutrition_score(today_totals: Dict[str, float]) -> Dict[str, str]:
    total_kcal = today_totals.get("kcal", 0)
    protein = today_totals.get("protein", 0)
    veg_score = today_totals.get("veg_score", 0)

    score = 50
    if total_kcal == 0:
        score = 20
    elif 1600 <= total_kcal <= 2400:
        score += 20
    elif total_kcal < 1400 or total_kcal > 2600:
        score -= 5

    if protein >= 60:
        score += 20
    elif protein >= 40:
        score += 10
    else:
        score -= 5

    if veg_score >= 2:
        score += 10

    score = max(0, min(100, int(score)))

    if score >= 90:
        grade = "S"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 55:
        grade = "C"
    else:
        grade = "D"

    reasons = []
    if total_kcal == 0:
        reasons.append("本日の食事記録がありません")
    elif total_kcal < 1400:
        reasons.append("カロリーが少なめです")
    elif total_kcal > 2600:
        reasons.append("カロリーが高めです")
    else:
        reasons.append("カロリーは適正範囲です")

    if protein < 40:
        reasons.append("たんぱく質が不足気味です")
    else:
        reasons.append("たんぱく質が十分です")

    if veg_score < 2:
        reasons.append("野菜スコアを上げましょう")
    else:
        reasons.append("野菜摂取は良好です")

    return {"score": score, "grade": grade, "reasons": reasons[:3]}


def _nutrition_demo_totals(labels: List[str]) -> Tuple[Dict[str, Dict[str, float]], Dict[str, float]]:
    kcal_demo = [1680, 1820, 1760, 1910, 1740, 2050, 1860]
    protein_demo = [58, 64, 62, 71, 59, 76, 68]

    daily_totals = {
        label: {"kcal": kcal_demo[idx], "protein": protein_demo[idx]}
        for idx, label in enumerate(labels)
    }
    today_totals = {
        "kcal": kcal_demo[-1],
        "protein": protein_demo[-1],
        "veg_score": 3,
    }
    return daily_totals, today_totals


DEFAULT_STAPLE_KCAL = 252  # Approx. one bowl of cooked rice.


def _build_nutrition_context(user_id: int, use_demo: bool = False) -> Dict[str, object]:
    recipes_map = {recipe["id"]: recipe for recipe in fetch_recipes()}
    today = date.today()
    labels = _current_week_monday_to_sunday(today)

    daily_totals = {label: {"kcal": 0, "protein": 0} for label in labels}
    today_totals = {"kcal": 0, "protein": 0, "veg_score": 0}

    logs = fetch_cooking_logs_range(user_id, labels[0], labels[-1])
    if use_demo or not logs:
        daily_totals, today_totals = _nutrition_demo_totals(labels)
    else:
        days_with_logs = set()
        for log in logs:
            recipe = recipes_map.get(log["recipe_id"])
            if not recipe:
                continue
            nutrition = json.loads(recipe["nutrition_json"])
            day_key = log["cooked_at_date"]
            if day_key in daily_totals:
                days_with_logs.add(day_key)
                daily_totals[day_key]["kcal"] += nutrition.get("kcal", 0)
                daily_totals[day_key]["protein"] += nutrition.get("protein", 0)
            if day_key == today.isoformat():
                today_totals["kcal"] += nutrition.get("kcal", 0)
                today_totals["protein"] += nutrition.get("protein", 0)
                today_totals["veg_score"] += nutrition.get("veg_score", 0)

        for day_key in days_with_logs:
            daily_totals[day_key]["kcal"] += DEFAULT_STAPLE_KCAL
        if today.isoformat() in days_with_logs:
            today_totals["kcal"] += DEFAULT_STAPLE_KCAL

    score_data = _nutrition_score(today_totals)
    kcal_series = [daily_totals[label]["kcal"] for label in labels]
    protein_series = [daily_totals[label]["protein"] for label in labels]

    alerts = []
    if today_totals["protein"] < 40:
        alerts.append("たんぱく質を強化しましょう")
    if today_totals["veg_score"] < 2:
        alerts.append("野菜摂取が不足しています")
    if not alerts:
        alerts = [
            "栄養バランスは良好です",
            "水分を1.5L以上を目安に維持しましょう",
            "夕食の野菜量をもう1皿増やすとさらに安定します",
        ]

    pantry_items = fetch_pantry_items(user_id)
    pantry_names = {item["name"] for item in pantry_items}
    shopping_list = []
    if today_totals["protein"] < 40:
        for item in ["鶏むね肉", "豆腐", "牛乳"]:
            if item not in pantry_names:
                shopping_list.append(item)
    if today_totals["veg_score"] < 2:
        for item in ["ブロッコリー", "トマト", "玉ねぎ"]:
            if item not in pantry_names:
                shopping_list.append(item)
    if not shopping_list:
        shopping_list = ["牛乳", "卵"]

    return {
        "score_data": score_data,
        "labels": labels,
        "kcal_series": kcal_series,
        "protein_series": protein_series,
        "alerts": alerts,
        "shopping_list": shopping_list,
        "today_totals": today_totals,
    }


@app.get("/m/nutrition")
@mobile_login_required
def mobile_nutrition():
    use_demo = request.args.get("demo") == "1"
    return render_template(
        "mobile/nutrition.html",
        user=current_user(),
        mobile_active="nutrition",
        **_build_nutrition_context(session["user_id"], use_demo=use_demo),
    )


@app.get("/m/notifications")
@mobile_login_required
def mobile_notifications():
    user_id = session["user_id"]
    expiry_alerts = fetch_expiry_alerts(user_id)
    return render_template(
        "mobile/notifications.html",
        user=current_user(),
        mobile_active="notifications",
        alerts=expiry_alerts,
        alert_count=len(expiry_alerts),
    )


@app.get("/nutrition")
@login_required
def nutrition():
    use_demo = request.args.get("demo") == "1"
    return render_template(
        "nutrition.html",
        user=current_user(),
        **_build_nutrition_context(session["user_id"], use_demo=use_demo),
    )


@app.get("/notifications")
@login_required
def notifications():
    user_id = session["user_id"]
    expiry_alerts = fetch_expiry_alerts(user_id)
    return render_template(
        "notifications.html",
        user=current_user(),
        alerts=expiry_alerts,
        alert_count=len(expiry_alerts),
    )


if __name__ == "__main__":
    app.run(debug=True)
