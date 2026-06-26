"""Output rendering for SCRY skill."""

import json
from typing import Dict, List, Optional

from .schema import Report, ScryItem
from .source_base import SourceMeta

# Source display order and emoji
SOURCE_DISPLAY = {
    "hackernews": ("Hacker News", "🟡"),
    "lobsters": ("Lobsters", "🦞"),
    "devto": ("Dev.to", "📝"),
    "github": ("GitHub", "🐙"),
    "gitlab": ("GitLab", "🦊"),
    "arxiv": ("ArXiv", "📄"),
    "semantic_scholar": ("Semantic Scholar", "🎓"),
    "openalex": ("OpenAlex", "📚"),
    "bluesky": ("Bluesky", "🦋"),
    "mastodon": ("Mastodon", "🐘"),
    "wikipedia": ("Wikipedia", "📖"),
    "gdelt": ("GDELT", "🌍"),
    "techmeme": ("Techmeme", "📰"),
    "polymarket": ("Polymarket", "📊"),
    "sec_edgar": ("SEC EDGAR", "🏛️"),
    "coingecko": ("CoinGecko", "🪙"),
    "reddit": ("Reddit", "🟠"),
    "x_twitter": ("X", "🔵"),
    "youtube": ("YouTube", "🔴"),
    "tiktok": ("TikTok", "🎵"),
    "instagram": ("Instagram", "📸"),
    "product_hunt": ("Product Hunt", "🚀"),
    "stackoverflow": ("Stack Overflow", "📋"),
    "threads": ("Threads", "🧵"),
    "huggingface": ("HuggingFace", "🤗"),
    "substack": ("Substack", "📬"),
    "google_news": ("Google News", "📰"),
    "websearch": ("Web", "🌐"),
}


def _format_engagement(item: ScryItem) -> str:
    """Format engagement metrics for display."""
    eng = item.engagement
    if not eng:
        return ""

    parts = []
    sid = item.source_id

    if sid in ("reddit",):
        if eng.score is not None:
            parts.append(f"{eng.score}pts")
        if eng.num_comments is not None:
            parts.append(f"{eng.num_comments}cmt")

    elif sid in ("x_twitter", "bluesky", "mastodon", "threads"):
        if eng.likes is not None:
            parts.append(f"{eng.likes}likes")
        if eng.reposts is not None:
            parts.append(f"{eng.reposts}rt")
        if eng.replies is not None:
            parts.append(f"{eng.replies}replies")

    elif sid in ("youtube", "tiktok", "instagram"):
        if eng.views is not None:
            parts.append(f"{eng.views}views")
        if eng.likes is not None:
            parts.append(f"{eng.likes}likes")
        if eng.num_comments is not None:
            parts.append(f"{eng.num_comments}cmt")

    elif sid in ("hackernews", "lobsters"):
        if eng.score is not None:
            parts.append(f"{eng.score}pts")
        if eng.num_comments is not None:
            parts.append(f"{eng.num_comments}cmt")

    elif sid in ("github", "gitlab"):
        if eng.stars is not None:
            parts.append(f"{eng.stars}★")
        if eng.forks is not None:
            parts.append(f"{eng.forks}forks")

    elif sid in ("arxiv", "semantic_scholar", "openalex"):
        if eng.citations is not None:
            parts.append(f"{eng.citations}citations")

    elif sid in ("polymarket",):
        if eng.volume is not None:
            parts.append(f"${eng.volume:,.0f}vol")

    elif sid in ("devto", "stackoverflow"):
        if eng.score is not None:
            parts.append(f"{eng.score}pts")
        if eng.likes is not None:
            parts.append(f"{eng.likes}likes")
        if eng.num_comments is not None:
            parts.append(f"{eng.num_comments}cmt")

    elif sid in ("huggingface",):
        if eng.downloads is not None:
            parts.append(f"{eng.downloads}dl")
        if eng.likes is not None:
            parts.append(f"{eng.likes}likes")

    elif sid in ("product_hunt",):
        if eng.score is not None:
            parts.append(f"{eng.score}votes")
        if eng.num_comments is not None:
            parts.append(f"{eng.num_comments}cmt")

    elif sid in ("coingecko",):
        if eng.volume is not None:
            parts.append(f"${eng.volume:,.0f}vol")

    return f"[{', '.join(parts)}]" if parts else ""


