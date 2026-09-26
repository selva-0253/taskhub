from fastapi.testclient import TestClient

from app.main import app, tasks 

client = TestClient(app)

def setup_function():
    tasks.clear()

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test task",
            "description": "This is a test task"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "This is a test task"
    assert data["completed"] is False
    assert data["id"] == 1

def test_get_tasks():
    client.post("/tasks", json={"title": "task 1"})
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "task 1"

def test_get_task():
    client.post("/tasks", json={"title": "task 1"})
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "task 1"

def test_nonexistence_task():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Task not found"

def test_update_task():
    client.post("/tasks", json={"title": "task 1"})
    response = client.put("/tasks/1", json={"title": "updated task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated task"

def test_delete_task():
    client.post("/tasks", json={"title": "task 1"})
    response = client.delete("/tasks/1")
    assert response.status_code == 204


def test_task_created_without_title():
    response = client.post("/tasks", json={"description": "No title"})
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["body", "title"]

def test_get_task_with_invalid_id():
    client.post("/tasks", json={"title": "task 1"})
    response = client.get("/tasks/abc")
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["loc"] == ["path", "task_id"]

    