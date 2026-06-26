#!/usr/bin/env python3
"""Normalize raw WeRead export data into recommendation-friendly JSON."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize a raw WeRead export into recommendation-friendly JSON."
    )
    parser.add_argument("--input", required=True, help="Path to raw WeRead JSON.")
    parser.add_argument("--output", required=True, help="Path to normalized JSON output.")
    return parser.parse_args()


def load_raw(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("Raw WeRead export must be a JSON object.")
    return payload


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_to_iso(value: Any) -> Optional[str]:
    if value in (None, "", 0, "0"):
        return None
    try:
        timestamp = int(value)
    except (TypeError, ValueError):
        return None
    if timestamp <= 0:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_categories(book: Dict[str, Any], info: Dict[str, Any]) -> List[str]:
    categories: List[str] = []
    for source in (book.get("categories"), info.get("categories")):
        if not source:
            continue
        for item in source:
            if isinstance(item, dict):
                name = item.get("title") or item.get("name")
            else:
                name = item
            if name:
                categories.append(str(name).strip())
    return dedupe_preserve_order(categories)


def build_book_lists_map(archives: Iterable[Dict[str, Any]]) -> Dict[str, List[str]]:
    mapping: Dict[str, List[str]] = {}
    for archive in archives or []:
        list_name = str(archive.get("name") or "").strip()
        if not list_name:
            continue
        for book_id in archive.get("bookIds") or []:
            book_key = str(book_id)
            mapping.setdefault(book_key, []).append(list_name)
    for book_id, names in mapping.items():
        mapping[book_id] = dedupe_preserve_order(names)
    return mapping


def compute_status(book: Dict[str, Any], progress: Dict[str, Any]) -> Tuple[str, bool]:
    is_finished = int(book.get("finishReading") or 0) == 1
    progress_value = float(progress.get("progress") or 0)
    if is_finished:
        return "finished", True
    if progress_value > 0:
        return "reading", False
    return "unread", False


def compute_engagement_score(
    *,
    is_finished: bool,
    progress: float,
    reading_time_seconds: int,
    note_count: int,
    bookmark_count: int,
    review_count: int,
    last_read_at: Optional[str],
) -> float:
    score = 0.0

    if is_finished:
        score += 25.0

    score += min(max(progress, 0.0), 100.0) * 0.25
    score += min(reading_time_seconds / 3600.0, 20.0) * 1.5

    interaction_score = note_count * 2.5 + bookmark_count * 1.0 + review_count * 4.0
    score += min(interaction_score, 25.0)

    if last_read_at:
        try:
            last_dt = datetime.fromisoformat(last_read_at.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_days = max((now - last_dt).days, 0)
            recency_bonus = max(0.0, 15.0 - min(age_days, 90) / 6.0)
            score += recency_bonus
        except ValueError:
            pass

    return round(min(score, 100.0), 1)


def normalize_books(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    shelf_sync = raw.get("shelf_sync") or {}
    notebook = raw.get("notebook") or {}
    book_info = raw.get("book_info") or {}

    books = shelf_sync.get("books") or []
    progress_items = shelf_sync.get("bookProgress") or []
    progress_by_book = {
        str(item.get("bookId")): item for item in progress_items if item.get("bookId")
    }
    notebook_by_book = {
        str(item.get("bookId")): item for item in (notebook.get("books") or []) if item.get("bookId")
    }
    book_lists_map = build_book_lists_map(shelf_sync.get("archive") or [])

    normalized: List[Dict[str, Any]] = []
    for book in books:
        book_id = str(book.get("bookId") or "").strip()
        if not book_id:
            continue

        progress_item = progress_by_book.get(book_id, {})
        notebook_item = notebook_by_book.get(book_id, {})
        info = book_info.get(book_id) or {}

        status, is_finished = compute_status(book, progress_item)
        progress = float(progress_item.get("progress") or 0)
        reading_time_seconds = int(progress_item.get("readingTime") or 0)
        last_read_at = timestamp_to_iso(progress_item.get("updateTime"))
        note_count = int(notebook_item.get("noteCount") or 0)
        bookmark_count = int(notebook_item.get("bookmarkCount") or 0)
        review_count = int(notebook_item.get("reviewCount") or 0)
        interaction_count = note_count + bookmark_count + review_count
        public_rating = extract_public_rating(info)

        record = {
            "book_id": book_id,
            "title": str(book.get("title") or info.get("title") or "").strip(),
            "author": str(book.get("author") or info.get("author") or "").strip(),
            "translator": str(book.get("translator") or info.get("translator") or "").strip(),
            "categories": parse_categories(book, info),
            "book_lists": book_lists_map.get(book_id, []),
            "status": status,
            "is_finished": is_finished,
            "progress": round(progress, 1),
            "reading_time_seconds": reading_time_seconds,
            "last_read_at": last_read_at,
            "note_count": note_count,
            "bookmark_count": bookmark_count,
            "review_count": review_count,
            "interaction_count": interaction_count,
            "engagement_score": compute_engagement_score(
                is_finished=is_finished,
                progress=progress,
                reading_time_seconds=reading_time_seconds,
                note_count=note_count,
                bookmark_count=bookmark_count,
                review_count=review_count,
                last_read_at=last_read_at,
            ),
            "is_imported": book_id.startswith("CB_"),
            "is_paid": bool(int(book.get("paid") or 0)),
            "public_rating": public_rating,
            "intro": str(info.get("intro") or "").strip(),
        }
        normalized.append(record)

    normalized.sort(
        key=lambda item: (
            item["engagement_score"],
            item["last_read_at"] or "",
            item["title"],
        ),
        reverse=True,
    )
    return normalized


def extract_public_rating(info: Dict[str, Any]) -> Optional[float]:
    rating = info.get("newRating")
    if rating in (None, ""):
        return None
    try:
        numeric = float(rating)
    except (TypeError, ValueError):
        return None
    return round(numeric / 1000.0, 2) if numeric > 100 else round(numeric, 2)


def build_summary(books: List[Dict[str, Any]]) -> Dict[str, Any]:
    status_counts = Counter(book["status"] for book in books)
    category_counter: Counter[str] = Counter()
    category_weighted: Counter[str] = Counter()
    book_list_counter: Counter[str] = Counter()
    book_list_weighted: Counter[str] = Counter()
    imported_vs_native = {"imported": 0, "native": 0}

    for book in books:
        if book["is_imported"]:
            imported_vs_native["imported"] += 1
        else:
            imported_vs_native["native"] += 1

        for name in book["categories"]:
            category_counter[name] += 1
            category_weighted[name] += book["engagement_score"]

        for name in book["book_lists"]:
            book_list_counter[name] += 1
            book_list_weighted[name] += book["engagement_score"]

    top_categories = [
        {
            "name": name,
            "books": count,
            "weighted_score": round(category_weighted[name], 1),
        }
        for name, count in category_counter.most_common(8)
    ]
    top_book_lists = [
        {
            "name": name,
            "books": count,
            "weighted_score": round(book_list_weighted[name], 1),
        }
        for name, count in book_list_counter.most_common(8)
    ]

    return {
        "total_books": len(books),
        "status_counts": {
            "finished": status_counts.get("finished", 0),
            "reading": status_counts.get("reading", 0),
            "unread": status_counts.get("unread", 0),
        },
        "top_categories": top_categories,
        "top_book_lists": top_book_lists,
        "imported_vs_native": imported_vs_native,
    }


def build_profile_inputs(books: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    highest_engagement = sorted(
        books, key=lambda item: (item["engagement_score"], item["title"]), reverse=True
    )[:5]
    recent_books = sorted(
        (book for book in books if book["last_read_at"]),
        key=lambda item: item["last_read_at"],
        reverse=True,
    )[:5]
    unfinished_books = sorted(
        (
            book
            for book in books
            if not book["is_finished"]
            and (book["progress"] > 0 or book["reading_time_seconds"] > 0)
        ),
        key=lambda item: (
            momentum_score(item),
            item["last_read_at"] or "",
        ),
        reverse=True,
    )[:5]

    return {
        "highest_engagement_books": [profile_book_view(book) for book in highest_engagement],
        "recent_books": [profile_book_view(book) for book in recent_books],
        "unfinished_books_with_momentum": [profile_book_view(book) for book in unfinished_books],
    }


def momentum_score(book: Dict[str, Any]) -> float:
    return round(
        float(book["progress"]) * 0.6
        + min(book["reading_time_seconds"] / 3600.0, 12.0) * 3.0
        + book["interaction_count"] * 1.5,
        1,
    )


def profile_book_view(book: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "book_id": book["book_id"],
        "title": book["title"],
        "author": book["author"],
        "status": book["status"],
        "progress": book["progress"],
        "engagement_score": book["engagement_score"],
        "last_read_at": book["last_read_at"],
        "categories": book["categories"],
    }


def build_llm_hints(books: List[Dict[str, Any]], summary: Dict[str, Any]) -> List[str]:
    hints: List[str] = []

    recent_books = [book for book in books if book["last_read_at"]]
    if recent_books:
        recent_categories = Counter(
            category
            for book in sorted(recent_books, key=lambda item: item["last_read_at"], reverse=True)[:5]
            for category in book["categories"]
        )
        if recent_categories:
            names = ", ".join(name for name, _ in recent_categories.most_common(3))
            hints.append(f"最近阅读重心偏向：{names}。")

    engaged_books = [book for book in books if book["engagement_score"] >= 60]
    if engaged_books:
        engaged_categories = Counter(
            category for book in engaged_books for category in book["categories"]
        )
        if engaged_categories:
            names = ", ".join(name for name, _ in engaged_categories.most_common(3))
            hints.append(f"高互动书主要集中在：{names}。")

    finished_categories = Counter(
        category for book in books if book["is_finished"] for category in book["categories"]
    )
    if finished_categories:
        names = ", ".join(name for name, _ in finished_categories.most_common(3))
        hints.append(f"完读率较高的类型包括：{names}。")

    status_counts = summary["status_counts"]
    if status_counts["reading"] > 0:
        hints.append(f"当前有 {status_counts['reading']} 本书处于在读状态，可优先判断是否续读。")

    imported_count = summary["imported_vs_native"]["imported"]
    if imported_count > 0:
        hints.append(f"书架里有 {imported_count} 本导入书，推荐时注意区分导入来源与原生微信读书书籍。")

    return hints[:6]


def dedupe_preserve_order(values: Iterable[str]) -> List[str]:
    seen = set()
    result: List[str] = []
    for value in values:
        cleaned = str(value).strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()

    raw = load_raw(input_path)
    books = normalize_books(raw)
    summary = build_summary(books)
    profile_inputs = build_profile_inputs(books)
    llm_hints = build_llm_hints(books, summary)

    payload = {
        "generated_at": utc_now_iso(),
        "source_file": str(input_path),
        "summary": summary,
        "profile_inputs": profile_inputs,
        "llm_hints": llm_hints,
        "books": books,
    }
    write_json(output_path, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
