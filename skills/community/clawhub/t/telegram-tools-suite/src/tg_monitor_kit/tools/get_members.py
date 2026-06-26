import asyncio

from telethon import TelegramClient
from telethon.tl.types import User

from tg_monitor_kit.client import build_client
from tg_monitor_kit.config import load_config


def _mask_phone(phone: str | None) -> str:
    if not phone:
        return "无公开手机号"
    if len(phone) <= 4:
        return "*" * len(phone)
    return f"{phone[:2]}***{phone[-2:]}"


async def run(target_group: str) -> None:
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
    print(f"✅ 已找到群 {target_group}，成员列表如下：\n")
    members = []
    async for participant in client.iter_participants(target_chat):
        if isinstance(participant, User):
            user_id = participant.id
            first_name = participant.first_name or ""
            last_name = participant.last_name or ""
            full_name = f"{first_name} {last_name}".strip()
            username = f"@{participant.username}" if participant.username else "无用户名"
            phone = _mask_phone(participant.phone)
            is_bot = "🤖 机器人" if participant.bot else "👤 普通用户"
            members.append(f"ID: {user_id} | 昵称: {full_name} | {username} | 手机号: {phone} | 类型: {is_bot}")
    print(f"群成员总数：{len(members)}人\n")
    for m in members:
        print(m)
    await client.disconnect()


def main(target_group: str) -> None:
    asyncio.run(run(target_group))
