#!/usr/bin/env python3
"""
tg-channel-reader — Telegram channel reader skill for OpenClaw
Reads posts from public/private Telegram channels via MTProto (Telethon)
"""

import argparse
import asyncio
import json
import os
import sqlite3
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from tg_session_guard import (
    NetworkError,
    NotAuthorizedError,
    SessionLockTimeout,
    backup_session,
    load_last_good_info,
    restore_last_good,
    save_last_good,
    session_lock,
)

try:
    from telethon import TelegramClient
    from telethon.errors import (
        FloodWaitError,
        ChannelInvalidError,
        ChannelPrivateError,
        ChannelBannedError,
        ChatForbiddenError,
        ChatInvalidError,
        ChatRestrictedError,
        PeerIdInvalidError,
        UsernameNotOccupiedError,
        UserBannedInChannelError,
        InviteHashExpiredError,
        InviteHashInvalidError,
    )
    from telethon.tl.types import Channel, MessageMediaWebPage
    from telethon.tl.functions.channels import GetFullChannelRequest
except ImportError:
    print(json.dumps({"error": "telethon not installed. Run: pip install telethon"}))
    sys.exit(1)


def _channel_error(channel: str, error_type: str, message: str, action: str) -> dict:
    """Build a structured channel error dict for the agent."""
    return {
        "error": message,
        "error_type": error_type,
        "channel": channel,
        "action": action,
    }


# ── Session helpers ──────────────────────────────────────────────────────────

_SESSION_NAMES = [
    ".tg-reader-session.session",
    ".telethon-reader.session",
    "tg-reader-session.session",
    "telethon-reader.session",
]

# SOCKS5 proxy for MTProto, populated by get_config() from ~/.tg-reader.json
# ("socks_proxy") or the TG_PROXY env var. Some hosts filter direct MTProto,
# so a client may need to route through it. Telethon's native python-socks
# dict form, so no PySocks dependency is required.
_PROXY: dict | None = None


def _parse_proxy(spec):
    """Parse "host:port" or "socks5://[user:pass@]host:port" into a Telethon
    python-socks proxy dict, or return None for an empty/invalid spec."""
    if not spec:
        return None
    spec = spec.strip()
    scheme = "socks5"
    if "://" in spec:
        scheme, spec = spec.split("://", 1)
    username = password = None
    if "@" in spec:
        creds, spec = spec.rsplit("@", 1)
        if ":" in creds:
            username, password = creds.split(":", 1)
    if ":" not in spec:
        return None
    host, port = spec.rsplit(":", 1)
    try:
        port = int(port)
    except ValueError:
        return None
    proxy = {"proxy_type": scheme, "addr": host, "port": port}
    if username:
        proxy["username"] = username
        proxy["password"] = password
    return proxy


def _find_session_files() -> list:
    """Find tg-reader session files in home directory and current working directory.

    Only looks for known tg-reader session names — does not scan for
    arbitrary *.session files to avoid exposing unrelated session paths.
    """
    found = []
    seen: set = set()
    dirs_checked: set = set()
    for d in [Path.home(), Path.cwd()]:
        d = d.resolve()
        if d in dirs_checked:
            continue
        dirs_checked.add(d)
        for name in _SESSION_NAMES:
            f = d / name
            if f.exists():
                resolved = f.resolve()
                if resolved in seen:
                    continue
                seen.add(resolved)
                found.append(f)
    found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return found


