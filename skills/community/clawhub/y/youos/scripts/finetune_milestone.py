#!/usr/bin/env python3
"""Fine-tune milestone helper: readiness check + optional full run."""

from __future__ import annotations

import argparse
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]


def _count_quality_pairs(db_path: Path) -> int:
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute(
            """
            SELECT COUNT(*)
            FROM feedback_pairs
            WHERE COALESCE(rating, 0) >= 4
              AND COALESCE(edit_distance_pct, 1.0) <= 0.25
              AND LENGTH(COALESCE(edited_reply, '')) >= 15
            """
        ).fetchone()
        return int(row[0] if row else 0)
    finally:
        conn.close()


def main() -> None:
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    parser = argparse.ArgumentParser(description="Fine-tune milestone readiness and run helper")
    parser.add_argument("--db", default=str(resolve_sqlite_path(get_settings().database_url)), help="Path to SQLite DB")
    parser.add_argument("--threshold", type=int, default=30, help="Minimum quality feedback pairs")
    parser.add_argument("--run", action="store_true", help="Run export + finetune + pre/post eval when threshold met")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        raise SystemExit(1)

    quality_pairs = _count_quality_pairs(db_path)
    print(f"Quality feedback pairs: {quality_pairs} (threshold: {args.threshold})")

    if quality_pairs < args.threshold:
        print("Milestone not reached. Keep reviewing feedback before fine-tuning.")
        raise SystemExit(2)

    print("Milestone reached ✅")

    if not args.run:
        return

    cmds = [
        [sys.executable, str(ROOT_DIR / "scripts" / "run_eval.py"), "--summary-only", "--tag", "pre-milestone"],
        [sys.executable, str(ROOT_DIR / "scripts" / "export_feedback_jsonl.py")],
        [sys.executable, str(ROOT_DIR / "scripts" / "finetune_lora.py")],
        [sys.executable, str(ROOT_DIR / "scripts" / "run_eval.py"), "--summary-only", "--tag", "post-milestone"],
    ]

    for cmd in cmds:
        print("\n$ " + " ".join(cmd))
        result = subprocess.run(cmd, cwd=str(ROOT_DIR))
        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
