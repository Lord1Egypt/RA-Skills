#!/usr/bin/env python3
"""
fetch_products.py — Fetch product data from the Zyte API in parallel.

This script sends concurrent product extraction requests to the Zyte API
for a list of e-commerce URLs. It handles rate limiting, error recovery,
gzip decompression, and writes individual response files for downstream
parsing by parse_product.py.

Usage:
    python3 fetch_products.py <api_key> <url1> <url2> ... [<urlN>]
    echo "url1\\nurl2" | python3 fetch_products.py <api_key> -

Arguments:
    api_key     Your Zyte API key
    url1..urlN  Product page URLs to extract (2–20+ supported)
    -           Read URLs from stdin (one per line)

Output files:
    /tmp/product_1_raw.json, /tmp/product_2_raw.json, ...
    Each file contains the raw Zyte API JSON response for one URL.

Stdout:
    JSON summary with per-URL status, timings, and output file paths.

Stderr:
    Progress messages showing each URL as it completes.

Exit codes:
    0  All URLs fetched successfully
    1  Some URLs failed (partial success — check summary for details)
    2  All URLs failed, or invalid input (no URLs provided, etc.)

Dependencies:
    Python 3.8+ standard library only (no pip installs needed).
    Uses: urllib.request, concurrent.futures, gzip, json, base64

Rate limit behavior:
    The Zyte API uses requests-per-minute (RPM) limits, not concurrency
    limits. The default is 1,400 RPM. This script caps parallel workers
    at 5 as a conservative default — not because Zyte requires it, but
    to avoid overwhelming a single target domain. For 2–20 URLs this is
    well within the RPM budget. If HTTP 429 is received, the script
    retries with exponential backoff (2s → 4s → 8s) up to 3 times.
"""

import json
import gzip
import sys
import time
import urllib.request
import urllib.error
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Maximum number of concurrent API requests. Zyte allows unlimited
# concurrency (RPM-based limits), but we cap at 5 to be conservative
# with target domain load and response time predictability.
MAX_CONCURRENT = 5

# Retry configuration for HTTP 429 (rate limited) and network errors.
# Uses exponential backoff: 2s, 4s, 8s between retries.
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # seconds; doubles each retry

# Per-request timeout. Zyte product extraction uses browser rendering
# which can take 10-60s depending on the target site.
REQUEST_TIMEOUT = 120  # seconds


# ---------------------------------------------------------------------------
# Core fetch logic
# ---------------------------------------------------------------------------

def fetch_one(api_key: str, url: str, index: int) -> dict:
    """Fetch product data for a single URL from the Zyte API.

    Sends a POST request with {"url": "<url>", "product": true} and saves
    the response to /tmp/product_<index>_raw.json.

    The payload is intentionally minimal — just url + product: true. The
    Zyte API's product extraction uses browser-based AI rendering by
    default, which is the most reliable mode for e-commerce sites.

    Args:
        api_key: Zyte API key for authentication.
        url: The product page URL to extract.
        index: 1-based index used for output filename and summary ordering.

    Returns:
        A dict with: index, url, status, http_code, file_path, error, elapsed.
        Status is one of: "ok", "no_product_data", "auth_error",
        "payload_error", "http_error", "network_error".
    """
    output_path = f"/tmp/product_{index}_raw.json"

    # Build HTTP Basic Auth header (Zyte uses api_key as username, empty password)
    auth_string = base64.b64encode(f"{api_key}:".encode()).decode()

    # The extraction payload — kept minimal on purpose.
    # "product": true triggers Zyte's AI product extraction pipeline.
    payload = json.dumps({"url": url, "product": True}).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_string}",
        # Request gzip compression to reduce bandwidth. We handle
        # decompression manually below because urllib doesn't auto-
        # decompress when Accept-Encoding is set explicitly.
        "Accept-Encoding": "gzip, deflate",
    }

    req = urllib.request.Request(
        "https://api.zyte.com/v1/extract",
        data=payload,
        headers=headers,
        method="POST",
    )

    last_error = None
    start = time.time()

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                raw_bytes = resp.read()

                # Decompress gzip if the server sent compressed data.
                # We check for the gzip magic number (0x1f 0x8b) because
                # urllib.request does NOT auto-decompress when we set the
                # Accept-Encoding header manually.
                if raw_bytes[:2] == b"\x1f\x8b":
                    raw_bytes = gzip.decompress(raw_bytes)

                body = raw_bytes.decode("utf-8", errors="replace")

            # Write the raw response to disk for parse_product.py
            with open(output_path, "w") as f:
                f.write(body)

            elapsed = round(time.time() - start, 1)

            # Quick sanity check: does the response contain product data?
            # Full parsing is done by parse_product.py — this is just a
            # fast pass/fail check so the summary is accurate.
            try:
                data = json.loads(body, strict=False)
                has_product = bool(data.get("product"))
            except json.JSONDecodeError:
                has_product = False

            return {
                "index": index,
                "url": url,
                "status": "ok" if has_product else "no_product_data",
                "http_code": 200,
                "file_path": output_path,
                "error": None if has_product else "Response contained no .product field",
                "elapsed": elapsed,
            }

        except urllib.error.HTTPError as e:
            # Read the error response body for diagnostic info
            last_error = e
            error_body = ""
            try:
                error_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass

            if e.code == 429 and attempt < MAX_RETRIES:
                # Rate limited — back off and retry.
                # Zyte recommends exponential backoff for 429 responses.
                # You are NOT charged for 429 responses.
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                time.sleep(backoff)
                continue

            elif e.code == 401:
                # Bad API key — no point retrying
                return _error_result(index, url, start, "auth_error", 401,
                                     "Invalid API key (HTTP 401)")

            elif e.code == 422:
                # Unprocessable request — usually means conflicting payload
                # fields (e.g. combining incompatible extraction options)
                return _error_result(index, url, start, "payload_error", 422,
                                     f"Unprocessable request (HTTP 422): {error_body[:200]}")

            else:
                # Other HTTP errors (520, 521, 5xx, etc.)
                return _error_result(index, url, start, "http_error", e.code,
                                     f"HTTP {e.code}: {error_body[:200]}")

        except (urllib.error.URLError, TimeoutError, OSError) as e:
            # Network-level errors (DNS failure, timeout, connection refused)
            last_error = e
            if attempt < MAX_RETRIES:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                time.sleep(backoff)
                continue

    # All retries exhausted
    return _error_result(index, url, start, "network_error", None,
                         f"Failed after {MAX_RETRIES + 1} attempts: {last_error}")


