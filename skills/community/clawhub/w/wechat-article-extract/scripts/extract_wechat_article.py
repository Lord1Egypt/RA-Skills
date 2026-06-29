#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

CHINA_TZ = timezone(timedelta(hours=8))
IMAGE_MARKER_PREFIX = "WECHAT_IMAGE_"
TRACKING_QUERY_KEYS = {
    "chksm",
    "scene",
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "share_token",
    "sharer_shareinfo",
    "sharer_shareinfo_first",
}
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 MicroMessenger/8.0"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}


def cleanup_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def is_public_wechat_article(url: str) -> bool:
    parsed = urlparse(str(url or "").strip())
    return parsed.scheme in {"http", "https"} and parsed.hostname == "mp.weixin.qq.com" and parsed.path.startswith("/s")


def strip_tracking_params(url: str) -> str:
    parsed = urlparse(str(url or "").strip())
    filtered = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key not in TRACKING_QUERY_KEYS
    ]
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, urlencode(filtered), parsed.fragment))


def fetch_html(url: str, timeout: int = 20, max_retries: int = 3, retry_delay: float = 1.0) -> dict[str, Any]:
    if not is_public_wechat_article(url):
        raise ValueError("URL must be a public mp.weixin.qq.com/s article link")

    clean_url = strip_tracking_params(url)
    last_error = ""
    status_code = 0
    for attempt in range(1, max(1, max_retries) + 1):
        try:
            request = Request(clean_url, headers=DEFAULT_HEADERS)
            with urlopen(request, timeout=timeout) as response:
                status_code = getattr(response, "status", 0) or 200
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset, errors="replace")
            return {"html": body, "source_url": clean_url, "status_code": status_code, "attempt": attempt}
        except HTTPError as exc:
            status_code = exc.code
            last_error = str(exc)
        except URLError as exc:
            last_error = str(exc.reason)
        except Exception as exc:
            last_error = str(exc)
        if attempt < max_retries:
            time.sleep(max(0.0, retry_delay) * attempt)

    raise RuntimeError(f"Failed to fetch WeChat article: status={status_code or 'unknown'} error={last_error}")


def extract_first(pattern: str, text: str, default: str = "", flags: int = re.I | re.S) -> str:
    match = re.search(pattern, text, flags)
    if not match:
        return default
    return html.unescape(match.group(1).strip())


def convert_timestamp_to_china_text(timestamp_text: str) -> str:
    timestamp = int(str(timestamp_text or "0").strip() or 0)
    if timestamp <= 0:
        return ""
    return datetime.fromtimestamp(timestamp, tz=CHINA_TZ).strftime("%Y-%m-%d %H:%M")


def extract_article_id(source_url: str, page_html: str) -> str:
    parsed = urlparse(source_url)
    query_map = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if cleanup_text(query_map.get("sn")):
        return cleanup_text(query_map.get("sn"))

    slug = cleanup_text(parsed.path.rstrip("/").split("/")[-1])
    if slug and slug != "s":
        return slug

    composite = "__".join(
        cleanup_text(query_map.get(key)) for key in ("__biz", "mid", "idx", "sn") if cleanup_text(query_map.get(key))
    )
    if composite:
        return composite
    return hashlib.sha1(page_html.encode("utf-8")).hexdigest()[:16]


def extract_js_content_html(page_html: str) -> str:
    match = re.search(r'<div[^>]+id="js_content"[^>]*>(.*?)</div>\s*<script', page_html, re.I | re.S)
    if match:
        return match.group(1)
    match = re.search(r'<div[^>]+id="js_content"[^>]*>(.*?)</div>', page_html, re.I | re.S)
    return match.group(1) if match else ""


def normalize_image_url(value: Any) -> str:
    url = html.unescape(str(value or "").strip())
    if url.startswith("//"):
        url = f"https:{url}"
    return url if url.startswith("http") else ""


def build_image_marker(index: int) -> str:
    return f"[[{IMAGE_MARKER_PREFIX}{index}]]"


def extract_style_value(style_text: str, property_name: str) -> str:
    match = re.search(rf"(?:^|;)\s*{re.escape(property_name)}\s*:\s*([^;]+)", str(style_text or ""), re.I)
    return cleanup_text(match.group(1)) if match else ""


def parse_image_scale(img_html: str) -> float | None:
    style = extract_first(r'style="([^"]+)"', img_html) or extract_first(r"style='([^']+)'", img_html)
    width_value = extract_style_value(style, "width")
    if width_value.endswith("%"):
        try:
            scale = float(width_value[:-1].strip()) / 100
            return round(scale, 4) if 0 < scale <= 1 else None
        except Exception:
            return None

    data_width = extract_first(r'data-w="([^"]+)"', img_html) or extract_first(r"data-w='([^']+)'", img_html)
    if width_value.endswith("px") and data_width:
        try:
            scale = float(width_value[:-2].strip()) / float(data_width)
            return round(scale, 4) if 0 < scale <= 1 else None
        except Exception:
            return None
    return None


