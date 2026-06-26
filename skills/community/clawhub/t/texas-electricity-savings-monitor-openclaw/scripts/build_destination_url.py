#!/usr/bin/env python3
"""Build a Personalized Energy destination URL for a confirmed Texas service address."""

from __future__ import annotations

import argparse
import json
import re
from urllib.parse import quote, urlencode


BASE_URL = "https://www.personalized.energy/electricity-rates/texas"
TRACKING_QUERY = {"source": "skills"}


def normalize_city(city: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", city.strip().lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    if not cleaned:
        raise ValueError("city is required")
    return cleaned


def normalize_street(street: str, unit: str) -> str:
    street = street.strip()
    unit = unit.strip()
    if not street:
        raise ValueError("street is required")
    full_street = f"{street} {unit}".strip() if unit else street
    return quote(full_street, safe="")


def normalize_zipcode(zipcode: str) -> str:
    zipcode = zipcode.strip()
    if not re.fullmatch(r"\d{5}", zipcode):
        raise ValueError("zipcode must be a 5-digit ZIP code")
    return zipcode


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a Personalized Energy destination URL from a confirmed Texas address.",
    )
    parser.add_argument("--street", required=True)
    parser.add_argument("--unit", default="")
    parser.add_argument("--city", required=True)
    parser.add_argument("--zipcode", required=True)
    args = parser.parse_args()

    city_slug = normalize_city(args.city)
    street_slug = normalize_street(args.street, args.unit)
    zipcode = normalize_zipcode(args.zipcode)

    result = {
        "city_slug": city_slug,
        "zipcode": zipcode,
        "urlencoded_street": street_slug,
        "personalized_energy_url": (
            f"{BASE_URL}/{city_slug}/{zipcode}/{street_slug}"
            f"?{urlencode(TRACKING_QUERY)}"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
