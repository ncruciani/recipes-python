from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User
from datetime import datetime
db = "recipes"

class Recipe:
    def __init__(self, data):
        self.id =data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = User.get_by_id({'id': data['user_id']})


    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under30, user_id ) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result
    

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under30=%(under30)s WHERE id = %(id)s;"
        connectToMySQL(db).query_db(query, data)
        return



    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            recipe_data = {
                'id': row['id'],
                'name': row['name'],
                'description': row['description'],
                'instructions': row['instructions'],
                'date_made': row['date_made'],
                'under30': row['under30'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
                'user_id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password']
            }
            recipe = Recipe(recipe_data)
            recipes.append(recipe)
        return recipes


    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    


    @staticmethod
    def validate_recipe(form_data):
        errors = []
        if len(form_data['name']) < 1:
            errors.append('Name is required.')
        if len(form_data['description']) < 1:
            errors.append('Description is required.')
        if len(form_data['instructions']) < 1:
            errors.append('Instructions are required.')
        if len(form_data['date_made']) < 1:
            errors.append('Date Made is required.')
        if 'under30' not in form_data:
            errors.append('Please specify if this can be made in under 30 minutes.')
        return errors

