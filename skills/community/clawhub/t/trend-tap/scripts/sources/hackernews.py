"""
Hacker News top stories — official Firebase API, zero API key.
"""

import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def fetch(top: int = 10, timeout: int = 15) -> dict:
    """Fetch top stories from Hacker News.

    Returns:
        {
            "source": "hackernews",
            "label": "Hacker News",
            "emoji": "💻",
            "fetched_at": <ISO>,
            "items": [{"rank": 1, "title": "...", "url": "...", "score": 342, "comments": 120}, ...]
        }
    """
    try:
        req = urllib.request.Request(_TOP_URL, headers={
            "User-Agent": "TrendTap/2.0",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            story_ids = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return _error(str(e))

    story_ids = story_ids[:top]

    items = []
    with ThreadPoolExecutor(max_workers=min(top, 8)) as pool:
        futures = {pool.submit(_fetch_item, sid, timeout): idx
                   for idx, sid in enumerate(story_ids)}
        results = [None] * len(story_ids)
        for future in as_completed(futures):
            idx = futures[future]
            try:
                results[idx] = future.result()
            except Exception:
                results[idx] = None

    for i, item_data in enumerate(results, 1):
        if item_data is None:
            continue
        hn_url = f"https://news.ycombinator.com/item?id={item_data.get('id', '')}"
        items.append({
            "rank": i,
            "title": item_data.get("title", ""),
            "url": item_data.get("url", hn_url),
            "hn_url": hn_url,
            "score": item_data.get("score", 0),
            "comments": item_data.get("descendants", 0),
        })

    return {
        "source": "hackernews",
        "label": "Hacker News",
        "emoji": "💻",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _fetch_item(story_id: int, timeout: int):
    try:
        url = _ITEM_URL.format(story_id)
        req = urllib.request.Request(url, headers={"User-Agent": "TrendTap/2.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def _error(msg: str) -> dict:
    return {
        "source": "hackernews",
        "label": "Hacker News",
        "emoji": "💻",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
