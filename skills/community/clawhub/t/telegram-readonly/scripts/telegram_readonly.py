#!/usr/bin/env python3
import argparse
import asyncio
import getpass
import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

CONFIG_DIR = Path.home() / ".config" / "telegram-readonly"
CONFIG_PATH = CONFIG_DIR / "config.json"


def eprint(*args: Any, **kwargs: Any) -> None:
    print(*args, file=sys.stderr, **kwargs)


@dataclass
class Settings:
    api_id: int
    api_hash: str
    session_string: str


def chmod_600(path: Path) -> None:
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def load_raw_config() -> dict[str, Any]:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text())
    return {}


def save_config(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2) + "\n")
    chmod_600(CONFIG_PATH)


def load_settings(require_session: bool = True) -> Settings:
    data = load_raw_config()
    api_id_raw = os.getenv("TELEGRAM_API_ID") or data.get("api_id")
    api_hash = os.getenv("TELEGRAM_API_HASH") or data.get("api_hash")
    session_string = os.getenv("TELEGRAM_SESSION_STRING") or data.get("session_string") or ""

    if not api_id_raw:
        raise SystemExit(
            "Missing TELEGRAM_API_ID. Set env vars or run auth first."
        )
    if not api_hash:
        raise SystemExit(
            "Missing TELEGRAM_API_HASH. Set env vars or run auth first."
        )
    if require_session and not session_string:
        raise SystemExit(
            "Missing TELEGRAM_SESSION_STRING/session_string. Run auth first."
        )

    try:
        api_id = int(api_id_raw)
    except ValueError as exc:
        raise SystemExit("TELEGRAM_API_ID must be an integer") from exc

    return Settings(api_id=api_id, api_hash=api_hash, session_string=session_string)


def iso(dt: Any) -> Optional[str]:
    if not dt:
        return None
    try:
        return dt.isoformat()
    except Exception:
        return str(dt)


async def build_client(settings: Settings):
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except Exception as exc:
        raise SystemExit(
            "Telethon is not installed. Install it with: pip install telethon"
        ) from exc

    client = TelegramClient(
        StringSession(settings.session_string),
        settings.api_id,
        settings.api_hash,
        receive_updates=False,
    )
    await client.connect()
    if not await client.is_user_authorized():
        raise SystemExit("Telegram session is not authorized. Run auth first.")
    return client


def is_muted_dialog(dialog: Any) -> bool:
    notify_settings = getattr(dialog.dialog, "notify_settings", None)
    mute_until = getattr(notify_settings, "mute_until", None) if notify_settings else None
    if mute_until is None:
        return False
    mute_str = str(mute_until)
    if mute_str.startswith("2038-"):
        return True
    return False


def dialog_to_dict(dialog: Any) -> dict[str, Any]:
    entity = dialog.entity
    return {
        "id": dialog.id,
        "name": dialog.name,
        "title": getattr(entity, "title", None),
        "username": getattr(entity, "username", None),
        "is_user": dialog.is_user,
        "is_group": dialog.is_group,
        "is_channel": dialog.is_channel,
        "is_bot": bool(getattr(entity, "bot", False)),
        "unread_count": dialog.unread_count,
        "unread_mentions_count": getattr(dialog, "unread_mentions_count", None),
        "date": iso(dialog.date),
        "pinned": dialog.pinned,
        "archived": dialog.archived,
        "muted": is_muted_dialog(dialog),
    }


def message_to_dict(message: Any) -> dict[str, Any]:
    sender = getattr(message, "sender", None)
    sender_name = None
    if sender is not None:
        first = getattr(sender, "first_name", None) or ""
        last = getattr(sender, "last_name", None) or ""
        title = getattr(sender, "title", None) or ""
        sender_name = (first + " " + last).strip() or title or getattr(sender, "username", None)
    return {
        "id": message.id,
        "date": iso(message.date),
        "text": message.message,
        "sender_id": getattr(message, "sender_id", None),
        "sender_name": sender_name,
        "out": message.out,
        "mentioned": getattr(message, "mentioned", None),
        "media": bool(message.media),
        "reply_to": getattr(getattr(message, "reply_to", None), "reply_to_msg_id", None),
    }


