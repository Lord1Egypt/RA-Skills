"""Per-store stock and pickup ETA for a TCIN near a ZIP via fiats_v1.

Replaces the deprecated pdp_fulfillment_v1 (HTTP 410 Gone).
"""

from __future__ import annotations

import argparse
import sys

from . import _common as c


def fetch(
    *,
    tcin: str,
    nearby: str,
    radius: int,
    limit: int,
    requested_quantity: int,
    only_available: bool,
    visitor_id: str,
) -> dict:
    params = {
        "tcin": tcin,
        "nearby": nearby,
        "radius": radius,
        "limit": limit,
        "requested_quantity": requested_quantity,
        "channel": "WEB",
        "visitor_id": visitor_id,
    }
    if only_available:
        params["include_only_available_stores"] = "true"
    return c.api_get("fiats_v1", params)


def trim(raw: dict) -> dict:
    ff = c.safe_get(raw, "data", "fulfillment_fiats", default={}) or {}
    locations = ff.get("locations") or []
    stores = []
    for loc in locations:
        store = loc.get("store", {}) or {}
        addr = store.get("mailing_address", {}) or {}
        stores.append(
            {
                "store_id": loc.get("location_id"),
                "name": store.get("location_name"),
                "city": addr.get("city"),
                "state": addr.get("state"),
                "zip": addr.get("postal_code"),
                "distance_mi": loc.get("distance"),
                "available_qty": loc.get("location_available_to_promise_quantity"),
                "pickup": c.safe_get(loc, "order_pickup", "availability_status"),
                "pickup_date": c.safe_get(loc, "order_pickup", "pickup_date"),
                "pickup_eta_min": c.safe_get(loc, "order_pickup", "guest_pick_sla"),
                "in_store": c.safe_get(loc, "in_store_only", "availability_status"),
                "curbside": c.safe_get(loc, "curbside", "availability_status"),
            }
        )
    return {
        "tcin": ff.get("product_id"),
        "stores_checked": len(stores),
        "stores": stores,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="fulfillment",
        description="Per-store stock & pickup ETA for a TCIN near a ZIP.",
    )
    p.add_argument("tcin")
    p.add_argument("--zip", dest="nearby", required=True, help="ZIP code")
    p.add_argument("--radius", type=int, default=50, help="Miles (default 50)")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--qty", dest="requested_quantity", type=int, default=1)
    p.add_argument(
        "--only-available",
        action="store_true",
        help="Filter out stores that have no stock.",
    )
    p.add_argument("--visitor-id", default=c.DEFAULT_VISITOR_ID)
    p.add_argument("--raw", action="store_true")
    args = p.parse_args(argv)

    try:
        raw = fetch(
            tcin=args.tcin,
            nearby=args.nearby,
            radius=args.radius,
            limit=args.limit,
            requested_quantity=args.requested_quantity,
            only_available=args.only_available,
            visitor_id=args.visitor_id,
        )
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    c.emit(raw if args.raw else trim(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
