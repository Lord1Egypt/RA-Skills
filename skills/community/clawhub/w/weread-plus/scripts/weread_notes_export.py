#!/usr/bin/env python3
"""Export personal WeRead highlights and thoughts for one book."""

from __future__ import annotations

import argparse
from collections import defaultdict
from typing import Any

from weread_common import (
    WeReadError,
    api_post,
    bestbookmark_link,
    book_author,
    book_id,
    book_title,
    compact_text,
    fail,
    json_dumps,
    resolve_book,
    timestamp_to_date,
    write_or_print,
)


def fetch_mine_reviews(bookid: str, limit: int = 500) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    synckey = 0
    while len(reviews) < limit:
        data = api_post("/review/list/mine", {"bookid": bookid, "count": min(100, limit - len(reviews)), "synckey": synckey})
        page = data.get("reviews") or []
        reviews.extend(page)
        if not data.get("hasMore") or not page:
            break
        synckey = data.get("synckey") or 0
        if not synckey:
            break
    return reviews


def chapter_map(chapters: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    mapping = {}
    for chapter in chapters or []:
        uid = str(chapter.get("chapterUid") or "")
        if uid:
            mapping[uid] = chapter
    return mapping


def clean_mine_review(raw: dict[str, Any]) -> dict[str, Any]:
    review = raw.get("review") if isinstance(raw.get("review"), dict) else raw
    return {
        "reviewId": review.get("reviewId") or raw.get("reviewId"),
        "content": review.get("content"),
        "abstract": review.get("abstract"),
        "chapterUid": review.get("chapterUid"),
        "chapterName": review.get("chapterName"),
        "range": review.get("range"),
        "star": review.get("star"),
        "isFinish": review.get("isFinish"),
        "createDate": timestamp_to_date(review.get("createTime")),
    }


def export_data(book: dict[str, Any]) -> dict[str, Any]:
    bid = book_id(book)
    bookmarks_data = api_post("/book/bookmarklist", {"bookId": bid})
    mine_reviews_raw = fetch_mine_reviews(bid)
    chapters = bookmarks_data.get("chapters") or []
    chapters_by_uid = chapter_map(chapters)

    highlights = []
    for raw in bookmarks_data.get("updated") or []:
        chapter_uid = raw.get("chapterUid")
        range_value = raw.get("range")
        chapter = chapters_by_uid.get(str(chapter_uid), {})
        highlights.append(
            {
                "bookmarkId": raw.get("bookmarkId"),
                "chapterUid": chapter_uid,
                "chapterTitle": chapter.get("title"),
                "markText": raw.get("markText"),
                "range": range_value,
                "colorStyle": raw.get("colorStyle"),
                "createDate": timestamp_to_date(raw.get("createTime")),
                "link": bestbookmark_link(bid, chapter_uid, range_value),
            }
        )

    thoughts = [clean_mine_review(raw) for raw in mine_reviews_raw]
    return {
        "book": book,
        "summary": {
            "highlightCount": len(highlights),
            "thoughtCount": len(thoughts),
            "chapterCount": len(chapters),
            "bookmarkContentAvailable": False,
        },
        "chapters": chapters,
        "highlights": highlights,
        "thoughts": thoughts,
    }


def markdown_export(data: dict[str, Any]) -> str:
    book = data["book"]
    lines = [f"# {book_title(book)} 笔记导出", ""]
    if book_author(book):
        lines.append(f"作者：{book_author(book)}")
        lines.append("")
    summary = data["summary"]
    lines.append("## 概览")
    lines.append(f"- 划线：{summary['highlightCount']} 条")
    lines.append(f"- 想法/点评：{summary['thoughtCount']} 条")
    lines.append("- 书签：当前官方接口只提供数量口径，不导出书签内容")
    lines.append("")

    highlights_by_chapter: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in data.get("highlights") or []:
        key = item.get("chapterTitle") or f"章节 {item.get('chapterUid') or '未知'}"
        highlights_by_chapter[key].append(item)

    thoughts_by_anchor: dict[str, list[dict[str, Any]]] = defaultdict(list)
    loose_thoughts: list[dict[str, Any]] = []
    for thought in data.get("thoughts") or []:
        anchor = f"{thought.get('chapterUid')}|{thought.get('range')}"
        if thought.get("chapterUid") and thought.get("range"):
            thoughts_by_anchor[anchor].append(thought)
        else:
            loose_thoughts.append(thought)

    lines.append("## 划线")
    for chapter_title, items in highlights_by_chapter.items():
        lines.append(f"### {chapter_title}")
        for index, item in enumerate(items, 1):
            lines.append(f"{index}. {item.get('createDate') or ''}".rstrip())
            if item.get("markText"):
                lines.append(f"> {item['markText']}")
            if item.get("link"):
                lines.append(f"打开：{item['link']}")
            anchor = f"{item.get('chapterUid')}|{item.get('range')}"
            for thought in thoughts_by_anchor.get(anchor, []):
                if thought.get("content"):
                    lines.append(f"想法：{thought['content']}")
            lines.append("")

    if loose_thoughts:
        lines.append("## 无法关联到具体划线的想法/点评")
        for thought in loose_thoughts:
            label = thought.get("chapterName") or "整本书/未知位置"
            lines.append(f"### {label}")
            if thought.get("createDate"):
                lines.append(f"- 日期：{thought['createDate']}")
            if thought.get("star") not in (None, "", -1):
                lines.append(f"- 评分：{thought['star']}")
            if thought.get("content"):
                lines.append("")
                lines.append(compact_text(thought["content"], 1200))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Export personal WeRead notes for one book")
    parser.add_argument("--book", help="Book title")
    parser.add_argument("--book-id", help="Book ID")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", help="Optional output path")
    args = parser.parse_args()

    try:
        book, candidates = resolve_book(book=args.book, bookid=args.book_id)
        data = export_data(book)
        if candidates:
            data["searchCandidates"] = candidates
    except WeReadError as exc:
        fail(str(exc))

    content = json_dumps(data) if args.format == "json" else markdown_export(data)
    write_or_print(content, args.output)


if __name__ == "__main__":
    main()
