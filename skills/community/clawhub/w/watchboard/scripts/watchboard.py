#!/usr/bin/env python3
"""
Watchboard CLI — Query intelligence dashboards from watchboard.dev

Public API v1 — no API key needed, CORS enabled, cached 1h server-side.

Usage:
    python3 watchboard.py list [--domain X] [--status X]
    python3 watchboard.py summary <slug>
    python3 watchboard.py breaking
    python3 watchboard.py events <slug> [--limit N]
    python3 watchboard.py kpis <slug>
    python3 watchboard.py search <query> [--tracker slug]
    python3 watchboard.py detail <slug>
    python3 watchboard.py rss <slug>

Add --json to any command for raw JSON output.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import re
import os
import time
from pathlib import Path

BASE_URL = "https://watchboard.dev"
API_V1 = f"{BASE_URL}/api/v1"
CACHE_DIR = Path("/tmp/watchboard-cache")
CACHE_TTL = 3600  # 1 hour (matches server cache)

# ─── Caching ───────────────────────────────────────────────────────────────────

def cached_fetch(url: str, force: bool = False) -> bytes:
    """Fetch URL with local file cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r'[^\w\-.]', '_', url.replace('https://', ''))
    cache_file = CACHE_DIR / safe_name

    if not force and cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < CACHE_TTL:
            return cache_file.read_bytes()

    req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Watchboard/2.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        cache_file.write_bytes(data)
        return data
    except urllib.error.HTTPError as e:
        print(json.dumps({"error": f"HTTP {e.code}", "url": url}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e), "url": url}))
        sys.exit(1)


def fetch_api(endpoint: str) -> dict:
    """Fetch a JSON endpoint from the v1 API."""
    url = f"{API_V1}/{endpoint}"
    return json.loads(cached_fetch(url))


def fetch_rss(slug: str = None) -> str:
    """Fetch RSS feed (kept as fallback)."""
    if slug:
        url = f"{BASE_URL}/{slug}/rss"
    else:
        url = f"{BASE_URL}/rss"
    return cached_fetch(url).decode("utf-8")


def parse_rss(xml_text: str) -> list:
    root = ET.fromstring(xml_text)
    items = []
    for item in root.findall(".//item"):
        items.append({
            "title": (item.find("title").text or "").strip() if item.find("title") is not None else "",
            "link": (item.find("link").text or "").strip() if item.find("link") is not None else "",
            "description": (item.find("description").text or "").strip() if item.find("description") is not None else "",
            "pubDate": (item.find("pubDate").text or "").strip() if item.find("pubDate") is not None else "",
        })
    return items


# ─── Tracker directory (cached) ───────────────────────────────────────────────

_tracker_cache = None

def get_trackers() -> list:
    """Fetch tracker directory from API (cached in-memory + disk)."""
    global _tracker_cache
    if _tracker_cache is not None:
        return _tracker_cache
    data = fetch_api("trackers.json")
    _tracker_cache = data.get("trackers", [])
    return _tracker_cache


def resolve_slug(input_str: str) -> str:
    """Resolve a tracker name/slug to canonical slug using the live directory."""
    lower = input_str.lower().strip()
    trackers = get_trackers()

    # Direct match
    for t in trackers:
        if t["slug"] == lower:
            return lower

    # Fuzzy: substring match on slug or name
    candidates = []
    for t in trackers:
        if lower in t["slug"] or lower in t.get("name", "").lower() or lower in t.get("shortName", "").lower():
            candidates.append(t["slug"])

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        print(json.dumps({
            "error": f"Ambiguous tracker '{input_str}'",
            "candidates": candidates
        }))
        sys.exit(1)

    # Tag search as last resort
    for t in trackers:
        tags = [tag.lower() for tag in t.get("tags", [])]
        if lower in tags:
            candidates.append(t["slug"])
    if len(candidates) == 1:
        return candidates[0]

    print(json.dumps({
        "error": f"Tracker '{input_str}' not found",
        "hint": "Use 'watchboard.py list' to see available trackers"
    }))
    sys.exit(1)


