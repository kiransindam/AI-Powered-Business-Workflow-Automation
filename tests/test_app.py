from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_process_sales_request():
    response = client.post("/process", json={
        "name": "Jamie Example",
        "email": "jamie@example.com",
        "subject": "Pricing for a new order",
        "message": "Could you share pricing for a product order?",
        "source": "test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "sales"
    assert data["priority"] == "normal"
    assert data["ai_mode"] in {"rules", "llm"}
    assert data["request_id"]

def test_high_priority_request_needs_review():
    response = client.post("/process", json={
        "name": "Taylor Example",
        "email": "taylor@example.com",
        "subject": "Urgent access issue",
        "message": "We have an urgent outage and cannot access the system.",
        "source": "test"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "high"
    assert data["status"] == "needs_review"

def test_validation_rejects_invalid_email():
    response = client.post("/process", json={
        "name": "Jamie",
        "email": "not-an-email",
        "subject": "Need help",
        "message": "Please help with an issue"
    })
    assert response.status_code == 422
