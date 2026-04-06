from flask import Flask, request, jsonify, render_template
from markupsafe import escape
import sqlite3
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")


def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    return "Flask app de test OK"


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = get_db()
    cur = conn.cursor()

    # parametrizat, nu string concatenation
    cur.execute("SELECT id, name FROM users WHERE name LIKE ?", (f"%{q}%",))
    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(r) for r in rows])


@app.route("/profile/<username>")
def profile(username):
    # escape output
    safe_username = escape(username)
    return render_template('profile.html', username=safe_username)


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?",
        (username, password),
    )
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401


if __name__ == "__main__":
    # debug=False pentru rulare normală
    app.run(host="127.0.0.1", port=5000, debug=False)
