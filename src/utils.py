import logging
import os
from dotenv import load_dotenv

from data.companies import EMPLOYERS_LIST

from hh_api import HhApiImplementation
from db_manager import DBManager

# Настройки логирования
logging.basicConfig(level=logging.ERROR)


def main():
    load_dotenv()

    db_params = {
        'dbname': os.getenv('dbname'),
        'user': os.getenv('user'),
        'password': os.getenv('password'),
        'host': os.getenv('host'),
        'port': os.getenv('port')
    }

    key_w = input('Введите ключевое слово: ')

    # Создаем экземпляр DBManager для взаимодействия с базой данных
    db_manager = DBManager(db_params)

    # Создаем экземпляр HhApiImplementation для получения данных о компаниях и вакансиях
    hh_api = HhApiImplementation()

    # Проходим по списку компаний и получаем информацию о вакансиях для каждой компании
    data_to_insert = []

    for employer in EMPLOYERS_LIST:
        company_id = employer['id']
        company_name = employer['name']

        # Получаем данные о вакансиях для текущей компании
        vacancies_data = hh_api.get_vacancies_by_employer(company_id)

        # Формируем данные для вставки в базу данных
        data_to_insert.append({'company_name': company_name, 'vacancies': vacancies_data})

    # Вставляем данные в базу данных
    db_manager.insert_data_batch(data_to_insert)

    # Выводим результаты
    print("Companies and Vacancies Count:", db_manager.get_companies_and_vacancies_count())
    print("All Vacancies:", db_manager.get_all_vacancies())
    print("Average Salary:", db_manager.get_avg_salary())
    print("Vacancies with Higher Salary:", db_manager.get_vacancies_with_higher_salary())
    print("Vacancies with Keyword:", db_manager.get_vacancies_with_keyword(key_w))

    # Закрываем соединение с базой данных
    db_manager.close_connection()
