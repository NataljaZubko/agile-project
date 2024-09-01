from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserAPITests(APITestCase):

    def test_get_user_list(self):
        User.objects.create_user(username="user1", password="password123")
        User.objects.create_user(username="user2", password="password123")

        url = reverse('user-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_register_user(self):
        url = reverse('user-register')
        data = {
            "username": "new_user",
            "password": "new_password123",
            "email": "new_user@example.com"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'new_user')

    def test_register_user_validation_error(self):
        url = reverse('user-register')
        data = {
            "username": "",
            "password": "short",
            "email": "invalid_email"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)

class UserDetailAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            first_name='John',
            last_name='Doe',
            email='john@example.com'
        )

    def test_get_user_detail(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['first_name'], 'John')
        self.assertEqual(response.data['last_name'], 'Doe')
        self.assertEqual(response.data['email'], 'john@example.com')

    def test_get_nonexistent_user_detail(self):
        url = reverse('user-detail', args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Not found.')