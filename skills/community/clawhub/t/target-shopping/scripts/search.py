"""Search Target by keyword or category via plp_search_v2."""

from __future__ import annotations

import argparse
import sys
import urllib.parse

from . import _common as c


def fetch(
    *,
    keyword: str | None,
    category: str | None,
    count: int,
    offset: int,
    store_id: str,
    pricing_store_id: str,
    visitor_id: str,
) -> dict:
    if not keyword and not category:
        raise ValueError("at least one of --keyword or --category is required")

    if keyword and category:
        page = f"/c/-/N-{category}?searchTerm={urllib.parse.quote(keyword)}"
    elif keyword:
        page = f"/s/{urllib.parse.quote(keyword)}"
    else:
        page = f"/c/-/N-{category}"
    params = {
        "channel": "WEB",
        "count": count,
        "offset": offset,
        "page": page,
        "platform": "desktop",
        "pricing_store_id": pricing_store_id,
        "store_id": store_id,
        "visitor_id": visitor_id,
        "default_purchasability_filter": "true",
        "include_sponsored": "true",
        "new_search": "true",
        "spellcheck": "true",
    }
    if keyword:
        params["keyword"] = keyword
    if category:
        params["category"] = category
    return c.api_get("plp_search_v2", params)


def trim(raw: dict, *, query_label: str) -> dict:
    sr = c.safe_get(raw, "data", "search", "search_response", default={})
    products = c.safe_get(raw, "data", "search", "products", default=[]) or []
    meta = sr.get("metadata", {}) or {}

    results = []
    for p in products:
        item = p.get("item", {}) or {}
        enr = item.get("enrichment", {}) or {}
        results.append(
            {
                "tcin": p.get("tcin"),
                "title": c.safe_get(item, "product_description", "title"),
                "brand": c.safe_get(item, "primary_brand", "name"),
                "price": c.safe_get(p, "price", "formatted_current_price"),
                "reg_price": c.safe_get(p, "price", "reg_retail"),
                "save_percent": c.safe_get(p, "price", "save_percent"),
                "rating": c.safe_get(
                    p, "ratings_and_reviews", "statistics", "rating", "average"
                ),
                "review_count": c.safe_get(
                    p, "ratings_and_reviews", "statistics", "rating", "count"
                ),
                "buy_url": enr.get("buy_url"),
                "image": c.safe_get(enr, "image_info", "primary_image", "url"),
            }
        )

    return {
        "query": query_label,
        "total_results": meta.get("total_results"),
        "current_page": meta.get("current_page"),
        "total_pages": meta.get("total_pages"),
        "count_returned": len(results),
        "results": results,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="search",
        description=(
            "Search Target.com via plp_search_v2. Accepts a keyword, a "
            "category N-id, or both (to search within a category — useful "
            "for fresh-grocery searches that get drowned by shelf-stable "
            "hits in catalog-wide keyword search). See "
            "references/categories.md for common N-ids."
        ),
    )
    p.add_argument("keyword", nargs="?", help="Free-text keyword search")
    p.add_argument(
        "--category",
        help=(
            "Target category N-id (e.g. '5xteg' for headphones, '5xt6n' "
            "for meat & seafood). Combine with a keyword to scope."
        ),
    )
    p.add_argument("--count", type=int, default=10, help="Results per page (≤24)")
    p.add_argument("--offset", type=int, default=0)
    p.add_argument("--store-id", default=c.get_default_store())
    p.add_argument("--pricing-store-id", default=None,
                   help="Defaults to --store-id")
    p.add_argument("--visitor-id", default=c.DEFAULT_VISITOR_ID)
    p.add_argument("--raw", action="store_true",
                   help="Emit full raw response instead of trimmed view")
    args = p.parse_args(argv)

    pricing = args.pricing_store_id or args.store_id

    try:
        raw = fetch(
            keyword=args.keyword,
            category=args.category,
            count=args.count,
            offset=args.offset,
            store_id=args.store_id,
            pricing_store_id=pricing,
            visitor_id=args.visitor_id,
        )
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    label = args.keyword or f"category:{args.category}"
    c.emit(raw if args.raw else trim(raw, query_label=label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
