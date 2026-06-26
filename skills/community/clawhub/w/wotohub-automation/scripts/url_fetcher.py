#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional

import os
import time

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:  # pragma: no cover - runtime dependency guard
    requests = None
    HTTPAdapter = None
    Retry = None

_HEADER_PROFILES = [
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept-Language': 'en-US,en;q=0.9',
    },
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'en-US,en;q=0.9',
    },
]


def _require_requests():
    if requests is None:
        raise RuntimeError(
            "URL fetching requires the optional dependency 'requests'. "
            "Please install it with: pip install requests"
        )


def _create_session(retries: int = 2):
    _require_requests()
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=['GET']
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def fetch_url_text(url: str, timeout: int = 12, retries: int = 2, verify_tls: Optional[bool]= None) -> dict:
    session = _create_session(retries)
    last_exc = None
    if verify_tls is None:
        verify_tls = os.environ.get('WOTOHUB_INSECURE_FETCH', '').strip().lower() not in {'1', 'true', 'yes'}

    for attempt in range(retries + 1):
        profile = _HEADER_PROFILES[min(attempt, len(_HEADER_PROFILES) - 1)]
        headers = {
            'User-Agent': profile['User-Agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': profile['Accept-Language'],
            'Accept-Encoding': 'gzip, deflate',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Referer': url,
        }
        try:
            resp = session.get(url, headers=headers, timeout=timeout, verify=verify_tls, allow_redirects=True)
            resp.raise_for_status()
            html = resp.text
            session.close()
            return {
                'url': url,
                'finalUrl': resp.url,
                'statusCode': resp.status_code,
                'contentType': resp.headers.get('Content-Type', ''),
                'contentLength': len(html or ''),
                'html': html,
                'attempt': attempt + 1,
                'headerProfile': attempt,
            }
        except requests.exceptions.RequestException as e:
            last_exc = e
            if attempt < retries:
                time.sleep(2 ** attempt)
            continue

    session.close()
    raise last_exc


def strip_html(html: str) -> str:
    import re
    html = re.sub(r'(?is)<script[^>]*>.*?</script>', ' ', html)
    html = re.sub(r'(?is)<style[^>]*>.*?</style>', ' ', html)
    html = re.sub(r'(?is)<noscript[^>]*>.*?</noscript>', ' ', html)
    html = re.sub(r'(?i)<br\s*/?>', '\n', html)
    html = re.sub(r'(?i)</p\s*>', '\n', html)
    html = re.sub(r'(?i)</div\s*>', '\n', html)
    text = re.sub(r'(?s)<[^>]+>', ' ', html)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
