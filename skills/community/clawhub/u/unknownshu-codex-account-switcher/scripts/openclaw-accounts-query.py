#!/usr/bin/env python3
"""Fast local account/status query for OpenClaw NapCat commands.

Reads local auth profile metadata and prints a short Chinese summary. It never
prints access tokens, refresh tokens, API keys, or credential file contents.
"""
import json
import os
import sys
import time
import subprocess
import tempfile
import urllib.request
from pathlib import Path
import fcntl

OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
OPENCLAW_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
OPENCLAW_AGENT_DIR = Path(os.environ.get("OPENCLAW_AGENT_DIR", str(OPENCLAW_HOME / "agents" / OPENCLAW_AGENT_ID / "agent")))
STATE_PATH = Path(os.environ.get("OPENCLAW_AUTH_STATE", str(OPENCLAW_AGENT_DIR / "auth-state.json")))
PROFILES_PATH = Path(os.environ.get("OPENCLAW_AUTH_PROFILES", str(OPENCLAW_AGENT_DIR / "auth-profiles.json")))
QUOTA_SCRIPT = Path(os.environ.get("OPENCLAW_QUOTA_SCRIPT", str(Path(__file__).resolve().with_name("openai-codex-quota-query.py"))))
DEFAULT_MODEL = os.environ.get("OPENCLAW_DEFAULT_MODEL", "openai-codex/gpt-5.5")
FALLBACK_MODEL = os.environ.get("OPENCLAW_FALLBACK_MODEL", "cch/gpt-5.4")
PROVIDER = "openai-codex"
LOCK_PATH = Path(os.environ.get("OPENCLAW_ACCOUNT_QUERY_LOCK", "/tmp/openclaw-account-query.lock"))
WHAM_URL = "https://chatgpt.com/backend-api/wham/usage"


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


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


def bar(percent, width=10):
    try:
        value = max(0.0, min(100.0, float(percent)))
    except Exception:
        value = 0.0
    filled = int(round(value / 100.0 * width))
    return "█" * filled + "░" * (width - filled)


def fmt_expiry(ms):
    try:
        ts = float(ms) / 1000.0
    except Exception:
        return "未知"
    delta = int(ts - time.time())
    if delta <= 0:
        return "已过期"
    days = delta // 86400
    hours = (delta % 86400) // 3600
    if days:
        return f"{days}d 后过期"
    return f"{hours}h 后过期"


