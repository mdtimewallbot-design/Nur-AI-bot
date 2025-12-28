import os
import asyncio
import nest_asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from flask import Flask
from threading import Thread

# Render-এর জন্য Flask সার্ভার (এটি বটকে ২৪ ঘণ্টা চালু রাখবে)
app = Flask('')

@app.route('/')
def home():
    return "নূর AI সচল আছে! ✨"

def run_flask():
    # Render-এর দেওয়া Port ব্যবহার করবে
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# তোর দেওয়া বটের কনফিগারেশন
TELEGRAM_TOKEN = "8097916754:AAE0OxXnzp72pSl9uj4bejdBbnsxBhTulMs"
OPENROUTER_API_KEY = "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"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # ছোট মেসেজের জন্য কম টোকেন, বড় উত্তরের জন্য বেশি টোকেন
    if user_input.lower() in ['ঠিক আছে', 'এখন না', 'পরে', 'ok'] or \
       any(word in user_input.lower() for word in ['hello','hi','hey']):
        max_tokens = 150
    else:
        max_tokens = 500

    data = {
        "model": "openai/gpt-4o",
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": (
                    "তোমার নাম 'নূর' ✨। তুমি অত্যন্ত বুদ্ধিমান, শিক্ষিত, সব বিষয় জানাশুনা AI 🧠📚। "
                    "সবসময় বাংলায় উত্তর দাও 🇧🇩। Casual chat -> সংক্ষিপ্ত reply। "
                    "Lesson -> বিস্তারিত ব্যাখ্যা। ইমোজি ব্যবহার করো 😊।"
                )
            },
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )
        reply = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        print(f"Error: {e}")

async def run_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 নূর AI এখন চালু আছে...")
    await application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    # Flask সার্ভার আলাদা থ্রেডে চালানো হচ্ছে
    t = Thread(target=run_flask)
    t.start()
    
    # টেলিগ্রাম বট চালানো হচ্ছে
    nest_asyncio.apply()
    asyncio.run(run_bot())
