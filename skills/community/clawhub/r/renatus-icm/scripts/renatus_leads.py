#!/usr/bin/env python3
"""
renatus_leads.py

Export leads from the Renatus ICM Supabase project into workspace CSV/JSON files.

Usage:
  # Export all leads to workspace/renatus_leads.csv and .json
  python3 scripts/renatus_leads.py --export

  # Dry run (show data without saving)
  python3 scripts/renatus_leads.py --dry-run

  # Export a specific number
  python3 scripts/renatus_leads.py --export --limit 200

  # Convert existing workspace JSON to CSV
  python3 scripts/renatus_leads.py --convert-json

Requirements:
  - SUPABASE_URL and LEAD_ADMIN_TOKEN environment variables (or --ref/--token flags)
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from config_loader import load_config
    _cfg = load_config()
except Exception:
    _cfg = {}

DEFAULT_WORKSPACE = Path("/home/umbrel/.openclaw/workspace")
DEFAULT_CSV = DEFAULT_WORKSPACE / "renatus_leads.csv"
DEFAULT_JSON = DEFAULT_WORKSPACE / "renatus_leads.json"


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Export and manage Renatus leads from Supabase.")
    ap.add_argument("--export", action="store_true", help="Export leads from Supabase to CSV/JSON")
    ap.add_argument("--convert-json", action="store_true", help="Convert renatus_leads.json to renatus_leads.csv")
    ap.add_argument("--dry-run", action="store_true", help="Show data without saving files")
    ap.add_argument("--limit", type=int, default=500, help="Max leads to export (default: 500)")
    supabase_url_cfg = _cfg.get("supabase_url", "") if isinstance(_cfg, dict) else ""
    supabase_ref_cfg = _cfg.get("supabase_ref", "") if isinstance(_cfg, dict) else ""
    ap.add_argument("--ref", default=os.environ.get("SUPABASE_URL", supabase_ref_cfg or "").replace("https://", "").replace(".supabase.co", ""),
                    help="Supabase project ref (default: from config.json or env)")
    lead_token_cfg = _cfg.get("lead_token", "") if isinstance(_cfg, dict) else ""
    ap.add_argument("--token", default=os.environ.get("LEAD_ADMIN_TOKEN", lead_token_cfg),
                    help="Lead admin token (default: from config.json or env)")
    ap.add_argument("--output-dir", type=Path, default=DEFAULT_WORKSPACE,
                    help="Output directory for CSV/JSON files")
    ap.add_argument("--format", choices=["csv", "json", "both"], default="both",
                    help="Output format (default: both)")
    return ap.parse_args()


def fetch_leads(ref: str, token: str, limit: int) -> list[dict]:
    """Fetch leads from lead-admin-export edge function."""
    url = f"https://{ref}.supabase.co/functions/v1/lead-admin-export?limit={limit}"
    req = urllib.request.Request(url, headers={
        "x-admin-token": token,
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"HTTP {e.code}: {body}. Check SUPABASE_URL / RENATUS_SUPABASE_REF and LEAD_ADMIN_TOKEN / RENATUS_LEAD_TOKEN.") from e

    if not data.get("ok"):
        raise RuntimeError(f"API error: {data.get('error', 'unknown')}")

    rows = data.get("rows", [])
    print(f"Fetched {len(rows)} leads from Supabase")
    return rows


def rows_to_csv(rows: list[dict], path: Path) -> None:
    """Write leads to CSV."""
    if not rows:
        print("No rows to write")
        return

    # Flatten top-level fields + phone from metadata
    fieldnames = ["name", "email", "phone", "company", "notes", "cta_type", "source_page", "created_at"]
    meta_fields = set()
    for row in rows:
        meta = row.get("metadata") or {}
        meta_fields.update(meta.keys())

    all_fields = fieldnames + sorted(meta_fields)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            meta = row.get("metadata") or {}
            flat = {k: v for k, v in row.items() if k != "metadata"}
            flat["phone"] = meta.get("phone", "")
            flat["event_id"] = meta.get("event_id", "")
            flat["registration_id"] = meta.get("registration_id", "")
            flat["lead_id"] = meta.get("lead_id", "")
            flat["guest_user_id"] = meta.get("guest_user_id", "")
            flat["registered_sessions"] = "; ".join(meta.get("registered_sessions", [])) if meta.get("registered_sessions") else ""
            for k, v in meta.items():
                if k not in flat:
                    flat[k] = v
            writer.writerow(flat)

    print(f"Written: {path} ({path.stat().st_size:,} bytes)")


def rows_to_json(rows: list[dict], path: Path) -> None:
    """Write leads to JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "exported_at": datetime.utcnow().isoformat() + "Z",
            "total": len(rows),
            "rows": rows,
        }, f, indent=2, default=str)
    print(f"Written: {path} ({path.stat().st_size:,} bytes)")


