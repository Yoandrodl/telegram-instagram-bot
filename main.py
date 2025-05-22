from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Kirim link Instagram (Reels, Post, atau Story) ke bot ini.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "instagram.com" in url:
        await update.message.reply_text("Sedang mengambil media, tunggu sebentar...")

        try:
            ig_api = "https://igram.io/i/"
            response = requests.post(ig_api, data={"url": url})
            if response.ok:
                await update.message.reply_text("Media berhasil diambil (perlu parsing detail).")
                await update.message.reply_text(response.text[:1000])
            else:
                await update.message.reply_text("Gagal mengambil media dari Instagram.")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
    else:
        await update.message.reply_text("Link tidak dikenali. Kirim link Instagram yang valid ya!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
