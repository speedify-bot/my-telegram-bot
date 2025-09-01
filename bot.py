import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# ===========================
# توکن تلگرام: از Environment Variable میاد
# ===========================
TOKEN = os.getenv("TELEGRAM_TOKEN")

# ===========================
# فانکشن Start
# ===========================
async def start(update: Update, context):
    await update.message.reply_text(
        "سلام! ربات آماده است.\n"
        "لینک موزیک ارسال کن یا /price <symbol> برای قیمت رمزارز استفاده کن."
    )

# ===========================
# دریافت قیمت رمزارز
# ===========================
async def price(update: Update, context):
    if len(context.args) == 0:
        await update.message.reply_text("لطفا یک نماد وارد کن، مثال: /price btc")
        return

    symbol = context.args[0].lower()
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"

    try:
        response = requests.get(url).json()
        if symbol in response:
            price_usd = response[symbol]["usd"]
            await update.message.reply_text(f"قیمت {symbol.upper()} الان: ${price_usd}")
        else:
            await update.message.reply_text("رمزارز پیدا نشد، لطفا نماد درست وارد کن.")
    except Exception as e:
        await update.message.reply_text(f"خطا در دریافت قیمت: {e}")

# ===========================
# دانلود موزیک از لینک (ساده)
# ===========================
async def download_music(update: Update, context):
    text = update.message.text
    # برای تست ساده فقط لینک رو برمیگردونه
    await update.message.reply_text(f"لینک دریافت شد: {text}\n(اینجا میتونی کد دانلود واقعی اضافه کنی)")

# ===========================
# main
# ===========================
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_music))

    print("ربات در حال اجراست...")
    app.run_polling()

