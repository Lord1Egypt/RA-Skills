#!/usr/bin/env python3
"""Subscription Churn Analysis

Scores accounts against an ICP profile for subscription churn analysis.

Parameters for this build:
{
  "criteria": [
    {
      "name": "low or falling usage",
      "weight": 30
    },
    {
      "name": "payment failure",
      "weight": 25
    },
    {
      "name": "rising ticket count",
      "weight": 20
    },
    {
      "name": "renewal within 60 days",
      "weight": 15
    },
    {
      "name": "tenure under six months",
      "weight": 10
    }
  ]
}

Usage:
    python3 subscription_churn_analysis.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Subscription Churn Analysis"


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


CRITERIA = [{"name": "low or falling usage", "weight": 30}, {"name": "payment failure", "weight": 25}, {"name": "rising ticket count", "weight": 20}, {"name": "renewal within 60 days", "weight": 15}, {"name": "tenure under six months", "weight": 10}]


def run(input_path, out_dir):
    rows = read_csv(input_path)
    report = [f"# {TITLE} scores", "", f"source: {input_path}", ""]
    scored = []
    for row in rows:
        total = 0.0
        for crit in CRITERIA:
            try:
                value = float(str(row.get(crit.get("column", ""), "") or "0").replace(",", ""))
            except ValueError:
                value = 0.0
            total += value * float(crit.get("weight", 1))
        scored.append((total, str(row.get("name") or row.get("company") or row.get("account") or "account"), row))
    scored.sort(key=lambda item: item[0], reverse=True)
    for rank, (total, name, row) in enumerate(scored, 1):
        report.append(f"{rank}. {name} - {total:.2f}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never send cancellation outreach or any email to the customer; the user sends it.", "Never include a customer's personal data in a shared report; use the account ID.", "Never promise a save discount or a refund; the user approves pricing."]:
        report.append(f"- {rule}")
    write_out(out_dir, "scores.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
