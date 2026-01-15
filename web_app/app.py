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
    {"id": "int", "name": "str", "category": "str", "email": "str"},
    primary_key="id",
    unique_keys=["email"]
)

@app.route("/")
def index():
    users = db.get_table("users").select()
    return render_template("index.html", users=users)

@app.route("/add", methods=["POST"])
def add_user():
    user = {
        "id": int(request.form.get("id")),
        "name": request.form.get("name"),
        "category": request.form.get("category", ""),  # <-- CATEGORY/ROLE
        "email": request.form.get("email")
    }

    try:
        db.get_table("users").insert(user)  # use get_table().insert()
    except ValueError as e:
        print(f"Error: {e}")

    return redirect("/")


@app.route("/update", methods=["POST"])
def update_user():
    criteria = {"id": request.form.get("id")}
    updates = {
        "name": request.form.get("name"),
        "category": request.form.get("category", ""),  # use .get with default
        "email": request.form.get("email")
    }
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
