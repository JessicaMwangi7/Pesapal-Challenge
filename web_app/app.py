# web_app/app.py

from flask import Flask, render_template, request, redirect
import sys
sys.path.append("..")

from rdbms import Database

app = Flask(__name__)
db = Database()

# Define users table with types as strings to match rdbms.py
db.create_table(
    "users",
    {"id": "int", "name": "str", "email": "str"},
    primary_key="id",
    unique_keys=["email"]
)

@app.route("/")
def index():
    users = db.get_table("users").select()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    data = {
        "id": request.form["id"],
        "name": request.form["name"],
        "email": request.form["email"]
    }
    try:
        db.get_table("users").insert(data)
    except ValueError as e:
        print(f"Error: {e}")
    return redirect("/")

@app.route("/update", methods=["POST"])
def update_user():
    criteria = {"id": request.form["id"]}
    updates = {"name": request.form["name"], "email": request.form["email"]}
    try:
        count = db.get_table("users").update(criteria, updates)
        print(f"{count} row(s) updated.")
    except ValueError as e:
        print(f"Error: {e}")
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_user():
    criteria = {"id": request.form["id"]}
    try:
        count = db.get_table("users").delete(criteria)
        print(f"{count} row(s) deleted.")
    except ValueError as e:
        print(f"Error: {e}")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
