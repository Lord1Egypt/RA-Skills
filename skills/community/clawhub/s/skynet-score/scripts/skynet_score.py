#!/usr/bin/env python3

"""Skynet score: call API and return raw JSON."""

from __future__ import annotations

import argparse
import gzip
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode


DEFAULT_API_URL = "https://open.api.certik.com/projects"


class SkynetScoreError(RuntimeError):
    pass


@dataclass
class SkynetScoreClient:
    api_url: str = DEFAULT_API_URL
    timeout_seconds: float = 20.0

    def search(self, keyword: str) -> dict[str, Any]:
        params = urlencode({"keyword": keyword})
        url = f"{self.api_url}?{params}"
        try:
            request = urllib.request.Request(
                url,
                method="GET",
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/122.0.0.0 Safari/537.36"
                    ),
                    "Connection": "keep-alive",
                },
            )
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                raw_bytes = response.read()
                encoding = response.headers.get("Content-Encoding", "")
                if encoding == "gzip":
                    raw_bytes = gzip.decompress(raw_bytes)
                elif encoding == "br":
                    try:
                        import brotli as _brotli

                        raw_bytes = _brotli.decompress(raw_bytes)
                    except ImportError:
                        pass
                raw = raw_bytes.decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8")
            except Exception:
                body = ""
            raise SkynetScoreError(f"HTTP error: status={exc.code}, body={body[:300]}") from exc
        except urllib.error.URLError as exc:
            raise SkynetScoreError(f"Network error: {exc}") from exc

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise SkynetScoreError("Response is not valid JSON.") from exc

        return data


def build_client(api_url: str | None = None, timeout_seconds: float | None = None) -> SkynetScoreClient:
    return SkynetScoreClient(
        api_url=api_url or DEFAULT_API_URL,
        timeout_seconds=timeout_seconds or 20.0,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Skynet score search via direct API")
    parser.add_argument("--keyword", required=True, help="Project keyword, e.g. uniswap")
    return parser.parse_args()


def run(args: argparse.Namespace) -> dict[str, Any]:
    keyword = args.keyword.strip()
    if not keyword:
        raise SkynetScoreError("Keyword cannot be empty.")

    client = build_client(
        api_url=None,
    )
    return client.search(keyword=keyword)


def main() -> int:
    args = parse_args()
    try:
        print(json.dumps(run(args), ensure_ascii=False, indent=2))
        return 0
    except SkynetScoreError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "hint": "Check the keyword or try again later.",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
