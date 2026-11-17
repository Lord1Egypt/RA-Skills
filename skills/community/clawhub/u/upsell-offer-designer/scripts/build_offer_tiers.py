#!/usr/bin/env python3
"""Upsell Offer Designer

Builds a tiered price table for upsell offer designer.

Parameters for this build:
{
  "base_cost": 120,
  "markup_pct": 40
}

Usage:
    python3 upsell_offer_designer.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Upsell Offer Designer"


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


BASE_COST = 120
MARKUP = 40


def run(input_path, out_dir):
    data = read_flat(input_path)
    tiers = data.get("tiers") or ["Basic", "Standard", "Premium"]
    if isinstance(tiers, str):
        tiers = [item.strip() for item in tiers.split(",") if item.strip()]
    report = [f"# {TITLE} price tiers", "", f"source: {input_path}", f"base cost: {BASE_COST}", f"markup: x{MARKUP}", ""]
    for index, tier in enumerate(tiers, 1):
        price = BASE_COST * MARKUP * index
        report.append(f"- {tier}: {price:,.2f} USD")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never offer a discount above the approved ladder or a term that finance has not signed off.", "Never use a competitor's pricing in the offer without a documented like-for-like comparison.", "Never promise a renewal discount that has not been approved in writing."]:
        report.append(f"- {rule}")
    write_out(out_dir, "price-tiers.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
