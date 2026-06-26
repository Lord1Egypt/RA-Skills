#!/usr/bin/env python3
"""
search_cache.py
~~~~~~~~~~~~~~~
基于 payload hash 的搜索结果缓存，TTL 3 分钟。

缓存路径：/tmp/woto_search_cache/
每个缓存项为 {key}.json，内容为完整的 search_output dict。

TTL 通过 mtime 判定，无需维护独立的过期时间。
"""
from __future__ import annotations

from typing import Optional

import hashlib
import json
import os
import time
from pathlib import Path

try:
    from config import CACHE_TTL_SECONDS
except ImportError:
    CACHE_TTL_SECONDS: int = 180

CACHE_DIR: str = "/tmp/woto_search_cache"
os.makedirs(CACHE_DIR, exist_ok=True)


# ── key 生成 ─────────────────────────────────────────────────────────────────

def _cache_key(payload: dict, token: Optional[str]) -> str:
    """对 payload + token 生成短 hash（取前16位）。"""
    data = json.dumps(payload, sort_keys=True, ensure_ascii=False) + (token or "")
    return hashlib.sha256(data.encode()).hexdigest()[:16]


# ── 缓存读写 ─────────────────────────────────────────────────────────────────

def cache_get(payload: dict, token: Optional[str]) -> Optional[dict]:
    """
    若缓存命中且未过期，返回缓存的 search_output dict。
    否则返回 None（过期或不存在均删除缓存文件）。
    """
    key = _cache_key(payload, token)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if not os.path.exists(path):
        return None

    mtime = os.path.getmtime(path)
    if time.time() - mtime > CACHE_TTL_SECONDS:
        try:
            os.unlink(path)
        except OSError:
            pass
        return None

    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)   # type: ignore[no-any-return]
    except Exception:
        try:
            os.unlink(path)
        except OSError:
            pass
        return None


def cache_set(payload: dict, token: Optional[str], data: dict) -> None:
    """将 search_output 写入缓存文件。"""
    key = _cache_key(payload, token)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass


def cache_clear() -> int:
    """清空所有缓存文件，返回删除数量。"""
    count = 0
    if os.path.isdir(CACHE_DIR):
        for fname in os.listdir(CACHE_DIR):
            if fname.endswith(".json"):
                try:
                    os.unlink(os.path.join(CACHE_DIR, fname))
                    count += 1
                except OSError:
                    pass
    return count
