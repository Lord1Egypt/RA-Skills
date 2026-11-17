"""tgwidget: check, render, send and update Telegram HTML widgets.

    tgwidget check widget.html [--chat-data JSON|@file] [--public-data ...]
    tgwidget render widget.html --out shot.png [--scheme dark] [--width 320]
    tgwidget send widget.html --chat-id ID --caption TEXT [--chat-data ...]
    tgwidget edit --chat-id ID --message-id N [--chat-data ...] [--caption TEXT]

Every command prints one JSON object. Exit codes: 0 ok, 1 refused or failed,
2 bad usage.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from . import __version__
from .check import check_html, check_state
from .report import Report
from .target import TargetError, resolve
from .telegram import TOKEN_ENV_VARS, BotApi, TelegramError, redact, token_from_env
from .urls import ENV_VAR as ALLOWLIST_ENV, load_allowlist, scan_text

MAX_CAPTION = 1024


def _out(obj: Dict[str, Any], token: Optional[str] = None) -> None:
    text = json.dumps(obj, ensure_ascii=False, indent=2)
    print(redact(text, token if token is not None else token_from_env()))


def _read_value(value: Optional[str]) -> Optional[str]:
    """A literal string, or @path to read it from a file (@- for stdin)."""
    if value is None:
        return None
    if value.startswith("@"):
        path = value[1:]
        if path == "-":
            return sys.stdin.read()
        with open(path, encoding="utf-8") as f:
            return f.read().rstrip("\n")
    return value


def _read_html(path: str) -> bytes:
    if path == "-":
        return sys.stdin.buffer.read()
    with open(path, "rb") as f:
        return f.read()


def _allowlist(args):
    # Operator configuration only (the environment the agent framework runs in). There is
    # deliberately no command-line flag: the model writes the command line.
    try:
        return load_allowlist()
    except ValueError as e:
        raise SystemExit(_usage_error("bad %s: %s" % (ALLOWLIST_ENV, e)))


def _usage_error(message: str) -> int:
    _out({"ok": False, "errors": [{"rule": "usage", "message": message}]})
    return 2


def _full_check(args, html: bytes) -> Report:
    allow = _allowlist(args)
    report = check_html(html, allow)
    check_state("chat_data", _read_value(getattr(args, "chat_data", None)), allow, report)
    check_state("public_data", _read_value(getattr(args, "public_data", None)), allow, report)
    report.stats["link_allowlist"] = [
        ("*." if e.wildcard else "") + e.host + e.path for e in allow
    ]
    return report


def cmd_check(args) -> int:
    report = _full_check(args, _read_html(args.file))
    result = report.to_dict()
    if args.text:
        lines = ["OK" if report.ok else "REFUSED"]
        for kind in ("errors", "warnings"):
            for i in result[kind]:
                lines.append("%s %s%s: %s" % (kind[:-1].upper(), i["rule"],
                                               " (line %d)" % i["line"] if "line" in i else "", i["message"]))
        s = result["stats"]
        lines.append("size: %s bytes, %s compressed of %s" % (s.get("bytes"), s.get("compressed_bytes"),
                                                             s.get("compressed_limit")))
        print("\n".join(lines))
    else:
        _out(result)
    return 0 if report.ok else 1


def cmd_render(args) -> int:
    from .render import render

    html = _read_html(args.file).decode("utf-8", errors="replace")
    result = render(html, args.out, width=args.width, scheme=args.scheme,
                    chat_data=_read_value(args.chat_data), public_data=_read_value(args.public_data))
    _out(result)
    return 0 if result.get("ok") else 1


def _caption_problems(caption: str, allow) -> List[Dict[str, str]]:
    problems = []
    if len(caption) > MAX_CAPTION:
        problems.append({"rule": "caption", "message": "caption is %d characters (limit %d)"
                                                       % (len(caption), MAX_CAPTION)})
    for url, why in scan_text(caption, allow):
        problems.append({"rule": "link-not-allowed", "message": "caption mentions %r: %s" % (url[:80], why)})
    return problems


def _need_token():
    token = token_from_env()
    if not token:
        raise SystemExit(_usage_error("no bot token: set %s (or %s)" % TOKEN_ENV_VARS))
    return token


def _bot_api(token: str, test_env: bool) -> BotApi:
    try:
        return BotApi(token, test_env=test_env)
    except ValueError as e:
        raise SystemExit(_usage_error(str(e)))


PRIVATE_ONLY = ("in production, widgets live only in a private chat with a user (a positive numeric "
                "chat id); groups, channels and @usernames are refused")


def cmd_send(args) -> int:
    try:
        target = resolve(args.chat_id, args.thread_id)
    except TargetError as e:
        return _usage_error(str(e))
    caption = (_read_value(args.caption) or "").strip()
    if not caption:
        return _usage_error("--caption is required: it is the chat-list text and what apps without widget "
                            "support show instead of the widget")
    if not args.test_env and not target.is_private:
        return _usage_error(PRIVATE_ONLY)

    html = _read_html(args.file)
    report = _full_check(args, html)
    allow = _allowlist(args)
    for p in _caption_problems(caption, allow):
        report.add(p["rule"], p["message"])
    if report.stats.get("uses_requests") and not args.allow_queries:
        report.warn("js-requests", "sent without --allow-queries: every request() is rejected with NOT_ALLOWED")
    if not report.ok:
        result = report.to_dict()
        result["sent"] = False
        _out(result)
        return 1

    payload = {
        "chat_id": target.api_chat_id(),
        "html": html.decode("utf-8"),
        "caption": caption,
        "chat_data": _read_value(args.chat_data),
        "public_data": _read_value(args.public_data),
        "width": args.width,
        "height": args.height,
        "show_caption_above_media": True if args.caption_above else None,
        "allow_queries": True if args.allow_queries else None,
        "disable_notification": True if args.silent else None,
        "reply_parameters": {"message_id": args.reply_to} if args.reply_to else None,
        "message_thread_id": target.thread_id,
    }
    if args.dry_run:
        result = report.to_dict()
        result.update({"sent": False, "dry_run": True,
                       "would_send": {k: v for k, v in payload.items() if v is not None and k != "html"}})
        _out(result)
        return 0

    token = _need_token()
    try:
        msg = _bot_api(token, args.test_env).call("sendWidget", payload)
    except TelegramError as e:
        _out({"ok": False, "sent": False, "telegram_error": e.to_dict(), "warnings": report.to_dict()["warnings"]},
             token)
        return 1
    _out({
        "ok": True, "sent": True,
        "chat_id": (msg.get("chat") or {}).get("id"), "message_id": msg.get("message_id"),
        "compressed_bytes": report.stats.get("compressed_bytes"),
        "warnings": report.to_dict()["warnings"],
    }, token)
    return 0


def cmd_edit(args) -> int:
    try:
        target = resolve(args.chat_id)
    except TargetError as e:
        return _usage_error(str(e))
    if not args.test_env and not target.is_private:
        return _usage_error(PRIVATE_ONLY)
    if not args.message_id:
        return _usage_error("--message-id is required (from the output of send)")
    chat_data = _read_value(args.chat_data)
    public_data = _read_value(args.public_data)
    caption = _read_value(args.caption)
    if chat_data is None and public_data is None and caption is None:
        return _usage_error("nothing to change: pass --chat-data, --public-data and/or --caption")
    allow = _allowlist(args)
    report = Report()
    check_state("chat_data", chat_data, allow, report)
    check_state("public_data", public_data, allow, report)
    if caption is not None:
        for p in _caption_problems(caption, allow):
            report.add(p["rule"], p["message"])
    if not report.ok:
        result = report.to_dict()
        result["edited"] = False
        _out(result)
        return 1

    token = _need_token()
    api = _bot_api(token, args.test_env)
    target = {"chat_id": target.api_chat_id(), "message_id": args.message_id}
    done = []
    try:
        if chat_data is not None or public_data is not None:
            try:
                api.call("editMessageWidgetData", dict(target, chat_data=chat_data, public_data=public_data))
                done.append("state")
            except TelegramError as e:
                if "not modified" not in e.description:
                    raise
                done.append("state (unchanged)")
        if caption is not None:
            try:
                api.call("editMessageCaption", dict(target, caption=caption))
                done.append("caption")
            except TelegramError as e:
                if "not modified" not in e.description:
                    raise
                done.append("caption (unchanged)")
    except TelegramError as e:
        _out({"ok": False, "edited": done, "telegram_error": e.to_dict()}, token)
        return 1
    _out({"ok": True, "edited": done, "chat_id": target["chat_id"], "message_id": args.message_id}, token)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="tgwidget", description="Check, render and send Telegram HTML widgets.")
    p.add_argument("--version", action="version", version="tgwidget " + __version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def state_args(sp):
        sp.add_argument("--chat-data", help="chat state: a string (often JSON) or @file")
        sp.add_argument("--public-data", help="shared state: a string (often JSON) or @file")

    c = sub.add_parser("check", help="check a widget before sending it")
    c.add_argument("file", help="widget HTML file, or - for stdin")
    state_args(c)
    c.add_argument("--text", action="store_true", help="human-readable output instead of JSON")
    c.set_defaults(func=cmd_check)

    r = sub.add_parser("render", help="run the widget in headless Chromium and take a screenshot")
    r.add_argument("file")
    r.add_argument("--out", help="screenshot PNG path")
    r.add_argument("--width", type=int, default=320, help="bubble width in px (default 320)")
    r.add_argument("--scheme", choices=("light", "dark"), default="light")
    r.add_argument("--chat-data")
    r.add_argument("--public-data")
    r.set_defaults(func=cmd_render)

    s = sub.add_parser("send", help="check, then send with sendWidget")
    s.add_argument("file")
    s.add_argument("--chat-id", help="the private chat with the user: a number or telegram:<id> "
                                     "(Hermes: defaults to the current conversation)")
    s.add_argument("--caption", help="required: text shown in the chat list and by apps without widgets")
    state_args(s)
    s.add_argument("--width", type=int, help="width anchor in px (omit: full bubble width)")
    s.add_argument("--height", type=int, help="height anchor in px (omit: content height)")
    s.add_argument("--caption-above", action="store_true", help="show the caption above the widget")
    s.add_argument("--allow-queries", action="store_true",
                   help="let the widget send requests (only useful if the bot answers widget_query updates)")
    s.add_argument("--silent", action="store_true", help="send without notification sound")
    s.add_argument("--reply-to", type=int, help="message id to reply to")
    s.add_argument("--thread-id", type=int, help="message_thread_id for topics")
    s.add_argument("--test-env", action="store_true", help="use Telegram's test environment")
    s.add_argument("--dry-run", action="store_true", help="check and show what would be sent")
    s.set_defaults(func=cmd_send)

    e = sub.add_parser("edit", help="change a sent widget's state and/or caption")
    e.add_argument("--chat-id", help="as for send")
    e.add_argument("--message-id", type=int)
    e.add_argument("--caption", help="new caption (or @file)")
    state_args(e)
    e.add_argument("--test-env", action="store_true")
    e.set_defaults(func=cmd_edit)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 1
    except OSError as e:
        return _usage_error("%s: %s" % (type(e).__name__, getattr(e, "strerror", None) or "cannot read input"))
