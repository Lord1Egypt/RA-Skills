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
CONFIG_FORMAT_VERSION = 2
# 401/403 临时冷却时间（秒）：不再永久 disable，过期后自动重新探测 key
# 默认 1 小时（3600 秒）。用户反馈：401/403 永久 disable 太激进，
# key 可能因账号改密码、配额月度重置、临时 API 故障后恢复。
AUTH_COOLDOWN_SECONDS = 3600


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


def normalize_key_entry(item):
    if isinstance(item, str):
        return {
            'key': item,
            'account': None,
            'notes': None,
        }
    if isinstance(item, dict):
        key = item.get('key')
        if not key:
            raise ValueError(f'invalid key entry without key: {item!r}')
        return {
            'key': key,
            'account': item.get('account') or item.get('source'),
            'notes': item.get('notes'),
        }
    raise ValueError(f'unsupported key entry: {item!r}')


def config_needs_migration(raw_cfg):
    if raw_cfg.get('format_version') != CONFIG_FORMAT_VERSION:
        return True
    for item in raw_cfg.get('keys', []):
        if isinstance(item, str):
            return True
        if isinstance(item, dict) and 'source' in item:
            return True
    return False


def migrate_config(raw_cfg):
    migrated = {
        'format_version': CONFIG_FORMAT_VERSION,
        'cooldown_minutes': int(raw_cfg.get('cooldown_minutes', 10)),
        'keys': [normalize_key_entry(item) for item in raw_cfg.get('keys', [])],
    }
    save_json(CONFIG, migrated)
    return migrated


def load_config():
    raw_cfg = load_json(CONFIG, {})
    if config_needs_migration(raw_cfg):
        raw_cfg = migrate_config(raw_cfg)
    keys = [normalize_key_entry(item) for item in raw_cfg.get('keys', [])]
    return {
        'format_version': CONFIG_FORMAT_VERSION,
        'cooldown_minutes': int(raw_cfg.get('cooldown_minutes', 10)),
        'keys': keys,
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


def key_value(item):
    return item['key'] if isinstance(item, dict) else item


def key_meta(item):
    if isinstance(item, dict):
        return {
            'account': item.get('account'),
            'notes': item.get('notes'),
        }
    return {'account': None, 'notes': None}


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


def mark_error(cfg, state, idx, msg, disable=False, retry_after_seconds=None):
    """Record an error against state.keys[idx].

    If retry_after_seconds is given (e.g. parsed from Tavily's Retry-After
    header on a 429), use that as the cooldown window. Otherwise fall back
    to cfg['cooldown_minutes'] so the worst case is still bounded — but
    defaulted to 20s when cfg hasn't been configured, instead of the
    previous 10-minute hard floor. Caller is responsible for converting
    header strings to ints before passing.
    """
    state['keys'][idx]['last_error'] = msg
    if disable:
        cd = None
    elif retry_after_seconds is not None and retry_after_seconds > 0:
        cd = (now() + timedelta(seconds=retry_after_seconds)).isoformat(timespec='seconds')
    else:
        minutes = cfg.get('cooldown_minutes', 10)
        if minutes >= 1:
            # Legacy minutes-based config: honour it.
            cd = (now() + timedelta(minutes=minutes)).isoformat(timespec='seconds')
        else:
            # Sub-minute config (e.g. 0.05 = 3s): treat as fractional minutes
            # → use seconds directly so we can express <1 minute cooldowns.
            cd = (now() + timedelta(seconds=minutes * 60)).isoformat(timespec='seconds')
    state['keys'][idx]['cooldown_until'] = cd
    state['keys'][idx]['disabled'] = disable
    save_json(STATE, state)


def mark_success(state, idx):
    state['keys'][idx]['last_error'] = None
    state['keys'][idx]['cooldown_until'] = None
    state['keys'][idx]['disabled'] = False
    save_json(STATE, state)


def choose_key(cfg, state):
    candidates = []
    for i, item in enumerate(cfg['keys']):
        key = key_value(item)
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
    for i, item in enumerate(cfg['keys']):
        key = key_value(item)
        meta = key_meta(item)
        try:
            raw = fetch_usage(key)
            summary = parse_usage_summary(raw)
            update_usage_snapshot(state, i, summary)
            state['keys'][i]['disabled'] = False
            state['keys'][i]['last_error'] = None
            result.append({'index': i, 'key': mask(key), 'ok': True, 'usage': summary, **meta})
        except urllib.error.HTTPError as e:
            msg = f'HTTP {e.code}'
            disable = False  # 401/403 走 1h 临时 cooldown，不永久 disable
            retry_after_seconds = AUTH_COOLDOWN_SECONDS if e.code in (401, 403) else None
            if e.code in (401, 403):
                msg = f'HTTP {e.code} (auth error, retry in 1h)'
            mark_error(cfg, state, i, msg, disable=disable, retry_after_seconds=retry_after_seconds)
            result.append({'index': i, 'key': mask(key), 'ok': False, 'error': msg, 'disabled': disable,
                           'retry_after_seconds': retry_after_seconds, **meta})
        except Exception as e:
            msg = str(e)
            mark_error(cfg, state, i, msg, disable=False)
            result.append({'index': i, 'key': mask(key), 'ok': False, 'error': msg, 'disabled': False, **meta})
    return result


def cmd_status(cfg, state):
    sync_all_usage(cfg, state)
    out = {
        'format_version': cfg.get('format_version', CONFIG_FORMAT_VERSION),
        'month': state['month'],
        'key_count': len(cfg['keys']),
        'keys': []
    }
    for i, item in enumerate(cfg['keys']):
        key = key_value(item)
        meta = key_meta(item)
        st = state['keys'][i]
        usage = st.get('last_usage') or {}
        out['keys'].append({
            'index': i,
            'key': mask(key),
            'account': meta.get('account'),
            'notes': meta.get('notes'),
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
            disable = False  # 401/403 改为临时 cooldown，不再永久 disable（key 可能恢复）
            retry_after_seconds = None
            if e.code == 429:
                ra = e.headers.get('Retry-After') if e.headers else None
                if ra:
                    try:
                        retry_after_seconds = int(ra)
                    except (TypeError, ValueError):
                        pass
                if retry_after_seconds:
                    msg = f'HTTP {e.code} (retry in {retry_after_seconds}s)'
            elif e.code in (401, 403):
                # 401/403 走 1 小时临时 cooldown，过期后 choose_key 会自动重试探测
                retry_after_seconds = AUTH_COOLDOWN_SECONDS
                msg = f'HTTP {e.code} (auth error, retry in 1h)'
            tried.append({'index': idx, 'key': mask(key), 'error': msg, 'disabled': disable,
                          'retry_after_seconds': retry_after_seconds})
            mark_error(cfg, state, idx, msg, disable=disable, retry_after_seconds=retry_after_seconds)
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
