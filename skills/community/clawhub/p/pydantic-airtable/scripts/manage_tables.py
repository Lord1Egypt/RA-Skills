#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

from pydantic_airtable import AirtableConfig, AirtableManager


def load_json_arg(value: str):
    if value.startswith("@"):
        return json.loads(Path(value[1:]).read_text())
    return json.loads(value)


def configure(base_id: str | None) -> AirtableConfig:
    token = os.getenv("AIRTABLE_ACCESS_TOKEN")
    cfg_base_id = base_id or os.getenv("AIRTABLE_BASE_ID")
    if not token:
        raise SystemExit("Set AIRTABLE_ACCESS_TOKEN.")
    return AirtableConfig(access_token=token, base_id=cfg_base_id or "", table_name=None)


def main():
    p = argparse.ArgumentParser(
        description="Manage Airtable tables via pydantic-airtable. Reads AIRTABLE_ACCESS_TOKEN and optionally AIRTABLE_BASE_ID from the environment unless --base-id is provided. --fields/--updates accept inline JSON or @file.json, which reads a local file from disk."
    )
    p.add_argument("action", choices=["list-bases", "base-schema", "table-schema", "create-table", "update-table", "delete-table"])
    p.add_argument("--base-id", help="Override Airtable base id")
    p.add_argument("--table", help="Table name")
    p.add_argument("--table-id", help="Table id")
    p.add_argument("--name", help="New table name")
    p.add_argument("--fields", help="Inline JSON or @file.json")
    p.add_argument("--updates", help="Inline JSON or @file.json")
    args = p.parse_args()

    manager = AirtableManager(configure(args.base_id))

    if args.action == "list-bases":
        result = manager.list_bases()
    elif args.action == "base-schema":
        result = manager.get_base_schema(base_id=args.base_id)
    elif args.action == "table-schema":
        if not args.table:
            raise SystemExit("--table is required for table-schema")
        result = manager.get_table_schema(table_name=args.table, base_id=args.base_id)
    elif args.action == "create-table":
        if not args.name or not args.fields:
            raise SystemExit("--name and --fields are required for create-table")
        result = manager.create_table(name=args.name, fields=load_json_arg(args.fields), base_id=args.base_id)
    elif args.action == "update-table":
        if not args.table_id or not args.updates:
            raise SystemExit("--table-id and --updates are required for update-table")
        result = manager.update_table(table_id=args.table_id, updates=load_json_arg(args.updates), base_id=args.base_id)
    elif args.action == "delete-table":
        if not args.table_id:
            raise SystemExit("--table-id is required for delete-table")
        result = manager.delete_table(table_id=args.table_id, base_id=args.base_id)
    else:
        raise SystemExit(f"Unsupported action: {args.action}")

    json.dump(result, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
