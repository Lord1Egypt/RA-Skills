#!/usr/bin/env python3
"""SEO Content Brief Builder

Builds a structured seo-content-brief from a brief and checks every field against its limit.

Parameters for this build:
{
  "fields": [
    "title_tag",
    "meta_description",
    "slug",
    "h2s"
  ],
  "limits": {
    "title_tag": 60,
    "meta_description": 155,
    "slug": 75,
    "h2s": 60
  },
  "output": "seo-content-brief"
}

Usage:
    python3 seo_content_brief_builder.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "SEO Content Brief Builder"


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


FIELDS = ["title_tag", "meta_description", "slug", "h2s"]
LIMITS = {"title_tag": 60, "meta_description": 155, "slug": 75, "h2s": 60}


def run(input_path, out_dir):
    data = read_flat(input_path)
    report = []
    report.append(f"# {TITLE}")
    report.append("")
    report.append(f"source: {input_path}")
    report.append("")
    missing = []
    for field in FIELDS:
        value = data.get(field, "")
        limit = LIMITS.get(field)
        if isinstance(value, list):
            value = "; ".join(str(v) for v in value)
        value = str(value or "")
        if not value:
            missing.append(field)
            report.append(f"- {field}: EMPTY")
        elif limit and len(value) > limit:
            report.append(f"- {field}: {len(value)} chars, limit {limit} - TOO LONG")
        else:
            report.append(f"- {field}: {len(value)} chars" + (f", limit {limit}" if limit else ""))
    report.append("")
    if missing:
        report.append("## Missing from the brief")
        for field in missing:
            report.append(f"- {field}")
    else:
        report.append("## All fields present")
    report.append("")
    report.append("## Guardrails to keep")
    for rule in ["Never write a statistic, a ranking promise or a traffic number into the brief without a named source.", "Never copy the wording of a competing page; the brief has to point at primary sources.", "Never publish the brief or the draft; the writer and the editor publish it."]:
        report.append(f"- {rule}")
    write_out(out_dir, "seo-content-brief.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
