#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
SearXNG API Wrapper v2.1.0

Instance URL resolved in priority order:
  1. --instance CLI argument
  2. skill-config.json (in the skill root directory)
  3. Built-in default
"""

import sys
import json
import hashlib
import time
import html.parser
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

import requests


def _load_skill_config() -> dict:
    """Load settings from skill-config.json in the skill root directory."""
    config_path = Path(__file__).parent.parent / "skill-config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                data = json.load(f)
            return data.get("config", {})
        except (json.JSONDecodeError, IOError):
            pass
    return {}


# Valid SearXNG time_range values (per SearXNG API docs)
VALID_TIME_RANGES = {"year", "month", "week", "day"}

# Aliases that map to valid SearXNG time ranges
TIME_RANGE_ALIASES: Dict[str, str] = {
    "hour": "day",
    "24h": "day",
    "7d": "week",
    "30d": "month",
}

VALID_CATEGORIES = [
    "general", "news", "science", "files", "images",
    "videos", "music", "social media", "it"
]


class _TextExtractor(html.parser.HTMLParser):
    """Strip HTML tags and extract visible text."""

    SKIP_TAGS = {"script", "style", "head", "nav", "footer", "noscript"}

    def __init__(self):
        super().__init__()
        self._skip = 0
        self._parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self._parts.append(text)

    def get_text(self, max_chars: int = 4000) -> str:
        return " ".join(self._parts)[:max_chars]


@dataclass
class SearchResult:
    """Represents a single SearXNG search result."""
    title: str
    url: str
    snippet: str
    img_url: str = ""
    engine: str = ""
    score: float = 0.0
    full_content: str = ""

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "img_url": self.img_url,
            "engine": self.engine,
            "score": self.score,
        }
        if self.full_content:
            d["full_content"] = self.full_content
        return d


class SearXNGClient:
    """SearXNG API client with caching and rate limiting."""

    DEFAULT_INSTANCE = ""  # Set in skill-config.json → default_instance
    DEFAULT_RATE_LIMIT = 2.0   # seconds between requests
    DEFAULT_CACHE_EXPIRY = 3600  # seconds

    CACHE_DIR = Path.home() / ".openclaw" / "searxng-cache"

    def __init__(
        self,
        base_url: str = None,
        rate_limit: float = None,
        cache_expiry: int = None,
        cache_enabled: bool = None,
    ):
        cfg = _load_skill_config()

        # Resolve instance URL: arg > skill-config.json > default
        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            cfg_url = cfg.get("default_instance", "").strip()
            self.base_url = cfg_url.rstrip("/") if cfg_url else self.DEFAULT_INSTANCE

        # Resolve rate limit: arg > skill-config.json > default
        self.rate_limit = float(rate_limit if rate_limit is not None else cfg.get("rate_limit", self.DEFAULT_RATE_LIMIT))

        # Resolve cache expiry: arg > skill-config.json > default
        self.cache_expiry = int(cache_expiry if cache_expiry is not None else cfg.get("cache_expiry", self.DEFAULT_CACHE_EXPIRY))

        # Resolve cache enabled: arg > skill-config.json > default
        if cache_enabled is not None:
            self.cache_enabled = cache_enabled
        else:
            self.cache_enabled = bool(cfg.get("cache_enabled", True))

        self.last_request = 0.0
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "OpenClaw-SearXNG-Skill/2.0"})

        if self.cache_enabled:
            self.CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Rate limiting
    # ------------------------------------------------------------------

    def _wait_for_rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------

    def _cache_key(self, query: str, **params) -> str:
        raw = f"{query}|{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _cache_path(self, key: str) -> Path:
        return self.CACHE_DIR / f"{key}.json"

    def _load_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Return cached payload dict or None if missing/expired."""
        if not self.cache_enabled:
            return None
        path = self._cache_path(key)
        if not path.exists():
            return None
        try:
            with open(path) as f:
                data = json.load(f)
            age = time.time() - data.get("timestamp", 0)
            if age < self.cache_expiry:
                return {"results": data["results"], "age": int(age)}
        except (KeyError, json.JSONDecodeError, IOError):
            pass
        return None

    def _save_cache(self, key: str, results: List[Dict[str, Any]]):
        if not self.cache_enabled:
            return
        try:
            with open(self._cache_path(key), "w") as f:
                json.dump({"timestamp": time.time(), "results": results}, f)
        except IOError as e:
            print(f"Warning: cache write failed: {e}", file=sys.stderr)

    # ------------------------------------------------------------------
    # Parameter helpers
    # ------------------------------------------------------------------

    def _fetch_full_content(self, url: str, max_chars: int = 4000) -> str:
        """Fetch a URL and return stripped plain text, up to max_chars."""
        if not url:
            return ""
        try:
            self._wait_for_rate_limit()
            resp = self.session.get(url, timeout=8, allow_redirects=True)
            resp.raise_for_status()
            ct = resp.headers.get("Content-Type", "")
            if "html" not in ct and "text" not in ct:
                return ""
            extractor = _TextExtractor()
            extractor.feed(resp.text)
            return extractor.get_text(max_chars)
        except Exception as e:
            print(f"Warning: could not fetch {url}: {e}", file=sys.stderr)
            return ""

    def _normalize_time_range(self, time_range: str) -> Optional[str]:
        """Map aliases to valid SearXNG time ranges, warn on unknown values."""
        if time_range in VALID_TIME_RANGES:
            return time_range
        mapped = TIME_RANGE_ALIASES.get(time_range)
        if mapped:
            print(f"Info: time_range '{time_range}' mapped to '{mapped}'", file=sys.stderr)
            return mapped
        print(f"Warning: unknown time_range '{time_range}', ignoring", file=sys.stderr)
        return None

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(
        self,
        query: str,
        categories: List[str] = None,
        time_range: str = None,
        language: str = "en",
        safesearch: bool = True,
        pageno: int = 1,
        full_content: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute a search query against the configured SearXNG instance.

        Args:
            query:       Search query string (min 2 chars)
            categories:  One or more of VALID_CATEGORIES
            time_range:  One of VALID_TIME_RANGES or TIME_RANGE_ALIASES keys
            language:    BCP-47 language tag (default: "en")
            safesearch:  Enable safe search filtering
            pageno:      Results page number (1-based)

        Returns:
            dict with keys: results, metadata, status
        """
        query = (query or "").strip()
        if len(query) < 2:
            return {"error": "Query must be at least 2 characters", "status": "error"}

        params: Dict[str, Any] = {
            "q": query,
            "format": "json",
            "pageno": max(1, pageno),
            "language": language,
            "safesearch": "1" if safesearch else "0",
        }

        if categories:
            params["categories"] = ",".join(categories)

        if time_range:
            normalized = self._normalize_time_range(time_range)
            if normalized:
                params["time_range"] = normalized

        # Cache lookup
        key = self._cache_key(query, **params)
        cached = self._load_cache(key)
        if cached:
            return {
                "results": cached["results"],
                "metadata": {
                    "from_cache": True,
                    "cache_age_seconds": cached["age"],
                    "query": query,
                    "count": len(cached["results"]),
                },
                "status": "success",
            }

        self._wait_for_rate_limit()

        try:
            url = f"{self.base_url}/search"
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.Timeout:
            return {"error": "Request timed out after 10s", "status": "error"}
        except requests.exceptions.ConnectionError as e:
            return {"error": f"Connection failed to {self.base_url}: {e}", "status": "error"}
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP {e.response.status_code}: {e}", "status": "error"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}", "status": "error"}
        except ValueError as e:
            return {"error": f"Invalid JSON response: {e}", "status": "error"}

        results: List[Dict[str, Any]] = []

        # Direct answers (e.g. calculator, quick facts) — prepend, not replace
        for answer in data.get("answers", []):
            text = answer if isinstance(answer, str) else answer.get("answer", str(answer))
            results.append({
                "title": "Direct Answer",
                "url": "",
                "snippet": text,
                "img_url": "",
                "engine": "searxng",
                "score": 1.0,
            })

        # Main results
        for r in data.get("results", data.get("items", [])):
            url = r.get("url", r.get("link", ""))
            fetched = self._fetch_full_content(url) if full_content else ""
            results.append(SearchResult(
                title=r.get("title", ""),
                url=url,
                snippet=r.get("content", r.get("snippet", "")),
                img_url=r.get("img_url", ""),
                engine=r.get("engine", ""),
                score=float(r.get("score", 0.0)),
                full_content=fetched,
            ).to_dict())

        self._save_cache(key, results)

        return {
            "results": results,
            "metadata": {
                "from_cache": False,
                "query": query,
                "count": len(results),
                "categories": categories,
                "time_range": params.get("time_range"),
                "instance": self.base_url,
            },
            "status": "success",
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="SearXNG Search Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Categories: {', '.join(VALID_CATEGORIES)}
Time ranges: {', '.join(sorted(VALID_TIME_RANGES) + sorted(TIME_RANGE_ALIASES))}
  (aliases: hour/24h→day, 7d→week, 30d→month)

Instance URL priority: --instance > skill-config.json > built-in default
""",
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--instance",
        default=None,
        metavar="URL",
        help="SearXNG instance URL (overrides config)",
    )
    parser.add_argument(
        "--categories",
        nargs="*",
        choices=VALID_CATEGORIES,
        metavar="CATEGORY",
        help="One or more search categories (quote 'social media' if needed)",
    )
    parser.add_argument(
        "--time-range",
        choices=list(VALID_TIME_RANGES) + list(TIME_RANGE_ALIASES),
        metavar="RANGE",
        dest="time_range",
        help="Time range filter",
    )
    parser.add_argument("--language", default="en", metavar="LANG", help="Language code (default: en)")
    parser.add_argument("--pageno", type=int, default=1, metavar="N", help="Page number (default: 1)")
    parser.add_argument("--no-safesearch", action="store_true", help="Disable safe search")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache for this request")
    parser.add_argument("--full-content", action="store_true", dest="full_content",
                        help="Fetch full page text for each result (slower, richer context)")

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(1)

    client = SearXNGClient(
        base_url=args.instance,
        cache_enabled=False if args.no_cache else None,
    )

    result = client.search(
        query=args.query,
        categories=args.categories,
        time_range=args.time_range,
        language=args.language,
        safesearch=not args.no_safesearch,
        pageno=args.pageno,
        full_content=args.full_content,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
