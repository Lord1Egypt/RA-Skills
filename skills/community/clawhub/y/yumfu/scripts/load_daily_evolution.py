#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def evolution_path(user_id: str, universe: str) -> Path:
    return Path.home() / 'clawd' / 'memory' / 'yumfu' / 'evolution' / universe / f'user-{user_id}.json'


def main():
    parser = argparse.ArgumentParser(description='Load YumFu daily evolution sidecar state')
    parser.add_argument('--user-id', required=True)
    parser.add_argument('--universe', required=True)
    args = parser.parse_args()

    path = evolution_path(args.user_id, args.universe)
    if not path.exists():
        print(json.dumps({'exists': False, 'sidecar_path': str(path), 'data': None}, ensure_ascii=False))
        return

    data = json.loads(path.read_text())
    print(json.dumps({'exists': True, 'sidecar_path': str(path), 'data': data}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
