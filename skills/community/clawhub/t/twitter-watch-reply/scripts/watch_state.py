#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from common import DATA_DIR, CONFIG_PATH, STATE_PATH, EXAMPLE_PATH, ensure_data_dir, load_json, save_json


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_files():
    ensure_data_dir()
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text(EXAMPLE_PATH.read_text(encoding='utf-8'), encoding='utf-8')
    if not STATE_PATH.exists():
        save_json(STATE_PATH, {
            'seenTweetIds': [],
            'replyLog': [],
            'pendingTweets': [],
            'notifiedTweetIds': [],
            'lastCheckedAt': None,
            'lastCheckedByAuthor': {}
        })
    print(json.dumps({'ok': True, 'dataDir': str(DATA_DIR), 'config': str(CONFIG_PATH), 'state': str(STATE_PATH)}, ensure_ascii=False))


def show_config():
    print(CONFIG_PATH.read_text(encoding='utf-8'))


def list_authors():
    cfg = load_json(CONFIG_PATH, {})
    print('\n'.join(cfg.get('authors', [])))


def add_author(author: str):
    cfg = load_json(CONFIG_PATH, {})
    authors = cfg.setdefault('authors', [])
    if author not in authors:
        authors.append(author)
    save_json(CONFIG_PATH, cfg)
    print(json.dumps({'ok': True, 'authors': authors}, ensure_ascii=False))


def remove_author(author: str):
    cfg = load_json(CONFIG_PATH, {})
    authors = cfg.setdefault('authors', [])
    cfg['authors'] = [a for a in authors if a != author]
    save_json(CONFIG_PATH, cfg)
    print(json.dumps({'ok': True, 'authors': cfg['authors']}, ensure_ascii=False))


def seen(tweet_id: str):
    state = load_json(STATE_PATH, {})
    ids = state.setdefault('seenTweetIds', [])
    if tweet_id not in ids:
        ids.append(tweet_id)
    state['lastCheckedAt'] = now_iso()
    save_json(STATE_PATH, state)
    print(json.dumps({'ok': True, 'seen': tweet_id}, ensure_ascii=False))


def was_seen(tweet_id: str):
    state = load_json(STATE_PATH, {})
    print('true' if tweet_id in state.get('seenTweetIds', []) else 'false')


def usage():
    print('Usage: watch_state.py init|show-config|list-authors|add-author <handle>|remove-author <handle>|seen <tweet_id>|was-seen <tweet_id>')
    raise SystemExit(1)


def main(argv: list[str]):
    if len(argv) < 2:
        usage()
    cmd = argv[1]
    if cmd == 'init':
        init_files()
    elif cmd == 'show-config':
        show_config()
    elif cmd == 'list-authors':
        list_authors()
    elif cmd == 'add-author' and len(argv) >= 3:
        add_author(argv[2])
    elif cmd == 'remove-author' and len(argv) >= 3:
        remove_author(argv[2])
    elif cmd == 'seen' and len(argv) >= 3:
        seen(argv[2])
    elif cmd == 'was-seen' and len(argv) >= 3:
        was_seen(argv[2])
    else:
        usage()

if __name__ == '__main__':
    main(sys.argv)
