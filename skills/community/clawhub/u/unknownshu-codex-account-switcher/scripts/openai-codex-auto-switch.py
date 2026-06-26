#!/usr/bin/env python3
"""Auto-switch OpenClaw openai-codex auth profile when 5h quota is low.

When the active account's 5h remaining quota is below the threshold, probe all
other Codex OAuth profiles, choose one whose 5h and weekly quota are both above
the sufficient threshold, switch auth order to it, and optionally notify a NapCat
QQ group. Never prints or sends tokens/secrets.
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PROVIDER = "openai-codex"
ACTIVE_5H_THRESHOLD = float(os.environ.get("OPENCLAW_CODEX_SWITCH_THRESHOLD", "20"))
SUFFICIENT_THRESHOLD = float(os.environ.get("OPENCLAW_CODEX_SWITCH_SUFFICIENT_THRESHOLD", "20"))
PREFER_DELTA = float(os.environ.get("OPENCLAW_CODEX_SWITCH_PREFER_DELTA", "100"))
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", str(Path.home() / ".openclaw")))
OPENCLAW_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
OPENCLAW_AGENT_DIR = Path(os.environ.get("OPENCLAW_AGENT_DIR", str(OPENCLAW_HOME / "agents" / OPENCLAW_AGENT_ID / "agent")))
STATE_PATH = Path(os.environ.get("OPENCLAW_AUTH_STATE", str(OPENCLAW_AGENT_DIR / "auth-state.json")))
PROFILES_PATH = Path(os.environ.get("OPENCLAW_AUTH_PROFILES", str(OPENCLAW_AGENT_DIR / "auth-profiles.json")))
CONFIG_PATH = Path(os.environ.get("OPENCLAW_CONFIG", str(OPENCLAW_HOME / "openclaw.json")))
LOG_PATH = Path(os.environ.get("OPENCLAW_CODEX_SWITCH_LOG", str(OPENCLAW_HOME / "logs" / "openai-codex-auto-switch.log")))
WHAM_URL = "https://chatgpt.com/backend-api/wham/usage"
DEFAULT_NOTIFY_GROUP = os.environ.get("OPENCLAW_CODEX_SWITCH_NOTIFY_GROUP", "")


def log(msg):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y-%m-%d %H:%M:%S %z")
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")


def load_json(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        if default is not None:
            return default
        raise


def email_of(profile_id, profiles=None):
    cred = (profiles or {}).get(profile_id) or {}
    return cred.get("email") or profile_id.split(":", 1)[-1]


def get_active_profile(state, profile_ids):
    order = (state.get("order") or {}).get(PROVIDER)
    if isinstance(order, list):
        for pid in order:
            if pid in profile_ids:
                return pid
    last = (state.get("lastGood") or {}).get(PROVIDER)
    if last in profile_ids:
        return last
    return profile_ids[0] if profile_ids else None


def window_remaining(result, name):
    by_name = {w.get("name"): w for w in result.get("windows", [])}
    w = by_name.get(name) or {}
    return w.get("remaining")


def probe_usage(profile_id, cred):
    access = cred.get("access")
    if not access:
        return {"profileId": profile_id, "ok": False, "error": "missing_access"}
    headers = {
        "Authorization": "Bearer " + access,
        "Accept": "application/json",
        "User-Agent": "CodexAutoSwitch",
    }
    if cred.get("accountId"):
        headers["ChatGPT-Account-Id"] = str(cred["accountId"])
    req = urllib.request.Request(WHAM_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.load(res)
    except Exception as e:
        return {"profileId": profile_id, "ok": False, "error": type(e).__name__}

    rl = data.get("rate_limit") or {}
    windows = []
    for name in ("primary_window", "secondary_window"):
        w = rl.get(name)
        if isinstance(w, dict) and isinstance(w.get("used_percent"), (int, float)):
            used = max(0.0, min(100.0, float(w["used_percent"])))
            windows.append({
                "name": name,
                "used": used,
                "remaining": 100.0 - used,
                "reset_after_seconds": w.get("reset_after_seconds"),
            })
    if not windows:
        return {"profileId": profile_id, "ok": False, "error": "no_windows"}
    return {
        "profileId": profile_id,
        "ok": True,
        "limitReached": bool(rl.get("limit_reached")),
        "remaining": min(w["remaining"] for w in windows),
        "windows": windows,
    }


def fmt_pct(value):
    try:
        return f"{float(value):.0f}%"
    except Exception:
        return "?%"


def fmt_result(pid, r, profiles):
    email = email_of(pid, profiles)
    if not r.get("ok"):
        return f"{email}=ERR:{r.get('error','?')}"
    p = window_remaining(r, "primary_window")
    w = window_remaining(r, "secondary_window")
    return f"{email}=5h:{fmt_pct(p)}/week:{fmt_pct(w)}"


def is_in_cooldown(state, profile_id):
    stat = ((state.get("usageStats") or {}).get(profile_id) or {})
    try:
        return float(stat.get("cooldownUntil") or 0) > time.time() * 1000
    except Exception:
        return False


def candidate_ok(state, result):
    if not result.get("ok") or result.get("limitReached"):
        return False
    pid = result.get("profileId")
    if pid and is_in_cooldown(state, pid):
        return False
    primary = window_remaining(result, "primary_window")
    weekly = window_remaining(result, "secondary_window")
    if primary is None or weekly is None:
        return False
    return primary >= SUFFICIENT_THRESHOLD and weekly >= SUFFICIENT_THRESHOLD


def set_order(first, all_profile_ids, dry_run=False):
    new_order = [first] + [pid for pid in all_profile_ids if pid != first]
    if dry_run:
        return new_order
    cmd = ["openclaw", "models", "auth", "order", "set", "--provider", PROVIDER, *new_order]
    subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return new_order


def napcat_config():
    cfg = load_json(CONFIG_PATH, {})
    return ((cfg.get("channels") or {}).get("napcat") or {})


def notify_group(text, group_id=DEFAULT_NOTIFY_GROUP, dry_run=False):
    if not group_id:
        return
    if dry_run:
        log(f"dry-run notify group {group_id}: {text}")
        return
    cfg = napcat_config()
    send_url = cfg.get("sendUrl") or "http://127.0.0.1:3000/send_msg"
    token = cfg.get("accessToken") or ""
    body = json.dumps({"group_id": str(group_id), "message": text}, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(send_url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            res.read(200)
    except Exception as exc:
        log(f"notify failed: {type(exc).__name__}: {exc}")


def build_switched_message(active, best, best_result, active_result, profiles):
    bp = window_remaining(best_result, "primary_window")
    bw = window_remaining(best_result, "secondary_window")
    ap = window_remaining(active_result, "primary_window") if active_result else None
    aw = window_remaining(active_result, "secondary_window") if active_result else None
    return (
        "Codex 账号已自动切换。\n"
        f"原因：原账号 5h 剩余 {fmt_pct(ap)}，低于 {ACTIVE_5H_THRESHOLD:.0f}% 阈值。\n"
        f"原账号：{email_of(active, profiles)}（5h {fmt_pct(ap)} / Week {fmt_pct(aw)}）\n"
        f"新账号：{email_of(best, profiles)}（5h {fmt_pct(bp)} / Week {fmt_pct(bw)}）"
    )


def build_no_candidate_message(active, active_result, results, profiles):
    ap = window_remaining(active_result, "primary_window") if active_result else None
    aw = window_remaining(active_result, "secondary_window") if active_result else None
    lines = [
        "Codex 账号未能自动切换。",
        f"原因：当前账号 5h 剩余 {fmt_pct(ap)}，低于 {ACTIVE_5H_THRESHOLD:.0f}% 阈值，但没有找到 5h 和 Week 都 ≥ {SUFFICIENT_THRESHOLD:.0f}% 的可用其他账号。",
        f"当前账号：{email_of(active, profiles)}（5h {fmt_pct(ap)} / Week {fmt_pct(aw)}）",
        "其他账号：",
    ]
    for pid, r in results.items():
        if pid == active:
            continue
        lines.append("- " + fmt_result(pid, r, profiles))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="do not switch or notify; log intended actions")
    parser.add_argument("--notify", action="store_true", help="send QQ group notification on switch/no-candidate")
    parser.add_argument("--notify-group", default=DEFAULT_NOTIFY_GROUP)
    args = parser.parse_args(argv)

    profiles_store = load_json(PROFILES_PATH)
    state = load_json(STATE_PATH, {}) if STATE_PATH.exists() else {}
    profiles = {
        pid: cred for pid, cred in (profiles_store.get("profiles") or {}).items()
        if cred.get("provider") == PROVIDER and cred.get("type") == "oauth"
    }
    profile_ids = list(profiles.keys())
    if len(profile_ids) < 2:
        msg = "skip: fewer than two openai-codex oauth profiles"
        log(msg)
        return 0

    active = get_active_profile(state, profile_ids)
    results = {pid: probe_usage(pid, cred) for pid, cred in profiles.items()}
    active_result = results.get(active)
    summary = ", ".join(fmt_result(pid, r, profiles) for pid, r in results.items())

    active_primary = window_remaining(active_result or {}, "primary_window")
    candidates = [r for pid, r in results.items() if pid != active and candidate_ok(state, r)]
    best_candidate = max(candidates, key=lambda r: window_remaining(r, "primary_window") or 0, default=None)
    best_primary = window_remaining(best_candidate or {}, "primary_window") if best_candidate else None
    should_prefer_much_better = (
        active_result and active_result.get("ok") and active_primary is not None
        and best_primary is not None and best_primary - active_primary >= PREFER_DELTA
    )
    if active_result and active_result.get("ok") and active_primary is not None and active_primary >= ACTIVE_5H_THRESHOLD and not active_result.get("limitReached") and not should_prefer_much_better:
        log(f"ok: active={active}, 5h={active_primary:.1f}%; {summary}")
        return 0

    if not candidates:
        msg = build_no_candidate_message(active, active_result or {}, results, profiles)
        log(f"no switch: {msg.replace(chr(10), ' | ')}; {summary}")
        if args.notify:
            notify_group(msg, args.notify_group, dry_run=args.dry_run)
        return 1

    best = max(candidates, key=lambda r: min(window_remaining(r, "primary_window") or 0, window_remaining(r, "secondary_window") or 0))
    order = set_order(best["profileId"], profile_ids, dry_run=args.dry_run)
    msg = build_switched_message(active, best["profileId"], best, active_result or {}, profiles)
    log(f"switched: dry={args.dry_run} order={order}; {msg.replace(chr(10), ' | ')}; {summary}")
    if args.notify:
        notify_group(msg, args.notify_group, dry_run=args.dry_run)
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
