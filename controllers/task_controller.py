from database.__init__ import database
import app_config
from flask import jsonify
from bson.objectid import ObjectId

def create_task(task):
    try:
        task.createdByUid = task.createdByUid.lower()
        task.createdByName = task.createdByName.lower()
        task.assignedToUid = task.assignedToUid.lower()
        task.assignedToName = task.assignedToName.lower()
        task.description = task.description.lower()
        
        if not isinstance(task.done, bool):
            raise ValueError("The 'done' attribute must be a boolean")

        print(task.__dict__)

        collection = database.database[app_config.CONST_TASK_COLLECTION]

        return collection.insert_one(task.__dict__)
    
        
        
    except:
        raise Exception("Error when creating task!")
    
def fetch_tasks(token):
    try: 
        collection = database.database[app_config.CONST_TASK_COLLECTION]
        tasks = []
        for task in collection.find({"createdByUid": token['id']}):
            if task['createdByUid'] == token['id']:
                current_task = {
                    'createdByUid': task['createdByUid'],
                    'createdByName': task['createdByName'],
                    'assignedToUid': task['assignedToUid'],
                    'assignedToName': task['assignedToName'],
                    'description': task['description'],
                    'done': task['done'],
                    'taskUid': str(task['_id'])
                }
            tasks.append(current_task)

        if len(tasks) == 0:
            return jsonify({'error': 'No tasks found for the user'}), 404
        return jsonify({'tasks': tasks})
    except:
        raise Exception("Error when trying to fetch tasks!")
    
def fetch_assigned_to(token):
    try:
        collection = database.database[app_config.CONST_TASK_COLLECTION]

        tasks = []
        for task in collection.find({"assignedToUid": token['id']}):
            if token['id'] == task['assignedToUid']:
                current_task = {
                    'createdByUid': task['createdByUid'],
                    'createdByName': task['createdByName'],
                    'assignedToUid': task['assignedToUid'],
                    'assignedToName': task['assignedToName'],
                    'description': task['description'],
                    'done': task['done'],
                    'taskUid': str(task['_id'])
                }
            tasks.append(current_task)

        if len(tasks) == 0:
            return jsonify({'error': 'No tasks found for the user'}), 404

        return jsonify({'tasks': tasks})
    except:
        raise Exception("Error when trying to fetch tasks assigned to a user!")
    
def update_task(taskUid, token, done_status):
    try:
        collection = database.database[app_config.CONST_TASK_COLLECTION]

        current_task = collection.find_one({"_id": ObjectId(taskUid)})

        if not current_task:
            return {'error': 'Task not found'}, 404

        if token['id'] != current_task['assignedToUid']:
            return {'error': 'Unauthorized: Users can only change status when task is assigned to them'}, 403

        if current_task['done'] == done_status:
            return {'taskUid': taskUid, 'modified_count': 0}, 200

        collection.update_one({"_id": ObjectId(taskUid)}, {"$set": {"done": done_status}})

        return {'taskUid': taskUid}, 200

    except:
        return {'error': 'Something went wrong when updating the task'}, 500

def delete_task(taskUid, token):
    try:
        collection = database.database[app_config.CONST_TASK_COLLECTION]
        current_task = collection.find_one({"_id": ObjectId(taskUid)})

        if not current_task:
            return jsonify({'error': 'Task not found'}), 404

        if 'createdByUid' not in current_task:
            return jsonify({'error': 'Task does not have a createdByUid field'}), 400

        print(f"CreatedByUid: {current_task['createdByUid']}")
        if token['id'] != current_task['createdByUid']:
            return jsonify({'error': 'Unauthorized: Only the user who created the task can delete it'}), 403

        result = collection.delete_one({"_id": ObjectId(taskUid)})

        if result.deleted_count == 0:
            return jsonify({'error': 'Task not found'}), 404

        return jsonify({'tasksAffected': result.deleted_count}), 200

    except:
        raise Exception ({'error': 'Something went wrong when deleting the task'})

