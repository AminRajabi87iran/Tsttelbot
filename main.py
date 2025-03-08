from telethon import TelegramClient, events, functions, types
from datetime import datetime
import random
import pytz
from convertdate import persian
import asyncio
from telethon.errors import rpcerrorlist
from keep_alive import keep_alive
keep_alive()

API_ID = "9180601"
API_HASH = "7c9cf404fdaa6d0fa630da93d0bd637a"
SESSION_NAME = "self_bot"

iran_timezone = pytz.timezone('Asia/Tehran')

update_last_name = "🟢"
update_bio = "🟢"
auto_reply_enabled = "🔴"
away_message = "سلام! من الآن آفلاین هستم. به محض آنلاین شدن پاسخ خواهم داد. 🙏"

async def send_welcome_message(client):
    welcome_message = (
        "✅ ربات با موفقیت فعال شد.\n\n"
        "برای مشاهده لیست دستورات از کامند 'راهنما' استفاده کنید."
    )
    try:
        await client.send_message("me", welcome_message)
        print("✅ پیام خوش‌آمدگویی ارسال شد.")
    except Exception as e:
        print(f"⚠️ خطا در ارسال پیام خوش‌آمدگویی: {e}")

async def send_help_message(event):
    commands = f"""
    💡 دستورات موجود:
    1. `timename on` - فعال کردن تغییر خودکار نام خانوادگی.
    2. `timename off` - غیرفعال کردن تغییر خودکار نام خانوادگی.
    3. `timebio on` - فعال کردن تغییر خودکار بیو.
    4. `timebio off` - غیرفعال کردن تغییر خودکار بیو.
    5. `autoreply on` - فعال کردن پاسخ‌دهی خودکار.
    6. `autoreply off` - غیرفعال کردن پاسخ‌دهی خودکار.
    7. `tagall` - تگ کردن همه اعضای گروه.
    8. `del  <count>` - حذف تعداد مشخصی از پیام‌های شما.
    9. `راهنما` - نمایش این لیست.
--------------------------------    

    Time Name : {update_last_name}
    Time Bio : {update_bio}
    Auto Reply : {auto_reply_enabled}
    """
    await event.edit(commands)

async def handle_message(event):
    global update_last_name, update_bio, auto_reply_enabled

    command = event.raw_text.lower()
    if command.startswith("del"):
        try:
            # استخراج تعداد پیام‌ها
            parts = command.split()
            if len(parts) < 2 or not parts[1].isdigit():
                await event.edit("❌ دستور نامعتبر! لطفاً تعداد پیام‌ها را مشخص کنید. مثال: `del 5`")
                return

            count = int(parts[1])
            if count <= 0:
                await event.edit("❌ تعداد پیام‌ها باید عددی مثبت باشد.")
                return

            # حذف پیام‌ها
            deleted_count = 0
            count += 1
            async for msg in event.client.iter_messages(event.chat_id, from_user="me"):
                if deleted_count >= count:
                    break
                try:
                    await msg.delete()
                    deleted_count += 1
                except rpcerrorlist.MessageDeleteForbiddenError:
                    print("⚠️ خطا: حذف پیام امکان‌پذیر نیست.")
           
        except Exception as e:
            await event.respond(f"⚠️ خطا در حذف پیام‌ها: {e}")
            print(f"⚠️ خطا: {e}")

    elif command == "timename on":
        update_last_name = "🟢"
        await event.edit("✅ تغییر خودکار نام خانوادگی فعال شد.")
        print("✅ تغییر خودکار نام خانوادگی فعال شد.")

    elif command == "timename off":
        update_last_name = "🔴"
        await event.edit("❌ تغییر خودکار نام خانوادگی غیرفعال شد.")
        print("❌ تغییر خودکار نام خانوادگی غیرفعال شد.")

    elif command == "timebio on":
        update_bio = "🟢"
        await event.edit("✅ تغییر خودکار بیو فعال شد.")
        print("✅ تغییر خودکار بیو فعال شد.")

    elif command == "timebio off":
        update_bio = "🔴"
        await event.edit("❌ تغییر خودکار بیو غیرفعال شد.")
        print("❌ تغییر خودکار بیو غیرفعال شد.")

    elif command == "autoreply on":
        auto_reply_enabled = "🟢"
        await event.edit("✅ پاسخ‌دهی خودکار فعال شد.")
        print("✅ پاسخ‌دهی خودکار فعال شد.")

    elif command == "autoreply off":
        auto_reply_enabled = "🔴"
        await event.edit("❌ پاسخ‌دهی خودکار غیرفعال شد.")
        print("❌ پاسخ‌دهی خودکار غیرفعال شد.")

