from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

TOKEN = "8698093520:AAHlR_C4TQZPo3WmJ9tpCtPtrNk89uGoMQU"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n\n"
        "Men tarjima botiman.\n"
        "Menga istalgan tildagi matnni yuboring, men uni o'zbek tiliga tarjima qilaman."
    )

async def tarjima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = GoogleTranslator(source="auto", target="uz").translate(text)
    await update.message.reply_text(result)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tarjima))

print("✅ Bot ishga tushdi!")
app.run_polling()