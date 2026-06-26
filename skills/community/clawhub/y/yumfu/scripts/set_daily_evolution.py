#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def evolution_path(user_id: str, universe: str) -> Path:
    return Path.home() / 'clawd' / 'memory' / 'yumfu' / 'evolution' / universe / f'user-{user_id}.json'


def main():
    parser = argparse.ArgumentParser(description='Enable/disable YumFu daily evolution in sidecar state (safe mode)')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--enabled', required=True, choices=['true', 'false'])
    parser.add_argument('--channel', default='telegram')
    parser.add_argument('--cadence', default='daily')
    parser.add_argument('--cron-id', default=None)
    args = parser.parse_args()

    path = evolution_path(args.user_id, args.universe)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = {}

    enabled = args.enabled == 'true'
    now = datetime.now()
    state = {
        'user_id': args.user_id,
        'universe': args.universe,
        'enabled': enabled,
        'channel': args.channel,
        'cadence': args.cadence,
        'cron_id': args.cron_id,
        'last_tick_at': existing.get('last_tick_at'),
        'next_tick_at': (now + timedelta(days=1)).isoformat() if enabled else None,
        'last_summary': existing.get('last_summary'),
        'last_story_text': existing.get('last_story_text'),
        'last_severity': existing.get('last_severity'),
        'last_image_prompt': existing.get('last_image_prompt'),
        'pending_hooks': existing.get('pending_hooks', []),
        'meta': existing.get('meta', {}),
        'history': existing.get('history', [])
    }

    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'success': True,
        'sidecar_path': str(path),
        'enabled': enabled,
        'channel': args.channel,
        'cadence': args.cadence,
        'next_tick_at': state['next_tick_at']
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
