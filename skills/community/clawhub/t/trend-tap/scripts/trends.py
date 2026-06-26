#!/usr/bin/env python3
"""
Trend Tap — main entry point.
Aggregates trending topics from 7 platforms concurrently.
Zero external dependencies. Zero API keys.
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

from sources import twitter, reddit, google, hackernews, zhihu, bilibili, weibo

_ALL_SOURCES = {
    "twitter":    twitter,
    "reddit":     reddit,
    "google":     google,
    "hackernews": hackernews,
    "zhihu":      zhihu,
    "bilibili":   bilibili,
    "weibo":      weibo,
}

_SOURCE_ORDER = ["twitter", "reddit", "google", "hackernews", "zhihu", "bilibili", "weibo"]


_MAX_RETRIES = 2
_RETRY_DELAY = 1.5


def _fetch_source(name: str, module, top: int, region: str, timeout: int) -> dict:
    """Wrapper: call module.fetch() with retry on failure."""
    kwargs: dict = {"top": top, "timeout": timeout}
    if name in ("twitter", "google") and region:
        kwargs["region"] = region

    last_err = ""
    for attempt in range(_MAX_RETRIES + 1):
        try:
            result = module.fetch(**kwargs)
            if result.get("error") and attempt < _MAX_RETRIES:
                last_err = result["error"]
                time.sleep(_RETRY_DELAY)
                continue
            return result
        except Exception as e:
            last_err = str(e)
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)
                continue

    return {
        "source": name,
        "label": name,
        "emoji": "❓",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "error": "Failed after {} retries: {}".format(_MAX_RETRIES + 1, last_err),
        "items": [],
    }


def fetch_all(sources: Optional[List[str]] = None, top: int = 10,
              region: str = "", timeout: int = 12) -> List[dict]:
    """Fetch from multiple sources concurrently."""
    if not sources:
        sources = list(_SOURCE_ORDER)

    results_map: Dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=len(sources)) as pool:
        futures = {}
        for name in sources:
            mod = _ALL_SOURCES.get(name)
            if not mod:
                continue
            futures[pool.submit(_fetch_source, name, mod, top, region, timeout)] = name

        for future in as_completed(futures):
            name = futures[future]
            try:
                results_map[name] = future.result()
            except Exception as e:
                results_map[name] = {
                    "source": name, "error": str(e), "items": [],
                    "fetched_at": datetime.now(timezone.utc).isoformat(),
                }

    return [results_map[s] for s in sources if s in results_map]


def format_overview(results: List[dict]) -> str:
    """One-line-per-platform summary for progressive disclosure."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"📡 Trend Tap — {now}", ""]

    for r in results:
        emoji = r.get("emoji", "•")
        label = r.get("label", r.get("source", "?"))

        if r.get("error"):
            lines.append(f"{emoji} {label}: ⚠️ {r['error']}")
            continue

        items = r.get("items", [])
        if not items:
            lines.append(f"{emoji} {label}: (no data)")
            continue

        top_item = items[0]
        title = top_item.get("title", "")
        detail = _overview_detail(r["source"], top_item)
        lines.append(f"{emoji} {label}: {title}{detail}")

    lines.append("")
    lines.append("Want to see more from any platform? Tell me which one (e.g. \"show reddit top 10\").")
    return "\n".join(lines)


def _overview_detail(source: str, item: dict) -> str:
    """Build a short detail suffix for the overview line."""
    parts = []
    if source == "reddit":
        sub = item.get("subreddit", "")
        score = item.get("score", 0)
        if sub:
            parts.append(sub)
        if score:
            parts.append(f"{_human_number(score)} upvotes")
    elif source == "hackernews":
        score = item.get("score", 0)
        if score:
            parts.append(f"{score} points")
    elif source == "google":
        traffic = item.get("traffic", "")
        if traffic:
            parts.append(traffic)
    elif source == "zhihu":
        heat = item.get("heat", "")
        if heat:
            parts.append(heat)
    elif source == "bilibili":
        views = item.get("views", 0)
        if views:
            parts.append(f"{_human_number(views)} views")
    elif source == "weibo":
        label = item.get("label", "")
        heat = item.get("heat", "")
        if label:
            parts.append(label)
        elif heat:
            parts.append(f"热度 {_human_number(int(heat))}" if heat.isdigit() else heat)

    return f" — {', '.join(parts)}" if parts else ""


