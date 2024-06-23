from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'password2': 'newpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'newuser')

    def test_user_profile_update(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        url = reverse('user-detail', kwargs={'pk': user.id})
        data = {
            'username': 'updatedusername',
            'email': 'updateduser@example.com'
        }
        self.client.force_authenticate(user=user)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertEqual(user.username, 'updatedusername')
        self.assertEqual(user.email, 'updateduser@example.com')

    def test_token_obtain_pair(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # def test_user_delete(self):
    #     user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
    #     url = reverse('user-detail', kwargs={'pk': user.id})
    #     self.client.force_authenticate(user=user)
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     user.refresh_from_db()
    #     self.assertTrue(user.deleted)
