import os
from datetime import datetime, timedelta, timezone

from PIL import Image, ImageDraw, ImageFont
from pyrogram import enums, filters
from pyrogram.types import (
    Message, ChatMemberUpdated,
    InlineKeyboardMarkup, InlineKeyboardButton
)

from POISONMUSIC import app

# ─────────────────────────────
# CONFIG
# ─────────────────────────────
LOGGER = getLogger(__name__)

class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        self.data[chat_id] = {}

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(500, 500)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user, chatname, id, uname):
    background = Image.open("POISONMUSIC/assets/poison.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)
    pfp = pfp.resize((1157, 1158))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('POISONMUSIC/assets/font.ttf', size=110)
    welcome_font = ImageFont.truetype('POISONMUSIC/assets/font.ttf', size=60)
    draw.text((1800, 700), f'NAME: {user}', fill=(255, 255, 255), font=font)
    draw.text((1800, 830), f'ID: {id}', fill=(255, 255, 255), font=font)
    draw.text((1800, 965), f"USERNAME : {uname}", fill=(255, 255, 255), font=font)
    pfp_position = (391, 336)
    background.paste(pfp, pfp_position, pfp)
    background.save(f"downloads/welcome#{id}.png")
    return f"downloads/welcome#{id}.png"

@ app.on_chat_member_updated(filters.group, group=-3)
async def greet_group(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    A = await wlcm.find_one(chat_id)
    if (
        not member.new_chat_member
        or member.new_chat_member.status in {"banned", "left", "restricted"}
        or member.old_chat_member
    ):
        return
    user = member.new_chat_member.user if member.new_chat_member else member.from_user
    try:
        pic = await app.download_media(
            user.photo.big_file_id, file_name=f"pp{user.id}.png"
        )
    except AttributeError:
        pic = "POISONMUSIC/assets/POISONMUSIC/assets/poison.png"
    if (temp.MELCOW).get(f"welcome-{member.chat.id}") is not None:
        try:
            await temp.MELCOW[f"welcome-{member.chat.id}"].delete()
        except Exception as e:
            LOGGER.error(e)
    try:
        welcomeimg = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )
        temp.MELCOW[f"welcome-{member.chat.id}"] = await app.send_photo(
            member.chat.id,
            photo=welcomeimg,
            caption=f"""
**❅────✦ ᴡєʟᴄσϻє ᴛσ ✦────❅
{chat_title}
▰▰▰▰▰▰▰▰▰▰▰▰▰
➻ ηᴧϻє ✧ {mention}
➻ ɪᴅ ✧ `{uid}`
➻ ᴜsєʀηᴧϻє ✧ @{uname}
▰▰▰▰▰▰▰▰▰▰▰▰▰
➻ ᴛσᴛᴧʟ ϻєϻʙєʀs ✧ {count}
❅─────✧❅✦❅✧─────❅**
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{('๏ ᴠɪєᴡ ηєᴡ ϻєϻʙєʀ ๏')}", url=f"tg://openmessage?user_id={user.id}")],
                [InlineKeyboardButton(f"{('๏ ᴋɪᴅηᴧᴘ ϻє ʙᴧʙʏ ๏')}", url=f"https://t.me/{client.username}?startgroup=true")],
            ])
        )

        last_messages.setdefault(cid, []).append(sent)
        if len(last_messages[cid]) > WELCOME_LIMIT:
            old_msg = last_messages[cid].pop(0)
            try: await old_msg.delete()
            except: pass

    except Exception:
        await client.send_message(cid, f"<b>🎉 ᴡєʟᴄσϻє, {user.mention}!</b>")
    finally:
        for f in (avatar, img):
            if f and os.path.exists(f) and "POISONMUSIC/assets" not in f:
                try: os.remove(f)
                except: pass
