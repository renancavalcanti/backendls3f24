from flask import Flask, jsonify, request
from pymongo import MongoClient
from views.user_view import user
from views.user_task_view import task

app = Flask(__name__)

app.register_blueprint(user)
app.register_blueprint(task)


@app.route('/', methods=['GET'])
def home():
    return "<h1>HOME HOME</h1>"

if __name__ == '__main__':
    app.run()
