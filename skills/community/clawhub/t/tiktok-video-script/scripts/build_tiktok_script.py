#!/usr/bin/env python3
"""TikTok Video Script Writer

Turns raw notes into a structured digest for tiktok video script writer.

Parameters for this build:
{
  "sections": [
    "Hook",
    "Beats",
    "On-screen text",
    "Caption",
    "Disclosure flags"
  ]
}

Usage:
    python3 tiktok_video_script_writer.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "TikTok Video Script Writer"


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


SECTIONS = ["Hook", "Beats", "On-screen text", "Caption", "Disclosure flags"]


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
    for rule in ["Never use a commercial sound the user has not licensed for business use.", "Never write a hook that mocks a protected class or targets a sensitive personal attribute.", "Never promise views, engagement rates or sales from a video."]:
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
