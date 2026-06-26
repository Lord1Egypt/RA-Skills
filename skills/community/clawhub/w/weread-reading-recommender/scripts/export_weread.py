#!/usr/bin/env python3
"""Export local WeRead data into a raw JSON snapshot."""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


SHELF_SYNC_URL = "https://weread.qq.com/web/shelf/sync"
NOTEBOOK_URL = "https://weread.qq.com/api/user/notebook"
BOOK_INFO_URL = "https://weread.qq.com/api/book/info"
DEFAULT_ENV_VAR = "WEREAD_COOKIE"
DEFAULT_TIMEOUT = 15.0


class ExportError(RuntimeError):
    """Raised when export cannot continue safely."""


@dataclass
class CookieSource:
    source: str
    env_var: Optional[str] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export WeRead shelf and notebook data to a raw JSON file."
    )
    parser.add_argument("--out", required=True, help="Path to write the raw JSON export.")
    parser.add_argument("--cookie", help="Cookie string to use for this run.")
    parser.add_argument("--cookie-file", help="Path to a local file containing the cookie.")
    parser.add_argument(
        "--env-var",
        default=DEFAULT_ENV_VAR,
        help=f"Environment variable name to read cookie from. Default: {DEFAULT_ENV_VAR}",
    )
    parser.add_argument(
        "--include-book-info",
        action="store_true",
        help="Fetch per-book metadata via the book info endpoint.",
    )
    parser.add_argument(
        "--detail-limit",
        type=int,
        default=0,
        help="Max number of books to fetch detail for. 0 means all books when enabled.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help=f"HTTP timeout in seconds. Default: {DEFAULT_TIMEOUT}",
    )
    return parser.parse_args()


def resolve_cookie(args: argparse.Namespace) -> tuple[str, CookieSource]:
    if args.cookie:
        cookie = args.cookie.strip()
        if not cookie:
            raise ExportError("--cookie was provided but is empty.")
        return cookie, CookieSource(source="cli")

    if args.cookie_file:
        cookie_path = Path(args.cookie_file).expanduser()
        if not cookie_path.exists():
            raise ExportError(f"Cookie file does not exist: {cookie_path}")
        if not cookie_path.is_file():
            raise ExportError(f"Cookie path is not a file: {cookie_path}")
        cookie = cookie_path.read_text(encoding="utf-8").strip()
        if not cookie:
            raise ExportError(f"Cookie file is empty: {cookie_path}")
        return cookie, CookieSource(source="file")

    env_name = args.env_var or DEFAULT_ENV_VAR
    cookie = os.environ.get(env_name, "").strip()
    if cookie:
        return cookie, CookieSource(source="env", env_var=env_name)

    raise ExportError(
        "No cookie available. Provide --cookie, --cookie-file, or set the "
        f"{env_name} environment variable."
    )


