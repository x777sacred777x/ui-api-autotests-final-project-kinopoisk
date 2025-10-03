# pages/base_page.py

from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """
    Базовый класс для всех страниц. Реализует основные методы
    для работы с WebDriver.
    """

    def __init__(self, driver: WebDriver, url: str):
        self.driver = driver
        self.url = url

    def open(self) -> None:
        """Открывает URL страницы в браузере."""
        self.driver.get(self.url)

    def find_element(
            self, locator: Tuple[str, str], time: int = 10) -> WebElement:
        """
        Находит один элемент на странице с использованием явного ожидания.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator),
            message=f"Не удалось найти элемент по локатору {locator}"
        )

    def find_elements(
            self, locator: Tuple[str, str], time: int = 10) -> list[WebElement]:
        """
        Находит все элементы на странице, соответствующие локатору.
        """
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_all_elements_located(locator),
            message=f"Не удалось найти элементы по локатору {locator}"
        )

    def wait_for_element_clickable(
            self, locator: Tuple[str, str], time: int = 10) -> WebElement:
        """
        Ожидает, пока элемент станет кликабельным.
        """
        return WebDriverWait(
            self.driver,
            time).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент по локатору {locator} "
                    f"не стал кликабельным за {time} секунд")

    def wait_for_element_visible(
            self, locator: Tuple[str, str], time: int = 10) -> WebElement:
        """
        Ожидает, пока элемент станет видимым.
        """
        return WebDriverWait(
            self.driver,
            time).until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент по локатору {locator} "
                    f"не стал видимым за {time} секунд")
