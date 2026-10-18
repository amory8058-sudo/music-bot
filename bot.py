import os
import telebot

# تم وضع التوكين الخاص بك هنا مباشرة
TOKEN = "8772933159:AAFRgtCmrRF0pY7DtA40k0Gy-NKdYWh3Cic"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  bot.reply_to(
      message,
      "أهلاً بك في بوت الموسيقى! 🎵\nأرسل اسم الأغنية التي تبحث عنها وسأقوم"
      " بمساعدتك.",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  bot.reply_to(
      message,
      f"جاري البحث عن الموسيقى الخاصة بـ: {message.text} 🎧\n(يمكنك تطوير"
      " هذا الجزء لاحقاً بروابط أو ملفات صوتية)",
  )


if __name__ == "__main__":
  print("البوت يعمل الآن بنجاح...")
  bot.infinity_polling()