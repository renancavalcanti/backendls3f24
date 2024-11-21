from flask import Blueprint, jsonify, request
from database.__init__ import database
from controllers.task_controller import create_task, fetch_tasks, fetch_assigned_to, update_task, delete_task
from controllers.user_controller import find_users
from models.task_model import Task
from helpers.token_validation import validate_jwt

task = Blueprint("tasks", __name__)

@task.route('/tasks', methods=['POST'])
def add_task():
    try:
        my_body = request.json
        token = validate_jwt()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        if "description" not in my_body or "assignedToUid" not in my_body:
            return jsonify({"error": 'Error validating form'}), 400
        
        assignedName = find_users(my_body['assignedToUid'])
        createdName = find_users(token['id'])

        my_task = Task(token['id'], createdName, my_body['assignedToUid'], assignedName, my_body['description'], False)
        result = create_task(my_task)

        return jsonify({"id": str(result.inserted_id)})
    except:
        return jsonify({"error": "An error when creating task"}), 400


@task.route('/tasks/createdby', methods=['GET'])
def get_tasks():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401
        
        return fetch_tasks(token=token)
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500
    
@task.route('/tasks/assignedto', methods=['GET'])
def get_assigned_to():
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401
        
        return fetch_assigned_to(token=token)
    except:
        return jsonify({'error': 'Something wrong happened when fetching tasks!'}), 500
    
@task.route('/tasks/<taskUid>', methods=['PATCH', 'POST'])
def update_task_route(taskUid):
    try:
        token = validate_jwt()
        my_body = request.json

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401
        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403
        if 'done' not in my_body:
            return jsonify({"error": 'Status done not found in the request'}), 400

        result, status_code = update_task(taskUid, token, my_body['done'])

        return jsonify(result), status_code
    except:
        return jsonify({'error': 'Something wrong happened when updating task!'}), 500
    
@task.route('/v1/tasks/<taskUid>', methods=['DELETE'])
def deleteTask(taskUid):
    try:
        token = validate_jwt()
        if token == 400:
            return jsonify({'error': 'Token is missing in the request!'}), 400
        if token == 401:
            return jsonify({'error': 'Invalid authentication token!'}), 401

        return delete_task(taskUid, token)
    except:
        return jsonify({'error': 'Something went wrong when deleting the task!'}), 500