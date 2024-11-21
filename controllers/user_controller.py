from database.__init__ import database
import app_config
import bcrypt
from datetime import datetime, timedelta
from flask import jsonify
import jwt

def generate_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def create_user(user):

    try:
        user.name = user.name.lower()
        user.email = user.email.lower()
        user.password = generate_hash_password(user.password)

        print(user.__dict__)

        collection = database.database[app_config.CONST_USER_COLLECTION]

        if collection.find_one({"email": user.email}):
            return "Duplicated User"

        return collection.insert_one(user.__dict__)
    except:
        raise Exception("Error when creating user!")
    
def login_user(user_information):
    try: 
        email = user_information["email"].lower()   
        password = user_information["password"].encode('utf-8')

        collection = database.database[app_config.CONST_USER_COLLECTION]

        current_user = collection.find_one({"email": email})

        if not current_user:
            return "Invalid email"
        
        if not bcrypt.checkpw(password, current_user["password"]):
            return "Invalid password"
        
        expiration = datetime.utcnow() + timedelta(seconds = app_config.JWT_EXPIRATION)
        jwt_data = {'email': current_user['email'], 'id': str(current_user['_id']), 'exp': expiration}

        jwt_to_return = jwt.encode(payload = jwt_data, key = app_config.TOKEN_SECRET)

        logged_user = {
            'id': str(current_user['_id']),
            'name': current_user['name'],
            'email': current_user['email']
        }
        return jsonify({'token': jwt_to_return, 'expiration': app_config.JWT_EXPIRATION, 'logged_user': logged_user})
    except:
        raise Exception("Error when trying to login user!")

def fetch_users():
    try: 
        collection = database.database[app_config.CONST_USER_COLLECTION]
        users = []
        for user in collection.find():
            current_user = {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email']
            }
            users.append(current_user)
        return jsonify({'users': users})
    except:
        raise Exception("Error when trying to fetch users!")
    
def find_users(user_id):
    try:
        collection = database.database[app_config.CONST_USER_COLLECTION]
        for user in collection.find():
            if str(user['_id']) == user_id:
                return user["name"]
    except:
        raise Exception("User is not in the database!")