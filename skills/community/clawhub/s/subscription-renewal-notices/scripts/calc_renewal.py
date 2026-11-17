#!/usr/bin/env python3
"""Subscription Renewal Notices

Computes the subscription renewal notices number from the values the user supplies.

Parameters for this build:
{
  "formula": "renewal_total_usd = new_price_usd * term_months + (days_elapsed / term_days) * new_price_usd, then apply discount_pct",
  "fields": [
    "current_price_usd",
    "new_price_usd",
    "term_months",
    "days_elapsed",
    "term_days",
    "discount_pct"
  ]
}

Usage:
    python3 subscription_renewal_notices.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Subscription Renewal Notices"


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


FIELDS = ["current_price_usd", "new_price_usd", "term_months", "days_elapsed", "term_days", "discount_pct"]
FORMULA = 'renewal_total_usd = new_price_usd * term_months + (days_elapsed / term_days) * new_price_usd, then apply discount_pct'


def run(input_path, out_dir):
    data = read_flat(input_path)
    values = {}
    for field in FIELDS:
        raw = str(data.get(field, "") or "0").replace(",", "").replace("$", "").replace("%", "")
        try:
            values[field] = float(raw)
        except ValueError:
            values[field] = 0.0
    report = [f"# {TITLE}", "", f"source: {input_path}", ""]
    for field, value in values.items():
        report.append(f"- {field}: {value:g}")
    report.append("")
    report.append(f"formula: {FORMULA or 'documented in the skill'}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never send the notice; the billing system and a person deliver it.", "Never state a renewal amount or a price change that the billing system does not show.", "Never replace the cancellation path with a retention offer only."]:
        report.append(f"- {rule}")
    write_out(out_dir, "calculation.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
