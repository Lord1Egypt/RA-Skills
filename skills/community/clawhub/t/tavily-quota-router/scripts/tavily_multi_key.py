#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CONFIG = BASE / 'config' / 'keys.json'
STATE = BASE / 'state' / 'quota.json'
SEARCH_URL = 'https://api.tavily.com/search'
USAGE_URL = 'https://api.tavily.com/usage'


def now():
    return datetime.now()


def current_month():
    return now().strftime('%Y-%m')


def load_json(path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def load_config():
    cfg = load_json(CONFIG, {})
    return {
        'cooldown_minutes': int(cfg.get('cooldown_minutes', 10)),
        'keys': list(cfg.get('keys', [])),
    }


def normalize_state(cfg):
    state = load_json(STATE, {'month': '', 'keys': []})
    month = current_month()
    if state.get('month') != month:
        state = {'month': month, 'keys': []}
    keys_state = state.get('keys', [])
    norm = []
    for i, _key in enumerate(cfg['keys']):
        old = keys_state[i] if i < len(keys_state) and isinstance(keys_state[i], dict) else {}
        norm.append({
            'last_error': old.get('last_error'),
            'cooldown_until': old.get('cooldown_until'),
            'last_usage': old.get('last_usage'),
            'last_sync_at': old.get('last_sync_at'),
            'disabled': bool(old.get('disabled', False))
        })
    state['keys'] = norm
    return state


def is_cooled(st):
    v = st.get('cooldown_until')
    if not v:
        return False
    try:
        return now() < datetime.fromisoformat(v)
    except Exception:
        return False


def mask(k):
    if len(k) <= 12:
        return k[:3] + '***'
    return k[:8] + '...' + k[-4:]


def fetch_usage(api_key):
    req = urllib.request.Request(USAGE_URL, headers={'Authorization': f'Bearer {api_key}'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def parse_usage_summary(data):
    key_usage = data.get('key', {}) if isinstance(data, dict) else {}
    account = data.get('account', {}) if isinstance(data, dict) else {}
    return {
        'key_usage': key_usage.get('usage'),
        'search_usage': key_usage.get('search_usage'),
        'crawl_usage': key_usage.get('crawl_usage'),
        'extract_usage': key_usage.get('extract_usage'),
        'map_usage': key_usage.get('map_usage'),
        'research_usage': key_usage.get('research_usage'),
        'plan_name': account.get('current_plan'),
        'plan_usage': account.get('plan_usage'),
        'plan_limit': account.get('plan_limit')
    }


def usage_remaining(summary):
    limit_ = summary.get('plan_limit')
    usage = summary.get('plan_usage')
    if isinstance(limit_, int) and isinstance(usage, int):
        return max(0, limit_ - usage)
    return None


def update_usage_snapshot(state, idx, usage_data):
    state['keys'][idx]['last_usage'] = usage_data
    state['keys'][idx]['last_sync_at'] = now().isoformat(timespec='seconds')
    save_json(STATE, state)


def mark_error(cfg, state, idx, msg, disable=False):
    state['keys'][idx]['last_error'] = msg
    state['keys'][idx]['cooldown_until'] = None if disable else (now() + timedelta(minutes=cfg['cooldown_minutes'])).isoformat(timespec='seconds')
    state['keys'][idx]['disabled'] = disable
    save_json(STATE, state)


def mark_success(state, idx):
    state['keys'][idx]['last_error'] = None
    state['keys'][idx]['cooldown_until'] = None
    state['keys'][idx]['disabled'] = False
    save_json(STATE, state)


def choose_key(cfg, state):
    candidates = []
    for i, key in enumerate(cfg['keys']):
        st = state['keys'][i]
        if st.get('disabled'):
            continue
        if is_cooled(st):
            continue
        usage = st.get('last_usage') or {}
        remaining = usage_remaining(usage)
        if remaining is not None and remaining <= 0:
            continue
        sort_remaining = remaining if remaining is not None else 10**9
        search_usage = usage.get('search_usage')
        sort_usage = search_usage if isinstance(search_usage, int) else 10**9
        candidates.append((-sort_remaining, sort_usage, i, key))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))
    _, _, idx, key = candidates[0]
    return idx, key


def do_search_with_key(api_key, query, count):
    payload = json.dumps({
        'api_key': api_key,
        'query': query,
        'max_results': count
    }).encode('utf-8')
    req = urllib.request.Request(SEARCH_URL, data=payload, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def sync_all_usage(cfg, state):
    result = []
    for i, key in enumerate(cfg['keys']):
        try:
            raw = fetch_usage(key)
            summary = parse_usage_summary(raw)
            update_usage_snapshot(state, i, summary)
            state['keys'][i]['disabled'] = False
            state['keys'][i]['last_error'] = None
            result.append({'index': i, 'key': mask(key), 'ok': True, 'usage': summary})
        except urllib.error.HTTPError as e:
            msg = f'HTTP {e.code}'
            disable = e.code in (401, 403)
            mark_error(cfg, state, i, msg, disable=disable)
            result.append({'index': i, 'key': mask(key), 'ok': False, 'error': msg, 'disabled': disable})
        except Exception as e:
            msg = str(e)
            mark_error(cfg, state, i, msg, disable=False)
            result.append({'index': i, 'key': mask(key), 'ok': False, 'error': msg, 'disabled': False})
    return result


def cmd_status(cfg, state):
    sync_all_usage(cfg, state)
    out = {
        'month': state['month'],
        'key_count': len(cfg['keys']),
        'keys': []
    }
    for i, key in enumerate(cfg['keys']):
        st = state['keys'][i]
        usage = st.get('last_usage') or {}
        out['keys'].append({
            'index': i,
            'key': mask(key),
            'disabled': st.get('disabled', False),
            'cooldown_until': st.get('cooldown_until'),
            'last_error': st.get('last_error'),
            'last_sync_at': st.get('last_sync_at'),
            'search_usage': usage.get('search_usage'),
            'key_usage': usage.get('key_usage'),
            'plan_name': usage.get('plan_name'),
            'plan_usage': usage.get('plan_usage'),
            'plan_limit': usage.get('plan_limit'),
            'plan_remaining': usage_remaining(usage)
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_reset_month(cfg):
    state = {'month': current_month(), 'keys': [{'last_error': None, 'cooldown_until': None, 'last_usage': None, 'last_sync_at': None, 'disabled': False} for _ in cfg['keys']]}
    save_json(STATE, state)
    print(json.dumps({'ok': True, 'message': 'local state reset', 'month': state['month']}, ensure_ascii=False))


def cmd_test_keys(cfg, state):
    if not cfg['keys']:
        print(json.dumps({
            'ok': False,
            'error': 'no keys configured',
            'config': str(CONFIG),
            'example': str(BASE / 'config' / 'keys.example.json')
        }, ensure_ascii=False, indent=2))
        return
    result = sync_all_usage(cfg, state)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search(cfg, state, query, count):
    if not cfg['keys']:
        print(json.dumps({'ok': False, 'error': 'no keys configured', 'config': str(CONFIG)}, ensure_ascii=False))
        sys.exit(2)

    sync_all_usage(cfg, state)
    tried = []
    while True:
        picked = choose_key(cfg, state)
        if not picked:
            print(json.dumps({'ok': False, 'error': 'no available key', 'tried': tried}, ensure_ascii=False, indent=2))
            sys.exit(3)
        idx, key = picked
        try:
            data = do_search_with_key(key, query, count)
            mark_success(state, idx)
            try:
                raw_usage = fetch_usage(key)
                update_usage_snapshot(state, idx, parse_usage_summary(raw_usage))
            except Exception:
                pass
            print(json.dumps({
                'ok': True,
                'provider': 'tavily-multi-key',
                'key_index': idx,
                'key': mask(key),
                'usage': state['keys'][idx].get('last_usage'),
                'results': data.get('results', []),
                'answer': data.get('answer')
            }, ensure_ascii=False, indent=2))
            return
        except urllib.error.HTTPError as e:
            msg = f'HTTP {e.code}'
            disable = e.code in (401, 403)
            tried.append({'index': idx, 'key': mask(key), 'error': msg, 'disabled': disable})
            mark_error(cfg, state, idx, msg, disable=disable)
        except Exception as e:
            msg = str(e)
            tried.append({'index': idx, 'key': mask(key), 'error': msg, 'disabled': False})
            mark_error(cfg, state, idx, msg, disable=False)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd', required=True)

    sub.add_parser('status')
    sub.add_parser('test-keys')
    sub.add_parser('reset-month')

    s = sub.add_parser('search')
    s.add_argument('--query', required=True)
    s.add_argument('--count', type=int, default=5)

    args = parser.parse_args()
    cfg = load_config()
    state = normalize_state(cfg)
    save_json(STATE, state)

    if args.cmd == 'status':
        cmd_status(cfg, state)
    elif args.cmd == 'test-keys':
        cmd_test_keys(cfg, state)
    elif args.cmd == 'reset-month':
        cmd_reset_month(cfg)
    elif args.cmd == 'search':
        cmd_search(cfg, state, args.query, args.count)


if __name__ == '__main__':
    main()
