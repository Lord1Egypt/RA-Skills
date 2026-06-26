"""
台灣職籃 — 磁碟 TTL 快取模組
"""

import hashlib
import json
import os
import sys
import time as _time
from pathlib import Path
from typing import Any, Optional

# ─── Debug 模式 ───

_DEBUG: bool = os.environ.get('BASKETBALL_DEBUG', '').lower() in ('1', 'true', 'yes')


def _debug_log(msg: str) -> None:
    """若 BASKETBALL_DEBUG=1 則輸出 debug 訊息至 stderr"""
    if os.environ.get('BASKETBALL_DEBUG', '').lower() in ('1', 'true', 'yes'):
        print(f'[DEBUG] {msg}', file=sys.stderr)


# ─── TTL 快取 ───

_CACHE_DIR = Path.home() / '.cache' / 'taiwan-basketball'
_CACHE_TTL_DEFAULT = 300  # 5 分鐘

# 依資料類型設定 TTL（秒）
CACHE_TTL = {
    'schedule': 300,    # 賽程：5 分鐘
    'games': 600,       # 比賽結果：10 分鐘
    'standings': 600,   # 戰績：10 分鐘
    'player': 3600,     # 球員數據：1 小時
    'leaders': 600,     # 排行榜：10 分鐘
    'live': 60,         # 即時比分：1 分鐘
    'boxscore': 300,    # Box Score：5 分鐘
    'transactions': 3600,  # 交易資訊：1 小時
    'default': 300,
}

_cache_enabled: bool = True


def _cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def _cache_get(key: str) -> Optional[Any]:
    """從磁碟快取讀取，若過期則回傳 None"""
    if not _cache_enabled:
        return None
    cache_file = _CACHE_DIR / f'{key}.json'
    if not cache_file.exists():
        return None
    try:
        data = json.loads(cache_file.read_text(encoding='utf-8'))
        ttl = data.get('ttl', _CACHE_TTL_DEFAULT)
        if _time.time() - data.get('timestamp', 0) < ttl:
            _debug_log(f'Cache hit: {key}')
            return data['value']
        _debug_log(f'Cache expired: {key}')
    except (json.JSONDecodeError, KeyError, OSError):
        pass
    return None


def _cache_set(key: str, value: Any, ttl: int = _CACHE_TTL_DEFAULT) -> None:
    """將資料寫入磁碟快取"""
    if not _cache_enabled:
        return
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = _CACHE_DIR / f'{key}.json'
        cache_file.write_text(
            json.dumps({'timestamp': _time.time(), 'ttl': ttl, 'value': value}, ensure_ascii=False),
            encoding='utf-8',
        )
        _debug_log(f'Cache set: {key} (TTL={ttl}s)')
    except OSError as e:
        _debug_log(f'Cache write failed: {e}')


def disable_cache() -> None:
    """停用快取（CLI --no-cache 旗標使用）"""
    global _cache_enabled
    _cache_enabled = False
