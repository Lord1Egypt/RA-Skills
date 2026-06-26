#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

SET_SCRIPT = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'set_daily_evolution.py'
RUNNER = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'run_daily_evolution_job.py'
APPLY_RUNNER = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'run_daily_evolution.py'


def shell_quote_single(s: str) -> str:
    return s.replace("'", "'\"'\"'")


def main():
    parser = argparse.ArgumentParser(description='Create a per-player YumFu daily evolution cron job')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--target', required=True, help='Telegram/chat target id')
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--time', default='20:00', help='Local delivery time HH:MM')
    parser.add_argument('--tz', default='America/Los_Angeles')
    parser.add_argument('--agent', default='main')
    args = parser.parse_args()

    hh, mm = args.time.split(':', 1)
    cron_expr = f'{int(mm)} {int(hh)} * * *'
    name = f'YumFu Daily Evolution [{args.universe}:{args.user_id}]'

    message = f'''Run YumFu daily evolution for one player in safe sidecar mode.

Player:
- user_id: {args.user_id}
- universe: {args.universe}
- channel: {args.channel}
- target: {args.target}

Steps:
1. Run: python3 {RUNNER} --user-id {args.user_id} --universe {args.universe}
2. Read the JSON payload and generate one concise daily evolution update in the player's preferred language.
3. Generate one image matching image_prompt.
4. Write the generated JSON result to ~/clawd/tmp/yumfu-daily-{args.universe}-{args.user_id}.json
5. Run execution helper:
   python3 ~/clawd/skills/yumfu/scripts/execute_daily_evolution_delivery.py --user-id {args.user_id} --universe {args.universe} --target {args.target} --json ~/clawd/tmp/yumfu-daily-{args.universe}-{args.user_id}.json
6. Follow the returned execution plan exactly:
   - send listed `sends` items in order
   - after each successful send, run the matching `mark_commands`
   - run `apply_command` after delivery steps complete
7. Persist sidecar only using the returned `apply_command` (do not invent an alternate persistence path):
   python3 {APPLY_RUNNER} --user-id {args.user_id} --universe {args.universe} --apply-from-json ~/clawd/tmp/yumfu-daily-{args.universe}-{args.user_id}.json

Rules:
- Never mutate the main save directly
- No separate report-generated notification
- Keep the update short, scene-forward, and easy to reply to
- End with a natural re-entry hook
- Daily evolution should deliver image/text first, then TTS voice bubble by default unless the save explicitly turned TTS off
- Use `execute_daily_evolution_delivery.py` as the default low-freedom bridge for daily evolution delivery instead of hand-rolling image/TTS/state steps ad hoc
- If TTS generation fails, still send the main in-world update and report the gap honestly instead of pretending voice was delivered'''

    cmd = [
        'openclaw', 'cron', 'add',
        '--name', name,
        '--agent', args.agent,
        '--cron', cron_expr,
        '--tz', args.tz,
        '--session', 'isolated',
        '--wake', 'now',
        '--message', message,
        '--timeout-seconds', '180',
        '--no-deliver',
        '--json'
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    result = json.loads(proc.stdout)
    cron_id = result.get('id') or result.get('job', {}).get('id')

    # store enabled sidecar state with cron id
    if cron_id:
        sub = subprocess.run([
            'python3', str(SET_SCRIPT),
            '--user-id', args.user_id,
            '--universe', args.universe,
            '--enabled', 'true',
            '--channel', args.channel,
            '--cadence', 'daily',
            '--cron-id', cron_id,
        ], capture_output=True, text=True)
        if sub.returncode != 0:
            print(sub.stderr.strip() or sub.stdout.strip(), file=sys.stderr)
            sys.exit(sub.returncode)
        sidecar_update = json.loads(sub.stdout)
    else:
        sidecar_update = None

    print(json.dumps({
        'success': True,
        'cron_id': cron_id,
        'cron_expr': cron_expr,
        'tz': args.tz,
        'sidecar_update': sidecar_update,
        'raw': result
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
