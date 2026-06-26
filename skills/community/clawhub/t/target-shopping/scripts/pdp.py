"""Get Target product details by TCIN via pdp_client_v1."""

from __future__ import annotations

import argparse
import sys

from . import _common as c


def fetch(*, tcin: str, store_id: str, pricing_store_id: str, visitor_id: str) -> dict:
    params = {
        "tcin": tcin,
        "store_id": store_id,
        "pricing_store_id": pricing_store_id,
        "has_pricing_store_id": "true",
        "channel": "WEB",
        "visitor_id": visitor_id,
    }
    return c.api_get("pdp_client_v1", params)


def trim(raw: dict) -> dict:
    p = c.safe_get(raw, "data", "product", default={}) or {}
    item = p.get("item", {}) or {}
    pd = item.get("product_description", {}) or {}
    enr = item.get("enrichment", {}) or {}
    price = p.get("price", {}) or {}
    rr = c.safe_get(p, "ratings_and_reviews", "statistics", default={}) or {}

    return {
        "tcin": p.get("tcin"),
        "title": pd.get("title"),
        "brand": c.safe_get(item, "primary_brand", "name"),
        "description": pd.get("downstream_description"),
        "bullets": pd.get("bullet_descriptions") or [],
        "price": {
            "formatted": price.get("formatted_current_price"),
            "current": price.get("current_retail"),
            "reg": price.get("reg_retail"),
            "current_min": price.get("current_retail_min"),
            "current_max": price.get("current_retail_max"),
        },
        "rating": {
            "average": c.safe_get(rr, "rating", "average"),
            "count": rr.get("review_count") or c.safe_get(rr, "rating", "count"),
        },
        "buy_url": enr.get("buy_url"),
        "images": {
            "primary": c.safe_get(enr, "image_info", "primary_image", "url"),
            "alternates": [
                a.get("url")
                for a in (c.safe_get(enr, "image_info", "alternate_images", default=[]) or [])
            ],
        },
        "promotions": [
            {
                "id": pr.get("promotion_id"),
                "message": pr.get("threshold_message")
                or pr.get("promotion_short_description"),
            }
            for pr in (p.get("promotions") or [])
        ],
        "variants": [
            {
                "tcin": ch.get("tcin"),
                "title": c.safe_get(
                    ch, "item", "product_description", "title"
                ),
                "price": c.safe_get(ch, "price", "formatted_current_price"),
            }
            for ch in (p.get("children") or [])
        ],
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="pdp", description="Get Target product details by TCIN."
    )
    p.add_argument("tcin")
    p.add_argument("--store-id", default=c.get_default_store())
    p.add_argument("--pricing-store-id", default=None)
    p.add_argument("--visitor-id", default=c.DEFAULT_VISITOR_ID)
    p.add_argument("--raw", action="store_true")
    args = p.parse_args(argv)

    pricing = args.pricing_store_id or args.store_id
    try:
        raw = fetch(
            tcin=args.tcin,
            store_id=args.store_id,
            pricing_store_id=pricing,
            visitor_id=args.visitor_id,
        )
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    c.emit(raw if args.raw else trim(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
