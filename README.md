# :computer: Курсовая 5 - Работа с базами данных

## О проекте

Этот проект представляет собой базу данных для хранения информации о вакансиях различных компаний, полученных с 
использованием API hh.ru. Компании перечисленны в словаре, в файле data/companies.py.

## Используемые технологии

- Python
- PostgreSQL
- psycopg2 (для работы с PostgreSQL)
- requests (для работы с API hh.ru)
- python-dotenv
- pytest
- flake8

## Установка и запуск

### Склонируйте репозиторий:
```bash
git clone https://github.com/CHAPAPOPA/Skypro_kyrsovaya_5.git
```
### Перейдите в папку с проектом
```bash
cd Skypro_kyrsovaya_5
```
### Установите зависимости:
Сначала активируем poetry
```bash
poetry shell
```
Затем установим все зависимости из pyproject.toml
```bash
poetry install
```
### Запустите программу:

```bash
python src\main.py
```

## Структура проекта

### Skypro_kyrsovaya_5
- `data`
  - `companies.py`
- `src`
  - `init.py`
  - `db_manager.py`
  - `hh_api.py`
  - `utils.py`
- `tests`
  - `init.py`
  - `hh_api_test.py`
- `config.py`
- `main.py`
- `flake8`
- `poetry.lock`
- `pyproject.toml`
