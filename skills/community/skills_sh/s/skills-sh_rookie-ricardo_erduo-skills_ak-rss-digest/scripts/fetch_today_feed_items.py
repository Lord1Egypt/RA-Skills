#!/usr/bin/env python3

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import re
import ssl
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path


USER_AGENT = "Mozilla/5.0 (compatible; ak-rss-digest/1.0; +https://openai.com)"
ACCEPT = "application/rss+xml, application/atom+xml, application/xml, text/xml, */*;q=0.8"
DEFAULT_TIMEOUT = 15
DEFAULT_TZ = "Asia/Shanghai"
DEFAULT_DAYS = 7


def local_name(tag):
    return tag.rsplit("}", 1)[-1]


def strip_html(raw):
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def first_text(parent, names):
    for child in parent:
        if local_name(child.tag) in names:
            text = "".join(child.itertext()).strip()
            if text:
                return text
    return ""


def first_link(entry):
    for child in entry:
        if local_name(child.tag) != "link":
            continue
        href = child.attrib.get("href")
        rel = child.attrib.get("rel", "alternate")
        if href and rel == "alternate":
            return href
        text = "".join(child.itertext()).strip()
        if text:
            return text
        if href:
            return href
    return ""


def parse_datetime(raw):
    if not raw:
        return None
    value = raw.strip()
    try:
        parsed = parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=dt.timezone.utc)
        return parsed
    except (TypeError, ValueError, IndexError):
        pass

    normalized = value.replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed


def load_feeds(opml_path):
    root = ET.parse(opml_path).getroot()
    feeds = []
    for outline in root.findall(".//outline[@type='rss']"):
        feeds.append(
            {
                "name": outline.attrib.get("text") or outline.attrib.get("title") or "",
                "xml_url": outline.attrib["xmlUrl"],
                "html_url": outline.attrib.get("htmlUrl", ""),
            }
        )
    return feeds


def fetch_url(url, timeout):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": ACCEPT,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as resp:
        return resp.read(), resp.geturl(), resp.headers.get("Content-Type", "")


def parse_atom(root, feed_meta):
    feed_title = first_text(root, {"title"}) or feed_meta["name"]
    entries = []
    for entry in root:
        if local_name(entry.tag) != "entry":
            continue
        published_raw = first_text(entry, {"published", "updated", "issued", "created"})
        entries.append(
            {
                "feed_name": feed_title,
                "feed_url": feed_meta["xml_url"],
                "site_url": feed_meta["html_url"],
                "title": first_text(entry, {"title"}) or "(untitled)",
                "link": first_link(entry),
                "published_raw": published_raw,
                "published_at": parse_datetime(published_raw),
                "summary": strip_html(first_text(entry, {"summary", "content"})),
            }
        )
    return entries


def parse_rss(root, feed_meta):
    channel = None
    if local_name(root.tag) == "rss":
        for child in root:
            if local_name(child.tag) == "channel":
                channel = child
                break
    elif local_name(root.tag) in {"RDF", "rdf"}:
        channel = root
    else:
        channel = root

    feed_title = first_text(channel, {"title"}) or feed_meta["name"]
    entries = []
    for item in channel.iter():
        if local_name(item.tag) != "item":
            continue
        published_raw = first_text(item, {"pubDate", "published", "date", "updated"})
        entries.append(
            {
                "feed_name": feed_title,
                "feed_url": feed_meta["xml_url"],
                "site_url": feed_meta["html_url"],
                "title": first_text(item, {"title"}) or "(untitled)",
                "link": first_link(item) or first_text(item, {"guid"}),
                "published_raw": published_raw,
                "published_at": parse_datetime(published_raw),
                "summary": strip_html(first_text(item, {"description", "encoded", "content", "summary"})),
            }
        )
    return entries


def parse_feed(content, feed_meta):
    root = ET.fromstring(content)
    tag = local_name(root.tag)
    if tag == "feed":
        return parse_atom(root, feed_meta)
    if tag in {"rss", "RDF", "rdf"}:
        return parse_rss(root, feed_meta)
    raise ValueError(f"Unsupported feed root tag: {root.tag}")


def fetch_feed(feed_meta, timeout):
    try:
        content, final_url, content_type = fetch_url(feed_meta["xml_url"], timeout)
        entries = parse_feed(content, feed_meta)
        return {
            "feed": feed_meta,
            "status": "ok",
            "final_url": final_url,
            "content_type": content_type,
            "entries": entries,
        }
    except Exception as exc:
        return {
            "feed": feed_meta,
            "status": "error",
            "error": f"{type(exc).__name__}: {exc}",
            "entries": [],
        }


