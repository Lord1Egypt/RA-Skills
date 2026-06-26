#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

OPENCLAW_BIN = os.environ.get("OPENCLAW_BIN", "openclaw")
DEFAULT_TZ = os.environ.get("OPENCLAW_REMINDER_TZ", "UTC")
NAME_PREFIX = "reminder:"


def run_openclaw(args):
    cmd = [OPENCLAW_BIN, "cron", *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}")
    return proc.stdout.strip()


def load_jobs(include_all=True):
    args = ["list", "--json"]
    if include_all:
        args.insert(1, "--all")
    raw = run_openclaw(args)
    data = json.loads(raw or "{}")
    return data.get("jobs", [])


def parse_job_dt(job):
    at = job.get("schedule", {}).get("at")
    if not at:
        return None
    return datetime.fromisoformat(at.replace("Z", "+00:00"))


def localize(dt, tz_name=DEFAULT_TZ):
    return dt.astimezone(ZoneInfo(tz_name))


def is_reminder(job):
    return str(job.get("name", "")).startswith(NAME_PREFIX)


def reminder_title(job):
    name = str(job.get("name", ""))
    return name[len(NAME_PREFIX):] if name.startswith(NAME_PREFIX) else name


def reminder_text(job):
    text = str(job.get("payload", {}).get("text", ""))
    marker = "Reply with exactly this text and nothing else: "
    return text.split(marker, 1)[1] if marker in text else text


def print_jobs(jobs, tz_name=DEFAULT_TZ):
    rows = []
    for job in jobs:
        dt = parse_job_dt(job)
        local = localize(dt, tz_name).strftime("%Y-%m-%d %H:%M:%S %Z") if dt else "-"
        rows.append({
            "id": job.get("id"),
            "enabled": job.get("enabled"),
            "when": local,
            "title": reminder_title(job),
            "text": reminder_text(job),
        })
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def cmd_create(args):
    channel = args.channel or os.environ.get("OPENCLAW_REMINDER_CHANNEL")
    to = args.to or os.environ.get("OPENCLAW_REMINDER_TO")
    account = args.account or os.environ.get("OPENCLAW_REMINDER_ACCOUNT")
    if not channel or not to or not account:
        raise SystemExit("create requires --channel, --to, and --account (or matching OPENCLAW_REMINDER_* env vars)")

    title = args.title.strip()
    text = args.text.strip() if args.text else f"Reminder: {title}"
    reminder_message = (
        "You are delivering a scheduled reminder. "
        f"Reply with exactly this text and nothing else: {text}"
    )
    cmd = [
        "add",
        "--name", f"{NAME_PREFIX}{title}",
        "--at", args.at,
        "--tz", args.tz,
        "--channel", channel,
        "--to", to,
        "--account", account,
        "--announce",
        "--expect-final",
        "--delete-after-run",
        "--session", "isolated",
        "--message", reminder_message,
        "--json",
    ]
    if args.disabled:
        cmd.append("--disabled")
    raw = run_openclaw(cmd)
    print(raw)


def cmd_pending(args):
    now = datetime.now(timezone.utc)
    jobs = [j for j in load_jobs() if is_reminder(j)]
    pending = []
    for job in jobs:
        dt = parse_job_dt(job)
        if dt and dt >= now and job.get("enabled", False):
            pending.append(job)
    print_jobs(sorted(pending, key=lambda j: parse_job_dt(j)), args.tz)


def cmd_upcoming(args):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=args.days)
    jobs = [j for j in load_jobs() if is_reminder(j)]
    upcoming = []
    for job in jobs:
        dt = parse_job_dt(job)
        if dt and now <= dt <= end and job.get("enabled", False):
            upcoming.append(job)
    print_jobs(sorted(upcoming, key=lambda j: parse_job_dt(j)), args.tz)


def cmd_overdue(args):
    now = datetime.now(timezone.utc)
    jobs = [j for j in load_jobs() if is_reminder(j)]
    overdue = []
    for job in jobs:
        dt = parse_job_dt(job)
        if dt and dt < now and job.get("enabled", False):
            overdue.append(job)
    print_jobs(sorted(overdue, key=lambda j: parse_job_dt(j)), args.tz)


def cmd_delete(args):
    if not args.id and not args.title:
        raise SystemExit("delete requires --id or --title")
    jobs = [j for j in load_jobs() if is_reminder(j)]
    target = None
    if args.id:
        target = next((j for j in jobs if j.get("id") == args.id), None)
    else:
        exact = f"{NAME_PREFIX}{args.title}"
        target = next((j for j in jobs if j.get("name") == exact), None)
    if not target:
        raise SystemExit("reminder not found")
    if parse_job_dt(target) and parse_job_dt(target) < datetime.now(timezone.utc):
        raise SystemExit("refusing to delete an already overdue reminder via delete; inspect first")
    raw = run_openclaw(["remove", target["id"], "--json"])
    print(raw)


def build_parser():
    ap = argparse.ArgumentParser(description="Manage OpenClaw reminder cron jobs")
    sub = ap.add_subparsers(dest="cmd", required=True)

    create = sub.add_parser("create", help="Create a one-shot reminder")
    create.add_argument("--title", required=True)
    create.add_argument("--text", help="Final reminder text; default is Reminder: <title>")
    create.add_argument("--at", required=True, help="Offset-less datetime like 2026-04-26 14:00 or ISO datetime")
    create.add_argument("--tz", default=DEFAULT_TZ)
    create.add_argument("--channel")
    create.add_argument("--to")
    create.add_argument("--account")
    create.add_argument("--disabled", action="store_true")
    create.set_defaults(func=cmd_create)

    pending = sub.add_parser("pending", help="List enabled future reminders")
    pending.add_argument("--tz", default=DEFAULT_TZ)
    pending.set_defaults(func=cmd_pending)

    upcoming = sub.add_parser("upcoming", help="List reminders due within N days")
    upcoming.add_argument("--days", type=int, default=3)
    upcoming.add_argument("--tz", default=DEFAULT_TZ)
    upcoming.set_defaults(func=cmd_upcoming)

    overdue = sub.add_parser("overdue", help="List enabled reminders whose scheduled time already passed")
    overdue.add_argument("--tz", default=DEFAULT_TZ)
    overdue.set_defaults(func=cmd_overdue)

    delete = sub.add_parser("delete", help="Delete a future reminder by id or title")
    delete.add_argument("--id")
    delete.add_argument("--title")
    delete.set_defaults(func=cmd_delete)
    return ap


def main():
    ap = build_parser()
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
