import allure
import pytest


from http import HTTPStatus

import requests

from data import Data
import helpers


@pytest.mark.get_url('login_courier')
class TestLoginCourier:

    @allure.title('[Позитивный] Авторизация курьера')
    def test_login_courier_positive(self, get_url, get_new_data):
        payload = helpers.register_new_courier_and_return_login_password(get_new_data)
        response = requests.post(get_url, payload)
        assert response.status_code == HTTPStatus.OK and 'id' in response.json()

    @allure.title('[Негативный] Авторизация курьера с некорректными доступами')
    @pytest.mark.parametrize('condition', ('incorrect_login', 'incorrect_password'))
    def test_login_courier_with_incorrect_creds(
            self, get_url, condition, get_new_data):
        current_data = helpers.register_new_courier_and_return_login_password(get_new_data)
        payload = helpers.get_data_for_check_response_error(condition, current_data)
        response = requests.post(get_url, payload)
        assert response.json()['message'] == Data.ERROR_TEXT_FOR_INCORRECT_LOGIN_OR_PASSWORD

    @allure.title('[Негативный] Авторизация несуществующего пользователя')
    def test_login_courier_with_required_fields_available_success(self, get_url, get_new_data):
        payload = helpers.register_new_courier_and_return_login_password(get_new_data)
        payload['login'] = f"new{get_new_data['login']}"
        response = requests.post(get_url, payload)
        message = response.json()['message']
        assert response.status_code == HTTPStatus.NOT_FOUND and message == Data.ERROR_TEXT_FOR_INCORRECT_LOGIN_OR_PASSWORD
