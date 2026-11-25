# -*- coding: utf-8 -*-
"""Parameterised cross-check for reconstructed tables (standard library only).

Checks
  row_checks      one expression per row (sum or product of columns) vs a target column
  column_checks   data rows summed per column vs the value printed in the total row
  decimal_checks  decimal-place consistency inside a column
  jump_checks     magnitude jumps between neighbouring rows (column band errors)
  sequence_check  key sequence continuity (gaps, duplicates, reversals)
  required        cells that must never be empty (row anchors)

Usage
  python verify_table.py rows.csv --spec checks.json --report verify.json
  python verify_table.py rows.csv                 # no spec -> structural checks only

Exit codes
  0  every check passed
  1  at least one check open or failed
  2  input or spec error

The spec is JSON. Every key is optional:

  {
    "tolerance": 0.005,
    "label_cols": ["name"],
    "total_labels": ["TOTAL", "合计"],
    "required": ["id", "name"],
    "row_checks":    [{"target": "amount", "parts": ["qty", "price"], "op": "product"}],
    "column_checks": [{"col": "amount"}],
    "decimal_checks":[{"col": "price", "places": 2}],
    "jump_checks":   [{"col": "amount", "factor": 10}],
    "sequence_check":{"col": "id", "allow_gaps": true}
  }
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys

NUM_RE = re.compile(r"-?\d+(?:[.,]\d+)?")
FULLWIDTH = str.maketrans("０１２３４５６７８９．－，％", "0123456789.-,%")
MAX_ITEMS = 50

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        pass


def norm(text) -> str:
    return (text or "").translate(FULLWIDTH).replace("\u00a0", " ").strip()


def to_number(text):
    """Return float or None. Handles 1,234.50 / (12.00) / 12.00- / full-width digits."""
    raw = norm(text)
    if not raw:
        return None
    negative = False
    if raw.startswith("(") and raw.endswith(")"):
        negative, raw = True, raw[1:-1]
    if raw.endswith("-"):
        negative, raw = True, raw[:-1]
    match = NUM_RE.search(raw)
    if not match:
        return None
    try:
        value = float(match.group().replace(",", ""))
    except ValueError:
        return None
    return -value if negative else value


def decimals(text) -> int:
    match = re.search(r"\.(\d+)", norm(text).replace(",", ""))
    return len(match.group(1)) if match else 0


def make(check, target, expected, actual, tol, level=None, note="", failures=None,
         checked=0):
    diff = None
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        diff = round(actual - expected, 10)
    if level is None:
        level = "pass" if diff is not None and abs(diff) <= tol else "open"
    return {
        "check": check, "target": target, "expected": expected, "actual": actual,
        "diff": diff, "tolerance": tol, "level": level, "note": note,
        "checked": checked, "failures": failures or [],
    }


def is_total_row(row, labels, label_cols):
    for col in label_cols:
        cell = norm(row.get(col, ""))
        if cell and any(cell.startswith(lab) or cell == lab for lab in labels):
            return True
    for key, value in row.items():
        if key and any(norm(value) == lab for lab in labels):
            return True
    return False


def resolve_op(op, values):
    if op == "product":
        out = 1.0
        for value in values:
            out *= value
        return out
    return sum(values)


def check_rows(rows, spec):
    results = []
    tol = float(spec.get("tolerance", 0.005))
    for rule in spec.get("row_checks", []):
        target, parts = rule.get("target"), rule.get("parts", [])
        op = rule.get("op", "sum")
        label = rule.get("label") or f"{target} = {op}({', '.join(parts)})"
        failures, checked = [], 0
        for index, row in enumerate(rows, start=2):
            got = to_number(row.get(target))
            values = [to_number(row.get(part)) for part in parts]
            if got is None or any(value is None for value in values):
                continue
            checked += 1
            expect = resolve_op(op, values)
            if abs(got - expect) > tol:
                failures.append({
                    "line": index, "cell": target, "actual": got,
                    "expected": round(expect, 6), "diff": round(got - expect, 6),
                })
        results.append(make(label, target, checked, checked - len(failures), tol,
                            level="pass" if not failures and checked else "open",
                            note=(f"{len(failures)} row(s) failed" if failures else ("" if checked else "no numeric row matched the rule")),
                            failures=failures[:MAX_ITEMS], checked=checked))
    return results


def check_columns(rows, spec, data_rows, total_rows):
    results = []
    tol = float(spec.get("tolerance", 0.005))
    for rule in spec.get("column_checks", []):
        col = rule.get("col")
        label = rule.get("label") or f"column total: {col}"
        printed = None
        for row in total_rows:
            printed = to_number(row.get(col))
            if printed is not None:
                break
        values = [to_number(row.get(col)) for row in data_rows]
        values = [value for value in values if value is not None]
        actual = round(sum(values), 10) if values else None
        if printed is None:
            results.append(make(label, col, None, actual, tol, level="open",
                                note="no total row value found for this column",
                                checked=len(values)))
            continue
        results.append(make(label, col, printed, actual, tol, checked=len(values)))
    return results


def check_decimals(rows, spec):
    results = []
    for rule in spec.get("decimal_checks", []):
        col, places = rule.get("col"), int(rule.get("places", 2))
        failures, seen = [], []
        for index, row in enumerate(rows, start=2):
            raw = norm(row.get(col))
            if not raw or to_number(raw) is None:
                continue
            got = decimals(raw)
            seen.append(got)
            if got != places:
                failures.append({"line": index, "cell": col, "raw": raw,
                                 "decimals": got, "expected": places})
        dominant = max(set(seen), key=seen.count) if seen else None
        results.append(make(f"decimals: {col} == {places}", col, places, dominant, 0,
                            level="pass" if not failures else "open",
                            note=f"{len(failures)} of {len(seen)} values differ",
                            failures=failures[:MAX_ITEMS], checked=len(seen)))
    return results


def check_jumps(rows, spec):
    results = []
    for rule in spec.get("jump_checks", []):
        col, factor = rule.get("col"), float(rule.get("factor", 10))
        failures, previous = [], None
        for index, row in enumerate(rows, start=2):
            value = to_number(row.get(col))
            if value is None or value == 0:
                continue
            if previous is not None:
                low, high = sorted((abs(previous), abs(value)))
                if low > 0 and high / low > factor:
                    failures.append({"line": index, "cell": col, "prev": previous,
                                     "value": value, "ratio": round(high / low, 3)})
            previous = value
        results.append(make(f"magnitude jump < x{factor:g}: {col}", col, 0, len(failures), 0,
                            level="pass" if not failures else "open",
                            note=f"{len(failures)} jump(s) exceed the factor",
                            failures=failures[:MAX_ITEMS]))
    return results


def check_sequence(rows, spec):
    rule = spec.get("sequence_check") or {}
    col = rule.get("col")
    if not col:
        return []
    allow_gaps = bool(rule.get("allow_gaps", True))
    keys, failures, gaps = [], [], []
    for index, row in enumerate(rows, start=2):
        raw = norm(row.get(col))
        if not raw:
            continue
        try:
            value = int(float(NUM_RE.search(raw).group()))
            keys.append((index, value))
        except (AttributeError, ValueError):
            continue
    for (line_a, a), (line_b, b) in zip(keys, keys[1:]):
        if b == a:
            failures.append({"line": line_b, "value": b, "issue": "duplicate"})
        elif b < a:
            failures.append({"line": line_b, "value": b, "issue": "descending"})
        elif b > a + 1:
            gaps.append({"line": line_b, "from": a, "to": b, "missing": b - a - 1})
    level = "pass"
    note = f"{len(gaps)} gap(s)"
    if failures:
        level = "open"
    elif gaps and not allow_gaps:
        level = "open"
        note += " (gaps not allowed by spec)"
    return [make(f"sequence: {col}", col, len(keys), len(keys) - len(failures), 0, level=level, note=note,
                 failures=(failures + gaps)[:MAX_ITEMS], checked=len(keys))]


def check_required(rows, spec):
    cols = spec.get("required") or []
    if not cols:
        return []
    failures = []
    for index, row in enumerate(rows, start=2):
        for col in cols:
            if not norm(row.get(col)):
                failures.append({"line": index, "cell": col, "issue": "empty anchor"})
    return [make("required cells", ", ".join(cols), len(rows), len(rows) - len(failures), 0,
                 level="pass" if not failures else "open",
                 note=f"{len(failures)} empty required cell(s)",
                 failures=failures[:MAX_ITEMS], checked=len(rows))]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Cross-check a reconstructed table.")
    parser.add_argument("csv_path")
    parser.add_argument("--spec", help="JSON file with check rules")
    parser.add_argument("--report", help="write the full JSON report here")
    parser.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args(argv)

    try:
        with open(args.csv_path, "r", encoding=args.encoding, newline="") as handle:
            reader = csv.DictReader(handle)
            rows = [row for row in reader]
            fields = reader.fieldnames or []
    except OSError as exc:
        print(f"cannot read {args.csv_path}: {exc}", file=sys.stderr)
        return 2

    if not fields:
        print("input has no header row", file=sys.stderr)
        return 2

    spec = {}
    if args.spec:
        try:
            with open(args.spec, "r", encoding="utf-8-sig") as handle:
                spec = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"cannot read spec: {exc}", file=sys.stderr)
            return 2

    spec.setdefault("label_cols", fields[:2])
    spec.setdefault("total_labels", ["合计", "总计", "小计", "TOTAL"])

    flags = [is_total_row(row, spec["total_labels"], spec["label_cols"]) for row in rows]
    total_rows = [row for row, flag in zip(rows, flags) if flag]
    data_rows = [row for row, flag in zip(rows, flags) if not flag]

    results = []
    results += check_required(data_rows, spec)
    results += check_rows(data_rows, spec)
    results += check_columns(rows, spec, data_rows, total_rows)
    results += check_decimals(data_rows, spec)
    results += check_jumps(data_rows, spec)
    results += check_sequence(data_rows, spec)

    summary = {
        "file": args.csv_path,
        "columns": len(fields),
        "data_rows": len(data_rows),
        "total_rows": len(total_rows),
        "pass": sum(1 for item in results if item["level"] == "pass"),
        "explained": sum(1 for item in results if item["level"] == "explained"),
        "open": sum(1 for item in results if item["level"] == "open"),
        "fail": sum(1 for item in results if item["level"] == "fail"),
    }
    report = {"summary": summary, "checks": results}

    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"{args.csv_path}: {summary['data_rows']} data rows, "
          f"{summary['total_rows']} total row(s), {len(fields)} columns")
    for item in results:
        flag = item["level"].upper()
        print(f"  [{flag}] {item['check']}  expected={item['expected']} "
              f"actual={item['actual']} diff={item['diff']}")
    bad = summary["open"] + summary["fail"]
    print(f"result: {summary['pass']} pass, {bad} open/fail")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
