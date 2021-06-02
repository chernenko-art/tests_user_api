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
    
    # Отправка запроса получение данных рандомного пользователя
    logging.info(f'Установка соединения с {url}')
    response = get(url)

    # Проверка валидности ответа на запрос
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


def do_register(number=1):
    """Метод doRegister (запрос на регистрацию пользователя)

    Args:
        number: количество пользователей

    """
    endpoint = '/tasks/rest/doregister'

    # Словарь для хранения данных, зарегестрированных пользователей
    user_params_dict = {}
    # Переменная для генерации ключей user_params_dict
    key_user = 0

    # Цикл регистрации пользователей
    for _ in range(number):
        logging.info('Вызов метода doRegister')
        
        # Запрос данных рандомного пользователя
        email, name, password = random_user_generator()
        
        # Отправка запроса на регистрацию пользователя
        logging.info(f'Установка соединения с {url_adress() + endpoint}')
        response = post(url_adress() + endpoint, json={
            "email": email,
            "name": name,
            "password": password
        })
        logging.info(f'Отправлен запрос на регистрацию пользователя:\
            "name" : "{name}", "email" : "{email}", "password" : "{password}"')
        
        # Проверка валидности ответа на запрос
        if valid_response(response):
            user_params_dict[str(key_user)] = {
                "json" : response.json(),
                "email": email,
                "name": name,
                "password": password
                }
            # Генерация ключа следующего пользователя
            key_user += 1
        else:
            logging.error('Ошибка в методе doregister')
    
    # Возврат словаря с данными зарегестрированных пользователей
    return user_params_dict


def do_login(email, password):
    """Метод doLogin (запрос на авторизацию пользователя)"""

    logging.info('Вызов метода doLogin')
    endpoint = '/tasks/rest/dologin'
    
    # Отправка запроса на авторизацию пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "email": email,
        "password": password
    })
    logging.info(f'Отправлен запрос на авторизацию пользователя:\
         "email" : "{email}", "password" : "{password}"')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе doLogin')
    

def create_task(task_title, task_description, email_owner, email_assign):
    """Метод CreateTask (создание задачи пользователю)"""
    
    logging.info('Вызов метода CreateTask')
    endpoint = '/tasks/rest/createtask'
    
    # Отправка запроса на создание задачи
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "task_title": task_title,
        "task_description": task_description,
        "email_owner": email_owner,
        "email_assign": email_assign
    })
    logging.info(f'Отправлен запрос на создание задачи пользователю: {email_assign}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateTask')


def create_company(company_name, company_type, company_users, email_owner):
    """Метод CreateCompany (создание компании с привязкой пользователей)"""
    
    logging.info('Вызов метода CreateCompany')
    endpoint = '/tasks/rest/createcompany'
    
    # Отправка запроса на создание компании
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "company_name": company_name,
        "company_type": company_type,
        "company_users": company_users,
        "email_owner": email_owner
    })
    logging.info(f'Отправлен запрос на создание компании: {company_name}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def create_user(email, name, tasks, companies,
    hobby=None, adres=None, name1=None,
    surname1=None, fathername1=None,
    cat=None, dog=None, parrot=None,
    cavy=None, hamster=None, squirrel=None,
    phone=None, inn=None, gender=None,
    birthday=None, date_start=None):
    """Метод CreateUser (создание пользователей c атрибутами)"""
    
    logging.info('Вызов метода CreateUser')
    endpoint = '/tasks/rest/createuser'
    
    # Отправка запроса на создание пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "email": email,
        "name": name,
        "tasks": tasks,
        "companies": companies,
        "hobby": hobby,
        "adres": adres,
        "name1": name1,
        "surname1": surname1,
        "fathername1": fathername1,
        "cat": cat,
        "dog": dog,
        "parrot": parrot,
        "cavy": cavy,
        "hamster": hamster,
        "squirrel": squirrel,
        "phone": phone,
        "inn": inn,
        "gender": gender,
        "birthday": birthday,
        "date_start": date_start
    })
    logging.info(f'Отправлен запрос на создание пользователя: {email}')
    
    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def create_user_with_task(email, name, tasks, companies,
                hobby=None, adres=None, name1=None,
                surname1=None, fathername1=None,
                cat=None, dog=None, parrot=None,
                cavy=None, hamster=None, squirrel=None,
                phone=None, inn=None, gender=None,
                birthday=None, date_start=None):
    """Метод CreateUser (создание пользователей c атрибутами)"""

    logging.info('Вызов метода CreateUser')
    endpoint = '/tasks/rest/createuserwithtasks'

    # Отправка запроса на создание пользователя
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, json={
        "email": email,
        "name": name,
        "tasks": tasks,
        "companies": companies,
        "hobby": hobby,
        "adres": adres,
        "name1": name1,
        "surname1": surname1,
        "fathername1": fathername1,
        "cat": cat,
        "dog": dog,
        "parrot": parrot,
        "cavy": cavy,
        "hamster": hamster,
        "squirrel": squirrel,
        "phone": phone,
        "inn": inn,
        "gender": gender,
        "birthday": birthday,
        "date_start": date_start
    })
    logging.info(f'Отправлен запрос на создание пользователя: {email}')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе CreateCompany')


def add_avatar(email, avatar):
    """Метод addAvatar (добавление аватара пользователю)"""

    logging.info('Вызов метода addAvatar')
    endpoint = '/tasks/rest/addavatar'

    # Отправка запроса на добавление аватара пользователю
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint, 
                    data={"email": email}, files={'avatar': avatar})

    logging.info(f'Отправлен запрос на добавление аватара пользователю: "email" : "{email}"')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе addAvatar')


def delele_avatar(email):
    """Метод DeleteAvatar (удаление аватара пользователю)"""

    logging.info('Вызов метода addAvatar')
    endpoint = '/tasks/rest/deleteavatar'

    # Отправка запроса на добавление аватара пользователю
    logging.info(f'Установка соединения с {url_adress() + endpoint}')
    response = post(url_adress() + endpoint,
                    data={"email": email})

    logging.info(
        f'Отправлен запрос на удаление аватара пользователю: "email" : "{email}"')

    # Проверка валидности ответа на запрос
    if valid_response(response):
        return response.json()
    else:
        logging.error('Ошибка в методе DeleteAvatar')
