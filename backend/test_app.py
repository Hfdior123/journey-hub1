import pytest
from app import app
import allure

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@allure.step("Test home endpoint")
def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Travel Reservation System!"}
    allure.attach(str(response.json), name="Home Response", attachment_type=allure.attachment_type.TEXT)

@allure.step("Test book endpoint")
def test_book_destination(client):
    payload = {"destination": "Paris"}
    response = client.post("/book", json=payload)
    assert response.status_code == 200
    assert response.json == {"status": "success", "destination": "Paris"}
    allure.attach(str(response.json), name="Booking Response", attachment_type=allure.attachment_type.TEXT)
