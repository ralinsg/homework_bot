
import logging
import time
from telegram import Bot
import requests
from_date = 0
TELEGRAM_TOKEN = "5514799309:AAGAveZP67Y6nO3ePAaS64Ho-YAkTCmXrxE"
TELEGRAM_CHAT_ID = 81848
PRACTICUM_TOKEN = "AQAAAAAauEGfAAYckfJD6IniRkHhnOTzg6Szf7U"
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)


def send_message(bot, text):
    text = "Hi"
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  # начальное значение timestamp или 0
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        api_response = requests.get(
            url=ENDPOINT,
            headers=HEADERS,
            params=params)
    except Exception:
        logging.error("Ошибка при запросе к API")
        response = api_response.json()

if __name__ == "__main__":
    main()
