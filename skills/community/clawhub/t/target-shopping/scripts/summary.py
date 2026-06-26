"""Get a lightweight summary + fulfillment for multiple TCINs at once.

Uses product_summary_with_fulfillment_v1 — much cheaper than calling
pdp_client_v1 N times for shortlists, carts, or recommendations.
"""

from __future__ import annotations

import argparse
import sys

from . import _common as c


def fetch(
    *,
    tcins: list[str],
    store_id: str,
    pricing_store_id: str,
    zip_code: str | None,
    state: str | None,
    latitude: str | None,
    longitude: str | None,
) -> dict:
    params = {
        "tcins": ",".join(tcins),
        "store_id": store_id,
        "pricing_store_id": pricing_store_id,
        "has_pricing_store_id": "true",
        "channel": "WEB",
        "zip": zip_code,
        "state": state,
        "latitude": latitude,
        "longitude": longitude,
    }
    return c.api_get("product_summary_with_fulfillment_v1", params)


def trim(raw: dict) -> dict:
    summaries = c.safe_get(raw, "data", "product_summaries", default=[]) or []
    out = []
    for s in summaries:
        item = s.get("item", {}) or {}
        pd = item.get("product_description", {}) or {}
        enr = item.get("enrichment", {}) or {}
        ff = s.get("fulfillment", {}) or {}
        store_opts = ff.get("store_options") or []
        primary_store = store_opts[0] if store_opts else {}
        services = c.safe_get(ff, "shipping_options", "services", default=[]) or []
        std_ship = next(
            (
                sv
                for sv in services
                if sv.get("shipping_method_id") == "STANDARD"
            ),
            services[0] if services else {},
        )
        out.append(
            {
                "tcin": s.get("tcin"),
                "title": pd.get("title"),
                "buy_url": enr.get("buy_url"),
                "sold_out": ff.get("sold_out"),
                "shipping_status": c.safe_get(
                    ff, "shipping_options", "availability_status"
                ),
                "shipping_eta": std_ship.get("min_delivery_date"),
                "primary_store_id": primary_store.get("location_id"),
                "primary_store_name": c.safe_get(primary_store, "store", "location_name"),
                "primary_store_pickup": c.safe_get(
                    primary_store, "order_pickup", "availability_status"
                ),
                "primary_store_qty": primary_store.get(
                    "location_available_to_promise_quantity"
                ),
            }
        )
    return {"count": len(out), "items": out}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="summary",
        description=(
            "Get summary + fulfillment for multiple TCINs in a single call."
        ),
    )
    p.add_argument(
        "tcins",
        nargs="+",
        help="One or more TCINs (space-separated).",
    )
    p.add_argument("--store-id", default=c.get_default_store())
    p.add_argument("--pricing-store-id", default=None)
    p.add_argument("--zip", dest="zip_code", default=None)
    p.add_argument("--state", default=None)
    p.add_argument("--latitude", default=None)
    p.add_argument("--longitude", default=None)
    p.add_argument("--raw", action="store_true")
    args = p.parse_args(argv)

    pricing = args.pricing_store_id or args.store_id
    try:
        raw = fetch(
            tcins=args.tcins,
            store_id=args.store_id,
            pricing_store_id=pricing,
            zip_code=args.zip_code,
            state=args.state,
            latitude=args.latitude,
            longitude=args.longitude,
        )
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    c.emit(raw if args.raw else trim(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
