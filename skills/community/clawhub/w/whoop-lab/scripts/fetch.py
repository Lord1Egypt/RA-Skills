#!/usr/bin/env python3
"""
General-purpose WHOOP API fetcher with full pagination support.

Usage:
  python3 fetch.py <endpoint> [--limit N] [--start YYYY-MM-DD] [--end YYYY-MM-DD] [--all]

Examples:
  python3 fetch.py /recovery --limit 1          # latest record
  python3 fetch.py /recovery --days 30          # last 30 days (auto-paginated)
  python3 fetch.py /recovery --all              # entire account history
  python3 fetch.py /activity/sleep --start 2025-01-01 --end 2025-12-31 --all
  python3 fetch.py /activity/workout --days 90
  python3 fetch.py /user/profile/basic          # non-paginated endpoint
"""

import json
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import requests

# config.py lives alongside this script — always resolve so cwd doesn't matter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import config as _cfg

CREDS_PATH = _cfg.creds_path()
BASE_URL = "https://api.prod.whoop.com/developer/v2"
PAGE_SIZE = 25  # WHOOP max per page


def load_creds():
    if not CREDS_PATH.exists():
        print(f"ERROR: {CREDS_PATH} not found. Run auth.py first.", file=sys.stderr)
        sys.exit(1)
    with open(CREDS_PATH) as f:
        return json.load(f)


def maybe_refresh(creds):
    """Auto-refresh if token expires within 60 seconds."""
    if creds.get("expires_at", 0) - time.time() > 60:
        return creds
    print("Token expired, refreshing...", file=sys.stderr)
    import subprocess
    script = Path(__file__).parent / "refresh_token.py"
    subprocess.run([sys.executable, str(script), "--force"], check=True)
    with open(CREDS_PATH) as f:
        return json.load(f)


def _get(endpoint, params, headers):
    """Single HTTP GET, returns parsed JSON."""
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        print("401 Unauthorized — try running refresh_token.py --force", file=sys.stderr)
        sys.exit(1)
    resp.raise_for_status()
    return resp.json()


def fetch_one(endpoint, params=None):
    """Fetch a single page (non-paginated endpoints like /user/profile/basic)."""
    creds = load_creds()
    creds = maybe_refresh(creds)
    headers = {"Authorization": f"Bearer {creds['access_token']}"}
    return _get(endpoint, params or {}, headers)


def fetch_all(endpoint, params=None, max_records=None):
    """
    Fetch all records across pages for collection endpoints.
    Returns a flat list of records.

    - max_records: stop after this many total (None = fetch everything)
    """
    creds = load_creds()
    creds = maybe_refresh(creds)
    headers = {"Authorization": f"Bearer {creds['access_token']}"}

    base_params = dict(params or {})
    base_params["limit"] = PAGE_SIZE

    all_records = []
    next_token = None
    page = 0

    while True:
        page_params = dict(base_params)
        if next_token:
            page_params["nextToken"] = next_token

        page += 1
        print(f"  Fetching page {page}...", file=sys.stderr)

        data = _get(endpoint, page_params, headers)

        # Non-paginated endpoint (e.g. /user/profile/basic) — return as-is
        if "records" not in data:
            return data

        records = data.get("records", [])
        all_records.extend(records)

        next_token = data.get("next_token")

        if max_records and len(all_records) >= max_records:
            all_records = all_records[:max_records]
            break

        if not next_token:
            break

    print(f"  Total records fetched: {len(all_records)}", file=sys.stderr)
    return {"records": all_records, "next_token": None}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="WHOOP API fetcher with pagination")
    parser.add_argument("endpoint", help="API endpoint path, e.g. /recovery")
    parser.add_argument("--limit", type=int, default=None,
                        help="Max records to return (omit for all within date range)")
    parser.add_argument("--days", type=int, default=None,
                        help="Fetch last N days (sets start/end automatically)")
    parser.add_argument("--start", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", help="End date YYYY-MM-DD")
    parser.add_argument("--all", action="store_true",
                        help="Fetch entire account history (ignores --limit)")
    args = parser.parse_args()

    params = {}

    # --days sets start/end automatically
    if args.days:
        end_dt = datetime.now(timezone.utc)
        start_dt = end_dt - timedelta(days=args.days)
        params["start"] = start_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        params["end"] = end_dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if args.start:
        params["start"] = f"{args.start}T00:00:00.000Z"
    if args.end:
        params["end"] = f"{args.end}T23:59:59.000Z"

    # Decide fetch strategy
    if args.all or args.days or (args.start and not args.limit):
        # Paginate through everything
        max_records = None if (args.all or args.days) else args.limit
        data = fetch_all(args.endpoint, params, max_records=max_records)
    elif args.limit:
        # Single page with explicit limit (fast path for --limit 1 etc.)
        params["limit"] = min(args.limit, PAGE_SIZE)
        if args.limit > PAGE_SIZE:
            # Still need pagination
            data = fetch_all(args.endpoint, params, max_records=args.limit)
        else:
            data = fetch_one(args.endpoint, params)
    else:
        # Default: single page, 25 records
        params["limit"] = PAGE_SIZE
        data = fetch_one(args.endpoint, params)

    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