def _validate_session(session_name: str) -> None:
    """Verify the session file exists; exit with a JSON error and hints if not.

    Both Pyrogram and Telethon store sessions as ``{name}.session``.
    This check prevents a silent re-auth prompt when the file is missing.
    """
    session_file = Path(f"{session_name}.session")
    if session_file.exists():
        return

    found = _find_session_files()
    error: dict = {
        "error": f"Session file not found: {session_file}",
        "expected_path": str(session_file),
        "fix": [
            "Run 'tg-reader-telethon auth' to create a new session",
            "Or set TG_SESSION=/path/to/existing-session (without .session suffix)",
            "Or add {\"session\": \"/path/to/session\"} to ~/.tg-reader.json",
            "Or pass --session-file /path/to/session (without .session suffix)",
        ],
    }
    if found:
        error["found_sessions"] = [str(f) for f in found[:10]]
        # Deliberately no "use the freshest file" suggestion: a found file may
        # be an empty or never-authorized session, and agents follow such
        # suggestions blindly (this is how session paths drifted apart in
        # production). Verify authorization first.
        error["note"] = (
            "Do NOT switch to a found session file blindly — it may hold no "
            "authorized user. Verify first: tg-reader-check --online "
            "--session-file <path without .session>"
        )
    lkg = load_last_good_info(session_name)
    if lkg:
        error["last_good_backup"] = {
            "path": lkg.get("path"),
            "verified_at": lkg.get("verified_at"),
            "username": lkg.get("username"),
        }
        error["restore_command"] = "tg-reader-telethon restore-session"

    print(json.dumps(error, indent=2))
    sys.exit(1)


# ── Config ──────────────────────────────────────────────────────────────────

def get_config(config_file=None, session_file=None):
    """Load credentials from env or config file (env takes priority).

    Args:
        config_file: Explicit path to config JSON (overrides ~/.tg-reader.json)
        session_file: Explicit path to session file (overrides default and config value)
    """
    global _PROXY

    api_id = os.environ.get("TG_API_ID")
    api_hash = os.environ.get("TG_API_HASH")
    session_name = os.environ.get("TG_SESSION", str(Path.home() / ".telethon-reader"))
    proxy_spec = os.environ.get("TG_PROXY")

    # Read the config file whenever it exists — the proxy lives there even when
    # credentials come from the environment.
    config_path = Path(config_file) if config_file else Path.home() / ".tg-reader.json"
    if config_path.exists():
        with open(config_path) as f:
            cfg = json.load(f)
            api_id = api_id or cfg.get("api_id")
            api_hash = api_hash or cfg.get("api_hash")
            session_name = cfg.get("session", session_name)
            proxy_spec = proxy_spec or cfg.get("socks_proxy")

    _PROXY = _parse_proxy(proxy_spec)

    # Explicit --session-file overrides everything
    if session_file:
        session_name = session_file

    if not api_id or not api_hash:
        print(json.dumps({
            "error": "Missing credentials. Set TG_API_ID and TG_API_HASH env vars, "
                     "or create ~/.tg-reader.json with {\"api_id\": ..., \"api_hash\": \"...\"}. "
                     "For isolated agents, pass --config-file /path/to/tg-reader.json"
        }))
        sys.exit(1)

    # Normalize: strip .session suffix if user passed full filename
    if session_name.endswith(".session"):
        session_name = session_name[: -len(".session")]

    return int(api_id), api_hash, session_name


# ── Non-interactive client ───────────────────────────────────────────────────

@asynccontextmanager
async def _authorized_client(session_name: str, api_id: int, api_hash: str):
    """Open a client with NO interactive auth path — never prompts for a phone.

    ``connect()`` + ``is_user_authorized()`` instead of ``start()`` (which
    prompts for a phone number on an unauthorized session). ``get_me()``
    identifies the user for the last-good manifest.

    Raises NotAuthorizedError / NetworkError; the two are never conflated:
    a network failure says nothing about session validity, and reporting it
    as an auth problem pushes agents toward destructive re-auth.

    On a clean exit the now-verified session is snapshotted as last-known-good
    (client disconnected first, caller still holds the lock). This lives here,
    not in each caller, so every authorized path gets the snapshot — including
    channel-error returns, where the session itself is fine.
    """
    try:
        client = TelegramClient(session_name, api_id, api_hash, proxy=_PROXY)
        await client.connect()
    except sqlite3.Error as e:
        raise NotAuthorizedError(f"Session file could not be opened (corrupted?): {e}")
    except (OSError, TimeoutError, ConnectionError) as e:
        raise NetworkError(str(e))
    except Exception as e:
        # Unknown failure — default to "network", the non-destructive verdict.
        raise NetworkError(f"{type(e).__name__}: {e}")
    body_ok = False
    try:
        if not await client.is_user_authorized():
            raise NotAuthorizedError(
                "Session file exists but holds NO authorized user. This does not "
                "mean Telegram revoked anything — the local file may be empty, "
                "corrupted, or overwritten by another process."
            )
        try:
            me = await client.get_me()
        except Exception as e:
            raise NetworkError(f"Could not verify authorization: {type(e).__name__}: {e}")
        yield client, me
        body_ok = True
    finally:
        await client.disconnect()
    if body_ok:
        save_last_good(session_name, user_id=me.id, username=me.username, backend="telethon")


