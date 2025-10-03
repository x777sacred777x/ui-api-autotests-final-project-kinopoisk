# tests/test_ui.py

import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.advanced_search_page import AdvancedSearchPage


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script(
        "Object.defineProperty(navigator, "
        "'webdriver', {get: () => undefined})")
    yield driver
    driver.quit()


@allure.epic("UI Тесты")
@allure.feature("Расширенный поиск на Кинопоиске")
@pytest.mark.ui
class TestAdvancedSearch:

    @allure.story("Поиск по названию фильма")
    @allure.title("Тест поиска фильма 'Интерстеллар'")
    def test_search_by_title(self, driver):
        search_page = AdvancedSearchPage(driver)
        search_page.open()

        search_page.enter_title("Интерстеллар")
        search_page.click_search_main()

        results = search_page.get_search_result_titles()
        with allure.step("Проверка, что 'Интерстеллар' "
                         "есть в результатах поиска"):
            assert any("интерстеллар" in r.lower() for r in results), \
                f"Фильм 'Интерстеллар' не найден. Найдены: {results}"

    @allure.story("Поиск по жанру")
    @allure.title("Тест поиска по жанру 'фантастика'")
    def test_search_by_genre(self, driver):
        search_page = AdvancedSearchPage(driver)
        search_page.open()

        search_page.select_genre_fantastika()
        search_page.click_search_main()

        results = search_page.get_search_result_titles()
        with allure.step("Проверка, что результаты поиска не пустые"):
            assert len(
                results) > 0, "Результаты поиска по жанру 'фантастика' пусты"

    @allure.story("Поиск по актеру")
    @allure.title("Тест поиска по актеру 'Леонардо ДиКаприо'")
    def test_search_by_actor(self, driver):
        search_page = AdvancedSearchPage(driver)
        search_page.open()

        search_page.enter_actor("Леонардо ДиКаприо")
        search_page.click_search_actor()

        results = search_page.get_search_result_titles()
        with allure.step("Проверка, что найдены фильмы с Леонардо ДиКаприо"):
            assert len(results) > 0, "Фильмы с Леонардо ДиКаприо не найдены"

    @allure.story("Поиск по году")
    @allure.title("Тест поиска фильмов 2020 года")
    def test_search_by_year(self, driver):
        search_page = AdvancedSearchPage(driver)
        search_page.open()

        search_page.enter_year("2020")
        search_page.click_search_main()

        results = search_page.get_search_result_titles()
        with allure.step("Проверка, что результаты поиска не пустые"):
            assert len(results) > 0, "Фильмы 2020 года не найдены"

    @allure.story("Поиск по невалидному названию")
    @allure.title("Тест поиска по невалидному запросу")
    def test_search_by_invalid_name(self, driver):
        search_page = AdvancedSearchPage(driver)
        search_page.open()

        search_page.enter_title("абракадабрафыв12345несуществующийфильм")
        search_page.click_search_main()

        with allure.step("Проверка отображения сообщения о пустом результате"):
            assert search_page.is_empty_result_message_present(), \
                "Сообщение о пустом результате не найдено"
