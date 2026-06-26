#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from common import STATE_PATH, load_json, save_json


def main(argv: list[str]):
    if len(argv) < 2:
        print('Usage: mark_notified.py <tweet_id>')
        raise SystemExit(1)
    tweet_id = str(argv[1])
    state = load_json(STATE_PATH, {})
    ids = state.setdefault('notifiedTweetIds', [])
    if tweet_id not in ids:
        ids.append(tweet_id)
        save_json(STATE_PATH, state)
    print(json.dumps({'ok': True, 'notified': tweet_id}, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv)
