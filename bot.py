import os
import random
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, CallbackQueryHandler

TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)
app = Flask(__name__)

romantic = ["Ты делаешь мою жизнь ярче одним взглядом ✨", "С тобой каждый момент кажется волшебным 🌟"]
motivational = ["Ты справишься — в тебе огромная сила 🔥", "Каждый шаг вперёд — уже победа 🏁"]
funny = ["Ты как Wi-Fi в кафе — притягиваешь всех без исключения 📶", "С тобой даже понедельник кажется пятницей 🎉"]
cozy = ["С тобой даже тишина уютная 🤍", "Ты — как плед, под который хочется спрятаться 🧺"]

dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

def start(update, context):
    keyboard = [
        [InlineKeyboardButton("💖 Романтичный", callback_data='romantic')],
        [InlineKeyboardButton("🔥 Мотивационный", callback_data='motivational')],
        [InlineKeyboardButton("😂 Смешной", callback_data='funny')],
        [InlineKeyboardButton("🧸 Уютный", callback_data='cozy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выбери комплимент:", reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query
    category = query.data
    compliment = random.choice(globals()[category])
    query.edit_message_text(text=compliment)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))