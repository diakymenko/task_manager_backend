from app.models import *
from flask import jsonify, make_response, abort, request


def validate_task_post_request(request):
    request_body = request.get_json()

    if "title" not in request_body or request_body["title"] == "":
        abort(make_response(jsonify(
            {
                "details": "Please enter a valid task title!"
            }), 400))
    if "description" not in request_body or request_body["description"] == "":
        abort(make_response(jsonify(
            {
                "details": "Please enter a valid task description!"
            }), 400))
    completed = request_body["completed"] if "completed" in request_body else False
    task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed=completed)
    return task


def validate_task_patch_request(request, id):
    task = validate_task_by_id(id)
    request_body = request.get_json()

    if "title" in request_body:
        task.title = request_body["title"]
    if "description" in request_body:
        task.description = request_body["description"]
    if "completed" in request_body:
        task.completed = request_body["completed"]

    return task


def validate_task_by_id(id):
    task = Task.query.get(id)
    if task:
        return task
    abort(
        make_response({"details": f'Task with id #{id} not found'}, 404))
