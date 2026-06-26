#!/usr/bin/env python3
"""
parse_product.py — Parse a Zyte API product extraction response into clean JSON.

Reads a raw Zyte API response file (as saved by fetch_products.py) and extracts
a normalized product data dict. Handles the various edge cases found in real
Zyte API responses: control characters in JSON, brand format variations,
missing/null fields, and mainImage format differences.

Usage:
    python3 parse_product.py <response_file> [<output_file>]

Arguments:
    response_file   Path to raw Zyte API JSON response file
    output_file     Optional path to write parsed JSON (defaults to stdout)

Exit codes:
    0  Success — parsed product JSON written
    1  No product data found in response (.product is null or missing)
    2  Invalid JSON, file not found, or IO error

Dependencies:
    Python 3.8+ standard library only (no pip installs needed).

Why Python instead of jq:
    Zyte API responses frequently contain control characters (form feeds,
    vertical tabs, etc.) inside JSON string values. These cause jq to crash:
        "Invalid string: control characters from U+0000 through U+001F
         must be escaped"
    Python's json.loads(strict=False) handles these gracefully, which is
    why this script exists instead of a jq one-liner.
"""

import json
import sys


def parse_product(raw_json: str) -> dict:
    """Parse a raw Zyte API response string into a normalized product dict.

    Args:
        raw_json: The full JSON response body from the Zyte API as a string.

    Returns:
        A dict with normalized product fields, or None if no product data
        was found in the response.

    The function handles these known edge cases:

    1. Control characters — json.loads(strict=False) permits unescaped
       control chars inside string values.

    2. Brand format — Zyte returns brand as either:
       - A string: "SomeBrand"
       - An object: {"name": "SomeBrand"}
       The isinstance check handles both.

    3. aggregateRating — may be null, missing entirely, or a dict with
       ratingValue/reviewCount/bestRating. The `or {}` guard prevents
       KeyError when the field is null.

    4. mainImage — may be a URL string or an object {"url": "..."}.

    5. description — truncated to 500 chars to keep downstream output
       manageable.
    """
    # strict=False allows control characters inside JSON strings
    data = json.loads(raw_json, strict=False)

    # The product data lives under the "product" key
    product = data.get("product", {})
    if not product:
        return None

    # --- Handle brand format variation ---
    # Brand can be a plain string or an object with a "name" field
    brand = product.get("brand")
    if isinstance(brand, dict):
        brand = brand.get("name")

    # --- Handle aggregateRating safely ---
    # May be null, missing, or a dict; `or {}` covers null case
    agg = product.get("aggregateRating") or {}

    # --- Handle mainImage format variation ---
    # Can be a URL string or {"url": "..."} object
    main_image = product.get("mainImage")
    if isinstance(main_image, dict):
        main_image = main_image.get("url")

    # --- Build normalized output ---
    return {
        "name": product.get("name"),
        "price": product.get("price"),
        "currency": product.get("currency"),
        "currencyRaw": product.get("currencyRaw"),
        "brand": brand,
        "sku": product.get("sku"),
        "availability": product.get("availability"),
        "rating": agg.get("ratingValue"),
        "reviewCount": agg.get("reviewCount"),
        "bestRating": agg.get("bestRating"),
        "description": (product.get("description") or "")[:500],
        "features": product.get("features", []),
        "additionalProperties": product.get("additionalProperties", []),
        "breadcrumbs": [
            b.get("name", "") for b in product.get("breadcrumbs", [])
        ],
        "mainImage": main_image,
        "url": product.get("url"),
        "regularPrice": product.get("regularPrice"),
    }


def main():
    """CLI entry point: read a response file, write parsed JSON."""
    if len(sys.argv) < 2:
        print(
            "Usage: python3 parse_product.py <response_file> [<output_file>]",
            file=sys.stderr,
        )
        sys.exit(2)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    # --- Read the raw response file ---
    try:
        with open(input_path, "rb") as f:
            raw = f.read().decode("utf-8", errors="replace")
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(2)

    # --- Parse the product data ---
    try:
        result = parse_product(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}", file=sys.stderr)
        sys.exit(2)

    if result is None:
        print("No product data found in response", file=sys.stderr)
        sys.exit(1)

    # --- Output the normalized JSON ---
    output = json.dumps(result, indent=2, ensure_ascii=False)

    if output_path:
        with open(output_path, "w") as f:
            f.write(output)
        print(f"Parsed product written to {output_path}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
