#!/usr/bin/env python3
"""Convert a CSV table into region-id -> value JSON for recolor_choropleth.py."""
import argparse
import csv
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("out_json")
    ap.add_argument("--id-col", required=True)
    ap.add_argument("--value-col", required=True)
    ap.add_argument("--numeric", action="store_true")
    args = ap.parse_args()

    out = {}
    with Path(args.csv_path).open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = (row.get(args.id_col) or "").strip()
            raw = (row.get(args.value_col) or "").strip()
            if not rid or raw == "":
                continue
            out[rid] = float(raw.replace(",", "")) if args.numeric else raw

    Path(args.out_json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.out_json} ({len(out)} rows)")


if __name__ == "__main__":
    main()
