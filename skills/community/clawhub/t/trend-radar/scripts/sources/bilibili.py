"""
Bilibili 综合热门 — multiple API strategies, zero API key.

Strategies:
  1. Popular ranking API (may require Wbi signature in newer versions)
  2. Popular series API (simpler, less restrictive)
  3. Hot search word list (as fallback)
"""

import json
import urllib.request
from datetime import datetime, timezone

_RANKING_URL = "https://api.bilibili.com/x/web-interface/ranking/v2"
_POPULAR_URL = "https://api.bilibili.com/x/web-interface/popular?ps={ps}&pn=1"
_HOT_SEARCH_URL = "https://s.search.bilibili.com/main/suggest?term=&main_ver=v1"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.bilibili.com",
    "Origin": "https://www.bilibili.com",
}


def fetch(top: int = 10, timeout: int = 15) -> dict:
    """Fetch hot videos/topics from Bilibili."""
    result = _try_popular(top, timeout)
    if result:
        return result

    result = _try_ranking(top, timeout)
    if result:
        return result

    result = _try_hot_search(top, timeout)
    if result:
        return result

    return _error("All Bilibili methods failed — API may have changed")


def _try_ranking(top, timeout):
    req = urllib.request.Request(_RANKING_URL, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    if data.get("code", -1) != 0:
        return None

    video_list = data.get("data", {}).get("list", [])
    if not video_list:
        return None

    return _build_video_result(video_list, top)


def _try_popular(top, timeout):
    url = _POPULAR_URL.format(ps=min(top, 20))
    req = urllib.request.Request(url, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    if data.get("code", -1) != 0:
        return None

    video_list = data.get("data", {}).get("list", [])
    if not video_list:
        return None

    return _build_video_result(video_list, top)


def _build_video_result(video_list, top):
    items = []
    for i, v in enumerate(video_list[:top], 1):
        stat = v.get("stat", {})
        bvid = v.get("bvid", "")
        items.append({
            "rank": i,
            "title": v.get("title", ""),
            "url": "https://www.bilibili.com/video/{}".format(bvid) if bvid else "",
            "author": v.get("owner", {}).get("name", ""),
            "views": stat.get("view", 0),
            "danmaku": stat.get("danmaku", 0),
            "likes": stat.get("like", 0),
        })

    return {
        "source": "bilibili",
        "label": "Bilibili",
        "emoji": "📺",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _try_hot_search(top, timeout):
    """Fallback: B站搜索热词"""
    req = urllib.request.Request(_HOT_SEARCH_URL, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    results = data.get("result", {}).get("tag", [])
    if not results:
        return None

    items = []
    for i, entry in enumerate(results[:top], 1):
        word = entry.get("value", "")
        items.append({
            "rank": i,
            "title": word,
            "url": "https://search.bilibili.com/all?keyword={}".format(
                urllib.request.quote(word, safe="")),
            "author": "",
            "views": 0,
        })

    return {
        "source": "bilibili",
        "label": "Bilibili",
        "emoji": "📺",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _error(msg):
    return {
        "source": "bilibili",
        "label": "Bilibili",
        "emoji": "📺",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
