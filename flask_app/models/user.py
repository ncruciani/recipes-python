from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt
import re


db = "recipes"
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])


    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])


    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['email']) < 1:
            flash('you need to put an email in silly', 'register')
            is_valid = False
        elif not email_regex.match(form_data['email']):
            flash('Invalid email address.', 'register')
            is_valid = False
        elif User.get_by_email(form_data):
            flash('someone already has this email silly goose pick another one.', 'register')
            is_valid = False
        if len(form_data['password']) < 8:
            flash('Password must be at least 8 characters long.', 'register')
            is_valid = False
        if form_data['password'] != form_data['confirm_password']:
            flash('Passwords have to be the same', 'register')
            is_valid = False
        if len(form_data['first_name']) < 3:
            flash('First name must be at least 3 characters long.', 'register')
            is_valid = False
        if len(form_data['last_name']) < 3:
            flash('Last name must be at least 3 characters long.', 'register')
            is_valid = False
        return is_valid


    @staticmethod
    def validate_login(form_data):
        if not email_regex.match(form_data['email']):
            flash('Invalid email/password.', 'login')
            return False
        user = User.get_by_email(form_data)
        if not user:
            flash('Invalid email/password.', 'login')
            return False
        if not bcrypt.check_password_hash(user.password, form_data['password']):
            flash('Invalid email/password.', 'login')
            return False
        return user
    

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(db).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users