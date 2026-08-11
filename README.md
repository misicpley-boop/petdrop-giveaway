# PetDrop

Безопасный сайт раздачи виртуальных питомцев. Он принимает только игровой ник и выбранного питомца. Пароли, cookies и токены Roblox не собираются.

## Локальный запуск
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
set ADMIN_PASSWORD=your-admin-password
python app.py

## Публичный запуск
Проект подготовлен для Render. Загрузите папку в GitHub и создайте Web Service на Render. Build command: `pip install -r requirements.txt`. Start command: `gunicorn app:app`. В Environment задайте ADMIN_PASSWORD.

## Важно
Не используйте официальный логотип/домен Roblox или Adopt Me и не просите у пользователей реальные пароли.
