#!/usr/bin/env python3
"""SCRY — The Ultimate Multi-Source Research Skill.

Usage:
    python3 scry.py <topic> [options]

Options:
    --emit=compact|json|md      Output format (default: compact)
    --quick                     Fast mode (fewer results)
    --deep                      Comprehensive mode
    --days=N                    Look back N days (default: 30)
    --domain=DOMAIN             Force domain (tech|science|finance|crypto|news|entertainment|general)
    --sources=src1,src2,...     Only use specific sources
    --tier=N                    Only use sources from tier N (1, 2, or 3)
    --mock                      Use fixture data (no network)
    --debug                     Enable debug logging
    --no-native-web             Skip native web search (let assistant do WebSearch)
"""

import json
import os
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

# Add lib to path
sys.path.insert(0, os.path.dirname(__file__))

from lib import cache, dates
from lib.conflict import detect_conflicts
from lib.dedupe import cross_source_link, dedupe_items
from lib.domain import classify_topic, get_primary_domain
from lib.env import get_config
from lib.normalize import normalize_items
from lib.render import render_compact, render_json, render_stats
from lib.schema import Report, ScryItem
from lib.score import score_items, sort_items
from lib.source_registry import SourceRegistry

DEBUG = False

TIMEOUT_PROFILES = {
    "quick": {"global": 90, "per_source": 20},
    "default": {"global": 180, "per_source": 45},
    "deep": {"global": 300, "per_source": 75},
}


def log(msg: str):
    if DEBUG:
        sys.stderr.write(f"[scry] {msg}\n")
        sys.stderr.flush()


def _timeout_handler(signum, frame):
    sys.stderr.write("[scry] Global timeout reached. Outputting partial results.\n")
    # Don't exit — let the main thread handle partial results


def parse_args(argv: List[str]) -> Dict[str, Any]:
    args = {
        "topic": "",
        "emit": "compact",
        "depth": "default",
        "days": 30,
        "domain": None,
        "sources": None,
        "tier": None,
        "mock": False,
        "debug": False,
        "no_native_web": False,
    }

    positional = []
    for arg in argv[1:]:
        if arg.startswith("--emit="):
            args["emit"] = arg.split("=", 1)[1]
        elif arg == "--quick":
            args["depth"] = "quick"
        elif arg == "--deep":
            args["depth"] = "deep"
        elif arg.startswith("--days="):
            args["days"] = int(arg.split("=", 1)[1])
        elif arg.startswith("--domain="):
            args["domain"] = arg.split("=", 1)[1]
        elif arg.startswith("--sources="):
            args["sources"] = arg.split("=", 1)[1].split(",")
        elif arg.startswith("--tier="):
            args["tier"] = int(arg.split("=", 1)[1])
        elif arg == "--mock":
            args["mock"] = True
        elif arg == "--debug":
            args["debug"] = True
        elif arg == "--no-native-web":
            args["no_native_web"] = True
        elif not arg.startswith("--"):
            positional.append(arg)

    args["topic"] = " ".join(positional)
    return args


def search_source(source, topic, from_date, to_date, depth, config):
    """Search a single source. Returns (source_id, items, error)."""
    meta = source.meta()
    try:
        raw_items = source.search(topic, from_date, to_date, depth, config)
        # Enrich if not quick mode
        if depth != "quick" and raw_items:
            raw_items = source.enrich(raw_items, depth, config)
        # Normalize to ScryItem
        items = normalize_items(raw_items, meta.id, meta.id_prefix, from_date, to_date)
        return (meta.id, items, None)
    except Exception as e:
        log(f"Error searching {meta.id}: {e}")
        return (meta.id, [], str(e))


