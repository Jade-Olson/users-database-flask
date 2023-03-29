from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("users_cr").query_db(query)
        users = []
        for one_user in results:
            users.append(cls(one_user))
        return users
    @classmethod
    def create_user(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES (%(fname)s, %(lname)s, %(email)s, NOW(), NOW())"
        return connectToMySQL("users_cr").query_db(query, data)
    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name = %(fname_new)s, last_name = %(lname_new)s, email = %(email_new)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL("users_cr").query_db(query, data)
    @classmethod
    def get_one(cls, id):
        data = {"id": id}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL("users_cr").query_db(query, data)
        return result
    @classmethod
    def delete(cls, id):
        data = {"id": id}
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL("users_cr").query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["fname"]) < 1:
            flash("First Name is required.")
            is_valid = False
        if len(user["lname"]) < 1:
            flash("Last Name is required.")
            is_valid = False
        if len(user["email"]) < 1:
            flash("Email is required.")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email Format.")
            is_valid = False
        return is_valid
