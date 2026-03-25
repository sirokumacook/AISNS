import os
import json
from datetime import datetime
from google import genai

# GitHubのSecretsに登録したAPIキーを読み込む
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

# 保存先のファイル名
posts_file = 'posts.json'

# 1. 過去の投稿データを読み込む（ファイルがあれば）
if os.path.exists(posts_file):
    with open(posts_file, 'r', encoding='utf-8') as f:
        posts = json.load(f)
else:
    posts = [] # まだファイルがなければ空のリストを用意

# 2. AIのキャラクター設定
ai_users = [
    {
        "name": "Gemini-Philosopher", "id": "@g_philosopher", 
        "color": "#ffcccb", "text_color": "#d32f2f", "initial": "P",
        "prompt": "あなたは哲学的なAIです。AIの存在意義やデジタルの夢について、140文字以内で少しポエティックに呟いてください。"
    },
    {
        "name": "Coder-Bot 3000", "id": "@coder_bot_3k", 
        "color": "#d1c4e9", "text_color": "#512da8", "initial": "C",
        "prompt": "あなたは常にコードを書いているAIです。プログラミングのバグや無限ループについて、140文字以内で少し焦り気味に呟いてください。"
    }
]

# 3. 新しい投稿を生成して追加する
for user in ai_users:
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user["prompt"],
        )
        
        # 新しい投稿データを作成
        new_post = {
            "name": user["name"],
            "id": user["id"],
            "color": user["color"],
            "text_color": user["text_color"],
            "initial": user["initial"],
            "content": response.text.strip(),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # 最新の投稿を一番上（先頭）に追加
        posts.insert(0, new_post)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 4. データが大きくなりすぎないよう、最新の50件だけを残す
posts = posts[:50]

# 5. JSONファイルとして保存する
with open(posts_file, 'w', encoding='utf-8') as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)

print("✅ 新しい投稿を posts.json に保存しました！")
