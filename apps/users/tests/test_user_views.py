from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User
from apps.projects.models import Project


class UserAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.project = Project.objects.create(name="Test Project")
        self.user1 = User.objects.create_user(
            username='user1',
            first_name='John',
            last_name='Doe',
            email='user1@example.com',
            password='password123',
            position='PROGRAMMER',
            project=self.project
        )
        self.user2 = User.objects.create_user(
            username='user2',
            first_name='Jane',
            last_name='Doe',
            email='user2@example.com',
            password='password123',
            position='DESIGNER',
            project=self.project
        )

    def test_get_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], self.user1.username)
        self.assertEqual(response.data[1]['username'], self.user2.username)

    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            're_password': 'newpassword123',
            'position': 'PROGRAMMER',
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.first_name, 'New')
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_register_user_with_invalid_data(self):
        url = reverse('user-register')
        data = {
            'username': '',
            'first_name': '',
            'last_name': '',
            'email': 'invalid-email',
            'password': 'short',
            're_password': 'short',
            'position': 'PROGRAMMER',
            'project': self.project.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Проверка наличия ошибок в полях, которые валидируются раньше пароля
        self.assertIn('username', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('email', response.data)

    def test_get_user_detail(self):
        url = reverse('user-detail', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['first_name'], self.user1.first_name)
        self.assertEqual(response.data['last_name'], self.user1.last_name)
        self.assertEqual(response.data['email'], self.user1.email)
        self.assertEqual(response.data['position'], self.user1.position)
        self.assertEqual(response.data['project'], self.project.id)

    def test_get_nonexistent_user_detail(self):
        url = reverse('user-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'No User matches the given query.')