def _print_session_error(session_name: str, error_type: str, message: str) -> None:
    """Print a structured session-level error for the agent."""
    err: dict = {"error": message, "error_type": error_type}
    if error_type == "not_authorized":
        lkg = load_last_good_info(session_name)
        if lkg:
            err["last_good_backup"] = {
                "path": lkg.get("path"),
                "verified_at": lkg.get("verified_at"),
                "username": lkg.get("username"),
            }
            err["action"] = "offer_restore"
            err["restore_command"] = "tg-reader-telethon restore-session"
        else:
            err["action"] = "run_auth_interactive"
            err["fix"] = "tg-reader-telethon auth  (interactive — needs phone + code from the user)"
        err["background_policy"] = (
            "If this is a scheduled/background run: do NOT attempt auth or "
            "restore, do NOT delete/move session files or edit the config — "
            "notify the user and exit."
        )
    else:
        err["action"] = "retry_later"
    print(json.dumps(err, indent=2))


# ── Core ─────────────────────────────────────────────────────────────────────

def parse_since(since: str) -> datetime:
    """Parse --since flag: '24h', '7d', '2026-02-01', etc."""
    since = since.strip()
    now = datetime.now(timezone.utc)
    if since.endswith("h"):
        return now - timedelta(hours=int(since[:-1]))
    if since.endswith("d"):
        return now - timedelta(days=int(since[:-1]))
    if since.endswith("w"):
        return now - timedelta(weeks=int(since[:-1]))
    # Try ISO date
    try:
        dt = datetime.fromisoformat(since)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        raise ValueError(f"Cannot parse --since value: {since!r}. Use '24h', '7d', or 'YYYY-MM-DD'.")


def _extract_web_page(msg):
    """Return link-preview card fields from msg.media (MessageMediaWebPage).

    Telethon wraps the card in MessageMediaWebPage with a WebPage object inside.
    WebPageEmpty / WebPagePending / WebPageNotModified are skipped because they
    do not expose a usable URL.

    Returns a dict, or None when there is no preview or the preview has no URL.
    """
    media = getattr(msg, "media", None)
    if not isinstance(media, MessageMediaWebPage):
        return None
    wp = getattr(media, "webpage", None)
    if not wp:
        return None
    url = getattr(wp, "url", None)
    if not url:
        return None
    data = {"url": url}
    for field in ("display_url", "title", "description", "site_name"):
        value = getattr(wp, field, None)
        if value:
            data[field] = value
    return data


def _synth_text_from_web_page(wp: dict) -> str:
    """Build text from title/description/url so card-only posts surface real content."""
    parts = []
    if wp.get("title"):
        parts.append(wp["title"])
    if wp.get("description"):
        parts.append(wp["description"])
    if wp.get("url"):
        parts.append(wp["url"])
    return "\n\n".join(parts)


async def _check_discussion_group(client, entity) -> bool:
    """Check whether the channel has a linked discussion group (comments)."""
    try:
        full = await client(GetFullChannelRequest(entity))
        return full.full_chat.linked_chat_id is not None
    except Exception:
        return False


