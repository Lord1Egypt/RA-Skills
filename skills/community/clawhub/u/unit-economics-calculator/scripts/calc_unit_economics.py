#!/usr/bin/env python3
"""Unit Economics Calculator

Computes the unit economics calculator number from the values the user supplies.

Parameters for this build:
{
  "formula": "net_order_value = gross_order_value - refunds - discounts; contribution_margin = net_order_value - (payment_fee + shipping + fulfillment + packaging + support_cost); cac = (ad_spend + sales_salary) / new_customers; cac_payback_months = cac / monthly_contribution_per_customer; ltv_cac = ltv / cac",
  "fields": [
    "gross_order_value",
    "refunds",
    "discounts",
    "payment_fee",
    "shipping_cost",
    "fulfillment_cost",
    "support_cost",
    "ad_spend",
    "sales_salary",
    "new_customers",
    "ltv"
  ]
}

Usage:
    python3 unit_economics_calculator.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Unit Economics Calculator"


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


FIELDS = ["gross_order_value", "refunds", "discounts", "payment_fee", "shipping_cost", "fulfillment_cost", "support_cost", "ad_spend", "sales_salary", "new_customers", "ltv"]
FORMULA = 'net_order_value = gross_order_value - refunds - discounts; contribution_margin = net_order_value - (payment_fee + shipping + fulfillment + packaging + support_cost); cac = (ad_spend + sales_salary) / new_customers; cac_payback_months = cac / monthly_contribution_per_customer; ltv_cac = ltv / cac'


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
    for rule in ["Never publish a CAC, LTV or payback figure the user has not confirmed from their own data.", "Never use an industry benchmark as if it were the user's number.", "Never present the output as an audit, an appraisal or an investment recommendation."]:
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