def main():
    global DEBUG

    args = parse_args(sys.argv)
    topic = args["topic"]

    if not topic:
        sys.stderr.write("Usage: python3 scry.py <topic> [options]\n")
        sys.exit(1)

    DEBUG = args["debug"]
    if args["debug"]:
        os.environ["SCRY_DEBUG"] = "1"

    # Date range
    from_date, to_date = dates.get_date_range(args["days"])

    # Domain classification
    if args["domain"]:
        domain = args["domain"]
    else:
        domain = get_primary_domain(topic)
    log(f"Topic: {topic}")
    log(f"Domain: {domain}")
    log(f"Date range: {from_date} to {to_date}")

    # Check cache
    source_key = ",".join(args["sources"]) if args["sources"] else ""
    cached = cache.load_cache(topic, from_date, to_date, source_key)
    if cached and not args["mock"]:
        log("Using cached results")
        report = Report.from_dict(cached)
        report.from_cache = True
        report.cache_age_hours = cached.get("_cache_age_hours", 0)
        _output(report, args["emit"])
        return

    # Load config
    config = get_config()
    if args["mock"]:
        config["_mock"] = True

    # Discover sources
    registry = SourceRegistry()
    registry.discover()

    # Select sources
    if args["sources"]:
        sources = registry.get_by_ids(args["sources"], config)
    elif args["tier"]:
        sources = registry.get_by_tier(args["tier"], config)
    else:
        sources = registry.get_available(config)

    log(f"Sources available: {len(sources)}")
    for s in sources:
        log(f"  - {s.meta().id} (tier {s.meta().tier})")

    if not sources:
        sys.stderr.write("[scry] No sources available. Check API keys and binaries.\n")
        sys.exit(1)

    # Set global timeout
    depth = args["depth"]
    timeout_profile = TIMEOUT_PROFILES[depth]

    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, _timeout_handler)
        signal.alarm(timeout_profile["global"])

    # Phase 1: Parallel search across all sources
    all_items: List[ScryItem] = []
    errors: Dict[str, str] = {}
    sources_used: List[str] = []
    sources_skipped: List[str] = []

    max_workers = min(len(sources), 16)
    per_source_timeout = timeout_profile["per_source"]

    sys.stderr.write(f"[scry] Searching {len(sources)} sources for '{topic}' (domain: {domain}, depth: {depth})...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for source in sources:
            future = executor.submit(
                search_source, source, topic, from_date, to_date, depth, config
            )
            futures[future] = source.meta().id

        for future in as_completed(futures, timeout=timeout_profile["global"]):
            source_id = futures[future]
            try:
                sid, items, error = future.result(timeout=per_source_timeout)
                if error:
                    errors[sid] = error
                    sources_skipped.append(sid)
                    sys.stderr.write(f"[scry]   ✗ {sid}: {error}\n")
                elif items:
                    all_items.extend(items)
                    sources_used.append(sid)
                    sys.stderr.write(f"[scry]   ✓ {sid}: {len(items)} items\n")
                else:
                    sources_skipped.append(sid)
                    sys.stderr.write(f"[scry]   - {sid}: 0 items\n")
            except Exception as e:
                errors[source_id] = str(e)
                sources_skipped.append(source_id)
                sys.stderr.write(f"[scry]   ✗ {source_id}: {e}\n")

    # Cancel alarm
    if hasattr(signal, "SIGALRM"):
        signal.alarm(0)

    sys.stderr.write(f"[scry] Collected {len(all_items)} items from {len(sources_used)} sources\n")

    # Filter out items with very low relevance (noise from broad API queries)
    before_filter = len(all_items)
    all_items = [item for item in all_items if item.relevance >= 0.15]
    if len(all_items) < before_filter:
        sys.stderr.write(f"[scry] Filtered {before_filter - len(all_items)} low-relevance items\n")

    # Pipeline: score → dedupe → cross-link → conflict detect
    all_items = score_items(all_items, domain, args["days"])
    all_items = sort_items(all_items)
    all_items = dedupe_items(all_items)
    cross_source_link(all_items)
    conflicts = detect_conflicts(all_items)

    # Build report
    report = Report(
        topic=topic,
        domain=domain,
        range_from=from_date,
        range_to=to_date,
        depth=depth,
        items=all_items,
        sources_used=sources_used,
        sources_skipped=sources_skipped,
        errors=errors,
        conflicts=conflicts,
    )

    # Cache results
    if not args["mock"]:
        cache.save_cache(topic, from_date, to_date, report.to_dict(), source_key)

    _output(report, args["emit"])


def _output(report: Report, emit: str):
    if emit == "json":
        print(render_json(report))
    elif emit == "compact":
        print(render_compact(report))
        print(render_stats(report))
    else:
        print(render_compact(report))


if __name__ == "__main__":
    main()
