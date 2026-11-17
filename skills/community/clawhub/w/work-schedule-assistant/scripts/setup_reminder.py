#!/usr/bin/env python3
"""Create an OpenClaw cron job for the daily work schedule reminder."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def validate_time(value: str) -> tuple[int, int]:
    try:
        hour_text, minute_text = value.split(":", 1)
        hour, minute = int(hour_text), int(minute_text)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("时间必须为 HH:MM") from exc
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise argparse.ArgumentTypeError("时间超出范围")
    return hour, minute


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time", default="08:30", help="Daily time, HH:MM")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    parser.add_argument("--channel", default="last")
    parser.add_argument("--to")
    parser.add_argument("--name", default="每日工作日程提醒")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and not shutil.which("openclaw"):
        raise SystemExit("未找到 openclaw 命令")
    hour, minute = validate_time(args.time)
    schedule_script = Path(__file__).with_name("work_schedule.py").resolve()
    python = shutil.which("python3") or sys.executable
    command_argv = [
        python,
        str(schedule_script),
        "brief",
        "--date",
        "today",
    ]
    command = [
        "openclaw",
        "cron",
        "create",
        f"{minute} {hour} * * *",
        "--name",
        args.name,
        "--command-argv",
        json.dumps(command_argv, ensure_ascii=False),
        "--command-cwd",
        str(schedule_script.parent.parent),
        "--announce",
        "--channel",
        args.channel,
        "--tz",
        args.timezone,
    ]
    if args.to:
        command.extend(["--to", args.to])
    if args.dry_run:
        print(json.dumps(command, ensure_ascii=False, indent=2))
        return
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
