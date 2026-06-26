#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json

from common import events_path, run_path


def main() -> int:
    parser = argparse.ArgumentParser(description='List events from events.jsonl.')
    parser.add_argument('--run', required=True, help='Run directory')
    parser.add_argument('--limit', type=int, help='Only show the last N events')
    parser.add_argument('--json', action='store_true', help='Emit raw JSON array')
    args = parser.parse_args()

    ep = events_path(run_path(args.run))
    if not ep.exists():
        raise SystemExit(f'Missing events.jsonl at {ep}')

    events = [json.loads(line) for line in ep.read_text(encoding='utf-8').splitlines() if line.strip()]
    if args.limit:
        events = events[-args.limit :]

    if args.json:
        print(json.dumps(events, indent=2))
    else:
        for event in events:
            print(f"{event['seq']}\t{event['ts']}\t{event['type']}\t{event.get('task_id') or '-'}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
