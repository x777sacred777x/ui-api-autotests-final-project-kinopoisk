# config.py

import os
from dotenv import load_dotenv

load_dotenv()

# URL для страницы расширенного поиска
BASE_URL_UI = "https://www.kinopoisk.ru/"
ADVANCED_SEARCH_URL = "https://www.kinopoisk.ru/s/"

# Базовый URL для всех запросов к API
BASE_URL_API = "https://api.kinopoisk.dev/v1.4"

# Получаем значение API-токена из переменных окружения
API_TOKEN = os.getenv("KINOPOISK_API_TOKEN")

if not API_TOKEN:
    raise ValueError(
        "Не найден API-токен. Проверьте наличие файла .env "
        "и переменной KINOPOISK_API_TOKEN")
