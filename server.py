print("🔥 SERVER COM POSTGRES 🔥")

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import psycopg

# ===== CONFIG =====
DATABASE_URL = os.getenv("DATABASE_URL")

import socket
import psycopg

# força IPv4
orig_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4(*args, **kwargs):
    return [res for res in orig_getaddrinfo(*args, **kwargs) if res[0] == socket.AF_INET]

socket.getaddrinfo = getaddrinfo_ipv4

app = Flask(__name__)
CORS(app)

# ===== SERVIR HTML =====
@app.route('/')
def home():
    with open("LancamentoHoras.html", "r", encoding="utf-8") as f:
        return f.read()

# ===== SALVAR =====
@app.route('/save', methods=['POST'])
def save():
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

# ===== CARREGAR =====
@app.route('/load')
def load():
    conn = psycopg.connect(DATABASE_URL)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, employee, serial, model, activity,
               initialhour, finalhour, duration, note
        FROM lancamentos
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
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
    print(f"🔥 Rodando na porta {port}")
    app.run(host='0.0.0.0', port=port)
