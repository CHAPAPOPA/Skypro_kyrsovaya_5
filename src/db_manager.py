import psycopg2
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DBManager:
    def __init__(self, db_params):
        self.conn = psycopg2.connect(**db_params)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) UNIQUE
            )
        ''')
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(id),
                title VARCHAR(255),
                min_salary INTEGER,
                max_salary INTEGER,
                currency VARCHAR(10),
                url VARCHAR(255)
            )
        ''')
        self.conn.commit()

    def insert_data_batch(self, data):
        for entry in data:
            company_name = entry.get('company_name', 'Unknown Company')
            vacancies = entry.get('vacancies', [])

            self.cur.execute('''
                INSERT INTO companies (name) VALUES (%s)
                ON CONFLICT (name) DO NOTHING
            ''', (company_name,))

            self.cur.execute('SELECT id FROM companies WHERE name = %s', (company_name,))
            company_id = self.cur.fetchone()[0]

            for vacancy in vacancies:
                title = vacancy.get('name', 'Unknown Title')

                salary_data = vacancy.get('salary')
                from_salary = salary_data.get('from') if salary_data else 0
                to_salary = salary_data.get('to') if salary_data else 0
                currency = salary_data.get('currency') if salary_data else None

                url = vacancy.get('url', 'Unknown Link')

                self.cur.execute('''
                    INSERT INTO vacancies (company_id, title, min_salary, max_salary, currency, url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (company_id, title, from_salary, to_salary, currency, url))

            logger.info("Inserted data for company: %s", company_name)  # Добавлено логгирование

        self.conn.commit()

    def insert_vacancies(self, company_name, vacancies):
        self.cur.execute('''
            INSERT INTO companies (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        ''', (company_name,))

        self.cur.execute('SELECT id FROM companies WHERE name = %s', (company_name,))
        company_id = self.cur.fetchone()[0]

        for vacancy in vacancies:
            title = vacancy.get('name', 'Unknown Title')

            salary_data = vacancy.get('salary')
            from_salary = salary_data.get('from') if salary_data else 0
            to_salary = salary_data.get('to') if salary_data else 0
            currency = salary_data.get('currency') if salary_data else None

            url = vacancy.get('url', 'Unknown Link')

            self.cur.execute('''
                INSERT INTO vacancies (company_id, title, min_salary, max_salary, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (company_id, title, from_salary, to_salary, currency, url))

    def get_companies_and_vacancies_count(self):
        self.cur.execute('''
            SELECT companies.name, COUNT(vacancies.id) 
            FROM companies 
            LEFT JOIN vacancies ON companies.id = vacancies.company_id 
            GROUP BY companies.name
        ''')
        return self.cur.fetchall()

    def get_all_vacancies(self):
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary, vacancies.max_salary, vacancies.currency, vacancies.url 
            FROM vacancies 
            JOIN companies ON vacancies.company_id = companies.id
        ''')
        return self.cur.fetchall()

    def get_avg_salary(self):
        self.cur.execute('''
                SELECT AVG(
                    CASE
                        WHEN vacancies.min_salary IS NOT NULL THEN vacancies.min_salary
                        WHEN vacancies.max_salary IS NOT NULL THEN vacancies.max_salary
                        ELSE NULL
                    END
                )
                FROM vacancies
            ''')
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary, vacancies.max_salary, vacancies.currency, vacancies.url
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
            WHERE
                -- Условие сравнения зарплаты средней зарплаты
                (vacancies.min_salary > %s OR vacancies.max_salary > %s)
        ''', (avg_salary, avg_salary))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute('''
            SELECT companies.name, vacancies.title, vacancies.min_salary, vacancies.max_salary, vacancies.currency, vacancies.url
            FROM vacancies 
            JOIN companies ON vacancies.company_id = companies.id
            WHERE LOWER(vacancies.title) LIKE %s
        ''', ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()

    def close_connection(self):
        self.cur.close()
        self.conn.close()
