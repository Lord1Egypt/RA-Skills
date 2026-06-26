#!/usr/bin/env python3
"""
Space Duck — Send a Telegram message via your platform-held bot (δ-lite).

INTENT: Owner-side wrapper around `POST /beak/telegram/send-as`. The platform
        holds your bot's encrypted token; this script asks it to send a
        message on your behalf, audited and beak_key-gated. Closes the
        BYOB Telegram outbound loop introduced in lambda v539.

CALLS:  POST https://beak.spaceduckling.com/beak/telegram/send-as
AUTH:   x-beak-key header from ~/.space-duck/config.json (the duck's
        per-agent Beak Key, written by pair.py).

Usage:
  # Manual one-off send
  python3 tg_send.py --spaceduck-id <SD> --chat-id <CHAT> --text "hello"

  # Threaded reply (useful inside telegram_listener.py auto-reply hook)
  python3 tg_send.py --spaceduck-id <SD> --chat-id <CHAT> \
      --text "reply text" --reply-to <MESSAGE_ID>

  # Pipe text in (so the listener can `cmd | tg_send.py …`)
  echo "hello via stdin" | python3 tg_send.py --spaceduck-id <SD> --chat-id <CHAT>

  # Markdown / HTML
  python3 tg_send.py --spaceduck-id <SD> --chat-id <CHAT> \
      --text "*bold* _italic_" --parse-mode Markdown

  # Importable
  from tg_send import send_as
  res = send_as(spaceduck_id, chat_id, text, beak_key=..., reply_to=...)

Exit codes:
  0 — Telegram accepted the message (returns JSON: {ok, message_id, ...})
  1 — Local error (missing args, config not found, etc.)
  2 — Auth error (403 from platform)
  3 — Telegram-side error (502 from platform with tg_error / tg_status)
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_API = os.environ.get('SPACE_DUCK_API', 'https://beak.spaceduckling.com')
CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'


def _load_config():
    """Return (beak_key, default_spaceduck_id) from ~/.space-duck/config.json
    or raise FileNotFoundError. spaceduck_id may be empty if multi-duck."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f'Config not found at {CONFIG_PATH}. Run `python3 pair.py` first.')
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    return cfg.get('beak_key', ''), cfg.get('spaceduck_id', '')


def send_as(spaceduck_id, chat_id, text, *, beak_key=None,
            reply_to=None, parse_mode=None, disable_preview=False,
            idempotency_key=None, reply_markup=None,
            api_base=DEFAULT_API):
    """Send a message via /beak/telegram/send-as.

    Returns (status_code, response_dict). 200 means Telegram accepted.

    `reply_markup` (0.3.6+): dict per Telegram's sendMessage API, e.g.
    {'inline_keyboard': [[{'text': 'Approve', 'callback_data': '…'}]]}.
    The platform passes it through unchanged to Telegram.
    """
    if beak_key is None:
        beak_key, _ = _load_config()
    if not beak_key:
        raise ValueError('No beak_key (pass beak_key= or run pair.py)')
    if not spaceduck_id or chat_id in (None, '') or not text:
        raise ValueError('spaceduck_id, chat_id, text are all required')

    body = {
        'spaceduck_id': spaceduck_id,
        'chat_id': chat_id,
        'text': text,
    }
    if parse_mode:
        body['parse_mode'] = parse_mode
    if reply_to:
        body['reply_to_message_id'] = int(reply_to)
    if disable_preview:
        body['disable_web_page_preview'] = True
    if idempotency_key:
        body['idempotency_key'] = idempotency_key
    if isinstance(reply_markup, dict):
        body['reply_markup'] = reply_markup

    req = urllib.request.Request(
        api_base.rstrip('/') + '/beak/telegram/send-as',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'x-beak-key': beak_key},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as he:
        try:
            err_body = json.loads(he.read())
        except Exception:
            err_body = {'error': 'http_error', 'detail': str(he)[:200]}
        return he.code, err_body


def answer_callback(spaceduck_id, callback_query_id, *, text='',
                    show_alert=False, beak_key=None, api_base=DEFAULT_API):
    """0.3.7 — wraps Telegram's answerCallbackQuery via Lambda's
    /beak/telegram/answer-callback endpoint (v677+).

    Use after the listener claims a pending sda:* callback so the
    Telegram client closes the grey spinner immediately instead of
    hanging until its 10s timeout.

    Returns (status, dict). 200 = Telegram accepted.
    """
    if beak_key is None:
        beak_key, _ = _load_config()
    if not beak_key:
        raise ValueError('No beak_key (pass beak_key= or run pair.py)')
    if not spaceduck_id or not callback_query_id:
        raise ValueError('spaceduck_id and callback_query_id required')
    body = {
        'spaceduck_id': spaceduck_id,
        'callback_query_id': callback_query_id,
        'text': (text or '')[:200],
        'show_alert': bool(show_alert),
    }
    req = urllib.request.Request(
        api_base.rstrip('/') + '/beak/telegram/answer-callback',
        data=json.dumps(body).encode(),
        headers={'Content-Type': 'application/json', 'x-beak-key': beak_key},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as he:
        try:
            return he.code, json.loads(he.read())
        except Exception:
            return he.code, {'error': 'http_error', 'detail': str(he)[:200]}


def _chat_id_arg(raw):
    # Telegram chat IDs are integers; channel/group usernames look like '@foo'.
    # Accept both transparently.
    raw = str(raw).strip()
    if raw.startswith('@'):
        return raw
    try:
        return int(raw)
    except ValueError:
        return raw


def main(argv=None):
    p = argparse.ArgumentParser(description='Send a Telegram message via your Space Duck bot.')
    p.add_argument('--spaceduck-id', help='Spaceduck ID (defaults to config.json value)')
    p.add_argument('--chat-id', required=True, help='Telegram chat ID (int) or @channelusername')
    p.add_argument('--text', help='Message body. If omitted, reads from stdin.')
    p.add_argument('--reply-to', type=int, help='reply_to_message_id for threaded reply')
    p.add_argument('--parse-mode', choices=['Markdown', 'MarkdownV2', 'HTML'],
                   help='Telegram parse_mode')
    p.add_argument('--disable-preview', action='store_true',
                   help='Disable URL preview')
    p.add_argument('--idempotency-key', help='Stable key for dedup audit (auto if absent)')
    p.add_argument('--api', default=DEFAULT_API, help='Override API base (advanced)')
    args = p.parse_args(argv)

    try:
        beak_key, default_sd = _load_config()
    except FileNotFoundError as e:
        print(f'ERR: {e}', file=sys.stderr)
        return 1
    sd_id = args.spaceduck_id or default_sd
    if not sd_id:
        print('ERR: --spaceduck-id required (no default in config)', file=sys.stderr)
        return 1

    text = args.text
    if text is None:
        text = sys.stdin.read().rstrip('\n')
    if not text:
        print('ERR: text empty (pass --text or pipe via stdin)', file=sys.stderr)
        return 1

    chat_id = _chat_id_arg(args.chat_id)

    try:
        status, resp = send_as(
            sd_id, chat_id, text,
            beak_key=beak_key,
            reply_to=args.reply_to,
            parse_mode=args.parse_mode,
            disable_preview=args.disable_preview,
            idempotency_key=args.idempotency_key,
            api_base=args.api,
        )
    except Exception as e:
        print(f'ERR: {e}', file=sys.stderr)
        return 1

    print(json.dumps(resp))
    if status == 200:
        return 0
    if status == 403:
        return 2
    return 3


if __name__ == '__main__':
    sys.exit(main())
