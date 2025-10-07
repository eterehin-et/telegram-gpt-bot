import os
import time
import telebot
import openai
from collections import defaultdict, deque

# Загружаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

if not TELEGRAM_TOKEN or not OPENAI_KEY:
    raise RuntimeError("⚠️ Не установлены TELEGRAM_TOKEN и/или OPENAI_KEY")

# Инициализация клиентов
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_KEY

# Храним последние 3 сообщения для каждого пользователя
user_contexts = defaultdict(lambda: deque(maxlen=6))  
# (6 сообщений = 3 реплики пользователя + 3 ответа модели)

def ask_openai(user_id, new_message):
    """Отправляем контекст вместе с новым сообщением в OpenAI"""
    history = list(user_contexts[user_id])
    history.append({"role": "user", "content": new_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=history,
            max_tokens=800,
        )
        reply = response.choices[0].message["content"].strip()

        # Сохраняем новое сообщение и ответ в историю
        user_contexts[user_id].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        print(f"[Ошибка OpenAI] {e}")
        return "⚠️ Произошла ошибка при обращении к ChatGPT."

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        "👋 Привет! Я бот с ChatGPT. Пиши мне, и я постараюсь помочь.\n"
        "Я запоминаю последние 3 реплики, чтобы разговор был связным."
    )

@bot.message_handler(commands=['reset'])
def reset_context(message):
    """Сброс контекста"""
    user_contexts.pop(message.chat.id, None)
    bot.reply_to(message, "🧹 Контекст сброшен! Начинаем заново.")

@bot.message_handler(func=lambda msg: True)
def handle_message(message):
    user_id = message.chat.id
    text = message.text.strip()

    print(f"[{message.from_user.username}] {text}")

    reply = ask_openai(user_id, text)
    try:
        bot.reply_to(message, reply)
    except Exception as e:
        print("Ошибка при отправке ответа:", e)

if __name__ == "__main__":
    print("✅ Бот с контекстом запущен...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print("Ошибка polling:", e)
            time.sleep(5)
