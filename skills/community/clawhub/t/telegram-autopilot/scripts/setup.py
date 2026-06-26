#!/usr/bin/env python3
"""Telegram Autopilot — Login Setup
Handles OTP code + 2FA password via file-based exchange.
"""

import argparse
import asyncio
import json
import os
import sys

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


async def main(args):
    session_path = os.path.join(args.workdir, args.session)
    code_file = os.path.join(args.workdir, "enter_code.txt")
    pw_file = os.path.join(args.workdir, "enter_password.txt")

    for f in (code_file, pw_file):
        if os.path.exists(f):
            os.remove(f)

    client = TelegramClient(session_path, args.api_id, args.api_hash)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"ALREADY_LOGGED_IN: {me.first_name} (@{me.username}) ID={me.id}", flush=True)
        await client.disconnect()
        return

    print("REQUESTING_CODE", flush=True)
    result = await client.send_code_request(args.phone)
    print("CODE_SENT", flush=True)

    code = await _poll_file(code_file, timeout=300)
    if not code:
        print("TIMEOUT_NO_CODE", flush=True)
        await client.disconnect()
        return

    print(f"GOT_CODE: {code}", flush=True)

    try:
        await client.sign_in(phone=args.phone, code=code, phone_code_hash=result.phone_code_hash)
        me = await client.get_me()
        print(f"SUCCESS: {me.first_name} (@{me.username}) ID={me.id}", flush=True)
    except SessionPasswordNeededError:
        print("2FA_REQUIRED", flush=True)
        if args.password:
            pw = args.password
        else:
            pw = await _poll_file(pw_file, timeout=300)
        if not pw:
            print("TIMEOUT_NO_PASSWORD", flush=True)
            await client.disconnect()
            return
        try:
            await client.sign_in(password=pw)
            me = await client.get_me()
            print(f"SUCCESS_2FA: {me.first_name} (@{me.username}) ID={me.id}", flush=True)
        except Exception as e:
            print(f"2FA_ERROR: {e}", flush=True)
    except Exception as e:
        print(f"SIGN_IN_ERROR: {e}", flush=True)

    await client.disconnect()


async def _poll_file(path, timeout=300, interval=0.2):
    for _ in range(int(timeout / interval)):
        if os.path.exists(path):
            with open(path) as f:
                val = f.read().strip()
            if val:
                return val
        await asyncio.sleep(interval)
    return None


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Telegram Autopilot Login")
    p.add_argument("--api-id", type=int, required=True)
    p.add_argument("--api-hash", required=True)
    p.add_argument("--phone", required=True)
    p.add_argument("--password", default=None, help="2FA password (optional, can also use file)")
    p.add_argument("--session", default="user", help="Session file name")
    p.add_argument("--workdir", default=".", help="Working directory for session and code files")
    args = p.parse_args()
    asyncio.run(main(args))
