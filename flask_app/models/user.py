from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import  flash, session, request
from flask_bcrypt import Bcrypt        
from flask_app.models.sighting import Sighting

import re

bcrypt= Bcrypt(app)   

class User:
    db = 'websighting_schema'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.reported_sightings = []


#create

    @classmethod
    def create_user(cls, data):
        if not cls.validate_user_regis(data):
            return False
        parsed_data= cls.parse_user_data(data)
        print('Z'*50)
        print(parsed_data)
        query="""
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,parsed_data)
        print('User created with id of',user_id)
        session['user_id'] = user_id
        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        return user_id

#read
    
    @classmethod
    def get_user_by_email(cls,email):
        data = {'email':email}
        query="""
        SELECT * FROM users
        WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        print('X'*50)
        print(results)
        if len(results) < 1:
            flash('***User not registered***')
            return
        user = User(results[0])
        return user

    @classmethod
    def get_one_user(cls, data):
        query="""
        SELECT * FROM users
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if len(result) < 1:
            return False
        user = cls(result[0])
        return user

    @classmethod
    def get_one_user_sighting(cls, data):
        query= """
        SELECT * FROM users
        LEFT JOIN authors
        ON users.id = authors.user_id
        LEFT JOIN sightings
        ON sightings.id = authors.sighting_id
        WHERE users.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        user = cls(results[0])
        print('k'*50)
        print(user)
        for row in results:
            if row['sightings.id'] == None:
                break
            data = {
                'id': row['sightings.id'],
                'location': row['location'],
                'description': row['description'],
                'description': row['number_of'],
                'description': row['when'],
                'user_id':row['user.id'],
                'created_at': row['sightings.created_at'],
                'updated_at': row['sightings.updated_at']
            }
            user.reported_sightings.append(data)
        return user
#update

    @classmethod
    def be_skeptic(cls,data):
        query="""
        INSERT INTO skeptics (user_id,sighting_id)
        VALUES (%(user_id)s,%(sighting_id)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query,data)

#delete
# validate
    @staticmethod
    def validate_user_regis(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX=re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")        
        is_valid=True
        if len(data['first_name']) < 2:
            is_valid=False
            flash("First name needs to be longer than 2 characters")
        if len(data['last_name']) < 2:
            is_valid=False
            flash("Last name needs to be longer than 2 characters")
        if User.get_user_by_email(data['email']):
            is_valid=False
            flash('Email has already been registered')
        if not EMAIL_REGEX.match(data['email']):
            is_valid=False
            flash("Invalid Email")
        if not PASSWORD_REGEX.match(data['password']):
            is_valid=False
            flash("Password needs to contain at least 8 characters, one number and one uppercase letter.")
        if data['password'] != data['check']:
            is_valid=False
            flash("Passwords do not match")
        return is_valid

    @staticmethod
    def parse_user_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email']
        parsed_data['password']= bcrypt.generate_password_hash(data['password'])
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            print(this_user.first_name)
            if this_user:
                if bcrypt.check_password_hash(this_user.password, data['password']):
                    print('did it')
                    session['user_id'] = this_user.id
                    session['first_name'] = this_user.first_name
                    session['last_name'] =this_user.last_name
                    return True
                flash('***Your login info is incorrect.***')
                return False       