def build_session(cookie: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Cookie": cookie,
            "Referer": "https://weread.qq.com/",
            "Origin": "https://weread.qq.com",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/123.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/plain, */*",
        }
    )
    return session


def request_json(
    session: requests.Session,
    method: str,
    url: str,
    *,
    timeout: float,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
) -> Any:
    try:
        response = session.request(
            method,
            url,
            timeout=timeout,
            params=params,
            data=data,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExportError(f"Request failed for {url}: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise ExportError(f"Invalid JSON returned by {url}") from exc

    detect_auth_failure(payload, url)
    return payload


def detect_auth_failure(payload: Any, url: str) -> None:
    if isinstance(payload, dict):
        text_fields = [
            str(payload.get("errMsg", "")),
            str(payload.get("errmsg", "")),
            str(payload.get("message", "")),
            str(payload.get("msg", "")),
        ]
        combined = " ".join(text_fields).lower()
        if payload.get("code") in {401, 403} or payload.get("errcode") in {401, 403}:
            raise ExportError(f"Authentication failed for {url}. Cookie may be expired.")
        if any(
            keyword in combined
            for keyword in ("login", "登录", "expired", "unauthorized", "cookie")
        ):
            raise ExportError(f"Authentication failed for {url}. Cookie may be expired.")


def fetch_shelf_sync(session: requests.Session, timeout: float) -> Dict[str, Any]:
    payload = request_json(session, "GET", SHELF_SYNC_URL, timeout=timeout)
    if not isinstance(payload, dict):
        raise ExportError("Unexpected shelf sync payload shape; expected a JSON object.")
    return payload


def fetch_notebook(session: requests.Session, timeout: float) -> Dict[str, Any]:
    payload = request_json(session, "GET", NOTEBOOK_URL, timeout=timeout)
    if not isinstance(payload, dict):
        raise ExportError("Unexpected notebook payload shape; expected a JSON object.")
    return payload


def fetch_book_info(
    session: requests.Session,
    book_ids: Iterable[str],
    timeout: float,
    detail_limit: int,
) -> tuple[Dict[str, Any], List[str]]:
    results: Dict[str, Any] = {}
    warnings: List[str] = []

    unique_book_ids = []
    seen = set()
    for book_id in book_ids:
        if not book_id or book_id in seen:
            continue
        seen.add(book_id)
        unique_book_ids.append(book_id)

    if detail_limit > 0:
        unique_book_ids = unique_book_ids[:detail_limit]

    for book_id in unique_book_ids:
        try:
            payload = request_json(
                session,
                "GET",
                BOOK_INFO_URL,
                timeout=timeout,
                params={"bookId": book_id},
            )
        except ExportError as exc:
            warnings.append(f"Failed to fetch book info for {book_id}: {exc}")
            continue

        results[book_id] = payload

    return results, warnings


def build_summary(shelf_sync: Dict[str, Any], notebook: Dict[str, Any]) -> Dict[str, int]:
    books = shelf_sync.get("books") or []
    progress_items = shelf_sync.get("bookProgress") or []
    notebook_books = notebook.get("books") or []

    progress_by_book = {
        str(item.get("bookId")): item for item in progress_items if item.get("bookId")
    }

    finished_books = 0
    reading_books = 0
    unread_books = 0

    for book in books:
        book_id = str(book.get("bookId", ""))
        is_finished = int(book.get("finishReading") or 0) == 1
        progress = progress_by_book.get(book_id, {}).get("progress") or 0

        if is_finished:
            finished_books += 1
        elif progress and float(progress) > 0:
            reading_books += 1
        else:
            unread_books += 1

    return {
        "total_books": len(books),
        "finished_books": finished_books,
        "reading_books": reading_books,
        "unread_books": unread_books,
        "notebook_books": len(notebook_books),
    }


def extract_book_ids(shelf_sync: Dict[str, Any], notebook: Dict[str, Any]) -> List[str]:
    book_ids: List[str] = []
    for book in shelf_sync.get("books") or []:
        if book.get("bookId"):
            book_ids.append(str(book["bookId"]))
    for book in notebook.get("books") or []:
        if book.get("bookId"):
            book_ids.append(str(book["bookId"]))
    return book_ids


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(out_path: Path, payload: Dict[str, Any]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def print_summary(out_path: Path, summary: Dict[str, int], warnings: List[str]) -> None:
    print(f"Exported WeRead data to {out_path}")
    print(f"  total_books: {summary['total_books']}")
    print(f"  finished_books: {summary['finished_books']}")
    print(f"  reading_books: {summary['reading_books']}")
    print(f"  unread_books: {summary['unread_books']}")
    print(f"  notebook_books: {summary['notebook_books']}")
    if warnings:
        print(f"  warnings: {len(warnings)}")


def main() -> int:
    args = parse_args()

    if args.detail_limit < 0:
        raise ExportError("--detail-limit must be >= 0.")
    if args.timeout <= 0:
        raise ExportError("--timeout must be > 0.")

    cookie, cookie_source = resolve_cookie(args)
    session = build_session(cookie)

    shelf_sync = fetch_shelf_sync(session, args.timeout)
    notebook = fetch_notebook(session, args.timeout)

    warnings: List[str] = []
    book_info: Dict[str, Any] = {}
    if args.include_book_info:
        book_ids = extract_book_ids(shelf_sync, notebook)
        book_info, detail_warnings = fetch_book_info(
            session,
            book_ids,
            args.timeout,
            args.detail_limit,
        )
        warnings.extend(detail_warnings)

    summary = build_summary(shelf_sync, notebook)
    payload: Dict[str, Any] = {
        "exported_at": utc_now_iso(),
        "source": "weread-local-cookie",
        "summary": summary,
        "shelf_sync": shelf_sync,
        "notebook": notebook,
        "book_info": book_info,
    }

    source_meta = {"cookie_source": cookie_source.source}
    if cookie_source.env_var:
        source_meta["cookie_env_var"] = cookie_source.env_var
    payload["source_meta"] = source_meta

    if warnings:
        payload["warnings"] = warnings

    out_path = Path(args.out).expanduser()
    write_json(out_path, payload)
    print_summary(out_path, summary, warnings)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ExportError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