def convert_json_to_csv(json_path: Path, csv_path: Path) -> None:
    """Convert existing renatus_leads.json to CSV."""
    with open(json_path) as f:
        data = json.load(f)

    rows = data if isinstance(data, list) else data.get("rows", [])
    if not rows:
        print("No rows found in JSON file")
        return
    rows_to_csv(rows, csv_path)


def show_sample(rows: list[dict], n: int = 5) -> None:
    """Print a sample of leads."""
    for row in rows[:n]:
        phone = (row.get("metadata") or {}).get("phone", "")
        sessions = (row.get("metadata") or {}).get("registered_sessions", [])
        print(f"  {row.get('name', '?')} <{row.get('email', '?')}> | {phone} | {row.get('created_at', '')}")
        if sessions:
            print(f"    sessions: {', '.join(sessions)}")
    if len(rows) > n:
        print(f"  ... and {len(rows) - n} more")


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # --convert-json
    if args.convert_json:
        json_path = args.output_dir / "renatus_leads.json"
        if not json_path.exists():
            print(f"File not found: {json_path}", file=sys.stderr)
            return 1
        csv_path = args.output_dir / "renatus_leads.csv"
        print(f"Converting {json_path} → {csv_path}")
        convert_json_to_csv(json_path, csv_path)
        return 0

    # --export
    if args.export:
        if not args.ref or not args.token:
            print("ERROR: Missing --ref or --token. Set in config.json or set RENATUS_SUPABASE_REF / RENATUS_LEAD_TOKEN env vars.", file=sys.stderr)
            print("  Set SUPABASE_URL and LEAD_ADMIN_TOKEN env vars, or pass --ref and --token.", file=sys.stderr)
            return 1

        print(f"Fetching up to {args.limit} leads from {args.ref}.supabase.co...")
        try:
            rows = fetch_leads(args.ref, args.token, args.limit)
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1

        if args.dry_run:
            print("\nSample (first 5):")
            show_sample(rows)
            return 0

        if args.format in ("csv", "both"):
            csv_path = args.output_dir / "renatus_leads.csv"
            rows_to_csv(rows, csv_path)

        if args.format in ("json", "both"):
            json_path = args.output_dir / "renatus_leads.json"
            rows_to_json(rows, json_path)

        print(f"\nTotal leads exported: {len(rows)}")
        print(f"Files: {args.output_dir / 'renatus_leads.csv'} + .json")
        return 0

    # Default: show status of workspace leads files
    csv_path = args.output_dir / "renatus_leads.csv"
    json_path = args.output_dir / "renatus_leads.json"

    if csv_path.exists():
        with open(csv_path) as f:
            count = sum(1 for _ in f) - 1
        print(f"CSV: {csv_path} ({count:,} leads, {csv_path.stat().st_size:,} bytes)")
    else:
        print(f"CSV: not found (run with --export)")

    if json_path.exists():
        with open(json_path) as f:
            data = json.load(f)
        total = len(data) if isinstance(data, list) else data.get("total", "?")
        print(f"JSON: {json_path} ({total:,} leads, {json_path.stat().st_size:,} bytes)")
    else:
        print(f"JSON: not found (run with --export)")

    print("\nUsage:")
    print("  --export       Export from Supabase to CSV/JSON")
    print("  --convert-json Convert renatus_leads.json to CSV")
    print("  --dry-run      Preview without saving")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
