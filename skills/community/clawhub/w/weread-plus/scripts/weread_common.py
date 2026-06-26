#!/usr/bin/env python3
"""Shared helpers for the weread-plus skill."""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


GATEWAY_URL = "https://i.weread.qq.com/api/agent/gateway"
DEFAULT_OFFICIAL_SKILL_DIR = Path("~/.codex/skills/weread-skills").expanduser()
FALLBACK_SKILL_VERSION = "1.0.3"


class WeReadError(RuntimeError):
    """Raised for regular API or local configuration failures."""


class UpgradeRequired(WeReadError):
    """Raised when the gateway asks the official skill to upgrade."""


def official_skill_dir() -> Path:
    raw = os.environ.get("WEREAD_OFFICIAL_SKILL_DIR")
    return Path(raw).expanduser() if raw else DEFAULT_OFFICIAL_SKILL_DIR


def official_skill_version() -> str:
    skill_md = official_skill_dir() / "SKILL.md"
    if not skill_md.exists():
        return FALLBACK_SKILL_VERSION
    text = skill_md.read_text(encoding="utf-8")
    match = re.search(r"^version:\s*([^\s]+)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else FALLBACK_SKILL_VERSION


def api_key() -> str:
    key = os.environ.get("WEREAD_API_KEY", "").strip()
    if not key:
        raise WeReadError("WEREAD_API_KEY is not set")
    if not key.startswith("wrk-"):
        raise WeReadError("WEREAD_API_KEY is set but does not look like a WeRead key")
    return key


def json_dumps(data: Any, *, pretty: bool = True) -> str:
    if pretty:
        return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False)
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def make_opener() -> urllib.request.OpenerDirector:
    # Local desktop environments often leave stale localhost proxy variables.
    # Direct Tencent API access is the safest default; opt back into proxies with
    # WEREAD_IGNORE_PROXY=0 when needed.
    if os.environ.get("WEREAD_IGNORE_PROXY", "1") == "0":
        return urllib.request.build_opener()
    return urllib.request.build_opener(urllib.request.ProxyHandler({}))


def api_post(api_name: str, params: dict[str, Any] | None = None, *, timeout: int = 30) -> dict[str, Any]:
    params = dict(params or {})
    if "api_name" in params and params["api_name"] != api_name:
        raise WeReadError("api_name must not be duplicated with a different value")

    body = {"api_name": api_name, **{k: v for k, v in params.items() if k != "api_name"}}
    body.setdefault("skill_version", official_skill_version())

    encoded = json_dumps(body, pretty=False).encode("utf-8")
    request = urllib.request.Request(
        GATEWAY_URL,
        data=encoded,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "User-Agent": "weread-plus/1.0",
        },
    )

    try:
        with make_opener().open(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise WeReadError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise WeReadError(f"Network error: {exc.reason}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WeReadError(f"API did not return JSON: {raw[:500]}") from exc

    if isinstance(data, dict) and data.get("upgrade_info"):
        info = data.get("upgrade_info") or {}
        message = info.get("message") if isinstance(info, dict) else str(info)
        raise UpgradeRequired(message or "WeRead official skill upgrade is required")

    if isinstance(data, dict) and data.get("errcode") not in (None, 0):
        message = data.get("errmsg") or data.get("msg") or json_dumps(data, pretty=False)
        raise WeReadError(f"WeRead API error {data.get('errcode')}: {message}")

    if not isinstance(data, dict):
        raise WeReadError("API returned a non-object JSON response")
    return data


def get_path(value: Any, path: str, default: Any = None) -> Any:
    current = value
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part, default)
        elif isinstance(current, list) and part.isdigit():
            index = int(part)
            current = current[index] if 0 <= index < len(current) else default
        else:
            return default
        if current is default:
            return default
    return current


def first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def compact_text(text: Any, limit: int = 160) -> str:
    if text is None:
        return ""
    s = re.sub(r"\s+", " ", str(text)).strip()
    if len(s) <= limit:
        return s
    return s[: max(0, limit - 1)].rstrip() + "…"


def timestamp_to_date(value: Any) -> str:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return ""
    if number <= 0:
        return ""
    return datetime.fromtimestamp(number).strftime("%Y-%m-%d")


def seconds_text(value: Any) -> str:
    try:
        seconds = int(value)
    except (TypeError, ValueError):
        return ""
    if seconds < 60:
        return f"{seconds}秒"
    minutes = seconds // 60
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}小时{minutes}分钟"
    return f"{minutes}分钟"


