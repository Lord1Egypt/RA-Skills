#!/usr/bin/env python3
"""Enrich a small set of Xiaoyuzhou URLs under a strict cap."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import zlib
from html import unescape
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List
from urllib.request import Request, urlopen

USER_AGENT = "podcast-radar-cn/0.1 (+https://github.com/XiaohuoluFM/xhlfm-skills)"
NEXT_DATA_PATTERN = re.compile(
    rb'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
    re.DOTALL,
)
PODCAST_URL_TEMPLATE = "https://www.xiaoyuzhoufm.com/podcast/{pid}"
READ_CHUNK_SIZE = 16384
MAX_READ_BYTES = 512000


class TextExtractor(HTMLParser):
    BLOCK_TAGS = {"p", "div", "section", "figure", "figcaption", "li", "ul", "ol", "h1", "h2", "h3", "h4"}

    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        if tag == "br":
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        text = unescape("".join(self.parts))
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich a small number of Xiaoyuzhou episode or podcast pages. Hard-capped to 20 URLs."
    )
    parser.add_argument("--episode-url", action="append", default=[], help="Episode URL to enrich. May be repeated.")
    parser.add_argument("--podcast-url", action="append", default=[], help="Podcast URL to enrich. May be repeated.")
    parser.add_argument(
        "--from-json",
        help="Path to JSON from fetch_xyz_rank.py. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--max-items",
        type=int,
        default=20,
        help="Hard cap on URLs to enrich in one run. Default: 20.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=1.2,
        help="Base delay between sequential requests.",
    )
    parser.add_argument(
        "--jitter-seconds",
        type=float,
        default=0.4,
        help="Random extra delay added per request.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print the JSON output.",
    )
    return parser.parse_args()


def fetch_next_data(url: str) -> Dict[str, Any]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Encoding": "gzip",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urlopen(request, timeout=30) as response:
        content_encoding = (response.getheader("Content-Encoding") or "").lower()
        decompressor = zlib.decompressobj(16 + zlib.MAX_WBITS) if "gzip" in content_encoding else None
        chunks: List[bytes] = []
        total_read = 0
        while total_read < MAX_READ_BYTES:
            raw_chunk = response.read(READ_CHUNK_SIZE)
            if not raw_chunk:
                break
            total_read += len(raw_chunk)
            chunk = decompressor.decompress(raw_chunk) if decompressor else raw_chunk
            if chunk:
                chunks.append(chunk)
            payload = extract_next_data_from_html_bytes(b"".join(chunks))
            if payload is not None:
                return payload

    raise ValueError("Could not find __NEXT_DATA__ within the read limit.")


def extract_next_data_from_html_bytes(html: bytes) -> Dict[str, Any] | None:
    match = NEXT_DATA_PATTERN.search(html)
    if not match:
        return None
    return json.loads(match.group(1).decode("utf-8"))


def load_json_payload(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def dedupe_preserve(items: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for item in items:
        value = item.strip()
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def extract_urls_from_payload(payload: Any) -> List[str]:
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        items = payload.get("items", [])
    else:
        return []

    urls: List[str] = []
    for item in items:
        if isinstance(item, str):
            urls.append(item)
            continue
        if not isinstance(item, dict):
            continue

        if item.get("kind") == "episode" and item.get("episodeUrl"):
            urls.append(item["episodeUrl"])
            continue
        if item.get("kind") == "podcast" and item.get("xyzUrl"):
            urls.append(item["xyzUrl"])
            continue
        if item.get("episodeUrl"):
            urls.append(item["episodeUrl"])
            continue
        if item.get("xyzUrl"):
            urls.append(item["xyzUrl"])
            continue
        links = item.get("links")
        if isinstance(links, dict) and links.get("xyz"):
            urls.append(links["xyz"])
    return urls


def html_to_text(value: Any) -> str | None:
    if not value:
        return None
    if not isinstance(value, str):
        return str(value)
    extractor = TextExtractor()
    extractor.feed(value)
    return extractor.text() or None


def enrich_episode(url: str, episode: Dict[str, Any]) -> Dict[str, Any]:
    podcast = episode.get("podcast") or {}
    pid = episode.get("pid")
    return {
        "kind": "episode",
        "url": url,
        "eid": episode.get("eid"),
        "pid": pid,
        "title": episode.get("title"),
        "description": episode.get("description"),
        "shownotesText": html_to_text(episode.get("shownotes")),
        "durationSeconds": episode.get("duration"),
        "playCount": episode.get("playCount"),
        "commentCount": episode.get("commentCount"),
        "favoriteCount": episode.get("favoriteCount"),
        "clapCount": episode.get("clapCount"),
        "pubDate": episode.get("pubDate"),
        "podcastUrl": PODCAST_URL_TEMPLATE.format(pid=pid) if pid else None,
        "podcast": {
            "title": podcast.get("title"),
            "author": podcast.get("author"),
            "brief": podcast.get("brief"),
            "description": podcast.get("description"),
            "subscriptionCount": podcast.get("subscriptionCount"),
            "episodeCount": podcast.get("episodeCount"),
        },
    }


def enrich_podcast(url: str, podcast: Dict[str, Any]) -> Dict[str, Any]:
    podcasters = podcast.get("podcasters") or []
    recent_episodes = podcast.get("episodes") or []
    return {
        "kind": "podcast",
        "url": url,
        "pid": podcast.get("pid"),
        "title": podcast.get("title"),
        "author": podcast.get("author"),
        "brief": podcast.get("brief"),
        "description": podcast.get("description"),
        "subscriptionCount": podcast.get("subscriptionCount"),
        "episodeCount": podcast.get("episodeCount"),
        "latestEpisodePubDate": podcast.get("latestEpisodePubDate"),
        "podcasters": [
            {"uid": podcaster.get("uid"), "nickname": podcaster.get("nickname")}
            for podcaster in podcasters[:5]
        ],
        "recentEpisodes": [
            {
                "eid": episode.get("eid"),
                "title": episode.get("title"),
                "pubDate": episode.get("pubDate"),
                "playCount": episode.get("playCount"),
            }
            for episode in recent_episodes[:5]
        ],
    }


def enrich_url(url: str) -> Dict[str, Any]:
    next_data = fetch_next_data(url)
    page_props = next_data.get("props", {}).get("pageProps", {})

    if "episode" in page_props:
        return enrich_episode(url, page_props["episode"])
    if "podcast" in page_props:
        return enrich_podcast(url, page_props["podcast"])
    raise ValueError(f"Unsupported Xiaoyuzhou page shape for URL: {url}")


def main() -> int:
    args = parse_args()

    urls = list(args.episode_url) + list(args.podcast_url)
    if args.from_json:
        urls.extend(extract_urls_from_payload(load_json_payload(args.from_json)))

    urls = dedupe_preserve(urls)
    if not urls:
        raise SystemExit("No URLs supplied. Use --episode-url, --podcast-url, or --from-json.")

    if len(urls) > args.max_items:
        raise SystemExit(
            f"Refusing to enrich {len(urls)} URLs. Narrow the shortlist to {args.max_items} or fewer first."
        )

    items: List[Dict[str, Any]] = []
    for index, url in enumerate(urls):
        if index:
            delay = max(0.0, args.sleep_seconds + random.uniform(0.0, max(0.0, args.jitter_seconds)))
            time.sleep(delay)
        items.append(enrich_url(url))

    response = {
        "requestedUrls": urls,
        "returnedCount": len(items),
        "items": items,
    }

    if args.pretty:
        json.dump(response, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        json.dump(response, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
