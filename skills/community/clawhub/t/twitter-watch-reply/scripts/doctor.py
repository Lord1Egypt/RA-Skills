#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, urllib.request, urllib.error
from common import DATA_DIR, CONFIG_PATH, STATE_PATH, EXAMPLE_PATH, ensure_data_dir, load_json

INFO_URL = 'https://ai.6551.io/open/twitter_user_info'


def ok(name, detail=None):
    return {'check': name, 'ok': True, 'detail': detail}


def bad(name, detail=None):
    return {'check': name, 'ok': False, 'detail': detail}


def check_token():
    token = os.environ.get('TWITTER_TOKEN')
    if not token:
        return bad('TWITTER_TOKEN', 'missing; get one from https://6551.io/mcp and export TWITTER_TOKEN in the same runtime environment')
    return ok('TWITTER_TOKEN', 'present')


def check_paths():
    ensure_data_dir()
    return ok('paths', {
        'dataDir': str(DATA_DIR),
        'configExists': CONFIG_PATH.exists(),
        'stateExists': STATE_PATH.exists(),
        'exampleExists': EXAMPLE_PATH.exists(),
    })


def check_config_json():
    if not CONFIG_PATH.exists():
        return bad('config.json', 'missing; run watch_state.py init first')
    try:
        cfg = load_json(CONFIG_PATH, {})
    except Exception as e:
        return bad('config.json', f'invalid json: {e}')
    authors = cfg.get('authors', [])
    return ok('config.json', {'authorsCount': len(authors), 'authors': authors[:10]})


def check_state_json():
    if not STATE_PATH.exists():
        return bad('state.json', 'missing; run watch_state.py init first')
    try:
        state = load_json(STATE_PATH, {})
    except Exception as e:
        return bad('state.json', f'invalid json: {e}')
    return ok('state.json', {
        'seenTweetIds': len(state.get('seenTweetIds', [])),
        'pendingTweets': len(state.get('pendingTweets', [])),
        'replyLog': len(state.get('replyLog', [])),
    })


def check_6551_connectivity(sample_user='elonmusk'):
    token = os.environ.get('TWITTER_TOKEN')
    if not token:
        return bad('6551_connectivity', 'skipped: TWITTER_TOKEN missing')
    payload = {'username': sample_user}
    req = urllib.request.Request(INFO_URL, data=json.dumps(payload).encode('utf-8'), method='POST')
    req.add_header('Authorization', f'Bearer {token}')
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode('utf-8', 'replace')
            data = json.loads(body)
            screen_name = (((data or {}).get('data') or {}).get('screenName'))
            return ok('6551_connectivity', {'http': resp.status, 'sampleUser': screen_name or sample_user})
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')[:300]
        return bad('6551_connectivity', {'http': e.code, 'body': body})
    except Exception as e:
        return bad('6551_connectivity', repr(e))


def main():
    checks = [
        check_token(),
        check_paths(),
        check_config_json(),
        check_state_json(),
        check_6551_connectivity(),
    ]
    overall = all(c.get('ok') for c in checks)
    print(json.dumps({'ok': overall, 'checks': checks}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if overall else 1)


if __name__ == '__main__':
    main()