def replace_images_with_markers(content_html: str) -> tuple[str, list[dict[str, Any]]]:
    image_entries: list[dict[str, Any]] = []

    def repl(match: re.Match[str]) -> str:
        img_html = match.group(0)
        source_url = ""
        for pattern in (r'data-src="([^"]+)"', r"data-src='([^']+)'", r'src="([^"]+)"', r"src='([^']+)'"):
            source_url = normalize_image_url(extract_first(pattern, img_html))
            if source_url:
                break
        if not source_url:
            return "\n\n"

        marker = build_image_marker(len(image_entries) + 1)
        image_entry: dict[str, Any] = {"marker": marker, "sourceUrl": source_url}
        scale = parse_image_scale(img_html)
        if scale:
            image_entry["scale"] = scale
        image_entries.append(image_entry)
        return f"\n\n{marker}\n\n"

    return re.sub(r"<img\b[^>]*>", repl, str(content_html or ""), flags=re.I), image_entries


def cleanup_inline_text(value: Any) -> str:
    text = html.unescape(str(value or "")).replace("\r", "")
    return re.sub(r"\s+", " ", text).strip()


def escape_markdown_table_cell(text: str) -> str:
    return str(text or "").replace("\\", "\\\\").replace("|", "\\|")


def html_fragment_to_inline_text(fragment: str) -> str:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", str(fragment or ""), flags=re.I | re.S)
    text = re.sub(r"<br\s*/?>", "<br>", text, flags=re.I)
    text = re.sub(r"</?(p|section|article|blockquote|ul|ol|li|div|span)[^>]*>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    parts = [cleanup_inline_text(part) for part in text.split("<br>")]
    return "<br>".join(part for part in parts if part)


def convert_html_table_to_markdown(table_html: str) -> str:
    rows: list[list[str]] = []
    for row_match in re.finditer(r"<tr[^>]*>(.*?)</tr>", str(table_html or ""), re.I | re.S):
        row_html = row_match.group(1)
        cells = []
        for cell_match in re.finditer(r"<t[hd][^>]*>(.*?)</t[hd]>", row_html, re.I | re.S):
            cells.append(escape_markdown_table_cell(html_fragment_to_inline_text(cell_match.group(1))))
        if any(cell.strip() for cell in cells):
            rows.append(cells)
    if not rows:
        return ""

    column_count = max(len(row) for row in rows)
    normalized_rows = [row + [""] * (column_count - len(row)) for row in rows]
    lines = [
        f"| {' | '.join(normalized_rows[0])} |",
        f"| {' | '.join(['---'] * column_count)} |",
    ]
    lines.extend(f"| {' | '.join(row)} |" for row in normalized_rows[1:])
    return "\n".join(lines)


def replace_tables_with_markdown(content_html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        markdown = convert_html_table_to_markdown(match.group(0))
        return f"\n\n{markdown}\n\n" if markdown else "\n\n"

    return re.sub(r"<table[^>]*>.*?</table>", repl, str(content_html or ""), flags=re.I | re.S)


def html_to_plain_text(content_html: str) -> str:
    text = replace_tables_with_markdown(content_html)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", text, flags=re.I | re.S)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"</?(p|section|article|blockquote|ul|ol|li|h1|h2|h3|h4|h5|h6)[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"<img[^>]*>", "", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text).replace("\r", "")
    raw_lines = [cleanup_text(line) for line in text.split("\n")]

    blocks: list[str] = []
    table_lines: list[str] = []
    for line in raw_lines:
        if not line:
            if table_lines:
                blocks.append("\n".join(table_lines))
                table_lines = []
            continue
        if line.startswith("|"):
            table_lines.append(line)
            continue
        if table_lines:
            blocks.append("\n".join(table_lines))
            table_lines = []
        blocks.append(line)
    if table_lines:
        blocks.append("\n".join(table_lines))
    return re.sub(r"\n{3,}", "\n\n", "\n\n".join(blocks)).strip()


def remove_image_markers(text: str) -> str:
    cleaned = re.sub(rf"\[\[{IMAGE_MARKER_PREFIX}\d+\]\]", "", str(text or ""))
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def parse_article(page_html: str, source_url: str) -> dict[str, Any]:
    title = extract_first(r'<meta[^>]+property="og:title"[^>]+content="([^"]+)"', page_html)
    title = title or extract_first(r'var\s+msg_title\s*=\s*"([^"]+)"', page_html)

    author = extract_first(r'<a[^>]+id="js_name"[^>]*>(.*?)</a>', page_html)
    author = author or extract_first(r'var\s+nickname\s*=\s*htmlDecode\("([^"]+)"\)', page_html)
    author = author or extract_first(r'<meta[^>]+name="author"[^>]+content="([^"]+)"', page_html)

    publish_time = convert_timestamp_to_china_text(extract_first(r'var\s+ct\s*=\s*"?(\d{10})"?', page_html))
    content_html = extract_js_content_html(page_html)
    if not content_html:
        raise RuntimeError("Could not find WeChat article body node #js_content")

    marked_content_html, image_entries = replace_images_with_markers(content_html)
    content_with_image_markers = html_to_plain_text(marked_content_html)
    content = remove_image_markers(content_with_image_markers)
    if not content:
        raise RuntimeError("WeChat article body is empty")

    return {
        "articleId": extract_article_id(source_url, page_html),
        "title": cleanup_text(title),
        "author": cleanup_text(author),
        "publishTime": publish_time,
        "sourceUrl": source_url,
        "content": content,
        "contentWithImageMarkers": content_with_image_markers,
        "imageEntries": image_entries,
        "imageUrls": [entry["sourceUrl"] for entry in image_entries if entry.get("sourceUrl")],
        "imageCount": len(image_entries),
        "coverImageUrl": image_entries[0]["sourceUrl"] if image_entries else "",
    }


def render_markdown(record: dict[str, Any]) -> str:
    lines = [
        f"# {record.get('title') or 'Untitled WeChat Article'}",
        "",
        f"- Account: {record.get('author') or 'Unknown'}",
        f"- Published: {record.get('publishTime') or 'Unknown'}",
        f"- Source: {record.get('sourceUrl') or ''}",
        f"- Images: {record.get('imageCount') or 0}",
        "",
        "---",
        "",
        str(record.get("contentWithImageMarkers") or record.get("content") or "").strip(),
    ]
    image_urls = [str(url).strip() for url in record.get("imageUrls") or [] if str(url).strip()]
    if image_urls:
        lines.extend(["", "---", "", "## Images", ""])
        lines.extend(f"{idx}. {url}" for idx, url in enumerate(image_urls, start=1))
    return "\n".join(lines).strip() + "\n"


def guess_image_suffix(content_type: str, source_url: str) -> str:
    suffix = mimetypes.guess_extension((content_type or "").split(";")[0].strip())
    if suffix:
        return ".jpg" if suffix == ".jpe" else suffix
    path_suffix = Path(urlparse(source_url).path).suffix.lower()
    return path_suffix if path_suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"} else ".jpg"


def download_images(record: dict[str, Any], output_dir: Path, timeout: int = 30) -> list[dict[str, str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded: list[dict[str, str]] = []
    for idx, entry in enumerate(record.get("imageEntries") or [], start=1):
        url = str(entry.get("sourceUrl") or "").strip()
        if not url:
            continue
        request = Request(url, headers={**DEFAULT_HEADERS, "Referer": "https://mp.weixin.qq.com/"})
        with urlopen(request, timeout=timeout) as response:
            body = response.read()
            suffix = guess_image_suffix(response.headers.get("Content-Type", ""), url)
        file_path = output_dir / f"{idx:02d}{suffix}"
        file_path.write_bytes(body)
        downloaded.append({"marker": entry.get("marker", ""), "path": str(file_path), "sourceUrl": url})
    return downloaded


def write_output(payload: str, output_path: str) -> None:
    if output_path:
        Path(output_path).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract a public WeChat Official Account article.")
    parser.add_argument("url", nargs="?", help="Public mp.weixin.qq.com/s article URL")
    parser.add_argument("--html-file", help="Read article HTML from a local file instead of fetching the URL")
    parser.add_argument("--source-url", default="", help="Canonical source URL to store when using --html-file")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output", "-o", default="", help="Write output to this file instead of stdout")
    parser.add_argument("--download-images", default="", help="Optional directory for downloading article images")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=1.0)
    args = parser.parse_args(argv)

    if args.html_file:
        source_url = args.source_url or args.url or "about:blank"
        page_html = Path(args.html_file).read_text(encoding="utf-8")
        record = parse_article(page_html, source_url)
        record["statusCode"] = None
        record["attempt"] = 0
    else:
        if not args.url:
            raise SystemExit("Provide a WeChat article URL or --html-file")
        fetched = fetch_html(args.url, timeout=args.timeout, max_retries=args.max_retries, retry_delay=args.retry_delay)
        record = parse_article(fetched["html"], fetched["source_url"])
        record["statusCode"] = fetched["status_code"]
        record["attempt"] = fetched["attempt"]

    if args.download_images:
        record["downloadedImages"] = download_images(record, Path(args.download_images))

    if args.format == "json":
        write_output(json.dumps(record, ensure_ascii=False, indent=2) + "\n", args.output)
    else:
        write_output(render_markdown(record), args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
