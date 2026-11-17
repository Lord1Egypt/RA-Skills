#!/usr/bin/env python3
"""Restaurant Menu Copy Writer

Finds and merges duplicate records for restaurant menu copy writer.

Parameters for this build:
{
  "key_column": "menu_item_name",
  "normalize": "text"
}

Usage:
    python3 restaurant_menu_copy_writer.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Restaurant Menu Copy Writer"


def read_flat(path):
    """Read a small YAML-ish file: `key: value`, `- item` lists, '#' comments."""
    data, key = {}, None
    try:
        raw = open(path, encoding="utf-8", errors="replace").read()
    except OSError as exc:
        raise SystemExit(f"cannot read {path}: {exc}")
    for line in raw.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        stripped = line.strip()
        if stripped.startswith("- "):
            if key is None:
                continue
            data.setdefault(key, [])
            if isinstance(data[key], list):
                data[key].append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ":" in stripped:
            name, _, value = stripped.partition(":")
            name, value = name.strip(), value.strip().strip('"').strip("'")
            if value == "":
                data[name] = []
                key = name
            else:
                data[name] = value
                key = None
    return data


def read_csv(path):
    import csv
    with open(path, newline="", encoding="utf-8", errors="replace") as handle:
        return list(csv.DictReader(handle))


def write_out(out_dir, name, lines):
    import os
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, name)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    print(f"wrote {path}")
    return path


KEY_COLUMN = 'menu_item_name'
NORMALIZE = 'text'


def normalize_value(value):
    text = str(value or "").strip()
    if NORMALIZE == "email":
        return text.lower()
    if NORMALIZE == "domain":
        return text.lower().split("@")[-1].strip()
    if NORMALIZE == "phone":
        return re.sub(r"[^0-9]", "", text)[-10:]
    return re.sub(r"\s+", " ", text).lower()


def run(input_path, out_dir):
    rows = read_csv(input_path)
    seen = {}
    duplicates = []
    unique = []
    for row in rows:
        key = normalize_value(row.get(KEY_COLUMN, ""))
        if key in seen:
            duplicates.append((row, seen[key]))
        else:
            seen[key] = row
            unique.append(row)
    report = [f"# {TITLE} duplicates", "", f"source: {input_path}", "", f"rows: {len(rows)}", f"unique: {len(unique)}", f"duplicates: {len(duplicates)}", ""]
    for row, first in duplicates[:100]:
        report.append(f"- {row.get(KEY_COLUMN, '')} already seen as {first.get(KEY_COLUMN, '')}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never invent a dish, a price, a supplier name, a farm partner or a preparation step.", "Never label a dish allergen-free, gluten-free, organic, sustainable or free range without the kitchen's written confirmation.", "Never post calorie counts for a chain or for a menu until the menu has been checked against the federal menu labeling rule."]:
        report.append(f"- {rule}")
    write_out(out_dir, "duplicates.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