# ─── Formatters ────────────────────────────────────────────────────────────────

def fmt_tracker_line(t: dict) -> str:
    """Format a single tracker for list display."""
    icon = t.get("icon", "")
    slug = t["slug"]
    domain = t.get("domain", "")
    status = t.get("status", "")
    updated = t.get("lastUpdated", "")[:10]
    breaking = " 🔴 BREAKING" if t.get("breaking") else ""
    return f"  {icon} {slug:<40} {domain:<14} {status:<8} {updated}{breaking}"


def fmt_kpi(kpi: dict) -> str:
    """Format a single KPI for display."""
    label = kpi.get("label", "")
    value = kpi.get("value", "")
    delta = kpi.get("delta", "")
    trend = kpi.get("trend", "")
    contested = " ⚠️ CONTESTED" if kpi.get("contested") else ""
    delta_str = f" ({delta})" if delta else ""
    return f"  • {label}: {value}{delta_str}{contested}"


def fmt_event(ev: dict) -> str:
    """Format a single event for display."""
    date = ev.get("date", "")
    title = ev.get("title", "")
    etype = ev.get("type", "")
    sources = ev.get("sources", [])
    src_str = ", ".join(s.get("name", "") for s in sources[:3]) if sources else ""
    return f"  [{date}] [{etype}] {title}" + (f"\n    Sources: {src_str}" if src_str else "")


def fmt_breaking(item: dict) -> str:
    """Format a breaking tracker item."""
    icon = item.get("icon", "")
    slug = item.get("slug", "")
    headline = item.get("headline", "")
    return f"  {icon} {slug}: {headline}"


# ─── Commands ──────────────────────────────────────────────────────────────────

def cmd_list(args):
    """List all available trackers from the live directory."""
    trackers = get_trackers()

    # Optional filters
    if args.domain:
        trackers = [t for t in trackers if t.get("domain", "").lower() == args.domain.lower()]
    if args.status:
        trackers = [t for t in trackers if t.get("status", "").lower() == args.status.lower()]

    if args.json:
        print(json.dumps({"trackers": trackers, "count": len(trackers)}, indent=2))
        return

    domains = sorted(set(t.get("domain", "unknown") for t in trackers))
    print(f"Watchboard — {len(trackers)} trackers across {len(domains)} domains\n")
    print(f"  {'SLUG':<40} {'DOMAIN':<14} {'STATUS':<8} UPDATED")
    print(f"  {'─' * 40} {'─' * 14} {'─' * 8} {'─' * 10}")
    for t in sorted(trackers, key=lambda x: (x.get("domain", ""), x["slug"])):
        print(fmt_tracker_line(t))


def cmd_summary(args):
    """Get summary for a tracker: meta + latest digest + top KPIs."""
    slug = resolve_slug(args.tracker)
    data = fetch_api(f"trackers/{slug}.json")

    if args.json:
        print(json.dumps(data, indent=2))
        return

    config = data.get("config", {})
    meta = data.get("meta", {})
    digest = data.get("latestDigest", {})
    kpis = data.get("kpis", [])

    print(f"{config.get('icon', '')} {config.get('name', slug)}")
    print(f"  {config.get('description', '')}")
    print()

    if meta.get("dateline"):
        print(f"📅 {meta['dateline']}")
    if meta.get("heroHeadline"):
        print(f"📰 {meta['heroHeadline']}")
    if meta.get("heroSubtitle"):
        print(f"  {meta['heroSubtitle']}")
    print()

    if digest:
        print(f"📋 Latest Digest ({digest.get('date', 'N/A')}):")
        if digest.get("title"):
            print(f"  {digest['title']}")
        if digest.get("summary"):
            print(f"  {digest['summary']}")
        print()

    if kpis:
        print(f"📊 Key Performance Indicators ({len(kpis)}):")
        for kpi in kpis[:10]:
            print(fmt_kpi(kpi))
        if len(kpis) > 10:
            print(f"  ... and {len(kpis) - 10} more (use 'kpis {slug}' for all)")
    print()

    event_count = data.get("eventCount", 0)
    print(f"📈 {event_count} total events tracked")
    if meta.get("breaking"):
        print("🔴 BREAKING — active developments")
    print(f"\n🔗 {BASE_URL}/{slug}")


