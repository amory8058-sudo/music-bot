import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
import yt_dlp

# بيانات البوت (تقدر تسيبها زي ما هي أو تقرأها من Environment Variables)
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

app = Client(
    "music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("🎵 أهلاً بك! بوت الأغاني يعمل بكفاءة وجاهز لاستقبال أمر /play.")

@app.on_message(filters.command("play"))
async def play_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ من فضلك اكتب اسم الأغنية أو رابط اليوتيوب بعد الأمر.\nمثال:\n`/play faded`")
        return
    
    query = " ".join(message.command[1:])
    m = await message.reply_text(f"🔍 جاري البحث عن: `{query}`...")

    try:
        # استخراج رابط اليوتيوب مباشرة باستخدام yt-dlp
        ydl_opts = {'format': 'bestaudio', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in query or "youtu.be" in query:
                info = ydl.extract_info(query, download=False)
            else:
                info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            
            stream_url = info['url']
            title = info.get('title', 'مقطع صوتي')

        await call_py.join_group_call(
            message.chat.id,
            MediaStream(stream_url)
        )
        await m.edit_text(f"🎶 جاري تشغيل الآن: **{title}**")
    
    except Exception as e:
        await m.edit_text(f"❌ حدث خطأ أثناء التشغيل:\n`{e}`")

@app.on_message(filters.command("stop"))
async def stop_cmd(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹️ تم إيقاف التشغيل ومغادرة المكون الصوتي.")
    except Exception as e:
        await message.reply_text(f"❌ حدث خطأ:\n`{e}`")

async def main():
    await app.start()
    await call_py.start()
    print("Bot Started Successfully!")
    from pyrogram import idle
    await idle()

if __name__ == "__main__":
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
