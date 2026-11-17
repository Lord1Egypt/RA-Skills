#!/usr/bin/env python3
"""Search bundled safety footwear product data.

This script is intentionally local-only: it reads data/products.json and prints
JSON. It does not use the network, environment variables, or external services.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "data" / "products.json"


def tokenize(value: str) -> set[str]:
    return {
        token.strip().lower()
        for token in value.replace("/", " ").replace("-", " ").replace(",", " ").split()
        if token.strip()
    }


def product_text(product: dict) -> str:
    parts = [
        product.get("name", ""),
        product.get("type", ""),
        product.get("buyer_fit", ""),
        " ".join(product.get("materials", [])),
        " ".join(product.get("applications", [])),
        " ".join(product.get("certification_keywords", [])),
        " ".join(product.get("oem_options", [])),
    ]
    return " ".join(parts).lower()


def score_product(query_tokens: set[str], product: dict) -> int:
    text = product_text(product)
    score = sum(2 for token in query_tokens if token in text)
    if product.get("type", "").lower() in " ".join(query_tokens):
        score += 3
    return score


def main() -> int:
    parser = argparse.ArgumentParser(description="Search static B2B safety footwear product data.")
    parser.add_argument("--query", required=True, help="Buyer need, product, material, application, or certification keywords.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum number of matches to return.")
    args = parser.parse_args()

    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    query_tokens = tokenize(args.query)
    scored = [
        (score_product(query_tokens, product), product)
        for product in products
    ]
    matches = [
        product
        for score, product in sorted(scored, key=lambda item: item[0], reverse=True)
        if score > 0
    ][: max(args.limit, 1)]

    if not matches:
        matches = products[: max(args.limit, 1)]

    print(json.dumps({
        "ok": True,
        "query": args.query,
        "matches": matches,
        "note": "Results use bundled static product data. Verify certifications, MOQ, and lead time with the supplier before ordering."
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
