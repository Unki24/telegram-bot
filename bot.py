import os
import random
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")

romantic_compliments = [
    "Ты — моё вдохновение 💖", "С тобой всё становится лучше 🌟", "Ты украшаешь собой этот мир 🌷",
    "Твоя улыбка лечит душу 😊", "Ты делаешь мой день особенным ☀️"
] * 20  # всего 100

motivational_compliments = [
    "Ты способен на всё 💪", "У тебя всё получится 🌈", "Ты светишься уверенностью 🔥",
    "Ты — сила, которая движет мир 🌍", "Ты вдохновляешь не только себя, но и других 🌟"
] * 20

funny_compliments = [
    "Ты как Wi-Fi — всегда притягиваешь 😄", "Ты смешнее мемов в 3 ночи 😂", "С тобой весело даже молчать 🤪",
    "Ты как кот в интернете — невозможно не залипнуть 🐱", "Ты — ходячий позитив 🎉"
] * 20

cozy_compliments = [
    "Ты как одеяло в холодную ночь 🧸", "С тобой уютно даже в бурю 🌧️", "Ты — моя зона комфорта ☕",
    "С тобой всегда тепло, даже без пледа 🔥", "Ты словно любимая книга перед сном 📖"
] * 20

def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💖 Романтичный", callback_data="romantic")],
        [InlineKeyboardButton("🔥 Мотивационный", callback_data="motivational")],
        [InlineKeyboardButton("😂 Смешной", callback_data="funny")],
        [InlineKeyboardButton("🧸 Уютный", callback_data="cozy")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Выбери категорию комплиментов 👇", reply_markup=build_keyboard())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    compliments = {
        "romantic": romantic_compliments,
        "motivational": motivational_compliments,
        "funny": funny_compliments,
        "cozy": cozy_compliments
    }.get(query.data, [])

    if compliments:
        await query.message.reply_text(random.choice(compliments))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    application.update_queue.put_nowait(Update.de_json(request.get_json(force=True), application.bot))
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    application.bot.delete_webhook()
    application.bot.set_webhook(url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))