def _error_result(index, url, start, status, http_code, error):
    """Build a standardized error result dict."""
    return {
        "index": index,
        "url": url,
        "status": status,
        "http_code": http_code,
        "file_path": None,
        "error": error,
        "elapsed": round(time.time() - start, 1),
    }


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python3 fetch_products.py <api_key> <url1> [url2] ... [urlN]\n"
            "       echo 'url1\\nurl2' | python3 fetch_products.py <api_key> -",
            file=sys.stderr,
        )
        sys.exit(2)

    api_key = sys.argv[1]

    # Collect URLs from command-line args or stdin
    if sys.argv[2] == "-":
        urls = [line.strip() for line in sys.stdin if line.strip()]
    else:
        urls = [u for u in sys.argv[2:] if u.strip()]

    if not urls:
        print("Error: No URLs provided", file=sys.stderr)
        sys.exit(2)

    # ---------- Validate URLs ----------
    valid = []      # (index, url) tuples for valid URLs
    results = []    # collect results for invalid URLs immediately

    for i, url in enumerate(urls, 1):
        if url.startswith("http://") or url.startswith("https://"):
            valid.append((i, url))
        else:
            results.append({
                "index": i,
                "url": url,
                "status": "invalid_url",
                "http_code": None,
                "file_path": None,
                "error": "URL must start with http:// or https://",
                "elapsed": 0,
            })

    if not valid:
        # Every URL was invalid
        summary = {"total": len(urls), "success": 0, "failed": len(urls), "results": results}
        print(json.dumps(summary, indent=2))
        sys.exit(2)

    # ---------- Fetch in parallel ----------
    # Worker count = min(valid URLs, MAX_CONCURRENT)
    workers = min(len(valid), MAX_CONCURRENT)
    total_start = time.time()

    print(f"Fetching {len(valid)} URLs with {workers} parallel workers...",
          file=sys.stderr)

    with ThreadPoolExecutor(max_workers=workers) as pool:
        # Submit all fetch tasks
        futures = {
            pool.submit(fetch_one, api_key, url, idx): (idx, url)
            for idx, url in valid
        }

        # Collect results as they complete (order may differ from input)
        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            # Print progress to stderr
            marker = "✓" if result["status"] == "ok" else "✗"
            print(
                f"  {marker} [{result['index']}/{len(urls)}] "
                f"{result['url'][:60]}... "
                f"({result['elapsed']}s)",
                file=sys.stderr,
            )

    total_elapsed = round(time.time() - total_start, 1)

    # ---------- Build summary ----------
    # Sort results by index so output order matches input order
    results.sort(key=lambda r: r["index"])

    success_count = sum(1 for r in results if r["status"] == "ok")
    failed_count = len(results) - success_count

    summary = {
        "total": len(urls),
        "success": success_count,
        "failed": failed_count,
        "total_elapsed": total_elapsed,
        "parallel_workers": workers,
        "results": results,
    }

    # Print summary to stdout (machine-readable JSON)
    print(json.dumps(summary, indent=2))

    # Exit code signals overall success/failure
    if success_count == 0:
        sys.exit(2)
    elif failed_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
