# AI 冷蔵庫システム（食材・レシピ管理アプリ）

冷蔵庫や買い物袋の写真を撮るだけで、AI が食材を認識して在庫に登録し、
手持ちの食材で作れるレシピを栄養バランスと合わせて提案する Web アプリ。

**HAL EVENT WEEK 銅賞（2026.03）**

デモ：<https://fridge.masteren.online/>

## テーマ

「冷蔵庫に何があるか分からない」「食材を使い切れずに捨ててしまう」という
日常の困りごとを、写真1枚から解決することを目指した。
在庫の登録を手入力ではなく画像認識にすることで、続けやすさを重視している。

## 主な機能

- **画像から食材を認識** … 写真をアップロードすると、OpenAI の Vision モデルが
  食材名・数量・単位を JSON で返す。結果は画面上で修正してから在庫に保存できる。
- **在庫管理** … 食材の追加・編集・削除。賞味期限が 7 日以内の食材は通知に表示。
- **レシピ提案** … 50 品のレシピを、手持ち食材との一致率と栄養スコアで
  ランク付け（SSS〜C）して表示。「低脂質」などの目的で絞り込みもできる。
- **レシピ編集** … 材料・手順・栄養値（kcal / たんぱく質 / 脂質 / 炭水化物）を画面から編集。
- **調理記録と栄養** … 「作った」を記録し、今週の調理履歴やたんぱく質量を集計。
- **スマホ対応** … スマホからのアクセスを自動判定し、専用画面（`/m/...`）に切り替え。
  Android アプリから使う JSON API も用意。

## 技術スタック

| 分類 | 使用技術 |
| --- | --- |
| バックエンド | Python / Flask 3 |
| データベース | SQLite |
| AI | OpenAI Responses API（`gpt-4.1-mini`、画像入力 + Structured Outputs） |
| フロントエンド | Jinja2 テンプレート、CSS、JavaScript |
| インフラ | Ubuntu / nginx / gunicorn / Let's Encrypt（Tencent Cloud） |

## ファイル構成

アプリ本体は `public/fridge/` にある。

| ファイル | 役割 |
| --- | --- |
| `app.py` | ルーティング、レシピのランク付け、デモキャッシュなど |
| `db.py` | テーブル定義と SQL。DB アクセスはすべてここに集約 |
| `services/openai_vision.py` | OpenAI API を呼び出して食材を認識する処理 |
| `recipes_data.py` | レシピの初期データ（50 品） |
| `templates/` | PC 用画面（Jinja2） |
| `templates/mobile/` | スマホ用画面 |
| `static/` | CSS・画像・スマホ用 JS、デモ用サンプル画像 |

## 起動手順

```bash
cd public/fridge

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt gunicorn

# 環境変数（必須）
export OPENAI_API_KEY=sk-...
export FLASK_SECRET_KEY=任意のランダムな文字列

# 1回目だけ: レシピの初期データを投入
python -c "import db; db.init_db(); db.seed_data()"

# 起動
python app.py
```

ブラウザで <http://localhost:5000> を開き、ユーザー登録してから利用する。

- `db.sqlite3` は自動生成される（Git 管理外）。
- `FLASK_SECRET_KEY` が未設定の場合は起動時にエラーになる（安全のため、デフォルト値は持たせていない）。
- 本番環境では gunicorn + nginx で動かしている。

## 画面

| URL | 内容 |
| --- | --- |
| `/` | 起動画面 |
| `/auth` | ログイン・ユーザー登録 |
| `/home` | ホーム。在庫数・期限間近の食材・おすすめレシピ |
| `/recognize` | 写真から食材を認識して在庫に登録 |
| `/pantry` | 在庫一覧・編集 |
| `/recipes` | レシピ一覧（ランク付き・目的別の絞り込み） |
| `/recipes/<id>` | レシピ詳細・編集・「作った」記録 |
| `/nutrition` | 栄養の集計 |
| `/notifications` | 賞味期限のお知らせ |
| `/m/...` | 上記のスマホ版 |

## 工夫した点

### AI の出力を JSON スキーマで固定

Vision モデルの返答をそのまま使うと、形式が毎回少しずつ変わってしまう。
OpenAI の Structured Outputs（`json_schema`, `strict: true`）を使い、
`name`（日本語名）・`name_en`・`quantity`・`unit`・`confidence` の形を固定した。
タイムアウトや JSON 以外の返答は専用の例外クラスに分けて、画面にエラーを出せるようにしている。

### デモ画像の結果をキャッシュ

展示会では同じサンプル画像が何度も使われる。画像の SHA-256 ハッシュをキーに
認識結果をファイルに保存し、2 回目以降は API を呼ばずに即座に結果を返す。
応答が速くなり、API の利用料金も抑えられる。

### レシピのランク付け

手持ち食材との一致率（最大 60 点）と、栄養スコア（たんぱく質・野菜・カロリー・
脂質から最大 40 点）を合計し、SSS〜C の 6 段階で表示する。
足りない必須食材が多いほど減点されるので、「今すぐ作れるレシピ」が上位に来る。

### PC とスマホで画面を自動切り替え

Client Hints（`Sec-CH-UA-Mobile`）を優先して判定し、使えないブラウザでは
User-Agent で判定する。スマホでは片手で操作しやすい専用レイアウトを表示する。

### セキュリティ

- パスワードは `pbkdf2:sha256` でハッシュ化して保存。登録時は 10 文字以上・
  大文字・小文字・数字・記号を必須にしている。
- API キーとセッション用の秘密鍵は環境変数から読み込み、コードやリポジトリには含めない。
- SQL の値はすべてプレースホルダ（`?`）で渡している。