async def _fetch_comments(client, entity, message_id: int, comment_limit: int) -> list:
    """Fetch discussion replies (comments) for a single channel post.

    Returns a list of comment dicts. Skips media-only comments (no text).
    Re-raises FloodWaitError so the caller can handle retries.
    """
    comments = []
    try:
        async for reply in client.iter_messages(entity, reply_to=message_id, limit=comment_limit):
            text = reply.message or ""
            web_page = _extract_web_page(reply)
            if not text and web_page:
                text = _synth_text_from_web_page(web_page)
            if not text:
                continue
            from_user = None
            if reply.sender:
                from_user = getattr(reply.sender, "username", None) or str(reply.sender_id)
            reply_date = reply.date.replace(tzinfo=timezone.utc)
            comment = {
                "id": reply.id,
                "date": reply_date.isoformat(),
                "text": text,
                "from_user": from_user,
            }
            if web_page:
                comment["web_page"] = web_page
            comments.append(comment)
    except FloodWaitError:
        raise  # let caller handle retry
    except Exception:
        pass  # comments unavailable for this post
    return comments


async def fetch_messages(client: TelegramClient, channel: str, since: datetime, limit: int, text_only: bool,
                         comments: bool = False, comment_limit: int = 10, comment_delay: float = 3,
                         min_id: int = 0):
    """Fetch messages from a single channel."""
    messages = []

    try:
        # Get the channel entity
        entity = await client.get_entity(channel)

        # Ensure it's a channel
        if not isinstance(entity, Channel):
            return {"error": f"'{channel}' is not a channel", "channel": channel}

        # Check discussion group availability once (only when comments requested)
        has_discussion = False
        if comments:
            has_discussion = await _check_discussion_group(client, entity)

        # Fetch messages
        msg_index = 0
        async for msg in client.iter_messages(entity, limit=limit, min_id=min_id):
            # Check if message is older than 'since'
            msg_date = msg.date.replace(tzinfo=timezone.utc)
            if msg_date < since:
                break

            # Extract message data
            text = msg.message or ""

            # Link-preview card: extract structured fields and treat as non-media
            # so behaviour matches the Pyrogram backend (--text-only keeps these
            # posts; has_media reflects "real" attachments only).
            web_page = _extract_web_page(msg)
            has_other_media = msg.media is not None and not isinstance(msg.media, MessageMediaWebPage)

            # When the message has no text of its own, synthesize text from the
            # card so the post surfaces in --text-only and downstream agents.
            if not text and web_page:
                text = _synth_text_from_web_page(web_page)

            # --text-only: skip posts that have no text at all
            if text_only and not text:
                continue

            entry = {
                "id": msg.id,
                "date": msg_date.isoformat(),
                "text": text,
                "views": msg.views or 0,
                "forwards": msg.forwards or 0,
                "link": f"https://t.me/{channel.lstrip('@')}/{msg.id}",
                "has_media": has_other_media,
            }

            if has_other_media:
                entry["media_type"] = type(msg.media).__name__
            if web_page:
                entry["web_page"] = web_page

            # Fetch comments for this post
            if comments and has_discussion:
                if msg_index > 0:
                    await asyncio.sleep(comment_delay)
                try:
                    post_comments = await _fetch_comments(client, entity, msg.id, comment_limit)
                    entry["comment_count"] = len(post_comments)
                    entry["comments"] = post_comments
                except FloodWaitError as e:
                    if e.seconds <= _FLOOD_WAIT_MAX:
                        await asyncio.sleep(e.seconds)
                        try:
                            post_comments = await _fetch_comments(client, entity, msg.id, comment_limit)
                            entry["comment_count"] = len(post_comments)
                            entry["comments"] = post_comments
                        except Exception:
                            entry["comment_count"] = 0
                            entry["comments"] = []
                    else:
                        entry["comment_count"] = 0
                        entry["comments"] = []
                        entry["comments_error"] = f"Rate limited: retry after {e.seconds}s"

            messages.append(entry)
            msg_index += 1

    except (ChannelPrivateError, ChatForbiddenError, ChatRestrictedError) as e:
        return _channel_error(
            channel, "access_denied",
            f"Channel is private or access denied: {e}",
            "remove_from_list_or_rejoin",
        )
    except (ChannelBannedError, UserBannedInChannelError) as e:
        return _channel_error(
            channel, "banned",
            f"Banned from channel: {e}",
            "remove_from_list",
        )
    except (ChannelInvalidError, ChatInvalidError, PeerIdInvalidError,
            UsernameNotOccupiedError, ValueError) as e:
        return _channel_error(
            channel, "not_found",
            f"Channel not found or username is incorrect: {e}",
            "check_username",
        )
    except (InviteHashExpiredError, InviteHashInvalidError) as e:
        return _channel_error(
            channel, "invite_expired",
            f"Invite link expired or invalid: {e}",
            "request_new_invite",
        )
    except FloodWaitError as e:
        return _channel_error(
            channel, "flood_wait",
            f"Rate limited: retry after {e.seconds}s",
            f"wait_{e.seconds}s",
        )
    except Exception as e:
        return _channel_error(
            channel, "unexpected",
            f"Unexpected error: {e}",
            "report_to_user",
        )

    result = {
        "channel": channel,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "since": since.isoformat(),
        "count": len(messages),
        "messages": messages,
    }
    if comments:
        result["comments_enabled"] = True
        result["comments_available"] = has_discussion
    return result


