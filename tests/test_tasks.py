from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.dependencies import get_current_user_id

client = TestClient(app)


def override_get_current_user_id():
    return 1


app.dependency_overrides[get_current_user_id] = override_get_current_user_id


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_task():
    response = client.post("/tasks/", json={
        "title": "Тестовая задача",
        "priority": "high"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Тестовая задача"
    assert data["priority"] == "high"
    assert data["done"] is False


def test_get_tasks():
    setup_function()
    client.post("/tasks/", json={"title": "Задача 1", "priority": "low"})
    client.post("/tasks/", json={"title": "Задача 2", "priority": "medium"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_task_by_id():
    setup_function()
    create_response = client.post("/tasks/", json={
        "title": "Найди меня",
        "priority": "medium"
    })
    task_id = create_response.json()["id"]
    response = client.get("/tasks/" + str(task_id))
    assert response.status_code == 200
    assert response.json()["title"] == "Найди меня"


def test_update_task():
    setup_function()
    create_response = client.post("/tasks/", json={
        "title": "Обновить меня",
        "priority": "low"
    })
    task_id = create_response.json()["id"]
    response = client.patch("/tasks/" + str(task_id), json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True


def test_delete_task():
    setup_function()
    create_response = client.post("/tasks/", json={
        "title": "Удали меня",
        "priority": "low"
    })
    task_id = create_response.json()["id"]
    delete_response = client.delete("/tasks/" + str(task_id))
    assert delete_response.status_code == 204
    get_response = client.get("/tasks/" + str(task_id))
    assert get_response.status_code == 404


def test_filter_by_done():
    setup_function()
    client.post("/tasks/", json={"title": "Активная", "priority": "medium"})
    create_response = client.post("/tasks/", json={"title": "Выполненная", "priority": "medium"})
    task_id = create_response.json()["id"]
    client.patch("/tasks/" + str(task_id), json={"done": True})
    response = client.get("/tasks/?done=false")
    tasks = response.json()
    assert all(not t["done"] for t in tasks)


def test_create_category():
    setup_function()
    response = client.post("/categories/", json={"name": "Работа"})
    assert response.status_code == 201
    assert response.json()["name"] == "Работа"


def test_task_not_found():
    response = client.get("/tasks/99999")
    assert response.status_code == 404