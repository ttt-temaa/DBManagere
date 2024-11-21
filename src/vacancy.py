class Vacancy:
    """Класс работы с вакансиями"""

    def __init__(self, name: str, link: str, salary: float, requirement: str, employer_name: str):
        self.__name = name
        self.__link = link
        self.__salary = salary
        self.__requirement = requirement
        self.__employer_name = employer_name
        self.__validation()

    @property
    def salary(self) -> float:
        return self.__salary

    @property
    def name(self) -> str:
        return self.__name

    @property
    def link(self) -> str:
        return self.__link

    @property
    def requirement(self) -> str:
        return self.__requirement

    @property
    def employer_name(self) -> str:
        return self.__employer_name

    def __lt__(self, other: "Vacancy") -> bool:
        return self.__salary < other.salary

    def __le__(self, other: "Vacancy") -> bool:
        return self.__salary <= other.salary

    def __validation(self) -> None:
        """Метод для валидации вакансий"""
        if self.__salary is None:
            self.__salary = 0.0

        if self.__requirement is None:
            self.__requirement = "NotFound"

        if self.__employer_name is None:
            self.__employer_name = "NotFound"

    def __str__(self) -> str:
        return (
            f"Name vacancy: {self.__name}, link: {self.__link}, salary: {self.__salary}, requirement: "
            f"{self.__requirement}"
        )

    @classmethod
    def vacancy_from_hh(cls, data: dict) -> "Vacancy":
        """Метод для преобразования вакансий из hh.ru"""
        salary = data.get("salary")
        if salary is not None:
            if salary.get("to") is None:
                salary = salary.get("from")
            else:
                salary = salary.get("to")
        requirement = data.get("snippet")
        if requirement is not None:
            requirement = requirement.get("requirement")
        employer_name = data.get('employer')
        if employer_name is not None:
            employer_name = employer_name.get("name")
        return cls(
            name=data.get("name", "NotFound"),
            link=data.get("alternate_url", "error"),
            salary=salary,
            requirement=requirement,
            employer_name=employer_name
        )