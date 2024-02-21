from flask import request, jsonify, Blueprint
from app.controllers.tasks_validation import *

from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")


@tasks_bp.route('/', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    return jsonify(
        [{'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed} for task
         in tasks]), 200


@tasks_bp.route('/', methods=['POST'])
def create_task():
    task = validate_task_post_request(request)

    db.session.add(task)
    db.session.commit()

    return jsonify(
        {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}), 201


@tasks_bp.route('/<id>', methods=['DELETE'])
def delete_task(id):
    task = validate_task_by_id(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify(), 204


@tasks_bp.route('/<id>', methods=['PATCH'])
def update_task(id):
    task = validate_task_patch_request(request, id)

    db.session.add(task)
    db.session.commit()

    return jsonify(
        {'id': task.id, 'title': task.title, 'description': task.description, 'completed': task.completed}), 200
