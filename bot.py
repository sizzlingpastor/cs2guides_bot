import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request

# ===== Настройки бота =====
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN в переменных окружения!")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Текст приветствия с жирным заголовком
welcome_text = (
    "*КАК ЖЕ ПЛОХО ОПТИМИЗИРОВАНА CS2!.. 👿*\n\n"
    "Игра лагает даже на топовых ПК. Забирай 2 эффективных гайда, как повысить FPS — пользуемся сами.\n\n"
    "🔽 Подпишись на [Контрач](https://t.me/+nlO1yhckyvg1NWVi), чтобы забрать гайд"
)

# Кнопка "Готово" для проверки подписки (пока что не проверяет реально подписан ли юзер)
def get_ready_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Готово ✅", callback_data="ready")
    keyboard.add(button)
    return keyboard

# Кнопка-ссылка для выдачи гида
def get_guide_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Посмотреть гайд", url="https://t.me/c/1909782692/309")
    keyboard.add(button)
    return keyboard

# ===== Хэндлеры =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=get_ready_keyboard()
    )

# Обработка нажатия кнопки "Готово"
@bot.callback_query_handler(func=lambda call: call.data == "ready")
def handle_ready(call):
    bot.answer_callback_query(call.id)  # скрывает "часики" на кнопке
    bot.send_message(
        call.message.chat.id,
        "Спасибо за подписку! Вот обещанный гайд!",
        reply_markup=get_guide_keyboard()
    )

# ===== Flask webhook =====
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def home():
    return "Бот cs2guides_bot живой!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Устанавливаем webhook при запуске
    APP_URL = os.getenv("RENDER_EXTERNAL_URL")
    if not APP_URL:
        raise ValueError("Не найден RENDER_EXTERNAL_URL! Render сам его подставляет.")
    webhook_url = f"{APP_URL}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    print(f"Webhook установлен: {webhook_url}")
    app.run(host="0.0.0.0", port=port)

