
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

timesheets = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        timesheets.append({
            "employee": request.form["employee"],
            "hours": request.form["hours"],
            "task": request.form["task"]
        })
        return redirect(url_for("index"))
    return render_template("index.html", timesheets=timesheets)

if __name__ == "__main__":
    app.run(debug=True)
