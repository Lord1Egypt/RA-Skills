#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_weibo_hot.py - Fetch Weibo realtime hot searches, normalize, dedup.

Based on the weibo skill (weibo.com/ajax/side/hotSearch desktop AJAX API).
Windows-native: no Unix dependencies, safe file IO for NTFS.

Exit codes:
  0  - Success, hotlist unchanged (dedup).
  42 - Success, hotlist CHANGED (caller should trigger Skill #2).
  1  - Error (network, parse, IO).
"""

import argparse
import hashlib
import json
import os
import sys
import io
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Force UTF-8 output (fixes garbled Chinese in NSSM/PowerShell)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import requests
except ImportError:
    print('[error] requests library not installed. Run: pip install requests',
          file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# HARDCODED: Path.home() under NSSM resolves to SYSTEM profile, not Intel.
STATE_DIR = r'C:\Users\Intel\.openclaw\state\weibo_hot'
HOT_JSON = os.path.join(STATE_DIR, 'hot.json')
HOT_SHA = os.path.join(STATE_DIR, 'hot.sha256')
LAST_FETCH = os.path.join(STATE_DIR, 'last_fetch.txt')
DEBUG_RESP = os.path.join(STATE_DIR, 'debug_response.json')

API_URL = 'https://weibo.com/ajax/side/hotSearch'

DEFAULT_UA = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)
USER_AGENT = os.environ.get('WEIBO_UA', DEFAULT_UA)

MAX_RETRIES = 3
RETRY_CODES = {429, 500, 502, 503, 504}
BACKOFF_BASE = 2  # seconds

DEFAULT_LIMIT = 50

CST = timezone(timedelta(hours=8))

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ensure_state_dir():
    os.makedirs(STATE_DIR, exist_ok=True)


def fetch_raw():
    """Fetch the Weibo AJAX API with retries and exponential backoff.

    Mirrors the error handling from the proven weibo skill (weibo_hot.py).
    """
    headers = {
        'User-Agent': USER_AGENT,
        'Referer': 'https://weibo.com/',
    }
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(API_URL, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if 'data' in data and 'realtime' in data['data']:
                return data
            else:
                # API returned valid JSON but unexpected structure
                # Dump for debugging, then retry
                ensure_state_dir()
                with open(DEBUG_RESP, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                last_err = ValueError('data.realtime missing in response')
                print(
                    f'[retry] Unexpected API structure, saved to debug_response.json '
                    f'(attempt {attempt+1}/{MAX_RETRIES})',
                    file=sys.stderr,
                )
                wait = BACKOFF_BASE ** (attempt + 1)
                time.sleep(wait)
                continue

        except requests.exceptions.HTTPError as e:
            last_err = e
            code = e.response.status_code if e.response else 0
            if code in RETRY_CODES:
                wait = BACKOFF_BASE ** (attempt + 1)
                print(
                    f'[retry] HTTP {code}, waiting {wait}s '
                    f'(attempt {attempt+1}/{MAX_RETRIES})',
                    file=sys.stderr,
                )
                time.sleep(wait)
                continue
            raise
        except requests.RequestException as e:
            last_err = e
            wait = BACKOFF_BASE ** (attempt + 1)
            print(
                f'[retry] Network error: {e}, waiting {wait}s '
                f'(attempt {attempt+1}/{MAX_RETRIES})',
                file=sys.stderr,
            )
            time.sleep(wait)
        except json.JSONDecodeError as e:
            # API returned empty body or HTML — dump raw text for debugging
            last_err = e
            ensure_state_dir()
            try:
                raw_text = response.text[:2000] if response else '(no response)'
                with open(DEBUG_RESP, 'w', encoding='utf-8') as f:
                    f.write(raw_text)
            except Exception:
                pass
            wait = BACKOFF_BASE ** (attempt + 1)
            print(
                f'[retry] JSON decode error: {e}, waiting {wait}s '
                f'(attempt {attempt+1}/{MAX_RETRIES})',
                file=sys.stderr,
            )
            time.sleep(wait)
    raise RuntimeError(f'Failed after {MAX_RETRIES} retries: {last_err}')


def parse_items(data, limit=DEFAULT_LIMIT):
    """Extract hot search items from API response.

    API response shape (already validated by fetch_raw):
      { "data": { "realtime": [ { "word": ..., "num": ..., "category": ... }, ... ] } }
    """
    realtime = data['data']['realtime'][:limit]
    items = []
    seen_titles = set()
    for idx, item in enumerate(realtime):
        word = (item.get('word') or '').strip()
        if not word or word in seen_titles:
            continue
        seen_titles.add(word)

        num = item.get('num', 0)
        category = (item.get('category') or '').strip()
        # Build a search URL from the word
        search_url = f'https://s.weibo.com/weibo?q=%23{requests.utils.quote(word)}%23'

        items.append({
            'rank': idx + 1,
            'title': word,
            'hot': num if isinstance(num, int) else 0,
            'category': category,
            'url': search_url,
        })
    return items


def canonical_json(obj):
    """Deterministic JSON string for hashing."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def sha256_hex(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return ''


def safe_replace(src, dst):
    """Atomic-ish file replace that works on Windows NTFS."""
    if os.path.exists(dst):
        bak = dst + '.bak'
        try:
            if os.path.exists(bak):
                os.remove(bak)
            os.rename(dst, bak)
        except OSError:
            os.remove(dst)
    os.rename(src, dst)


def write_file(path, content):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(content)
    safe_replace(tmp, path)


def write_json_file(path, obj):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    safe_replace(tmp, path)


def format_hot_list(items):
    """Format hot list for console display (matches weibo skill style)."""
    if not items:
        return 'No hot search data.'
    lines = ['\U0001f525 ' + chr(0x5fae) + chr(0x535a) + chr(0x70ed) + chr(0x641c) + chr(0x699c),
             chr(0x2500) * 50]
    for item in items:
        rank = item['rank']
        title = item['title']
        hot = item['hot']
        hot_str = f'{hot:,}' if isinstance(hot, int) else str(hot)
        lines.append(f'{rank:2d}. {title:<30} \U0001f525 {hot_str}')
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Fetch Weibo hot searches')
    parser.add_argument('-l', '--limit', type=int, default=DEFAULT_LIMIT,
                        help=f'Number of items to fetch (default: {DEFAULT_LIMIT})')
    parser.add_argument('--raw', action='store_true',
                        help='Output raw JSON data')
    args = parser.parse_args()

    ensure_state_dir()

    print('[fetch] Requesting Weibo hot search API...')
    data = fetch_raw()

    items = parse_items(data, limit=args.limit)
    if not items:
        print('[warn] No items parsed from API response.', file=sys.stderr)
        sys.exit(1)

    print(f'[fetch] Parsed {len(items)} hot search items.')

    # If --raw, just dump and exit (no state management)
    if args.raw:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        sys.exit(0)

    now = datetime.now(CST).isoformat()
    hot_obj = {
        'fetched_at': now,
        'source': 'weibo.com',
        'items': items,
    }

    # Dedup check: hash only the title+hot pairs (ignore url which may vary)
    dedup_payload = [{'title': it['title'], 'hot': it['hot']} for it in items]
    new_hash = sha256_hex(canonical_json(dedup_payload))
    old_hash = read_file(HOT_SHA)

    if new_hash == old_hash:
        print('[dedup] no change')
        write_file(LAST_FETCH, now)
        sys.exit(0)

    # Hotlist changed - write state files
    write_json_file(HOT_JSON, hot_obj)
    write_file(HOT_SHA, new_hash)
    write_file(LAST_FETCH, now)
    print(f'[fetch] Hotlist updated. New hash: {new_hash[:16]}...')

    # Print formatted list
    print()
    print(format_hot_list(items))

    # Exit 42 signals "changed" to the scheduler / runner wrapper
    sys.exit(42)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'[error] {e}', file=sys.stderr)
        sys.exit(1)
