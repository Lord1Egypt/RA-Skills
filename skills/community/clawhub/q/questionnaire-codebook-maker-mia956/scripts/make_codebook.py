#!/usr/bin/env python3
"""Create a questionnaire codebook from a CSV file.

Input CSV columns:
  item_id,item_text,dimension,scale_min,scale_max,reverse

The script outputs:
  - codebook.md
  - variable_map.tsv

It uses only Python's standard library.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, List

REQUIRED_COLUMNS = ["item_id", "item_text", "dimension", "scale_min", "scale_max", "reverse"]


def slugify(value: str, fallback: str = "item") -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    if not text:
        text = fallback
    if not re.match(r"^[a-z]", text):
        text = f"{fallback}_{text}"
    return text[:18]


def normalize_reverse(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "r", "reverse", "reversed", "是", "反向"}


def read_items(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"Missing required column(s): {', '.join(missing)}")
        rows = []
        for i, row in enumerate(reader, 1):
            cleaned = {k: (row.get(k) or "").strip() for k in REQUIRED_COLUMNS}
            if not cleaned["item_id"]:
                cleaned["item_id"] = str(i)
            rows.append(cleaned)
        return rows


def build_variable(row: Dict[str, str], index: int) -> str:
    dim = slugify(row.get("dimension", "scale"), "scale")
    numbers = re.findall(r"\d+", row.get("item_id", ""))
    suffix = numbers[-1] if numbers else str(index)
    return f"{dim[:10]}_{int(suffix):02d}"


def reverse_formula(scale_min: str, scale_max: str) -> str:
    try:
        lo = float(scale_min)
        hi = float(scale_max)
        total = lo + hi
        if total.is_integer():
            total_text = str(int(total))
        else:
            total_text = str(total)
        return f"reversed = {total_text} - original"
    except ValueError:
        return "reversed = min + max - original"


def main() -> int:
    parser = argparse.ArgumentParser(description="Make questionnaire codebook from CSV")
    parser.add_argument("csv_file", help="Input CSV file")
    parser.add_argument("--out-dir", default="output", help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.csv_file)
    if not input_path.exists():
        raise SystemExit(f"File not found: {input_path}")

    rows = read_items(input_path)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    seen_vars = set()
    records = []
    for idx, row in enumerate(rows, 1):
        var = build_variable(row, idx)
        original = var
        counter = 2
        while var in seen_vars:
            var = f"{original}_{counter}"
            counter += 1
        seen_vars.add(var)
        is_reverse = normalize_reverse(row["reverse"])
        response_range = f"{row['scale_min']}–{row['scale_max']}"
        records.append({
            "variable": var,
            "item_id": row["item_id"],
            "dimension": row["dimension"],
            "item_text": row["item_text"],
            "response_range": response_range,
            "reverse_scored": "yes" if is_reverse else "no",
            "scoring_note": reverse_formula(row["scale_min"], row["scale_max"]) if is_reverse else "use original score",
            "missing_rule": "treat blank/NA as missing; compute dimension mean if >=80% valid",
        })

    tsv_path = out_dir / "variable_map.tsv"
    headers = ["variable", "item_id", "dimension", "item_text", "response_range", "reverse_scored", "scoring_note", "missing_rule"]
    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t")
        writer.writeheader()
        writer.writerows(records)

    md_path = out_dir / "codebook.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Questionnaire Codebook\n\n")
        f.write("## Variable map\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
        for rec in records:
            f.write("| " + " | ".join(str(rec[h]).replace("|", "/") for h in headers) + " |\n")
        f.write("\n## Scoring notes\n\n")
        dims = sorted({rec["dimension"] for rec in records})
        for dim in dims:
            dim_vars = [rec["variable"] for rec in records if rec["dimension"] == dim]
            f.write(f"- {dim}: compute the mean or sum of {', '.join(dim_vars)} after reverse scoring.\n")
        f.write("\n## Reverse-scored variables\n\n")
        reverse_records = [rec for rec in records if rec["reverse_scored"] == "yes"]
        if reverse_records:
            for rec in reverse_records:
                f.write(f"- {rec['variable']}: {rec['scoring_note']}\n")
        else:
            f.write("- None marked.\n")

    print(f"Wrote {md_path}")
    print(f"Wrote {tsv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
