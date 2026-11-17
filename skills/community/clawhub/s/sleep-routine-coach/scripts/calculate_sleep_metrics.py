#!/usr/bin/env python3
"""Deterministically calculate non-diagnostic sleep metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sleep_core import (
    SleepRoutineError,
    default_data_dir,
    find_record,
    load_records,
    print_json,
    public_record,
    recalculate_record,
    validate_date,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--date")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--include-audit", action="store_true")
    args = parser.parse_args()
    try:
        if args.input:
            value = json.loads(args.input.read_text(encoding="utf-8"))
            records = value if isinstance(value, list) else [value]
        else:
            records = load_records(args.data_dir)
        if args.date:
            selected = find_record(records, validate_date(args.date))
            if selected is None:
                raise SleepRoutineError(f"No record for {args.date}")
            records = [selected]
        calculated = [public_record(recalculate_record(dict(record)), args.include_audit) for record in records]
        print_json(calculated[0] if args.date or (args.input and len(calculated) == 1) else calculated)
        return 0
    except (SleepRoutineError, json.JSONDecodeError, OSError) as exc:
        parser.error(str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