def cmd_breaking(args):
    """Show trackers with breaking news."""
    data = fetch_api("breaking.json")
    items = data.get("items", [])

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(f"🔴 BREAKING — {len(items)} active trackers\n")
    for item in items:
        print(fmt_breaking(item))
        subtitle = item.get("subtitle", "")
        if subtitle:
            # Truncate long subtitles for readability
            if len(subtitle) > 200:
                subtitle = subtitle[:200] + "..."
            print(f"    {subtitle}")
        print()


def cmd_events(args):
    """Get recent events for a tracker."""
    slug = resolve_slug(args.tracker)
    data = fetch_api(f"events/{slug}.json")
    events = data.get("events", [])
    total = data.get("total", len(events))

    if args.limit:
        events = events[:args.limit]

    if args.json:
        print(json.dumps({"slug": slug, "total": total, "events": events}, indent=2))
        return

    print(f"📰 Events for {slug} — showing {len(events)} of {total}\n")
    for ev in events:
        print(fmt_event(ev))
        detail = ev.get("detail", "")
        if detail:
            if len(detail) > 300:
                detail = detail[:300] + "..."
            print(f"    {detail}")
        print()


def cmd_kpis(args):
    """Get KPIs for a tracker."""
    slug = resolve_slug(args.tracker)
    data = fetch_api(f"kpis/{slug}.json")
    kpis = data.get("kpis", [])

    if args.json:
        print(json.dumps(data, indent=2))
        return

    print(f"📊 KPIs for {slug} (updated {data.get('lastUpdated', 'N/A')[:10]})\n")
    for kpi in kpis:
        print(fmt_kpi(kpi))
        if kpi.get("contested") and kpi.get("contestNote"):
            note = kpi["contestNote"]
            if len(note) > 300:
                note = note[:300] + "..."
            print(f"    ⚠️  {note}")
        print()


def cmd_search(args):
    """Search events across all trackers (or one) using the search index."""
    data = fetch_api("search-index.json")
    events = data.get("events", [])
    query = args.query.lower()

    # Filter by tracker if specified
    if args.tracker:
        slug = resolve_slug(args.tracker)
        events = [e for e in events if e.get("slug") == slug]

    # Client-side keyword search
    results = []
    for ev in events:
        text = f"{ev.get('title', '')} {ev.get('slug', '')}".lower()
        if query in text:
            results.append(ev)

    if args.json:
        print(json.dumps({
            "query": args.query,
            "tracker": args.tracker if args.tracker else "all",
            "results": results[:args.limit],
            "total_matches": len(results),
        }, indent=2))
        return

    print(f"🔍 Search: \"{args.query}\"" + (f" in {args.tracker}" if args.tracker else " (all trackers)"))
    print(f"   {len(results)} matches found\n")
    for ev in results[:args.limit]:
        slug = ev.get("slug", "")
        date = ev.get("date", "")
        title = ev.get("title", "")
        etype = ev.get("type", "")
        print(f"  [{date}] [{etype}] {slug}: {title}")


