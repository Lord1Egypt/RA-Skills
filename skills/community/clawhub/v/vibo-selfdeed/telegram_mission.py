#!/usr/bin/env python3
"""telegram_mission.py — Telegram interface for vibo-selfdeed.

The mission stage (steps) is visible to the owner in Telegram:
  notify  — send a message (stage/status)
  ask     — ✅/❌ buttons and wait for the answer (fix confirmation)
  report  — final mission report

Tokens:
  TELEGRAM_MISSION_TOKEN — token of a DEDICATED mission bot (buttons; needs polling)
  TELEGRAM_BOT_TOKEN     — main bot token (notify only, no polling)
  TELEGRAM_MISSION_CHAT  — owner chat_id (number)

Without a token — local output (dry-run), mission works as before.

Usage:
  python3 telegram_mission.py notify "🔍 SCAN: found 3 issues"
  python3 telegram_mission.py ask "Apply fixes?" "Fix 1: divide by zero"
  python3 telegram_mission.py report "Task: ..." "Success: 100%"
  # ask returns 0 (yes) / 1 (no) / 2 (timeout/error)
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TOKEN = os.environ.get("TELEGRAM_MISSION_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT = os.environ.get("TELEGRAM_MISSION_CHAT", "")
API = "https://api.telegram.org/bot"


def _api(method: str, payload: dict) -> dict:
    if not TOKEN or not CHAT:
        print("⚠️ Telegram not configured (TELEGRAM_MISSION_TOKEN/CHAT unset) — "
              "mission data stays local.", file=sys.stderr)
        return {"ok": False, "error": "not configured"}
    print("⚠️ sending mission data to Telegram (external service).", file=sys.stderr)
    req = urllib.request.Request(
        f"{API}{TOKEN}/{method}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def _send(text: str, buttons: list[list[str]] | None = None) -> dict:
    payload = {"chat_id": CHAT, "text": text, "parse_mode": "HTML"}
    if buttons:
        payload["reply_markup"] = {
            "inline_keyboard": [[{"text": b, "callback_data": b} for b in row] for row in buttons]
        }
    return _api("sendMessage", payload)


def notify(text: str) -> int:
    if not TOKEN or not CHAT:
        print("⚠️ Telegram not configured (TELEGRAM_MISSION_TOKEN/CHAT unset) — mission data stays local.", file=sys.stderr)
        print(f"📨 [telegram off] {text}")
        return 0
    try:
        _send(text)
        print(f"📨 sent: {text[:80]}")
        return 0
    except Exception as e:
        print(f"❌ telegram: {e}")
        return 1


def ask(text: str, detail: str = "", timeout_s: int = 300) -> int:
    """✅/❌ buttons + wait for answer. 0=yes, 1=no, 2=no answer."""
    if not TOKEN or not CHAT:
        print("⚠️ Telegram not configured (TELEGRAM_MISSION_TOKEN/CHAT unset) — mission data stays local.", file=sys.stderr)
        print(f"❓ [telegram off] {text}")
        print(f"   {detail}")
        return 2
    try:
        msg = _send(text, [["✅ Apply", "❌ Reject"]])
        msg_id = msg["result"]["message_id"]
        # wait for callback (polling with offset)
        offset = 0
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            try:
                up = _api("getUpdates", {"offset": offset, "timeout": 25})
            except Exception:
                time.sleep(2)
                continue
            for u in up.get("result", []):
                offset = u["update_id"] + 1
                cb = u.get("callback_query") or {}
                if cb.get("message", {}).get("message_id") == msg_id:
                    data = cb.get("data", "")
                    ans = 0 if data.startswith("✅") else 1
                    try:
                        _api("answerCallbackQuery", {"callback_query_id": cb["id"]})
                    except Exception:
                        pass
                    print(f"🔘 answer: {data}")
                    return ans
            time.sleep(1)
        print("⏰ no answer within timeout")
        return 2
    except Exception as e:
        print(f"❌ telegram ask: {e}")
        return 2


def report(task: str, lines: list[str]) -> int:
    body = f"<b>🏁 MISSION REPORT</b>\n<b>Task:</b> {task}\n" + "\n".join(lines)
    return notify(body)


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "notify"
    if cmd == "notify":
        return notify(sys.argv[2] if len(sys.argv) > 2 else "")
    if cmd == "ask":
        text = sys.argv[2] if len(sys.argv) > 2 else "Confirmation?"
        detail = sys.argv[3] if len(sys.argv) > 3 else ""
        return ask(text, detail)
    if cmd == "report":
        task = sys.argv[2] if len(sys.argv) > 2 else ""
        lines = sys.argv[3:] if len(sys.argv) > 3 else []
        return report(task, lines)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
