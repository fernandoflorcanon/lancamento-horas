print("🔥🔥🔥 SERVER COM SQLITE 🔥🔥🔥")

from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
import os
import sys
import sqlite3

# ===== PATHS =====
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = BASE_PATH
HTML_FILE = "LancamentoHoras.html"

app = Flask(__name__)
CORS(app)

# ===== BANCO (AGORA PADRÃO PARA LOCAL E RENDER) =====
DB_PATH = os.path.join(BASE_PATH, "lancamentos.db")

# ===== INICIALIZA BANCO =====
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        employee TEXT,
        serial TEXT,
        model TEXT,
        activity TEXT,
        initialHour TEXT,
        finalHour TEXT,
        duration TEXT,
        note TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ===== SERVIR HTML =====
@app.route('/')
def home():
    path = os.path.join(HTML_DIR, HTML_FILE)
    if not os.path.exists(path):
        return f"ERRO: Arquivo nao encontrado: {path}", 500
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# ===== SALVAR =====
@app.route('/save', methods=['POST'])
def save():
    data = request.get_json(silent=True) or {}

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO records (
        date, employee, serial, model, activity,
        initialHour, finalHour, duration, note
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    conn.close()

    return jsonify({'ok': True})

# ===== CARREGAR =====
@app.route('/load')
def load():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT date, employee, serial, model, activity,
           initialHour, finalHour, duration, note
    FROM records
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    records = []

    for r in rows:
        records.append({
            "date": r[0],
            "employee": r[1],
            "serial": r[2],
            "model": r[3],
            "activity": r[4],
            "initialHour": r[5],
            "finalHour": r[6],
            "duration": r[7],
            "note": r[8]
        })

    return jsonify(records)

# ===== HEALTH =====
@app.route('/health')
def health():
    return jsonify({'status': 'running'})

# ===== RUN =====
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5500))

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            pass

    print(f"🔥 Rodando na porta {port}")
    app.run(host='0.0.0.0', port=port)
