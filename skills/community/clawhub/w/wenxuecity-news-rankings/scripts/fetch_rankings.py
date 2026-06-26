#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


WENXUECITY_NEWS_URL = "https://www.wenxuecity.com/news/"
# Keep source ASCII-only (more portable across shells/editors); Python will render these as Unicode.
HOT_24H_LABEL = "\u0032\u0034\u5c0f\u65f6\u70ed\u70b9\u6392\u884c"  # 24小时热点排行
DISCUSS_24H_LABEL = "\u0032\u0034\u5c0f\u65f6\u8ba8\u8bba\u6392\u884c"  # 24小时讨论排行


@dataclass(frozen=True)
class RankingItem:
    rank: int
    title: str
    url: str
    image_url: str | None = None


class _WenxuecityRankingsParser(HTMLParser):
    def __init__(self, *, base_url: str) -> None:
        super().__init__(convert_charrefs=True)
        self._base_url = base_url
        self._tag_stack: list[str] = []

        self._in_hourlist = False
        self._hourlist_depth: int | None = None
        self._hourlist_label: str | None = None
        self._hourlist_items: list[RankingItem] = []

        self._in_h4 = False
        self._h4_buf: list[str] = []

        self._in_item = False
        self._item_depth: int | None = None
        self._item_href: str | None = None
        self._item_title_buf: list[str] = []
        self._item_image_url: str | None = None

        self._in_title_div = False
        self._title_div_depth: int | None = None

        self._in_title_a = False

        self.rankings: dict[str, list[RankingItem]] = {}

    @staticmethod
    def _get_attr(attrs: list[tuple[str, str | None]], name: str) -> str | None:
        for k, v in attrs:
            if k == name:
                return v
        return None

    @staticmethod
    def _classes(attrs: list[tuple[str, str | None]]) -> set[str]:
        klass = _WenxuecityRankingsParser._get_attr(attrs, "class") or ""
        return {c for c in klass.split() if c}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._tag_stack.append(tag)
        depth = len(self._tag_stack)

        if tag == "div":
            classes = self._classes(attrs)
            if (not self._in_hourlist) and ("block" in classes and "hourlist" in classes):
                self._in_hourlist = True
                self._hourlist_depth = depth
                self._hourlist_label = None
                self._hourlist_items = []
                return

            if self._in_hourlist and (not self._in_item) and ("imagetitle_left" in classes):
                self._in_item = True
                self._item_depth = depth
                self._item_href = None
                self._item_title_buf = []
                self._item_image_url = None
                self._in_title_div = False
                self._title_div_depth = None
                self._in_title_a = False
                return

            if self._in_item and ("title" in classes):
                self._in_title_div = True
                self._title_div_depth = depth
                return

        if self._in_hourlist and tag == "h4":
            self._in_h4 = True
            self._h4_buf = []
            return

        if self._in_item and tag == "img":
            src = self._get_attr(attrs, "src")
            if src and not self._item_image_url:
                self._item_image_url = urljoin(self._base_url, src)
            return

        if self._in_title_div and tag == "a":
            href = self._get_attr(attrs, "href")
            if href:
                self._item_href = urljoin(self._base_url, href)
            self._in_title_a = True
            return

    def handle_data(self, data: str) -> None:
        if self._in_h4:
            self._h4_buf.append(data)
            return
        if self._in_title_a:
            self._item_title_buf.append(data)
            return

    def handle_endtag(self, tag: str) -> None:
        depth = len(self._tag_stack)

        if tag == "h4" and self._in_h4:
            self._in_h4 = False
            label = "".join(self._h4_buf).strip()
            if label:
                self._hourlist_label = label
            self._h4_buf = []

        if tag == "a" and self._in_title_a:
            self._in_title_a = False

        if tag == "div" and self._in_title_div and self._title_div_depth == depth:
            self._in_title_div = False
            self._title_div_depth = None

        if tag == "div" and self._in_item and self._item_depth == depth:
            title = " ".join("".join(self._item_title_buf).split()).strip()
            href = (self._item_href or "").strip()
            if title and href:
                self._hourlist_items.append(
                    RankingItem(
                        rank=len(self._hourlist_items) + 1,
                        title=title,
                        url=href,
                        image_url=self._item_image_url,
                    )
                )
            self._in_item = False
            self._item_depth = None
            self._item_href = None
            self._item_title_buf = []
            self._item_image_url = None

        if tag == "div" and self._in_hourlist and self._hourlist_depth == depth:
            label = (self._hourlist_label or "").strip()
            if label and self._hourlist_items:
                self.rankings[label] = list(self._hourlist_items)
            self._in_hourlist = False
            self._hourlist_depth = None
            self._hourlist_label = None
            self._hourlist_items = []

        if self._tag_stack:
            self._tag_stack.pop()


def _fetch_html(url: str, *, timeout_s: float, user_agent: str) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
        },
    )
    with urlopen(req, timeout=timeout_s) as resp:
        raw = resp.read()
        charset = "utf-8"
        content_type = resp.headers.get("Content-Type") or ""
        if "charset=" in content_type:
            charset = content_type.split("charset=", 1)[1].split(";", 1)[0].strip() or charset
        return raw.decode(charset, errors="replace")


