#!/usr/bin/env python3
"""SMS Campaign Compliance

Flags US compliance risks in a draft for sms campaign compliance.

Parameters for this build:
{
  "rules": [
    {
      "label": "Prize or guaranteed-win claim",
      "pattern": "(?i)\\b(guaranteed|you have won|you won|winner|cash prize|claim your prize)\\b"
    },
    {
      "label": "Health, debt or approval outcome claim",
      "pattern": "(?i)\\b(cure|cures|treats your|eliminates debt|guaranteed approval|loan approval|double your money)\\b"
    },
    {
      "label": "Automated or prerecorded voice disclosure",
      "pattern": "(?i)\\b(this is an automated|recorded message|press 1 to)\\b"
    },
    {
      "label": "Short code sender without identification",
      "pattern": "(?i)\\bshort code\\b"
    },
    {
      "label": "Urgency or scarcity wording to review",
      "pattern": "(?i)\\b(act now|last chance|today only|expires in|limited time)\\b"
    }
  ]
}

Usage:
    python3 sms_campaign_compliance.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "SMS Campaign Compliance"


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


RULES = [{"label": "Prize or guaranteed-win claim", "pattern": "(?i)\\b(guaranteed|you have won|you won|winner|cash prize|claim your prize)\\b"}, {"label": "Health, debt or approval outcome claim", "pattern": "(?i)\\b(cure|cures|treats your|eliminates debt|guaranteed approval|loan approval|double your money)\\b"}, {"label": "Automated or prerecorded voice disclosure", "pattern": "(?i)\\b(this is an automated|recorded message|press 1 to)\\b"}, {"label": "Short code sender without identification", "pattern": "(?i)\\bshort code\\b"}, {"label": "Urgency or scarcity wording to review", "pattern": "(?i)\\b(act now|last chance|today only|expires in|limited time)\\b"}]


def run(input_path, out_dir):
    text = open(input_path, encoding="utf-8", errors="replace").read()
    lines = text.splitlines()
    report = [f"# {TITLE} compliance check", "", f"source: {input_path}", ""]
    hits = []
    for number, line in enumerate(lines, 1):
        low = line.lower()
        for rule in RULES:
            pattern = str(rule.get("pattern", "")).lower()
            if pattern and pattern in low:
                hits.append((number, rule.get("label", pattern), line.strip()[:120]))
    if hits:
        report.append("## Flags")
        for number, label, snippet in hits:
            report.append(f"- line {number} - {label}: {snippet}")
    else:
        report.append("## No flags")
    report.append("")
    report.append("A flag is a prompt for a human, not a verdict. Fix the wording, then re-run.")
    report.append("")
    report.append("## Guardrails to keep")
    for rule_text in ["Never state that a draft is TCPA compliant or offer legal advice; flag the risk and send it to counsel.", "Never invent a consent record, a consent date or a capture method that the team has not documented.", "Never write a message that claims a prize, a prize odds claim or an outcome the offer does not have."]:
        report.append(f"- {rule_text}")
    write_out(out_dir, "compliance-check.md", report)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
