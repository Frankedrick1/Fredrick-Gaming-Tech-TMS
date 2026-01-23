from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for login sessions

# TEMP user (later we can use database)
USERS = {
    "admin": "admin123"
}

timesheets = []

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        timesheets.append({
            "employee": request.form["employee"],
            "task": request.form["task"],
            "hours": request.form["hours"]
        })
        return redirect(url_for("index"))

    return render_template("index.html", timesheets=timesheets, user=session["user"])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
)
