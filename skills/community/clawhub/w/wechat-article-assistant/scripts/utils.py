#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared helpers for the WeChat Article Assistant skill."""

from __future__ import annotations

import hashlib
import json
import re
import time
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Iterable


def now_ts() -> int:
    return int(time.time())


def format_timestamp(timestamp: int | None) -> str:
    if not timestamp:
        return ""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(value: str, fallback: str = "untitled", limit: int = 120) -> str:
    cleaned = re.sub(r"[<>:\"/\\|?*\x00-\x1F]+", "_", (value or "").strip())
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ._")
    if not cleaned:
        cleaned = fallback
    return cleaned[:limit].rstrip(" ._") or fallback


def stable_hash(value: str, length: int = 12) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:length]


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)


def write_json(path: Path, data: Any) -> Path:
    path.write_text(json_dumps(data), encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    raise ValueError(f"无法解析布尔值: {value}")


def success(data: Any, formatted_text: str = "") -> dict[str, Any]:
    return {
        "success": True,
        "data": data,
        "formatted_text": formatted_text,
    }


def failure(error: str, data: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "success": False,
        "error": error,
        "formatted_text": error,
    }
    if data is not None:
        payload["data"] = data
    return payload


def cookie_entities_to_header(cookies: Iterable[dict[str, Any]]) -> str:
    parts: list[str] = []
    for item in cookies:
        name = str(item.get("name") or "").strip()
        value = str(item.get("value") or "").strip()
        if not name or not value or value == "EXPIRED":
            continue
        parts.append(f"{name}={value}")
    return "; ".join(parts)


def cookiejar_to_entities(cookiejar: Any) -> list[dict[str, Any]]:
    entities: list[dict[str, Any]] = []
    for cookie in cookiejar:
        entities.append(
            {
                "name": cookie.name,
                "value": cookie.value,
                "domain": cookie.domain,
                "path": cookie.path,
                "expires": cookie.expires,
                "secure": bool(cookie.secure),
            }
        )
    return entities


def min_cookie_expiry(cookies: Iterable[dict[str, Any]]) -> int | None:
    candidates: list[int] = []
    for item in cookies:
        expires = item.get("expires") or item.get("expires_timestamp")
        if expires:
            if isinstance(expires, str) and not expires.isdigit():
                expires_int = int(parsedate_to_datetime(expires).timestamp())
            else:
                expires_int = int(expires)
                if expires_int > 10_000_000_000:
                    expires_int = expires_int // 1000
            candidates.append(expires_int)
    return min(candidates) if candidates else None


def normalize_mp_article_url(url: str) -> str:
    value = (url or "").strip()
    if not value:
        raise ValueError("缺少公众号文章链接")
    if not value.startswith(("http://", "https://")):
        value = f"https://{value}"
    return value


def normalize_mp_article_short_url(url: str) -> str:
    value = normalize_mp_article_url(url)
    match = re.search(r"https?://mp\.weixin\.qq\.com/s/[^\s?#]+", value, re.IGNORECASE)
    if match:
        return match.group(0)
    return value


def article_identity_from_link(link: str) -> dict[str, str]:
    from urllib.parse import parse_qs, urlparse

    parsed = urlparse(link)
    query = parse_qs(parsed.query)
    biz = (query.get("__biz") or ["SINGLE_ARTICLE_FAKEID"])[0]
    mid = (query.get("mid") or query.get("appmsgid") or ["0"])[0]
    idx = (query.get("idx") or query.get("itemidx") or ["1"])[0]
    aid = f"{mid}_{idx}" if mid and mid != "0" else f"single_{stable_hash(link, 16)}"
    return {
        "fakeid": biz,
        "aid": aid,
        "mid": mid,
        "idx": idx,
    }
