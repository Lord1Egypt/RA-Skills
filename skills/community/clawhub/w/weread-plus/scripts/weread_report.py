#!/usr/bin/env python3
"""Generate WeRead reading reports and bookshelf summaries."""

from __future__ import annotations

import argparse
from collections import Counter
from typing import Any

from weread_common import (
    WeReadError,
    api_post,
    book_author,
    book_id,
    book_title,
    fail,
    json_dumps,
    matching_book_in_state,
    reading_link,
    reading_state_from_shelf,
    seconds_text,
    timestamp_to_date,
)


def reading_report(mode: str) -> dict[str, Any]:
    data = api_post("/readdata/detail", {"mode": mode})
    read_longest = []
    for item in data.get("readLongest") or []:
        book = item.get("book") or item.get("albumInfo") or {}
        read_longest.append(
            {
                "bookId": book.get("bookId") or book.get("albumId"),
                "title": book.get("title") or book.get("name"),
                "author": book.get("author") or book.get("authorName"),
                "readTime": item.get("readTime"),
                "readTimeText": seconds_text(item.get("readTime")),
                "tags": item.get("tags") or [],
            }
        )
    return {
        "mode": mode,
        "baseTime": data.get("baseTime"),
        "readDays": data.get("readDays"),
        "totalReadTime": data.get("totalReadTime"),
        "totalReadTimeText": seconds_text(data.get("totalReadTime")),
        "dayAverageReadTime": data.get("dayAverageReadTime"),
        "dayAverageReadTimeText": seconds_text(data.get("dayAverageReadTime")),
        "compare": data.get("compare"),
        "readStat": data.get("readStat") or [],
        "preferCategory": data.get("preferCategory") or [],
        "preferTimeWord": data.get("preferTimeWord"),
        "preferAuthor": data.get("preferAuthor") or [],
        "preferPublisher": data.get("preferPublisher") or [],
        "readLongest": read_longest,
    }


def build_recent_book_entry(book: dict[str, Any], reading_state: dict[str, Any]) -> dict[str, Any]:
    finished = book.get("finishReading") == 1
    related_finished = matching_book_in_state(book, reading_state, prefix="finished")
    if related_finished and related_finished.get("bookId") == book_id(book):
        related_finished = None
    return {
        "bookId": book_id(book),
        "title": book_title(book),
        "author": book_author(book),
        "category": book.get("category"),
        "readUpdateDate": timestamp_to_date(book.get("readUpdateTime")),
        "finishReading": finished,
        "relatedFinished": bool(related_finished),
        "relatedFinishedBook": related_finished,
        "isTop": book.get("isTop") == 1,
        "secret": book.get("secret") == 1,
        "link": reading_link(book_id(book)),
    }


def shelf_report() -> dict[str, Any]:
    data = api_post("/shelf/sync", {})
    books = data.get("books") or []
    albums = data.get("albums") or []
    mp = data.get("mp")
    reading_state = reading_state_from_shelf(data)
    visible_total = len(books) + len(albums) + (1 if mp else 0)

    category_counts = Counter(str(book.get("category") or "未分类") for book in books)
    private_books = sum(1 for book in books if book.get("secret") == 1)
    private_albums = sum(1 for album in albums if (album.get("albumInfoExtra") or {}).get("secret") == 1)
    private_total = private_books + private_albums + (1 if mp else 0)
    finished = sum(1 for book in books if book.get("finishReading") == 1)
    recent = sorted(books, key=lambda book: int(book.get("readUpdateTime") or 0), reverse=True)[:20]

    return {
        "visibleTotal": visible_total,
        "ebookCount": len(books),
        "albumCount": len(albums),
        "hasMpEntry": bool(mp),
        "privateTotal": private_total,
        "publicTotal": visible_total - private_total,
        "finishedEbookCount": finished,
        "categoryCounts": category_counts.most_common(20),
        "recentBooks": [build_recent_book_entry(book, reading_state) for book in recent],
    }


def markdown_report(result: dict[str, Any]) -> str:
    lines = ["# 微信读书阅读报告", ""]
    if result.get("reading"):
        reading = result["reading"]
        lines.append(f"## 阅读统计：{reading['mode']}")
        lines.append(f"- 阅读天数：{reading.get('readDays')}")
        lines.append(f"- 总时长：{reading.get('totalReadTimeText')}")
        lines.append(f"- 自然日均：{reading.get('dayAverageReadTimeText')}")
        if reading.get("compare") not in (None, ""):
            lines.append(f"- 与上期日均对比：{reading['compare']}")
        if reading.get("readStat"):
            lines.append("- 摘要：" + "；".join(f"{item.get('stat')} {item.get('counts')}" for item in reading["readStat"] if item.get("stat")))
        if reading.get("preferCategory"):
            categories = [item.get("categoryTitle") or item.get("parentCategoryTitle") for item in reading["preferCategory"] if item.get("categoryTitle") or item.get("parentCategoryTitle")]
            lines.append(f"- 偏好分类：{'、'.join(categories[:6])}")
        if reading.get("readLongest"):
            lines.append("")
            lines.append("### 读得最多")
            for index, item in enumerate(reading["readLongest"][:10], 1):
                lines.append(f"{index}. {item.get('title')} / {item.get('author') or ''} / {item.get('readTimeText')}")
        lines.append("")

    if result.get("shelf"):
        shelf = result["shelf"]
        lines.append("## 书架")
        lines.append(f"- 可见条目：{shelf['visibleTotal']}（电子书 {shelf['ebookCount']}，有声书/专辑 {shelf['albumCount']}，文章收藏入口 {1 if shelf['hasMpEntry'] else 0}）")
        lines.append(f"- 公开/私密：{shelf['publicTotal']} / {shelf['privateTotal']}")
        lines.append(f"- 已读完电子书：{shelf['finishedEbookCount']}")
        if shelf.get("categoryCounts"):
            lines.append("- 分类：" + "；".join(f"{name} {count}" for name, count in shelf["categoryCounts"][:8]))
        lines.append("")
        lines.append("### 最近阅读")
        for index, book in enumerate(shelf.get("recentBooks") or [], 1):
            marks = []
            if book.get("finishReading"):
                marks.append("读完")
            if book.get("relatedFinished"):
                related = book.get("relatedFinishedBook") or {}
                marks.append(f"相关版本已读完：{related.get('title') or '同名书'}")
            if book.get("secret"):
                marks.append("私密")
            if book.get("isTop"):
                marks.append("置顶")
            suffix = f" ({'、'.join(marks)})" if marks else ""
            lines.append(f"{index}. {book.get('title')} / {book.get('author') or ''} / {book.get('readUpdateDate') or '无最近时间'}{suffix}")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate WeRead reading and shelf reports")
    parser.add_argument("--mode", choices=("weekly", "monthly", "annually", "overall"), default="monthly")
    parser.add_argument("--shelf", action="store_true", help="Include bookshelf summary")
    parser.add_argument("--reading-only", action="store_true", help="Only include reading stats")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    try:
        result: dict[str, Any] = {"reading": reading_report(args.mode)}
        if args.shelf and not args.reading_only:
            result["shelf"] = shelf_report()
    except WeReadError as exc:
        fail(str(exc))

    print(json_dumps(result) if args.format == "json" else markdown_report(result))


if __name__ == "__main__":
    main()
