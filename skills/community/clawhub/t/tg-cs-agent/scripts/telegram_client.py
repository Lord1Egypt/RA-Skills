"""Telegram interface: Telethon-based, replaces subprocess tgctl calls."""
import asyncio
from telethon import TelegramClient as TelethonClient, events
from telethon.tl.functions.messages import SetTypingRequest
from telethon.tl.types import User, SendMessageTypingAction, SendMessageCancelAction
from config import Config


class TelegramClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = TelethonClient(
            str(config.session_path),
            int(config.telegram_api_id),
            config.telegram_api_hash,
        )
        self._me = None

    async def connect(self):
        """Connect and verify auth. Auto-login if no session exists."""
        await self.client.connect()
        if not await self.client.is_user_authorized():
            print("[TG] No session found. Starting interactive login...")
            phone = input("Enter your phone number (e.g. +8613800138000): ").strip()
            await self.client.send_code_request(phone)
            code = input("Enter the verification code from Telegram: ").strip()
            try:
                await self.client.sign_in(phone, code)
            except Exception:
                password = input("2FA password required: ").strip()
                await self.client.sign_in(password=password)
            print("[TG] Login successful!")
        self._me = await self.client.get_me()
        print(f"[TG] Connected as {self._me.first_name} (@{self._me.username}, ID: {self._me.id})")

    async def disconnect(self):
        await self.client.disconnect()

    @property
    def my_id(self) -> int:
        return self._me.id if self._me else 0

    async def set_typing(self, chat_id, typing: bool = True):
        """Set or cancel typing status."""
        try:
            target = int(chat_id) if str(chat_id).lstrip("-").isdigit() else chat_id
            entity = await self.client.get_input_entity(target)
            if typing:
                await self.client(SetTypingRequest(peer=entity, action=SendMessageTypingAction()))
            else:
                await self.client(SetTypingRequest(peer=entity, action=SendMessageCancelAction()))
        except Exception as e:
            print(f"[TG] Failed to set typing for {chat_id}: {e}")

    async def send(self, chat_id, message: str) -> bool:
        """Send a message."""
        try:
            target = int(chat_id) if str(chat_id).lstrip("-").isdigit() else chat_id
            await self.client.send_message(target, message)
            print(f"[TG] Sent to {chat_id}: {message[:60]}")
            return True
        except Exception as e:
            print(f"[TG] Failed to send to {chat_id}: {e}")
            return False

    async def get_me(self) -> dict:
        """Get current user info."""
        if not self._me:
            return {}
        name = " ".join(filter(None, [self._me.first_name, self._me.last_name]))
        return {
            "id": str(self._me.id),
            "name": name,
            "phone": self._me.phone or "",
            "username": self._me.username or "",
        }

    async def listen(self, callback):
        """Listen for incoming messages, call callback(chat_id, sender_id, text) for each."""
        print("[TG] Starting message listener...")

        @self.client.on(events.NewMessage(incoming=True))
        async def handler(event):
            chat_id = str(event.chat_id)
            sender_id = str(event.sender_id)
            text = event.raw_text or ""
            if text:
                await callback(chat_id, sender_id, text)

        await self.client.run_until_disconnected()
