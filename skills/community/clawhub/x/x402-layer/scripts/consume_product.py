#!/usr/bin/env python3
"""
consume_product.py - Purchase and optionally download digital products from x402 Singularity Layer.

Products are sold at https://api.x402layer.cc/p/<slug> with a standard x402 402 challenge.
Pays with USDC on Base or Solana (X402_PREFER_NETWORK picks when both are offered), speaking
x402 v2 when the 402 carries a PAYMENT-REQUIRED header and v1 otherwise (X402_WIRE=v1 forces v1).

Usage:
    python consume_product.py <product-slug-or-url> [--download]

Examples:
    python consume_product.py my-product-slug
    python consume_product.py https://studio.x402layer.cc/pay/my-product-slug
    python consume_product.py https://api.x402layer.cc/p/my-product-slug --download

Credentials (explicit environment only, never a .env file):
    Base:   PRIVATE_KEY + WALLET_ADDRESS, or AWAL mode
    Solana: SOLANA_SECRET_KEY

Safer defaults:
- accepts only platform-hosted product URLs
- downloads only from trusted storage hosts
- after a payment is sent, a timeout / 202 / 5xx is reported as pending: never pay again for it
"""

import argparse
import json
import os
import re
from typing import Any, Dict, Optional
from urllib.parse import quote, urlparse

import requests

import x402_wire
from awal_bridge import awal_pay_url
from network_selection import pick_payment_option
from solana_signing import create_solana_payment_header, load_solana_wallet_address
from wallet_signing import is_awal_mode

API_BASE = "https://api.x402layer.cc"
TRUSTED_PRODUCT_HOSTS = {
    "api.x402layer.cc",
    "studio.x402layer.cc",
}
TRUSTED_DOWNLOAD_SUFFIXES = (
    ".supabase.co",
    ".supabase.in",
    ".supabase.net",
)
_SLUG_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


def _product_url(slug: str) -> str:
    slug = slug.strip().strip("/")
    if not _SLUG_RE.match(slug):
        raise ValueError(f"Not a valid product slug: {slug!r}")
    return f"{API_BASE}/p/{quote(slug, safe='')}"


def resolve_product_url(product_input: str) -> str:
    """Slug, Studio pay link, or API product link -> https://api.x402layer.cc/p/<slug>."""
    if not product_input.startswith("http"):
        return _product_url(product_input)

    parsed = urlparse(product_input)
    if parsed.scheme != "https" or parsed.netloc not in TRUSTED_PRODUCT_HOSTS:
        raise ValueError("Product URL must be an https link on api.x402layer.cc or studio.x402layer.cc")
    path = parsed.path
    if parsed.netloc == "studio.x402layer.cc" and path.startswith("/pay/"):
        return _product_url(path[len("/pay/"):])
    if parsed.netloc == "api.x402layer.cc" and path.startswith("/p/"):
        return _product_url(path[len("/p/"):])
    if parsed.netloc == "api.x402layer.cc" and path.startswith("/storage/product/"):
        # Legacy link format: the product route accepts the product id too.
        return _product_url(path[len("/storage/product/"):])
    raise ValueError("Unknown product URL format (expected /pay/<slug> or /p/<slug>)")


def _is_trusted_download_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        return False
    host = parsed.netloc.lower()
    if host in TRUSTED_PRODUCT_HOSTS:
        return True
    return any(host.endswith(suffix) for suffix in TRUSTED_DOWNLOAD_SUFFIXES)


