#!/usr/bin/env python3
"""RSS/Atom feed digest generator. Fetches, filters, deduplicates, and formats feed items."""

import argparse
import hashlib
import sys
from datetime import datetime, timedelta, timezone

try:
    import feedparser
except ImportError:
    print("Error: feedparser required. Install with: pip3 install feedparser")
    sys.exit(1)


def fetch_feeds(feed_urls, hours=24, keywords=None, exclude=None, limit=50):
    """Fetch items from multiple feeds with filtering."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    seen = set()
    items = []

    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            source = feed.feed.get("title", url)
            for entry in feed.entries:
                # Parse date
                published = None
                for date_field in ("published_parsed", "updated_parsed"):
                    t = entry.get(date_field)
                    if t:
                        try:
                            published = datetime(*t[:6], tzinfo=timezone.utc)
                        except Exception:
                            pass
                        break

                if published and published < cutoff:
                    continue

                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                summary = entry.get("summary", "").strip()[:500]

                # Dedup by title hash
                title_hash = hashlib.md5(title.encode()).hexdigest()
                if title_hash in seen:
                    continue
                seen.add(title_hash)

                # Keyword filter
                text = f"{title} {summary}".lower()
                if keywords:
                    if not any(kw.lower() in text for kw in keywords):
                        continue
                if exclude:
                    if any(kw.lower() in text for kw in exclude):
                        continue

                items.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "source": source,
                    "published": published,
                })
        except Exception as e:
            print(f"Warning: Failed to fetch {url}: {e}", file=sys.stderr)

    # Sort by date (newest first)
    items.sort(key=lambda x: x.get("published") or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return items[:limit]


def format_markdown(items, title="Feed Digest"):
    """Format items as Markdown."""
    lines = [f"# {title}\n"]
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append(f"*{len(items)} items*\n")

    for i, item in enumerate(items, 1):
        date_str = item["published"].strftime("%m/%d %H:%M") if item.get("published") else "?"
        lines.append(f"### {i}. [{item['title']}]({item['link']})")
        lines.append(f"**{item['source']}** · {date_str}\n")
        if item["summary"]:
            # Strip HTML tags roughly
            import re
            clean = re.sub(r"<[^>]+>", "", item["summary"])[:200]
            lines.append(f"> {clean}...\n")

    return "\n".join(lines)


def format_text(items):
    """Format items as plain text."""
    lines = []
    for i, item in enumerate(items, 1):
        date_str = item["published"].strftime("%m/%d %H:%M") if item.get("published") else "?"
        lines.append(f"{i}. [{date_str}] {item['title']}")
        lines.append(f"   {item['link']}")
        lines.append(f"   Source: {item['source']}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="RSS/Atom Feed Digest")
    sub = parser.add_subparsers(dest="command")

    fetch = sub.add_parser("fetch", help="Fetch and filter feeds")
    fetch.add_argument("--feeds", nargs="+", help="Feed URLs")
    fetch.add_argument("--feed-file", help="File with feed URLs (one per line)")
    fetch.add_argument("--hours", type=int, default=24, help="Look back N hours (default: 24)")
    fetch.add_argument("--keywords", help="Comma-separated include keywords")
    fetch.add_argument("--exclude", help="Comma-separated exclude keywords")
    fetch.add_argument("--limit", type=int, default=50, help="Max items (default: 50)")
    fetch.add_argument("--output", help="Output file (default: stdout)")
    fetch.add_argument("--format", choices=["markdown", "text"], default="markdown")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    feed_urls = args.feeds or []
    if args.feed_file:
        with open(args.feed_file) as f:
            feed_urls.extend(line.strip() for line in f if line.strip() and not line.startswith("#"))

    if not feed_urls:
        print("Error: No feed URLs provided. Use --feeds or --feed-file.")
        sys.exit(1)

    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None
    exclude = [k.strip() for k in args.exclude.split(",")] if args.exclude else None

    items = fetch_feeds(feed_urls, args.hours, keywords, exclude, args.limit)

    if args.format == "markdown":
        output = format_markdown(items)
    else:
        output = format_text(items)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(items)} items to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
