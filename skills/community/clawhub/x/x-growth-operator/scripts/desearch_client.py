from __future__ import annotations

import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from common import load_local_env


DESEARCH_BASE = "https://api.desearch.ai"


class DesearchError(Exception):
    pass


def get_api_key() -> str:
    load_local_env()
    key = os.environ.get("DESEARCH_API_KEY")
    if not key:
        raise DesearchError("DESEARCH_API_KEY environment variable not set.")
    return key


def api_request(method: str, path: str, params: dict | None = None, body: dict | None = None):
    api_key = get_api_key()
    url = f"{DESEARCH_BASE}{path}"

    if method == "GET" and params:
        filtered = {k: v for k, v in params.items() if v is not None and v != ""}
        if filtered:
            url = f"{url}?{urlencode(filtered, doseq=True)}"

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
        "User-Agent": "x-growth-operator/1.0",
    }

    data = None
    if method == "POST" and body:
        data = json.dumps(body).encode("utf-8")

    try:
        req = Request(url, data=data, headers=headers, method=method)
        with urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except HTTPError as error:
        raw = error.read().decode("utf-8") if error.fp else ""
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"detail": raw}
        raise DesearchError(f"HTTP {error.code}: {parsed}")
    except URLError as error:
        raise DesearchError(f"Connection failed: {error.reason}")


def search_posts(
    query: str,
    count: int = 10,
    sort: str = "Latest",
    user: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    lang: str | None = None,
    verified: bool = False,
    blue_verified: bool = False,
    is_quote: bool = False,
    is_video: bool = False,
    is_image: bool = False,
    min_retweets: int | None = None,
    min_replies: int | None = None,
    min_likes: int | None = None,
):
    params = {
        "query": query,
        "sort": sort,
        "user": user,
        "start_date": start_date,
        "end_date": end_date,
        "lang": lang,
        "count": count,
        "verified": "true" if verified else None,
        "blue_verified": "true" if blue_verified else None,
        "is_quote": "true" if is_quote else None,
        "is_video": "true" if is_video else None,
        "is_image": "true" if is_image else None,
        "min_retweets": min_retweets,
        "min_replies": min_replies,
        "min_likes": min_likes,
    }
    return api_request("GET", "/twitter", params=params)


def timeline(username: str, count: int = 20):
    return api_request("GET", "/twitter/user/posts", params={"username": username, "count": count})


def post_replies(post_id: str, count: int = 20, query: str | None = None):
    return api_request(
        "GET",
        "/twitter/replies/post",
        params={"post_id": post_id, "count": count, "query": query or ""},
    )


def normalize_tweets(payload) -> list[dict]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("tweets", "results", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


if __name__ == "__main__":
    print("This module is intended to be imported.", file=sys.stderr)
    raise SystemExit(1)
