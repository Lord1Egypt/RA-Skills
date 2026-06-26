#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path

from pydantic_airtable import AirtableConfig, AirtableManager


def load_class(module_path: str, class_name: str):
    path = Path(module_path).resolve()
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        return getattr(module, class_name)
    except AttributeError as exc:
        raise SystemExit(f"Class {class_name} not found in {module_path}") from exc


def configure(base_id: str | None, table_name: str | None) -> AirtableConfig:
    token = os.getenv("AIRTABLE_ACCESS_TOKEN")
    cfg_base_id = base_id or os.getenv("AIRTABLE_BASE_ID")
    if not token or not cfg_base_id:
        raise SystemExit("Set AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID, or pass --base-id.")
    return AirtableConfig(access_token=token, base_id=cfg_base_id, table_name=table_name)


def main():
    p = argparse.ArgumentParser(
        description="Run model-driven Airtable operations via pydantic-airtable. Reads AIRTABLE_ACCESS_TOKEN and AIRTABLE_BASE_ID from the environment unless --base-id is provided. WARNING: --module imports and executes the referenced local Python file, so only use trusted code."
    )
    p.add_argument("action", choices=["create-table-from-model", "sync-model", "validate-model"])
    p.add_argument("--module", required=True, help="Path to trusted Python module file; this file will be imported and executed")
    p.add_argument("--class-name", required=True, help="Model class name in module")
    p.add_argument("--base-id", help="Override Airtable base id")
    p.add_argument("--table", help="Override Airtable table name")
    p.add_argument("--create-missing-fields", action="store_true")
    p.add_argument("--update-field-types", action="store_true")
    args = p.parse_args()

    model_class = load_class(args.module, args.class_name)
    manager = AirtableManager(configure(args.base_id, args.table))

    if args.action == "create-table-from-model":
        result = manager.create_table_from_model(model_class, table_name=args.table, base_id=args.base_id)
    elif args.action == "sync-model":
        result = manager.sync_model_to_table(
            model_class,
            table_name=args.table,
            base_id=args.base_id,
            create_missing_fields=args.create_missing_fields,
            update_field_types=args.update_field_types,
        )
    elif args.action == "validate-model":
        result = manager.validate_model_against_table(model_class, table_name=args.table, base_id=args.base_id)
    else:
        raise SystemExit(f"Unsupported action: {args.action}")

    json.dump(result, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
