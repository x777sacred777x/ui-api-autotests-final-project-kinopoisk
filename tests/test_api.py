# tests/test_api.py

import pytest
import requests
import allure
from typing import Dict
from config import BASE_URL_API, API_TOKEN


def get_headers() -> Dict[str, str]:
    """
    Вспомогательная функция для формирования заголовков запроса.
    Вынесена отдельно, чтобы не дублировать код в каждом тесте.
    :return: Словарь с заголовками, включая токен авторизации.
    """
    return {
        "accept": "application/json",
        "X-API-KEY": API_TOKEN
    }


@allure.epic("API Тесты")
@allure.feature("Фильтрация и поиск фильмов")
@pytest.mark.api
class TestMovieAPI:
    """Группа тестов для проверки API Кинопоиска."""

    @allure.story("Поиск по году и жанру")
    @allure.title("GET /movie - Поиск криминальных фильмов 2025 года")
    def test_get_movie_by_year_and_genre(self):
        # Параметры запроса
        params = {'year': 2025, 'genres.name': 'криминал', 'limit': 10}

        with allure.step(f"Отправка GET-запроса на {BASE_URL_API}/movie "
                         f"с параметрами: {params}"):
            response = requests.get(
                f"{BASE_URL_API}/movie",
                headers=get_headers(),
                params=params)

        with allure.step("Проверка: статус-код ответа равен 200 (OK)"):
            assert response.status_code == 200

        with allure.step("Проверка: тело ответа содержит ключ 'docs' "
                         "со списком фильмов"):
            response_data = response.json()
            assert "docs" in response_data
            assert isinstance(response_data["docs"], list)

    @allure.story("Поиск по нескольким жанрам и году")
    @allure.title("GET /movie - Поиск триллеров и драм 2025 года")
    def test_get_movie_by_multiple_genres(self):
        # Знак '+' перед жанром означает строгое соответствие (И)
        params = {
            'genres.name': [
                '+триллер',
                '+драма'],
            'year': 2025,
            'limit': 5}
        with allure.step(f"Отправка GET-запроса на {BASE_URL_API}/movie "
                         f"с параметрами: {params}"):
            response = requests.get(
                f"{BASE_URL_API}/movie",
                headers=get_headers(),
                params=params)

        with allure.step("Проверка: статус-код ответа равен 200 (OK)"):
            assert response.status_code == 200
        with allure.step("Проверка: тело ответа содержит ключ 'docs'"):
            assert "docs" in response.json()

    @allure.story("Поиск по одному жанру")
    @allure.title("GET /movie - Поиск 5 боевиков")
    def test_get_movie_by_genre_action(self):
        params = {'genres.name': 'боевик', 'limit': 5}
        with allure.step(f"Отправка GET-запроса на {BASE_URL_API}/movie "
                         f"с параметрами: {params}"):
            response = requests.get(
                f"{BASE_URL_API}/movie",
                headers=get_headers(),
                params=params)

        with allure.step("Проверка: статус-код ответа равен 200 (OK)"):
            assert response.status_code == 200

    @allure.story("Фильтрация по типу контента")
    @allure.title("GET /movie - Поиск 5 мультфильмов")
    def test_get_movie_by_type_cartoon(self):
        params = {'type': 'cartoon', 'limit': 5}
        with allure.step(f"Отправка GET-запроса на {BASE_URL_API}/movie "
                         f"с параметрами: {params}"):
            response = requests.get(
                f"{BASE_URL_API}/movie",
                headers=get_headers(),
                params=params)

        with allure.step("Проверка: статус-код ответа равен 200 (OK)"):
            assert response.status_code == 200

        with allure.step("Проверка: все найденные элементы имеют "
                         "тип 'cartoon'"):
            for item in response.json()['docs']:
                assert item['type'] == 'cartoon'

    @allure.story("Поиск по названию")
    @allure.title("GET /movie/search - Поиск фильма 'Матрица революция'")
    def test_search_movie_by_query(self):
        params = {'query': 'Матрица революция', 'limit': 1}
        with allure.step(f"Отправка GET-запроса "
                         f"на {BASE_URL_API}/movie/search "
                         f"с параметрами: {params}"):
            response = requests.get(
                f"{BASE_URL_API}/movie/search",
                headers=get_headers(),
                params=params)

        with allure.step("Проверка: статус-код ответа равен 200 (OK)"):
            assert response.status_code == 200

        with allure.step("Проверка: в результатах есть фильм, "
                         "содержащий 'Матрица: Революция'"):
            # any() вернет True, если хотя бы один элемент в списке
            # удовлетворяет условию
            assert any('Матрица: Революция' in item.get('name', '')
                       for item in response.json()['docs'])
