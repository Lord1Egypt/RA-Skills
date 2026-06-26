#!/usr/bin/env python3
"""Fast local OpenAI Codex quota query for OpenClaw/NapCat commands.

Reads local OAuth profile metadata, calls ChatGPT WHAM usage directly, and prints
short human text. Never prints access/refresh tokens.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

PROVIDER = "openai-codex"
WHAM_URL = "https://chatgpt.com/backend-api/wham/usage"
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
OPENCLAW_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
OPENCLAW_AGENT_DIR = Path(os.environ.get("OPENCLAW_AGENT_DIR", str(OPENCLAW_HOME / "agents" / OPENCLAW_AGENT_ID / "agent")))
STATE_PATH = Path(os.environ.get("OPENCLAW_AUTH_STATE", str(OPENCLAW_AGENT_DIR / "auth-state.json")))
PROFILES_PATH = Path(os.environ.get("OPENCLAW_AUTH_PROFILES", str(OPENCLAW_AGENT_DIR / "auth-profiles.json")))
CURRENT_MODEL = os.environ.get("OPENCLAW_QUOTA_MODEL", "openai-codex/gpt-5.5")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def active_profile_id(state, profile_ids):
    order = (state.get("order") or {}).get(PROVIDER)
    if isinstance(order, list):
        for pid in order:
            if pid in profile_ids:
                return pid
    last = (state.get("lastGood") or {}).get(PROVIDER)
    if last in profile_ids:
        return last
    return profile_ids[0] if profile_ids else None


def probe_usage(profile_id, cred, timeout):
    access = cred.get("access")
    if not access:
        return {"profileId": profile_id, "ok": False, "error": "missing_access"}
    headers = {
        "Authorization": "Bearer " + access,
        "Accept": "application/json",
        "User-Agent": "CodexBar",
    }
    if cred.get("accountId"):
        headers["ChatGPT-Account-Id"] = str(cred["accountId"])
    req = urllib.request.Request(WHAM_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = json.load(res)
    except Exception as exc:
        return {"profileId": profile_id, "ok": False, "error": type(exc).__name__}

    rl = data.get("rate_limit") or {}
    windows = {}
    labels = {
        "primary_window": "5小时额度",
        "secondary_window": "本周额度",
    }
    for key, label in labels.items():
        w = rl.get(key)
        if isinstance(w, dict) and isinstance(w.get("used_percent"), (int, float)):
            used = max(0.0, min(100.0, float(w["used_percent"])))
            windows[key] = {
                "label": label,
                "used": used,
                "remaining": max(0.0, 100.0 - used),
                "reset_after_seconds": w.get("reset_after_seconds"),
                "reset_at": w.get("reset_at"),
            }
    if not windows:
        return {"profileId": profile_id, "ok": False, "error": "no_windows"}
    return {
        "profileId": profile_id,
        "ok": True,
        "email": cred.get("email") or profile_id.split(":", 1)[-1],
        "limitReached": bool(rl.get("limit_reached")),
        "windows": windows,
    }


def bar(percent, width=10):
    filled = int(round(max(0.0, min(100.0, percent)) / 100.0 * width))
    return "█" * filled + "░" * (width - filled)


def fmt_duration(seconds):
    try:
        seconds = int(float(seconds))
    except Exception:
        return ""
    if seconds < 0:
        seconds = 0
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"约 {days}d{hours}h"
    if hours:
        return f"约 {hours}h{minutes:02d}m"
    return f"约 {minutes}m"


def fmt_reset_at(epoch_seconds, now=None):
    try:
        ts = int(float(epoch_seconds))
    except Exception:
        return ""
    now = now or time.time()
    t = time.localtime(ts)
    n = time.localtime(now)
    if (t.tm_year, t.tm_yday) == (n.tm_year, n.tm_yday):
        return time.strftime("%H:%M", t)
    return time.strftime("%m-%d %H:%M", t)


def format_text(result, show_account=True, show_model=True):
    if not result.get("ok"):
        return f"额度查询失败：{result.get('error', 'unknown')}"
    lines = ["额度情况："]
    labels = {
        "primary_window": "5h ：",
        "secondary_window": "本周：",
    }
    reset_parts = []
    reset_labels = {
        "primary_window": "5h",
        "secondary_window": "本周",
    }
    for key in ("primary_window", "secondary_window"):
        w = (result.get("windows") or {}).get(key)
        if not w:
            continue
        remaining = w["remaining"]
        reset = fmt_duration(w.get("reset_after_seconds"))
        suffix = f"，{reset}" if reset else ""
        lines.append(f"{labels[key]}{bar(remaining)} {remaining:.0f}% 剩余{suffix}")
        reset_at = fmt_reset_at(w.get("reset_at"))
        if reset_at:
            reset_parts.append(f"{reset_labels[key]} {reset_at}")
    if reset_parts:
        lines.append(f"下次更新：{'，'.join(reset_parts)}")
    if show_model:
        lines.append(f"当前模型：{CURRENT_MODEL}")
    if result.get("email") and show_account:
        lines.append(f"账号：{result['email']}")
    if result.get("limitReached"):
        lines.append("当前账号已触发限流。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print raw safe JSON")
    parser.add_argument("--show-account", action="store_true", help="kept for compatibility; account is shown by default")
    parser.add_argument("--hide-account", action="store_true")
    parser.add_argument("--hide-model", action="store_true")
    parser.add_argument("--timeout", type=float, default=8.0)
    args = parser.parse_args()

    profiles_store = load_json(PROFILES_PATH)
    state = load_json(STATE_PATH) if STATE_PATH.exists() else {}
    profiles = {
        pid: cred for pid, cred in (profiles_store.get("profiles") or {}).items()
        if cred.get("provider") == PROVIDER and cred.get("type") == "oauth"
    }
    pid = active_profile_id(state, list(profiles.keys()))
    if not pid:
        result = {"ok": False, "error": "no_openai_codex_profile"}
    else:
        result = probe_usage(pid, profiles[pid], args.timeout)
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(format_text(result, show_account=not args.hide_account, show_model=not args.hide_model))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
