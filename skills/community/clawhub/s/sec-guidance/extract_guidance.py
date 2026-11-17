#!/usr/bin/env python3
"""
Extract forward-looking guidance from SEC 10-K/10-Q filings.

Two modes:
  - light (default): self-contained. Fetches from EDGAR, in-memory BM25,
    calls Claude/OpenAI. No infra needed. Requires ANTHROPIC_API_KEY or
    OPENAI_API_KEY.
  - heavy: delegates to a local RAG pipeline at $SEC_PIPELINE_DIR
    (Elasticsearch + sentence-transformers + Ollama). Higher quality for
    bulk/repeat use.

Mode auto-detects: if SEC_PIPELINE_DIR is set AND the pipeline is importable
AND Elasticsearch is reachable, heavy mode runs; otherwise light. Force with
--mode {auto,light,heavy}.

Usage:
  python extract_guidance.py --ticker AAPL --form 10-Q
  python extract_guidance.py --ticker AAPL --form 10-K --top-k 8
  python extract_guidance.py --query "What did management say about iPhone revenue?"
  python extract_guidance.py --mode light --ticker MSFT
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

GUIDANCE_QUERIES = [
    "What is management's guidance and outlook for future revenue and earnings?",
    "What forward-looking statements did management make about future performance expectations?",
    "What did management say about expected gross margins and profitability going forward?",
    "What new product launches, services, or business expansions did management project or plan?",
    "What macroeconomic conditions, risks, or uncertainties did management highlight for upcoming quarters?",
]


def _heavy_available() -> tuple[bool, str]:
    """Return (available, reason) — heavy needs SEC_PIPELINE_DIR + importable pipeline + reachable ES."""
    d = os.environ.get("SEC_PIPELINE_DIR")
    if not d:
        return False, "SEC_PIPELINE_DIR not set"
    p = Path(d)
    if not p.is_dir():
        return False, f"SEC_PIPELINE_DIR ({d}) is not a directory"
    sys.path.insert(0, str(p))
    try:
        from pipeline.index import get_es  # noqa: F401
    except Exception as e:
        return False, f"pipeline not importable from {d}: {e}"
    try:
        es = get_es()
        if not es.ping():
            return False, "Elasticsearch ping failed"
    except Exception as e:
        return False, f"Elasticsearch unreachable: {e}"
    return True, "ok"


def check_index_status(es):
    from pipeline.index import INDEX
    if not es.indices.exists(index=INDEX):
        return 0, []
    count = es.count(index=INDEX)["count"]
    files = []
    try:
        agg = es.search(
            index=INDEX,
            body={"size": 0, "aggs": {"files": {"terms": {"field": "source_file", "size": 200}}}},
        )
        files = [b["key"] for b in agg["aggregations"]["files"]["buckets"]]
    except Exception:
        pass
    return count, files


def ticker_source_files(es, ticker: str) -> set[str]:
    """Return source_file names whose indexed chunks are labeled with this ticker."""
    from pipeline.index import INDEX
    agg = es.search(
        index=INDEX,
        body={
            "size": 0,
            "query": {"term": {"ticker": ticker.upper()}},
            "aggs": {"files": {"terms": {"field": "source_file", "size": 1000}}},
        },
    )
    return {b["key"] for b in agg["aggregations"]["files"]["buckets"]}


def run_heavy(ticker: str, form: str, top_k: int, custom_query: str | None) -> None:
    from pipeline.embed import Embedder
    from pipeline.index import get_es
    from pipeline.retrieve import hybrid_search
    from pipeline.rerank import Reranker
    from pipeline.answer import generate_answer

    print(f"\n{'='*64}")
    print(f"  SEC GUIDANCE (heavy mode) | {ticker.upper()} {form.upper()}")
    print(f"{'='*64}\n")

    embedder = Embedder()
    es = get_es()
    doc_count, indexed_files = check_index_status(es)
    if doc_count == 0:
        print("ERROR: Index is empty. Run first:")
        print(f"  cd '{os.environ.get('SEC_PIPELINE_DIR')}' && python run_pipeline.py ingest")
        sys.exit(1)
    print(f"Index: {doc_count} docs across {len(indexed_files)} files")

    # The shared index may hold many companies' filings. Answers must come
    # only from the requested ticker's documents — never silently present
    # another company's filings under this ticker's banner.
    try:
        allowed_files = ticker_source_files(es, ticker)
    except Exception as e:
        print(f"ERROR: Could not resolve {ticker.upper()}'s documents in the index ({e}).")
        print("Refusing to answer from an unfiltered multi-company index.")
        sys.exit(1)
    if not allowed_files:
        print(f"ERROR: Index has no documents labeled ticker={ticker.upper()}.")
        print("Either ingest this ticker's filings, or your pipeline does not label")
        print("chunks with a 'ticker' field — heavy mode cannot safely attribute")
        print("answers without it. Falling back is unsafe; use light mode instead:")
        print(f"  python extract_guidance.py --mode light --ticker {ticker.upper()}")
        sys.exit(1)
    print(f"Scope: {len(allowed_files)} file(s) labeled {ticker.upper()}\n")

    try:
        reranker = Reranker()
    except Exception as e:
        print(f"WARNING: Reranker unavailable ({e}), using raw retrieval scores.\n")
        reranker = None

    queries = [custom_query] if custom_query else GUIDANCE_QUERIES
    for i, query in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] {query}")
        print("─" * 64)
        try:
            candidates = hybrid_search(query, embedder, es, top_k=top_k * 4)
            candidates = [c for c in candidates if c.get("source_file") in allowed_files]
            if not candidates:
                print(f"  No relevant passages found in {ticker.upper()}'s filings.\n")
                continue
            results = reranker.rerank(query, candidates, top_k=top_k) if reranker else candidates[:top_k]
            out = generate_answer(query, results)
            print(out["answer"])
            print("\nSources:")
            for src in out["sources"]:
                date = src.get("filing_date", "?")
                page = src.get("page_number", "?")
                print(f"  [{src['num']}] {src['source_file']}  p.{page}  filed {date}")
            print()
        except Exception as e:
            print(f"  ERROR: {e}\n")

    print(f"{'='*64}\nDone.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract management guidance from SEC 10-K/10-Q filings"
    )
    parser.add_argument("--ticker", default="AAPL")
    parser.add_argument("--form", default="auto",
                        choices=["auto", "10-Q", "10-K", "20-F", "40-F", "6-K", "8-K"],
                        help="auto tries 10-Q → 10-K → 20-F → 40-F → 6-K "
                             "(foreign private issuers file the latter three); "
                             "8-K is --diff only (Item 2.02 earnings releases)")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--query", help="Single custom guidance question")
    parser.add_argument("--json", action="store_true",
                        help="Structured JSON output (light mode only)")
    parser.add_argument("--demo", metavar="TICKER", nargs="?", const="AAPL",
                        help="Run light mode on a bundled cached filing — no "
                             "network, no API key, no third-party deps (default AAPL)")
    parser.add_argument("--mode", default="auto", choices=["auto", "light", "heavy"],
                        help="Force a mode. Default auto: heavy if available, else light.")
    parser.add_argument("--diff", action="store_true",
                        help="Guidance revision detection: compare the two most "
                             "recent guidance-bearing filings (8-K Item 2.02 "
                             "earnings releases first, then 10-Q/10-K) and emit "
                             "graded revision events (raised/lowered/dropped/...). "
                             "Needs an LLM (API key or `claude` CLI).")
    args = parser.parse_args()

    if args.diff:
        from guidance_diff import run_diff
        run_diff(args.ticker, args.form, as_json=args.json)
        return

    if args.form == "8-K":
        print("ERROR: --form 8-K is only meaningful with --diff (earnings-"
              "release revision detection). For one-off extraction use "
              "--form auto.")
        sys.exit(1)

    if args.demo:
        from sec_guidance_light import run_demo
        run_demo(args.demo, max(args.top_k, 8), args.query, as_json=args.json)
        return

    if args.mode == "heavy":
        ok, reason = _heavy_available()
        if not ok:
            print(f"ERROR: --mode heavy requested but unavailable ({reason})")
            sys.exit(1)
        if args.json:
            print("WARNING: --json is light-mode only, ignoring", file=sys.stderr)
        form = "10-Q" if args.form == "auto" else args.form
        run_heavy(args.ticker, form, args.top_k, args.query)
        return

    if args.mode == "light":
        from sec_guidance_light import run_light
        run_light(args.ticker, args.form, max(args.top_k, 8), args.query,
                  as_json=args.json)
        return

    # auto
    ok, reason = _heavy_available()
    if ok and not args.json:
        form = "10-Q" if args.form == "auto" else args.form
        run_heavy(args.ticker, form, args.top_k, args.query)
    else:
        print(f"[mode] heavy unavailable ({reason}) — using light" if not ok
              else "[mode] --json requested — using light", file=sys.stderr)
        from sec_guidance_light import run_light
        run_light(args.ticker, args.form, max(args.top_k, 8), args.query,
                  as_json=args.json)


if __name__ == "__main__":
    main()
