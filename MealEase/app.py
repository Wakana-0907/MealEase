import os
from flask import Flask, render_template, request, jsonify
# ここに必要なライブラリ（requestsなど）があれば適宜追加する

app = Flask(__name__)

# --- ここに既存のルート（@app.route）をすべて記述 ---

@app.route('/')
def index():
    # 既存のメイン画面を表示するコード
    return render_template('index.html')

# 音声入力やレシピ生成のAPIルートもここにそのまま残す
# 例: @app.route('/api/recipe', methods=['POST']) など

# --- デプロイ用の設定 ---

if __name__ == "__main__":
    # Renderなどのクラウドサービスでは環境変数「PORT」が指定
    # 指定がない場合はローカルテスト用に 5000 番を使用
    port = int(os.environ.get("PORT", 5000))
    
    # host="0.0.0.0" にすることで、ネットワーク外からのアクセスを許可

    app.run(host="0.0.0.0", port=port, debug=False)