#!/usr/bin/env python3
"""Win-Loss Analysis

Tallies the themes inside customer feedback for win-loss analysis.

Parameters for this build:
{
  "themes": {
    "price": [
      "too expensive",
      "budget",
      "cheaper",
      "cost",
      "discount"
    ],
    "capability": [
      "missing feature",
      "lacks",
      "does not support",
      "could not",
      "gap in"
    ],
    "timing": [
      "timing",
      "next quarter",
      "not now",
      "later",
      "push"
    ],
    "trust": [
      "reference",
      "risk",
      "concerned",
      "worried",
      "questionable"
    ],
    "no_decision": [
      "no decision",
      "ghosted",
      "unresponsive",
      "stalled",
      "silent"
    ]
  }
}

Usage:
    python3 win-loss_analysis.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Win-Loss Analysis"


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


THEMES = {"price": ["too expensive", "budget", "cheaper", "cost", "discount"], "capability": ["missing feature", "lacks", "does not support", "could not", "gap in"], "timing": ["timing", "next quarter", "not now", "later", "push"], "trust": ["reference", "risk", "concerned", "worried", "questionable"], "no_decision": ["no decision", "ghosted", "unresponsive", "stalled", "silent"]}


def run(input_path, out_dir):
    lines = [line.strip() for line in open(input_path, encoding="utf-8", errors="replace").read().splitlines() if line.strip()]
    counts = {theme: 0 for theme in THEMES}
    samples = {theme: [] for theme in THEMES}
    for line in lines:
        low = line.lower()
        for theme, triggers in THEMES.items():
            if any(trigger.lower() in low for trigger in triggers):
                counts[theme] += 1
                if len(samples[theme]) < 3:
                    samples[theme].append(line[:140])
    report = [f"# {TITLE} theme tally", "", f"source: {input_path}", "", f"lines: {len(lines)}", ""]
    for theme, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        report.append(f"- {theme}: {count}")
        for sample in samples[theme]:
            report.append(f"    - \"{sample}\"")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never put a competitor's confidential information, pricing notes or contract terms into the analysis.", "Never publish the deck outside the company without a legal review.", "Never change a CRM loss reason to make the numbers look better."]:
        report.append(f"- {rule}")
    write_out(out_dir, "theme-tally.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
