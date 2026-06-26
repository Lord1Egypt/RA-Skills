#!/usr/bin/env python3
"""
SearXNG Web Search Tool

A privacy-respecting web search tool powered by SearXNG metasearch engine.
Rewritten from PulseBot's built-in web_search skill for the agentskills.io standard.

Usage:
    python searxng_search.py "search query" [options]

Environment Variables:
    SEARXNG_BASE_URL    - SearXNG instance URL (default: http://localhost:8080)
    SEARXNG_MAX_RESULTS - Maximum results to return (default: 10)
    SEARXNG_LANGUAGE    - Default language (default: all)
    SEARXNG_SAFESEARCH  - Safe search level 0/1/2 (default: 0)
    SEARXNG_TIMEOUT     - Request timeout in seconds (default: 15)
    SEARXNG_CATEGORIES  - Default categories (default: general)

Copyright 2024-2026 Timeplus, Inc. Apache-2.0 License.
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print(
        json.dumps(
            {
                "query": "",
                "results": [],
                "suggestions": [],
                "answers": [],
                "total_results": 0,
                "error": "Missing dependency: pip install requests",
            }
        )
    )
    sys.exit(1)

logger = logging.getLogger(__name__)


class SearXNGSearchTool:
    """
    SearXNG-based web search tool.

    Provides structured web search results from a self-hosted SearXNG
    metasearch engine instance. SearXNG aggregates results from 243+
    search services (Google, Bing, DuckDuckGo, Brave, etc.) while
    preserving user privacy — no tracking, no profiling.

    This class is designed to be used both as a standalone CLI tool
    and as an importable module for agent frameworks like PulseBot.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        max_results: int = 0,
        language: Optional[str] = None,
        safesearch: Optional[int] = None,
        timeout: Optional[int] = None,
        categories: Optional[str] = None,
    ):
        self.base_url = (
            base_url
            or os.environ.get("SEARXNG_BASE_URL", "http://localhost:8080")
        ).rstrip("/")
        self.max_results = max_results or int(
            os.environ.get("SEARXNG_MAX_RESULTS", "10")
        )
        self.language = language or os.environ.get("SEARXNG_LANGUAGE", "all")
        self.safesearch = (
            safesearch
            if safesearch is not None
            else int(os.environ.get("SEARXNG_SAFESEARCH", "0"))
        )
        self.timeout = timeout or int(os.environ.get("SEARXNG_TIMEOUT", "15"))
        self.categories = categories or os.environ.get(
            "SEARXNG_CATEGORIES", "general"
        )
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "PulseBot-SearXNG-Skill/1.0",
            }
        )

    def search(
        self,
        query: str,
        categories: Optional[str] = None,
        engines: Optional[str] = None,
        language: Optional[str] = None,
        pageno: int = 1,
        time_range: Optional[str] = None,
        safesearch: Optional[int] = None,
        max_results: Optional[int] = None,
    ) -> dict[str, Any]:
        """
        Perform a web search via SearXNG.

        Args:
            query: Search query string.
            categories: Comma-separated categories
                        (general, images, videos, news, map, music, it, science, files, social media).
            engines: Comma-separated engine names (e.g. "google,bing,duckduckgo").
            language: Language code (e.g. "en", "zh", "de", "all").
            pageno: Page number for pagination (default: 1).
            time_range: Time filter — "day", "month", or "year".
            safesearch: Override safe search level (0, 1, 2).
            max_results: Override maximum number of results to return.

        Returns:
            dict with keys: query, results, suggestions, answers, total_results, error
        """
        if not query or not query.strip():
            return self._make_response(query="", error="Empty search query")

        effective_max = max_results or self.max_results
        params = {
            "q": query.strip(),
            "format": "json",
            "categories": categories or self.categories,
            "language": language or self.language,
            "safesearch": safesearch if safesearch is not None else self.safesearch,
            "pageno": pageno,
        }

        if engines:
            params["engines"] = engines
        if time_range and time_range in ("day", "month", "year"):
            params["time_range"] = time_range

        search_url = urljoin(self.base_url + "/", "search")

        try:
            response = self._session.get(
                search_url, params=params, timeout=self.timeout
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            return self._make_response(
                query=query,
                error=f"Cannot connect to SearXNG at {self.base_url}. "
                f"Ensure the instance is running and accessible.",
            )
        except requests.exceptions.Timeout:
            return self._make_response(
                query=query,
                error=f"Request to SearXNG timed out after {self.timeout}s.",
            )
        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else "unknown"
            if status == 403:
                return self._make_response(
                    query=query,
                    error="SearXNG returned 403 Forbidden. "
                    "Ensure JSON format is enabled in settings.yml: "
                    "search.formats: [html, json]",
                )
            if status == 429:
                return self._make_response(
                    query=query,
                    error="Rate limited by SearXNG. Try again later or "
                    "use a self-hosted instance with limiter disabled.",
                )
            return self._make_response(
                query=query,
                error=f"SearXNG HTTP error {status}: {e}",
            )
        except requests.exceptions.RequestException as e:
            return self._make_response(
                query=query,
                error=f"Request failed: {e}",
            )

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError) as e:
            return self._make_response(
                query=query,
                error=f"Invalid JSON response from SearXNG: {e}",
            )

        raw_results = data.get("results", [])
        results = []
        for r in raw_results[:effective_max]:
            result = {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", ""),
                "engines": r.get("engines", []),
                "score": r.get("score", 0),
                "category": r.get("category", ""),
            }
            if r.get("publishedDate"):
                result["published_date"] = r["publishedDate"]
            if r.get("thumbnail"):
                result["thumbnail"] = r["thumbnail"]
            if r.get("img_src"):
                result["image_url"] = r["img_src"]
            results.append(result)

        # Log unresponsive engines for debugging
        unresponsive = data.get("unresponsive_engines", [])
        if unresponsive:
            engine_issues = [f"{eng[0]}: {eng[1]}" for eng in unresponsive if len(eng) >= 2]
            if engine_issues:
                logger.warning("Unresponsive engines: %s", "; ".join(engine_issues))

        return self._make_response(
            query=query,
            results=results,
            suggestions=data.get("suggestions", []),
            answers=data.get("answers", []),
            total_results=len(results),
        )

    def search_news(
        self,
        query: str,
        language: Optional[str] = None,
        time_range: str = "day",
        max_results: Optional[int] = None,
    ) -> dict[str, Any]:
        """Convenience method for news-specific searches."""
        return self.search(
            query=query,
            categories="news",
            language=language,
            time_range=time_range,
            max_results=max_results,
        )

    def search_images(
        self,
        query: str,
        language: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> dict[str, Any]:
        """Convenience method for image searches."""
        return self.search(
            query=query,
            categories="images",
            language=language,
            max_results=max_results,
        )

    def search_it(
        self,
        query: str,
        language: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> dict[str, Any]:
        """Convenience method for IT/tech-specific searches."""
        return self.search(
            query=query,
            categories="it",
            language=language,
            max_results=max_results,
        )

    def check_health(self) -> dict[str, Any]:
        """
        Check if the SearXNG instance is reachable and JSON API is enabled.

        Returns:
            dict with keys: healthy (bool), base_url, version, error
        """
        config_url = urljoin(self.base_url + "/", "config")
        try:
            response = self._session.get(config_url, timeout=5)
            response.raise_for_status()
            config = response.json()
            return {
                "healthy": True,
                "base_url": self.base_url,
                "version": config.get("version", "unknown"),
                "engines_count": len(config.get("engines", [])),
                "categories": config.get("categories", []),
                "error": None,
            }
        except requests.exceptions.ConnectionError:
            return {
                "healthy": False,
                "base_url": self.base_url,
                "error": f"Cannot connect to {self.base_url}",
            }
        except Exception as e:
            return {
                "healthy": False,
                "base_url": self.base_url,
                "error": str(e),
            }

    def format_results_as_text(self, response: dict[str, Any]) -> str:
        """
        Format search results as readable text for LLM consumption.

        Args:
            response: Search response dict from self.search()

        Returns:
            Formatted string with numbered results.
        """
        if response.get("error"):
            return f"Search error: {response['error']}"

        results = response.get("results", [])
        if not results:
            return f"No results found for: {response.get('query', '')}"

        lines = [f"Search results for: {response['query']}\n"]

        for i, r in enumerate(results, 1):
            lines.append(f"{i}. {r['title']}")
            lines.append(f"   URL: {r['url']}")
            if r.get("snippet"):
                lines.append(f"   {r['snippet']}")
            if r.get("published_date"):
                lines.append(f"   Published: {r['published_date']}")
            engines_str = ", ".join(r.get("engines", []))
            if engines_str:
                lines.append(f"   Sources: {engines_str}")
            lines.append("")

        suggestions = response.get("suggestions", [])
        if suggestions:
            lines.append(f"Related searches: {', '.join(suggestions)}")

        answers = response.get("answers", [])
        if answers:
            lines.insert(1, f"Direct answer: {answers[0]}\n")

        return "\n".join(lines)

    @staticmethod
    def _make_response(
        query: str = "",
        results: Optional[list] = None,
        suggestions: Optional[list] = None,
        answers: Optional[list] = None,
        total_results: int = 0,
        error: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a standardized response dict."""
        return {
            "query": query,
            "results": results or [],
            "suggestions": suggestions or [],
            "answers": answers or [],
            "total_results": total_results,
            "error": error,
        }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Search the web using SearXNG metasearch engine.",
        epilog="Environment variables: SEARXNG_BASE_URL, SEARXNG_MAX_RESULTS, "
        "SEARXNG_LANGUAGE, SEARXNG_SAFESEARCH, SEARXNG_TIMEOUT, SEARXNG_CATEGORIES",
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument(
        "--base-url",
        default=None,
        help="SearXNG instance URL (default: $SEARXNG_BASE_URL or http://localhost:8080)",
    )
    parser.add_argument(
        "--categories",
        default=None,
        help="Search categories: general, images, videos, news, map, music, it, science, files, social media",
    )
    parser.add_argument(
        "--engines",
        default=None,
        help="Comma-separated engine names (e.g. google,bing,duckduckgo)",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Search language (e.g. en, zh, de, all)",
    )
    parser.add_argument(
        "--time-range",
        choices=["day", "month", "year"],
        default=None,
        help="Time range filter",
    )
    parser.add_argument(
        "--safesearch",
        type=int,
        choices=[0, 1, 2],
        default=None,
        help="Safe search level: 0=off, 1=moderate, 2=strict",
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=None,
        help="Maximum number of results to return",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=1,
        help="Page number for pagination (default: 1)",
    )
    parser.add_argument(
        "--text",
        action="store_true",
        help="Output as human-readable text instead of JSON",
    )
    parser.add_argument(
        "--health",
        action="store_true",
        help="Check SearXNG instance health and exit",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.WARNING)

    tool = SearXNGSearchTool(
        base_url=args.base_url,
        categories=args.categories,
        language=args.language,
        safesearch=args.safesearch,
    )

    # Health check mode
    if args.health:
        health = tool.check_health()
        print(json.dumps(health, indent=2))
        sys.exit(0 if health["healthy"] else 1)

    # Search mode requires a query
    if not args.query:
        parser.error("Search query is required (or use --health)")

    result = tool.search(
        query=args.query,
        categories=args.categories,
        engines=args.engines,
        language=args.language,
        pageno=args.page,
        time_range=args.time_range,
        safesearch=args.safesearch,
        max_results=args.max_results,
    )

    if args.text:
        print(tool.format_results_as_text(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

    # Exit with non-zero if there was an error
    if result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
