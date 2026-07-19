
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
import easyocr
import os

TOKEN = "8698093520:AAF9kS2wJUPVzxlTtyuwES-nP1WRC6op_co"

reader = easyocr.Reader(['en'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom!\n"
        "Matn yoki rasm yuboring. Men tarjima qilaman."
    )

async def tarjima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        result = GoogleTranslator(source="auto", target="uz").translate(text)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ Tarjima xatosi.")

async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    await file.download_to_drive("image.jpg")

    try:
        matn = "\n".join(reader.readtext("image.jpg", detail=0))

        if not matn:
            await update.message.reply_text("Rasmda matn topilmadi.")
            return

        tarjima = GoogleTranslator(source="auto", target="uz").translate(matn)

        await update.message.reply_text(
            f"📄 Matn:\n{matn}\n\n🌐 Tarjima:\n{tarjima}"
        )

    finally:
        if os.path.exists("image.jpg"):
            os.remove("image.jpg")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tarjima))
app.add_handler(MessageHandler(filters.PHOTO, photo))

print("Bot ishga tushdi.")
app.run_polling()
