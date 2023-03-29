from flask_app.models.user import User
from flask import render_template, redirect, request, session
from flask_app import app

@app.route("/create_user")
def create_form():
    return render_template("create.html")

@app.route("/users")
def display_users():
    users = User.get_all()
    return render_template("read.html", all_users = users)

@app.route("/new_user", methods = ["POST"])
def create_user():
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }

    if not User.validate_user(data):
        session["fname"] = data["fname"]
        session["lname"] = data["lname"]
        session["email"] = data["email"]
        return redirect("/create_user")


    User.create_user(data)
    users = User.get_all()
    uid = users[len(users)-1].id
    session.clear()
    return redirect(f"/users/{uid}")

@app.route("/users/<uid>")
def info(uid):
    user = User.get_one(uid)
    print(user)
    return render_template("info.html", user = user)

@app.route("/users/<uid>/edit")
def edit(uid):
    user = User.get_one(uid)
    return render_template("edit.html", user = user)

@app.route("/users/<uid>/edit/submit", methods = ["POST"])
def update_user(uid):
    data = {
        "fname_new": request.form["fname_new"],
        "lname_new": request.form["lname_new"],
        "email_new": request.form["email_new"],
        "id": uid
    }
    User.update_user(data)
    return redirect(f"/users/{uid}")

@app.route("/users/<uid>/destroy")
def destroy_user(uid):
    User.delete(uid)
    return redirect("/users")