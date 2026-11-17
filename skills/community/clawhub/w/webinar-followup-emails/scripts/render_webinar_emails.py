#!/usr/bin/env python3
"""Webinar Follow-up Emails

Fills the webinar follow-up emails template with rows from a CSV.

Parameters for this build:
{
  "template": "templates/webinar-followup.md",
  "mapping": {
    "{{subject_line}}": "subject_line",
    "{{first_name}}": "first_name",
    "{{body_paragraph}}": "body_paragraph",
    "{{event_name}}": "event_name",
    "{{event_date}}": "event_date",
    "{{event_time}}": "event_time",
    "{{time_zone}}": "time_zone",
    "{{join_link}}": "join_link",
    "{{host_name}}": "host_name",
    "{{replay_link}}": "replay_link",
    "{{cta_label}}": "cta_label",
    "{{cta_url}}": "cta_url",
    "{{sender_name}}": "sender_name",
    "{{company_name}}": "company_name",
    "{{postal_address}}": "postal_address",
    "{{unsubscribe_url}}": "unsubscribe_url"
  }
}

Usage:
    python3 webinar_follow-up_emails.py --input <file> --out <dir>
"""

import argparse
import os
import re
import sys

TITLE = "Webinar Follow-up Emails"


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


TEMPLATE = 'templates/webinar-followup.md'
MAPPING = {"{{subject_line}}": "subject_line", "{{first_name}}": "first_name", "{{body_paragraph}}": "body_paragraph", "{{event_name}}": "event_name", "{{event_date}}": "event_date", "{{event_time}}": "event_time", "{{time_zone}}": "time_zone", "{{join_link}}": "join_link", "{{host_name}}": "host_name", "{{replay_link}}": "replay_link", "{{cta_label}}": "cta_label", "{{cta_url}}": "cta_url", "{{sender_name}}": "sender_name", "{{company_name}}": "company_name", "{{postal_address}}": "postal_address", "{{unsubscribe_url}}": "unsubscribe_url"}


def run(input_path, out_dir):
    template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), TEMPLATE)
    if not os.path.exists(template_path):
        template_path = input_path
    template = open(template_path, encoding="utf-8", errors="replace").read()
    rows = read_csv(input_path)
    written = []
    for index, row in enumerate(rows, 1):
        body = template
        for placeholder, column in MAPPING.items():
            body = body.replace("{" + placeholder + "}", str(row.get(column, "")))
        name = os.path.join(out_dir, f"{index:02d}-" + (str(row.get(list(MAPPING.values())[0], "out")) if MAPPING else "out").replace(" ", "-").lower() + ".md")
        with open(name, "w", encoding="utf-8") as handle:
            handle.write(body)
        written.append(name)
    print(f"rendered {len(written)} file(s) into {out_dir}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", required=True, help="input file for this job")
    parser.add_argument("--out", default="./out", help="output directory")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    run(args.input, args.out)


if __name__ == "__main__":
    main()
