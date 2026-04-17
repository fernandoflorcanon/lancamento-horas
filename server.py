print("🔥 SERVER COM POSTGRES 🔥")

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg
import socket

# ===== CONFIG =====
DATABASE_URL = os.getenv("DATABASE_URL")

# ===== FORÇA IPv4 (IMPORTANTE PARA RENDER) =====
orig_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4(*args, **kwargs):
    return [res for res in orig_getaddrinfo(*args, **kwargs) if res[0] == socket.AF_INET]

socket.getaddrinfo = getaddrinfo_ipv4

app = Flask(__name__)
CORS(app)

# ===== SERVIR HTML =====
@app.route('/')
def home():
    try:
        with open("LancamentoHoras.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Erro ao abrir HTML: {str(e)}", 500

# ===== SALVAR =====
@app.route('/save', methods=['POST'])
def save():
    try:
        data = request.get_json(silent=True) or {}

        conn = psycopg.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO lancamentos (
                date, employee, serial, model, activity,
                initialhour, finalhour, duration, note
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('date',''),
            data.get('employee',''),
            data.get('serial',''),
            data.get('model',''),
            data.get('activity',''),
            data.get('initialHour',''),
            data.get('finalHour',''),
            data.get('duration',''),
            data.get('note','')
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'ok': True})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ===== CARREGAR (TESTE DE CONEXÃO) =====
@app.route('/load')
def load():
    try:
        conn = psycopg.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return {"status": "ok", "db": result}

    except Exception as e:
        return {"erro": str(e)}, 500


# ===== HEALTH =====
@app.route('/health')
def health():
    return jsonify({'status': 'running'})


# ===== RUN =====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5500))
    print(f"🔥 Rodando na porta {port}")
    app.run(host='0.0.0.0', port=port)
