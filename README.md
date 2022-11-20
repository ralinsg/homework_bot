
# Приложение homework_bot

Telegramm-бот, оповещающий о статусе домашнего задания студента Яндекс.Практикума, с системой логирования ошибок.



## Структура работы:

- Направляется запрос к API сервису Практикум.Домашка 
- Приложение проверяет статус отправленной на ревью домашней работы.
- При обновлении статуса анализирует ответ API и отправляет соответствующее уведомление в Telegram.
- Логирует свою работу и сообщает о важных проблемах в Telegram.
- С помощью пакета python-dotenv переменные окружения загружаются из файла .env и являются недоступными в коде программы, что позволяет обеспечить защиту персональных данных.


## Технологический стек:

- Python 3
- python-telegram-bot
- python-dotenv
- logging
- Clinet API
- Bot API
- JSON




## Установка приложения:

Клонировать репозиторий:

```bash
 git clone git@github.com:ralinsg/homework_bot.git

```
Перейти в склонированный репозиторий:
```bash
 cd homework_bot
```
Cоздать виртуальное окружение:
```bash
py -3.7 -m venv venv 
```
Активировать виртуальное окружение:
```bash
 source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```bash
 pip install -r requirements.txt
```
Создать файл .env со следующими данными:
```bash
PRACTICUM_TOKEN=<Ваш токен Яндекс.Практикума>
TELEGRAM_TOKEN=<Токен telegramm-бота>
TELEGRAM_CHAT_ID=<Ваш id в telegramm>
```

## Запуск проекта:

```bash
 python homework.py
```


## Автор

- [@ralinsg](https://github.com/ralinsg)