_FLOOD_WAIT_MAX = 60  # auto-retry only if wait is <= this many seconds


async def fetch_multiple(channels: list, since: datetime, limit: int, text_only: bool,
                         config_file=None, session_file=None, delay: float = 10,
                         min_ids: dict = None):
    """Fetch messages from multiple channels sequentially with delays.

    Channels are fetched one at a time to avoid Telegram FloodWait.
    If a FloodWait <= 60s is hit, the request is retried once automatically.
    """
    api_id, api_hash, session_name = get_config(config_file, session_file)
    _validate_session(session_name)

    results = []
    async with _authorized_client(session_name, api_id, api_hash) as (client, me):
        for i, channel in enumerate(channels):
            channel_min_id = (min_ids or {}).get(channel, 0)
            result = await fetch_messages(client, channel, since, limit, text_only,
                                          min_id=channel_min_id)

            # Auto-retry on FloodWait if wait is reasonable
            if (isinstance(result, dict) and result.get("error_type") == "flood_wait"):
                wait_action = result.get("action", "")
                try:
                    wait_seconds = int(wait_action.replace("wait_", "").replace("s", ""))
                except (ValueError, AttributeError):
                    wait_seconds = 0
                if 0 < wait_seconds <= _FLOOD_WAIT_MAX:
                    await asyncio.sleep(wait_seconds)
                    result = await fetch_messages(client, channel, since, limit, text_only,
                                                  min_id=channel_min_id)

            results.append(result)

            # Delay between channels (skip after the last one)
            if i < len(channels) - 1:
                await asyncio.sleep(delay)

    # _authorized_client snapshots the verified session as last-good on exit.
    return results


async def fetch_single(channel: str, since: datetime, limit: int, text_only: bool,
                       config_file=None, session_file=None,
                       comments: bool = False, comment_limit: int = 10, comment_delay: float = 3,
                       min_id: int = 0):
    """Fetch messages from a single channel."""
    api_id, api_hash, session_name = get_config(config_file, session_file)
    _validate_session(session_name)

    async with _authorized_client(session_name, api_id, api_hash) as (client, me):
        result = await fetch_messages(client, channel, since, limit, text_only,
                                      comments=comments, comment_limit=comment_limit,
                                      comment_delay=comment_delay, min_id=min_id)
    # _authorized_client snapshots the verified session as last-good on exit.
    return result


# ── Auth setup ───────────────────────────────────────────────────────────────

