"""Request SMS login code (Telethon)."""

from __future__ import annotations

import asyncio
import os

from telethon import TelegramClient

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


async def run_auth() -> None:
    cfg = load_config()
    phone = cfg.phone or os.environ.get("TELEGRAM_PHONE", "").strip()
    if not phone:
        raise SystemExit("请设置环境变量 TELEGRAM_PHONE（或在 .env 中）。")
    client: TelegramClient = build_client(cfg)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            result = await client.send_code_request(phone)
            print(f"SENT_CODE_SUCCESS:{result.phone_code_hash}")
        except Exception as e:
            print(f"ERROR_DURING_CODE_REQUEST:{e}")
    else:
        print("ALREADY_AUTHORIZED")
    await client.disconnect()


def main() -> None:
    asyncio.run(run_auth())
