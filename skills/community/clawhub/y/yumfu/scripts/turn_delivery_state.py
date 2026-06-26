#!/usr/bin/env python3
"""
Per-turn delivery state for YumFu.
Prevents duplicate sends such as:
- image first, then image+caption again
- multiple image sends for one turn
- multiple TTS bubbles for one turn
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

STATE_ROOT = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'delivery-state'


def state_path(user_id: str, universe: str, turn_id: str) -> Path:
    return STATE_ROOT / universe / f'user-{user_id}' / f'{turn_id}.json'


def load(user_id: str, universe: str, turn_id: str) -> dict:
    p = state_path(user_id, universe, turn_id)
    if not p.exists():
        return {
            'turn_id': turn_id,
            'user_id': user_id,
            'universe': universe,
            'created_at': datetime.now().isoformat(),
            'main_text_sent': False,
            'image_sent': False,
            'tts_sent': False,
            'storybook_sent': False,
            'image_mode': None,
        }
    return json.loads(p.read_text(encoding='utf-8'))


def save(payload: dict) -> Path:
    p = state_path(payload['user_id'], payload['universe'], payload['turn_id'])
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return p


def main() -> None:
    parser = argparse.ArgumentParser(description='Manage YumFu turn delivery state')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--turn-id', required=True)
    parser.add_argument('--mark', choices=['main_text_sent', 'image_sent', 'tts_sent', 'storybook_sent'])
    parser.add_argument('--image-mode', choices=['caption', 'fallback-image-only'])
    args = parser.parse_args()

    payload = load(args.user_id, args.universe, args.turn_id)
    if args.mark:
        payload[args.mark] = True
        payload['updated_at'] = datetime.now().isoformat()
    if args.image_mode:
        payload['image_mode'] = args.image_mode
        payload['updated_at'] = datetime.now().isoformat()
    path = save(payload)
    print(json.dumps({'success': True, 'path': str(path), 'state': payload}, ensure_ascii=False))


if __name__ == '__main__':
    main()
