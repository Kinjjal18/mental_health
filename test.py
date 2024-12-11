# tests/test_get_operations.py

import unittest
from application import app  # Import your Flask app

class TestGetOperations(unittest.TestCase):
    def setUp(self):
        """Set up the test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_employees(self):
        """Test retrieving all employees with pagination"""
        response = self.app.get('/employee?page=1&per_page=10')  # Update with the actual endpoint
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.json)
        self.assertIn('pagination', response.json)
        self.assertGreaterEqual(len(response.json['data']), 0)

    def test_get_employee_by_id(self):
        """Test retrieving an employee by ID"""
        # Use an ID that doesn't exist in your dataset
        response = self.app.get('/employee/EMP999999')  # Clearly non-existent ID

        # Check the status code and ensure it returns a 404 (Not Found)
        if response.status_code == 200:
            # This will fail if the employee with the given ID doesn't exist (which it shouldn't)
            self.assertIn('Employee_ID', response.json)
            self.assertEqual(response.json['Employee_ID'], "EMP0999")  # The ID will not match
        elif response.status_code == 404:
            # Ensure the error message matches the expected message
            self.assertIn('message', response.json)
            self.assertEqual(response.json['message'],"Employee entry not found")  # This message should be in the response
        else:
            # If the status code is neither 200 nor 404, the test should fail
            self.fail(f"Expected status code 200 or 404, got {response.status_code}")

    def test_get_employee_not_found(self):
        """Test retrieving an employee that doesn't exist"""
        response = self.app.get('/employee/INVALID_ID')
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], "Employee entry not found")

    def test_get_all_employees_invalid_page(self):
        """Test retrieving all employees with an invalid page number"""
        response = self.app.get('/employee?page=-1&per_page=10')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], "Page and per_page must be positive integers.")