async def cmd_auth(args: argparse.Namespace) -> int:
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except Exception as exc:
        raise SystemExit(
            "Telethon is not installed. Install it with: pip install telethon"
        ) from exc

    raw = load_raw_config()
    api_id_raw = args.api_id or os.getenv("TELEGRAM_API_ID") or raw.get("api_id")
    api_hash = args.api_hash or os.getenv("TELEGRAM_API_HASH") or raw.get("api_hash")
    if not api_id_raw or not api_hash:
        raise SystemExit("auth requires TELEGRAM_API_ID and TELEGRAM_API_HASH or --api-id/--api-hash")
    api_id = int(api_id_raw)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    client = TelegramClient(StringSession(raw.get("session_string", "")), api_id, api_hash)

    async def phone() -> str:
        return input("Telegram phone number (international format): ").strip()

    async def password() -> str:
        return getpass.getpass("Telegram 2FA password (if enabled): ")

    async def code() -> str:
        return input("Login code: ").strip()

    await client.start(phone=phone, password=password, code_callback=code)
    session_string = client.session.save()
    save_config({"api_id": api_id, "api_hash": api_hash, "session_string": session_string})
    me = await client.get_me()
    await client.disconnect()
    print(json.dumps({
        "ok": True,
        "saved_to": str(CONFIG_PATH),
        "account": {
            "id": getattr(me, "id", None),
            "username": getattr(me, "username", None),
            "first_name": getattr(me, "first_name", None),
            "last_name": getattr(me, "last_name", None),
        },
        "warning": "Session string is high-privilege. Protect this file like a password.",
    }, indent=2))
    return 0


def dialog_search_score(row: dict[str, Any], query: str) -> int:
    q = query.strip().lower()
    if not q:
        return 0
    name = (row.get("name") or "").lower()
    username = (row.get("username") or "").lower()
    title = (row.get("title") or "").lower()
    haystack = " ".join(part for part in [name, username, title] if part).strip()
    tokens = [t for t in q.split() if t]
    if not tokens:
        return 0
    if any(token not in haystack for token in tokens):
        return -1

    score = 0
    if q == username:
        score += 120
    if q == name:
        score += 100
    if q == title:
        score += 90
    if q in username:
        score += 60
    if q in name:
        score += 50
    if q in title:
        score += 40
    score += sum(8 for token in tokens if token in username)
    score += sum(6 for token in tokens if token in name)
    score += sum(5 for token in tokens if token in title)
    score += min(len(tokens), 5)
    return score


async def cmd_dialogs(args: argparse.Namespace) -> int:
    settings = load_settings()
    client = await build_client(settings)
    try:
        dialogs = await client.get_dialogs(limit=args.limit, archived=args.archived)
        data = [dialog_to_dict(d) for d in dialogs]
        if args.query:
            scored = []
            for row in data:
                score = dialog_search_score(row, args.query)
                if score >= 0:
                    scored.append((score, row))
            scored.sort(key=lambda item: (item[0], item[1].get("date") or ""), reverse=True)
            data = [row for _, row in scored]
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0
    finally:
        await client.disconnect()


async def resolve_entity(client: Any, chat: str) -> Any:
    try:
        return await client.get_entity(chat)
    except Exception as exc:
        raise SystemExit(f"Could not resolve chat/entity: {chat} ({exc})") from exc


async def cmd_messages(args: argparse.Namespace) -> int:
    settings = load_settings()
    client = await build_client(settings)
    try:
        entity = await resolve_entity(client, args.chat)
        messages = await client.get_messages(entity, limit=args.limit, min_id=args.min_id, max_id=args.max_id)
        data = [message_to_dict(m) for m in messages]
        if args.reverse:
            data = list(reversed(data))
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return 0
    finally:
        await client.disconnect()


async def cmd_search(args: argparse.Namespace) -> int:
    settings = load_settings()
    client = await build_client(settings)
    try:
        entity = await resolve_entity(client, args.chat) if args.chat else None
        results = []
        async for message in client.iter_messages(entity, search=args.query, limit=args.limit):
            results.append(message_to_dict(message))
        results = list(reversed(results)) if args.reverse else results
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return 0
    finally:
        await client.disconnect()


async def cmd_unread_dialogs(args: argparse.Namespace) -> int:
    settings = load_settings()
    client = await build_client(settings)
    try:
        dialogs = await client.get_dialogs(limit=args.scan_limit, archived=None)
        items = []
        for dialog in dialogs:
            row = dialog_to_dict(dialog)
            if (row.get("unread_count") or 0) <= 0:
                continue
            if not args.include_archived and row.get("archived"):
                continue
            if not args.include_muted and row.get("muted"):
                continue
            if args.only_dms and not row.get("is_user"):
                continue
            items.append(row)
        items.sort(key=lambda x: x.get("date") or "", reverse=True)
        print(json.dumps(items[: args.limit], indent=2, ensure_ascii=False))
        return 0
    finally:
        await client.disconnect()


