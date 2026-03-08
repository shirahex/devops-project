import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data
    assert "version" in data

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "tasks" in data
    assert "count" in data

def test_create_task(client):
    response = client.post(
        "/tasks",
        data=json.dumps({"title": "Test Task"}),
        content_type="application/json"
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["title"] == "Test Task"
    assert data["done"] == False

def test_create_task_missing_title(client):
    response = client.post(
        "/tasks",
        data=json.dumps({}),
        content_type="application/json"
    )
    assert response.status_code == 400

def test_update_task(client):
    response = client.put(
        "/tasks/1",
        data=json.dumps({"done": True}),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["done"] == True

def test_update_task_not_found(client):
    response = client.put(
        "/tasks/999",
        data=json.dumps({"done": True}),
        content_type="application/json"
    )
    assert response.status_code == 404

def test_delete_task(client):
    response = client.delete("/tasks/2")
    assert response.status_code == 200

def test_delete_task_not_found(client):
    response = client.delete("/tasks/999")
    assert response.status_code == 404
