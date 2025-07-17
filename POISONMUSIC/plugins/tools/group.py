from pyrogram import filters
from pyrogram.types import Message

from POISONMUSIC import app
from config import OWNER_ID


@app.on_message(filters.video_chat_started)
async def on_voice_chat_started(_, message: Message):
    await message.reply_text("🎙 **ᴠσɪᴄє ᴄʜᴧᴛ ʜᴧs sᴛᴧʀᴛєᴅ!**")


@app.on_message(filters.video_chat_ended)
async def on_voice_chat_ended(_, message: Message):
    await message.reply_text("🔕 **ᴠσɪᴄє ᴄʜᴧᴛ єηᴅєᴅ.**")


@app.on_message(filters.video_chat_members_invited)
async def on_voice_chat_members_invited(_, message: Message):
    inviter = message.from_user.mention if message.from_user else "Someone"
    invited_list = []

    for user in message.video_chat_members_invited.users:
        try:
            invited_list.append(f"[{user.first_name}](tg://user?id={user.id})")
        except:
            continue

    if invited_list:
        users = ", ".join(invited_list)
        await message.reply_text(f"👥 {inviter} ɪηᴠɪᴛєᴅ {users} ᴛσ ᴛʜє ᴠσɪᴄє ᴄʜᴧᴛ. 😉")


@app.on_message(filters.command("leavegroup") & filters.user(OWNER_ID))
async def leave_group(_, message: Message):
    await message.reply_text("👋 **ʟєᴧᴠɪηɢ ᴛʜɪs ɢʀσυᴘ...**")
    await app.leave_chat(chat_id=message.chat.id, delete=True)
