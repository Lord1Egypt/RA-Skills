import asyncio

from telethon import TelegramClient

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


async def run(target_group: str, limit: int) -> None:
    cfg = load_config()
    client: TelegramClient = build_client(cfg)
    await client.start()
    target_chat = None
    async for dialog in client.iter_dialogs():
        if dialog.title == target_group:
            target_chat = dialog.entity
            break
    if not target_chat:
        print(f"❌ 未找到群：{target_group}")
        await client.disconnect()
        return
    print(f"✅ 已找到群 {target_group}，最近{limit}条消息如下：\n")
    messages = []
    async for message in client.iter_messages(target_chat, limit=limit):
        if message.text:
            sender = await message.get_sender()
            sender_name = sender.first_name if sender else "未知用户"
            if hasattr(sender, 'last_name') and sender.last_name:
                sender_name += f" {sender.last_name}"
            time_str = message.date.strftime("%Y-%m-%d %H:%M")
            messages.insert(0, f"[{time_str}] {sender_name}: {message.text}")
    for msg in messages:
        print(msg)
    await client.disconnect()


def main(target_group: str, limit: int) -> None:
    asyncio.run(run(target_group, limit))
