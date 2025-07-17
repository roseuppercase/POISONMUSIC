from pyrogram.enums import ParseMode

from POISONMUSIC import app
from POISONMUSIC.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        logger_text = f"""
<b>{app.mention} ᴘʟᴧʏ ʟσɢ</b>

<b>ᴄʜᴧᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴧᴛ ηᴧϻє :</b> {message.chat.title}
<b>ᴄʜᴧᴛ ᴜsєʀηᴧϻє :</b> @{message.chat.username}

<b>ᴄʜᴧᴛ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ηᴧϻє :</b> {message.from_user.mention}
<b>ᴜsєʀηᴧϻє :</b> @{message.from_user.username}

<b>ǫᴜєʀʏ :</b> {message.text.split(None, 1)[1]}
<b>sᴛʀєᴧϻᴛʏᴘє :</b> {streamtype}"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
