import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
inventory = []

# API設定
EDAMAM_APP_ID = "1ac89caf"
EDAMAM_APP_KEY = "49c335aae9f6894d4ad1ea013fad590c"

TRANSLATION_MAP = {
    "鶏肉": "chicken", "たまご": "egg", "卵": "egg", "玉ねぎ": "onion", 
    "豚肉": "pork", "牛肉": "beef", "トマト": "tomato", "にんじん": "carrot",
    "じゃがいも": "potato", "牛乳": "milk", "キャベツ": "cabbage"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/add_item', methods=['POST'])
def add_item():
    data = request.json
    inventory.append(data)
    return jsonify({"status": "success", "inventory": inventory})

@app.route('/api/get_recipes', methods=['GET'])
def get_recipes():
    if not inventory:
        return jsonify({"recipes": []})

    inventory.sort(key=lambda x: x['expiry'])
    top_items = [item['name'] for item in inventory[:3]]
    search_query = ",".join([TRANSLATION_MAP.get(name, name) for name in top_items])
    
    url = "https://api.edamam.com/api/recipes/v2"
    params = {
        "type": "public",
        "q": search_query,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        recipes = []
        if "hits" in data:
            for hit in data['hits'][:5]:
                r = hit['recipe']
                recipes.append({
                    "label": r['label'], 
                    "url": r['url'], 
                    "image": r['image']
                })
        # コンソールで確認用
        print(f"DEBUG: Found {len(recipes)} recipes for {search_query}")
        return jsonify({"recipes": recipes})
    except Exception as e:
        return jsonify({"recipes": [], "error": str(e)})

if __name__ == '__main__':
    # ポート5001番で実行
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host="0.0.0.0", port=port)