async def setup_auth(config_file=None, session_file=None):
    """Interactive first-time auth — creates session file.

    An existing session file is backed up first (auth overwrites it), and the
    fresh session is verified with get_me() and snapshotted as last-good.
    """
    api_id, api_hash, session_name = get_config(config_file, session_file)
    backup = backup_session(session_name)
    if backup:
        print(f"Existing session backed up to: {backup}")
    print(f"Starting auth for session: {session_name}.session")
    print("You will receive a code in Telegram. Enter it when prompted.\n")

    client = TelegramClient(session_name, api_id, api_hash, proxy=_PROXY)

    # Use lambda to make phone input interactive
    await client.start(phone=lambda: input("Enter phone number (with country code, e.g. +79991234567): "))

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"\n✅ Authenticated as: {me.phone} ({me.first_name})")
        status = {
            "status": "authenticated",
            "user": me.username or str(me.id),
            "phone": me.phone,
            "session_file": f"{session_name}.session",
        }
        if backup:
            status["previous_session_backup"] = backup
        print(json.dumps(status))
    else:
        print(json.dumps({"error": "Authentication failed"}))
        sys.exit(1)

    await client.disconnect()
    save_last_good(session_name, user_id=me.id, username=me.username, backend="telethon")


# ── Session restore ──────────────────────────────────────────────────────────

async def _verify_authorized(session_name, api_id, api_hash):
    """Connect non-interactively and return the authorized user."""
    async with _authorized_client(session_name, api_id, api_hash) as (client, me):
        return me


def restore_session(config_file=None, session_file=None):
    """Restore the last-known-good session copy and verify it against Telegram.

    Explicit recovery for a destroyed/emptied session file. The broken file is
    moved aside (never deleted); the backup is checksum-verified before install.
    """
    api_id, api_hash, session_name = get_config(config_file, session_file)
    try:
        restored = restore_last_good(session_name)
    except ValueError as e:
        print(json.dumps({
            "error": str(e),
            "error_type": "not_authorized",
            "action": "run_auth_interactive",
        }, indent=2))
        sys.exit(1)

    try:
        me = asyncio.run(_verify_authorized(session_name, api_id, api_hash))
    except NotAuthorizedError as e:
        print(json.dumps({
            "status": "restored_but_not_authorized",
            "error": f"Restored the last-good copy, but Telegram does not accept it: {e}",
            "error_type": "not_authorized",
            "action": "run_auth_interactive",
            **restored,
        }, indent=2))
        sys.exit(1)
    except NetworkError as e:
        print(json.dumps({
            "status": "restored_unverified",
            "error": f"Restored the last-good copy, but could not reach Telegram to verify: {e}",
            "error_type": "network",
            "action": "retry_later",
            **restored,
        }, indent=2))
        sys.exit(1)

    # _verify_authorized already refreshed the last-good snapshot via the
    # context manager — no explicit save needed here.
    print(json.dumps({
        "status": "restored",
        "verified": True,
        "user": me.username or str(me.id),
        **restored,
    }, indent=2))


# ── Output helpers ────────────────────────────────────────────────────────────

def _print_text(result, since_label):
    """Print human-readable text output to stdout."""
    items = result if isinstance(result, list) else [result]
    for ch_result in items:
        if "error" in ch_result:
            print(f"[ERROR] {ch_result['channel']}: {ch_result['error']}")
            continue
        print(f"\n=== {ch_result['channel']} ({ch_result['count']} posts since {since_label}) ===")
        for msg in ch_result["messages"]:
            print(f"\n[{msg['date']}] {msg['link']}")
            print(msg["text"][:500] + ("..." if len(msg["text"]) > 500 else ""))
            wp = msg.get("web_page")
            if wp:
                title = wp.get("title") or wp.get("site_name") or ""
                url = wp.get("url", "")
                if title:
                    print(f"  \U0001f517 {title} — {url}")
                else:
                    print(f"  \U0001f517 {url}")
            if "comments" in msg and msg["comments"]:
                print(f"  [{msg['comment_count']} comments]")
                for c in msg["comments"]:
                    user = c.get("from_user") or "anonymous"
                    print(f"    @{user}: {c['text'][:200]}")


