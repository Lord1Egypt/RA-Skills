import asyncio

from telethon import TelegramClient

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


async def run() -> None:
    cfg = load_config()
    client: TelegramClient = build_client(cfg)
    await client.connect()
    me = await client.get_me()
    last_name = me.last_name if me.last_name else ''
    print(f'账号全名：{me.first_name} {last_name}')
    print(f'用户名：@{me.username if me.username else "未设置"}')
    print(f'手机号：{me.phone}')
    await client.disconnect()


def main() -> None:
    asyncio.run(run())
