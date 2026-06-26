"""
微博热搜 — scrapes the public weibo hot-search page, zero API key.

Strategy:
  1. Try the public AJAX endpoint first (fast, returns JSON)
  2. Fall back to HTML scraping if AJAX is blocked
"""

import json
import re
import urllib.request
from datetime import datetime, timezone

_AJAX_URL = "https://weibo.com/ajax/side/hotSearch"
_WEB_URL = "https://s.weibo.com/top/summary"

_HEAT_LABELS = {
    "hot": "热",
    "new": "新",
    "boom": "爆",
    "fei": "沸",
}


def fetch(top: int = 10, timeout: int = 15) -> dict:
    """Fetch hot search topics from Weibo.

    Returns:
        {
            "source": "weibo",
            "label": "微博",
            "emoji": "🔥",
            "fetched_at": <ISO>,
            "items": [{"rank": 1, "title": "...", "url": "...", "heat": "12345678", "label": "热"}, ...]
        }
    """
    result = _try_ajax(top, timeout)
    if result:
        return result

    result = _try_html(top, timeout)
    if result:
        return result

    return _error("All methods failed — Weibo may require login or is rate-limiting")


def _try_ajax(top: int, timeout: int):
    req = urllib.request.Request(_AJAX_URL, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://weibo.com/",
        "X-Requested-With": "XMLHttpRequest",
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    if not data.get("ok"):
        return None

    realtime = data.get("data", {}).get("realtime", [])
    if not realtime:
        return None

    items = []
    for i, entry in enumerate(realtime[:top], 1):
        word = entry.get("word", entry.get("note", ""))
        raw_hot = entry.get("raw_hot", entry.get("num", 0))
        label_key = entry.get("label_name", "")
        label = _HEAT_LABELS.get(label_key, label_key)
        search_word = urllib.request.quote(word, safe="")
        items.append({
            "rank": i,
            "title": word,
            "url": f"https://s.weibo.com/weibo?q=%23{search_word}%23",
            "heat": str(raw_hot),
            "label": label,
        })

    return {
        "source": "weibo",
        "label": "微博",
        "emoji": "🔥",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _try_html(top: int, timeout: int):
    req = urllib.request.Request(_WEB_URL, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": "SUB=_2AkMRqN6sf8NxqwFRmP8RzWnqaI12zwnEieKnQ-VbJRMxHRl-yT9kqhALtRB6Pu4ZCnHUmr8ybaY8z4nPmJNz3ZaWwZ-P",
    })

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    pattern = r'<td class="td-02">\s*<a[^>]*href="(/weibo\?q=[^"]*)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)

    if not matches:
        return None

    items = []
    for i, (href, title) in enumerate(matches[:top], 1):
        items.append({
            "rank": i,
            "title": title.strip(),
            "url": f"https://s.weibo.com{href}",
            "heat": "",
            "label": "",
        })

    return {
        "source": "weibo",
        "label": "微博",
        "emoji": "🔥",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _error(msg: str) -> dict:
    return {
        "source": "weibo",
        "label": "微博",
        "emoji": "🔥",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
