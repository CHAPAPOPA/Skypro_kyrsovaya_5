import pytest
from unittest.mock import MagicMock, patch
from src.hh_api import HhApiImplementation


@pytest.fixture
def mock_response():
    response = MagicMock()
    response.json.return_value = {
        "items": [
            {
                "employer": {"name": "Company1"},
                "name": "Vacancy1",
                "salary": {"from": 1000, "to": 2000, "currency": "RUB"},
                "alternate_url": "http://example.com/vacancy1"
            },
            {
                "employer": {"name": "Company2"},
                "name": "Vacancy2",
                "salary": {"from": None, "to": None, "currency": None},
                "alternate_url": "http://example.com/vacancy2"
            }
        ]
    }
    return response


@patch('requests.get')
def test_get_companies_and_vacancies(mock_get, mock_response):
    mock_get.return_value = mock_response

    api = HhApiImplementation()
    params = {'param1': 'value1', 'param2': 'value2'}
    result = api.get_companies_and_vacancies(params)

    assert isinstance(result, dict)
    assert "Company1" in result
    assert "Company2" in result
    assert len(result["Company1"]) == 1
    assert len(result["Company2"]) == 1

    vacancy1 = result["Company1"][0]
    vacancy2 = result["Company2"][0]

    assert vacancy1["name"] == "Vacancy1"
    assert vacancy1["salary"] == {"from": 1000, "to": 2000, "currency": "RUB"}
    assert vacancy1["url"] == "http://example.com/vacancy1"
    assert vacancy1["company_name"] == "Company1"

    assert vacancy2["name"] == "Vacancy2"
    assert vacancy2["salary"] == {"from": None, "to": None, "currency": None}
    assert vacancy2["url"] == "http://example.com/vacancy2"
    assert vacancy2["company_name"] == "Company2"


@patch('requests.get')
def test_get_vacancies_by_employer(mock_get, mock_response):
    mock_get.return_value = mock_response

    api = HhApiImplementation()
    company_id = "12345"
    result = api.get_vacancies_by_employer(company_id)

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["employer"]["name"] == "Company1"
    assert result[1]["employer"]["name"] == "Company2"
