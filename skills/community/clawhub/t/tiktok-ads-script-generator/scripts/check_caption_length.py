#!/usr/bin/env python3
"""TikTok Ads Script Generator

Measures a draft against the real per-channel limits for tiktok ads script generator.

Parameters for this build:
{
  "limits": {
    "caption": 100,
    "hook_overlay": 40
  }
}

Usage:
    python3 tiktok_ads_script_generator.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "TikTok Ads Script Generator"


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


LIMITS = {"caption": 100, "hook_overlay": 40}


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    body = " ".join(line.strip() for line in text.splitlines() if line.strip())
    words = len(body.split())
    report = [f"# {TITLE} length check", "", f"source: {input_path}", "", f"characters: {len(body)}", f"words: {words}", ""]
    for channel, limit in LIMITS.items():
        state = "OK" if len(body) <= limit else f"OVER by {len(body) - limit}"
        report.append(f"- {channel}: limit {limit} - {state}")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never invent a creator's name, a follower count, a comment or a review.", "Never use a creator's likeness, voice or a trending sound without that creator's written permission on file.", "Never promise a result the product has not been shown to deliver, and never include a health or income claim the team cannot source."]:
        report.append(f"- {rule}")
    write_out(out_dir, "length-check.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
