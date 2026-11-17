#!/usr/bin/env python3
"""
Space Duck — local Telegram getUpdates poller for Lane A ducks.

INTENT: Lane A doctrine (Josh ruling 2026-07-16) forbids platform-held
        webhooks for BYOB ducks, so DMs to the duck's bot are fetched by
        the duck's own runtime via long-poll getUpdates and handed to the
        already-running telegram_listener.py on localhost, using the exact
        HMAC-signed forward format the platform would have sent (v537+).
        This reuses the listener's verify/dedup/owner-approval/brain stack
        unchanged — the poller is transport only, it never touches brains.

TRANSPORT EXCLUSIVITY: getUpdates and webhooks are mutually exclusive on
        the Telegram side. On startup the poller refuses to run if the bot
        has a webhook registered (that would mean the platform, or someone,
        holds delivery — resolve that first; never silently deleteWebhook).

AUTH:   Bot token from the env var named by --token-env (systemd
        EnvironmentFile keeps it out of argv). beak_key + spaceduck_id from
        ~/.space-duck/config.json — HOME-scoped like every other rail.

Usage:
  DAVID_TG_BOT_TOKEN=... python3 telegram_poll.py --port 8790 \
      --token-env DAVID_TG_BOT_TOKEN
"""
import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

CONFIG = Path.home() / '.space-duck' / 'config.json'
OFFSET_FILE = Path.home() / '.space-duck' / 'tg_poll_offset.txt'


def log(msg):
    print(f'[TG-POLL] {msg}', flush=True)


def tg_call(token, method, params=None, timeout=60):
    data = json.dumps(params or {}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/{method}',
        data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=timeout) as r:
        resp = json.load(r)
    if not resp.get('ok'):
        raise RuntimeError(f'{method}: {resp}')
    return resp['result']


def forward(port, beak_key, payload_bytes, ts, nonce):
    # Mirrors lambda_function.py forward signing: secret is domain-separated
    # from beak_key; canonical bytes are f'{ts}.{nonce}.' + raw body.
    secret = hmac.new(beak_key.encode(), b'byob-hmac-v1', hashlib.sha256).digest()
    sig = hmac.new(secret, f'{ts}.{nonce}.'.encode() + payload_bytes,
                   hashlib.sha256).hexdigest()
    req = urllib.request.Request(
        f'http://127.0.0.1:{port}/beak/telegram/forward',
        data=payload_bytes, method='POST',
        headers={'Content-Type': 'application/json',
                 'X-SpaceDuck-Event': 'telegram.message',
                 'X-SpaceDuck-Timestamp': str(ts),
                 'X-SpaceDuck-Nonce': nonce,
                 'X-SpaceDuck-Idempotency-Key': nonce,
                 'X-SpaceDuck-Signature': f'sha256={sig}',
                 'X-SpaceDuck-Binding-State': 'VERIFIED'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return r.status


def main():
    ap = argparse.ArgumentParser(description='Local Telegram poller (Lane A)')
    ap.add_argument('--port', type=int, default=8788,
                    help='local telegram_listener.py port')
    ap.add_argument('--token-env', default='TG_BOT_TOKEN',
                    help='env var holding the bot token')
    args = ap.parse_args()

    token = os.environ.get(args.token_env, '').strip()
    if not token:
        log(f'FATAL: env {args.token_env} empty'); sys.exit(1)
    try:
        cfg = json.loads(CONFIG.read_text())
    except OSError:
        log(f'FATAL: {CONFIG} missing — run pair.py first'); sys.exit(1)
    beak_key, sd_id = cfg.get('beak_key', ''), cfg.get('spaceduck_id', '')
    if not beak_key or not sd_id:
        log('FATAL: config lacks beak_key/spaceduck_id'); sys.exit(1)

    me = tg_call(token, 'getMe')
    wh = tg_call(token, 'getWebhookInfo')
    if wh.get('url'):
        log(f"FATAL: webhook registered ({wh['url']}) — transport exclusivity; "
            'resolve who holds delivery before polling'); sys.exit(2)
    token_hash = hashlib.md5(token.encode()).hexdigest()
    log(f"polling as @{me.get('username')} → 127.0.0.1:{args.port} sd={sd_id[:8]}")

    offset = 0
    try:
        offset = int(OFFSET_FILE.read_text().strip())
    except (OSError, ValueError):
        pass

    while True:
        try:
            updates = tg_call(token, 'getUpdates',
                              {'offset': offset, 'timeout': 50,
                               'allowed_updates': ['message']}, timeout=60)
        except Exception as e:
            log(f'getUpdates error: {e} — retry in 5s'); time.sleep(5); continue
        for u in updates:
            ts, nonce = int(time.time()), os.urandom(16).hex()
            payload = json.dumps({
                'event': 'telegram.message', 'telegram_update': u,
                'spaceduck_id': sd_id, 'token_hash': token_hash,
                'timestamp': ts, 'idempotency_key': f"upd{u['update_id']}",
                'nonce': nonce}).encode()
            try:
                st = forward(args.port, beak_key, payload, ts, nonce)
                log(f"update {u['update_id']} → listener HTTP {st}")
            except Exception as e:
                log(f"forward of update {u['update_id']} failed: {e} — retry in 5s")
                time.sleep(5)
                break  # do not advance offset; re-fetch this update
            offset = u['update_id'] + 1
            try:
                OFFSET_FILE.write_text(str(offset))
            except OSError as e:
                log(f'offset persist failed: {e}')


if __name__ == '__main__':
    main()
