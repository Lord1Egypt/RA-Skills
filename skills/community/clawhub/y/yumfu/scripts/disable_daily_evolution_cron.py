#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

SET_SCRIPT = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'set_daily_evolution.py'
LOAD_EVOLUTION = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'load_daily_evolution.py'


def main():
    parser = argparse.ArgumentParser(description='Disable a YumFu daily evolution cron job and sidecar state')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    args = parser.parse_args()

    load = subprocess.run([
        'python3', str(LOAD_EVOLUTION),
        '--user-id', args.user_id,
        '--universe', args.universe,
    ], capture_output=True, text=True)
    if load.returncode != 0:
        print(load.stderr.strip() or load.stdout.strip(), file=sys.stderr)
        sys.exit(load.returncode)

    payload = json.loads(load.stdout)
    cron_id = None
    if payload.get('exists') and payload.get('data'):
        cron_id = payload['data'].get('cron_id')

    cron_result = None
    if cron_id:
        proc = subprocess.run(['openclaw', 'cron', 'disable', cron_id, '--json'], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            cron_result = json.loads(proc.stdout)
        else:
            cron_result = {'error': proc.stderr.strip() or proc.stdout.strip(), 'cron_id': cron_id}

    sub = subprocess.run([
        'python3', str(SET_SCRIPT),
        '--user-id', args.user_id,
        '--universe', args.universe,
        '--enabled', 'false'
    ], capture_output=True, text=True)
    if sub.returncode != 0:
        print(sub.stderr.strip() or sub.stdout.strip(), file=sys.stderr)
        sys.exit(sub.returncode)

    sidecar_update = json.loads(sub.stdout)
    print(json.dumps({'success': True, 'cron_id': cron_id, 'cron_result': cron_result, 'sidecar_update': sidecar_update}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
