#!/usr/bin/env python3
"""
WHOOP Data Fetcher
Fetches health data from WHOOP API v1 and exports as JSON or CSV.
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

TOKEN_FILE = Path.home() / ".whoop_tokens.json"
BASE_URL = "https://api.prod.whoop.com/developer/v1"
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"

VALID_TYPES = ["recovery", "sleep", "workout", "cycle", "profile", "body_measurement"]


def load_tokens():
    if not TOKEN_FILE.exists():
        print("ERROR: No tokens found. Run whoop_auth.py first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(TOKEN_FILE.read_text())


def get_access_token(client_id=None, client_secret=None):
    tokens = load_tokens()
    obtained = tokens.get("obtained_at", 0)
    expires_in = tokens.get("expires_in", 3600)
    # Refresh if expiring within 5 minutes
    if int(time.time()) > obtained + expires_in - 300:
        if not client_id or not client_secret:
            client_id = os.environ.get("WHOOP_CLIENT_ID", "")
            client_secret = os.environ.get("WHOOP_CLIENT_SECRET", "")
        if not client_id or not client_secret:
            print("WARNING: Token may be expired. Set WHOOP_CLIENT_ID/WHOOP_CLIENT_SECRET for auto-refresh.", file=sys.stderr)
        else:
            data = urllib.parse.urlencode({
                "grant_type": "refresh_token",
                "refresh_token": tokens["refresh_token"],
                "client_id": client_id,
                "client_secret": client_secret,
            }).encode()
            req = urllib.request.Request(TOKEN_URL, data=data, method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            with urllib.request.urlopen(req) as resp:
                tokens = json.loads(resp.read())
                tokens["obtained_at"] = int(time.time())
                TOKEN_FILE.write_text(json.dumps(tokens, indent=2))
    return tokens["access_token"]


def api_get(path, token, params=None):
    url = f"{BASE_URL}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def paginate(path, token, params=None):
    """Fetch all pages from a paginated WHOOP endpoint."""
    records = []
    next_token = None
    while True:
        p = dict(params or {})
        if next_token:
            p["nextToken"] = next_token
        data = api_get(path, token, p)
        records.extend(data.get("records", []))
        next_token = data.get("next_token")
        if not next_token:
            break
    return records


def fetch_recovery(token, start, end, limit=25):
    params = {"start": start, "end": end, "limit": limit}
    return paginate("/recovery", token, params)


def fetch_sleep(token, start, end, limit=25):
    params = {"start": start, "end": end, "limit": limit}
    return paginate("/activity/sleep", token, params)


def fetch_workout(token, start, end, limit=25):
    params = {"start": start, "end": end, "limit": limit}
    return paginate("/activity/workout", token, params)


def fetch_cycle(token, start, end, limit=25):
    params = {"start": start, "end": end, "limit": limit}
    return paginate("/cycle", token, params)


def fetch_profile(token):
    return api_get("/user/profile/basic", token)


def fetch_body_measurement(token):
    return api_get("/user/measurement/body", token)


def flatten_record(record, prefix=""):
    """Flatten nested dict for CSV export."""
    flat = {}
    for k, v in record.items():
        key = f"{prefix}{k}" if prefix else k
        if isinstance(v, dict):
            flat.update(flatten_record(v, prefix=f"{key}_"))
        else:
            flat[key] = v
    return flat


def write_csv(records, output_path):
    if not records:
        print(f"  No records to write.")
        return
    flat_records = [flatten_record(r) for r in records]
    all_keys = list(dict.fromkeys(k for r in flat_records for k in r.keys()))
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(flat_records)
    print(f"  Saved {len(flat_records)} records → {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Fetch WHOOP health data")
    parser.add_argument("--days", type=int, default=7, help="Number of past days to fetch (default: 7)")
    parser.add_argument("--types", default="recovery,sleep,workout,cycle",
                        help="Comma-separated data types (default: recovery,sleep,workout,cycle)")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    parser.add_argument("--output", default="whoop_data.json",
                        help="Output file (JSON) or directory (CSV)")
    parser.add_argument("--client-id", default=os.environ.get("WHOOP_CLIENT_ID"))
    parser.add_argument("--client-secret", default=os.environ.get("WHOOP_CLIENT_SECRET"))
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    token = get_access_token(args.client_id, args.client_secret)
    types = [t.strip() for t in args.types.split(",")]

    end_dt = datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(days=args.days)
    start = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    end = end_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    print(f"Fetching WHOOP data: {start} → {end}")
    result = {}

    for dtype in types:
        if dtype not in VALID_TYPES:
            print(f"  WARNING: Unknown type '{dtype}', skipping.")
            continue
        print(f"  Fetching {dtype}...")
        try:
            if dtype == "recovery":
                result["recovery"] = fetch_recovery(token, start, end)
            elif dtype == "sleep":
                result["sleep"] = fetch_sleep(token, start, end)
            elif dtype == "workout":
                result["workout"] = fetch_workout(token, start, end)
            elif dtype == "cycle":
                result["cycle"] = fetch_cycle(token, start, end)
            elif dtype == "profile":
                result["profile"] = fetch_profile(token)
            elif dtype == "body_measurement":
                result["body_measurement"] = fetch_body_measurement(token)
            count = len(result[dtype]) if isinstance(result[dtype], list) else 1
            print(f"    → {count} record(s)")
        except Exception as e:
            print(f"    ERROR fetching {dtype}: {e}", file=sys.stderr)

    if args.format == "json":
        indent = 2 if args.pretty else None
        output = json.dumps(result, indent=indent)
        if args.output == "-":
            print(output)
        else:
            Path(args.output).write_text(output)
            print(f"\nData saved → {args.output}")
    elif args.format == "csv":
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        for dtype, records in result.items():
            if isinstance(records, list):
                write_csv(records, out_dir / f"{dtype}.csv")
            else:
                write_csv([records], out_dir / f"{dtype}.csv")
        print(f"\nCSV files saved → {out_dir}/")


if __name__ == "__main__":
    main()
