# Yandex disk API interaction app

Приложение позволяет взаимодействовать с файлами Яндекс диска, расположенными по публичной ссылке.

## Взаимодействие:
1. Вы вводите публичный ключ (ссылка на ресурс Яндекс диска, к которому вам необходимо получить доступ).
2. Вы можете видеть все свои файлы, папки и подпапки.
3. Вы можете скачать выбранный вами файл.

## Локальный запуск:

### Через Docker:
1. Клонировать репозиторий: `git clone https://github.com/janetuyy/yadisk_app.git`
2. Перейти к папке проекта: `cd yadisk_app`
3. Создать изображение docker: `docker build -t имя_изображения .`
4. Запустить контейнер с пробросом портов: `docker run —name имя_контейнера -p 8000:8000 -d имя_изображения`
Приложение будет доступно по адресу: http://localhost:8000/

### Без использования Docker:
1. Клонировать репозиторий: `git clone https://github.com/janetuyy/yadisk_app.git`
2. Перейти к папке проекта: `cd yadisk_app`
3. Создать и активировать виртуальное окружение: `python -m venv venv`
`venv/Scripts/activate`
3. Установить зависимости: `pip install -r requirements.txt`
4. Применить миграции для БД: `python manage.py migrate`
5. Запустить локальный сервер: `python manage.py runserver`
Приложение будет доступно по адресу: http://127.0.0.1:8000/