def rating_text(value: Any) -> str:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return ""
    if score <= 0:
        return ""
    return f"{score / 10:.1f}/10"


def star_text(value: Any) -> str:
    try:
        score = int(value)
    except (TypeError, ValueError):
        return ""
    if score < 0:
        return "无评分"
    if score <= 5:
        stars = score
    else:
        stars = max(1, min(5, round(score / 20)))
    return "★" * stars + "☆" * (5 - stars)


def reading_count_score(value: Any) -> float:
    try:
        count = int(value)
    except (TypeError, ValueError):
        return 0.0
    if count <= 0:
        return 0.0
    return min(10.0, math.log10(count + 1) * 2.0)


def extract_book(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {}

    candidates = [
        raw,
        raw.get("bookInfo"),
        raw.get("book"),
        get_path(raw, "book.bookInfo"),
        get_path(raw, "bookInfo.book"),
    ]
    base: dict[str, Any] = {}
    for candidate in candidates:
        if isinstance(candidate, dict) and (candidate.get("bookId") or candidate.get("title")):
            base.update(candidate)
            break

    # Preserve useful fields that often live beside bookInfo.
    for key in ("readingCount", "newRating", "newRatingCount", "reason", "searchIdx", "idx"):
        if key in raw and key not in base:
            base[key] = raw[key]
    return base


def book_id(book: dict[str, Any]) -> str:
    return str(book.get("bookId") or book.get("bookid") or "").strip()


def book_title(book: dict[str, Any]) -> str:
    return str(book.get("title") or book.get("name") or "").strip()


def book_author(book: dict[str, Any]) -> str:
    return str(book.get("author") or book.get("authorName") or "").strip()


def normalized_title(value: Any) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[（(][^）)]*[）)]", "", text)
    return re.sub(r"[\s《》〈〉“”\"'‘’:：·.\-—_，,、/]+", "", text)


def normalized_author(value: Any) -> str:
    text = str(value or "").lower()
    text = re.sub(r"[\[【（(][^\]】）)]*[\]】）)]", "", text)
    return re.sub(r"[\s《》〈〉“”\"'‘’:：·.\-—_，,、/]+", "", text)


def book_identity_keys(book: dict[str, Any]) -> tuple[str, str, str]:
    return book_id(book), normalized_title(book_title(book)), normalized_author(book_author(book))


def _book_state_entry(book: dict[str, Any]) -> dict[str, Any]:
    return {
        "bookId": book_id(book),
        "title": book_title(book),
        "author": book_author(book),
    }


def _empty_book_state() -> dict[str, Any]:
    state: dict[str, Any] = {}
    for prefix in ("shelf", "finished"):
        state[f"{prefix}Ids"] = set()
        state[f"{prefix}TitleKeys"] = set()
        state[f"{prefix}TitleAuthorKeys"] = set()
        state[f"{prefix}BooksById"] = {}
        state[f"{prefix}BooksByTitle"] = {}
        state[f"{prefix}BooksByTitleAuthor"] = {}
    return state


def remember_book_state(state: dict[str, Any], book: dict[str, Any], *, prefix: str) -> None:
    bid, title_key, author_key = book_identity_keys(book)
    entry = _book_state_entry(book)
    if bid:
        state[f"{prefix}Ids"].add(bid)
        state[f"{prefix}BooksById"].setdefault(bid, entry)
    if not title_key:
        return
    if len(title_key) >= 4:
        state[f"{prefix}TitleKeys"].add(title_key)
        state[f"{prefix}BooksByTitle"].setdefault(title_key, entry)
    if author_key:
        key = (title_key, author_key)
        state[f"{prefix}TitleAuthorKeys"].add(key)
        state[f"{prefix}BooksByTitleAuthor"].setdefault(key, entry)


