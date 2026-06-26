#!/usr/bin/env python3
"""Fetch public reviews, single thought authors, and popular-highlight thoughts."""

from __future__ import annotations

import argparse
from typing import Any

from weread_common import (
    WeReadError,
    api_post,
    bestbookmark_link,
    book_author,
    book_id,
    book_title,
    compact_text,
    extract_book,
    fail,
    json_dumps,
    rating_text,
    reading_link,
    resolve_book,
    star_text,
    timestamp_to_date,
)


REVIEW_TYPES = {
    "all": 0,
    "recommend": 1,
    "bad": 2,
    "recent": 3,
    "normal": 4,
}


def clean_author(author: Any) -> dict[str, Any]:
    if not isinstance(author, dict):
        return {}
    return {
        "name": author.get("name") or author.get("nick") or author.get("nickname"),
        "userVid": author.get("userVid") or author.get("vid"),
        "avatar": author.get("avatar"),
    }


def maybe_compact(value: Any, full_content: bool, limit: int = 700) -> Any:
    if full_content:
        return value
    return compact_text(value, limit) if value else value


def clean_review_item(item: dict[str, Any], *, full_content: bool = False) -> dict[str, Any]:
    wrapper = item.get("review") if isinstance(item.get("review"), dict) else item
    review = wrapper.get("review") if isinstance(wrapper.get("review"), dict) else wrapper
    book = extract_book(review.get("book") or {})
    return {
        "idx": item.get("idx") or wrapper.get("idx") or review.get("idx"),
        "reviewId": wrapper.get("reviewId") or review.get("reviewId") or item.get("reviewId"),
        "content": maybe_compact(review.get("content") or review.get("abstract"), full_content),
        "htmlContent": review.get("htmlContent") if full_content else None,
        "star": review.get("star"),
        "starText": star_text(review.get("star")),
        "isFinish": review.get("isFinish"),
        "chapterName": review.get("chapterName"),
        "createDate": timestamp_to_date(review.get("createTime")),
        "author": clean_author(review.get("author")),
        "book": book,
    }


def public_reviews(book: dict[str, Any], review_type: str, count: int, *, full_content: bool = False) -> dict[str, Any]:
    data = api_post(
        "/review/list",
        {
            "bookId": book_id(book),
            "reviewListType": REVIEW_TYPES[review_type],
            "count": count,
        },
    )
    reviews = [clean_review_item(item, full_content=full_content) for item in data.get("reviews") or []]
    return {
        "book": book,
        "reviewType": review_type,
        "summary": {
            "reviewsCnt": data.get("reviewsCnt"),
            "recentTotalCnt": data.get("recentTotalCnt"),
            "reviewsHasMore": data.get("reviewsHasMore"),
            "reviewsHas5Star": data.get("reviewsHas5Star"),
            "reviewsHas1Star": data.get("reviewsHas1Star"),
            "friendCommentCount": data.get("friendCommentCount"),
            "friendUniqueCount": data.get("friendUniqueCount"),
            "deepVRecommendInfo": data.get("deepVRecommendInfo"),
            "deepVRecommendValue": data.get("deepVRecommendValue"),
            "deepVUniqueCount": data.get("deepVUniqueCount"),
        },
        "friendCommentUsers": data.get("friendCommentUsers") or [],
        "reviews": reviews,
    }


def single_review(review_id: str, *, full_content: bool = False) -> dict[str, Any]:
    data = api_post("/review/single", {"reviewId": review_id})
    review = data.get("review") or {}
    return {
        "reviewId": data.get("reviewId") or review_id,
        "content": maybe_compact(review.get("content") or review.get("abstract"), full_content, 1200),
        "htmlContent": data.get("htmlContent") if full_content else None,
        "bookId": review.get("bookId"),
        "chapterUid": review.get("chapterUid"),
        "range": review.get("range"),
        "createDate": timestamp_to_date(review.get("createTime")),
        "author": clean_author(review.get("author")),
        "raw": data,
    }


def popular_thoughts(book: dict[str, Any], highlight_count: int, thought_count: int, *, full_content: bool = False) -> dict[str, Any]:
    data = api_post("/book/bestbookmarks", {"bookId": book_id(book), "chapterUid": 0})
    highlights = []
    for item in (data.get("items") or [])[:highlight_count]:
        chapter_uid = item.get("chapterUid")
        range_value = item.get("range")
        thought_data = {}
        if chapter_uid not in (None, "") and range_value:
            thought_data = api_post(
                "/book/readreviews",
                {
                    "bookId": book_id(book),
                    "chapterUid": chapter_uid,
                    "reviews": [{"range": range_value, "count": thought_count}],
                },
            )
        thought_groups = []
        for group in thought_data.get("reviews") or []:
            page_reviews = []
            for raw_review in group.get("pageReviews") or []:
                review = raw_review.get("review") or {}
                page_reviews.append(
                    {
                        "reviewId": raw_review.get("reviewId") or review.get("reviewId"),
                        "content": maybe_compact(review.get("content"), full_content, 500),
                        "abstract": maybe_compact(review.get("abstract"), full_content, 300),
                        "createDate": timestamp_to_date(review.get("createTime")),
                        "author": clean_author(review.get("author")),
                    }
                )
            thought_groups.append(
                {
                    "range": group.get("range"),
                    "totalCount": group.get("totalCount"),
                    "hasMore": group.get("hasMore"),
                    "pageReviews": page_reviews,
                }
            )
        highlights.append(
            {
                "markText": maybe_compact(item.get("markText"), full_content, 600),
                "totalCount": item.get("totalCount"),
                "chapterUid": chapter_uid,
                "range": range_value,
                "userVid": item.get("userVid"),
                "link": bestbookmark_link(book_id(book), chapter_uid, range_value, item.get("userVid")),
                "thoughtGroups": thought_groups,
            }
        )
    return {"book": book, "highlights": highlights}


