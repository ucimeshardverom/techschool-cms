from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class BaseLoginTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            'user1', 'user1@example.com', 'GoodPass')

    def test_account_login(self):
        client = Client()

        # wrong password, no login
        credentials = {'login': 'user1', 'password': 'WrongPass'}
        response = client.post(reverse('account_login'), credentials,
                               follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['user'].pk)

        # good password login
        credentials.update(password='GoodPass')
        response = client.post(reverse('account_login'), credentials,
                               follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].pk, self.user.pk)

        client.logout()