def _retry_fetch_html(
    url: str, *, timeout_s: float, user_agent: str, retries: int, backoff_s: float
) -> str:
    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return _fetch_html(url, timeout_s=timeout_s, user_agent=user_agent)
        except (HTTPError, URLError, TimeoutError) as exc:
            last_exc = exc
            if attempt >= retries:
                break
            time.sleep(backoff_s * (2**attempt))
    assert last_exc is not None
    raise last_exc


def _render_markdown(
    *,
    fetched_at: datetime,
    source_url: str,
    hot_items: list[RankingItem],
    discuss_items: list[RankingItem],
    include_images: bool,
    requested_top: int,
) -> str:
    lines: list[str] = []
    lines.append("# 文学城新闻 24小时排行")
    lines.append(f"- 抓取时间: {fetched_at.isoformat(timespec='seconds')}")
    lines.append(f"- 来源: {source_url}")
    lines.append(f"- Top 参数: {requested_top} (实际: 热点 {len(hot_items)} / 讨论 {len(discuss_items)})")
    lines.append("")

    def add_section(title: str, items: list[RankingItem]) -> None:
        lines.append(f"## {title}")
        if not items:
            lines.append("_未抓取到条目_")
            lines.append("")
            return
        for it in items:
            if include_images and it.image_url:
                lines.append(f"{it.rank}. [{it.title}]({it.url})  \n   ![]({it.image_url})")
            else:
                lines.append(f"{it.rank}. [{it.title}]({it.url})")
        lines.append("")

    add_section(HOT_24H_LABEL, hot_items)
    add_section(DISCUSS_24H_LABEL, discuss_items)
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch Wenxuecity 24h hot & discussion rankings from https://www.wenxuecity.com/news/."
    )
    parser.add_argument("--url", default=WENXUECITY_NEWS_URL, help="Source page URL.")
    parser.add_argument("--top", type=int, default=15, help="Keep only top N (0 = all).")
    parser.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Output format.",
    )
    parser.add_argument("--output", default="", help="Write output to a file instead of stdout.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON.")
    parser.add_argument("--include-images", action="store_true", help="Include image_url in output.")
    parser.add_argument("--timeout", type=float, default=15.0, help="HTTP timeout seconds.")
    parser.add_argument("--retries", type=int, default=2, help="Retry count on transient failures.")
    parser.add_argument("--backoff", type=float, default=0.8, help="Backoff base seconds.")
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Exit 0 even if one of the two rankings is missing.",
    )
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    fetched_at = datetime.now().astimezone()

    try:
        html = _retry_fetch_html(
            args.url,
            timeout_s=args.timeout,
            user_agent="wenxuecity-news-rankings/1.0 (+https://www.wenxuecity.com/news/)",
            retries=max(0, args.retries),
            backoff_s=max(0.0, args.backoff),
        )
    except Exception as exc:
        print(f"[ERROR] fetch failed: {exc}", file=sys.stderr)
        return 2

    parser_ = _WenxuecityRankingsParser(base_url=args.url)
    parser_.feed(html)

    hot_items = parser_.rankings.get(HOT_24H_LABEL, [])
    discuss_items = parser_.rankings.get(DISCUSS_24H_LABEL, [])

    if args.top and args.top > 0:
        hot_items = hot_items[: args.top]
        discuss_items = discuss_items[: args.top]

    ok_hot = bool(hot_items)
    ok_discuss = bool(discuss_items)

    if args.format == "json":
        payload: dict[str, Any] = {
            "fetched_at": fetched_at.isoformat(timespec="seconds"),
            "source_url": args.url,
            "requested_top": args.top,
            "counts": {"hot_24h": len(hot_items), "discussion_24h": len(discuss_items)},
            "rankings": {
                "hot_24h": [
                    {
                        "rank": it.rank,
                        "title": it.title,
                        "url": it.url,
                        **({"image_url": it.image_url} if args.include_images else {}),
                    }
                    for it in hot_items
                ],
                "discussion_24h": [
                    {
                        "rank": it.rank,
                        "title": it.title,
                        "url": it.url,
                        **({"image_url": it.image_url} if args.include_images else {}),
                    }
                    for it in discuss_items
                ],
            },
            "found": {"hot_24h": ok_hot, "discussion_24h": ok_discuss},
        }
        text = json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None) + "\n"
    else:
        text = _render_markdown(
            fetched_at=fetched_at,
            source_url=args.url,
            hot_items=hot_items,
            discuss_items=discuss_items,
            include_images=bool(args.include_images),
            requested_top=int(args.top),
        )

    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    else:
        sys.stdout.write(text)

    if (ok_hot and ok_discuss) or args.allow_partial:
        return 0

    missing = []
    if not ok_hot:
        missing.append(HOT_24H_LABEL)
    if not ok_discuss:
        missing.append(DISCUSS_24H_LABEL)
    print(f"[ERROR] missing rankings: {', '.join(missing)}", file=sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
