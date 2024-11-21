import psycopg2

from src.vacancy import Vacancy
from src.config import config
from src.HH import HH
from psycopg2.extensions import connection, cursor


class DBManager:
    """Класс, который подключается к Базе данных PostgreSQL"""

    def __init__(self, database_name: str, params: dict):
        """Метод инициализации"""
        self.database_name = database_name
        self.params = params

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database_name}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {database_name}')

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                           CREATE TABLE IF NOT EXISTS employers (
                               id SERIAL PRIMARY KEY,
                               employer_name VARCHAR(255) NOT NULL UNIQUE
                           )
                       """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        link VARCHAR(255),
                        salary FLOAT,
                        requirement TEXT,
                        employer_id INTEGER REFERENCES employers(id)
                    )
                """)
        conn.commit()
        conn.close()

    def in_employers(self, employer_name: str) -> bool:
        """Функция проверки компании"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()

        cur.execute(
            f"""
            SELECT EXISTS(SELECT 1 FROM employers WHERE employer_name = '{employer_name}');
            """
        )
        return cur.fetchone()[0]

    def add_employer(self, employer_name: str, conn: connection, cur: cursor) -> int:
        """Метод добавления работодателей в компанию"""
        cur.execute(
            f"""
            INSERT INTO employers (employer_name)
            VALUES ('{employer_name}')
            RETURNING *
            """)
        conn.commit()
        return cur.fetchone()[0]

    def add_vacancies(self, data: list[Vacancy]) -> None:
        """Метод добавления вакансий в Базу данных"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        for vacancy in data:
            if not self.in_employers(vacancy.employer_name):
                id_ = self.add_employer(vacancy.employer_name, conn, cur)
            else:
                cur.execute(
                    f"""
                    SELECT id FROM employers WHERE employer_name = '{vacancy.employer_name}'
                    """
                )
                id_ = cur.fetchone()[0]
            print(id_)
            cur.execute(
                """
                INSERT INTO vacancies (name, link, salary, requirement, employer_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """, [vacancy.name, vacancy.link, vacancy.salary, vacancy.requirement, id_])
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> list:
        """Метод, который получает список и вакансиивсех компаний"""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT employer_name, COUNT(*) FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            GROUP BY employer_name
            """
        )

        return cur.fetchall()

    def get_all_vacancies(self) -> list:
        """Метод, получения всех вакансий с указанием названия,
        вакансии, зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT employer_name, name, salary, link FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.id
            """
        )

        return cur.fetchall()

    def get_avg_salary(self) -> float:
        """Метод, который получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT AVG(salary) FROM vacancies
            """
        )

        return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> list:
        """Метод, который получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """
        )

        return cur.fetchall()

    def get_vacancies_with_keyword(self, word: str) -> list:
        """Метод получает список всех вакансий, в названии, которых содержатся
        переданные в метод слова, например - python."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT * FROM vacancies
            WHERE name LIKE '%{word}%'
            """
        )

        return cur.fetchall()


params = {"host": "localhost",
          "user": "postgres",
          "password": "artemtrololo",
          "port": "5432"}
