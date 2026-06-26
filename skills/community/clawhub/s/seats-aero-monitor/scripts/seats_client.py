#!/usr/bin/env python3
"""Seats.aero partner API client."""

from __future__ import annotations

import gzip
import io
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


class SeatsClientError(RuntimeError):
    """Raised when Seats API returns an error."""


@dataclass
class SeatsClient:
    api_key: str
    base_url: str = "https://seats.aero/partnerapi"
    timeout_seconds: int = 20

    def _request_json(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        query = urllib.parse.urlencode(
            {k: v for k, v in params.items() if v is not None},
            doseq=True,
        )
        url = f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{query}"

        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "Accept": "application/json",
                "Partner-Authorization": self.api_key,
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "Referer": "https://seats.aero/",
                "Origin": "https://seats.aero",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_seconds) as resp:
                content = resp.read()
                # Handle compressed responses
                encoding = resp.headers.get('Content-Encoding', '')
                if encoding == 'gzip':
                    buf = io.BytesIO(content)
                    f = gzip.GzipFile(fileobj=buf)
                    content = f.read()
                elif encoding == 'br':
                    import brotli
                    content = brotli.decompress(content)
                body = content.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            content = exc.read()
            encoding = exc.headers.get('Content-Encoding', '')
            if encoding == 'gzip':
                buf = io.BytesIO(content)
                f = gzip.GzipFile(fileobj=buf)
                content = f.read()
            elif encoding == 'br':
                import brotli
                content = brotli.decompress(content)
            detail = content.decode("utf-8", errors="replace")
            raise SeatsClientError(f"Seats API HTTP {exc.code}: {detail[:500]}") from exc
        except urllib.error.URLError as exc:
            raise SeatsClientError(f"Seats API request failed: {exc}") from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise SeatsClientError(f"Seats API returned invalid JSON: {body[:300]}") from exc

    @staticmethod
    def _extract_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
        data = payload.get("data", payload)
        candidates: list[Any] = []
        if isinstance(data, list):
            candidates = data
        elif isinstance(data, dict):
            for key in ("items", "results", "trips", "availability", "data"):
                value = data.get(key)
                if isinstance(value, list):
                    candidates = value
                    break
        return [item for item in candidates if isinstance(item, dict)]

    def cached_search(
        self,
        *,
        origin: str,
        destination: str,
        cabin: str,
        start_date: str,
        end_date: str,
        program: str | None = None,
        airlines: list[str] | None = None,
        take: int = 500,
        max_pages: int = 3,
    ) -> list[dict[str, Any]]:
        """Query cached search and return flattened records.

        The partner API shape can vary by endpoint version, so this method accepts
        multiple pagination field names and merges all parsed list records.
        """

        records: list[dict[str, Any]] = []
        cursor: Any = None

        for _ in range(max_pages):
            params: dict[str, Any] = {
                "origin": origin.upper(),
                "origin_airport": origin.upper(),
                "destination": destination.upper(),
                "destination_airport": destination.upper(),
                "cabin": cabin.lower(),
                "startDate": start_date,
                "endDate": end_date,
                "take": take,
                # Common aliases seen across wrappers; ignored by server if unsupported.
                "source": program,
                "program": program,
                "airline": ",".join(airlines) if airlines else None,
                "airlines": ",".join(airlines) if airlines else None,
                "cursor": cursor,
            }
            payload = self._request_json("search", params)
            records.extend(self._extract_records(payload))

            data = payload.get("data", payload)
            next_cursor = None
            has_more = False
            if isinstance(data, dict):
                next_cursor = data.get("nextCursor", data.get("cursor"))
                has_more = bool(data.get("hasMore") or data.get("has_more"))

            if not has_more or not next_cursor:
                break
            cursor = next_cursor

        return records
