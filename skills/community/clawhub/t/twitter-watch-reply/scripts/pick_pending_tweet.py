#!/usr/bin/env python3
from __future__ import annotations
import json
from common import STATE_PATH, load_json


def main():
    state = load_json(STATE_PATH, {})
    pending = state.get('pendingTweets', [])
    if not pending:
        print(json.dumps({'ok': True, 'pending': None}, ensure_ascii=False))
        return
    print(json.dumps({'ok': True, 'pending': pending[0]}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
