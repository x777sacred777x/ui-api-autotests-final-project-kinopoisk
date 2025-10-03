# pages/advanced_search_page.py

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
from config import ADVANCED_SEARCH_URL


class AdvancedSearchLocators:
    """
    Локаторы для страницы https://www.kinopoisk.ru/s/
    """

    # --- Поля ввода ---
    TITLE_INPUT = (By.XPATH, '//*[@id="find_film"]')
    ACTOR_INPUT = (By.XPATH, '//*[@id="find_people"]')
    YEAR_INPUT = (By.XPATH, '//*[@id="year"]')

    # --- Жанры ---
    GENRE_FANTASTIKA = (By.XPATH, '//*[@id="m_act[genre]"]/option[30]')

    # --- Кнопки поиска ---
    SEARCH_BUTTON_MAIN = (By.XPATH, '//*[@id="formSearchMain"]/input[11]')
    SEARCH_BUTTON_ACTOR = (By.XPATH, '//*[@id="searchAdv"]/form[3]/input[10]')

    # --- Результаты ---
    SEARCH_RESULT_TITLES = (By.XPATH, '//a[contains(@href, "/film/")]')
    EMPTY_RESULT_MESSAGE = (
        By.XPATH,
        '//*[contains(text(), "ничего не найдено") or contains(text(),'
        ' "Не найдено")]')


class AdvancedSearchPage(BasePage):
    """
    Класс для работы со страницей расширенного поиска.
    """

    def __init__(self, driver):
        super().__init__(driver, ADVANCED_SEARCH_URL)

    def open(self) -> None:
        super().open()
        self.wait_for_page_load()

    def wait_for_page_load(self, timeout=15):
        WebDriverWait(
            self.driver, timeout).until(
            lambda d: d.execute_script("return "
                                       "document.readyState") == "complete")

    @allure.step("Ввод названия фильма: '{title}'")
    def enter_title(self, title: str) -> None:
        field = self.wait_for_element_clickable(
            AdvancedSearchLocators.TITLE_INPUT)
        field.clear()
        field.send_keys(title)

    @allure.step("Ввод имени актера: '{actor}'")
    def enter_actor(self, actor: str) -> None:
        field = self.wait_for_element_clickable(
            AdvancedSearchLocators.ACTOR_INPUT)
        field.clear()
        field.send_keys(actor)

    @allure.step("Ввод года: '{year}'")
    def enter_year(self, year: str) -> None:
        field = self.wait_for_element_clickable(
            AdvancedSearchLocators.YEAR_INPUT)
        field.clear()
        field.send_keys(year)

    @allure.step("Выбор жанра 'фантастика'")
    def select_genre_fantastika(self) -> None:
        option = self.wait_for_element_clickable(
            AdvancedSearchLocators.GENRE_FANTASTIKA)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", option)
        option.click()

    @allure.step("Нажатие на кнопку поиска (основная форма)")
    def click_search_main(self) -> None:
        button = self.wait_for_element_clickable(
            AdvancedSearchLocators.SEARCH_BUTTON_MAIN)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button)
        # JS‑клик вместо обычного
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Нажатие на кнопку поиска (по актёрам)")
    def click_search_actor(self) -> None:
        button = self.wait_for_element_clickable(
            AdvancedSearchLocators.SEARCH_BUTTON_ACTOR)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Получение заголовков результатов поиска")
    def get_search_result_titles(self) -> list[str]:
        WebDriverWait(
            self.driver,
            15).until(
            lambda d: d.find_elements(
                *
                AdvancedSearchLocators.SEARCH_RESULT_TITLES) or d.find_elements(
                *
                AdvancedSearchLocators.EMPTY_RESULT_MESSAGE))
        elements = self.find_elements(
            AdvancedSearchLocators.SEARCH_RESULT_TITLES, time=5)
        return [el.text.strip() for el in elements if el.text.strip()]

    @allure.step("Проверка наличия сообщения о пустом результате")
    def is_empty_result_message_present(self) -> bool:
        elements = self.find_elements(
            AdvancedSearchLocators.EMPTY_RESULT_MESSAGE, time=5)
        return len(elements) > 0
