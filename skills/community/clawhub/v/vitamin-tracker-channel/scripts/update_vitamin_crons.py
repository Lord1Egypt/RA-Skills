#!/usr/bin/env python3
"""Update OpenClaw cron jobs for vitamin/supplement reminders from VITAMINS.md."""

import os
import re
import json
import subprocess
from pathlib import Path

WORKSPACE = Path(os.environ.get('WORKSPACE', os.path.expanduser('~/.openclaw/workspace')))
VITAMINS = WORKSPACE / 'VITAMINS.md'
CHANNEL_ID = os.environ.get('VITAMIN_CHANNEL_ID', '')
SESSION_KEY_TEMPLATE = 'agent:main:discord:channel:{channel_id}'
TZ = os.environ.get('VITAMIN_TIMEZONE', 'UTC')


def parse_file(text: str):
    schedule = {}
    schedule_match = re.search(r'## Schedule\n(.*?)(?:\n## |\Z)', text, re.S)
    if not schedule_match:
        raise SystemExit('Could not find ## Schedule section in VITAMINS.md')
    for raw in schedule_match.group(1).splitlines():
        m = re.match(r'-\s+(.+?):\s+(\d{2}:\d{2})\s*$', raw.strip())
        if m:
            schedule[m.group(1)] = m.group(2)

    reminders = {}
    for label in schedule:
        pattern = rf'### {re.escape(label)}\n(.*?)(?=\n### |\n## |\Z)'
        m = re.search(pattern, text, re.S)
        if not m:
            raise SystemExit(f'Could not find section for {label}')
        lines = [ln.rstrip() for ln in m.group(1).strip().splitlines() if ln.strip()]
        items = []
        current = None
        for ln in lines:
            s = ln.strip()
            if s.startswith('- '):
                current = s[2:].strip()
                items.append(current)
            elif s.startswith('-'):
                current = s[1:].strip()
                items.append(current)
            else:
                if current is not None:
                    items[-1] = items[-1] + f' ({s.lstrip("- ").strip()})'
        reminders[label] = items
    return schedule, reminders


def time_to_cron(hhmm: str):
    hour, minute = hhmm.split(':')
    return f'{int(minute)} {int(hour)} * * *'


def join_items(items):
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f'{items[0]} and {items[1]}'
    return ', '.join(items[:-1]) + f', and {items[-1]}'


def build_message(label, items):
    return f'Vitamin reminder: {label} time. Take {join_items(items)}.'


def run_openclaw(args):
    cmd = ['openclaw', 'cron'] + args
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def ensure_job(label, hhmm, items, channel_id):
    slug = label.lower().replace(' ', '-')
    name = f'vitamins-{slug}-reminder'
    expr = time_to_cron(hhmm)
    reminder_text = build_message(label, items)
    session_key = SESSION_KEY_TEMPLATE.format(channel_id=channel_id)
    return run_openclaw([
        'add',
        '--name', name,
        '--session-key', session_key,
        '--cron', expr,
        '--tz', TZ,
        '--message', f'Send a brief reminder to the user in the bound session: "{reminder_text}"',
        '--timeout-seconds', '120',
        '--announce',
        '--channel', 'discord',
        '--to', channel_id,
        '--json',
    ])


def list_jobs():
    proc = run_openclaw(['list', '--json'])
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or 'Failed to list cron jobs')
    data = json.loads(proc.stdout)
    if isinstance(data, dict) and 'jobs' in data:
        return data['jobs']
    if isinstance(data, list):
        return data
    raise SystemExit('Unexpected cron list JSON format')


def remove_job(job_id):
    proc = run_openclaw(['remove', job_id])
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or f'Failed to remove job {job_id}')


def main():
    if not CHANNEL_ID:
        raise SystemExit('VITAMIN_CHANNEL_ID env var is required')
    if not VITAMINS.exists():
        raise SystemExit(f'VITAMINS.md not found at {VITAMINS}')

    text = VITAMINS.read_text()
    schedule, reminders = parse_file(text)

    existing = list_jobs()
    existing_by_name = {job.get('name'): job for job in existing}

    for label in schedule:
        slug = label.lower().replace(' ', '-')
        job_name = f'vitamins-{slug}-reminder'
        job = existing_by_name.get(job_name)
        if job and job.get('id'):
            remove_job(job['id'])
        proc = ensure_job(label, schedule[label], reminders[label], CHANNEL_ID)
        if proc.returncode != 0:
            raise SystemExit(proc.stderr.strip() or f'Failed to create {job_name}')
        print(f'Updated {job_name} -> {schedule[label]} {TZ}')


if __name__ == '__main__':
    main()
