from src.config import config
from src.DBManager import DBManager
from src.vacancy import Vacancy
from src.HH import HH


def main() -> None:
    """Основная функция, запускающая проект!"""
    params = config()
    bd_user = input("Впишите название Базы данных: ")
    db = DBManager(bd_user, params)
    hh = HH()
    user_vacancies = input("Введите слово, по которому осуществляется поиск вакансий: ")
    vacancies = []
    for vacancy in hh.vacancies:
        vacancies.append(Vacancy.vacancy_from_hh(vacancy))
    db.add_vacancies(vacancies)

    if input("Произвести подсчет количества вакансий каждой компании? [Да/Нет] ").lower().strip() == "Да":
        print(db.get_companies_and_vacancies_count())

    if input("Желаете вывести название, зарплату и ссылку на вакансии? [Да/Нет] ").lower().strip() == "Да":
        print(db.get_all_vacancies())

    if input("Вывести среднюю зарплату вакансий? [Да/Нет] ").lower().strip() == "Да":
        print(db.get_avg_salary())

    if input("Отсортировать вакансии по заработной плате выше средней? [Да/Нет] ").lower().strip() == "Да":
        print(db.get_vacancies_with_higher_salary())

    if input(
            "Произвести вывод вакансий, в названии которых есть ваше введенное слово?"
            " (Впишите следующим пунктом) [Да/Нет] ").lower().strip() == "Да":
        print(db.get_vacancies_with_keyword(input("Введи слово: ")))


if __name__ == '__main__':
    main()
