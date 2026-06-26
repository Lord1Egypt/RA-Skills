#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

GEN = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'scripts' / 'generate_storybook_v3.py'


def find_latest_output(universe: str, user_id: str):
    base = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'storybooks' / universe
    candidates = sorted(base.glob(f'user-{user_id}-*'), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


def main():
    parser = argparse.ArgumentParser(description='Refresh latest YumFu storybook HTML for a save/session')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--session-id')
    args = parser.parse_args()

    cmd = ['python3', str(GEN), '--user-id', args.user_id, '--universe', args.universe]
    if args.session_id:
        cmd += ['--session-id', args.session_id]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip() or proc.stdout.strip(), file=sys.stderr)
        sys.exit(proc.returncode)

    latest = find_latest_output(args.universe, args.user_id)
    if not latest:
        print(json.dumps({'success': False, 'error': 'storybook output not found'}, ensure_ascii=False))
        sys.exit(1)

    latest_link = latest.parent / f'user-{args.user_id}-latest'
    if latest_link.exists() or latest_link.is_symlink():
        latest_link.unlink()
    latest_link.symlink_to(latest, target_is_directory=True)

    html = latest / 'storybook.html'
    print(json.dumps({
        'success': True,
        'output_dir': str(latest),
        'latest_link': str(latest_link),
        'html': str(html),
        'generated_at': datetime.now().isoformat(),
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
