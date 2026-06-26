"""Complete sign-in with SMS code (env-only secrets)."""

from __future__ import annotations

import asyncio
import os

from telethon import TelegramClient

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


async def run_login() -> None:
    cfg = load_config()
    phone = cfg.phone or os.environ.get("TELEGRAM_PHONE", "").strip()
    code = os.environ.get("TG_CODE", "").strip()
    phone_code_hash = os.environ.get("TG_PHONE_CODE_HASH", "").strip()
    if not phone:
        raise SystemExit("请设置 TELEGRAM_PHONE。")
    if not code or not phone_code_hash:
        raise SystemExit("请设置 TG_CODE 与 TG_PHONE_CODE_HASH（来自 auth 步骤）。")
    client: TelegramClient = build_client(cfg)
    await client.connect()
    try:
        await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
        print("LOGIN_SUCCESS")
    except Exception as e:
        print(f"LOGIN_ERROR:{e}")
    await client.disconnect()


def main() -> None:
    asyncio.run(run_login())
