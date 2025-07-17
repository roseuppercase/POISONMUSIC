import asyncio
import os
import sys
from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config
from ..logging import LOGGER


class POISON(Client):
    def __init__(self):
        super().__init__(
            name="PoisonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            workers=30,
            max_concurrent_transmissions=7,
        )
        LOGGER(__name__).info("Bot client initialized.")

    async def _auto_restart(self):
        interval = getattr(config, "RESTART_INTERVAL", 86400)  # fallback 24 hours
        while True:
            await asyncio.sleep(interval)
            try:
                await self.disconnect()
                await self.start()
                LOGGER(__name__).info("🔄 Pyrogram session auto-restarted successfully.")
            except Exception as exc:
                LOGGER(__name__).warning(f"Auto-restart failed: {exc}")

    async def start(self):
        await super().start()
        asyncio.create_task(self._auto_restart())

        me = await self.get_me()
        self.username, self.id = me.username, me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.mention = me.mention

        try:
            await self.send_message(
                config.LOGGER_ID,
                (
                    f"<b>✦ ʙσᴛ sᴛᴧʀᴛєᴅ : {self.mention}</b>\n\n"                    
                    f"<b>➻ ηᴧϻє : {self.name}</b>\n"
                    f"<b>➻ ᴜsєʀηᴧϻє : @{self.username}</b></u>\n"
                    f"<b>➻ ᴜsєʀ ɪᴅ : <code>{self.id}</code></b>"
                ),
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("❌ Bot cannot access the log group/channel – add & promote it first!")
            sys.exit()
        except Exception as exc:
            LOGGER(__name__).error(f"❌ Failed to send startup message.\nReason: {type(exc).__name__}")
            sys.exit()

        try:
            member = await self.get_chat_member(config.LOGGER_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("❌ Promote the bot as admin in the log group/channel.")
                sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"❌ Could not check admin status: {e}")
            sys.exit()

        LOGGER(__name__).info(f"✅ Music Bot started as {self.name} (@{self.username})")