def markdown_reviews(result: dict[str, Any]) -> str:
    book = result["book"]
    lines = [f"# {book_title(book)} 公开书评", ""]
    meta = []
    if book_author(book):
        meta.append(book_author(book))
    if book.get("newRating"):
        meta.append(rating_text(book.get("newRating")))
    if meta:
        lines.append(" / ".join(meta))
        lines.append("")
    summary = result.get("summary") or {}
    if summary:
        lines.append("## 概览")
        for key in ("reviewsCnt", "recentTotalCnt", "friendCommentCount", "friendUniqueCount", "deepVUniqueCount"):
            if summary.get(key) not in (None, ""):
                lines.append(f"- {key}: {summary.get(key)}")
        if summary.get("deepVRecommendInfo"):
            info = summary["deepVRecommendInfo"]
            lines.append(f"- 资深会员：{info.get('title', '')} {info.get('subtitle', '')}".strip())
        lines.append("")
    lines.append("## 评论")
    for index, review in enumerate(result.get("reviews") or [], 1):
        author = review.get("author") or {}
        name = author.get("name") or "未知作者"
        lines.append(f"### {index}. {name} {review.get('starText') or ''}".rstrip())
        if author.get("userVid"):
            lines.append(f"- userVid: {author['userVid']}")
        if review.get("createDate"):
            lines.append(f"- 日期：{review['createDate']}")
        if review.get("reviewId"):
            lines.append(f"- reviewId: {review['reviewId']}")
        if review.get("content"):
            lines.append("")
            lines.append(compact_text(review["content"], 260))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def markdown_single(result: dict[str, Any]) -> str:
    author = result.get("author") or {}
    lines = [f"# 想法/评论详情：{result.get('reviewId')}", ""]
    lines.append(f"- 作者：{author.get('name') or '未知'}")
    if author.get("userVid"):
        lines.append(f"- userVid: {author['userVid']}")
    if author.get("avatar"):
        lines.append(f"- avatar: {author['avatar']}")
    if result.get("createDate"):
        lines.append(f"- 日期：{result['createDate']}")
    if result.get("bookId"):
        lines.append(f"- 打开书籍：{reading_link(result['bookId'])}")
    if result.get("content"):
        lines.append("")
        lines.append(compact_text(result["content"], 500))
    return "\n".join(lines).rstrip() + "\n"


def markdown_popular(result: dict[str, Any]) -> str:
    book = result["book"]
    lines = [f"# {book_title(book)} 热门划线与想法", ""]
    for index, highlight in enumerate(result.get("highlights") or [], 1):
        lines.append(f"## {index}. {highlight.get('totalCount') or 0} 人划线")
        if highlight.get("markText"):
            lines.append(f"> {compact_text(highlight['markText'], 360)}")
        if highlight.get("link"):
            lines.append(f"- 打开：{highlight['link']}")
        for group in highlight.get("thoughtGroups") or []:
            if group.get("totalCount") not in (None, ""):
                lines.append(f"- 想法总数：{group['totalCount']}")
            for thought in group.get("pageReviews") or []:
                author = thought.get("author") or {}
                name = author.get("name") or "未知作者"
                content = compact_text(thought.get("content"), 220)
                lines.append(f"  - {name}: {content}")
                if author.get("userVid"):
                    lines.append(f"    userVid: {author['userVid']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect WeRead public reviews and public thought authors")
    parser.add_argument("--book", help="Book title")
    parser.add_argument("--book-id", help="Book ID")
    parser.add_argument("--type", choices=tuple(REVIEW_TYPES), default="all")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--review-id", help="Fetch one review/thought by reviewId and show returned author fields")
    parser.add_argument("--popular-thoughts", action="store_true", help="Fetch thoughts below popular highlights")
    parser.add_argument("--highlight-count", type=int, default=3)
    parser.add_argument("--thought-count", type=int, default=5)
    parser.add_argument("--full-content", action="store_true", help="Return full public review/thought content instead of summaries")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    try:
        if args.review_id:
            result = single_review(args.review_id, full_content=args.full_content)
            print(json_dumps(result) if args.format == "json" else markdown_single(result))
            return

        book, candidates = resolve_book(book=args.book, bookid=args.book_id)
        result = (
            popular_thoughts(book, args.highlight_count, args.thought_count, full_content=args.full_content)
            if args.popular_thoughts
            else public_reviews(book, args.type, args.count, full_content=args.full_content)
        )
        if candidates:
            result["searchCandidates"] = candidates
    except WeReadError as exc:
        fail(str(exc))

    if args.format == "json":
        print(json_dumps(result))
    elif args.popular_thoughts:
        print(markdown_popular(result))
    else:
        print(markdown_reviews(result))


if __name__ == "__main__":
    main()
