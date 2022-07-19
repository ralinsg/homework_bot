import os
import sys
import time
import logging
import requests
from http import HTTPStatus
from telegram import Bot
from dotenv import load_dotenv

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
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message) -> list:
    """Отправляет сообщение о статусе домашней работы."""
    logger.info("Отправялем сообщение пользователю")
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)


def get_api_answer(current_timestamp: int) -> list:
    """Возвращает ответ API, преобразовав его к формату JSON."""
    logger.info("Возвращаем ответ API")
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    try:
        logger.info("Обращение к эндпоинту")
        api_response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params=params)
    except Exception:
        logger.error("Ошибка при запросе к API")
    if api_response.status_code == HTTPStatus.OK:
        return api_response.json()
    elif api_response.status_code != 200:
        logger.error("Ошибка статус кода")
        raise Exception


def check_response(response: list) -> list:
    """
    Проверяет ответ API на корректность.
    Возвращает список домашних работ.
    """
    logger.info("Проверка ответа API")
    try:
        homeworks_list = response["homeworks"]
    except KeyError:
        logger.error("Ошибка доступа по ключу")
    if not isinstance(homeworks_list, list):
        raise KeyError
    return homeworks_list


def parse_status(homework: dict) -> str:
    """
    Извлекает из информации о конкретной домашней работе.
    Статус этой работы. И возвращает троку, содержащую один
    из вердиктов словаря HOMEWORK_STATUSES.
    """
    logger.info("Извлекаем информацию о домашней работе")
    homework_name = homework["homework_name"]
    print(homework_name)
    homework_status = homework["status"]
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens() -> bool:
    """Проверяем доступность переменных окружения."""
    logger.info("Проверка обязательных переменных окружения")
    if (
        PRACTICUM_TOKEN is None
        or TELEGRAM_TOKEN is None
        or TELEGRAM_CHAT_ID is None
    ):
        return False
    return True


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        logger.critical("Отсутствие обязательных переменных окружения")
        exit()
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
            print(f"Время запроса {current_timestamp}")
            time.sleep(RETRY_TIME)

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(f"Возвращает пустой словарь {message}")
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