def fmt_cooldown(stat):
    try:
        until = float(stat.get("cooldownUntil") or 0) / 1000.0
    except Exception:
        return ""
    if until <= time.time():
        return ""
    reason = stat.get("cooldownReason") or "cooldown"
    if until > 4102444700:  # 2100-ish permanent marker used by auth-state
        return f"cooldown({reason})"
    delta = int(until - time.time())
    mins = max(1, delta // 60)
    return f"cooldown({reason}, 约{mins}m)"


def active_profile_id(state, profile_ids):
    order = (state.get("order") or {}).get(PROVIDER)
    if isinstance(order, list):
        for pid in order:
            if pid in profile_ids:
                return pid
    last = (state.get("lastGood") or {}).get(PROVIDER)
    if last in profile_ids:
        return last
    return profile_ids[0] if profile_ids else ""


def fmt_duration(seconds):
    try:
        seconds = int(float(seconds))
    except Exception:
        return ""
    days, rem = divmod(max(0, seconds), 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"约 {days}d{hours}h"
    if hours:
        return f"约 {hours}h{minutes:02d}m"
    return f"约 {minutes}m"


def set_order_in_state(state, first, profile_ids):
    state.setdefault("version", 1)
    state.setdefault("order", {})
    state["order"][PROVIDER] = [first] + [pid for pid in profile_ids if pid != first]
    atomic_write_json(STATE_PATH, state)


def restore_order(original_state):
    atomic_write_json(STATE_PATH, original_state)



def quota_result_direct(profile_id, cred, timeout=12):
    access = cred.get("access")
    if not access:
        return {"profileId": profile_id, "ok": False, "error": "missing_access"}
    headers = {
        "Authorization": "Bearer " + access,
        "Accept": "application/json",
        "User-Agent": "OpenClawAccountsQuery",
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
    for key, label in (("primary_window", "5小时额度"), ("secondary_window", "本周额度")):
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


def probe_all_codex_direct(codex):
    return {pid: quota_result_direct(pid, cred) for pid, cred in codex}

def quota_result_via_active_profile(profile_id, profile_ids):
    state = load_json(STATE_PATH, {"version": 1})
    set_order_in_state(state, profile_id, profile_ids)
    try:
        out = subprocess.check_output([str(QUOTA_SCRIPT), "--json"], text=True, timeout=12)
        result = json.loads(out)
        if not result.get("ok"):
            return {"ok": False, "error": result.get("error", "quota_failed")}
        return result
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "Timeout"}
    except Exception as exc:
        return {"ok": False, "error": type(exc).__name__}


def probe_all_codex_by_switching(codex, original_state):
    results = {}
    profile_ids = [pid for pid, _ in codex]
    if not profile_ids:
        return results
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("w", encoding="utf-8") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            # Use the exact same quota script path as /额度查询. This temporarily
            # changes auth order per account, then restores the starting state.
            for pid in profile_ids:
                results[pid] = quota_result_via_active_profile(pid, profile_ids)
        finally:
            restore_order(original_state)
            fcntl.flock(lock_file, fcntl.LOCK_UN)
    return results


def fmt_usage_line(result):
    if not result or not result.get("ok"):
        return f"额度未知({(result or {}).get('error', 'unknown')})"
    parts = []
    labels = [("primary_window", "5h"), ("secondary_window", "Week")]
    for key, label in labels:
        w = (result.get("windows") or {}).get(key)
        if not w:
            continue
        remaining = float(w.get("remaining") or 0)
        reset = fmt_duration(w.get("reset_after_seconds"))
        parts.append(f"{label} {bar(remaining, 8)} {remaining:.0f}%" + (f"/{reset}" if reset else ""))
    if result.get("limitReached"):
        parts.append("已限流")
    return " · ".join(parts) if parts else "额度未知"


def main():
    store = load_json(PROFILES_PATH, {"profiles": {}})
    state = load_json(STATE_PATH, {})
    original_state = json.loads(json.dumps(state, ensure_ascii=False)) if isinstance(state, dict) else {}
    profiles = store.get("profiles") or {}
    stats = state.get("usageStats") or {}

    codex = []
    for pid, cred in profiles.items():
        if cred.get("provider") == PROVIDER and cred.get("type") == "oauth":
            codex.append((pid, cred))
    codex.sort(key=lambda item: item[0])
    active = active_profile_id(state, [pid for pid, _ in codex])
    usage = probe_all_codex_direct(codex)

    lines = ["账号状态：", f"默认模型：{DEFAULT_MODEL}", f"备用模型：{FALLBACK_MODEL}"]

    lines.append("")
    lines.append("Codex 账号与额度：")
    if codex:
        lines.append("（直接按各账号 OAuth 查询，不切换当前账号）")
    if not codex:
        lines.append("- 未找到 openai-codex OAuth 账号")
    else:
        for pid, cred in codex:
            email = cred.get("email") or pid.split(":", 1)[-1]
            expiry = fmt_expiry(cred.get("expires"))
            cd = fmt_cooldown(stats.get(pid) or {})
            marker = "⭐ " if pid == active else ""
            status = "✅" if expiry != "已过期" and not cd.startswith("cooldown(auth") else "⚠️"
            extra = f"，{cd}" if cd else ""
            lines.append(f"- {marker}{email} {status} {expiry}{extra}")
            lines.append(f"  {fmt_usage_line(usage.get(pid))}")

    other = []
    for pid, cred in profiles.items():
        provider = cred.get("provider") or pid.split(":", 1)[0]
        if provider == PROVIDER:
            continue
        typ = cred.get("type") or "profile"
        other.append(f"{provider}({typ})")
    if other:
        lines.append("")
        lines.append("其他已配置：" + "、".join(sorted(set(other))))

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
