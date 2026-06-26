"""Get review summary + a few top reviews for a TCIN via product_review_v1.

NB: the working operation name is singular `product_review_v1` — the plural
form returns HTTP 400.
"""

from __future__ import annotations

import argparse
import sys

from . import _common as c


def fetch(*, tcin: str) -> dict:
    return c.api_get(
        "product_review_v1",
        {"tcin": tcin, "channel": "WEB"},
    )


def trim(raw: dict) -> dict:
    p = c.safe_get(raw, "data", "product", default={}) or {}
    rr = p.get("ratings_and_reviews", {}) or {}
    stats = rr.get("statistics", {}) or {}

    # product_review_v1 returns only summary stats (count + secondary_config).
    # Full review text lives behind a separate Bazaarvoice-style endpoint
    # on r2d2.target.com — not exposed here. Surface what we have plus a hint.
    return {
        "tcin": p.get("tcin"),
        "review_count": stats.get("review_count") or stats.get("count"),
        "average_rating": c.safe_get(stats, "rating", "average"),
        "rating_distribution": c.safe_get(stats, "rating", "distribution"),
        "secondary_attributes": [
            s.get("label") for s in (rr.get("secondary_config") or [])
        ],
        "note": (
            "Full review text is not returned by product_review_v1 — only the "
            "summary count. Use the buy_url to read reviews on target.com."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="reviews", description="Review summary + top reviews for a TCIN."
    )
    p.add_argument("tcin")
    p.add_argument("--raw", action="store_true")
    args = p.parse_args(argv)

    try:
        raw = fetch(tcin=args.tcin)
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    c.emit(raw if args.raw else trim(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
