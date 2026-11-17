#!/usr/bin/env python3
"""YouTube Video Script Writer

Computes the youtube video script writer number from the values the user supplies.

Parameters for this build:
{
  "formula": "script word budget = minutes * words_per_minute",
  "fields": [
    "minutes",
    "words_per_minute"
  ]
}

Usage:
    python3 youtube_video_script_writer.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "YouTube Video Script Writer"


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


FIELDS = ["minutes", "words_per_minute"]
FORMULA = 'script word budget = minutes * words_per_minute'


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
    for rule in ["Never suggest using music, clips or footage the user has not licensed.", "Never promise a view count, subscriber number or revenue for the video.", "Never paste a competitor's script or transcript into the draft."]:
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