def format_detail(results: List[dict]) -> str:
    """Full per-platform listing with rank, title, link, metric."""
    sections = []
    for r in results:
        emoji = r.get("emoji", "•")
        label = r.get("label", r.get("source", "?"))
        header = f"{emoji} {label}"

        if r.get("error"):
            sections.append(f"{header}\n  ⚠️ {r['error']}")
            continue

        items = r.get("items", [])
        if not items:
            sections.append(f"{header}\n  (no data)")
            continue

        lines = [header]
        for item in items:
            rank = item.get("rank", "")
            title = item.get("title", "")
            url = item.get("url", "")
            metric = _detail_metric(r["source"], item)

            if url:
                line = "  {rank:>2}. [{title}]({url})".format(rank=rank, title=title, url=url)
            else:
                line = "  {rank:>2}. {title}".format(rank=rank, title=title)
            if metric:
                line += "  ({})".format(metric)
            lines.append(line)

        sections.append("\n".join(lines))

    return "\n\n".join(sections)


def _detail_metric(source: str, item: dict) -> str:
    """Build a metric string for detail view."""
    if source == "reddit":
        parts = []
        sub = item.get("subreddit", "")
        if sub:
            parts.append(sub)
        score = item.get("score", 0)
        if score:
            parts.append(f"↑{_human_number(score)}")
        comments = item.get("comments", 0)
        if comments:
            parts.append(f"💬{_human_number(comments)}")
        return " · ".join(parts)
    elif source == "hackernews":
        parts = []
        score = item.get("score", 0)
        if score:
            parts.append(f"{score}pts")
        comments = item.get("comments", 0)
        if comments:
            parts.append(f"💬{comments}")
        return " · ".join(parts)
    elif source == "google":
        parts = []
        traffic = item.get("traffic", "")
        if traffic:
            parts.append(traffic)
        news = item.get("related_news", "")
        if news:
            parts.append(news[:60])
        return " · ".join(parts)
    elif source == "zhihu":
        heat = item.get("heat", "")
        return heat
    elif source == "bilibili":
        parts = []
        views = item.get("views", 0)
        if views:
            parts.append(f"▶{_human_number(views)}")
        author = item.get("author", "")
        if author:
            parts.append(author)
        return " · ".join(parts)
    elif source == "weibo":
        parts = []
        label = item.get("label", "")
        if label:
            parts.append(label)
        heat = item.get("heat", "")
        if heat and heat.isdigit():
            parts.append(f"热度{_human_number(int(heat))}")
        return " ".join(parts)
    return ""


def _human_number(n: int) -> str:
    """Convert large numbers to human-readable: 15200 -> 15.2K."""
    if n >= 100_000_000:
        return f"{n / 100_000_000:.1f}亿"
    if n >= 10_000_000:
        return f"{n / 10_000:.0f}万"
    if n >= 10_000:
        return f"{n / 10_000:.1f}万"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _save_daily(results: List[dict], out_dir: Path):
    """Save results to daily archive for scheduled briefings."""
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = out_dir / f"trends_{date_str}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Trend Tap — aggregate trending topics from 7 platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode", choices=["overview", "detail", "all"], default="overview",
        help="overview = 1-line per platform (default); detail = expanded; all = every platform expanded",
    )
    parser.add_argument(
        "--source", default="",
        help="Comma-separated source IDs: twitter,reddit,google,hackernews,zhihu,bilibili,weibo",
    )
    parser.add_argument("--top", type=int, default=10, help="Number of items per source (default: 10)")
    parser.add_argument("--region", default="", help="Region filter for twitter/google (e.g. US, CN, japan)")
    parser.add_argument("--timeout", type=int, default=12, help="HTTP timeout per request in seconds")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")
    parser.add_argument("--save", action="store_true", help="Save results to ~/.openclaw/trend-tap/daily/")

    args = parser.parse_args()

    sources = [s.strip() for s in args.source.split(",") if s.strip()] if args.source else None

    mode = args.mode
    if sources and mode == "overview":
        mode = "detail"

    if mode == "overview":
        top = 1
    elif mode == "all":
        sources = None
        top = args.top
    else:
        top = args.top

    t0 = time.monotonic()
    results = fetch_all(sources=sources, top=top, region=args.region, timeout=args.timeout)
    elapsed = time.monotonic() - t0

    if args.save:
        daily_dir = Path.home() / ".openclaw" / "trend-tap" / "daily"
        path = _save_daily(results, daily_dir)
        print("💾 Saved to {}".format(path), file=sys.stderr)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif mode == "overview":
        print(format_overview(results))
    else:
        print(format_detail(results))

    ok = sum(1 for r in results if not r.get("error"))
    total = len(results)
    print(f"\n⏱ {ok}/{total} sources fetched in {elapsed:.1f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
