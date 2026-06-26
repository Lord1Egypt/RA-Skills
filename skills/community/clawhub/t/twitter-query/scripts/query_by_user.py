#!/usr/bin/env python3
"""
Fetch tweets for one X/Twitter user via twitterapi.io GET /twitter/user/last_tweets.
Env: TWITTER_API_KEY (required), TWITTER_API_BASE (optional).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE = "https://api.twitterapi.io"
MAX_RETRIES = 3
RETRY_DELAY = 2.0


def _request(url: str, api_key: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "X-API-Key": api_key,
            "User-Agent": "twitter-query-skill/1.0",
        },
        method="GET",
    )
    last_err: Exception | None = None
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
                continue
            try:
                detail = e.read().decode("utf-8")
            except Exception:
                detail = ""
            raise SystemExit(f"HTTP {e.code}: {detail or e.reason}") from e
        except Exception as e:
            last_err = e
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
                continue
            raise
    raise SystemExit(str(last_err))


def _tweet_url(author: str | None, tweet_id: str | None) -> str | None:
    if author and tweet_id:
        return f"https://x.com/{author}/status/{tweet_id}"
    return None


def normalize_tweet(raw: dict) -> dict:
    author = (raw.get("author") or {}) if isinstance(raw.get("author"), dict) else {}
    un = author.get("userName") or author.get("username")
    tid = raw.get("id")
    out = {
        "id": tid,
        "url": raw.get("url") or _tweet_url(un, str(tid) if tid is not None else None),
        "text": raw.get("text"),
        "createdAt": raw.get("createdAt"),
        "lang": raw.get("lang"),
        "likeCount": raw.get("likeCount"),
        "retweetCount": raw.get("retweetCount"),
        "replyCount": raw.get("replyCount"),
        "quoteCount": raw.get("quoteCount"),
        "viewCount": raw.get("viewCount"),
        "isReply": raw.get("isReply"),
        "author": {
            "userName": un,
            "name": author.get("name"),
            "followers": author.get("followers"),
            "isBlueVerified": author.get("isBlueVerified"),
        },
    }
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="Query tweets by X username (last_tweets API).")
    p.add_argument("userName", help="Screen name without @")
    p.add_argument(
        "--max-pages",
        type=int,
        default=5,
        help="Max cursor pages (each page up to ~20 tweets). Default 5.",
    )
    p.add_argument(
        "--include-replies",
        action="store_true",
        help="Include reply tweets (default excludes per API default).",
    )
    args = p.parse_args()

    api_key = os.environ.get("TWITTER_API_KEY", "").strip()
    if not api_key:
        print("Missing TWITTER_API_KEY", file=sys.stderr)
        sys.exit(1)

    base = os.environ.get("TWITTER_API_BASE", DEFAULT_BASE).rstrip("/")
    user = args.userName.lstrip("@")

    all_raw: list[dict] = []
    cursor = ""
    pages = 0
    meta_pages: list[dict] = []

    while pages < args.max_pages:
        q = urllib.parse.urlencode(
            {
                "userName": user,
                "cursor": cursor,
                "includeReplies": "true" if args.include_replies else "false",
            }
        )
        url = f"{base}/twitter/user/last_tweets?{q}"
        data = _request(url, api_key)
        status = data.get("status")
        if status and status != "success":
            msg = data.get("message") or data.get("msg") or "unknown error"
            print(json.dumps({"meta": {"error": True, "message": msg, "raw": data}}, ensure_ascii=False))
            sys.exit(1)

        batch = data.get("tweets") or []
        all_raw.extend(batch)
        meta_pages.append(
            {
                "page": pages + 1,
                "count": len(batch),
                "has_next_page": data.get("has_next_page"),
            }
        )
        pages += 1
        if not data.get("has_next_page"):
            break
        cursor = data.get("next_cursor") or ""
        if not cursor:
            break

    out = {
        "meta": {
            "endpoint": "last_tweets",
            "userName": user,
            "includeReplies": args.include_replies,
            "pages_fetched": pages,
            "tweet_count": len(all_raw),
            "pages": meta_pages,
        },
        "tweets": [normalize_tweet(t) for t in all_raw],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
