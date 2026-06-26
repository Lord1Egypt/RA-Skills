#!/usr/bin/env python3
"""Fetch Xiaohongshu note pages and extract basic structured fields."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Dict, List, Optional
from urllib import error, request


UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


@dataclass
class NoteRecord:
    url: str
    note_id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    published_at: Optional[str]
    images: List[str]
    tags: List[str]
    interaction: Dict[str, Optional[int]]
    fetched_at_utc: str
    source_status: str


def read_urls(one_url: Optional[str], url_file: Optional[str]) -> List[str]:
    urls: List[str] = []
    if one_url:
        urls.append(one_url.strip())
    if url_file:
        for line in Path(url_file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            urls.append(line)
    deduped = []
    seen = set()
    for u in urls:
        if u and u not in seen:
            deduped.append(u)
            seen.add(u)
    return deduped


def fetch_html(url: str, timeout: int, cookie: Optional[str]) -> str:
    headers = {"User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"}
    if cookie:
        headers["Cookie"] = cookie
    req = request.Request(url=url, headers=headers)
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def _extract_meta(html: str, prop: str) -> Optional[str]:
    pattern = (
        r'<meta[^>]+(?:property|name)=["\']'
        + re.escape(prop)
        + r'["\'][^>]+content=["\']([^"\']+)["\']'
    )
    m = re.search(pattern, html, flags=re.IGNORECASE)
    return unescape(m.group(1).strip()) if m else None


def _extract_note_id(url: str, html: str) -> Optional[str]:
    m = re.search(r"/explore/([0-9a-zA-Z]+)", url)
    if m:
        return m.group(1)
    m = re.search(r'"noteId"\s*:\s*"([^"]+)"', html)
    if m:
        return m.group(1)
    return None


def _extract_json_ld(html: str) -> Dict[str, object]:
    out: Dict[str, object] = {}
    blocks = re.findall(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )
    for raw in blocks:
        raw = raw.strip()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    out.update(item)
        elif isinstance(payload, dict):
            out.update(payload)
    return out


def _parse_iso(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value
    return dt.astimezone(timezone.utc).isoformat()


def _extract_interaction_from_ld(ld: Dict[str, object]) -> Dict[str, Optional[int]]:
    metrics = {"like_count": None, "comment_count": None, "share_count": None, "collect_count": None}
    stats = ld.get("interactionStatistic")
    if not isinstance(stats, list):
        return metrics
    for item in stats:
        if not isinstance(item, dict):
            continue
        raw_type = str(item.get("interactionType", "")).lower()
        count = item.get("userInteractionCount")
        if not isinstance(count, int):
            try:
                count = int(str(count))
            except (TypeError, ValueError):
                continue
        if "like" in raw_type:
            metrics["like_count"] = count
        elif "comment" in raw_type:
            metrics["comment_count"] = count
        elif "share" in raw_type:
            metrics["share_count"] = count
    return metrics


def parse_note(url: str, html: str) -> NoteRecord:
    ld = _extract_json_ld(html)
    title = _extract_meta(html, "og:title") or ld.get("headline")
    if isinstance(title, str):
        title = title.strip()
    else:
        title = None

    desc = _extract_meta(html, "og:description") or ld.get("description")
    if isinstance(desc, str):
        desc = desc.strip()
    else:
        desc = None

    author = None
    author_obj = ld.get("author")
    if isinstance(author_obj, dict):
        author_name = author_obj.get("name")
        if isinstance(author_name, str):
            author = author_name.strip()

    images: List[str] = []
    first_image = _extract_meta(html, "og:image")
    if first_image:
        images.append(first_image)
    ld_image = ld.get("image")
    if isinstance(ld_image, str):
        images.append(ld_image)
    elif isinstance(ld_image, list):
        images.extend([x for x in ld_image if isinstance(x, str)])
    images = list(dict.fromkeys([x.strip() for x in images if x and x.strip()]))

    tags: List[str] = []
    keywords = ld.get("keywords")
    if isinstance(keywords, str):
        tags = [x.strip() for x in re.split(r"[,，]", keywords) if x.strip()]

    note = NoteRecord(
        url=url,
        note_id=_extract_note_id(url, html),
        title=title,
        description=desc,
        author=author,
        published_at=_parse_iso(ld.get("datePublished") if isinstance(ld, dict) else None),
        images=images,
        tags=tags,
        interaction=_extract_interaction_from_ld(ld),
        fetched_at_utc=datetime.now(timezone.utc).isoformat(),
        source_status="ok",
    )
    return note


def to_markdown(note: NoteRecord) -> str:
    lines = [
        f"# {note.title or 'Untitled'}",
        "",
        f"- URL: {note.url}",
        f"- Note ID: {note.note_id or 'N/A'}",
        f"- Author: {note.author or 'N/A'}",
        f"- Published: {note.published_at or 'N/A'}",
        f"- Like: {note.interaction.get('like_count')}",
        f"- Comment: {note.interaction.get('comment_count')}",
        f"- Share: {note.interaction.get('share_count')}",
        f"- Collect: {note.interaction.get('collect_count')}",
        "",
        "## Description",
        "",
        note.description or "",
        "",
        "## Tags",
        "",
        ", ".join(note.tags) if note.tags else "N/A",
        "",
        "## Images",
        "",
    ]
    if note.images:
        lines.extend([f"- {img}" for img in note.images])
    else:
        lines.append("- N/A")
    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and parse Xiaohongshu notes.")
    parser.add_argument("--url", help="Single Xiaohongshu note URL.")
    parser.add_argument("--url-file", help="File containing note URLs, one per line.")
    parser.add_argument("--cookie", help="Raw cookie header value.")
    parser.add_argument("--cookie-file", help="Read cookie header value from file.")
    parser.add_argument("--format", choices=["json", "md", "both"], default="json")
    parser.add_argument("--output", default="xhs_notes.json", help="Output path for JSON.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    if not args.url and not args.url_file:
        parser.error("Provide at least one of --url or --url-file.")

    cookie = args.cookie
    if args.cookie_file:
        cookie = Path(args.cookie_file).read_text(encoding="utf-8").strip()

    urls = read_urls(args.url, args.url_file)
    if not urls:
        parser.error("No valid URLs found.")

    records: List[NoteRecord] = []
    for url in urls:
        try:
            html = fetch_html(url, timeout=args.timeout, cookie=cookie)
            note = parse_note(url, html)
        except error.HTTPError as e:
            note = NoteRecord(
                url=url,
                note_id=None,
                title=None,
                description=f"HTTPError: {e.code}",
                author=None,
                published_at=None,
                images=[],
                tags=[],
                interaction={"like_count": None, "comment_count": None, "share_count": None, "collect_count": None},
                fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                source_status=f"http_error_{e.code}",
            )
        except Exception as e:  # noqa: BLE001
            note = NoteRecord(
                url=url,
                note_id=None,
                title=None,
                description=f"Error: {e}",
                author=None,
                published_at=None,
                images=[],
                tags=[],
                interaction={"like_count": None, "comment_count": None, "share_count": None, "collect_count": None},
                fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                source_status="error",
            )
        records.append(note)

    output_path = Path(args.output)
    data = [asdict(r) for r in records]

    if args.format in ("json", "both"):
        output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format in ("md", "both"):
        if len(records) == 1:
            md_path = output_path.with_suffix(".md")
            md_path.write_text(to_markdown(records[0]), encoding="utf-8")
        else:
            folder = output_path.parent / (output_path.stem + "_md")
            folder.mkdir(parents=True, exist_ok=True)
            for idx, note in enumerate(records, start=1):
                suffix = note.note_id or f"note_{idx}"
                safe = re.sub(r"[^0-9A-Za-z_-]+", "_", suffix)
                (folder / f"{safe}.md").write_text(to_markdown(note), encoding="utf-8")

    print(f"Processed {len(records)} URL(s).")
    print(f"Output base: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