def cmd_detail(args):
    """Get full tracker data (config, meta, kpis, digest, events, counts)."""
    slug = resolve_slug(args.tracker)
    data = fetch_api(f"trackers/{slug}.json")

    if args.json:
        print(json.dumps(data, indent=2))
        return

    config = data.get("config", {})
    meta = data.get("meta", {})
    digest = data.get("latestDigest", {})
    kpis = data.get("kpis", [])
    events = data.get("recentEvents", [])
    event_count = data.get("eventCount", 0)

    # Config
    print(f"{'═' * 60}")
    print(f"{config.get('icon', '')} {config.get('name', slug)}")
    print(f"{'═' * 60}")
    print(f"  Slug:    {config.get('slug', '')}")
    print(f"  Domain:  {config.get('domain', '')} / {config.get('region', '')}")
    print(f"  Status:  {config.get('status', '')} ({config.get('temporal', '')})")
    print(f"  Started: {config.get('startDate', 'N/A')}")
    if config.get("endDate"):
        print(f"  Ended:   {config['endDate']}")
    print(f"  {config.get('description', '')}")
    print()

    # Meta
    if meta:
        if meta.get("dateline"):
            print(f"📅 {meta['dateline']}")
        if meta.get("heroHeadline"):
            print(f"📰 {meta['heroHeadline']}")
        if meta.get("heroSubtitle"):
            print(f"  {meta['heroSubtitle']}")
        if meta.get("breaking"):
            print("🔴 BREAKING — active developments")
        print()

    # Digest
    if digest:
        print(f"📋 Latest Digest ({digest.get('date', 'N/A')}):")
        if digest.get("title"):
            print(f"  {digest['title']}")
        if digest.get("summary"):
            print(f"  {digest['summary']}")
        if digest.get("sectionsUpdated"):
            print(f"  Sections updated: {', '.join(digest['sectionsUpdated'])}")
        print()

    # KPIs
    if kpis:
        print(f"📊 KPIs ({len(kpis)}):")
        for kpi in kpis:
            print(fmt_kpi(kpi))
        print()

    # Recent events
    if events:
        print(f"📰 Recent Events (showing {len(events)} of {event_count}):")
        for ev in events[:15]:
            print(fmt_event(ev))
        if len(events) > 15:
            print(f"  ... {len(events) - 15} more (use 'events {slug}' for full list)")
        print()

    # Footer
    if meta.get("footerNote"):
        print(f"ℹ️  {meta['footerNote']}")
    print(f"\n🔗 {BASE_URL}/{slug}")


def cmd_rss(args):
    """Raw RSS feed for a tracker (fallback)."""
    slug = resolve_slug(args.tracker)
    items = parse_rss(fetch_rss(slug))

    if args.json:
        print(json.dumps({"tracker": slug, "items": items}, indent=2))
        return

    print(f"📡 RSS for {slug} — {len(items)} items\n")
    for item in items:
        print(f"  [{item.get('pubDate', '')}] {item.get('title', '')}")
        if item.get("description"):
            desc = item["description"]
            if len(desc) > 200:
                desc = desc[:200] + "..."
            print(f"    {desc}")
        print()


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Watchboard Intelligence Dashboard CLI v2")
    parser.add_argument("--json", action="store_true", help="Raw JSON output")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p = sub.add_parser("list", help="List all trackers")
    p.add_argument("--domain", help="Filter by domain (conflict, governance, culture, etc.)")
    p.add_argument("--status", help="Filter by status (active, archived)")

    # summary
    p = sub.add_parser("summary", help="Summary: meta + digest + top KPIs")
    p.add_argument("tracker", help="Tracker slug or name")

    # breaking
    sub.add_parser("breaking", help="Trackers with breaking news")

    # events
    p = sub.add_parser("events", help="Recent events for a tracker")
    p.add_argument("tracker", help="Tracker slug or name")
    p.add_argument("--limit", type=int, default=30, help="Max events (default 30)")

    # kpis
    p = sub.add_parser("kpis", help="KPIs for a tracker")
    p.add_argument("tracker", help="Tracker slug or name")

    # search
    p = sub.add_parser("search", help="Search events across trackers")
    p.add_argument("query", help="Search query")
    p.add_argument("--tracker", help="Limit search to one tracker")
    p.add_argument("--limit", type=int, default=20, help="Max results (default 20)")

    # detail
    p = sub.add_parser("detail", help="Full tracker data (all sections)")
    p.add_argument("tracker", help="Tracker slug or name")

    # rss (fallback)
    p = sub.add_parser("rss", help="RSS feed (fallback)")
    p.add_argument("tracker", help="Tracker slug or name")

    args = parser.parse_args()

    commands = {
        "list": cmd_list,
        "summary": cmd_summary,
        "breaking": cmd_breaking,
        "events": cmd_events,
        "kpis": cmd_kpis,
        "search": cmd_search,
        "detail": cmd_detail,
        "rss": cmd_rss,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
