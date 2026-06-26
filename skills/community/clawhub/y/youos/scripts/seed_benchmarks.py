"""Seed benchmark_cases table from fixtures/benchmark_cases.yaml."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parents[1]


def load_cases(fixtures_path: Path) -> list[dict]:
    return yaml.safe_load(fixtures_path.read_text(encoding="utf-8")) or []


def seed_benchmarks(
    cases: list[dict],
    db_path: Path,
) -> dict[str, int]:
    schema_sql = (ROOT_DIR / "docs" / "schema.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(schema_sql)
        inserted = 0
        updated = 0
        for case in cases:
            expected = json.dumps(case.get("expected_properties", {}))
            cur = conn.execute(
                "SELECT id FROM benchmark_cases WHERE case_key = ?",
                (case["case_key"],),
            )
            if cur.fetchone():
                conn.execute(
                    """
                    UPDATE benchmark_cases
                    SET category = ?, prompt_text = ?, expected_properties_json = ?,
                        reference_reply = ?, notes = ?
                    WHERE case_key = ?
                    """,
                    (
                        case["category"],
                        case["prompt_text"].strip(),
                        expected,
                        case.get("reference_reply"),
                        case.get("notes"),
                        case["case_key"],
                    ),
                )
                updated += 1
            else:
                conn.execute(
                    """
                    INSERT INTO benchmark_cases
                        (case_key, category, prompt_text, expected_properties_json, reference_reply, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        case["case_key"],
                        case["category"],
                        case["prompt_text"].strip(),
                        expected,
                        case.get("reference_reply"),
                        case.get("notes"),
                    ),
                )
                inserted += 1
        conn.commit()
    finally:
        conn.close()
    return {"inserted": inserted, "updated": updated, "total": len(cases)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed benchmark cases into DB")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=None,
        help="Path to SQLite database (default: the active instance from YOUOS_DATA_DIR)",
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=ROOT_DIR / "fixtures" / "benchmark_cases.yaml",
        help="Path to benchmark cases YAML (falls back to configs/benchmarks/golden.yaml)",
    )
    args = parser.parse_args()

    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    db_path = args.db_path or resolve_sqlite_path(get_settings().database_url)

    if args.fixtures.exists():
        cases = load_cases(args.fixtures)
        result = seed_benchmarks(cases, db_path)
        print(f"Benchmark seeder complete: {result['total']} cases processed")
        print(f"  Inserted: {result['inserted']}")
        print(f"  Updated:  {result['updated']}")
    else:
        # No fixture file — seed from the canonical golden.yaml that eval and
        # autoresearch share, so this never fails on a missing fixture.
        import sqlite3

        from app.evaluation.service import seed_benchmark_cases_from_golden

        conn = sqlite3.connect(db_path)
        try:
            n = seed_benchmark_cases_from_golden(conn)
        finally:
            conn.close()
        print(f"Benchmark seeder complete: seeded {n} cases from golden.yaml into {db_path}")


if __name__ == "__main__":
    main()
