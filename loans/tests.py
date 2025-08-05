from django.test import TestCase
from rest_framework.test import APIClient

class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_customer(self):
        response = self.client.post('/register', {
            "first_name": "Test",
            "last_name": "User",
            "age": 30,
            "monthly_income": 50000,
            "phone_number": "9998887776"
        }, format='json')
        self.assertEqual(response.status_code, 201)
