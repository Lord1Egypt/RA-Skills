#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ENABLE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'enable_daily_evolution.py'
DISABLE = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'disable_daily_evolution_cron.py'


def main():
    parser = argparse.ArgumentParser(description='Handle the player choice for YumFu daily evolution after /yumfu start')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--choice', required=True, choices=['yes', 'no'])
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--time', default='20:00')
    parser.add_argument('--tz', default='America/Los_Angeles')
    args = parser.parse_args()

    if args.choice == 'yes':
        proc = subprocess.run([
            'python3', str(ENABLE),
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
        payload = json.loads(proc.stdout)
        print(json.dumps({
            'success': True,
            'enabled': True,
            'message_zh': '已开启每日世界演进。之后会按设定时间自动发一条短的场景推进消息。',
            'message_en': 'Daily world evolution is enabled. You will get one short scene-forward update at the scheduled time.',
            'details': payload,
        }, ensure_ascii=False, indent=2))
        return

    proc = subprocess.run([
        'python3', str(DISABLE),
        '--user-id', args.user_id,
        '--universe', args.universe,
    ], capture_output=True, text=True)
    # If disable fails because nothing exists yet, still treat the choice as valid/no-op.
    if proc.returncode == 0 and proc.stdout.strip():
        details = json.loads(proc.stdout)
    else:
        details = {'note': 'No existing daily evolution cron to disable; leaving feature off.'}

    print(json.dumps({
        'success': True,
        'enabled': False,
        'message_zh': '未开启每日世界演进。这个世界只会在你主动继续游戏时推进。',
        'message_en': 'Daily world evolution stays off. This world will only advance when you actively continue playing.',
        'details': details,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
