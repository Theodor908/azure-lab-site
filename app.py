import os, socket, datetime
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return f"""
    <h1>Azure Lab - Theodor</h1>
    <p>Host: {socket.gethostname()}</p>
    <p>Region: {os.environ.get('REGION_NAME', 'n/a')}</p>
    <p>UTC: {datetime.datetime.utcnow():%Y-%m-%d %H:%M:%S}</p>
    <p><a href="/health">/health</a> | <a href="/secret">/secret</a> | <a href="/db">/db</a></p>
    """

@app.route("/health")
def health():
    return jsonify(status="ok")

@app.route("/secret")
def secret():
    pw = os.environ.get("DB_PASSWORD", "")
    return f"DB_PASSWORD din Key Vault: {'setat, ' + str(len(pw)) + ' caractere' if pw else 'lipsa'}"

@app.route("/db")
def db():
    try:
        import pymssql
        conn = pymssql.connect(server=os.environ["DB_SERVER"], user=os.environ["DB_USER"],
                               password=os.environ["DB_PASSWORD"], database=os.environ["DB_NAME"],
                               tds_version="7.4")
        cur = conn.cursor()
        cur.execute("SELECT id, text FROM notes")
        rows = cur.fetchall()
        return "<br>".join(f"{r[0]}: {r[1]}" for r in rows) or "tabela goala"
    except Exception as e:
        return f"eroare: {e}", 500