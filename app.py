from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

DB_NAME = "database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS timesheets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee TEXT,
        task TEXT,
        hours INTEGER
    )
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('Fredrick', 'fred1236', 'admin')
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            conn = get_db()
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, 'employee')",
                (username, password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username already exists")

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db()

    if request.method == "POST" and session["role"] == "employee":
        conn.execute(
            "INSERT INTO timesheets (employee, task, hours) VALUES (?, ?, ?)",
            (session["user"], request.form["task"], request.form["hours"])
        )
        conn.commit()

    timesheets = conn.execute("SELECT * FROM timesheets").fetchall()

    users = []
    if session["role"] == "admin":
        users = conn.execute(
            "SELECT id, username FROM users WHERE role='employee'"
        ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        timesheets=timesheets,
        users=users,
        user=session["user"],
        role=session["role"]
    )

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    if "user" not in session or session["role"] != "admin":
        return redirect(url_for("login"))

    conn = get_db()
    conn.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
