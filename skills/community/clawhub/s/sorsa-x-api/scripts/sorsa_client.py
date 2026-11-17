"""Minimal Sorsa API v3 client.

Reads the API key from the SORSA_API_KEY environment variable unless one is
passed explicitly. Requires `requests` (pip install requests).

Docs: https://docs.sorsa.io/ (LLM index: https://docs.sorsa.io/llms.txt)
Get a key: https://api.sorsa.io/overview
"""

from __future__ import annotations

import os
import time
from typing import Any, Iterator

import requests

BASE_URL = "https://api.sorsa.io/v3"

# Endpoints that use POST with a JSON body. Everything else is treated as GET.
_POST_ENDPOINTS = {
    "tweet-info", "tweet-info-bulk", "user-tweets", "comments", "quotes",
    "retweeters", "article", "search-tweets", "mentions", "search-users",
    "check-follow", "check-quoted", "check-retweet", "check-community-member",
    "community-members", "community-tweets", "community-search-tweets",
}


def resolve_user(identifier: str) -> dict:
    """Turn a handle, numeric ID, or profile URL into the right query param."""
    if identifier.startswith("http"):
        return {"user_link": identifier}
    if identifier.lstrip("@").isdigit():
        return {"user_id": identifier.lstrip("@")}
    return {"username": identifier.lstrip("@")}


class SorsaClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL,
                 max_retries: int = 3):
        self.api_key = api_key or os.environ.get("SORSA_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "No API key. Set SORSA_API_KEY or pass api_key=. "
                "Get one at https://api.sorsa.io/overview"
            )
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({"ApiKey": self.api_key})

    # -- low level --------------------------------------------------------
    def request(self, endpoint: str, *, params: dict | None = None,
                body: dict | None = None) -> Any:
        endpoint = endpoint.lstrip("/")
        is_post = body is not None or endpoint in _POST_ENDPOINTS
        url = f"{self.base_url}/{endpoint}"
        resp = None
        for attempt in range(self.max_retries):
            resp = self.session.request(
                "POST" if is_post else "GET",
                url,
                params=params,
                json=body if is_post else None,
                timeout=60,
            )
            if resp.status_code == 429:  # rate limited: exponential backoff
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()
            return resp.json()
        resp.raise_for_status()  # retries exhausted

    def get(self, endpoint: str, **params) -> Any:
        return self.request(endpoint, params=params)

    def post(self, endpoint: str, **body) -> Any:
        return self.request(endpoint, body=body)

    # -- pagination -------------------------------------------------------
    def paginate(self, endpoint: str, *, params: dict | None = None,
                 body: dict | None = None,
                 max_pages: int | None = None) -> Iterator[dict]:
        """Yield each page dict, following next_cursor until it runs out."""
        params = dict(params) if params is not None else None
        body = dict(body) if body is not None else None
        page = 0
        while True:
            data = self.request(endpoint, params=params, body=body)
            yield data
            page += 1
            cursor = data.get("next_cursor")
            if not cursor or (max_pages and page >= max_pages):
                return
            if body is not None:
                body["next_cursor"] = cursor
            else:
                params = dict(params or {})
                params["next_cursor"] = cursor

    # -- convenience ------------------------------------------------------
    def get_profile(self, identifier: str) -> dict:
        return self.get("info", **resolve_user(identifier))

    def user_tweets(self, identifier: str, max_pages: int = 1) -> list[dict]:
        out: list[dict] = []
        for pg in self.paginate("user-tweets", body=resolve_user(identifier),
                                max_pages=max_pages):
            out.extend(pg.get("tweets", []))
        return out

    def search_tweets(self, query: str, order: str = "popular",
                      max_pages: int = 1) -> list[dict]:
        out: list[dict] = []
        for pg in self.paginate("search-tweets",
                                body={"query": query, "order": order},
                                max_pages=max_pages):
            out.extend(pg.get("tweets", []))
        return out

    def followers(self, identifier: str, max_pages: int = 1) -> list[dict]:
        out: list[dict] = []
        for pg in self.paginate("followers", params=resolve_user(identifier),
                                max_pages=max_pages):
            out.extend(pg.get("users", []))
        return out

    def score(self, identifier: str) -> float | None:
        return self.get("score", **resolve_user(identifier)).get("score")

    def trends(self, woeid: int) -> dict:
        """Trending topics for a WOEID location. Returns {"trends": [...]}."""
        return self.get("trends", woeid=woeid)

    def space(self, *, space_id: str | None = None, link: str | None = None) -> dict:
        """Twitter/X Space details by Space ID or Space URL."""
        if not (space_id or link):
            raise ValueError("Provide space_id or link")
        params = {"id": space_id} if space_id else {"link": link}
        return self.get("spaces", **params)


if __name__ == "__main__":
    client = SorsaClient()
    me = client.get_profile("elonmusk")
    print(f"@{me['username']}: {me['followers_count']:,} followers")
