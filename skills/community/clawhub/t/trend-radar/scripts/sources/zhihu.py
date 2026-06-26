"""
知乎热榜 — multiple strategies, zero API key.

Strategies (tried in order):
  1. Public hot-list API (may require auth)
  2. Scrape zhihu.com/hot HTML page
  3. Use tophub.today aggregator as fallback
"""

import json
import re
import urllib.request
from datetime import datetime, timezone

_API_URL = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total"
_HOT_PAGE = "https://www.zhihu.com/hot"
_TOPHUB_URL = "https://tophub.today/n/mproPpoq6O"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.zhihu.com/",
}


def fetch(top: int = 10, timeout: int = 15) -> dict:
    """Fetch trending topics from 知乎."""
    result = _try_tophub(top, timeout)
    if result:
        return result

    result = _try_api(top, timeout)
    if result:
        return result

    result = _try_hot_page(top, timeout)
    if result:
        return result

    return _error("All methods failed — Zhihu may require login")


def _try_api(top, timeout):
    headers = dict(_HEADERS)
    headers["Accept"] = "application/json"
    req = urllib.request.Request(_API_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    entries = data.get("data", [])
    if not entries:
        return None

    items = []
    for i, entry in enumerate(entries[:top], 1):
        target = entry.get("target", {})
        title = target.get("title", "")
        qid = target.get("id", "")
        url = "https://www.zhihu.com/question/{}".format(qid) if qid else ""
        excerpt = target.get("excerpt", "")[:100]
        heat_text = entry.get("detail_text", "")
        items.append({
            "rank": i, "title": title, "url": url,
            "heat": heat_text, "excerpt": excerpt,
        })

    return _result(items)


def _try_hot_page(top, timeout):
    """Scrape zhihu.com/hot and extract from initialData JSON."""
    headers = dict(_HEADERS)
    headers["Accept"] = "text/html"
    req = urllib.request.Request(_HOT_PAGE, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    m = re.search(r'<script id="js-initialData"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not m:
        return None

    try:
        init = json.loads(m.group(1))
    except Exception:
        return None

    hot_list = (init.get("initialState", {}).get("topstory", {})
                .get("hotList", []))
    if not hot_list:
        return None

    items = []
    for i, entry in enumerate(hot_list[:top], 1):
        target = entry.get("target", {})
        title = target.get("titleArea", {}).get("text", "")
        link = target.get("link", {}).get("url", "")
        excerpt = target.get("excerptArea", {}).get("text", "")[:100]
        heat = target.get("metricsArea", {}).get("text", "")
        items.append({
            "rank": i, "title": title, "url": link,
            "heat": heat, "excerpt": excerpt,
        })

    return _result(items) if items else None


def _try_tophub(top, timeout):
    """Use tophub.today as a fallback (aggregates 知乎热榜)."""
    headers = dict(_HEADERS)
    headers["Accept"] = "text/html"
    req = urllib.request.Request(_TOPHUB_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    pattern = r'<a[^>]*href="(https://www\.zhihu\.com/question/\d+)"[^>]*>([^<]+)</a>'
    matches = re.findall(pattern, html)

    if not matches:
        pattern2 = r'<td class="al">\s*<a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern2, html)

    if not matches:
        return None

    items = []
    for i, (url, title) in enumerate(matches[:top], 1):
        items.append({
            "rank": i, "title": title.strip(), "url": url,
            "heat": "", "excerpt": "",
        })

    return _result(items)


def _result(items):
    return {
        "source": "zhihu",
        "label": "知乎",
        "emoji": "📖",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _error(msg):
    return {
        "source": "zhihu",
        "label": "知乎",
        "emoji": "📖",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
