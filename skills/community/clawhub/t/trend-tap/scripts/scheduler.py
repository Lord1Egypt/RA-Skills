#!/usr/bin/env python3
"""
Trend Tap scheduler — manages cron jobs for daily trend briefings.
Uses the system crontab (no external dependencies).
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_TRENDS_PY = _SCRIPT_DIR / "trends.py"
_CRON_TAG = "# trend-tap-daily"

_PYTHON = sys.executable or "python3"


def _get_current_crontab() -> str:
    """Read current user crontab, returns empty string if none."""
    try:
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout
    except Exception:
        pass
    return ""


def _write_crontab(content: str):
    """Write new crontab content."""
    proc = subprocess.Popen(
        ["crontab", "-"], stdin=subprocess.PIPE, text=True, timeout=10,
    )
    proc.communicate(input=content)
    if proc.returncode != 0:
        print("❌ Failed to write crontab", file=sys.stderr)
        sys.exit(1)


def _remove_our_lines(crontab: str) -> str:
    """Remove all trend-tap lines from crontab."""
    lines = crontab.splitlines()
    filtered = []
    skip_next = False
    for line in lines:
        if _CRON_TAG in line:
            skip_next = False
            continue
        if skip_next:
            skip_next = False
            continue
        filtered.append(line)
    return "\n".join(filtered) + "\n" if filtered else ""


def set_schedule(cron_expr: str, sources: str = "", top: int = 5, region: str = ""):
    """Add a cron job for trend-tap."""
    cmd_parts = [_PYTHON, str(_TRENDS_PY), "--mode", "all", "--top", str(top), "--save"]
    if sources:
        cmd_parts.extend(["--source", sources])
    if region:
        cmd_parts.extend(["--region", region])

    cmd = " ".join(cmd_parts)
    cron_line = f"{cron_expr} {cmd} {_CRON_TAG}"

    current = _get_current_crontab()
    cleaned = _remove_our_lines(current)
    new_content = cleaned.rstrip("\n") + "\n" + cron_line + "\n"

    _write_crontab(new_content)
    print(f"✅ Schedule set: {cron_expr}")
    print(f"   Command: {cmd}")
    print(f"   Results saved to: ~/.openclaw/trend-tap/daily/")


def list_schedules():
    """Show current trend-tap cron jobs."""
    current = _get_current_crontab()
    found = False
    for line in current.splitlines():
        if _CRON_TAG in line:
            clean = line.replace(_CRON_TAG, "").strip()
            print(f"📅 {clean}")
            found = True
    if not found:
        print("No trend-tap schedules found.")
        print("Set one with: python3 scheduler.py --set \"0 11 * * *\"")


def remove_schedule():
    """Remove all trend-tap cron jobs."""
    current = _get_current_crontab()
    cleaned = _remove_our_lines(current)
    _write_crontab(cleaned)
    print("🗑️ All trend-tap schedules removed.")


def main():
    parser = argparse.ArgumentParser(
        description="Manage trend-tap daily briefing schedules",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--set", metavar="CRON", help='Cron expression, e.g. "0 11 * * *" for daily 11AM')
    group.add_argument("--list", action="store_true", help="List current schedules")
    group.add_argument("--remove", action="store_true", help="Remove all schedules")

    parser.add_argument("--source", default="", help="Sources for scheduled fetch (comma-separated)")
    parser.add_argument("--top", type=int, default=5, help="Items per source (default: 5)")
    parser.add_argument("--region", default="", help="Region filter")

    args = parser.parse_args()

    if args.set:
        set_schedule(args.set, sources=args.source, top=args.top, region=args.region)
    elif args.list:
        list_schedules()
    elif args.remove:
        remove_schedule()


if __name__ == "__main__":
    main()
