# 🤖 Telegram ChatGPT Bot

Бот, который подключается к OpenAI GPT-4o-mini и отвечает пользователям в Telegram.

---

## 🔧 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/USERNAME/telegram-gpt-bot.git
   cd telegram-gpt-bot
2. Создайте виртуальную среду и установите зависимости:
   ```bash
   python -m venv venv
   source venv/bin/activate   # (Windows: .\venv\Scripts\Activate.ps1)
   pip install -r requirements.txt

3. Установите переменные окружения:
   ```bash
   export TELEGRAM_TOKEN="ваш_токен_от_BotFather"
   export OPENAI_KEY="ваш_API_ключ_OpenAI"

4. Запустите
   ```bash
   python bot.py
