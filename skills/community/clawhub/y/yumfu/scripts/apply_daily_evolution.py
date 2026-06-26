#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


def evolution_path(user_id: str, universe: str) -> Path:
    return Path.home() / 'clawd' / 'memory' / 'yumfu' / 'evolution' / universe / f'user-{user_id}.json'


def main():
    parser = argparse.ArgumentParser(description='Write YumFu daily evolution result to sidecar state (safe mode)')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--summary', required=True)
    parser.add_argument('--story-text', default='')
    parser.add_argument('--severity', default='minor')
    parser.add_argument('--image-prompt', default='')
    parser.add_argument('--hooks-json', default='[]')
    parser.add_argument('--meta-json', default='{}')
    parser.add_argument('--routes-json', default='[]')
    parser.add_argument('--default-route-json', default='{}')
    parser.add_argument('--advancement-level', default='normal')
    parser.add_argument('--advancement-at', default='')
    args = parser.parse_args()

    path = evolution_path(args.user_id, args.universe)
    path.parent.mkdir(parents=True, exist_ok=True)

    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text())
        except Exception:
            existing = {}

    now = datetime.now()
    hooks = json.loads(args.hooks_json)
    meta = json.loads(args.meta_json)
    routes = json.loads(args.routes_json)
    default_route = json.loads(args.default_route_json)

    advancement_at = args.advancement_at or now.isoformat()

    history = existing.get('history', [])
    history.append({
        'at': now.isoformat(),
        'summary': args.summary,
        'severity': args.severity,
        'story_text': args.story_text[:2000],
        'image_prompt': args.image_prompt,
        'hooks': hooks,
        'routes': routes,
        'default_route': default_route,
        'advancement_level': args.advancement_level,
        'advancement_at': advancement_at,
        'meta': meta,
    })

    active_route = default_route or existing.get('active_route') or {}

    state = {
        'user_id': args.user_id,
        'universe': args.universe,
        'last_tick_at': now.isoformat(),
        'next_tick_at': (now + timedelta(days=1)).isoformat(),
        'last_summary': args.summary,
        'last_story_text': args.story_text,
        'last_severity': args.severity,
        'last_image_prompt': args.image_prompt,
        'pending_hooks': hooks,
        'suggested_routes': routes,
        'default_route': default_route,
        'active_route': active_route,
        'last_advancement_level': args.advancement_level,
        'last_advancement_at': advancement_at,
        'last_major_advancement_at': advancement_at if args.advancement_level == 'major' else existing.get('last_major_advancement_at'),
        'meta': meta,
        'history': history[-30:]
    }

    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'success': True,
        'sidecar_path': str(path),
        'last_tick_at': state['last_tick_at'],
        'next_tick_at': state['next_tick_at'],
        'last_summary': state['last_summary']
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
