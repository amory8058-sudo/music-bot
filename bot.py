import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
# ملاحظة: سنستخدم yt-dlp لجلب روابط البث المباشر للأغاني من يوتيوب
import yt_dlp

# جلب المعلومات من متغيرات البيئة في Railway أو تعيينها مباشرة
API_ID = int(os.getenv("API_ID", "123456"))  # ضع الـ API_ID الخاص بك هنا أو في متغيرات البيئة
API_HASH = os.getenv("API_HASH", "your_api_hash")  # ضع الـ API_HASH هنا أو في متغيرات البيئة
BOT_TOKEN = "8772933159:AAFRgtCmrRF0pY7DtA40k0Gy-NKdYWh3Cic"
STRING_SESSION = os.getenv("STRING_SESSION", "")  # جلسة الحساب المساعد (Userbot)

# إعداد عميل البوت الحسابي أو المساعد للاتصال بالمكالمات الصوتية
# إذا لم توفر STRING_SESSION سيتم تشغيل البوت العادي للتنبيهات والأوامر
app = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command(["start", "help"]))
async def start_handler(client, message: Message):
    await message.reply_text(
        "✨ **أهلاً بك في بوت الموسيقى الاحترافي!**\n\n"
        "🎵 تشغيل الأغاني في المكالمات الصوتية للجروبات والقنوات.\n"
        "• استخدم الأمر: `/play [اسم الأغنية]` لتشغيلها في المحادثة الصوتية.\n"
        "• استخدم الأمر: `/stop` لإيقاف التشغيل."
    )

@app.on_message(filters.command(["play"]))
async def play_handler(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("❌ **يرجى كتابة اسم الأغنية بعد الأمر!**\nمثال: `/play عمرو دياب`")
    
    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 **جاري البحث والتحميل لـ:** `{query}`...")

    try:
        # البحث بواسطة yt-dlp للحصول على رابط البث الصوتي المباشر
        ydl_opts = {
            'format': 'bestaudio',
            'default_search': 'ytsearch',
            'noplaylist': True,
            'quiet': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            
            song_url = info['url']
            title = info.get('title', 'مقطوعة موسيقية')

        # بدء التشغيل في المكالمة الصوتية للـ Chat الحالي
        chat_id = message.chat.id
        await call_py.join_group_call(
            chat_id,
            AudioPiped(song_url)
        )
        await m.edit_text(f"▶️ **جاري الآن تشغيل:**\n`{title}`")
    except Exception as e:
        await m.edit_text(f"❌ **حدث خطأ أثناء التشغيل:**\n`{str(e)}`\n\n*(تأكد من بدء المكالمة الصوتية في الجروب وأن البوت المساعد داخل الجروب ومشرف)*")

@app.on_message(filters.command(["stop"]))
async def stop_handler(client, message: Message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ **تم إيقاف الموسيقى ومغادرة المكالمة الصوتية.**")
    except Exception as e:
        await message.reply_text(f"❌ **لا توجد مكالمة صوتية نشطة أو حدث خطأ:** `{str(e)}`")

async def main():
    await app.start()
    await call_py.start()
    print("🚀 بوت الموسيقى الاحترافي يعمل الآن بنجاح...")
    await idle()

if __name__ == "__main__":
    from pyrogram import idle
    app.run(main())
