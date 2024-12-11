import pytest
from application import app  # Import the Flask app


@pytest.fixture
def client():
    """Fixture for setting up the test client"""
    app.testing = True
    return app.test_client()


def test_get_all_employees(client):
    """Test retrieving all employees with pagination"""
    response = client.get('/employee?page=1&per_page=10')

    assert response.status_code == 200
    assert 'data' in response.json
    assert 'pagination' in response.json
    assert len(response.json['data']) >= 0


def test_get_employee_by_id(client):
    """Test retrieving an employee by ID"""
    response = client.get('/employee/EMP0001')  # Replace "EMP001" with a valid Employee_ID

    if response.status_code == 200:
        assert 'Employee_ID' in response.json
        assert response.json['Employee_ID'] == "EMP9999"
    elif response.status_code == 404:
        assert 'message' in response.json
        assert response.json['message'] == "Employee entry not found"


def test_get_employee_not_found(client):
    """Test retrieving an employee that doesn't exist"""
    response = client.get('/employee/INVALID_ID')

    assert response.status_code == 404
    assert 'message' in response.json
    assert response.json['message'] == "Employee entry not found"


def test_get_all_employees_invalid_page(client):
    """Test retrieving all employees with an invalid page number"""
    response = client.get('/employee?page=-1&per_page=10')

    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == "Page and per_page must be positive integers."
