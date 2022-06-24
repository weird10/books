from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import request, flash, session



class Sighting:
    db = 'websighting_schema'

    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.number = data['number']
        self.time_that = data['time_that']
        self.created_at=data['created_at']
        self.updated_at = data ['updated_at']
        self.author = data['author']
        self.user_id = data['user_id']
        self.skeptic = []
        

    
    @classmethod
    def create_sighting(cls, data):
        if not cls.validate_sighting_regis(data):
            return False
        query = "INSERT INTO sightings (location, description, number,author, time_that, user_id) VALUES ( %(location)s, %(description)s,%(number)s,%(author)s, %(time_that)s,%(user_id)s);"
        sighting_id = connectToMySQL(cls.db).query_db(query,data)
        print('sighting created with id of',sighting_id)
        return True
    
    
    @classmethod
    def get_all_sightings(cls):
        query="""
        SELECT * FROM sightings
        LEFT JOIN users on users.id = sightings.user_id 
        ;"""
        results = MySQLConnection(cls.db).query_db(query)
        all_sightings = []
        for n in results:
            all_sightings.append(cls(n)) 
        return all_sightings

    @classmethod
    def get_all_unsighted(cls,data):
        query = "SELECT * FROM sightings WHERE sightings.id NOT IN ( SELECT sighting_id FROM skeptics WHERE user_id = %(id)s );"
        results = connectToMySQL(cls.db).query_db(query,data)
        unsighted = []
        for row in results:
            unsighted.append(cls(row))
        print(unsighted)
        return results

    @classmethod
    def get_by_sighting_id(cls, data):
        query="""
        SELECT * FROM sightings
        WHERE id = %(id)s
        ;"""
        results = MySQLConnection(cls.db).query_db(query, data)
        sighting = cls(results[0])
        return sighting
    
    @classmethod
    def get_skeptics(cls, data):
        query= """
        SELECT * FROM sightings
        LEFT JOIN skeptics
        ON sightings.id = skeptics.sighting_id
        LEFT JOIN users
        ON users.id = skeptics.user_id
        WHERE sightings.id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        all_skeptic = cls(results[0])
        for row in results:
            if row['users.id'] == None:
                break
            data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            all_skeptic.skeptic.append(data) 
        return all_skeptic

        

    @classmethod
    def edit_sighting(cls,data):
        data = {
            'id': request.form['id'],
            'location' : request.form['location'],
            'description':request.form['description'],
            'number':request.form['number'],
            'time_that':request.form['time_that'],
            'author' : request.form['author']
            }
        if not cls.validate_sighting_regis(data):
            return False
        query="""
        UPDATE sightings 
        SET location = %(location)s, description = %(description)s, number = %(number)s, time_that = %(time_that)s, author=%(author)s, updated_at=NOW()
        WHERE id = %(id)s
        ;"""
        results = MySQLConnection(cls.db).query_db(query, data)
        return results


    @classmethod
    def delete_sighting(cls,data):
        query="""
        ON DELETE CASCADE
        DELETE FROM sightings
        WHERE id = %(id)s
        ;"""
        results = MySQLConnection(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_sighting_regis(data):
        is_valid=True
        if not (data['location']):
            is_valid=False
            flash("Sighting's location cannot be empty")
        if not (data['description']):
            flash("Sighting's description cannot be empty")
            is_valid=False
        if not (data['number']):
            is_valid=False
            flash("Sighting's number of sasquatch cannot be empty")
        if not (data['time_that']):
            is_valid=False
            flash("Sighting's date sighted cannot be empty")
        return is_valid
