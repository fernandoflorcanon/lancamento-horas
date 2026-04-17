print("🔥 SERVER COM SUPABASE API 🔥")

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# ===== CONFIG SUPABASE =====
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ===== HOME =====
@app.route('/')
def home():
    with open("LancamentoHoras.html", "r", encoding="utf-8") as f:
        return f.read()

# ===== SAVE =====
@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.get_json()

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/lancamentos",
            json={
                "date": data.get("date"),
                "employee": data.get("employee"),
                "serial": data.get("serial"),
                "model": data.get("model"),
                "activity": data.get("activity"),
                "initialhour": data.get("initialHour"),
                "finalhour": data.get("finalHour"),
                "duration": data.get("duration"),
                "note": data.get("note")
            },
            headers=HEADERS
        )

        return jsonify({"ok": True, "status": response.status_code})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ===== LOAD =====
@app.route('/load')
def load():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/lancamentos?order=id.desc",
            headers=HEADERS
        )

        data = response.json()

        return jsonify(data)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# ===== HEALTH =====
@app.route('/health')
def health():
    return jsonify({'status': 'running'})

# ===== RUN =====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5500))
    app.run(host='0.0.0.0', port=port)
