#!/usr/bin/env python3
"""Check the shared CH Skills database connection."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from db_core import close_pool, ping

ALPHA_SCHEMA_TABLES = [
    "items",
    "enrichments",
    "stock_daily",
    "stock_daily_basic",
    "stock_index_daily",
    "stock_trade_cal",
    "stock_basic",
    "stock_margin",
    "market_history",
    "reports",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check CH Skills PostgreSQL/SQLite connectivity."
    )
    parser.add_argument(
        "--alpha-schema",
        action="store_true",
        help="Verify all tables from init_alpha_data.sql exist.",
    )
    parser.add_argument(
        "--table",
        action="append",
        default=[],
        help="Require a specific table. Can be passed multiple times.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    required_tables = list(args.table)
    if args.alpha_schema:
        required_tables.extend(ALPHA_SCHEMA_TABLES)

    try:
        result = ping(required_tables=required_tables)
    except Exception as exc:
        error = {"ok": False, "error": str(exc)}
        if args.json:
            print(json.dumps(error, ensure_ascii=False, indent=2))
        else:
            print("[db] FAIL")
            print(f"error: {exc}")
        return 1
    finally:
        close_pool()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        status = "OK" if result["ok"] else "FAIL"
        print(f"[db] {status}")
        for key, value in result["config"].items():
            if value is not None:
                print(f"{key}: {value}")
        server = result.get("server")
        if server:
            print(
                "server: "
                f"db={server['database']} user={server['user']} "
                f"addr={server['server_addr']} port={server['server_port']}"
            )
        if result["tables"]:
            for table, exists in result["tables"].items():
                marker = "ok" if exists else "missing"
                print(f"table {table}: {marker}")
        if result.get("missing_tables"):
            print("missing_tables: " + ", ".join(result["missing_tables"]))

    return 0 if result["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
