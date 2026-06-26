import asyncio

from telethon import TelegramClient
from telethon.tl.types import Chat, Channel

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


async def run() -> None:
    cfg = load_config()
    client: TelegramClient = build_client(cfg)
    await client.start()
    print("正在获取账号的所有群组列表...\n")
    group_count = 0
    groups = []
    async for dialog in client.iter_dialogs():
        if isinstance(dialog.entity, (Chat, Channel)) and not dialog.is_user:
            group_count += 1
            groups.append(f"[{group_count}] {dialog.title} (ID: {dialog.id})")
    print(f"✅ 当前账号一共加入了 {group_count} 个群组/频道：")
    for g in groups:
        print(g)
    await client.disconnect()


def main() -> None:
    asyncio.run(run())
