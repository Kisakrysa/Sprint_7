import json

import allure
import pytest

from http import HTTPStatus

import requests

from data import Data
import helpers


@pytest.mark.get_url('create_courier')
class TestCreateCourier:

    @allure.title('[Позитивный] Создание курьера.')
    def test_create_courier_available_success(self, get_url, get_new_data):
        payload = get_new_data
        response = requests.post(url=get_url, data=payload)
        assert response.status_code == HTTPStatus.CREATED
        response_data = json.loads(response.text)
        assert response_data['ok'] == True

    @allure.title('[Негативный] Создание двух одинаковых курьеров.')
    def test_create_courier_as_prev_courier_unavailable_success(self, get_url, get_new_data):
        payload = helpers.register_new_courier_and_return_login_password(get_new_data)
        response = requests.post(url=get_url, data=payload)
        message = response.json()['message']
        assert response.status_code == HTTPStatus.CONFLICT
        assert message == Data.ERROR_TEXT_FOR_LOGIN_EXIST_YET

    @allure.title('[Негативный] Создание курьера - без обязательного поля')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_create_courier_without_one_required_field_unavailable_success(self, get_url, field, get_new_data):
        payload = dict.fromkeys([field, ])
        payload = helpers.get_data_without_one_required_field(payload, get_new_data)
        response = requests.post(url=get_url, data=payload)
        message = response.json()['message']
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert message == Data.ERROR_TEXT_FOR_CREATE_WITHOUT_REQUIRED_FIELD