def _write_output(result, output_path, fmt, since_label):
    """Write output to a file and print a short confirmation to stdout."""
    output_path = os.path.abspath(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        if fmt == "json":
            json.dump(result, f, ensure_ascii=False, indent=2)
            f.write("\n")
        else:
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                _print_text(result, since_label)
            f.write(buf.getvalue())

    if isinstance(result, list):
        count = sum(r.get("count", 0) for r in result if "error" not in r)
    else:
        count = result.get("count", 0) if "error" not in result else 0
    print(json.dumps({"status": "ok", "output_file": output_path, "count": count}, ensure_ascii=False))


# ── CLI helpers ──────────────────────────────────────────────────────────────

# Common flags hallucinated by LLM agents instead of --since
_FLAG_TYPOS = {
    "--hours": "--since (e.g. --since 24h)",
    "--days": "--since (e.g. --since 7d)",
    "--weeks": "--since (e.g. --since 2w)",
    "--time": "--since (e.g. --since 24h)",
    "--period": "--since (e.g. --since 24h)",
    "--after": "--since (e.g. --since 24h)",
    "--from": "--since (e.g. --since 24h or --since 2026-01-01)",
    "--media": "--text-only (inverted: use --text-only to exclude media-only posts)",
}


def _check_flag_typos():
    """Catch common parameter hallucinations from LLM agents and exit with a helpful JSON error."""
    for arg in sys.argv[1:]:
        if arg in _FLAG_TYPOS:
            print(json.dumps({
                "error": f"Unknown flag: {arg}. Did you mean {_FLAG_TYPOS[arg]}?",
                "action": "fix_command",
            }))
            sys.exit(1)


class _JsonArgumentParser(argparse.ArgumentParser):
    """ArgumentParser that outputs errors as JSON instead of plain text."""

    def error(self, message):
        # Check for flag typos in the error message
        for typo, fix in _FLAG_TYPOS.items():
            if typo in message:
                print(json.dumps({
                    "error": f"Unknown flag: {typo}. Did you mean {fix}?",
                    "action": "fix_command",
                }))
                sys.exit(1)
        print(json.dumps({"error": f"Invalid command: {message}", "action": "fix_command"}))
        sys.exit(1)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    _check_flag_typos()

    parser = _JsonArgumentParser(
        prog="tg-reader-telethon",
        description="Read Telegram channel posts for OpenClaw agent (Telethon version)"
    )
    # Global options (available to all subcommands)
    parser.add_argument("--config-file", default=None,
                        help="Path to config JSON (overrides ~/.tg-reader.json)")
    parser.add_argument("--session-file", default=None,
                        help="Path to session file (overrides default session path)")

    sub = parser.add_subparsers(dest="cmd", required=True)

    # fetch
    fetch_p = sub.add_parser("fetch", help="Fetch posts from one or more channels")
    fetch_p.add_argument("channels", nargs="+", help="Channel usernames e.g. @durov")
    fetch_p.add_argument("--since", default="24h", help="Time window: 24h, 7d, 2w, or YYYY-MM-DD")
    fetch_p.add_argument("--limit", type=int, default=100, help="Max posts per channel (default 100)")
    fetch_p.add_argument("--text-only", action="store_true",
                        help="Skip posts that have no text (media-only without caption)")
    fetch_p.add_argument("--delay", type=float, default=10,
                        help="Seconds to wait between channels (default 10)")
    fetch_p.add_argument("--comments", action="store_true",
                        help="Fetch comments for each post (single channel only)")
    fetch_p.add_argument("--comment-limit", type=int, default=10,
                        help="Max comments per post (default 10)")
    fetch_p.add_argument("--comment-delay", type=float, default=3,
                        help="Seconds between comment fetches per post (default 3)")
    fetch_p.add_argument("--format", choices=["json", "text"], default="json")
    fetch_p.add_argument("--output", nargs="?", const="tg-output.json", default=None,
                        help="Write output to file instead of stdout (default: tg-output.json)")
    fetch_p.add_argument("--all", action="store_true", dest="fetch_all",
                        help="Ignore read tracking and fetch all matching posts")
    fetch_p.add_argument("--state-file", default=None,
                        help="Path to state file for read tracking (overrides config)")

    # auth
    sub.add_parser("auth", help="Authenticate with Telegram (first-time setup)")

    # restore-session
    sub.add_parser("restore-session",
                   help="Restore the last-known-good session backup and verify it")

    args = parser.parse_args()
    cf = args.config_file
    sf = args.session_file
    _, _, session_name = get_config(cf, sf)

    if args.cmd != "auth":
        # Hard guard: non-interactive commands must never block on stdin.
        # _authorized_client leaves no prompt path, but if any library code
        # still tries to read input it gets EOFError instead of hanging.
        sys.stdin = open(os.devnull)

    try:
        # One tg-reader process per session at a time — concurrent access
        # corrupts the SQLite session file (see tasks/task-0004.md).
        with session_lock(session_name):
            _dispatch(args, cf, sf)
    except SessionLockTimeout:
        _print_session_error(
            session_name, "busy",
            "Another tg-reader process is using this session — try again later",
        )
        sys.exit(1)
    except NotAuthorizedError as e:
        _print_session_error(session_name, "not_authorized", str(e))
        sys.exit(1)
    except NetworkError as e:
        _print_session_error(session_name, "network", f"Could not reach Telegram: {e}")
        sys.exit(1)


def _dispatch(args, cf, sf):
    if args.cmd == "auth":
        asyncio.run(setup_auth(cf, sf))
        return

    if args.cmd == "restore-session":
        restore_session(cf, sf)
        return

    if args.cmd == "fetch":
        try:
            since_dt = parse_since(args.since)
        except ValueError as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)

        # Validate --comments constraints
        if args.comments:
            if len(args.channels) > 1:
                print(json.dumps({
                    "error": "--comments can only be used with a single channel",
                    "action": "remove_extra_channels_or_drop_comments",
                }))
                sys.exit(1)

        # Lower default limit when fetching comments (token economy)
        limit = args.limit
        if args.comments and limit == 100:
            limit = 30

        # Read tracking (read_unread mode)
        from tg_state import load_tracking_config, load_state, get_last_read_id, update_state, save_state

        read_unread, state_file_path = load_tracking_config(cf)
        if args.state_file:
            state_file_path = args.state_file

        use_tracking = read_unread and not args.fetch_all
        state = None
        min_id = 0
        min_ids = {}

        if use_tracking:
            state = load_state(state_file_path)
            if len(args.channels) == 1:
                min_id = get_last_read_id(state, args.channels[0])
            else:
                min_ids = {ch: get_last_read_id(state, ch) for ch in args.channels}

            # When tracking has state, --since is not needed — fetch all unread.
            # On first run (no state, min_id=0), --since still applies (default 24h).
            has_state = min_id > 0 or any(v > 0 for v in min_ids.values())
            if has_state:
                since_dt = datetime(2000, 1, 1, tzinfo=timezone.utc)

        if len(args.channels) == 1:
            result = asyncio.run(fetch_single(
                args.channels[0], since_dt, limit, args.text_only, cf, sf,
                comments=args.comments, comment_limit=args.comment_limit,
                comment_delay=args.comment_delay, min_id=min_id))
        else:
            result = asyncio.run(fetch_multiple(args.channels, since_dt, limit, args.text_only, cf, sf,
                                                delay=args.delay, min_ids=min_ids))

        # Update tracking state after successful fetch
        if use_tracking and state is not None:
            if isinstance(result, list):
                for ch_result in result:
                    if "error" not in ch_result and ch_result.get("messages"):
                        newest_id = max(m["id"] for m in ch_result["messages"])
                        update_state(state, ch_result["channel"], newest_id)
            elif "error" not in result and result.get("messages"):
                newest_id = max(m["id"] for m in result["messages"])
                update_state(state, result["channel"], newest_id)
            save_state(state, state_file_path)

        # Add tracking metadata to output
        if read_unread:
            tracking_meta = {"enabled": True}
            if args.fetch_all:
                tracking_meta["overridden"] = True
            if isinstance(result, list):
                for ch_result in result:
                    if "error" not in ch_result:
                        ch_result["read_unread"] = tracking_meta.copy()
            elif "error" not in result:
                result["read_unread"] = tracking_meta

        if args.output:
            _write_output(result, args.output, args.format, args.since)
        elif args.format == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            _print_text(result, args.since)


if __name__ == "__main__":
    main()