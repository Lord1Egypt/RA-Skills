#!/usr/bin/env python3
import sys
import json
import ssl
import ipaddress
import urllib.parse
import urllib.request
from typing import Dict, Tuple

TIMEOUT = 30
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 SafeSmartWebFetch/1.0'

SENSITIVE_KEYS = {
    'token', 'access_token', 'auth', 'authorization', 'apikey', 'api_key', 'key',
    'signature', 'sig', 'session', 'sessionid', 'code', 'state', 'secret', 'password',
    'passwd', 'jwt', 'bearer'
}

PRIVATE_PATH_HINTS = [
    '/login', '/signin', '/auth', '/oauth', '/callback', '/reset', '/admin',
    '/dashboard', '/settings', '/account', '/console'
]

ssl_context = ssl.create_default_context()


def is_private_host(host: str) -> bool:
    if not host:
        return True
    h = host.lower().strip('[]')
    if h in {'localhost'} or h.endswith('.local'):
        return True
    try:
        ip = ipaddress.ip_address(h)
        return ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
    except ValueError:
        pass
    if re_private_name(h):
        return True
    return False


def re_private_name(host: str) -> bool:
    # 没有公共后缀、像局域网主机名一样的短名，保守按私有处理
    return '.' not in host or host.endswith('.lan') or host.endswith('.home') or host.endswith('.internal')


def has_sensitive_query(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    frag = parsed.fragment.lower()
    for k, v in params:
        lk = k.lower()
        lv = (v or '').lower()
        if lk in SENSITIVE_KEYS:
            return True
        if any(s in lk for s in SENSITIVE_KEYS):
            return True
        if len(v) > 20 and any(x in lk for x in ['token', 'code', 'sig', 'key', 'auth']):
            return True
        if 'bearer' in lv:
            return True
    if any(x in frag for x in ['access_token', 'token=', 'session=', 'code=']):
        return True
    return False


def looks_private_link(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    path = (parsed.path or '').lower()
    if any(hint in path for hint in PRIVATE_PATH_HINTS):
        return True
    if has_sensitive_query(url):
        return True
    return False


def classify_url(url: str) -> Tuple[bool, str]:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        return False, 'non-http-url'
    host = parsed.hostname or ''
    if is_private_host(host):
        return False, 'private-or-local-host'
    if looks_private_link(url):
        return False, 'sensitive-or-private-link'
    return True, ''


def fetch_url(url: str, timeout: int = TIMEOUT) -> Dict:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
        content = response.read().decode('utf-8', errors='ignore')
        return {'success': response.status == 200, 'content': content, 'status': response.status}


def clean_service_urls(original_url: str):
    stripped = original_url.replace('https://', '').replace('http://', '')
    return [
        ('jina', f'https://r.jina.ai/http://{stripped}'),
        ('markdown-new', f'https://markdown.new/{original_url}'),
        ('defuddle', f'https://defuddle.md/{original_url}'),
    ]


def get_content(url: str) -> Dict:
    allow_third_party, blocked_reason = classify_url(url)

    if allow_third_party:
        for source, clean_url in clean_service_urls(url):
            try:
                result = fetch_url(clean_url)
                if result['success'] and len(result['content']) > 100:
                    return {
                        'success': True,
                        'url': clean_url,
                        'content': result['content'],
                        'source': source,
                        'used_third_party': True,
                        'blocked_reason': None,
                        'error': None,
                    }
            except Exception:
                pass

    try:
        result = fetch_url(url)
        if result['success']:
            return {
                'success': True,
                'url': url,
                'content': result['content'],
                'source': 'original',
                'used_third_party': False,
                'blocked_reason': blocked_reason or None,
                'error': None,
            }
    except Exception as e:
        return {
            'success': False,
            'url': url,
            'content': '',
            'source': 'none',
            'used_third_party': False,
            'blocked_reason': blocked_reason or None,
            'error': str(e),
        }

    return {
        'success': False,
        'url': url,
        'content': '',
        'source': 'none',
        'used_third_party': False,
        'blocked_reason': blocked_reason or None,
        'error': 'all fetch strategies failed',
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: fetch.py <url> [--json]', file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    as_json = '--json' in sys.argv
    result = get_content(url)
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result['success']:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(f"# Source: {result['source']}")
        print(f"# URL: {result['url']}")
        print(f"# Third-party: {str(result['used_third_party']).lower()}")
        if result['blocked_reason']:
            print(f"# Blocked-Reason: {result['blocked_reason']}")
        print()
        print(result['content'])


if __name__ == '__main__':
    main()
