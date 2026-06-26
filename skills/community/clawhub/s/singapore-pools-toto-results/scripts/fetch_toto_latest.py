#!/usr/bin/env python3
"""Fetch latest Singapore Pools TOTO draw results."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DRAW_TYPE_TO_FILE = {
    "normal": "toto_result_top_draws_en.html",
    "cascade": "toto_result_cascade_top_draws_en.html",
    "hongbao": "toto_result_hongbao_top_draws_en.html",
    "special": "toto_result_special_top_draws_en.html",
}

BASE_URL = "https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/"
SINGLE_RESULT_BASE_URL = (
    "https://www.singaporepools.com.sg/en/product/sr/Pages/toto_results.aspx?"
)


def fetch_text(url: str, timeout_seconds: int) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 "
                "Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        body = response.read()
    return body.decode("utf-8", errors="replace")


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return unescape(text).strip()


def first_match(pattern: str, text: str, flags: int = 0) -> str | None:
    match = re.search(pattern, text, flags)
    if not match:
        return None
    return strip_html(match.group(1))


def parse_latest_draw(html: str) -> dict[str, Any]:
    li_match = re.search(r"<li>\s*<div class='tables-wrap'>.*?</li>", html, re.S | re.I)
    if not li_match:
        raise ValueError("Could not find latest draw block in HTML payload.")
    block = li_match.group(0)

    draw_date = first_match(r"class='drawDate'[^>]*>(.*?)</th>", block, re.S | re.I)
    draw_number_raw = first_match(r"class='drawNumber'[^>]*>(.*?)</th>", block, re.S | re.I)
    draw_number_match = re.search(r"(\d+)", draw_number_raw or "")
    draw_number = int(draw_number_match.group(1)) if draw_number_match else None

    winning_numbers: list[int] = []
    for _, value in sorted(
        (
            (int(idx), strip_html(num))
            for idx, num in re.findall(r"class='win(\d+)'[^>]*>(.*?)</td>", block, re.S | re.I)
        ),
        key=lambda x: x[0],
    ):
        try:
            winning_numbers.append(int(value))
        except ValueError:
            continue

    additional_raw = first_match(r"class='additional'[^>]*>(.*?)</td>", block, re.S | re.I)
    additional_number = int(additional_raw) if additional_raw and additional_raw.isdigit() else None

    group_1_prize = first_match(r"class='jackpotPrize'[^>]*>(.*?)</td>", block, re.S | re.I)
    encrypted_query = first_match(
        r"class='btn[^']*linkShowWinningOutlets'[^>]*encryptedQueryString='([^']+)'",
        block,
        re.S | re.I,
    )
    single_result_url = (
        f"{SINGLE_RESULT_BASE_URL}{encrypted_query}" if encrypted_query else None
    )

    winning_shares: list[dict[str, str]] = []
    shares_table_match = re.search(
        r"class='table table-striped tableWinningShares'.*?</table>",
        block,
        re.S | re.I,
    )
    if shares_table_match:
        rows = re.findall(r"<tr>(.*?)</tr>", shares_table_match.group(0), re.S | re.I)
        for row in rows[1:]:
            cells = [strip_html(cell) for cell in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", row, re.S | re.I)]
            if len(cells) == 3 and cells[0].lower().startswith("group"):
                winning_shares.append(
                    {
                        "prize_group": cells[0],
                        "share_amount": cells[1],
                        "winning_shares": cells[2],
                    }
                )

    return {
        "draw_date": draw_date,
        "draw_number": draw_number,
        "winning_numbers": winning_numbers,
        "additional_number": additional_number,
        "group_1_prize": group_1_prize,
        "single_result_url": single_result_url,
        "winning_shares": winning_shares,
    }


def format_text(result: dict[str, Any], draw_type: str, source_url: str) -> str:
    lines = [
        f"Draw type: {draw_type}",
        f"Draw date: {result.get('draw_date') or '-'}",
        f"Draw number: {result.get('draw_number') or '-'}",
        "Winning numbers: "
        + (
            ", ".join(str(n) for n in result.get("winning_numbers", []))
            if result.get("winning_numbers")
            else "-"
        ),
        f"Additional number: {result.get('additional_number') or '-'}",
        f"Group 1 prize: {result.get('group_1_prize') or '-'}",
    ]

    if result.get("single_result_url"):
        lines.append(f"Single draw page: {result['single_result_url']}")
    lines.append(f"Source: {source_url}")

    shares = result.get("winning_shares") or []
    if shares:
        lines.append("Winning shares:")
        for share in shares:
            lines.append(
                f"  - {share['prize_group']}: {share['share_amount']} "
                f"({share['winning_shares']} shares)"
            )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch latest Singapore Pools TOTO result."
    )
    parser.add_argument(
        "--draw-type",
        choices=sorted(DRAW_TYPE_TO_FILE.keys()),
        default="normal",
        help="Result type to fetch (default: normal).",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout in seconds (default: 20).",
    )
    args = parser.parse_args()

    source_url = f"{BASE_URL}{DRAW_TYPE_TO_FILE[args.draw_type]}"

    try:
        html = fetch_text(source_url, timeout_seconds=args.timeout)
        parsed = parse_latest_draw(html)
    except HTTPError as exc:
        print(f"HTTP error from Singapore Pools: {exc.code} {exc.reason}", file=sys.stderr)
        return 2
    except URLError as exc:
        print(f"Network error while fetching Singapore Pools: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"Failed to parse latest TOTO result: {exc}", file=sys.stderr)
        return 3

    payload = {
        "draw_type": args.draw_type,
        "source_url": source_url,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "result": parsed,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(format_text(parsed, args.draw_type, source_url))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
