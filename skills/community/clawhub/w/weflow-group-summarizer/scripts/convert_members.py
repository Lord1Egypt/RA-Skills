#!/usr/bin/env python3
"""Convert WeFlow group member Excel export to a wxid->nickname JSON mapping."""

import argparse
import json
import os
import sys

try:
    import openpyxl
except ImportError:
    print("openpyxl is required: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    yaml = None  # Only needed with --yaml flag


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert WeFlow group member Excel to wxid->nickname JSON"
    )
    parser.add_argument("excel", help="Path to the Excel file exported by WeFlow")
    parser.add_argument("--yaml", help="Path to weflow-groups.yaml (updates members path for talker)")
    parser.add_argument("--talker", help="Talker chatroom ID (e.g. 12345@chatroom), required with --yaml")
    return parser.parse_args()


def build_mapping(excel_path):
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active

    # Row 4 (0-indexed row 3) is the header: 微信昵称, 微信备注, 群昵称, wxid, ...
    # Data starts from row 5 (0-indexed row 4)
    mapping = {}
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < 4:  # skip metadata and header rows
            continue
        nickname = row[0] or ""
        group_alias = row[2] or ""
        wxid = row[3] or ""
        if not wxid:
            continue
        display = nickname
        if group_alias:
            display = f"{nickname}（{group_alias}）"
        mapping[wxid] = display

    return mapping


def update_yaml(yaml_path, talker, members_json_path):
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    abs_path = os.path.abspath(members_json_path)

    found = False
    for group in data.get("groups", []):
        if group.get("talker") == talker:
            group["members"] = abs_path
            found = True
            break

    if not found:
        print(f"Warning: talker '{talker}' not found in {yaml_path}, appending new entry")
        data.setdefault("groups", []).append({"talker": talker, "members": abs_path})

    with open(yaml_path, "w") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def main():
    args = parse_args()

    mapping = build_mapping(args.excel)
    print(f"Found {len(mapping)} members")

    # Write JSON next to the Excel file
    json_path = os.path.splitext(args.excel)[0] + "_members.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Written to {json_path}")

    if args.yaml:
        if yaml is None:
            print("PyYAML is required for --yaml: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        if not args.talker:
            print("Error: --talker is required when using --yaml", file=sys.stderr)
            sys.exit(1)
        update_yaml(args.yaml, args.talker, json_path)
        print(f"Updated {args.yaml} with members path for talker {args.talker}")


if __name__ == "__main__":
    main()
