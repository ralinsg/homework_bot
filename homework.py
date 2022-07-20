import logging
import os
import sys
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from errors import ErrorsStatuscode, ErrorsText
from telegram import Bot

load_dotenv()

"""Создаем логгер"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRY_TIME = 600
ENDPOINT = "https://practicum.yandex.ru/api/user_api/homework_statuses/"
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}


HOMEWORK_STATUSES = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания."
}


def send_message(bot, message) -> list:
    """Отправляет сообщение о статусе домашней работы."""
    logger.info("Отправялем сообщение пользователю")
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception:
        raise ErrorsText("Ошибка отправки сообщения в телеграм")


def get_api_answer(current_timestamp: int) -> dict:
    """Возвращает ответ API, преобразовав его к формату JSON."""
    logger.info("Возвращаем ответ API")
    timestamp = current_timestamp
    params = {"from_date": timestamp}
    response = requests.get(
        url=ENDPOINT,
        headers=HEADERS,
        params=params)
    if response.status_code == HTTPStatus.OK:
        return response.json()
    elif response.status_code != 200:
        raise ErrorsStatuscode("Ошибка статус кода")


def check_response(response: dict) -> list:
    """
    Проверяет ответ API на корректность.
    Возвращает список домашних работ.
    """
    logger.info("Проверка ответа API")
    if not isinstance(response, dict):
        raise TypeError("Неверный тип данных")
    if "homeworks" not in response:
        raise KeyError()
    homeworks = response.get("homeworks")
    if not isinstance(homeworks, list):
        raise TypeError(f"Ошибка доступа по ключу {homeworks}")
    elif len(homeworks) == 0:
        raise ValueError("Пустой словарь")

    return homeworks


def parse_status(homework: dict) -> str:
    """
    Извлекает из информации о конкретной домашней работе.
    Статус этой работы. И возвращает троку, содержащую один
    из вердиктов словаря HOMEWORK_STATUSES.
    """
    logger.info("Извлекаем информацию о домашней работе")
    homework_name = homework.get("homework_name")
    homework_status = homework.get("status")
    if homework_status not in HOMEWORK_STATUSES:
        raise KeyError(f"Ошибка извлечение статуса работы {homework_status}")
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens() -> bool:
    """Проверяем доступность переменных окружения."""
    logger.info("Проверка обязательных переменных окружения")
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        logger.critical("Отсутствие обязательных переменных окружения")
        sys.exit()
    logger.info("Заходим в бота")
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            status = parse_status(homeworks[0])
            send_message(bot, status)
            current_timestamp = response["current_date"]

        except Exception as error:
            message = f"Сбой в работе программы: {error}"
            logger.error(f"Возвращает пустой словарь {message}")
        finally:
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
