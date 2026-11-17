#!/usr/bin/env python3
"""Fetch bounded items from one or more HTTP(S) RSS or Atom feeds."""

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from email.utils import parsedate_to_datetime


MAX_RESPONSE_BYTES = 5 * 1024 * 1024


def local_name(tag):
    return tag.rsplit("}", 1)[-1].lower()


def element_text(element):
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def first_child(parent, *names):
    wanted = {name.lower() for name in names}
    for child in parent:
        if local_name(child.tag) in wanted:
            return child
    return None


def clean_text(value, limit=500):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:limit]


def normalize_date(value):
    value = (value or "").strip()
    if not value:
        return ""
    try:
        parsed = parsedate_to_datetime(value)
        return parsed.isoformat(timespec="minutes")
    except (TypeError, ValueError, OverflowError):
        pass
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed.isoformat(timespec="minutes")
    except ValueError:
        return value


def atom_link(entry, base_url):
    fallback = ""
    for child in entry:
        if local_name(child.tag) != "link":
            continue
        href = (child.get("href") or "").strip()
        if not href:
            continue
        resolved = urllib.parse.urljoin(base_url, href)
        if (child.get("rel") or "alternate") == "alternate":
            return resolved
        if not fallback:
            fallback = resolved
    return fallback


def parse_atom(root, base_url, limit):
    title = clean_text(element_text(first_child(root, "title")), 200) or base_url
    items = []
    for entry in (child for child in root if local_name(child.tag) == "entry"):
        if len(items) >= limit:
            break
        summary = first_child(entry, "summary", "content", "description")
        published = first_child(entry, "published", "updated", "date")
        items.append(
            {
                "title": clean_text(element_text(first_child(entry, "title")), 300)
                or "(无标题)",
                "link": atom_link(entry, base_url),
                "summary": clean_text(element_text(summary)),
                "date": normalize_date(element_text(published)),
            }
        )
    return title, items


def parse_rss(root, base_url, limit):
    channel = first_child(root, "channel")
    if channel is None and local_name(root.tag) == "channel":
        channel = root
    if channel is None:
        raise ValueError("RSS channel not found")
    title = clean_text(element_text(first_child(channel, "title")), 200) or base_url
    items = []
    for entry in (child for child in channel if local_name(child.tag) == "item"):
        if len(items) >= limit:
            break
        link = element_text(first_child(entry, "link"))
        if not link:
            link = element_text(first_child(entry, "guid"))
        summary = first_child(entry, "description", "summary", "content", "encoded")
        published = first_child(entry, "pubdate", "date", "published", "updated")
        items.append(
            {
                "title": clean_text(element_text(first_child(entry, "title")), 300)
                or "(无标题)",
                "link": urllib.parse.urljoin(base_url, link.strip()) if link else "",
                "summary": clean_text(element_text(summary)),
                "date": normalize_date(element_text(published)),
            }
        )
    return title, items


def fetch(url, limit):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("only HTTP(S) feed URLs are allowed")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "YoooClaw-RSS/1.0 (+https://clawhub.ai/)",
            "Accept": "application/rss+xml, application/atom+xml, text/xml, application/xml",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        final_url = response.geturl()
        content = response.read(MAX_RESPONSE_BYTES + 1)
    if len(content) > MAX_RESPONSE_BYTES:
        raise ValueError("feed response exceeds 5 MiB")
    root = ET.fromstring(content)
    if local_name(root.tag) == "feed":
        feed_title, items = parse_atom(root, final_url, limit)
    else:
        feed_title, items = parse_rss(root, final_url, limit)
    return {
        "ok": True,
        "feed_title": feed_title,
        "url": final_url,
        "items": items,
    }


def fetch_result(url, limit):
    try:
        return fetch(url, limit)
    except (ET.ParseError, ValueError, urllib.error.URLError, TimeoutError) as error:
        return {"ok": False, "url": url, "items": [], "error": str(error)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("urls", nargs="+")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if not 1 <= args.limit <= 50:
        parser.error("--limit must be between 1 and 50")
    if not 1 <= args.workers <= 8:
        parser.error("--workers must be between 1 and 8")
    if len(args.urls) == 1:
        result = fetch_result(args.urls[0], args.limit)
        exit_code = 0 if result["ok"] else 1
    else:
        worker_count = min(args.workers, len(args.urls))
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            feeds = list(executor.map(lambda url: fetch_result(url, args.limit), args.urls))
        success_count = sum(1 for feed in feeds if feed["ok"])
        result = {
            "ok": success_count > 0,
            "source_count": len(feeds),
            "success_count": success_count,
            "failure_count": len(feeds) - success_count,
            "feeds": feeds,
        }
        exit_code = 0 if result["ok"] else 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
