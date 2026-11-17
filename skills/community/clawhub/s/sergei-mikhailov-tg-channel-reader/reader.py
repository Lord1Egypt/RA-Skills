#!/usr/bin/env python3
"""
tg-channel-reader — Telegram channel reader skill for OpenClaw
Reads posts from public/private Telegram channels via MTProto (Pyrogram)
"""

import argparse
import asyncio
import json
import os
import sqlite3
import sys
import time
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
    from pyrogram import Client
    from pyrogram.errors import (
        FloodWait,
        ChannelInvalid,
        ChannelPrivate,
        ChannelBanned,
        ChatForbidden,
        ChatInvalid,
        ChatRestricted,
        PeerIdInvalid,
        UsernameNotOccupied,
        UserBannedInChannel,
        InviteHashExpired,
        InviteHashInvalid,
        Unauthorized,
        SessionPasswordNeeded,
        PhoneCodeInvalid,
        PhoneCodeExpired,
        PhoneNumberInvalid,
    )
except ImportError:
    print(json.dumps({"error": "pyrofork not installed. Run: pip install pyrofork tgcrypto (do NOT install pyrogram — its PyPI release is frozen at 2.0.106 and drops content from recent posts)"}))
    sys.exit(1)


def _channel_error(channel: str, error_type: str, message: str, action: str) -> dict:
    """Build a structured channel error dict for the agent."""
    return {
        "error": message,
        "error_type": error_type,
        "channel": channel,
        "action": action,
    }


# Use Pyrogram's default device identity (Python MTProto client).
# Spoofing a mobile client causes Telegram to terminate sessions — the
# behaviour doesn't match and it's detected server-side.
_DEVICE: dict = {}

# SOCKS5 proxy for MTProto, populated by get_config() from ~/.tg-reader.json
# ("socks_proxy") or the TG_PROXY env var. Some hosts filter direct MTProto
# (TCP 443 to Telegram DCs), so a client may need to route through it.
_PROXY: dict | None = None


def _parse_proxy(spec):
    """Parse "host:port" or "socks5://[user:pass@]host:port" into a Pyrogram
    proxy dict, or return None for an empty/invalid spec."""
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
    proxy = {"scheme": scheme, "hostname": host, "port": port}
    if username:
        proxy["username"] = username
        proxy["password"] = password
    return proxy


# ── Session helpers ──────────────────────────────────────────────────────────

