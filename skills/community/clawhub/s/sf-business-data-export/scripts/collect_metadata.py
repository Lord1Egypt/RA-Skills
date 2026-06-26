#!/usr/bin/env python3
"""Collect normalized object metadata and field-baseline inputs for export."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def load_field_list(path: str) -> list[str]:
    source = Path(path)
    if source.suffix.lower() == ".json":
        payload = load_json(path)
        if not isinstance(payload, list):
            raise SystemExit(f"{path} must contain a JSON array of field API names")
        return [str(item) for item in payload]

    fields: list[str] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            value = line.strip()
            if value:
                fields.append(value)
    return fields


def run_command(args: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    output = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode == 0, output


def fetch_describe_from_sf(sobject: str, target_org: str | None) -> dict[str, Any]:
    command = ["sf", "sobject", "describe", "--sobject", sobject, "--json"]
    if target_org:
        command.extend(["--target-org", target_org])
    ok, output = run_command(command)
    if not ok:
        raise SystemExit(output or f"failed to describe sObject {sobject}")

    payload = json.loads(output)
    result = payload.get("result")
    if not isinstance(result, dict):
        raise SystemExit("unexpected describe output shape from Salesforce CLI")
    return result


def extract_record_types(describe: dict[str, Any]) -> list[dict[str, Any]]:
    raw_infos = describe.get("recordTypeInfos", [])
    results: list[dict[str, Any]] = []
    for item in raw_infos:
        if not isinstance(item, dict):
            continue
        results.append(
            {
                "name": item.get("name") or item.get("developerName") or item.get("recordTypeId"),
                "record_type_id": item.get("recordTypeId", ""),
                "available": bool(item.get("available", False)),
                "default": bool(item.get("defaultRecordTypeMapping", False)),
                "master": bool(item.get("master", False)),
            }
        )
    return results


def resolve_page_context(
    profile: str | None,
    record_type: str | None,
    record_types: list[dict[str, Any]],
) -> dict[str, Any]:
    available_record_types = [rt for rt in record_types if rt.get("available")]
    named_record_types = [rt for rt in available_record_types if rt.get("name")]
    names = [str(rt["name"]) for rt in named_record_types]

    if record_type:
        if record_type not in names:
            return {
                "status": "failed",
                "resolved_profile": profile or "current_user_profile",
                "resolved_record_type": "",
                "next_action": f"provide a valid record type from: {', '.join(names) if names else 'none found'}",
                "notes": ["requested record type not found in available record type mappings"],
            }
        return {
            "status": "resolved",
            "resolved_profile": profile or "current_user_profile",
            "resolved_record_type": record_type,
            "next_action": "",
            "notes": [],
        }

    if profile and len(names) > 1:
        return {
            "status": "needs_record_type",
            "resolved_profile": profile,
            "resolved_record_type": "",
            "next_action": f"provide the record type for profile {profile}",
            "notes": ["multiple record types are available in the requested profile context"],
        }

    if not profile and len(names) > 1:
        return {
            "status": "needs_confirmation",
            "resolved_profile": "current_user_profile",
            "resolved_record_type": "",
            "next_action": (
                "confirm whether to proceed with the current user's profile and an arbitrary record-type page, "
                "or provide a record type explicitly"
            ),
            "notes": ["multiple record types are available and no profile or record type was supplied"],
        }

    default_record_type = next((rt["name"] for rt in named_record_types if rt.get("default")), "")
    return {
        "status": "resolved",
        "resolved_profile": profile or "current_user_profile",
        "resolved_record_type": default_record_type,
        "next_action": "",
        "notes": [],
    }


def resolve_field_baseline(
    field_source: str,
    page_fields_file: str | None,
    explicit_fields_file: str | None,
) -> dict[str, Any]:
    if field_source == "explicit_fields":
        if not explicit_fields_file:
            return {
                "status": "failed",
                "source": "explicit_fields",
                "fields": [],
                "next_action": "provide an explicit fields file",
                "fallback_used": False,
            }
        return {
            "status": "resolved",
            "source": "explicit_fields",
            "fields": load_field_list(explicit_fields_file),
            "next_action": "",
            "fallback_used": False,
        }

    if page_fields_file:
        return {
            "status": "resolved",
            "source": "current_page_visible_fields",
            "fields": load_field_list(page_fields_file),
            "next_action": "",
            "fallback_used": False,
        }

    if explicit_fields_file:
        return {
            "status": "resolved",
            "source": "explicit_fields",
            "fields": load_field_list(explicit_fields_file),
            "next_action": "",
            "fallback_used": True,
        }

    return {
        "status": "failed",
        "source": "current_page_visible_fields",
        "fields": [],
        "next_action": (
            "provide page-visible fields from metadata collection or provide an explicit fields file"
        ),
        "fallback_used": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sobject", required=True, help="API name of the target sObject")
    parser.add_argument("--output", required=True, help="Output JSON path")
    parser.add_argument("--target-org", help="Salesforce org alias or username")
    parser.add_argument("--profile", help="Requested profile name")
    parser.add_argument("--record-type", help="Requested record type name")
    parser.add_argument(
        "--field-source",
        choices=["current_page", "explicit_fields"],
        default="current_page",
        help="Requested field baseline mode",
    )
    parser.add_argument(
        "--describe-input",
        help="Optional local describe JSON to use instead of calling Salesforce CLI",
    )
    parser.add_argument(
        "--page-fields-file",
        help="Optional file containing resolved current-page field API names",
    )
    parser.add_argument(
        "--explicit-fields-file",
        help="Optional file containing explicit field API names",
    )
    args = parser.parse_args()

    describe = load_json(args.describe_input) if args.describe_input else fetch_describe_from_sf(
        args.sobject, args.target_org
    )
    record_types = extract_record_types(describe)
    page_context = resolve_page_context(args.profile, args.record_type, record_types)
    field_baseline = resolve_field_baseline(
        args.field_source, args.page_fields_file, args.explicit_fields_file
    )

    payload = {
        "object_api_name": args.sobject,
        "target_org": args.target_org or "",
        "requested_profile": args.profile or "",
        "requested_record_type": args.record_type or "",
        "requested_field_source": args.field_source,
        "describe_status": "resolved",
        "describe": describe,
        "record_type_infos": record_types,
        "page_context": page_context,
        "field_baseline": field_baseline,
        "next_action": page_context["next_action"] or field_baseline["next_action"],
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    main()
