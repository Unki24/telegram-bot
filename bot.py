from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import os

# Комплименты
romantic = ["Ты делаешь мою жизнь ярче одним взглядом ✨", "С тобой каждый момент кажется волшебным 🌟"]
motivational = ["Ты справишься — в тебе огромная сила 🔥", "Каждый шаг вперёд — уже победа 🏁"]
funny = ["Ты как Wi-Fi в кафе — притягиваешь всех без исключения 📶", "С тобой даже понедельник кажется пятницей 🎉"]
cozy = ["С тобой даже тишина уютная 🤍", "Ты — как плед, под который хочется спрятаться 🧺"]

# Обработка команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💖 Романтичный", callback_data='romantic')],
        [InlineKeyboardButton("🔥 Мотивационный", callback_data='motivational')],
        [InlineKeyboardButton("😂 Смешной", callback_data='funny')],
        [InlineKeyboardButton("🧸 Уютный", callback_data='cozy')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери комплимент:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data
    compliment = random.choice(globals()[category])
    await query.edit_message_text(text=compliment)

def main():
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()