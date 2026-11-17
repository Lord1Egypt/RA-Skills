#!/usr/bin/env python3
"""Reddit Ads Copywriter

Turns raw notes into a structured digest for reddit ads copywriter.

Parameters for this build:
{
  "sections": [
    "subreddits",
    "audience",
    "community_rules",
    "tone",
    "hooks",
    "claims"
  ]
}

Usage:
    python3 reddit_ads_copywriter.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Reddit Ads Copywriter"


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


SECTIONS = ["subreddits", "audience", "community_rules", "tone", "hooks", "claims"]


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    blocks = []
    current = None
    for line in text.splitlines():
        if line.startswith("#"):
            current = line.lstrip("#").strip()
            blocks.append((current, []))
        elif blocks:
            blocks[-1][1].append(line.rstrip())
    report = [f"# {TITLE} digest", "", f"source: {input_path}", ""]
    for section in SECTIONS:
        report.append(f"## {section}")
        found = False
        for name, body in blocks:
            if section.lower() in name.lower():
                found = True
                for line in body:
                    if line.strip():
                        report.append(f"- {line.strip()}")
        if not found:
            report.append(f"- (no notes for {section})")
        report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never pretend to be a community member, post as a user or use a throwaway account to seed an ad.", "Never reuse a subreddit's name in a way that suggests the community endorsed the product.", "Never quote a comment or a user without the user's permission in writing."]:
        report.append(f"- {rule}")
    write_out(out_dir, "digest.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
