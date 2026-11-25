"""Audit entry point: connect to the auditee's local database, run the rules,
and write the summary to a target file.

Works under sealed execution as well:
- imports `checks` at the same level (MGC recognizes it)
- creates the output directory itself (MGC does not do that for you)
- writes conclusions and counts only, never raw rows

Usage:
    python run_audit.py --db /path/to/ledger.db --output result.json
Environment fallbacks:
    AUDIT_DB / AUDIT_OUTPUT / AUDIT_SAMPLE
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import checks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local ledger audit")
    parser.add_argument(
        "--db", default=os.environ.get("AUDIT_DB", "sample_ledger.db")
    )
    parser.add_argument(
        "--output", default=os.environ.get("AUDIT_OUTPUT", "audit_result.json")
    )
    parser.add_argument(
        "--sample", type=int, default=int(os.environ.get("AUDIT_SAMPLE", "50"))
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"database not found: {db_path}", file=sys.stderr)
        return 2

    con = sqlite3.connect(db_path)
    try:
        findings = checks.check_schema(con) + checks.check_ledger(con, args.sample)
    finally:
        con.close()

    # Keep rule names and hit counts only: no record ids, amounts, dates, or rows
    buckets: dict[tuple[str, str], int] = {}
    for item in findings:
        key = (item["rule"], item["level"])
        buckets[key] = buckets.get(key, 0) + 1

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": db_path.name,
        "sample_size": args.sample,
        "summary": checks.summarize(findings),
        "rules": [
            {"rule": rule, "level": level, "count": count}
            for (rule, level), count in sorted(buckets.items())
        ],
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(result["summary"], ensure_ascii=False))
    print(f"result written: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
