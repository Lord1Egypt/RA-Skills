#!/usr/bin/env python3
"""
Prepare an end-of-journey YumFu storybook refresh/generation.

Use this when a run reaches a real ending or the player explicitly retires / archives the run.
It does not send messages by itself. It generates/refreshes the latest HTML storybook and
returns structured JSON so the caller can deliver the HTML file back to chat.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
REFRESH = SCRIPT_DIR / 'refresh_storybook_v3.py'


def load_save(user_id: str, universe: str) -> dict[str, Any]:
    path = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'saves' / universe / f'user-{user_id}.json'
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def storybook_tracking_enabled(save: dict[str, Any]) -> bool:
    tracking = save.get('storybook_tracking')
    if isinstance(tracking, dict):
        return tracking.get('enabled', True) is not False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description='Prepare YumFu end-of-journey storybook generation')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--session-id')
    args = parser.parse_args()

    save = load_save(args.user_id, args.universe)
    if save and not storybook_tracking_enabled(save):
        print(json.dumps({
            'success': True,
            'generated': False,
            'skipped': True,
            'reason': 'storybook_tracking_disabled',
        }, ensure_ascii=False))
        return 0

    cmd = [sys.executable, str(REFRESH), '--user-id', args.user_id, '--universe', args.universe]
    if args.session_id:
        cmd += ['--session-id', args.session_id]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(json.dumps({
            'success': False,
            'generated': False,
            'error': proc.stderr.strip() or proc.stdout.strip() or 'storybook refresh failed',
            'command': cmd,
        }, ensure_ascii=False))
        return proc.returncode

    payload = json.loads(proc.stdout)
    payload['generated'] = True
    payload['send_back_to_chat'] = True
    payload['message'] = '📖 这局的结局 Storybook 已自动整理成 HTML 图文版，可以直接发回聊天。'
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
