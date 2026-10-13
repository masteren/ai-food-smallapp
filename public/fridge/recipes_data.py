# 日本語レシピデータ
INTERNATIONAL_RECIPES = [
    # 日本 🇯🇵
    {
        "title": "カレーライス",
        "region": "日本",
        "description": "日本国民料理、栄養豊富で美味しい",
        "ingredients": [
            {"name": "カレールー", "quantity": 2, "unit": "個"},
            {"name": "じゃがいも", "quantity": 1, "unit": "個"},
            {"name": "人参", "quantity": 1, "unit": "個"},
            {"name": "肉", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "肉と野菜を炒める",
            "水を加えて沸騰させる",
            "カレールーを加えて20分煮込む",
        ],
        "nutrition": {"kcal": 580, "protein": 24, "fat": 20, "carb": 72, "salt": 1.8, "veg_score": 2},
    },
    {
        "title": "親子丼",
        "region": "日本",
        "description": "鶏肉と卵の経典的な組み合わせ",
        "ingredients": [
            {"name": "鶏肉", "quantity": 200, "unit": "g"},
            {"name": "鶏卵", "quantity": 2, "unit": "個"},
            {"name": "玉ねぎ", "quantity": 0.5, "unit": "個"},
        ],
        "steps": [
            "鶏肉を切り、玉ねぎを細切りに",
            "鶏肉を塩辛いタレで煮込む",
            "卵液を流し入れ、半凝固状態で丼飯に盛る",
        ],
        "nutrition": {"kcal": 420, "protein": 28, "fat": 14, "carb": 48, "salt": 1.4, "veg_score": 1},
    },
    {
        "title": "生姜焼き",
        "region": "日本",
        "description": "甘辛い生姜味の炒め肉",
        "ingredients": [
            {"name": "豚肉", "quantity": 300, "unit": "g"},
            {"name": "生姜", "quantity": 3, "unit": "枚"},
        ],
        "steps": [
            "生姜を千切りに",
            "豚肉を炒めて色が変わるまで",
            "生姜と調味液を加えて炒める",
        ],
        "nutrition": {"kcal": 360, "protein": 32, "fat": 18, "carb": 12, "salt": 1.3, "veg_score": 0},
    },
    {
        "title": "唐揚げ",
        "region": "日本",
        "description": "日式チキンフライ",
        "ingredients": [
            {"name": "鶏もも肉", "quantity": 400, "unit": "g"},
            {"name": "醤油", "quantity": 3, "unit": "大さじ"},
        ],
        "steps": [
            "鶏肉を醤油に浸す",
            "小麦粉をつけて揚げる",
            "油を切って食べる",
        ],
        "nutrition": {"kcal": 520, "protein": 38, "fat": 28, "carb": 16, "salt": 1.6, "veg_score": 0},
    },
    {
        "title": "焼きうどん",
        "region": "日本",
        "description": "醤油の香りが濃厚な麺料理",
        "ingredients": [
            {"name": "うどん", "quantity": 300, "unit": "g"},
            {"name": "野菜", "quantity": 150, "unit": "g"},
            {"name": "肉", "quantity": 150, "unit": "g"},
        ],
        "steps": [
            "肉と野菜を炒める",
            "うどんを加えて炒める",
            "醤油と調味液を加えて混ぜ合わせる",
        ],
        "nutrition": {"kcal": 480, "protein": 24, "fat": 14, "carb": 64, "salt": 2.0, "veg_score": 1},
    },
    {
        "title": "味噌汁",
        "region": "日本",
        "description": "最も基本的な日本式スープ",
        "ingredients": [
            {"name": "味噌", "quantity": 2, "unit": "大さじ"},
            {"name": "豆腐", "quantity": 150, "unit": "g"},
            {"name": "昆布", "quantity": 5, "unit": "g"},
        ],
        "steps": [
            "昆布で出汁を作る",
            "豆腐を加える",
            "味噌で味付けする",
        ],
        "nutrition": {"kcal": 120, "protein": 10, "fat": 4, "carb": 10, "salt": 1.8, "veg_score": 1},
    },
    {
        "title": "てり焼きチキン",
        "region": "日本",
        "description": "甘辛い味わい、ご飯に合う",
        "ingredients": [
            {"name": "鶏肉", "quantity": 300, "unit": "g"},
            {"name": "てり焼きソース", "quantity": 4, "unit": "大さじ"},
        ],
        "steps": [
            "鶏肉を両面焼く",
            "てり焼きソースを加える",
            "汁が濃くなるまで煮込む",
        ],
        "nutrition": {"kcal": 340, "protein": 32, "fat": 14, "carb": 16, "salt": 1.5, "veg_score": 0},
    },
    {
        "title": "オムライス",
        "region": "日本",
        "description": "日本洋食の代表",
        "ingredients": [
            {"name": "米飯", "quantity": 2, "unit": "杯"},
            {"name": "鶏卵", "quantity": 3, "unit": "個"},
            {"name": "トマトソース", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "トマトソースでご飯を炒める",
            "卵焼きを作ってご飯を包む",
            "トマトソースをかけて装飾",
        ],
        "nutrition": {"kcal": 450, "protein": 16, "fat": 18, "carb": 56, "salt": 1.2, "veg_score": 1},
    },
    # 中国 🇨🇳
    {
        "title": "卵チャーハン",
        "region": "中国",
        "description": "世界で最も有名な中式の簡単料理、ご飯の最適な使い方",
        "ingredients": [
            {"name": "米飯", "quantity": 2, "unit": "杯"},
            {"name": "鶏卵", "quantity": 2, "unit": "個"},
            {"name": "ネギ", "quantity": 2, "unit": "本"},
        ],
        "steps": [
            "卵を混ぜて半熟まで炒めて盛り出す",
            "フライパンの油でご飯を炒める、ネギを加える",
            "卵を加えて素早く混ぜ合わせる",
        ],
        "nutrition": {"kcal": 480, "protein": 14, "fat": 12, "carb": 72, "salt": 1.2, "veg_score": 1},
    },
    {
        "title": "麻婆豆腐",
        "region": "中国",
        "description": "四川の名菜、ピリッとした下飯",
        "ingredients": [
            {"name": "豆腐", "quantity": 400, "unit": "g"},
            {"name": "豚ひき肉", "quantity": 150, "unit": "g"},
            {"name": "辛味噌", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "豆腐をカットして湯通し、水気を切る",
            "ひき肉を炒めて辛味噌を加えて香りを出す",
            "豆腐を加えて軽く混ぜ合わせ、スープを加えて10分煮込む",
        ],
        "nutrition": {"kcal": 320, "protein": 28, "fat": 18, "carb": 12, "salt": 2.0, "veg_score": 1},
    },
    {
        "title": "トマト卵炒め",
        "region": "中国",
        "description": "爽やかな酸味と甘さ、家庭料理の代表",
        "ingredients": [
            {"name": "トマト", "quantity": 2, "unit": "個"},
            {"name": "鶏卵", "quantity": 3, "unit": "個"},
        ],
        "steps": [
            "トマトをカットして卵を混ぜる",
            "卵を半熟まで炒めて盛り出す",
            "トマトを炒めて汁を出す、卵を戻して素早く炒める",
        ],
        "nutrition": {"kcal": 240, "protein": 12, "fat": 14, "carb": 18, "salt": 0.8, "veg_score": 2},
    },
    {
        "title": "宮保鶏丁",
        "region": "中国",
        "description": "甘辛の味わい、世界的に有名",
        "ingredients": [
            {"name": "鶏肉", "quantity": 300, "unit": "g"},
            {"name": "ピーナッツ", "quantity": 100, "unit": "g"},
            {"name": "唐辛子", "quantity": 2, "unit": "個"},
        ],
        "steps": [
            "鶏肉をサイコロ状にカットして炒める",
            "唐辛子とピーナッツを加えて炒める",
            "調味液を加えて素早く混ぜ合わせる",
        ],
        "nutrition": {"kcal": 420, "protein": 32, "fat": 22, "carb": 16, "salt": 1.5, "veg_score": 1},
    },
    {
        "title": "青唐辛子炒め",
        "region": "中国",
        "description": "経典的な快速炒め",
        "ingredients": [
            {"name": "豚肉", "quantity": 250, "unit": "g"},
            {"name": "青唐辛子", "quantity": 2, "unit": "個"},
        ],
        "steps": [
            "肉を千切りにして青唐辛子を千切りにする",
            "肉を素早く炒めて火を通す",
            "青唐辛子を加えて1分炒める",
        ],
        "nutrition": {"kcal": 280, "protein": 28, "fat": 14, "carb": 8, "salt": 1.2, "veg_score": 1},
    },
    {
        "title": "炸酱麺",
        "region": "中国",
        "description": "北方の代表的な麺料理",
        "ingredients": [
            {"name": "麺", "quantity": 300, "unit": "g"},
            {"name": "ひき肉", "quantity": 150, "unit": "g"},
            {"name": "豆板醤", "quantity": 3, "unit": "大さじ"},
        ],
        "steps": [
            "ひき肉を炒めて豆板醤を加える",
            "麺を茹でて水を切る",
            "炸酱をかける",
        ],
        "nutrition": {"kcal": 520, "protein": 22, "fat": 16, "carb": 72, "salt": 1.8, "veg_score": 0},
    },
    {
        "title": "酸辣湯",
        "region": "中国",
        "description": "温かく、食欲増進スープ",
        "ingredients": [
            {"name": "豆腐", "quantity": 200, "unit": "g"},
            {"name": "鶏卵", "quantity": 1, "unit": "個"},
            {"name": "酢", "quantity": 2, "unit": "大さじ"},
            {"name": "唐辛子", "quantity": 1, "unit": "個"},
        ],
        "steps": [
            "出汁を沸騰させて豆腐を加える",
            "卵を流し入れて卵花にする",
            "酢と唐辛子で味付けする",
        ],
        "nutrition": {"kcal": 180, "protein": 14, "fat": 8, "carb": 12, "salt": 1.5, "veg_score": 1},
    },
    {
        "title": "焼き餃子",
        "region": "中国",
        "description": "外側がカリッと、中がジューシーな小食",
        "ingredients": [
            {"name": "餃子の皮", "quantity": 20, "unit": "枚"},
            {"name": "肉詰め", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "詰め物を皮に包む",
            "フライパンの油で焼いて底面が黄金色になるまで",
            "水を加えて蓋をして蒸す、水が乾くまで",
        ],
        "nutrition": {"kcal": 380, "protein": 18, "fat": 12, "carb": 48, "salt": 1.6, "veg_score": 1},
    },
    # 韓国 🇰🇷
    {
        "title": "ビビンバ",
        "region": "韓国",
        "description": "栄養バランスの良い混ぜご飯",
        "ingredients": [
            {"name": "米飯", "quantity": 2, "unit": "杯"},
            {"name": "野菜", "quantity": 200, "unit": "g"},
            {"name": "コチュジャン", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "野菜を細切りにして別々に炒めるか湯通しする",
            "ご飯を丼に盛り、野菜を盛る",
            "コチュジャンを淋らしてよく混ぜ合わせる",
        ],
        "nutrition": {"kcal": 320, "protein": 12, "fat": 6, "carb": 56, "salt": 1.5, "veg_score": 3},
    },
    {
        "title": "部隊鍋",
        "region": "韓国",
        "description": "留学生の味方",
        "ingredients": [
            {"name": "インスタントラーメン", "quantity": 100, "unit": "g"},
            {"name": "ソーセージ", "quantity": 150, "unit": "g"},
            {"name": "キムチ", "quantity": 100, "unit": "g"},
        ],
        "steps": [
            "出汁を沸騰させてソーセージとキムチを加える",
            "ラーメンを加える",
            "麺が柔らかくなるまで煮込む",
        ],
        "nutrition": {"kcal": 380, "protein": 18, "fat": 14, "carb": 48, "salt": 2.2, "veg_score": 0},
    },
    {
        "title": "キムチ炒飯",
        "region": "韓国",
        "description": "辛味が爽やか",
        "ingredients": [
            {"name": "米飯", "quantity": 2, "unit": "杯"},
            {"name": "キムチ", "quantity": 150, "unit": "g"},
            {"name": "鶏卵", "quantity": 1, "unit": "個"},
        ],
        "steps": [
            "キムチを細かく切って汁が出るまで炒める",
            "ご飯を加えて素早く混ぜ合わせる",
            "卵を流し入れてかき混ぜる",
        ],
        "nutrition": {"kcal": 340, "protein": 10, "fat": 8, "carb": 56, "salt": 1.8, "veg_score": 1},
    },
    {
        "title": "辛い年糕炒め",
        "region": "韓国",
        "description": "ストリートフードの名物",
        "ingredients": [
            {"name": "年糕", "quantity": 300, "unit": "g"},
            {"name": "コチュジャン", "quantity": 3, "unit": "大さじ"},
        ],
        "steps": [
            "年糕をお湯で柔らかく",
            "炒めて少し焦げ目がつくまで",
            "コチュジャンを加えて素早く混ぜ合わせる",
        ],
        "nutrition": {"kcal": 280, "protein": 4, "fat": 6, "carb": 56, "salt": 1.6, "veg_score": 0},
    },
    {
        "title": "チヂミ",
        "region": "韓国",
        "description": "外がカリッと中がふんわり",
        "ingredients": [
            {"name": "小麦粉", "quantity": 200, "unit": "g"},
            {"name": "野菜", "quantity": 150, "unit": "g"},
        ],
        "steps": [
            "小麦粉と塩と水で生地を作る",
            "野菜を混ぜる",
            "両面がカリカリになるまで焼く",
        ],
        "nutrition": {"kcal": 260, "protein": 8, "fat": 8, "carb": 40, "salt": 1.2, "veg_score": 2},
    },
    # イタリア 🇮🇹
    {
        "title": "カルボナーラ",
        "region": "イタリア",
        "description": "濃厚な乳香",
        "ingredients": [
            {"name": "パスタ", "quantity": 300, "unit": "g"},
            {"name": "鶏卵", "quantity": 3, "unit": "個"},
            {"name": "ベーコン", "quantity": 100, "unit": "g"},
        ],
        "steps": [
            "ベーコンを細かく切って焼く",
            "パスタをal denteまで茹でる",
            "卵黄をベーコン油と混ぜ、熱いパスタに加える",
        ],
        "nutrition": {"kcal": 520, "protein": 24, "fat": 22, "carb": 58, "salt": 1.4, "veg_score": 0},
    },
    {
        "title": "トマトミートソースパスタ",
        "region": "イタリア",
        "description": "世界で最も普及したパスタ",
        "ingredients": [
            {"name": "パスタ", "quantity": 300, "unit": "g"},
            {"name": "ひき肉", "quantity": 200, "unit": "g"},
            {"name": "トマト", "quantity": 300, "unit": "g"},
        ],
        "steps": [
            "ひき肉を炒めて色が変わるまで",
            "トマトを加えて30分煮込む",
            "パスタを盛ってソースをかける",
        ],
        "nutrition": {"kcal": 480, "protein": 22, "fat": 14, "carb": 62, "salt": 1.3, "veg_score": 1},
    },
    {
        "title": "ニンニクオリーブオイルパスタ",
        "region": "イタリア",
        "description": "シンプルでクラシック",
        "ingredients": [
            {"name": "パスタ", "quantity": 300, "unit": "g"},
            {"name": "ニンニク", "quantity": 4, "unit": "片"},
            {"name": "オリーブオイル", "quantity": 4, "unit": "大さじ"},
        ],
        "steps": [
            "オリーブオイルでニンニクを炒める",
            "パスタをal denteまで茹でて水を切る",
            "オリーブオイルとパスタを混ぜ合わせる",
        ],
        "nutrition": {"kcal": 420, "protein": 14, "fat": 16, "carb": 56, "salt": 0.8, "veg_score": 0},
    },
    {
        "title": "フライパンピザ",
        "region": "イタリア",
        "description": "家庭版ピザ",
        "ingredients": [
            {"name": "ピザ生地", "quantity": 1, "unit": "枚"},
            {"name": "トマトソース", "quantity": 3, "unit": "大さじ"},
            {"name": "チーズ", "quantity": 100, "unit": "g"},
        ],
        "steps": [
            "ピザ生地をフライパンに入れる",
            "トマトソースを塗ってチーズを振りかける",
            "弱火で焼いて底面が黄金色になるまで",
        ],
        "nutrition": {"kcal": 380, "protein": 16, "fat": 14, "carb": 48, "salt": 1.6, "veg_score": 0},
    },
    {
        "title": "イタリアンラタトゥイユ",
        "region": "イタリア",
        "description": "健康的な野菜料理",
        "ingredients": [
            {"name": "ナス", "quantity": 200, "unit": "g"},
            {"name": "トマト", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "野菜をカット",
            "オリーブオイルで焼いて半熟になるまで",
            "トマトを加えて20分煮込む",
        ],
        "nutrition": {"kcal": 180, "protein": 6, "fat": 8, "carb": 24, "salt": 1.0, "veg_score": 3},
    },
    # フランス 🇫🇷
    {
        "title": "ハムチーズクレープ",
        "region": "フランス",
        "description": "フランスのストリートフード",
        "ingredients": [
            {"name": "クレープ生地", "quantity": 200, "unit": "g"},
            {"name": "ハム", "quantity": 100, "unit": "g"},
            {"name": "チーズ", "quantity": 80, "unit": "g"},
        ],
        "steps": [
            "クレープ生地を薄く焼く",
            "ハムとチーズを加える",
            "折り曲げるか巻く",
        ],
        "nutrition": {"kcal": 340, "protein": 18, "fat": 14, "carb": 36, "salt": 1.5, "veg_score": 0},
    },
    {
        "title": "フレンチオムレツ",
        "region": "フランス",
        "description": "なめらかな食感",
        "ingredients": [
            {"name": "鶏卵", "quantity": 3, "unit": "個"},
            {"name": "バター", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "卵液を混ぜる",
            "バターを融かして卵液を注ぐ",
            "弱火で絶えずかき混ぜて濃厚になるまで",
        ],
        "nutrition": {"kcal": 240, "protein": 16, "fat": 18, "carb": 2, "salt": 0.6, "veg_score": 0},
    },
    {
        "title": "玉ねぎスープ",
        "region": "フランス",
        "description": "経典的なスープ",
        "ingredients": [
            {"name": "玉ねぎ", "quantity": 500, "unit": "g"},
            {"name": "パン", "quantity": 2, "unit": "枚"},
        ],
        "steps": [
            "玉ねぎを細切りにして焦げ目がつくまで炒める",
            "出汁を加えて30分煮込む",
            "丼に盛ってパンとチーズを加える",
        ],
        "nutrition": {"kcal": 200, "protein": 8, "fat": 6, "carb": 28, "salt": 1.4, "veg_score": 1},
    },
    {
        "title": "クリームキノコチキン",
        "region": "フランス",
        "description": "濃厚なフレンチ風味",
        "ingredients": [
            {"name": "鶏肉", "quantity": 400, "unit": "g"},
            {"name": "キノコ", "quantity": 200, "unit": "g"},
            {"name": "生クリーム", "quantity": 200, "unit": "ml"},
        ],
        "steps": [
            "鶏肉を焼いて半熟になるまで盛り出す",
            "キノコを炒めて汁が出るまで",
            "生クリームと鶏肉を加えて20分煮込む",
        ],
        "nutrition": {"kcal": 420, "protein": 36, "fat": 24, "carb": 8, "salt": 1.2, "veg_score": 1},
    },
    # スペイン 🇪🇸
    {
        "title": "ニンニクエビ",
        "region": "スペイン",
        "description": "酒のつまみの名菜",
        "ingredients": [
            {"name": "エビ", "quantity": 300, "unit": "g"},
            {"name": "ニンニク", "quantity": 6, "unit": "片"},
            {"name": "オリーブオイル", "quantity": 3, "unit": "大さじ"},
        ],
        "steps": [
            "ニンニクを切る",
            "オリーブオイルでニンニクを炒める",
            "エビを加えて素早く炒める",
        ],
        "nutrition": {"kcal": 280, "protein": 32, "fat": 12, "carb": 4, "salt": 1.3, "veg_score": 0},
    },
    {
        "title": "スペイン式オムレツ",
        "region": "スペイン",
        "description": "国民料理",
        "ingredients": [
            {"name": "鶏卵", "quantity": 4, "unit": "個"},
            {"name": "ジャガイモ", "quantity": 300, "unit": "g"},
        ],
        "steps": [
            "ジャガイモを薄くスライスして半熟になるまで煮込む",
            "卵液とジャガイモを混ぜる",
            "両面がカリカリになるまで焼く",
        ],
        "nutrition": {"kcal": 320, "protein": 14, "fat": 14, "carb": 36, "salt": 1.0, "veg_score": 0},
    },
    {
        "title": "簡易シーフードライス",
        "region": "スペイン",
        "description": "家庭版パエリア",
        "ingredients": [
            {"name": "米", "quantity": 300, "unit": "g"},
            {"name": "冷凍シーフード", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "米を炒めて少し透明になるまで",
            "出汁とシーフードを加える",
            "中火で米が熟するまで煮込む",
        ],
        "nutrition": {"kcal": 420, "protein": 28, "fat": 8, "carb": 56, "salt": 1.6, "veg_score": 0},
    },
    # メキシコ 🇲🇽
    {
        "title": "タコス",
        "region": "メキシコ",
        "description": "どう包んでも美味しい",
        "ingredients": [
            {"name": "トルティーヤ", "quantity": 6, "unit": "枚"},
            {"name": "肉", "quantity": 250, "unit": "g"},
            {"name": "野菜", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "肉を炒めて調味する",
            "野菜を細切りにする",
            "肉と野菜をトルティーヤに包む",
        ],
        "nutrition": {"kcal": 380, "protein": 20, "fat": 12, "carb": 48, "salt": 1.8, "veg_score": 1},
    },
    {
        "title": "メキシコンチキンロール",
        "region": "メキシコ",
        "description": "巻いて食べる主食",
        "ingredients": [
            {"name": "鶏肉", "quantity": 300, "unit": "g"},
            {"name": "トルティーヤ", "quantity": 4, "unit": "枚"},
        ],
        "steps": [
            "鶏肉を炒めて完全に火を通す",
            "トルティーヤを広げて鶏肉を乗せる",
            "巻く",
        ],
        "nutrition": {"kcal": 340, "protein": 28, "fat": 10, "carb": 40, "salt": 1.2, "veg_score": 0},
    },
    {
        "title": "メキシコンビーフライス",
        "region": "メキシコ",
        "description": "重い味のどんぶり",
        "ingredients": [
            {"name": "牛肉", "quantity": 300, "unit": "g"},
            {"name": "米", "quantity": 2, "unit": "杯"},
            {"name": "スパイス", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "牛肉を炒めて色が変わるまで",
            "スパイスを加えて香りを出す",
            "ご飯に盛る",
        ],
        "nutrition": {"kcal": 520, "protein": 32, "fat": 18, "carb": 56, "salt": 1.6, "veg_score": 0},
    },
    {
        "title": "スパイシーコーンサラダ",
        "region": "メキシコ",
        "description": "爽やかな付け合わせ",
        "ingredients": [
            {"name": "トウモロコシ", "quantity": 200, "unit": "g"},
            {"name": "コチュジャン", "quantity": 1, "unit": "大さじ"},
        ],
        "steps": [
            "トウモロコシを茹でて水を切る",
            "コチュジャンと混ぜる",
            "冷蔵後に食べる",
        ],
        "nutrition": {"kcal": 160, "protein": 4, "fat": 4, "carb": 28, "salt": 1.0, "veg_score": 1},
    },
    # アメリカ 🇺🇸
    {
        "title": "ハンバーガー",
        "region": "アメリカ",
        "description": "アメリカンスタイル",
        "ingredients": [
            {"name": "牛肉", "quantity": 200, "unit": "g"},
            {"name": "パン", "quantity": 2, "unit": "枚"},
        ],
        "steps": [
            "牛肉でハンバーグを作る",
            "両面がカリカリになるまで焼く",
            "パンに挟む",
        ],
        "nutrition": {"kcal": 480, "protein": 28, "fat": 20, "carb": 40, "salt": 1.4, "veg_score": 0},
    },
    {
        "title": "フライドチキン",
        "region": "アメリカ",
        "description": "外がカリッと中がジューシー",
        "ingredients": [
            {"name": "鶏肉", "quantity": 400, "unit": "g"},
            {"name": "小麦粉", "quantity": 150, "unit": "g"},
        ],
        "steps": [
            "鶏肉をカット",
            "小麦粉をつけて揚げる",
            "油を切る",
        ],
        "nutrition": {"kcal": 520, "protein": 36, "fat": 26, "carb": 24, "salt": 1.3, "veg_score": 0},
    },
    {
        "title": "チーズマカロニ",
        "region": "アメリカ",
        "description": "学生の最愛",
        "ingredients": [
            {"name": "マカロニ", "quantity": 300, "unit": "g"},
            {"name": "チーズ", "quantity": 200, "unit": "g"},
        ],
        "steps": [
            "マカロニをal denteまで茹でる",
            "バターと牛乳でチーズを融かす",
            "マカロニと混ぜ合わせる",
        ],
        "nutrition": {"kcal": 520, "protein": 18, "fat": 20, "carb": 64, "salt": 1.2, "veg_score": 0},
    },
    {
        "title": "簡易焼きリブ",
        "region": "アメリカ",
        "description": "家庭版バーベキュー",
        "ingredients": [
            {"name": "豚肋骨", "quantity": 600, "unit": "g"},
            {"name": "ソース", "quantity": 4, "unit": "大さじ"},
        ],
        "steps": [
            "肋骨にソースをコーティング",
            "200度のオーブンで30分焼く",
            "反転して火が通るまで焼く",
        ],
        "nutrition": {"kcal": 580, "protein": 40, "fat": 36, "carb": 12, "salt": 1.8, "veg_score": 0},
    },
    # タイ 🇹🇭
    {
        "title": "バジル豚挽き肉",
        "region": "タイ",
        "description": "タイ国民菜",
        "ingredients": [
            {"name": "豚ひき肉", "quantity": 300, "unit": "g"},
            {"name": "バジル", "quantity": 20, "unit": "g"},
        ],
        "steps": [
            "豚ひき肉を炒めて完全に火を通す",
            "バジルの葉を加えて素早く炒めて香りを出す",
            "ご飯に盛る",
        ],
        "nutrition": {"kcal": 320, "protein": 28, "fat": 14, "carb": 24, "salt": 1.5, "veg_score": 1},
    },
    {
        "title": "トムヤムスープ",
        "region": "タイ",
        "description": "酸辣のスープ代表",
        "ingredients": [
            {"name": "エビ", "quantity": 250, "unit": "g"},
            {"name": "スープ素", "quantity": 1, "unit": "パック"},
        ],
        "steps": [
            "出汁を沸騰させてスープ素を加える",
            "エビを加えて色が変わるまで",
            "味付けする",
        ],
        "nutrition": {"kcal": 240, "protein": 24, "fat": 6, "carb": 12, "salt": 2.0, "veg_score": 1},
    },
    {
        "title": "タイ風炒飯",
        "region": "タイ",
        "description": "香り高い",
        "ingredients": [
            {"name": "米飯", "quantity": 2, "unit": "杯"},
            {"name": "鶏卵", "quantity": 1, "unit": "個"},
            {"name": "スパイス", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "卵を半熟まで炒めて盛り出す",
            "米飯を素早く炒めてスパイスを加える",
            "卵を戻して混ぜ合わせる",
        ],
        "nutrition": {"kcal": 420, "protein": 14, "fat": 12, "carb": 64, "salt": 1.4, "veg_score": 1},
    },
    {
        "title": "グリーンカレー",
        "region": "タイ",
        "description": "ココナッツの香りが辛い",
        "ingredients": [
            {"name": "カレーペースト", "quantity": 3, "unit": "大さじ"},
            {"name": "鶏肉", "quantity": 300, "unit": "g"},
        ],
        "steps": [
            "カレーペーストを香りが出るまで炒める",
            "鶏肉を加えて炒める",
            "ココナッツミルクを加えて20分煮込む",
        ],
        "nutrition": {"kcal": 380, "protein": 28, "fat": 18, "carb": 24, "salt": 1.6, "veg_score": 1},
    },
    # その他の国
    {
        "title": "ベトナム焼きそば",
        "region": "ベトナム",
        "description": "爽やかな快速炒め",
        "ingredients": [
            {"name": "焼きそば麺", "quantity": 300, "unit": "g"},
            {"name": "鶏卵", "quantity": 2, "unit": "個"},
            {"name": "豆もやし", "quantity": 100, "unit": "g"},
        ],
        "steps": [
            "卵を半熟まで炒めて盛り出す",
            "焼きそば麺を炒めてほぐす",
            "豆もやしと卵を加えて素早く混ぜ合わせる",
        ],
        "nutrition": {"kcal": 360, "protein": 14, "fat": 10, "carb": 52, "salt": 1.2, "veg_score": 1},
    },
    {
        "title": "海南鶏飯",
        "region": "シンガポール/マレーシア",
        "description": "一鍋で完成",
        "ingredients": [
            {"name": "鶏腿", "quantity": 500, "unit": "g"},
            {"name": "米", "quantity": 2, "unit": "杯"},
        ],
        "steps": [
            "鶏腿を出汁で煮込む",
            "鶏のスープで米を炊く",
            "鶏肉を切ってご飯に盛る",
        ],
        "nutrition": {"kcal": 480, "protein": 36, "fat": 16, "carb": 48, "salt": 1.4, "veg_score": 0},
    },
    {
        "title": "シンガポール炒米粉",
        "region": "シンガポール",
        "description": "カレーの風味",
        "ingredients": [
            {"name": "米粉", "quantity": 300, "unit": "g"},
            {"name": "カレー粉", "quantity": 2, "unit": "大さじ"},
        ],
        "steps": [
            "カレー粉を香りが出るまで炒める",
            "米粉をほぐしてカレー粉と混ぜる",
            "素早く炒める",
        ],
        "nutrition": {"kcal": 380, "protein": 12, "fat": 12, "carb": 56, "salt": 1.3, "veg_score": 0},
    },
    {
        "title": "インドバターチキン",
        "region": "インド",
        "description": "甘い香りのカレー",
        "ingredients": [
            {"name": "鶏肉", "quantity": 400, "unit": "g"},
            {"name": "カレーキューブ", "quantity": 2, "unit": "個"},
        ],
        "steps": [
            "鶏肉を炒めて半熟になるまで盛り出す",
            "カレーキューブをバターで融かす",
            "鶏肉を戻して20分煮込む",
        ],
        "nutrition": {"kcal": 420, "protein": 32, "fat": 20, "carb": 18, "salt": 1.4, "veg_score": 0},
    },
    {
        "title": "ドイツソーセージ＆ジャガイモ",
        "region": "ドイツ",
        "description": "ドイツ家庭料理",
        "ingredients": [
            {"name": "ソーセージ", "quantity": 300, "unit": "g"},
            {"name": "ジャガイモ", "quantity": 400, "unit": "g"},
        ],
        "steps": [
            "ジャガイモを茹でてカット",
            "ソーセージを焼いて両面がカリカリ",
            "混ぜ合わせる",
        ],
        "nutrition": {"kcal": 420, "protein": 22, "fat": 18, "carb": 40, "salt": 1.6, "veg_score": 0},
    },
]
