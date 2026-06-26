#!/usr/bin/env python3
from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from shared_utils import load_json, write_json
from tavily_client import search as tavily_search


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mk_mock_results(query: str, max_results: int) -> List[Dict[str, str]]:
    n = max(1, min(int(max_results or 5), 10))
    seed = sum(ord(ch) for ch in query) % 997
    out: List[Dict[str, str]] = []
    for i in range(1, n + 1):
        out.append(
            {
                "title": f"Mock context {i} for {query[:48]}",
                "url": f"https://example.com/mock/{seed}/{i}",
                "snippet": f"Mock snippet {i} (seed={seed}) about {query[:80]}",
            }
        )
    return out


def enrich_articles(
    payload: Dict[str, Any],
    max_results: int,
    max_snippets: int,
    timeout: float,
    mock: bool,
) -> Dict[str, Any]:
    articles = list(payload.get("articles") or [])

    enriched_ok = 0
    enriched_error = 0

    for idx, article in enumerate(articles):
        query = (article.get("title") or "").strip()
        fetched_at = _now_iso()

        if not query:
            article["enrichment"] = {
                "status": "error",
                "provider": "tavily",
                "query": "",
                "fetched_at": fetched_at,
                "web_context": [],
                "error": "empty_title_query",
            }
            enriched_error += 1
            continue

        try:
            results = _mk_mock_results(query, max_results) if mock else tavily_search(query, max_results=max_results, timeout=timeout)
            web_context = (results or [])[: max(1, int(max_snippets or 3))]
            if web_context:
                article["enrichment"] = {
                    "status": "ok",
                    "provider": "tavily",
                    "query": query,
                    "fetched_at": fetched_at,
                    "web_context": web_context,
                }
                enriched_ok += 1
            else:
                article["enrichment"] = {
                    "status": "error",
                    "provider": "tavily",
                    "query": query,
                    "fetched_at": fetched_at,
                    "web_context": [],
                    "error": "no_results_or_request_failed",
                }
                enriched_error += 1
        except Exception as exc:
            article["enrichment"] = {
                "status": "error",
                "provider": "tavily",
                "query": query,
                "fetched_at": fetched_at,
                "web_context": [],
                "error": str(exc),
            }
            enriched_error += 1

        # light throttling for external API
        if idx < len(articles) - 1:
            time.sleep(0.5)

    out = dict(payload)
    out["articles"] = articles
    out["article_count"] = len(articles)
    out["enrichment_stats"] = {
        "enriched_ok": enriched_ok,
        "enriched_error": enriched_error,
        "skipped": 0,
        "mock": bool(mock),
    }
    out["enriched_at"] = _now_iso()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase Enrichment: add web context before Phase B")
    ap.add_argument("--input", required=True, help="deep-set.json")
    ap.add_argument("--output", required=True, help="deep-set.enriched.json")
    ap.add_argument("--max-results", type=int, default=5)
    ap.add_argument("--max-snippets", type=int, default=3)
    ap.add_argument("--timeout", type=float, default=20.0)
    ap.add_argument("--mock", action="store_true")
    args = ap.parse_args()

    payload = load_json(Path(args.input), {})
    result = enrich_articles(
        payload=payload,
        max_results=args.max_results,
        max_snippets=args.max_snippets,
        timeout=args.timeout,
        mock=args.mock,
    )
    write_json(Path(args.output), result)

    stats = result.get("enrichment_stats") or {}
    print(
        "[phase_enrich] wrote"
        f" {args.output}"
        f" ok={stats.get('enriched_ok', 0)}"
        f" error={stats.get('enriched_error', 0)}"
        f" skipped={stats.get('skipped', 0)}"
        f" mock={stats.get('mock', False)}"
    )


if __name__ == "__main__":
    main()
