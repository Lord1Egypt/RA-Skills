"""
台灣職籃 — HTTP 請求工具模組
支援快取、指數退避重試
"""

import json
import time as _time
import urllib.error
import urllib.request
from typing import Any, Optional

from _cache import _cache_key, _cache_get, _cache_set, _debug_log, _CACHE_TTL_DEFAULT

_UA = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/131.0.0.0 Safari/537.36'
)
_FETCH_RETRIES = 3           # 最多重試次數
_FETCH_BACKOFF_BASE = 1.5    # 退避基數（秒）


def _fetch_html(url: str, ttl: int = _CACHE_TTL_DEFAULT) -> str:
    """用 urllib 抓 HTML，支援快取與指數退避重試"""
    key = _cache_key(url)
    cached = _cache_get(key)
    if cached is not None:
        return cached

    _debug_log(f'GET {url}')
    last_err: Exception = RuntimeError('No attempts made')
    for attempt in range(_FETCH_RETRIES):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': _UA})
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='replace')
            _cache_set(key, html, ttl)
            return html
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last_err = e
            if attempt < _FETCH_RETRIES - 1:
                wait = _FETCH_BACKOFF_BASE ** attempt
                _debug_log(
                    f'Request failed ({e}), retrying in {wait:.1f}s… '
                    f'(attempt {attempt + 1}/{_FETCH_RETRIES})'
                )
                _time.sleep(wait)
    raise urllib.error.URLError(f'Failed after {_FETCH_RETRIES} attempts: {last_err}')


def _fetch_json_url(
    url: str,
    headers: Optional[dict] = None,
    ttl: int = _CACHE_TTL_DEFAULT,
) -> Any:
    """用 urllib 抓 JSON，支援快取與指數退避重試"""
    key = _cache_key(url)
    cached = _cache_get(key)
    if cached is not None:
        return cached

    _debug_log(f'GET (JSON) {url}')
    req = urllib.request.Request(url)
    req.add_header('User-Agent', _UA)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    last_err: Exception = RuntimeError('No attempts made')
    for attempt in range(_FETCH_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
            _cache_set(key, data, ttl)
            return data
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            last_err = e
            if attempt < _FETCH_RETRIES - 1:
                wait = _FETCH_BACKOFF_BASE ** attempt
                _debug_log(
                    f'Request failed ({e}), retrying in {wait:.1f}s… '
                    f'(attempt {attempt + 1}/{_FETCH_RETRIES})'
                )
                _time.sleep(wait)
        except json.JSONDecodeError as e:
            raise ValueError(f'Invalid JSON from {url}: {e}') from e
    raise urllib.error.URLError(f'Failed after {_FETCH_RETRIES} attempts: {last_err}')
