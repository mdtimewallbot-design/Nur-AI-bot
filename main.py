import nest_asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = "8505632412:AAGDpWAjHYmcK6Rym96HzkRfMM3ay0eIp3Q"
OPENROUTER_API_KEY = "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"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # max_tokens control: casual chat small, lesson detailed
    if user_input.lower() in ['ঠিক আছে', 'এখন না', 'পরে', 'ok'] or \
       any(word in user_input.lower() for word in ['hello','hi','hey']):
        max_tokens = 180  # casual chat: 1–3 lines
    else:
        max_tokens = 500  # lesson / explanation: detailed

    data = {
        "model": "openai/gpt-4o",  # upgraded smart model
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "system",
                "content": (
                    "তোমার নাম 'নূর' ✨। তুমি অত্যন্ত বুদ্ধিমান, শিক্ষিত, সব বিষয় জানাশুনা AI 🧠📚। "
                    "তুমি মানুষের চেয়েও শিক্ষিত, পৃথিবীর প্রায় সব সাধারণ ও বিজ্ঞান বিষয় জানো 🌎। "
                    "Casual chat → ১–৩ লাইনের সংক্ষিপ্ত reply। "
                    "Lesson / explanation / grammar / example → যত দরকার detailed। "
                    "সবসময় বাংলায় উত্তর দাও 🇧🇩। User যদি English শেখার জন্য চায়, তখনই English 🇬🇧। "
                    "User যদি সাহায্য বা support offer দেয় → extra sentence দিবে না। "
                    "User যদি 'ঠিক আছে', 'এখন না', 'পরে', 'ok' বলে → ১–৩ লাইনের acknowledgement। "
                    "Lesson start হবে শুধুমাত্র যখন user লিখবে 'ইংরেজি শেখাও' বা 'Grammar শেখাও'। "
                    "Response এ ইমোজি থাকবে 😊।"
                )
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    reply = response.json()["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Nur AI is running...")
    await app.run_polling()

nest_asyncio.apply()
await main()
