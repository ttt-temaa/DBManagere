from abc import ABC, abstractmethod
from typing import Any

import requests


class Parser(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str, pages: int = 20) -> None:
        pass


class HH(Parser):
    """
    Класс для работы с API HeadHunter
    Класс Parser является родительским классом, который вам необходимо реализовать
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params: Any = {"text": "", "page": 0, "per_page": 100, "search_fields": ["skills", "title"]}
        self.__vacancies: list = []

    @property
    def url(self) -> str:
        return self.__url

    @property
    def headers(self) -> dict:
        return self.__headers

    @property
    def params(self) -> Any:
        return self.__params

    @property
    def vacancies(self) -> list:
        return self.__vacancies

    def __connect_api(self) -> None:
        """Метод подключения к API hh.ru"""
        response = requests.get(self.__url, headers=self.__headers, params=self.__params)
        if response.ok:
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)

    def load_vacancies(self, keyword: str, pages: int = 20) -> None:
        """Метод, который загружает вакансии из hh.ru"""
        self.__params["text"] = keyword
        while self.__params.get("page") != pages:
            self.__connect_api()
            self.__params["page"] += 1