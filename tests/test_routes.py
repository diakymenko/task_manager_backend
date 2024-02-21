import os

import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///tests.db"})

    yield app

    # clean up / reset resources here
    os.unlink('../instance/tests.db')


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_create_task(client):
    response = client.post("/tasks/", json={"title": "test task", "description": "my test task"},
                           headers={"Content-Type": "application/json"})

    assert response.status_code == 201
    assert response.json["title"] == "test task"
    assert response.json["description"] == "my test task"
    assert response.json["completed"] is False


def test_get_tasks(client):
    for i in range(3):
        test_create_task(client)

    response = client.get("/tasks/")
    assert len(response.json) == 3
    assert response.status_code == 200
    assert response.json[0]["title"] == "test task"


def test_delete_task_valid_id(client):
    for i in range(3):
        test_create_task(client)
    response = client.delete("/tasks/1", headers={"Content-Type": "application/json"})
    assert response.status_code == 204
    response = client.get("/tasks/")
    assert len(response.json) == 2


def test_delete_task_invalid_id(client):
    client.post("/tasks/", json={"title": "test task", "description": "my test task"},
                headers={"Content-Type": "application/json"})
    client.get("/tasks/")
    response = client.delete("/tasks/2", headers={"Content-Type": "application/json"})
    assert response.status_code == 404
    assert "details" in response.json
    assert "Task with id #2 not found" in response.json["details"]


def test_update_task(client):
    test_create_task(client)
    response = client.patch("/tasks/1", headers={"Content-Type": "application/json"},
                            json={"title": "updated task", "description": "my updated task", "completed": True})
    assert response.status_code == 200
    response = client.get("/tasks/")
    assert len(response.json) == 1
    assert response.json[0]["title"] == "updated task"
    assert response.json[0]["description"] == "my updated task"
    assert response.json[0]["completed"] is True


def test_empty_title_post_request(client):
    response = client.post("/tasks/", json={"title": "", "description": "task description"},
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert "details" in response.json
    assert "Please enter a valid task title!" in response.json["details"]


def test_no_title_attribute_post_request(client):
    response = client.post("/tasks/", json={"description": "task description"},
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 400
    assert "details" in response.json
    assert "Please enter a valid task title!" in response.json["details"]