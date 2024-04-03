import requests
from abc import ABC, abstractmethod
from collections import defaultdict
import logging


class HhApi(ABC):
    """Абстрактный класс для взаимодействия с API HeadHunter."""

    def __init__(self):
        """Инициализация класса HhApi."""
        self.base_url = "https://api.hh.ru"

    @abstractmethod
    def get_companies_and_vacancies(self, params):
        """Метод для получения списка компаний и вакансий на основе предоставленных параметров."""
        pass

    def _get_vacancies(self, endpoint, params=None):
        """Общий метод для получения вакансий."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data['items']
        except requests.exceptions.RequestException as e:
            logging.error(f"Произошла ошибка при получении данных: {e}")
            return []


class HhApiImplementation(HhApi):
    """Реализация класса HhApi."""

    def get_companies_and_vacancies(self, params):
        """Метод для получения списка компаний и вакансий на основе предоставленных параметров.

        Args:
            params (dict): Параметры для запроса к API.

        Returns:
            dict: Словарь, где ключи - названия компаний, значения - список вакансий.
        """
        endpoint = "/vacancies"
        data = self._get_vacancies(endpoint, params)
        formatted_companies_and_vacancies = defaultdict(list)

        for vacancy in data:
            company_name = vacancy.get("employer", {}).get("name", "Не указано")
            formatted_vacancy = {
                "name": vacancy.get("name", "Не указано"),
                "salary": vacancy.get("salary", "Не указано"),
                "url": vacancy.get("alternate_url", "Не указано"),
                "company_name": company_name
            }
            formatted_companies_and_vacancies[company_name].append(formatted_vacancy)

        return formatted_companies_and_vacancies

    def get_vacancies_by_employer(self, company_id):
        """Метод для получения списка вакансий для конкретной компании по её идентификатору.

        Args:
            company_id (str): Идентификатор компании.

        Returns:
            list: Список вакансий для данной компании.
        """
        endpoint = f"/vacancies?employer_id={company_id}"
        return self._get_vacancies(endpoint)