def reading_state_from_shelf(shelf: dict[str, Any]) -> dict[str, Any]:
    state = _empty_book_state()
    for item in shelf.get("books") or []:
        remember_book_state(state, item, prefix="shelf")
        if item.get("finishReading") == 1:
            remember_book_state(state, item, prefix="finished")
    return state


def matching_book_in_state(book: dict[str, Any], state: dict[str, Any], *, prefix: str) -> dict[str, Any] | None:
    bid, title_key, author_key = book_identity_keys(book)
    if bid and bid in state.get(f"{prefix}Ids", set()):
        return state.get(f"{prefix}BooksById", {}).get(bid) or {"bookId": bid}
    if title_key and author_key:
        by_title_author = state.get(f"{prefix}BooksByTitleAuthor", {})
        key = (title_key, author_key)
        if key in by_title_author:
            return by_title_author[key]
        for known_title, known_author in state.get(f"{prefix}TitleAuthorKeys", set()):
            if title_key == known_title and (author_key in known_author or known_author in author_key):
                return by_title_author.get((known_title, known_author))
    if title_key and not author_key and len(title_key) >= 4 and title_key in state.get(f"{prefix}TitleKeys", set()):
        return state.get(f"{prefix}BooksByTitle", {}).get(title_key)
    return None


def matches_reading_state(book: dict[str, Any], state: dict[str, Any], *, prefix: str) -> bool:
    return matching_book_in_state(book, state, prefix=prefix) is not None


def reading_link(bookid: str, chapter_uid: Any | None = None) -> str:
    if not bookid:
        return ""
    if chapter_uid not in (None, ""):
        return f"weread://reading?bId={bookid}&chapterUid={chapter_uid}"
    return f"weread://reading?bId={bookid}"


def bestbookmark_link(bookid: str, chapter_uid: Any, range_value: Any, user_vid: Any | None = None) -> str:
    if not bookid or chapter_uid in (None, "") or not range_value:
        return ""
    match = re.match(r"^\s*(\d+)\s*-\s*(\d+)\s*$", str(range_value))
    if not match:
        return ""
    start, end = match.groups()
    link = f"weread://bestbookmark?bookId={bookid}&chapterUid={chapter_uid}&rangeStart={start}&rangeEnd={end}"
    if user_vid not in (None, ""):
        link += f"&userVid={user_vid}"
    return link


def search_books(keyword: str, *, count: int = 8, scope: int = 10) -> list[dict[str, Any]]:
    data = api_post("/store/search", {"keyword": keyword, "scope": scope, "count": count})
    books: list[dict[str, Any]] = []
    for group in data.get("results") or []:
        for item in group.get("books") or []:
            book = extract_book(item)
            if book:
                books.append(book)
    return books


def resolve_book(*, book: str | None = None, bookid: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if bookid:
        info = api_post("/book/info", {"bookId": bookid})
        return extract_book(info) or {"bookId": bookid}, []
    if not book:
        raise WeReadError("Provide --book or --book-id")
    candidates = search_books(book, count=8, scope=10)
    if not candidates:
        raise WeReadError(f"No WeRead book search results for: {book}")

    exact = [item for item in candidates if book_title(item) == book]
    chosen = exact[0] if exact else candidates[0]
    bid = book_id(chosen)
    if bid:
        try:
            info = api_post("/book/info", {"bookId": bid})
            enriched = extract_book(info)
            if enriched:
                chosen.update(enriched)
        except WeReadError:
            pass
    return chosen, candidates


def shelf_book_ids(shelf: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for item in shelf.get("books") or []:
        bid = str(item.get("bookId") or "").strip()
        if bid:
            ids.add(bid)
    return ids


def write_or_print(content: str, output: str | None) -> None:
    if output:
        path = Path(output).expanduser()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(str(path))
    else:
        print(content)


def fail(message: str, *, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def now_stamp() -> int:
    return int(time.time())
