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


def configure(table_name: str | None, base_id: str | None) -> AirtableConfig:
    token = os.getenv("AIRTABLE_ACCESS_TOKEN")
    cfg_base_id = base_id or os.getenv("AIRTABLE_BASE_ID")
    if not token or not cfg_base_id:
        raise SystemExit("Set AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID, or pass --base-id.")
    return AirtableConfig(access_token=token, base_id=cfg_base_id, table_name=table_name)


def main():
    p = argparse.ArgumentParser(
        description="Manage Airtable records via pydantic-airtable. Reads AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID from the environment unless --base-id is provided. --fields/--records/--updates accept inline JSON or @file.json, which reads a local file from disk."
    )
    p.add_argument("action", choices=["list", "get", "create", "update", "delete", "batch-create", "batch-update"])
    p.add_argument("--table", help="Airtable table name")
    p.add_argument("--base-id", help="Override Airtable base id")
    p.add_argument("--record-id")
    p.add_argument("--fields", help="Inline JSON or @file.json")
    p.add_argument("--records", help="Inline JSON array or @file.json")
    p.add_argument("--updates", help="Inline JSON array or @file.json")
    p.add_argument("--view")
    p.add_argument("--max-records", type=int)
    args = p.parse_args()

    manager = AirtableManager(configure(args.table, args.base_id))

    if args.action == "list":
        result = manager.get_records(table_name=args.table, max_records=args.max_records, view=args.view)
    elif args.action == "get":
        if not args.record_id:
            raise SystemExit("--record-id is required for get")
        result = manager.get_record(record_id=args.record_id, table_name=args.table)
    elif args.action == "create":
        if not args.fields:
            raise SystemExit("--fields is required for create")
        result = manager.create_record(fields=load_json_arg(args.fields), table_name=args.table)
    elif args.action == "update":
        if not args.record_id or not args.fields:
            raise SystemExit("--record-id and --fields are required for update")
        result = manager.update_record(record_id=args.record_id, fields=load_json_arg(args.fields), table_name=args.table)
    elif args.action == "delete":
        if not args.record_id:
            raise SystemExit("--record-id is required for delete")
        result = manager.delete_record(record_id=args.record_id, table_name=args.table)
    elif args.action == "batch-create":
        if not args.records:
            raise SystemExit("--records is required for batch-create")
        payload = load_json_arg(args.records)
        results = [manager.create_record(fields=item, table_name=args.table) for item in payload]
        result = {"records": results}
    elif args.action == "batch-update":
        if not args.updates:
            raise SystemExit("--updates is required for batch-update")
        payload = load_json_arg(args.updates)
        results = []
        for item in payload:
            record_id = item.get("id") or item.get("record_id")
            fields = item.get("fields")
            if not record_id or fields is None:
                raise SystemExit("Each update item must contain id/record_id and fields")
            results.append(manager.update_record(record_id=record_id, fields=fields, table_name=args.table))
        result = {"records": results}
    else:
        raise SystemExit(f"Unsupported action: {args.action}")

    json.dump(result, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