_SESSION_NAMES = [
    ".tg-reader-session.session",
    ".telethon-reader.session",
    "tg-reader-session.session",
    "telethon-reader.session",
]


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
            "Run 'tg-reader auth' to create a new session",
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
        error["restore_command"] = "tg-reader restore-session"

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
    session_name = os.environ.get("TG_SESSION", str(Path.home() / ".tg-reader-session"))
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

    ``Client.connect()`` returns the authorization status without prompting;
    ``start()`` (what ``async with Client`` calls) would run ``authorize()``,
    which blocks on a phone-number prompt when the session is unauthorized —
    fatal in cron, and by then the SQLite session is already open for writing.
    ``get_me()`` then confirms Telegram actually accepts the auth key.

    Raises NotAuthorizedError / NetworkError; the two are never conflated:
    a network failure says nothing about session validity, and reporting it
    as an auth problem pushes agents toward destructive re-auth.

    On a clean exit (the body ran without raising) the now-verified session is
    snapshotted as last-known-good — the client is disconnected first so the
    SQLite file is quiesced, and the caller still holds the session lock. This
    lives here, not in each caller, so every authorized path gets the snapshot
    (including channel-error returns, where the session itself is fine).
    """
    app = Client(session_name, api_id=api_id, api_hash=api_hash, proxy=_PROXY, **_DEVICE)
    try:
        authorized = await app.connect()
    except sqlite3.Error as e:
        raise NotAuthorizedError(f"Session file could not be opened (corrupted?): {e}")
    except (OSError, TimeoutError, ConnectionError) as e:
        raise NetworkError(str(e))
    except Exception as e:
        # Unknown failure — default to "network", the non-destructive verdict.
        raise NetworkError(f"{type(e).__name__}: {e}")
    if not authorized:
        await app.disconnect()
        raise NotAuthorizedError(
            "Session file exists but holds NO authorized user. This does not "
            "mean Telegram revoked anything — the local file may be empty, "
            "corrupted, or overwritten by another process."
        )
    try:
        me = await app.get_me()
    except Unauthorized as e:
        await app.disconnect()
        raise NotAuthorizedError(
            f"Telegram rejected the session key ({type(e).__name__}): {e}"
        )
    except Exception as e:
        await app.disconnect()
        raise NetworkError(f"Could not verify authorization: {type(e).__name__}: {e}")
    body_ok = False
    try:
        await app.initialize()
        try:
            yield app, me
            body_ok = True
        finally:
            await app.terminate()
    finally:
        await app.disconnect()
    if body_ok:
        save_last_good(session_name, user_id=me.id, username=me.username, backend="pyrogram")


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
            err["restore_command"] = "tg-reader restore-session"
        else:
            err["action"] = "run_auth_interactive"
            err["fix"] = "tg-reader auth  (interactive — needs phone + code from the user)"
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
    """Return link-preview card fields from msg.web_page if present and usable.

    Pyrogram exposes the card as msg.web_page (separate from msg.media).
    Returns a dict, or None when there is no preview or the preview has no URL.
    """
    wp = getattr(msg, "web_page", None)
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


async def _check_discussion_group(app, channel: str) -> bool:
    """Check whether the channel has a linked discussion group (comments)."""
    try:
        chat = await app.get_chat(channel)
        return chat.linked_chat is not None
    except Exception:
        return False


async def _fetch_comments(app, channel: str, message_id: int, comment_limit: int) -> list:
    """Fetch discussion replies (comments) for a single channel post.

    Returns a list of comment dicts. Skips media-only comments (no text).
    Re-raises FloodWait so the caller can handle retries.
    """
    comments = []
    try:
        async for reply in app.get_discussion_replies(channel, message_id, limit=comment_limit):
            text = ""
            if reply.text:
                text = reply.text
            elif reply.caption:
                text = reply.caption
            web_page = _extract_web_page(reply)
            if not text and web_page:
                text = _synth_text_from_web_page(web_page)
            if not text:
                continue
            from_user = None
            if reply.from_user:
                from_user = reply.from_user.username or str(reply.from_user.id)
            reply_date = reply.date if reply.date.tzinfo else reply.date.replace(tzinfo=timezone.utc)
            comment = {
                "id": reply.id,
                "date": reply_date.isoformat(),
                "text": text,
                "from_user": from_user,
            }
            if web_page:
                comment["web_page"] = web_page
            comments.append(comment)
    except FloodWait:
        raise  # let caller handle retry
    except Exception:
        pass  # comments unavailable for this post
    return comments


async def _fetch_channel(app, channel: str, since: datetime, limit: int, text_only: bool,
                         comments: bool = False, comment_limit: int = 10, comment_delay: float = 3,
                         min_id: int = 0):
    """Fetch messages from a single channel using an existing Client session."""
    # Check discussion group availability once (only when comments requested)
    has_discussion = False
    if comments:
        has_discussion = await _check_discussion_group(app, channel)

    messages = []
    try:
        msg_index = 0
        async for msg in app.get_chat_history(channel, limit=limit):
            msg_date = msg.date if msg.date.tzinfo else msg.date.replace(tzinfo=timezone.utc)
            if msg_date < since:
                break
            # Break if we've reached already-read messages
            if min_id and msg.id <= min_id:
                break
            # Pyrogram: text for plain messages, caption for media messages
            text = ""
            if msg.text:
                text = msg.text
            elif msg.caption:
                text = msg.caption

            # Link-preview card (separate from msg.media in Pyrogram).
            # When the message has no text of its own, synthesize text from the
            # card so the post surfaces in --text-only and downstream agents.
            web_page = _extract_web_page(msg)
            if not text and web_page:
                text = _synth_text_from_web_page(web_page)

            # --text-only: skip posts that have no text at all
            if text_only and not text:
                continue

            entry = {
                "id": msg.id,
                "date": msg_date.isoformat(),
                "text": text,
                "views": msg.views,
                "forwards": msg.forwards,
                "link": f"https://t.me/{channel.lstrip('@')}/{msg.id}",
                "has_media": msg.media is not None,
            }
            if msg.media:
                entry["media_type"] = str(msg.media)
            if web_page:
                entry["web_page"] = web_page

            # Fetch comments for this post
            if comments and has_discussion:
                if msg_index > 0:
                    await asyncio.sleep(comment_delay)
                try:
                    post_comments = await _fetch_comments(app, channel, msg.id, comment_limit)
                    entry["comment_count"] = len(post_comments)
                    entry["comments"] = post_comments
                except FloodWait as e:
                    if e.value <= _FLOOD_WAIT_MAX:
                        await asyncio.sleep(e.value)
                        try:
                            post_comments = await _fetch_comments(app, channel, msg.id, comment_limit)
                            entry["comment_count"] = len(post_comments)
                            entry["comments"] = post_comments
                        except Exception:
                            entry["comment_count"] = 0
                            entry["comments"] = []
                    else:
                        entry["comment_count"] = 0
                        entry["comments"] = []
                        entry["comments_error"] = f"Rate limited: retry after {e.value}s"

            messages.append(entry)
            msg_index += 1
    except (ChannelPrivate, ChatForbidden, ChatRestricted) as e:
        return _channel_error(
            channel, "access_denied",
            f"Channel is private or access denied: {e}",
            "remove_from_list_or_rejoin",
        )
    except (ChannelBanned, UserBannedInChannel) as e:
        return _channel_error(
            channel, "banned",
            f"Banned from channel: {e}",
            "remove_from_list",
        )
    except (ChannelInvalid, ChatInvalid, PeerIdInvalid, UsernameNotOccupied) as e:
        return _channel_error(
            channel, "not_found",
            f"Channel not found or username is incorrect: {e}",
            "check_username",
        )
    except KeyError as e:
        # Pyrogram raises KeyError from resolve_peer / get_peer_by_username
        # when the username doesn't exist in Telegram's database
        return _channel_error(
            channel, "not_found",
            f"Username not found: {e}",
            "check_username",
        )
    except (InviteHashExpired, InviteHashInvalid) as e:
        return _channel_error(
            channel, "invite_expired",
            f"Invite link expired or invalid: {e}",
            "request_new_invite",
        )
    except FloodWait as e:
        return _channel_error(
            channel, "flood_wait",
            f"Rate limited: retry after {e.value}s",
            f"wait_{e.value}s",
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


async def fetch_messages(channel: str, since: datetime, limit: int, text_only: bool,
                         config_file=None, session_file=None,
                         comments: bool = False, comment_limit: int = 10, comment_delay: float = 3,
                         min_id: int = 0):
    api_id, api_hash, session_name = get_config(config_file, session_file)
    _validate_session(session_name)
    async with _authorized_client(session_name, api_id, api_hash) as (app, me):
        result = await _fetch_channel(app, channel, since, limit, text_only,
                                      comments=comments, comment_limit=comment_limit,
                                      comment_delay=comment_delay, min_id=min_id)
    # _authorized_client snapshots the verified session as last-good on exit.
    return result


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
    async with _authorized_client(session_name, api_id, api_hash) as (app, me):
        for i, channel in enumerate(channels):
            channel_min_id = (min_ids or {}).get(channel, 0)
            result = await _fetch_channel(app, channel, since, limit, text_only,
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
                    result = await _fetch_channel(app, channel, since, limit, text_only,
                                                  min_id=channel_min_id)

            results.append(result)

            # Delay between channels (skip after the last one)
            if i < len(channels) - 1:
                await asyncio.sleep(delay)

    # _authorized_client snapshots the verified session as last-good on exit.
    return results


# ── Channel info ─────────────────────────────────────────────────────────────

async def fetch_info(channel: str, config_file=None, session_file=None):
    api_id, api_hash, session_name = get_config(config_file, session_file)
    _validate_session(session_name)
    async with _authorized_client(session_name, api_id, api_hash) as (app, me):
        try:
            chat = await app.get_chat(channel)
            result = {
                "id": chat.id,
                "title": chat.title,
                "username": chat.username,
                "description": chat.description,
                "members_count": chat.members_count,
                "link": f"https://t.me/{chat.username}" if chat.username else None,
            }
        except (ChannelPrivate, ChatForbidden, ChatRestricted) as e:
            return _channel_error(
                channel, "access_denied",
                f"Channel is private or access denied: {e}",
                "remove_from_list_or_rejoin",
            )
        except (ChannelBanned, UserBannedInChannel) as e:
            return _channel_error(
                channel, "banned",
                f"Banned from channel: {e}",
                "remove_from_list",
            )
        except (ChannelInvalid, ChatInvalid, PeerIdInvalid, UsernameNotOccupied) as e:
            return _channel_error(
                channel, "not_found",
                f"Channel not found or username is incorrect: {e}",
                "check_username",
            )
        except KeyError as e:
            return _channel_error(
                channel, "not_found",
                f"Username not found: {e}",
                "check_username",
            )
        except Exception as e:
            return _channel_error(
                channel, "unexpected",
                f"Unexpected error: {e}",
                "report_to_user",
            )
    # _authorized_client snapshots the verified session as last-good on exit —
    # this includes the channel-error returns above (the session is fine).
    return result


# ── Auth setup ───────────────────────────────────────────────────────────────

# ── Onboarding auth (agent-drivable, staged, non-interactive) ────────────────
#
# A first-time login needs three things Telegram will only give a human: the
# phone number, the login code Telegram sends, and (if enabled) the cloud
# 2FA password. This flow lets an AI agent collect those from the user and
# drive the login on their behalf — one live process, structured JSON stages,
# never a blocking `ainput` prompt (which is invisible in agent/exec contexts).
#
# Stages emitted to stdout (one JSON object per line, flushed):
#   {"stage":"need_phone",   "next_action":"provide_phone"}
#   {"stage":"code_sent",    "next_action":"provide_code", "code_type":"app"|"sms"}
#   {"stage":"need_2fa",     "next_action":"provide_password"}
#   {"stage":"authorized",   "user":..., "user_id":...}
#   {"stage":"already_authorized", "user":...}
#   {"stage":"error", "reason":"phone_invalid"|"code_invalid"|"code_expired"|...}
#
# Secrets (code, password) are read from a file (`--code-file`/`--password-file`,
# polled) or stdin — never passed on argv, so they don't leak into `ps`/logs.

def _auth_emit(obj):
    """Emit a stage as one flushed JSON line; also mirror to a progress file
    (TG_AUTH_PROGRESS) so an agent can read stages even if stdout is buffered
    through wrapper layers."""
    line = json.dumps(obj, ensure_ascii=False)
    print(line, flush=True)
    progress = os.environ.get("TG_AUTH_PROGRESS")
    if progress:
        try:
            with open(progress, "a") as f:
                f.write(line + "\n")
        except OSError:
            pass


async def _read_secret(secret_file, timeout=900):
    """Read a code/password from a file (polled until non-empty) or, if no file
    is given, from stdin. Returns the stripped value, or None on timeout."""
    if secret_file:
        start = time.monotonic()
        while time.monotonic() - start < timeout:
            try:
                if os.path.exists(secret_file):
                    val = open(secret_file).read().strip()
                    if val:
                        return val
            except OSError:
                pass
            await asyncio.sleep(1.5)
        return None
    # stdin fallback — run the blocking read off the event loop
    loop = asyncio.get_event_loop()
    try:
        line = await loop.run_in_executor(None, sys.stdin.readline)
    except Exception:
        return None
    return line.strip() or None


async def _probe_authorized(session_name, api_id, api_hash):
    """Return the authorized user for an existing session, or None if the file
    is missing/unauthorized/unreachable. Never prompts."""
    if not Path(f"{session_name}.session").exists():
        return None
    app = Client(session_name, api_id=api_id, api_hash=api_hash, proxy=_PROXY, **_DEVICE)
    try:
        if not await app.connect():
            return None
        try:
            return await app.get_me()
        except Exception:
            return None
    except Exception:
        return None
    finally:
        try:
            await app.disconnect()
        except Exception:
            pass


def _move_dead_session(session_name):
    """Move an existing (unauthorized) session file aside so a fresh login can
    start with a clean auth key. Never deletes."""
    src = Path(f"{session_name}.session")
    if not src.exists():
        return None
    dst = f"{session_name}.session.dead-{time.strftime('%Y%m%d-%H%M%S')}"
    try:
        src.rename(dst)
        return dst
    except OSError:
        return None


def _save_phone_to_config(config_file, phone):
    """Persist the phone into the config JSON so future re-auths don't need to
    ask for it again. Best-effort; failures are non-fatal."""
    path = Path(config_file) if config_file else Path.home() / ".tg-reader.json"
    try:
        cfg = json.load(open(path)) if path.exists() else {}
        cfg["phone"] = phone
        with open(path, "w") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
        return True
    except (OSError, json.JSONDecodeError):
        return False


def auth_guide(config_file=None, session_file=None):
    """Print human step-by-step instructions so the USER can authorize the
    skill themselves (used when they'd rather not have the agent do it)."""
    _, _, session_name = get_config(config_file, session_file)
    print(f"""tg-channel-reader — authorize it yourself (about 1 minute)

You'll log a Telegram account into the skill so it can read channels for you.
The login session is stored locally on this machine (OpenClaw), in
  {session_name}.session
It never leaves the machine and is not uploaded anywhere.

1. In a terminal on this machine, run:
     tg-reader auth --phone +7XXXXXXXXXX
   (use the phone number of the Telegram account that will read channels)

2. Telegram sends you a LOGIN CODE — usually inside the Telegram app itself
   (the "Telegram" service chat), sometimes by SMS. When prompted, paste it.

3. If that account has a cloud password (Two-Step Verification), you'll be
   asked for it too. Enter it.

4. Verify it worked:
     tg-reader-check --online
   You should see  "authorized": true.

If direct Telegram access is blocked on this host, set a SOCKS5 proxy first
(see "SOCKS5 proxy" in the skill docs): add "socks_proxy": "127.0.0.1:1080"
to ~/.tg-reader.json (or export TG_PROXY=...).""")


async def setup_auth(config_file=None, session_file=None, phone=None,
                     code_file=None, password_file=None,
                     remember_phone=False, force=False):
    """Agent-drivable staged login. See the module comment above for stages.

    One live process: send code -> wait for the code (file/stdin) -> sign in
    -> (if needed) wait for the 2FA password -> verify. The existing session is
    backed up first; a dead/unauthorized session is moved aside so the fresh
    login starts clean. Runs under the session lock held by main().
    """
    api_id, api_hash, session_name = get_config(config_file, session_file)

    # Already authorized? Don't disturb a working session unless forced.
    existing = await _probe_authorized(session_name, api_id, api_hash)
    if existing is not None and not force:
        _auth_emit({
            "stage": "already_authorized",
            "user": existing.username or str(existing.id),
            "user_id": existing.id,
            "session_file": f"{session_name}.session",
            "message": "Session is already authorized — nothing to do. Pass --force to re-login.",
        })
        return

    # Need the phone before we can send a code.
    phone = (phone or "").strip()
    if not phone:
        _auth_emit({
            "stage": "need_phone",
            "next_action": "provide_phone",
            "message": "Ask the user for the phone number of the Telegram reader "
                       "account (international format, e.g. +79991234567), then re-run "
                       "with --phone. The login session is stored locally on this "
                       "machine (OpenClaw) and never uploaded.",
        })
        return

    # Log in on a SCRATCH session first, then swap it into place only after a
    # verified success. A failed or aborted login must never take down a working
    # session (that's the class of bug session-hardening exists to prevent).
    moved = None
    if force and existing is not None:
        work = f"{session_name}.new-{time.strftime('%Y%m%d-%H%M%S')}"
        for suf in (".session", ".session-journal"):
            try:
                os.remove(work + suf)
            except OSError:
                pass
    else:
        # Fresh login into the real path; a dead auth key would block send_code,
        # so move any dead file aside first (never delete).
        work = session_name
        moved = _move_dead_session(session_name)

    app = Client(work, api_id=api_id, api_hash=api_hash, proxy=_PROXY, **_DEVICE)
    await app.connect()
    try:
        try:
            sent = await app.send_code(phone)
        except PhoneNumberInvalid:
            _auth_emit({"stage": "error", "reason": "phone_invalid",
                        "message": f"Telegram rejected the phone number: {phone}"})
            return
        _auth_emit({
            "stage": "code_sent",
            "code_type": str(getattr(sent, "type", "unknown")),
            "next_action": "provide_code",
            "message": "Telegram sent a login code (check the Telegram app on that "
                       "account, or SMS). Ask the user for it and provide it via "
                       "--code-file or stdin.",
        })
        code = await _read_secret(code_file)
        if not code:
            _auth_emit({"stage": "error", "reason": "timeout_code",
                        "message": "No login code was provided in time."})
            return
        try:
            await app.sign_in(phone, sent.phone_code_hash, code)
        except SessionPasswordNeeded:
            _auth_emit({
                "stage": "need_2fa",
                "next_action": "provide_password",
                "message": "This account has a cloud password (Two-Step Verification). "
                           "Ask the user for it and provide it via --password-file or stdin.",
            })
            pw = await _read_secret(password_file)
            if not pw:
                _auth_emit({"stage": "error", "reason": "timeout_2fa",
                            "message": "No 2FA password was provided in time."})
                return
            await app.check_password(pw)
        except PhoneCodeInvalid:
            _auth_emit({"stage": "error", "reason": "code_invalid",
                        "message": "The login code was wrong. Re-run auth to get a new code."})
            return
        except PhoneCodeExpired:
            _auth_emit({"stage": "error", "reason": "code_expired",
                        "message": "The login code expired. Re-run auth to get a new code."})
            return

        me = await app.get_me()
    finally:
        try:
            await app.disconnect()
        except Exception:
            pass

    # Login verified (get_me succeeded). If we logged into a scratch session,
    # back up the current live one and atomically swap the new session in.
    backup = None
    if work != session_name:
        backup = backup_session(session_name)
        try:
            os.replace(f"{work}.session", f"{session_name}.session")
        except OSError as e:
            _auth_emit({"stage": "error", "reason": "swap_failed",
                        "message": f"Logged in but could not install the new session: {e}. "
                                   f"New session left at {work}.session"})
            return

    if remember_phone:
        _save_phone_to_config(config_file, phone)

    save_last_good(session_name, user_id=me.id, username=me.username, backend="pyrogram")

    result = {
        "stage": "authorized",
        "user": me.username or str(me.id),
        "user_id": me.id,
        "session_file": f"{session_name}.session",
        "message": "Done — the account is authorized and the skill can read channels. "
                   "The session is stored locally on this machine (OpenClaw); nothing "
                   "was uploaded.",
    }
    if backup:
        result["previous_session_backup"] = backup
    if moved:
        result["dead_session_moved_to"] = moved
    _auth_emit(result)


# ── Session restore ──────────────────────────────────────────────────────────

async def _verify_authorized(session_name, api_id, api_hash):
    """Connect non-interactively and return the authorized user."""
    async with _authorized_client(session_name, api_id, api_hash) as (app, me):
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
        prog="tg-reader",
        description="Read Telegram channel posts for OpenClaw agent"
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

    # info
    info_p = sub.add_parser("info", help="Get channel title, description and subscriber count")
    info_p.add_argument("channel", help="Channel username e.g. @durov")

    # auth
    auth_p = sub.add_parser("auth", help="Authenticate with Telegram (agent-drivable onboarding)")
    auth_p.add_argument("--phone", default=None,
                        help="Reader account phone, international format (+79991234567)")
    auth_p.add_argument("--code-file", default=None,
                        help="File the login code is read from (polled). Omit to read stdin.")
    auth_p.add_argument("--password-file", default=None,
                        help="File the 2FA cloud password is read from (polled). Omit to read stdin.")
    auth_p.add_argument("--remember-phone", action="store_true",
                        help="Save the phone into the config for future re-auths")
    auth_p.add_argument("--force", action="store_true",
                        help="Re-login even if the session is already authorized")
    auth_p.add_argument("--guide", action="store_true",
                        help="Print step-by-step instructions for the user to self-authorize, then exit")

    # restore-session
    sub.add_parser("restore-session",
                   help="Restore the last-known-good session backup and verify it")

    args = parser.parse_args()
    cf = args.config_file
    sf = args.session_file

    # --guide only prints instructions for the human — no session, no lock.
    if args.cmd == "auth" and getattr(args, "guide", False):
        auth_guide(cf, sf)
        return

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
    if args.cmd == "info":
        result = asyncio.run(fetch_info(args.channel, cf, sf))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "auth":
        asyncio.run(setup_auth(
            cf, sf,
            phone=args.phone,
            code_file=args.code_file,
            password_file=args.password_file,
            remember_phone=args.remember_phone,
            force=args.force,
        ))
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
            result = asyncio.run(fetch_messages(
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