def cmd_help(args: argparse.Namespace) -> int:
    payload = {
        "tool": "telegram-readonly",
        "purpose": "Read-only Telegram access for a user's personal account via Telethon/MTProto.",
        "defaults": {
            "dialogs": 50,
            "messages": 50,
            "search": 50,
            "unread-dialogs": 10,
            "unread-dms": 10,
            "unread_scan_limit": 200,
        },
        "notes": [
            "Read-only wrapper: no send/edit/delete/mark-read commands are exposed.",
            "dialogs --query uses token-based matching across name, username, and title.",
            "unread-dialogs and unread-dms exclude muted and archived chats by default.",
            "Dialog output includes is_user, is_group, is_channel, is_bot, archived, muted, and unread counts.",
        ],
        "commands": {
            "auth": "Interactive Telegram login; saves a local StringSession.",
            "dialogs": "List chats/dialogs. Use --query for token-based matching and --archived to view archived dialogs.",
            "messages": "Read recent messages from one chat. Requires --chat.",
            "search": "Search message text globally or within one chat.",
            "unread-dialogs": "List recent unread chats, excluding muted and archived by default.",
            "unread-dms": "List recent unread DM chats only, excluding muted and archived by default.",
            "help": "Show this command summary.",
        },
        "examples": [
            "telegram-readonly dialogs --query 'petros skynet'",
            "telegram-readonly messages --chat @suuuupaman --limit 20 --reverse",
            "telegram-readonly search 'btc_txid_here' --limit 20",
            "telegram-readonly unread-dialogs --limit 10",
            "telegram-readonly unread-dms --limit 10 --include-muted",
        ],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=(
            "Read-only Telegram wrapper built on Telethon. "
            "This tool intentionally exposes only read operations."
        )
    )
    sub = p.add_subparsers(dest="command", required=True)

    auth = sub.add_parser("auth", help="Interactive login and local config creation")
    auth.add_argument("--api-id", type=int)
    auth.add_argument("--api-hash")

    dialogs = sub.add_parser("dialogs", help="List dialogs/chats")
    dialogs.add_argument("--limit", type=int, default=50)
    dialogs.add_argument("--archived", action="store_true")
    dialogs.add_argument("--query", help="Filter by name/username/title")

    messages = sub.add_parser("messages", help="Read recent messages from one chat")
    messages.add_argument("--chat", required=True, help="Chat id, username, phone, or title resolvable by Telethon")
    messages.add_argument("--limit", type=int, default=50)
    messages.add_argument("--min-id", type=int, default=0)
    messages.add_argument("--max-id", type=int, default=0)
    messages.add_argument("--reverse", action="store_true", help="Output oldest -> newest")

    search = sub.add_parser("search", help="Search messages globally or within one chat")
    search.add_argument("query", help="Search query")
    search.add_argument("--chat", help="Optional chat/entity to restrict search")
    search.add_argument("--limit", type=int, default=50)
    search.add_argument("--reverse", action="store_true", help="Output oldest -> newest")

    unread_dialogs = sub.add_parser("unread-dialogs", help="List recent unread chats; default excludes muted and archived")
    unread_dialogs.add_argument("--limit", type=int, default=10)
    unread_dialogs.add_argument("--scan-limit", type=int, default=200, help="How many dialogs to scan before filtering")
    unread_dialogs.add_argument("--include-muted", action="store_true")
    unread_dialogs.add_argument("--include-archived", action="store_true")

    unread_dms = sub.add_parser("unread-dms", help="List recent unread direct-message chats; default excludes muted and archived")
    unread_dms.add_argument("--limit", type=int, default=10)
    unread_dms.add_argument("--scan-limit", type=int, default=200, help="How many dialogs to scan before filtering")
    unread_dms.add_argument("--include-muted", action="store_true")
    unread_dms.add_argument("--include-archived", action="store_true")

    sub.add_parser("help", help="Show a descriptive summary of commands, defaults, and examples")

    return p


async def async_main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "auth":
        return await cmd_auth(args)
    if args.command == "dialogs":
        return await cmd_dialogs(args)
    if args.command == "messages":
        return await cmd_messages(args)
    if args.command == "search":
        return await cmd_search(args)
    if args.command == "unread-dialogs":
        args.only_dms = False
        return await cmd_unread_dialogs(args)
    if args.command == "unread-dms":
        args.only_dms = True
        return await cmd_unread_dialogs(args)
    if args.command == "help":
        return cmd_help(args)
    parser.error("unknown command")
    return 2


def main() -> int:
    try:
        return asyncio.run(async_main())
    except KeyboardInterrupt:
        eprint("Interrupted")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
