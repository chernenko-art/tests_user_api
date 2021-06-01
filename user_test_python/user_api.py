from requests import get, put, post, delete
import logging
from conftest import level_logging, url_adress


# Конфигурация логов
FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d:%(funcName)-20s] %(message)s'
logging.basicConfig(level=level_logging(),
                    format=FORMAT,
                    datefmt='%m-%d %H:%M',
                    filename='user_tests.log'
                    )


def valid_response(response):
    """Проверка header ответа сервера"""
    logging.info('Проверка ответа от сервера')

    # Проверка status_code
    logging.info(f'Status code = {response.status_code}')
    if response.status_code != 200:
        logging.error(f'Status Code = {response.status_code}')
        return False
    
    # Проверка наличия 'application/json' в 'content-type'
    content_type = response.headers['content-type']
    logging.debug(f'Response headers: {response.headers}')
    header_list = [elem.strip() for elem in content_type.split(';')]
    if 'application/json' not in header_list:
        logging.error(f'"application/json" отсутствует в "content-type"')
        return False
    else:
        logging.debug(f'Response body = {response.json()}')
        logging.debug(f'Header "content-type" = [{response.headers["content-type"]}]')
        logging.info('Проверка ответа от сервера успешно выполнена')
        return True


def random_user_generator():
    """
    Получение данных рандомного пользователя
    с помощью api https://randomuser.me/
    """
    logging.info('Запуск получения данных рандомного пользователя')
    url = 'https://randomuser.me/api'
    logging.info(f'Установка соединения с {url}')
    response = get(url)
    if valid_response(response):
        response_body = response.json()
        email = response_body['results'][0]['email']
        logging.debug(f'Получен "email" : "{email}"')
        name = response_body['results'][0]['login']['username']
        logging.debug(f'Получен "name" : "{name}"')
        password = response_body['results'][0]['login']['password']
        logging.debug(f'Получен  "password" : "{password}"')
        logging.info(f'Получены данные рандомного пользователя:\
             "email" : "{email}", "name" : "{name}", "password" : "{password}"')
        return email, name, password
    else:
        logging.error('Ошибка в получении данных рандомного пользователя')


def do_register():
    """Метод doRegister (запрос на регистрацию пользователя)"""
    logging.info('Вызов метода doregister')
    endpoint = '/tasks/rest/doregister'
    email, name, password = random_user_generator()
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "email": email,
        "name": name,
        "password": password
    })
    logging.info(f'Отправлен запрос на регистрацию пользователя:\
         "name" : "{name}", "email" : "{email}", "password" : "{password}"')
    if valid_response(response):
        return response.json(), email, name, password
    else:
        logging.error('Ошибка в методе doregister')


def do_login(email, password):
    """Метод doLogin (запрос на авторизацию пользователя)"""
    logging.info('Вызов метода doLogin')
    endpoint = '/tasks/rest/dologin'
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "email": email,
        "password": password
    })
    logging.info(f'Отправлен запрос на авторизацию пользователя:\
         "email" : "{email}", "password" : "{password}"')
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе doLogin')
    