def serialize_item(item, target_tz):
    published_at = item["published_at"]
    published_local = published_at.astimezone(target_tz) if published_at else None
    return {
        "feed_name": item["feed_name"],
        "feed_url": item["feed_url"],
        "site_url": item["site_url"],
        "title": item["title"],
        "link": item["link"],
        "published_raw": item["published_raw"],
        "published_at": published_at.isoformat() if published_at else None,
        "published_local": published_local.isoformat() if published_local else None,
        "summary": item["summary"],
    }


def format_markdown(payload):
    target_label = payload.get("target_date")
    if payload.get("days", 1) > 1:
        target_label = f"{payload['target_date']} minus {payload['days'] - 1} day(s)"
    lines = [
        f"# RSS items for {target_label} ({payload['timezone']})",
        "",
        f"- Feeds checked: {payload['feed_count']}",
        f"- Feeds failed: {len(payload['errors'])}",
        f"- Matching items: {len(payload['items'])}",
        "",
    ]
    if payload["errors"]:
        lines.extend(["## Feed errors", ""])
        for error in payload["errors"]:
            lines.append(f"- {error['feed_name']}: {error['error']}")
        lines.append("")
    if payload["items"]:
        lines.extend(["## Items", ""])
        for item in payload["items"]:
            lines.append(f"### {item['title']}")
            lines.append(f"- Feed: {item['feed_name']}")
            lines.append(f"- Published: {item['published_local'] or item['published_raw'] or 'unknown'}")
            lines.append(f"- Link: {item['link']}")
            if item["summary"]:
                lines.append(f"- Summary: {item['summary']}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    skill_dir = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Fetch recent items from the configured RSS bundle.")
    parser.add_argument("--feeds-file", default=str(skill_dir / "references" / "feeds.opml"))
    parser.add_argument("--date", help="Target end date in YYYY-MM-DD. Default: current date in target timezone.")
    parser.add_argument(
        "--days",
        type=int,
        default=DEFAULT_DAYS,
        help=f"Number of days to include ending on --date. Default: {DEFAULT_DAYS}.",
    )
    parser.add_argument("--limit", type=int, help="Optional maximum number of items to return after sorting.")
    parser.add_argument("--timezone", default=DEFAULT_TZ)
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    if args.days < 1:
        raise SystemExit("--days must be at least 1")
    if args.limit is not None and args.limit < 1:
        raise SystemExit("--limit must be at least 1")

    try:
        target_tz = dt.ZoneInfo(args.timezone)
    except Exception as exc:
        raise SystemExit(f"Invalid timezone '{args.timezone}': {exc}")

    if args.date:
        target_date = dt.date.fromisoformat(args.date)
    else:
        target_date = dt.datetime.now(target_tz).date()
    start_date = target_date - dt.timedelta(days=args.days - 1)

    feeds = load_feeds(args.feeds_file)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [executor.submit(fetch_feed, feed, args.timeout) for feed in feeds]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    items = []
    errors = []
    for result in results:
        if result["status"] != "ok":
            errors.append(
                {
                    "feed_name": result["feed"]["name"],
                    "feed_url": result["feed"]["xml_url"],
                    "error": result["error"],
                }
            )
            continue
        for entry in result["entries"]:
            published_at = entry["published_at"]
            if not published_at:
                continue
            published_local = published_at.astimezone(target_tz)
            published_date = published_local.date()
            if published_date < start_date or published_date > target_date:
                continue
            if not entry["link"]:
                continue
            items.append(serialize_item(entry, target_tz))

    items.sort(
        key=lambda item: (
            item["published_local"] or "",
            item["feed_name"].lower(),
            item["title"].lower(),
        ),
        reverse=True,
    )
    errors.sort(key=lambda err: err["feed_name"].lower())
    if args.limit is not None:
        items = items[: args.limit]

    payload = {
        "start_date": start_date.isoformat(),
        "target_date": target_date.isoformat(),
        "days": args.days,
        "timezone": args.timezone,
        "feed_count": len(feeds),
        "items": items,
        "errors": errors,
    }

    if args.format == "markdown":
        sys.stdout.write(format_markdown(payload))
    else:
        json.dump(payload, sys.stdout, ensure_ascii=True, indent=2)
        sys.stdout.write("\n")


if __name__ == "__main__":
    if not hasattr(dt, "ZoneInfo"):
        from zoneinfo import ZoneInfo  # type: ignore

        dt.ZoneInfo = ZoneInfo  # type: ignore[attr-defined]
    main()
