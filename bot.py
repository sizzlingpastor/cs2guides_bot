import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Вставь сюда токен от BotFather
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Текст приветствия с жирным заголовком
welcome_text = (
    "*КАК ЖЕ ПЛОХО ОПТИМИЗИРОВАНА CS2!.. 👿*\n\n"
    "Игра лагает даже на топовых ПК. Забирай 2 эффективных гайда, как повысить FPS — пользуемся сами.\n\n"
    "🔽 Подпишись на [Контрач](https://t.me/+nlO1yhckyvg1NWVi), чтобы забрать гайд"
)

# Кнопка "Готово" для проверки подписки
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

# Команда /start
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

bot.polling()

