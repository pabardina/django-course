from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.test import APITestCase

from authentication.models import Account


class TestLoginView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = Account.objects.create_user(username="test",
                                                email='test@test.com',
                                                password='testing')
        self.user.save()

    def test_login(self):
        url = reverse('login')
        data = {'username': 'test', 'password': 'testing'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username="test", password="testing")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +
                                                   self.user.auth_token.key)
        url = reverse('logout')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 204)


class TestAccountViews(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = Account.objects.create_user(username="test",
                                                email='test@test.com',
                                                password='testing')
        self.user.save()

    def _require_login(self):
        self.client.login(username='test', password='testing')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

    # def test_list_accounts_not_authenticated(self):
    #     self.client.logout()
    #     url = reverse('account-list')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 401,
    #                      'Expected Response Code 401, received {0} instead.'.format(response.status_code))

    def test_register_with_existing_email_and_username(self):
        url = reverse('account-list')
        data = {'username': 'test', 'email': 'test@test.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400,
                         'Expected Response Code 400, received {0} instead.'.format(response.status_code))

    def test_list_accounts_authenticated(self):
        self._require_login()
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_GetAccount(self):
        url = reverse('account-detail',  args=[self.user.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_update_account_authenticated(self):
        """
        Trying to edit an account with an other account

        """
        self._require_login()
        new_user = Account.objects.create_user(username="test2",
                                               email='test2@test.com',
                                               password='testing')
        url = reverse('account-detail', args=[new_user.pk])
        data = {'first_name': 'test'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'.format(response.status_code))

    def test_update_account_when_owner(self):
        self._require_login()
        url = reverse('account-detail',  args=[self.user.pk])
        data = {'first_name': 'test'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200,
                         'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    def test_update_account_no_authenticated(self):
        url = reverse('account-detail',  args=[self.user.pk])
        data = {'first_name': 'test'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 401,
                         'Expected Response Code 401, received {0} instead.'.format(response.status_code))

    def test_delete_account_authenticated(self):
        """
        Trying to delete an account with an other account

        """
        self._require_login()
        new_user = Account.objects.create_user(username="test2",
                                               email='test2@test.com',
                                               password='testing')
        url = reverse('account-detail', args=[new_user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403,
                         'Expected Response Code 403, received {0} instead.'.format(response.status_code))

    def test_delete_account_when_owner(self):
        self._require_login()
        url = reverse('account-detail',  args=[self.user.pk])
        response = self.client.delete(url,)
        self.assertEqual(response.status_code, 204,
                         'Expected Response Code 204, received {0} instead.'.format(response.status_code))

    def test_delete_account_no_authenticated(self):
        url = reverse('account-detail',  args=[self.user.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401,
                         'Expected Response Code 401, received {0} instead.'.format(response.status_code))