def _request_product(url: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
    merged_headers = {"Accept": "application/json"}
    if headers:
        merged_headers.update(headers)
    return requests.get(url, headers=merged_headers, timeout=45)


def _download_url(result: Dict[str, Any]) -> Optional[str]:
    return result.get("download_url") or result.get("downloadUrl")


def _download_file(result: Dict[str, Any]) -> None:
    download_url = _download_url(result)
    if not download_url:
        print("No download URL returned")
        return
    if not _is_trusted_download_url(download_url):
        raise ValueError("Refusing to download from a non-trusted host")

    raw_filename = result.get("file_name") or result.get("fileName") or "downloaded_product"
    filename = os.path.basename(str(raw_filename))
    if not filename or filename in {".", ".."}:
        filename = "downloaded_product"

    print(f"\nDownloading file to: {filename}")
    file_response = requests.get(download_url, timeout=60)
    if file_response.status_code != 200:
        raise ValueError(f"Download failed: {file_response.status_code}")

    with open(filename, "wb") as handle:
        handle.write(file_response.content)
    print(f"Downloaded: {filename} ({len(file_response.content)} bytes)")


def _pay_with_local_keys(api_url: str) -> Dict[str, Any]:
    response = _request_product(api_url)
    if response.status_code == 200:
        return response.json()
    if response.status_code != 402:
        raise ValueError(f"Unexpected response: {response.status_code} - {response.text[:500]}")

    # v2 PAYMENT-REQUIRED header first, v1 JSON body otherwise (x402_wire).
    challenge = x402_wire.read_challenge(response)
    network, option, signer = pick_payment_option(challenge, context="product purchase")
    amount = int(option["maxAmountRequired"])

    print("Payment required:")
    print(f"  Network:   {network}")
    print(f"  Amount:    {amount} atomic units ({amount / 1_000_000:.6f} USDC)")
    print(f"  Recipient: {option.get('payTo')}")

    if network == "base":
        if signer is None:
            raise ValueError("Internal error: missing Base signer")
        header_name, payment = signer.create_payment_header(challenge, option)
        wallet = signer.wallet
    else:
        header_name, payment = create_solana_payment_header(challenge, option)
        wallet = load_solana_wallet_address() or ""

    print("\nSubmitting payment and requesting the product...")
    headers = {header_name: payment}
    if wallet:
        headers["x-wallet-address"] = wallet
    # From here the payment is SENT. A timeout, 202 or 5xx is pending, never a reason to pay again.
    try:
        paid = _request_product(api_url, headers=headers)
    except requests.RequestException as exc:
        return x402_wire.pending_result(None, exc)
    if x402_wire.is_ambiguous_status(paid.status_code):
        return x402_wire.pending_result(paid.status_code, paid.text)
    if paid.status_code != 200:
        raise ValueError(f"Payment failed: {paid.status_code} - {paid.text[:500]}")

    settlement = x402_wire.read_payment_response(paid)
    if settlement and settlement.get("transaction"):
        print(f"Settled: {settlement.get('transaction')} on {settlement.get('network')}")
    return paid.json()


def consume_product(product_input: str, download_file: bool = False) -> Dict[str, Any]:
    print(f"Resolving product: {product_input}")
    api_url = resolve_product_url(product_input)
    print(f"API URL: {api_url}")

    if is_awal_mode():
        print("Using AWAL to authorize the product purchase")
        result = awal_pay_url(api_url, method="GET", headers={"Accept": "application/json"})
        if result.get("error"):
            raise ValueError(result["error"])
    else:
        result = _pay_with_local_keys(api_url)

    if result.get("pending"):
        print("\nPayment sent but not confirmed yet. Do NOT pay again.")
        return result

    print("\nProduct purchased successfully")
    print(f"Download URL: {_download_url(result) or 'N/A'}")
    print(f"File Name: {result.get('file_name') or result.get('fileName') or 'N/A'}")

    if download_file:
        _download_file(result)

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Purchase a product from x402 Singularity Layer")
    parser.add_argument("product", help="Product slug, Studio pay link, or api.x402layer.cc/p/<slug> link")
    parser.add_argument("--download", action="store_true", help="Download the returned file after purchase")
    args = parser.parse_args()

    try:
        result = consume_product(args.product, download_file=args.download)
        print("\nResult:")
        print(json.dumps(result, indent=2))
        return 2 if result.get("pending") else 0
    except Exception as exc:
        print(f"\nError: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
