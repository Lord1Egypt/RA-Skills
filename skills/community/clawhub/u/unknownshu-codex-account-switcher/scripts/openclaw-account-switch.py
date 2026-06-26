#!/usr/bin/env python3
"""Switch OpenClaw openai-codex auth profile order by email/profile id.

Safe for chat commands: never prints tokens/secrets. It only rewrites auth-state.json
so the selected OAuth profile is first in the openai-codex auth order.
"""
import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path

PROVIDER = "openai-codex"
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
OPENCLAW_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
OPENCLAW_AGENT_DIR = Path(os.environ.get("OPENCLAW_AGENT_DIR", str(OPENCLAW_HOME / "agents" / OPENCLAW_AGENT_ID / "agent")))
STATE_PATH = Path(os.environ.get("OPENCLAW_AUTH_STATE", str(OPENCLAW_AGENT_DIR / "auth-state.json")))
PROFILES_PATH = Path(os.environ.get("OPENCLAW_AUTH_PROFILES", str(OPENCLAW_AGENT_DIR / "auth-profiles.json")))


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default
    except Exception as exc:
        raise SystemExit(f"读取失败：{path}: {type(exc).__name__}")


def atomic_write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    finally:
        try:
            if os.path.exists(tmp):
                os.unlink(tmp)
        except Exception:
            pass


def codex_profiles():
    store = load_json(PROFILES_PATH, {"profiles": {}})
    profiles = []
    for pid, cred in (store.get("profiles") or {}).items():
        if cred.get("provider") != PROVIDER or cred.get("type") != "oauth":
            continue
        email = cred.get("email") or pid.split(":", 1)[-1]
        profiles.append({"id": pid, "email": email, "expires": cred.get("expires")})
    return sorted(profiles, key=lambda item: item["email"].lower())


def resolve_target(value, profiles):
    raw = str(value or "").strip()
    if not raw:
        return None
    raw_l = raw.lower()
    matches = []
    for profile in profiles:
        pid_l = profile["id"].lower()
        email_l = profile["email"].lower()
        if raw_l == pid_l or raw_l == email_l or raw_l == pid_l.split(":", 1)[-1]:
            return profile
        if raw_l in email_l or raw_l in pid_l:
            matches.append(profile)
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        emails = "、".join(p["email"] for p in matches)
        raise SystemExit(f"匹配到多个账号，请写完整邮箱：{emails}")
    return None


def fmt_expiry(ms):
    try:
        delta = int(float(ms) / 1000 - time.time())
    except Exception:
        return "过期时间未知"
    if delta <= 0:
        return "已过期"
    days = delta // 86400
    hours = (delta % 86400) // 3600
    if days:
        return f"{days}d 后过期"
    return f"{hours}h 后过期"


def cooldown_note(state, profile_id):
    stat = ((state.get("usageStats") or {}).get(profile_id) or {})
    until = stat.get("cooldownUntil")
    reason = stat.get("cooldownReason") or "cooldown"
    try:
        until_s = float(until) / 1000
    except Exception:
        return ""
    if until_s <= time.time():
        return ""
    if until_s > 4102444700:
        return f"注意：该账号当前处于长期 cooldown（{reason}），切过去后可能仍不会被使用。"
    mins = max(1, int((until_s - time.time()) // 60))
    return f"注意：该账号当前 cooldown（{reason}，约 {mins}m），到期前可能不会被使用。"


def current_first(state, profiles):
    ids = {p["id"] for p in profiles}
    order = (state.get("order") or {}).get(PROVIDER)
    if isinstance(order, list):
        for pid in order:
            if pid in ids:
                return pid
    last = (state.get("lastGood") or {}).get(PROVIDER)
    if last in ids:
        return last
    return profiles[0]["id"] if profiles else ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="目标 Codex 账号邮箱或 profile id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    profiles = codex_profiles()
    if not profiles:
        raise SystemExit("没有找到 openai-codex OAuth 账号。")
    target = resolve_target(args.target, profiles)
    if not target:
        known = "、".join(p["email"] for p in profiles)
        raise SystemExit(f"未找到账号：{args.target}\n可用账号：{known}")

    state = load_json(STATE_PATH, {"version": 1})
    state.setdefault("version", 1)
    state.setdefault("order", {})
    profile_ids = [p["id"] for p in profiles]
    previous = current_first(state, profiles)
    new_order = [target["id"]] + [pid for pid in profile_ids if pid != target["id"]]

    if not args.dry_run:
        state["order"][PROVIDER] = new_order
        atomic_write_json(STATE_PATH, state)

    prev_email = next((p["email"] for p in profiles if p["id"] == previous), previous or "未知")
    lines = []
    if args.dry_run:
        lines.append("账号切换预检查通过。")
    else:
        lines.append("账号切换完成。")
    lines.append(f"当前优先账号：{target['email']}（{fmt_expiry(target.get('expires'))}）")
    if previous and previous != target["id"]:
        lines.append(f"上一优先账号：{prev_email}")
    note = cooldown_note(state, target["id"])
    if note:
        lines.append(note)
    return print("\n".join(lines)) or 0


if __name__ == "__main__":
    raise SystemExit(main())
