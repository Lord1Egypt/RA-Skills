# -*- coding: utf-8 -*-
"""Merge multi-page continuation tables (standard library only).

Handles the three seams that break naive concatenation:
  repeated header on page 2..N   -> removed
  footer / page-number rows      -> removed by regex
  row repeated across a seam     -> de-duplicated by key
and reports row accounting plus key-sequence continuity.

Usage
  python merge_continuation.py p1.csv p2.csv p3.csv --out merged.csv --report merge.json
  python merge_continuation.py p*.csv --key id --strict-gaps

Exit codes
  0  merged, no continuity problem
  1  merged, but duplicate / descending / (strict) gap in the key sequence
  2  input error
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import re
import sys

DEFAULT_FOOTER = r"续|接下页|下页|转下页|第\s*\d+\s*页|共\s*\d+\s*页|page\s*\d+"
PAD = ""

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        pass


def norm(text) -> str:
    return re.sub(r"\s+", "", (text or "")).strip()


def row_key(row, header):
    return "|".join(norm(row.get(col, "")) for col in header)


def header_similarity(left, right) -> float:
    return difflib.SequenceMatcher(None, norm(left), norm(right)).ratio()


def read_page(path, encoding):
    with open(path, "r", encoding=encoding, newline="") as handle:
        reader = csv.reader(handle)
        rows = [row for row in reader]
    if not rows:
        raise ValueError("empty file")
    header = [cell.strip() for cell in rows[0]]
    body = []
    for raw in rows[1:]:
        if not any(norm(cell) for cell in raw):
            continue
        if len(raw) < len(header):
            raw = raw + [PAD] * (len(header) - len(raw))
        body.append(dict(zip(header, raw)))
    return header, body


def numeric_key(value):
    match = re.search(r"-?\d+", norm(value))
    if not match:
        return None
    try:
        return int(match.group())
    except ValueError:
        return None


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Merge continuation-table pages.")
    parser.add_argument("inputs", nargs="+", help="page CSV files, in page order")
    parser.add_argument("--out", required=True, help="merged CSV path")
    parser.add_argument("--report", help="write the JSON report here")
    parser.add_argument("--key", help="key column for seam de-duplication")
    parser.add_argument("--header-similarity", type=float, default=0.8)
    parser.add_argument("--footer-regex", default=DEFAULT_FOOTER)
    parser.add_argument("--strict-gaps", action="store_true",
                        help="treat key-sequence gaps as an error")
    parser.add_argument("--encoding", default="utf-8-sig")
    args = parser.parse_args(argv)

    try:
        footer = re.compile(args.footer_regex)
    except re.error as exc:
        print(f"bad --footer-regex: {exc}", file=sys.stderr)
        return 2

    try:
        pages = [(path, *read_page(path, args.encoding)) for path in args.inputs]
    except (OSError, ValueError, csv.Error) as exc:
        print(f"cannot read input page: {exc}", file=sys.stderr)
        return 2

    canonical = pages[0][1]
    key = args.key or (canonical[0] if canonical else None)
    merged, dropped, per_page = [], [], []

    for path, header, body in pages:
        kept, removed_header, removed_footer, removed_seam = [], 0, 0, 0
        header_sig = "|".join(norm(cell) for cell in header)
        for row in body:
            text = " ".join(norm(value) for value in row.values())
            if footer.search(text):
                removed_footer += 1
                dropped.append({"page": path, "reason": "footer", "row": list(row.values())})
                continue
            if header_similarity(row_key(row, header), header_sig) >= args.header_similarity:
                removed_header += 1
                dropped.append({"page": path, "reason": "repeated header",
                                "row": list(row.values())})
                continue
            if merged and key and row.get(key) and merged[-1].get(key):
                if norm(row.get(key)) == norm(merged[-1].get(key)):
                    removed_seam += 1
                    dropped.append({"page": path, "reason": "seam duplicate",
                                    "row": list(row.values()), "key": key})
                    continue
            kept.append(row)
        merged.extend(kept)
        per_page.append({
            "page": path, "rows_read": len(body), "rows_kept": len(kept),
            "removed_header": removed_header, "removed_footer": removed_footer,
            "removed_seam": removed_seam,
        })

    keys, sequence_issues, gaps = [], [], []
    if key:
        for index, row in enumerate(merged, start=2):
            value = numeric_key(row.get(key, ""))
            if value is not None:
                keys.append((index, value))
    for (line_a, a), (line_b, b) in zip(keys, keys[1:]):
        if b == a:
            sequence_issues.append({"line": line_b, "value": b, "issue": "duplicate"})
        elif b < a:
            sequence_issues.append({"line": line_b, "value": b, "issue": "descending"})
        elif b > a + 1:
            gaps.append({"line": line_b, "from": a, "to": b, "missing": b - a - 1})

    try:
        with open(args.out, "w", encoding=args.encoding, newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=canonical, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(merged)
    except OSError as exc:
        print(f"cannot write {args.out}: {exc}", file=sys.stderr)
        return 2

    rows_read = sum(item["rows_read"] for item in per_page)
    removed = sum(item["removed_header"] + item["removed_footer"] + item["removed_seam"]
                  for item in per_page)
    summary = {
        "pages": len(pages),
        "output": args.out,
        "rows_read": rows_read,
        "rows_out": len(merged),
        "rows_removed": removed,
        "accounting_ok": rows_read - removed == len(merged),
        "key": key,
        "gaps": len(gaps),
        "sequence_issues": len(sequence_issues),
    }
    report = {"summary": summary, "per_page": per_page,
              "sequence": sequence_issues + gaps, "dropped": dropped}

    if args.report:
        with open(args.report, "w", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)

    print(f"{len(pages)} page(s): {rows_read} rows read, {removed} removed, "
          f"{len(merged)} rows written -> {args.out}")
    for item in per_page:
        print(f"  {item['page']}: read={item['rows_read']} kept={item['rows_kept']} "
              f"header={item['removed_header']} footer={item['removed_footer']} "
              f"seam={item['removed_seam']}")
    print(f"accounting: {rows_read} - {removed} = {len(merged)} "
          f"({'ok' if summary['accounting_ok'] else 'MISMATCH'})")
    print(f"key {key!r}: {len(gaps)} gap(s), {len(sequence_issues)} issue(s)")

    if sequence_issues or (gaps and args.strict_gaps):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
