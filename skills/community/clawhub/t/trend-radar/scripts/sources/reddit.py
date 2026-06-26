"""
Reddit trending posts — RSS feed (most reliable, zero API key).

Reddit's JSON endpoint aggressively blocks non-browser clients.
The Atom RSS feed at /r/popular.rss is much more permissive.
"""

import json
import re
import urllib.request
from datetime import datetime, timezone

_RSS_URL = "https://www.reddit.com/r/popular.rss"
_JSON_URL = "https://www.reddit.com/r/popular/hot.json"


def fetch(top: int = 10, timeout: int = 15) -> dict:
    """Fetch hot posts from r/popular.

    Returns:
        {
            "source": "reddit",
            "label": "Reddit",
            "emoji": "👽",
            "fetched_at": <ISO>,
            "items": [{"rank": 1, "title": "...", "url": "...", "subreddit": "...", "author": "..."}, ...]
        }
    """
    result = _try_rss(top, timeout)
    if result:
        return result

    result = _try_json(top, timeout)
    if result:
        return result

    return _error("Reddit blocked all requests. Try again later.")


def _try_rss(top, timeout):
    req = urllib.request.Request(_RSS_URL, headers={
        "User-Agent": "TrendRadar/1.0",
        "Accept": "application/rss+xml, application/xml, text/xml",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.DOTALL)
    if not entries:
        return None

    items = []
    for i, entry in enumerate(entries[:top], 1):
        title_m = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", entry)
        link_m = re.search(r'<link[^>]*href="([^"]*)"', entry)
        author_m = re.search(r"<name>([^<]*)</name>", entry)
        cat_m = re.search(r'<category[^>]*term="([^"]*)"', entry)

        title = title_m.group(1).strip() if title_m else ""
        url = link_m.group(1).strip() if link_m else ""
        author = author_m.group(1).strip() if author_m else ""
        subreddit = "r/{}".format(cat_m.group(1)) if cat_m else ""

        items.append({
            "rank": i,
            "title": _unescape_html(title),
            "url": url,
            "subreddit": subreddit,
            "author": author,
        })

    return {
        "source": "reddit",
        "label": "Reddit",
        "emoji": "👽",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _try_json(top, timeout):
    req = urllib.request.Request(_JSON_URL, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    children = data.get("data", {}).get("children", [])
    if not children:
        return None

    items = []
    rank = 0
    for child in children:
        d = child.get("data", {})
        if d.get("stickied"):
            continue
        rank += 1
        if rank > top:
            break
        items.append({
            "rank": rank,
            "title": d.get("title", ""),
            "url": "https://reddit.com{}".format(d.get("permalink", "")),
            "subreddit": d.get("subreddit_name_prefixed", ""),
            "score": d.get("score", 0),
            "comments": d.get("num_comments", 0),
        })

    return {
        "source": "reddit",
        "label": "Reddit",
        "emoji": "👽",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "items": items,
    }


def _unescape_html(s):
    """Basic HTML entity unescape."""
    s = s.replace("&amp;", "&")
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&quot;", '"')
    s = s.replace("&#39;", "'")
    return s


def _error(msg):
    return {
        "source": "reddit",
        "label": "Reddit",
        "emoji": "👽",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": msg,
        "items": [],
    }
