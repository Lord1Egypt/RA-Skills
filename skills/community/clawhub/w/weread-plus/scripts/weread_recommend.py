#!/usr/bin/env python3
"""Recommend WeRead books using bookshelf, notes, reading stats, and platform recommendations."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from typing import Any

from weread_common import (
    WeReadError,
    api_post,
    book_author,
    book_id,
    book_title,
    compact_text,
    extract_book,
    fail,
    json_dumps,
    matches_reading_state,
    rating_text,
    reading_count_score,
    reading_link,
    reading_state_from_shelf,
    resolve_book,
    search_books,
    seconds_text,
)


MODE_CHOICES = ("safe", "expand", "challenge")


def fetch_notebooks(limit: int = 200) -> list[dict[str, Any]]:
    books: list[dict[str, Any]] = []
    last_sort = None
    while len(books) < limit:
        params: dict[str, Any] = {"count": min(100, limit - len(books))}
        if last_sort:
            params["lastSort"] = last_sort
        data = api_post("/user/notebooks", params)
        page = data.get("books") or []
        books.extend(page)
        if not data.get("hasMore") or not page:
            break
        last_sort = page[-1].get("sort")
        if not last_sort:
            break
    return books


def note_total(item: dict[str, Any]) -> int:
    return int(item.get("reviewCount") or 0) + int(item.get("noteCount") or 0) + int(item.get("bookmarkCount") or 0)


def profile_summary(shelf: dict[str, Any], annual: dict[str, Any], notebooks: list[dict[str, Any]]) -> dict[str, Any]:
    categories = []
    for item in annual.get("preferCategory") or []:
        title = item.get("categoryTitle") or item.get("parentCategoryTitle")
        if title:
            categories.append(str(title))

    shelf_categories = Counter()
    for item in shelf.get("books") or []:
        category = item.get("category")
        if category:
            shelf_categories[str(category)] += 1

    top_note_books = []
    for item in sorted(notebooks, key=note_total, reverse=True)[:8]:
        book = item.get("book") or item
        top_note_books.append(
            {
                "bookId": item.get("bookId") or book.get("bookId"),
                "title": book.get("title"),
                "author": book.get("author"),
                "noteTotal": note_total(item),
                "reviewCount": item.get("reviewCount") or 0,
                "noteCount": item.get("noteCount") or 0,
                "bookmarkCount": item.get("bookmarkCount") or 0,
            }
        )

    read_longest = []
    for item in annual.get("readLongest") or []:
        book = item.get("book") or item.get("albumInfo") or {}
        title = book.get("title") or book.get("name")
        if title:
            read_longest.append(
                {
                    "bookId": book.get("bookId") or book.get("albumId"),
                    "title": title,
                    "author": book.get("author") or book.get("authorName"),
                    "readTime": item.get("readTime"),
                    "readTimeText": seconds_text(item.get("readTime")),
                    "tags": item.get("tags") or [],
                }
            )

    recent_finished = []
    finished_books = [item for item in shelf.get("books") or [] if item.get("finishReading") == 1]
    for book in sorted(finished_books, key=lambda item: int(item.get("readUpdateTime") or 0), reverse=True)[:12]:
        recent_finished.append(
            {
                "bookId": book_id(book),
                "title": book_title(book),
                "author": book_author(book),
            }
        )

    return {
        "shelfBookCount": len(shelf.get("books") or []),
        "shelfAlbumCount": len(shelf.get("albums") or []),
        "preferredCategories": categories[:8],
        "shelfTopCategories": shelf_categories.most_common(8),
        "topNoteBooks": top_note_books,
        "readLongest": read_longest[:8],
        "recentFinishedBooks": recent_finished,
    }


def candidate_key(book: dict[str, Any]) -> str:
    bid = book_id(book)
    if bid:
        return f"id:{bid}"
    return f"title:{book_title(book)}|{book_author(book)}"


def add_candidate(
    candidates: dict[str, dict[str, Any]],
    raw: dict[str, Any],
    *,
    source: str,
    source_reason: str,
    seed_title: str | None = None,
) -> None:
    book = extract_book(raw)
    if not book:
        return
    key = candidate_key(book)
    if key == "title:|":
        return
    existing = candidates.setdefault(
        key,
        {
            "book": book,
            "sources": [],
            "sourceReasons": [],
            "seedTitles": [],
            "score": 0.0,
            "factors": [],
            "warnings": [],
        },
    )
    existing["book"].update({k: v for k, v in book.items() if v not in (None, "", [], {})})
    if source not in existing["sources"]:
        existing["sources"].append(source)
    if source_reason and source_reason not in existing["sourceReasons"]:
        existing["sourceReasons"].append(source_reason)
    if seed_title and seed_title not in existing["seedTitles"]:
        existing["seedTitles"].append(seed_title)


def goal_terms(goal: str | None) -> list[str]:
    if not goal:
        return []
    terms = [goal.strip().lower()]
    terms.extend(part.lower() for part in re.split(r"[\s,，、/]+", goal) if part.strip())
    return sorted(set(term for term in terms if term))


def text_blob(book: dict[str, Any]) -> str:
    values = [
        book.get("title"),
        book.get("author"),
        book.get("category"),
        book.get("intro"),
        book.get("reason"),
        book.get("publisher"),
    ]
    return " ".join(str(value).lower() for value in values if value)


def category_matches(category: str, preferred: list[str]) -> bool:
    if not category:
        return False
    return any(category in item or item in category for item in preferred)


def score_candidate(
    item: dict[str, Any],
    *,
    mode: str,
    profile: dict[str, Any],
    goal: str | None,
    reading_state: dict[str, Any] | None = None,
    shelf_ids: set[str] | None = None,
) -> None:
    book = item["book"]
    factors: list[str] = []
    warnings: list[str] = []
    score = 0.0
    state = reading_state or {
        "shelfIds": shelf_ids or set(),
        "shelfTitleKeys": set(),
        "shelfTitleAuthorKeys": set(),
        "finishedIds": set(),
        "finishedTitleKeys": set(),
        "finishedTitleAuthorKeys": set(),
    }

    sources = set(item["sources"])
    if "personalized" in sources:
        score += 8
        factors.append("来自微信读书个性化推荐")
    if "similar" in sources:
        score += 10
        seeds = "、".join(item["seedTitles"][:3])
        factors.append(f"与高投入种子书相似{f'：{seeds}' if seeds else ''}")
    if "goal-search" in sources:
        score += 8
        factors.append("匹配当前主题搜索")

    category = str(book.get("category") or "")
    preferred_categories = [str(x) for x in profile.get("preferredCategories") or []]
    if category_matches(category, preferred_categories):
        score += 8 if mode == "safe" else 5
        factors.append(f"贴近你的偏好分类：{category}")
    elif category and mode == "expand":
        score += 2
        factors.append(f"提供相邻探索方向：{category}")

    terms = goal_terms(goal)
    if terms:
        blob = text_blob(book)
        matches = [term for term in terms if term in blob]
        if matches:
            score += 10 + min(6, len(matches) * 2)
            factors.append(f"匹配目标关键词：{'、'.join(matches[:3])}")

    rating = book.get("newRating")
    try:
        rating_number = float(rating)
    except (TypeError, ValueError):
        rating_number = 0.0
    if rating_number:
        score += min(8, rating_number / 12.5)
        factors.append(f"公开评分 {rating_text(rating_number)}")

    reading_count = book.get("readingCount")
    crowd_score = reading_count_score(reading_count)
    if crowd_score:
        score += crowd_score
        factors.append(f"有一定阅读热度：{reading_count} 人在读")

    if mode == "challenge":
        challenge_words = ("哲学", "思想", "社会", "历史", "政治", "经济", "科学", "心理", "文化", "管理")
        blob = text_blob(book)
        if any(word in blob for word in challenge_words):
            score += 6
            factors.append("挑战模式加权：主题更偏思想或系统性")
        warnings.append("挑战模式候选可能更难读，需要预留整块时间")
    elif mode == "safe":
        if "similar" in sources:
            score += 4
        warnings.append("稳妥模式会更接近既有口味，探索性较弱")
    else:
        warnings.append("拓展模式保留口味匹配，同时引入相邻主题")

    on_shelf = matches_reading_state(book, state, prefix="shelf")
    finished = matches_reading_state(book, state, prefix="finished")
    item["onShelf"] = on_shelf
    item["finishedReading"] = finished

    if finished:
        score -= 100
        warnings.append("这本书已经读完")
    elif on_shelf:
        score -= 18
        warnings.append("这本书已经在你的书架中")
    else:
        score += 3
        factors.append("不在当前可见电子书书架中")

    if not factors:
        factors.append("元数据较少，建议先试读或查看书评")

    item["score"] = round(score, 2)
    item["factors"] = factors[:8]
    item["warnings"] = warnings[:4]


def fetch_similar_for_seed(seed: dict[str, Any], candidates: dict[str, dict[str, Any]], *, count: int) -> None:
    bid = book_id(seed)
    if not bid:
        return
    data = api_post("/book/similar", {"bookId": bid, "count": count})
    books = data.get("books") or data.get("booksimilar", {}).get("books") or []
    for item in books:
        add_candidate(
            candidates,
            item,
            source="similar",
            source_reason=f"similar to {book_title(seed)}",
            seed_title=book_title(seed),
        )


def markdown_output(result: dict[str, Any]) -> str:
    lines = []
    profile = result["profile"]
    lines.append(f"# 微信读书伴侣推荐")
    lines.append("")
    lines.append(f"- 模式：{result['mode']}")
    if result.get("goal"):
        lines.append(f"- 当前目标：{result['goal']}")
    if profile.get("preferredCategories"):
        lines.append(f"- 偏好分类：{'、'.join(profile['preferredCategories'][:5])}")
    lines.append("")

    for index, item in enumerate(result["recommendations"], 1):
        book = item["book"]
        title = book_title(book) or "未命名"
        author = book_author(book)
        lines.append(f"## {index}. {title}")
        meta = []
        if author:
            meta.append(author)
        if book.get("category"):
            meta.append(str(book.get("category")))
        if book.get("newRating"):
            meta.append(rating_text(book.get("newRating")))
        if item.get("finishedReading"):
            meta.append("已读完")
        if item.get("onShelf"):
            meta.append("已在书架")
        meta.append(f"score {item['score']}")
        lines.append(" / ".join(part for part in meta if part))
        if book.get("reason"):
            lines.append(f"- 平台理由：{compact_text(book.get('reason'), 120)}")
        if book.get("intro"):
            lines.append(f"- 简介：{compact_text(book.get('intro'), 180)}")
        lines.append(f"- 为什么推荐：{'；'.join(item['factors'][:4])}")
        if item.get("warnings"):
            lines.append(f"- 可能不适合：{'；'.join(item['warnings'][:2])}")
        link = reading_link(book_id(book))
        if link:
            lines.append(f"- 打开：{link}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend WeRead books with transparent scoring")
    parser.add_argument("--mode", choices=MODE_CHOICES, default="expand")
    parser.add_argument("--goal", help="Current reading goal or topic")
    parser.add_argument("--seed-book", help="Seed book title for similar recommendations")
    parser.add_argument("--seed-book-id", help="Seed bookId for similar recommendations")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--include-shelf", action="store_true", help="Keep candidates already on shelf")
    parser.add_argument("--include-finished", action="store_true", help="Keep candidates already marked as finished")
    args = parser.parse_args()

    try:
        shelf = api_post("/shelf/sync", {})
        annual = api_post("/readdata/detail", {"mode": "annually"})
        notebooks = fetch_notebooks(limit=200)
    except WeReadError as exc:
        fail(str(exc))

    profile = profile_summary(shelf, annual, notebooks)
    reading_state = reading_state_from_shelf(shelf)
    candidates: dict[str, dict[str, Any]] = {}

    try:
        data = api_post("/book/recommend", {"count": max(12, min(30, args.count * 3))})
        for item in data.get("books") or []:
            add_candidate(candidates, item, source="personalized", source_reason="platform personalized")
    except WeReadError:
        pass

    if args.goal:
        try:
            for book in search_books(args.goal, count=max(10, min(30, args.count * 3)), scope=10):
                add_candidate(candidates, book, source="goal-search", source_reason=args.goal)
        except WeReadError:
            pass

    seeds: list[dict[str, Any]] = []
    if args.seed_book or args.seed_book_id:
        try:
            seed, _ = resolve_book(book=args.seed_book, bookid=args.seed_book_id)
            seeds.append(seed)
        except WeReadError as exc:
            fail(str(exc))

    for item in profile.get("topNoteBooks") or []:
        if item.get("bookId") and item.get("title"):
            seeds.append({"bookId": item["bookId"], "title": item["title"], "author": item.get("author")})
    for item in profile.get("readLongest") or []:
        if item.get("bookId") and item.get("title"):
            seeds.append({"bookId": item["bookId"], "title": item["title"], "author": item.get("author")})

    seen_seed_ids = set()
    unique_seeds = []
    for seed in seeds:
        bid = book_id(seed)
        key = bid or book_title(seed)
        if key and key not in seen_seed_ids:
            seen_seed_ids.add(key)
            unique_seeds.append(seed)

    for seed in unique_seeds[:5]:
        try:
            fetch_similar_for_seed(seed, candidates, count=10)
        except WeReadError:
            continue

    for item in candidates.values():
        score_candidate(item, mode=args.mode, profile=profile, reading_state=reading_state, goal=args.goal)

    ranked = sorted(candidates.values(), key=lambda item: item["score"], reverse=True)
    if not args.include_finished:
        ranked = [item for item in ranked if not item.get("finishedReading")]
    if not args.include_shelf:
        ranked = [item for item in ranked if not item.get("onShelf")]

    result = {
        "mode": args.mode,
        "goal": args.goal,
        "profile": profile,
        "seedBooks": [{"bookId": book_id(seed), "title": book_title(seed), "author": book_author(seed)} for seed in unique_seeds[:5]],
        "recommendations": ranked[: args.count],
    }

    if args.format == "json":
        print(json_dumps(result))
    else:
        print(markdown_output(result))


if __name__ == "__main__":
    main()
