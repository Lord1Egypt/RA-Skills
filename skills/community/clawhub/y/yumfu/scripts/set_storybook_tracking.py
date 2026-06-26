#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def load_save(user_id: str, universe: str):
    save_path = Path.home() / 'clawd' / 'memory' / 'yumfu' / 'saves' / universe / f'user-{user_id}.json'
    if not save_path.exists():
        raise FileNotFoundError(f'No save found: {save_path}')
    with open(save_path, 'r', encoding='utf-8') as f:
        return save_path, json.load(f)


def main():
    parser = argparse.ArgumentParser(description='Enable/disable YumFu storybook tracking per save')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    parser.add_argument('--enabled', required=True, choices=['true', 'false'])
    parser.add_argument('--auto-refresh-html', default='true', choices=['true', 'false'])
    parser.add_argument('--delivery', default='on-request', choices=['on-request', 'final-only', 'milestones'])
    args = parser.parse_args()

    save_path, data = load_save(args.user_id, args.universe)
    tracking = data.get('storybook_tracking', {})
    tracking.update({
        'enabled': args.enabled == 'true',
        'auto_refresh_html': args.auto_refresh_html == 'true',
        'delivery': args.delivery,
        'last_updated': datetime.now().isoformat(),
    })
    data['storybook_tracking'] = tracking

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(json.dumps({
        'success': True,
        'save_path': str(save_path),
        'storybook_tracking': tracking,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
