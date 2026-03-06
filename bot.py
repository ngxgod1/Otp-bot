import requests
import time
import re
import telegram
import phonenumbers
from phonenumbers import geocoder
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = "8642429610:AAFFllSv1R4k7hP3f69jIm2a46eNw_LIlE0"
CHAT_ID = -1003776501180

API_URL = "http://147.135.212.197/crapi/time/viewstats"
TOKEN = "RFZWNEVBdlJ7iWhFfGZYan1UgWFqZIOGX2KChVxjmFt7aZVza4w="

bot = telegram.Bot(token=BOT_TOKEN)

sent = set()

print("✅ OTP Forwarder Started...")

while True:

    try:

        r = requests.get(API_URL, params={"token": TOKEN}, timeout=20)
        data = r.json()

        if "data" not in data:
            time.sleep(5)
            continue

        entries = data["data"]

        for sms in entries:

            number = sms.get("num")
            message = sms.get("message")
            dt = sms.get("dt")
            service = str(sms.get("cli","")).lower()

            unique = str(number) + str(dt)

            if unique in sent:
                continue

            sent.add(unique)

            otp_match = re.search(r"\d{3}-\d{3}", str(message))

            if otp_match:
                otp = otp_match.group()
            else:
                continue

            if "whatsapp" in service:
                tag = "#WS"
            elif "telegram" in service:
                tag = "#TG"
            else:
                tag = "#SMS"

            try:
                numobj = phonenumbers.parse("+" + number)
                country = geocoder.description_for_number(numobj, "en")
            except:
                country = "Unknown"

            text = f"""📩 NEW MESSAGE RECIEVED

{tag} 🟢 {country}
+{number}

#English
"""

            keyboard = [
                [InlineKeyboardButton(f"🔑 {otp}", callback_data="otp")],
                [
                    InlineKeyboardButton("📞 Channel", url="https://t.me/TeamOFDark1"),
                    InlineKeyboardButton("💬 Chat", url="https://t.me/NumOTPCHAT")
                ],
                [
                    InlineKeyboardButton("📦 Numbers", url="https://t.me/NumOTPV1BOT")
                ]
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            try:

                bot.send_message(
                    chat_id=CHAT_ID,
                    text=text,
                    reply_markup=reply_markup
                )

                print("✅ OTP Forwarded:", otp)

            except Exception as tg_error:

                print("Telegram Error:", tg_error)

    except Exception as api_error:

        print("API Error:", api_error)

    time.sleep(5)
