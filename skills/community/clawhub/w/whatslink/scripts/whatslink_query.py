#!/usr/bin/env python3
"""Query whatslink.info for public link metadata.

Uses only Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_ENDPOINT = "https://whatslink.info/api/v1/link"
DEFAULT_UA = "OpenClaw-whatslink-skill/0.1.1 (+https://whatslink.info/)"


def human_size(value: Any) -> str:
    """Return a human-readable byte size while preserving the raw byte count."""
    try:
        size = float(value)
    except (TypeError, ValueError):
        return "unknown"

    if size < 0:
        return f"{value} B"

    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    idx = 0
    while size >= 1024 and idx < len(units) - 1:
        size /= 1024.0
        idx += 1

    if idx == 0:
        rendered = str(int(size))
    else:
        rendered = f"{size:.1f}".rstrip("0").rstrip(".")
    return f"{rendered} {units[idx]} ({int(float(value))} bytes)"


def build_query_url(endpoint: str, target_url: str) -> str:
    separator = "&" if "?" in endpoint else "?"
    return f"{endpoint}{separator}{urlencode({'url': target_url})}"


def fetch_metadata(endpoint: str, target_url: str, timeout: float, user_agent: str | None) -> dict[str, Any]:
    query_url = build_query_url(endpoint, target_url)
    headers = {"User-Agent": user_agent or DEFAULT_UA, "Accept": "application/json"}
    request = Request(query_url, headers=headers)

    try:
        with urlopen(request, timeout=timeout) as response:
            status = getattr(response, "status", response.getcode())
            body = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"HTTP error {exc.code}: {detail or exc.reason}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise RuntimeError(f"Request timed out after {timeout:g}s") from exc

    if status < 200 or status >= 300:
        raise RuntimeError(f"HTTP error {status}")

    try:
        data = json.loads(body.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise RuntimeError("Response was not valid UTF-8") from exc
    except json.JSONDecodeError as exc:
        snippet = body[:200].decode("utf-8", "replace")
        raise RuntimeError(f"Response was not valid JSON: {snippet}") from exc

    if not isinstance(data, dict):
        raise RuntimeError(f"Unexpected JSON shape: {type(data).__name__}")

    error = data.get("error")
    if error:
        raise RuntimeError(f"WhatsLink error: {error}")

    return data


def extract_screenshot_url(item: Any) -> str | None:
    """Return a screenshot URL from known WhatsLink screenshot shapes."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        value = item.get("screenshot") or item.get("url")
        if isinstance(value, str) and value:
            return value
    return None


def format_summary(
    data: dict[str, Any],
    target_url: str,
    *,
    include_screenshots: bool = True,
    max_screenshots: int | None = None,
) -> str:
    screenshots = data.get("screenshots") or []
    if not isinstance(screenshots, list):
        screenshots = []

    all_screenshot_urls = [url for url in (extract_screenshot_url(item) for item in screenshots) if url]
    screenshot_urls = all_screenshot_urls
    if max_screenshots is not None:
        screenshot_urls = screenshot_urls[:max_screenshots]

    lines = [
        "WhatsLink 元数据",
        f"URL: {target_url}",
        f"名称: {data.get('name') or 'unknown'}",
        f"类型: {data.get('type') or 'unknown'}",
        f"文件类型: {data.get('file_type') or 'unknown'}",
        f"大小: {human_size(data.get('size'))}",
        f"文件数: {data.get('count') if data.get('count') is not None else 'unknown'}",
        f"截图数: {len(screenshots)}",
    ]

    if screenshots and include_screenshots:
        if max_screenshots == 0:
            lines.append("截图 URL: 已按 --max-screenshots 0 隐藏")
        elif screenshot_urls:
            limit_note = ""
            if max_screenshots is not None and len(screenshot_urls) < len(all_screenshot_urls):
                limit_note = f"（仅显示前 {max_screenshots} 张）"
            lines.append(f"截图 URL{limit_note}:")
            lines.extend(f"- {url}" for url in screenshot_urls)
        else:
            lines.append("截图 URL: 未在响应中找到可用 URL")
    elif screenshots and not include_screenshots:
        lines.append("截图 URL: 已隐藏（--no-screenshots）")

    if not data.get("name") and not data.get("size") and not data.get("count"):
        lines.append("提示：WhatsLink 未识别出有用的链接元数据。")

    return "\n".join(lines)


def non_negative_int(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("value must be an integer") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("value must be greater than or equal to 0")
    return value


def positive_timeout(raw: str) -> float:
    try:
        value = float(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("timeout must be a number") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("timeout must be greater than 0")
    return value


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查询公开链接的 WhatsLink 元数据。")
    parser.add_argument("url", help="要检查的公开 URL。不要传入私密、带 token 或内网链接。")
    parser.add_argument("--json", action="store_true", help="输出 WhatsLink 原始 JSON 响应。")
    parser.add_argument("--no-screenshots", action="store_true", help="在人类可读摘要中隐藏截图 URL。")
    parser.add_argument("--max-screenshots", type=non_negative_int, default=None, help="摘要中最多展示的截图 URL 数量（默认：全部）。传 0 表示不列出。")
    parser.add_argument("--timeout", type=positive_timeout, default=20.0, help="请求超时时间，单位秒（默认：20）。")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help=f"API endpoint (default: {DEFAULT_ENDPOINT}).")
    parser.add_argument("--user-agent", default=None, help="可选的自定义 User-Agent。")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        data = fetch_metadata(args.endpoint, args.url, args.timeout, args.user_agent)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        include_screenshots = not args.no_screenshots
        print(format_summary(data, args.url, include_screenshots=include_screenshots, max_screenshots=args.max_screenshots))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