def render_compact(report: Report, limit: int = 15) -> str:
    """Render report in compact format for assistant synthesis."""
    lines = []
    lines.append(f"## SCRY Research Results: {report.topic}")
    lines.append(f"**Domain:** {report.domain}")
    lines.append(f"**Date Range:** {report.range_from} to {report.range_to}")
    lines.append(f"**Depth:** {report.depth}")
    lines.append(f"**Sources used:** {len(report.sources_used)} | **Skipped:** {len(report.sources_skipped)}")

    if report.from_cache:
        lines.append(f"**⚠️ Cached results** (age: {report.cache_age_hours:.1f}h)")

    if report.errors:
        lines.append("")
        lines.append("**Errors:**")
        for src, err in report.errors.items():
            name, _ = SOURCE_DISPLAY.get(src, (src, ""))
            lines.append(f"  - {name}: {err}")

    # Group items by source
    source_order = list(SOURCE_DISPLAY.keys())
    seen_sources = set()

    for source_id in source_order:
        source_items = report.items_by_source(source_id)
        if not source_items:
            continue

        seen_sources.add(source_id)
        name, emoji = SOURCE_DISPLAY.get(source_id, (source_id, ""))
        lines.append("")
        lines.append(f"### {emoji} {name}")

        for item in source_items[:limit]:
            eng_str = _format_engagement(item)
            xref = ""
            if item.cross_refs:
                xref = f" [also on: {', '.join(item.cross_refs)}]"

            author_str = ""
            if item.author:
                if item.source_id in ("reddit",):
                    author_str = f" r/{item.extras.get('subreddit', '')}"
                elif item.source_id in ("x_twitter", "bluesky", "mastodon", "threads",
                                        "tiktok", "instagram"):
                    author_str = f" @{item.author}"
                elif item.source_id in ("youtube",):
                    author_str = f" {item.author}"
                else:
                    author_str = f" {item.author}"

            date_str = f" ({item.date})" if item.date else ""

            lines.append(f"**{item.id}** (score:{item.score}){author_str}{date_str} {eng_str}{xref}")
            lines.append(f"  {item.title[:200]}")
            lines.append(f"  {item.url}")

            if item.snippet:
                lines.append(f"  *{item.snippet[:200]}*")

            if item.why_relevant:
                lines.append(f"  Why: {item.why_relevant}")

            # Source-specific extras
            extras = item.extras
            if extras.get("top_comments"):
                lines.append("  Insights:")
                for cmt in extras["top_comments"][:3]:
                    if isinstance(cmt, dict):
                        lines.append(f"    - {cmt.get('text', '')[:150]}")
                    else:
                        lines.append(f"    - {str(cmt)[:150]}")

            if extras.get("outcome_prices"):
                lines.append(f"  Odds: {extras['outcome_prices']}")

            if extras.get("abstract"):
                lines.append(f"  Abstract: {extras['abstract'][:200]}")

    # Conflicts section
    if report.conflicts:
        lines.append("")
        lines.append("### ⚠️ Conflicts Detected")
        for conflict in report.conflicts:
            lines.append(f"  - **{conflict['title']}**: {conflict['detail']}")

    lines.append("")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    """Render report as JSON."""
    return json.dumps(report.to_dict(), indent=2, default=str)


def render_stats(report: Report) -> str:
    """Render stats summary block for display."""
    lines = []
    lines.append("---")
    lines.append("✅ All agents reported back!")

    source_order = list(SOURCE_DISPLAY.keys())
    for source_id in source_order:
        items = report.items_by_source(source_id)
        if not items:
            continue

        name, emoji = SOURCE_DISPLAY.get(source_id, (source_id, ""))
        count = len(items)

        # Aggregate engagement
        total_eng = {}
        for item in items:
            if not item.engagement:
                continue
            eng = item.engagement
            for field in ("score", "likes", "views", "num_comments", "reposts",
                          "stars", "forks", "citations", "downloads", "volume"):
                val = getattr(eng, field, None)
                if val is not None:
                    total_eng[field] = total_eng.get(field, 0) + val

        stats_parts = [f"{count} items"]
        if "score" in total_eng and source_id in ("reddit", "hackernews", "lobsters", "devto", "stackoverflow"):
            stats_parts.append(f"{total_eng['score']} pts")
        if "likes" in total_eng:
            stats_parts.append(f"{total_eng['likes']} likes")
        if "views" in total_eng:
            stats_parts.append(f"{total_eng['views']} views")
        if "num_comments" in total_eng:
            stats_parts.append(f"{total_eng['num_comments']} comments")
        if "stars" in total_eng:
            stats_parts.append(f"{total_eng['stars']}★")
        if "citations" in total_eng:
            stats_parts.append(f"{total_eng['citations']} citations")
        if "volume" in total_eng:
            stats_parts.append(f"${total_eng['volume']:,.0f} vol")

        prefix = "├─" if source_id != source_order[-1] else "└─"
        lines.append(f"{prefix} {emoji} {name}: {' │ '.join(stats_parts)}")

    # Top voices
    top_voices = []
    for item in sorted(report.items, key=lambda x: x.score, reverse=True)[:5]:
        if item.author:
            if item.source_id in ("x_twitter", "bluesky", "mastodon", "threads",
                                    "tiktok", "instagram"):
                top_voices.append(f"@{item.author}")
            elif item.source_id in ("reddit",):
                sub = item.extras.get("subreddit", "")
                if sub:
                    top_voices.append(f"r/{sub}")
            elif item.source_id in ("hackernews", "lobsters"):
                top_voices.append(item.author)
    if top_voices:
        lines.append(f"└─ 🗣️ Top voices: {', '.join(dict.fromkeys(top_voices))}")

    lines.append("---")
    return "\n".join(lines)
