"""Find Target stores near a ZIP or city via nearby_stores_v1.

Doubles as the canonical way to discover store_id values to set in
TARGET_DEFAULT_STORE_ID.
"""

from __future__ import annotations

import argparse
import sys

from . import _common as c


def fetch(*, place: str, limit: int, within: int) -> dict:
    return c.api_get(
        "nearby_stores_v1",
        {"place": place, "limit": limit, "within": within},
    )


def trim(raw: dict) -> dict:
    stores = c.safe_get(raw, "data", "nearby_stores", "stores", default=[]) or []
    out = []
    for s in stores:
        addr = s.get("mailing_address", {}) or {}
        geo = s.get("geographic_specifications", {}) or {}
        out.append(
            {
                "store_id": s.get("store_id"),
                "name": s.get("location_name"),
                "address": addr.get("address_line1"),
                "city": addr.get("city"),
                "state": addr.get("region") or addr.get("state"),
                "zip": addr.get("postal_code"),
                "phone": s.get("main_voice_phone_number"),
                "distance_mi": s.get("distance"),
                "timezone": geo.get("iso_time_zone_code"),
            }
        )
    return {"count": len(out), "stores": out}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="stores", description="Find Target stores near a ZIP or city."
    )
    p.add_argument("place", help="ZIP code or 'City, ST'")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--within", type=int, default=50, help="Miles")
    p.add_argument("--raw", action="store_true")
    args = p.parse_args(argv)

    try:
        raw = fetch(place=args.place, limit=args.limit, within=args.within)
    except Exception as e:  # noqa: BLE001
        c.fail(str(e))

    c.emit(raw if args.raw else trim(raw))
    return 0


if __name__ == "__main__":
    sys.exit(main())
