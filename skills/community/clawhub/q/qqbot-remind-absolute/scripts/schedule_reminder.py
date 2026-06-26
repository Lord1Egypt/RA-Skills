from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

STATE_PATH = Path(__file__).resolve().parent.parent / "data" / "user_timezones.json"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("action", nargs="?", default="add", choices=["add", "list", "remove", "set-timezone", "get-timezone"])
    p.add_argument("--content")
    p.add_argument("--to")
    p.add_argument("--at")
    p.add_argument("--in", dest="in_minutes", type=int)
    p.add_argument("--cron")
    p.add_argument("--id")
    p.add_argument("--timezone")
    return p.parse_args()


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_timezone_for_target(target: str) -> str | None:
    return load_state().get(target)


def set_timezone_for_target(target: str, timezone: str) -> None:
    ZoneInfo(timezone)
    state = load_state()
    state[target] = timezone
    save_state(state)


def find_openclaw_cmd() -> str:
    candidates = [
        "openclaw.cmd",
        str(Path.home() / "AppData" / "Roaming" / "npm" / "openclaw.cmd"),
    ]
    for candidate in candidates:
        try:
            result = subprocess.run([candidate, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
            if result.returncode == 0 or result.stdout or result.stderr:
                return candidate
        except FileNotFoundError:
            continue
    raise SystemExit("openclaw.cmd not found in PATH.")


def print_json(data: object) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def ensure_timezone(target: str, explicit_timezone: str | None) -> str:
    if explicit_timezone:
        try:
            ZoneInfo(explicit_timezone)
        except ZoneInfoNotFoundError:
            raise SystemExit("无效时区，请使用 IANA 时区名，例如 Asia/Shanghai")
        set_timezone_for_target(target, explicit_timezone)
        return explicit_timezone
    stored = get_timezone_for_target(target)
    if stored:
        return stored
    raise SystemExit("首次创建提醒前需要先显式设置时区。请先告诉我你的时区，例如 Asia/Shanghai")


def parse_time_text(text: str, tz_name: str) -> tuple[str | None, str | None]:
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = text.strip().replace("：", ":").replace(".", ":")

    recurring_prefix = {
        "每天": "*",
        "每日": "*",
        "工作日": "1-5",
        "周一": "1",
        "周二": "2",
        "周三": "3",
        "周四": "4",
        "周五": "5",
        "周六": "6",
        "周日": "0",
        "周天": "0",
        "星期一": "1",
        "星期二": "2",
        "星期三": "3",
        "星期四": "4",
        "星期五": "5",
        "星期六": "6",
        "星期日": "0",
        "星期天": "0",
    }
    period_map = {
        "凌晨": 0,
        "早上": 8,
        "上午": 9,
        "中午": 12,
        "下午": 15,
        "晚上": 20,
        "今晚": 20,
    }

    prefix = None
    for key in sorted(recurring_prefix.keys(), key=len, reverse=True):
        if raw.startswith(key):
            prefix = key
            raw = raw[len(key):].strip()
            break

    tomorrow = False
    if raw.startswith("明天"):
        tomorrow = True
        raw = raw[2:].strip()
    elif raw.startswith("今天"):
        raw = raw[2:].strip()

    period = None
    for key in period_map:
        if raw.startswith(key):
            period = key
            raw = raw[len(key):].strip()
            break

    normalized = raw.replace("点半", ":30").replace("点", ":").replace("分", "")
    if normalized.endswith(":"):
        normalized += "00"
    if ":" not in normalized and normalized.isdigit():
        normalized = f"{normalized}:00"

    try:
        hour_str, minute_str = normalized.split(":", 1)
        hour = int(hour_str)
        minute = int(minute_str or "0")
    except ValueError:
        raise SystemExit("无法解析时间，请改用更明确的格式。")

    if period in {"下午", "晚上", "今晚"} and 1 <= hour <= 11:
        hour += 12
    if period == "中午" and hour < 11:
        hour += 12
    if period == "凌晨" and hour == 12:
        hour = 0

    if prefix:
        return None, f"{minute} {hour} * * {recurring_prefix[prefix]}"

    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M", "%H:%M"):
        try:
            parsed = datetime.strptime(text.strip().replace(".", ":"), fmt)
            if fmt == "%H:%M":
                dt = now.replace(hour=parsed.hour, minute=parsed.minute, second=0, microsecond=0)
                if dt <= now:
                    dt += timedelta(days=1)
                return dt.isoformat(timespec="minutes"), None
            dt = parsed.replace(tzinfo=tz)
            return dt.isoformat(timespec="minutes"), None
        except ValueError:
            continue

    dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if tomorrow:
        dt += timedelta(days=1)
    elif dt <= now:
        dt += timedelta(days=1)
    return dt.isoformat(timespec="minutes"), None


def create_job(openclaw_cmd: str, *, content: str, to: str, timezone: str, dt: str | None, cron: str | None) -> dict:
    name = f"Reminder: {content}"
    message = (
        f"你是一个提醒助手。请直接提醒用户：{content}。"
        "要求：1. 直接输出提醒内容 2. 不要解释身份 3. 简短自然 4. 带一点关怀语气。"
    )
    cmd = [
        openclaw_cmd,
        "cron",
        "add",
        "--name",
        name,
        "--session",
        "isolated",
        "--message",
        message,
        "--channel",
        "qqbot",
        "--to",
        to,
        "--announce",
        "--json",
    ]
    if cron:
        cmd.extend(["--cron", cron, "--tz", timezone])
    else:
        cmd.extend(["--at", dt, "--delete-after-run"])
    result = run_cmd(cmd)
    if result.returncode != 0:
        raise SystemExit(result.stderr or result.stdout)
    payload = json.loads(result.stdout.strip())
    return {
        "id": payload.get("id"),
        "name": name,
        "timezone": timezone,
        "schedule": payload.get("schedule"),
        "delivery": payload.get("delivery"),
    }


def main() -> int:
    args = parse_args()
    openclaw_cmd = find_openclaw_cmd()

    if args.action == "set-timezone":
        if not args.to or not args.timezone:
            raise SystemExit("set-timezone 需要 --to 和 --timezone")
        set_timezone_for_target(args.to, args.timezone)
        print_json({"ok": True, "to": args.to, "timezone": args.timezone})
        return 0

    if args.action == "get-timezone":
        if not args.to:
            raise SystemExit("get-timezone 需要 --to")
        print_json({"to": args.to, "timezone": get_timezone_for_target(args.to)})
        return 0

    if args.action == "list":
        if not args.to:
            raise SystemExit("list 需要 --to")
        result = run_cmd([openclaw_cmd, "cron", "list", "--json"])
        if result.returncode != 0:
            raise SystemExit(result.stderr or result.stdout)
        parsed = json.loads(result.stdout or "[]")
        items = parsed.get("jobs", parsed) if isinstance(parsed, dict) else parsed
        filtered = []
        for item in items:
            delivery = item.get("delivery") or {}
            if delivery.get("channel") == "qqbot" and delivery.get("to") == args.to:
                filtered.append({
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "schedule": item.get("schedule"),
                    "enabled": item.get("enabled"),
                })
        print_json(filtered)
        return 0

    if args.action == "remove":
        if not args.id:
            raise SystemExit("remove 需要 --id")
        result = run_cmd([openclaw_cmd, "cron", "rm", args.id, "--json"])
        if result.returncode != 0:
            raise SystemExit(result.stderr or result.stdout)
        print_json(json.loads(result.stdout.strip()) if result.stdout.strip() else {"ok": True})
        return 0

    if not args.to:
        raise SystemExit("add 需要 --to")
    timezone = ensure_timezone(args.to, args.timezone)

    if not args.content:
        raise SystemExit("add 需要 --content")

    dt = None
    cron = args.cron
    if args.in_minutes is not None:
        target = datetime.now(ZoneInfo(timezone)) + timedelta(minutes=args.in_minutes)
        dt = target.isoformat(timespec="minutes")
    elif args.at:
        dt, cron = parse_time_text(args.at, timezone)
    elif not cron:
        raise SystemExit("add 需要 --at、--in 或 --cron 之一")

    print_json(create_job(openclaw_cmd, content=args.content, to=args.to, timezone=timezone, dt=dt, cron=cron))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
