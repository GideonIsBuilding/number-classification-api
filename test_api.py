import pytest
from flask import json
from api import app  # Import your Flask app (replace 'your_flask_file' with the actual file name)

@pytest.fixture
def client():
    """Set up the Flask test client."""
    app.config["TESTING"] = True  # Enable test mode
    with app.test_client() as client:
        yield client

def test_valid_prime_number(client):
    """Test a valid prime number."""
    response = client.get("/api/classify-number?number=7")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["number"] == 7
    assert data["is_prime"] is True
    assert "prime" in data["properties"]

def test_valid_perfect_number(client):
    """Test a valid perfect number."""
    response = client.get("/api/classify-number?number=6")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["is_perfect"] is True
    assert "perfect" in data["properties"]

def test_valid_armstrong_number(client):
    """Test a valid Armstrong number (371)."""
    response = client.get("/api/classify-number?number=371")
    data = response.get_json()
    
    assert response.status_code == 200
    assert "armstrong" in data["properties"]
    assert data["fun_fact"] == "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"

def test_negative_number(client):
    """Test a negative number (should still classify correctly)."""
    response = client.get("/api/classify-number?number=-5")
    data = response.get_json()
    
    assert response.status_code == 200
    assert data["number"] == -5
    assert "odd" in data["properties"]

def test_non_numeric_input(client):
    """Test when input is an alphabet (should return error)."""
    response = client.get("/api/classify-number?number=abc")
    data = response.get_json()
    
    assert response.status_code == 400
    assert data["number"] == "alphabet"
    assert data["error"] is True

def test_missing_input(client):
    """Test when no number is provided (should return error)."""
    response = client.get("/api/classify-number")
    data = response.get_json()
    
    assert response.status_code == 400
    assert data["number"] == "missing input"
    assert data["error"] is True

def test_fun_fact_fallback(client, monkeypatch):
    """Test fallback logic when Numbers API is unavailable."""
    def mock_get_fun_fact(n):
        return f"{n} is an Armstrong number because {' + '.join(f'{d}^{len(str(n))}' for d in str(n))} = {n}"
    
    monkeypatch.setattr("api.get_fun_fact", mock_get_fun_fact)
    
    response = client.get("/api/classify-number?number=371")
    data = response.get_json()

    assert response.status_code == 200
    assert data["fun_fact"] == "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371"