async def update_profile_with_telethon(client):
    try:
        number_fonts = {
    "0123456789",
    "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗",
    "⊘𝟙ϩӠ५ƼϬ7𝟠९",
    "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡",  
    "⁰¹²³⁴⁵⁶⁷⁸⁹",
    "₀₁₂₃₄₅₆₇₈₉",
    "0ƖԶՅՎटმԴՑԳ",
    "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",
    "0ƖᄅƐㄣϛ6ㄥ89",
    "０１２３４５６７８９",
    "ᦲ᧒ᒿᗱᔰƼᦆᒣᲖၦ",
    "۰۱۲۳۴۵۶۷۸۹",
    "𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
}

        now = datetime.now(iran_timezone)
        current_time = now.strftime('%H:%M')
        shamsi_date = persian.from_gregorian(now.year, now.month, now.day)
        current_shamsi_date = f"{shamsi_date[0]}/{shamsi_date[1]:02d}/{shamsi_date[2]:02d}"
        selected_font = random.choice(list(number_fonts))
        formatted_time = ''.join([selected_font[int(c)] if c.isdigit() else c for c in current_time])

        if update_last_name == "🟢":
            await client(functions.account.UpdateProfileRequest(last_name=f"{formatted_time}"))
            print(f"Last Name Updated. {current_time}")

        if update_bio == "🟢":
            new_bio = f"فضولی شما در ساعت {current_time} و در تاریخ {current_shamsi_date} ثبت شد ✅️"
            await client(functions.account.UpdateProfileRequest(about=new_bio))
            print(f"Bio Updated. {current_time}")
    except Exception as e:
        print(f"⚠️ خطا در به‌روزرسانی پروفایل: {e}")

async def auto_reply(event, client):
    if event.is_private and auto_reply_enabled == "🟢":
        try:
            sender = await event.get_sender()
            sender_name = f"@{sender.username}" or f"{sender.first_name} {sender.last_name or ''}"
            sender_id = sender.id

            saved_message = (
                f"📩 کاربر [{sender_name}](tg://user?id={sender_id}) "
                f"به شما پیام داده است."
            )
            if 'bot' not in sender_name:
                me = await client.get_entity("me")
                if not isinstance(me.status, types.UserStatusOnline):
                    await event.reply(away_message)
                    print(f"✅ پیام پاسخ خودکار برای {sender_id} ارسال شد.")
                    await client.send_message("me", saved_message)
                    print(f"✅ پیام ثبت شد: {saved_message}")

        except Exception as e:
            print(f"⚠️ خطا در پاسخ‌دهی خودکار یا ثبت پیام: {e}")

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        await send_welcome_message(client)

        @client.on(events.NewMessage(pattern="راهنما", outgoing=True))
        async def help_listener(event):
            await send_help_message(event)

        @client.on(events.NewMessage(outgoing=True))
        async def command_listener(event):
            await handle_message(event)

        @client.on(events.NewMessage(incoming=True))
        async def incoming_listener(event):
            await auto_reply(event, client)

        while True:
            try:
                await update_profile_with_telethon(client)
                await asyncio.sleep(60)
            except Exception as e:
                print(f"⚠️ خطا: {e}")
                await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
