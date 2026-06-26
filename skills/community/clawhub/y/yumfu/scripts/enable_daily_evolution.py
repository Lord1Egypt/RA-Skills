#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

CREATE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'create_daily_evolution_cron.py'


def main():
    parser = argparse.ArgumentParser(description='One-shot helper: enable YumFu daily evolution for a player/world')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--time', default='20:00')
    parser.add_argument('--tz', default='America/Los_Angeles')
    args = parser.parse_args()

    proc = subprocess.run([
        'python3', str(CREATE),
        '--user-id', args.user_id,
        '--universe', args.universe,
        '--target', args.target,
        '--channel', args.channel,
        '--time', args.time,
        '--tz', args.tz,
    ], capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)
    print(proc.stdout)


if __name__ == '__main__':
    main()
