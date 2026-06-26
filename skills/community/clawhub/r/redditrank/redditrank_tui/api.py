"""Async API client for RedditRank endpoints."""

from __future__ import annotations

import json
from typing import AsyncIterator

import httpx

from redditrank_tui.config import API_BASE, load_api_key


class APIError(Exception):
    def __init__(self, message: str, code: str = ""):
        super().__init__(message)
        self.code = code


class RedditRankAPI:
    """Thin async wrapper around the RedditRank HTTP API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or load_api_key() or ""
        self.base = API_BASE.rstrip("/")

    @property
    def _headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.api_key:
            h["x-api-key"] = self.api_key
        return h

    # ── Usage / Account ───────────────────────────────────────────────────

    async def get_usage(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{self.base}/api/v1/usage", headers=self._headers)
            r.raise_for_status()
            return r.json()

    async def validate_key(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.base}/api/v1/auth/validate",
                headers=self._headers,
                json={"token": self.api_key},
            )
            r.raise_for_status()
            return r.json()

    # ── History ───────────────────────────────────────────────────────────

    async def list_sessions(self, limit: int = 20, offset: int = 0) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"{self.base}/api/v1/history/sessions",
                headers=self._headers,
                params={"limit": limit, "offset": offset},
            )
            r.raise_for_status()
            return r.json()

    async def get_session(self, session_id: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"{self.base}/api/v1/history/sessions/{session_id}",
                headers=self._headers,
            )
            r.raise_for_status()
            return r.json()

    async def list_drafts(self, limit: int = 20, offset: int = 0) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"{self.base}/api/v1/history/drafts",
                headers=self._headers,
                params={"limit": limit, "offset": offset},
            )
            r.raise_for_status()
            return r.json()

    # ── Register ──────────────────────────────────────────────────────────

    async def register(self, email: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.base}/api/v1/auth/register",
                json={"email": email},
            )
            r.raise_for_status()
            return r.json()

    async def verify(self, email: str, code: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{self.base}/api/v1/auth/verify",
                json={"email": email, "code": code},
            )
            r.raise_for_status()
            return r.json()

    # ── SSE Streams ───────────────────────────────────────────────────────

    async def discover_stream(
        self,
        *,
        product_url: str = "",
        product_description: str = "",
    ) -> AsyncIterator[tuple[str, dict]]:
        """Yield (event_type, data) tuples from the discover SSE stream."""
        payload: dict = {}
        if product_url:
            payload["product_url"] = product_url
        elif product_description:
            payload["product_description"] = product_description

        async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=10)) as c:
            async with c.stream(
                "POST",
                f"{self.base}/api/v1/discover/stream",
                headers=self._headers,
                json=payload,
            ) as resp:
                resp.raise_for_status()
                buffer = ""
                async for chunk in resp.aiter_text():
                    buffer += chunk
                    while "\n\n" in buffer:
                        block, buffer = buffer.split("\n\n", 1)
                        event_type, event_data = _parse_sse(block)
                        if event_type and event_data is not None:
                            yield event_type, event_data

    async def draft_stream(
        self,
        *,
        thread_url: str,
        product_name: str,
        product_url: str = "",
        product_description: str = "",
    ) -> AsyncIterator[tuple[str, dict]]:
        """Yield (event_type, data) tuples from the draft SSE stream."""
        payload = {
            "thread_url": thread_url,
            "product": {
                "name": product_name,
                "url": product_url,
                "description": product_description,
            },
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=10)) as c:
            async with c.stream(
                "POST",
                f"{self.base}/api/v1/draft/stream",
                headers=self._headers,
                json=payload,
            ) as resp:
                resp.raise_for_status()
                buffer = ""
                async for chunk in resp.aiter_text():
                    buffer += chunk
                    while "\n\n" in buffer:
                        block, buffer = buffer.split("\n\n", 1)
                        event_type, event_data = _parse_sse(block)
                        if event_type and event_data is not None:
                            yield event_type, event_data


def _parse_sse(block: str) -> tuple[str, dict | None]:
    """Parse a single SSE event block into (event_type, parsed_data)."""
    event_type = ""
    data_str = ""
    for line in block.strip().split("\n"):
        if line.startswith("event: "):
            event_type = line[7:]
        elif line.startswith("data: "):
            data_str = line[6:]
    if not event_type or not data_str:
        return "", None
    try:
        return event_type, json.loads(data_str)
    except json.JSONDecodeError:
        return event_type, {"raw": data_str}
