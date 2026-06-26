#!/usr/bin/env python3
"""Query flight options from the Variflight ticket API."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = (
    "https://ticket.variflight.com/ticket-api-gateway/open/search/flightListAI"
)
FIXED_FLIGHT_NUM = 10
DEFAULT_TIMEOUT_SECONDS = 20


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("limit must be greater than 0")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Query flight list by departure/arrival IATA code and date."
    )
    parser.add_argument("--dep", required=True, help="Departure IATA city code")
    parser.add_argument("--arr", required=True, help="Arrival IATA city code")
    parser.add_argument("--date", required=True, help="Departure date in YYYY-MM-DD")
    parser.add_argument(
        "--limit",
        type=positive_int,
        help="Only display the first N results in text mode",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON payload instead of formatted lines",
    )
    return parser.parse_args()


def normalize_iata(value: str, field_name: str) -> str:
    normalized = value.strip().upper()
    if not re.fullmatch(r"[A-Z]{3}", normalized):
        raise ValueError(f"{field_name} must be a 3-letter IATA city code")
    return normalized


def normalize_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date must use YYYY-MM-DD format") from exc
    return value


def fetch_flights(dep: str, arr: str, departure_date: str) -> dict[str, Any]:
    params = urlencode(
        {
            "dep": dep,
            "arr": arr,
            "date": departure_date,
            "flightNum": FIXED_FLIGHT_NUM,
        }
    )
    request = Request(
        f"{API_URL}?{params}",
        headers={
            "accept": "application/json",
            "user-agent": "openclaw-flight-search-skill/1.0",
        },
    )

    try:
        with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            raw = response.read().decode(charset)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"request failed: {exc.reason}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError("response was not valid JSON") from exc

    code = payload.get("code")
    if code != 0:
        msg = payload.get("msg") or "unknown API error"
        raise RuntimeError(f"API error {code}: {msg}")

    return payload


def flight_tags(item: dict[str, Any]) -> str:
    tags = item.get("flight_tag") or []
    texts = []
    for tag in tags:
        if isinstance(tag, dict):
            text = str(tag.get("text", "")).strip()
            if text:
                texts.append(text)
    return " / ".join(texts) or "-"


def transfer_text(item: dict[str, Any]) -> str:
    transfer = item.get("transfer")
    if transfer:
        return f"经{transfer}中转"
    return "直飞"


def price_text(item: dict[str, Any]) -> str:
    price = item.get("min_price")
    if price in (None, ""):
        return "价格未知"
    return f"¥{price}"


def print_text(payload: dict[str, Any], limit: int | None) -> None:
    data = payload.get("data") or {}
    info = data.get("info") or {}
    flights = data.get("list") or []

    route = info.get("go") or "未知航线"
    date_label = info.get("date") or "未知日期"
    print(f"航线: {route}")
    print(f"日期: {date_label}")
    print(f"结果数: {len(flights)}")

    if not flights:
        print("未返回航班。")
        return

    display = flights[:limit] if limit else flights
    for index, item in enumerate(display, start=1):
        dep_time = item.get("dep_time") or "--:--"
        dep_name = item.get("dep_name") or "-"
        arr_time = item.get("arr_time") or "--:--"
        arr_name = item.get("arr_name") or "-"
        cabin = item.get("cabin") or "-"
        duration = item.get("duration") or "-"
        print(
            f"{index:>2}. {dep_time} {dep_name} -> {arr_time} {arr_name} | "
            f"{cabin} | {duration} | {price_text(item)} | "
            f"{transfer_text(item)} | {flight_tags(item)}"
        )

    if limit and len(flights) > limit:
        print(f"仅显示前 {limit} 条，完整结果共 {len(flights)} 条。")


def main() -> int:
    args = parse_args()

    try:
        dep = normalize_iata(args.dep, "dep")
        arr = normalize_iata(args.arr, "arr")
        departure_date = normalize_date(args.date)
        payload = fetch_flights(dep, arr, departure_date)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.json:
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        print()
        return 0

    print_text(payload, args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
