import requests

BASE_URL = "http://localhost:8004"

def test_bourbons():
    response = requests.get(f"{BASE_URL}/bourbons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)