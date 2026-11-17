#!/usr/bin/env python3
"""Query Zoho Social MCP actions, profiles, and tasks directly from JSON data.

This CLI is designed for fast, token-efficient use by agents and operators.
It operates entirely on local JSON/JSONL references and requires no network
access or credentials.

Examples:
  # List all available role profiles
  python3 scripts/lookup_actions.py --profiles

  # List task recipes
  python3 scripts/lookup_actions.py --tasks

  # Inspect actions in a specific profile (resolved with inheritance)
  python3 scripts/lookup_actions.py --profile social-creator

  # Inspect actions for a task recipe
  python3 scripts/lookup_actions.py --task media-asset-management

  # Search actions by keyword in name or description
  python3 scripts/lookup_actions.py --search "draft"

  # Search and return only action names (compact for copying into MCP setup)
  python3 scripts/lookup_actions.py --search "upload" --names-only

  # Validate the catalog and profiles for consistency
  python3 scripts/lookup_actions.py --validate
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = REPOSITORY / "references" / "actions.jsonl"
DEFAULT_PROFILES = REPOSITORY / "references" / "profiles.json"


class ActionLookupError(Exception):
    """Raised on invalid catalog or profile structures."""


def load_catalog(path: Path) -> dict[str, dict]:
    if not path.exists():
        raise ActionLookupError(f"actions catalog not found: {path}")
    actions = {}
    for line_num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ActionLookupError(f"{path}:{line_num}: invalid JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ActionLookupError(f"{path}:{line_num}: record must be a JSON object")
        for field in ("key", "name", "summary", "description"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ActionLookupError(
                    f"{path}:{line_num}: field '{field}' must be a non-empty string"
                )
        key = record["key"]
        if key in actions:
            raise ActionLookupError(f"{path}:{line_num}: duplicate action key '{key}'")
        actions[key] = record
    return actions


def load_profiles_data(path: Path) -> dict:
    if not path.exists():
        raise ActionLookupError(f"profiles file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ActionLookupError(f"{path}: invalid JSON: {exc}") from exc


def resolve_profile_actions(profile_id: str, profiles_dict: dict, seen: set[str] | None = None) -> list[str]:
    if seen is None:
        seen = set()
    if profile_id in seen:
        raise ActionLookupError(f"circular profile inheritance detected at '{profile_id}'")
    seen.add(profile_id)

    if profile_id not in profiles_dict:
        raise ActionLookupError(f"profile '{profile_id}' not found")

    data = profiles_dict[profile_id]
    actions = []
    parent_id = data.get("extends")
    if parent_id:
        actions.extend(resolve_profile_actions(parent_id, profiles_dict, seen))

    for act in data.get("actions", []):
        if act not in actions:
            actions.append(act)

    denied = set(data.get("denied", []))
    if denied:
        actions = [act for act in actions if act not in denied]

    return actions


def validate_all(catalog: dict[str, dict], profiles_data: dict) -> list[str]:
    errors = []
    if profiles_data.get("version") != 1:
        errors.append("profiles file must have version 1")
    if profiles_data.get("service") != "social":
        errors.append("profiles file service must be 'social'")

    catalog_keys = {key for key, record in catalog.items() if not record.get("removed")}
    profiles = profiles_data.get("profiles", {})
    for p_id, p_data in profiles.items():
        actions = p_data.get("actions", [])
        if len(actions) != len(set(actions)):
            errors.append(f"Profile '{p_id}' contains duplicate actions")
        for act in actions:
            if act not in catalog_keys:
                errors.append(f"Profile '{p_id}' references unknown action: '{act}'")
        denied = p_data.get("denied", [])
        if len(denied) != len(set(denied)):
            errors.append(f"Profile '{p_id}' contains duplicate denied actions")
        for den in denied:
            if den not in catalog_keys:
                errors.append(f"Profile '{p_id}' denies unknown action: '{den}'")
        ext = p_data.get("extends")
        if ext and ext not in profiles:
            errors.append(f"Profile '{p_id}' extends non-existent profile: '{ext}'")

    for p_id in profiles:
        try:
            resolve_profile_actions(p_id, profiles)
        except ActionLookupError as exc:
            errors.append(str(exc))

    tasks = profiles_data.get("tasks", {})
    for t_id, t_data in tasks.items():
        actions = t_data.get("actions", [])
        if len(actions) != len(set(actions)):
            errors.append(f"Task '{t_id}' contains duplicate actions")
        for act in actions:
            if act not in catalog_keys:
                errors.append(f"Task '{t_id}' references unknown action: '{act}'")

    return errors


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Query Zoho Social MCP actions, profiles, and tasks directly from JSON."
    )
    parser.add_argument(
        "--catalog",
        default=str(DEFAULT_CATALOG),
        help=f"path to actions.jsonl (default: {DEFAULT_CATALOG})",
    )
    parser.add_argument(
        "--profiles-file",
        default=str(DEFAULT_PROFILES),
        help=f"path to profiles.json (default: {DEFAULT_PROFILES})",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--profiles", action="store_true", help="list all configured role profiles")
    group.add_argument("--tasks", action="store_true", help="list all configured task recipes")
    group.add_argument("--profile", metavar="ID", help="inspect actions in a role profile")
    group.add_argument("--task", metavar="ID", help="inspect actions in a task recipe")
    group.add_argument("--search", metavar="QUERY", help="search actions by keyword in name or description")
    group.add_argument("--action", metavar="NAME", help="get full description of a specific action")
    group.add_argument("--validate", action="store_true", help="validate profiles and tasks against the catalog")

    parser.add_argument("--raw", action="store_true", help="include raw profile actions without inheritance")
    parser.add_argument("--names-only", action="store_true", help="output only action names, one per line")
    parser.add_argument("--json", action="store_true", help="output results as JSON")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    catalog_path = Path(args.catalog)
    profiles_path = Path(args.profiles_file)

    try:
        catalog = load_catalog(catalog_path)
        profiles_data = load_profiles_data(profiles_path)
    except ActionLookupError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    profiles = profiles_data.get("profiles", {})
    tasks = profiles_data.get("tasks", {})

    if args.validate:
        errors = validate_all(catalog, profiles_data)
        if errors:
            print(f"Validation FAILED with {len(errors)} error(s):")
            for err in errors:
                print(f"  - {err}")
            return 1
        active_count = sum(1 for record in catalog.values() if not record.get("removed"))
        print(
            f"Validation OK: {active_count} active actions, "
            f"{len(profiles)} profiles, {len(tasks)} tasks."
        )
        return 0

    if args.profiles:
        if args.json:
            print(json.dumps(profiles, indent=2, ensure_ascii=False))
            return 0
        print("Configured Profiles:")
        for p_id, p_info in profiles.items():
            ext = f" (extends: {p_info['extends']})" if p_info.get("extends") else ""
            print(f"  - {p_id:22} {p_info.get('name', '')}{ext}")
            print(f"    {p_info.get('description', '')}")
        return 0

    if args.tasks:
        if args.json:
            print(json.dumps(tasks, indent=2, ensure_ascii=False))
            return 0
        print("Configured Task Recipes:")
        for t_id, t_info in tasks.items():
            print(f"  - {t_id:32} {t_info.get('name', '')}")
            print(f"    {t_info.get('description', '')}")
        return 0

    if args.profile:
        p_id = args.profile
        if p_id not in profiles:
            print(f"Error: profile '{p_id}' not found.", file=sys.stderr)
            return 1
        p_info = profiles[p_id]
        if args.raw:
            action_names = p_info.get("actions", [])
        else:
            action_names = resolve_profile_actions(p_id, profiles)

        if args.names_only:
            for name in action_names:
                print(catalog.get(name, {}).get("name", name))
            return 0

        if args.json:
            out = {
                "id": p_id,
                "name": p_info.get("name"),
                "description": p_info.get("description"),
                "extends": p_info.get("extends"),
                "total_actions": len(action_names),
                "actions": [
                    {
                        "name": act,
                        "summary": catalog.get(act, {}).get("summary", ""),
                    }
                    for act in action_names
                ],
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0

        print(f"Profile: {p_info.get('name')} ({p_id})")
        print(f"Description: {p_info.get('description')}")
        if p_info.get("extends") and not args.raw:
            print(f"Inherits from: {p_info['extends']}")
        print(f"Total Actions: {len(action_names)}\n")
        for act in sorted(action_names):
            display_name = catalog.get(act, {}).get("name", act)
            summary = catalog.get(act, {}).get("summary", "")
            print(f"  - {display_name:35} {summary[:75]}")
        return 0

    if args.task:
        t_id = args.task
        if t_id not in tasks:
            print(f"Error: task '{t_id}' not found.", file=sys.stderr)
            return 1
        t_info = tasks[t_id]
        action_names = t_info.get("actions", [])

        if args.names_only:
            for name in action_names:
                print(catalog.get(name, {}).get("name", name))
            return 0

        if args.json:
            out = {
                "id": t_id,
                "name": t_info.get("name"),
                "description": t_info.get("description"),
                "total_actions": len(action_names),
                "actions": [
                    {
                        "name": act,
                        "summary": catalog.get(act, {}).get("summary", ""),
                    }
                    for act in action_names
                ],
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0

        print(f"Task: {t_info.get('name')} ({t_id})")
        print(f"Description: {t_info.get('description')}")
        print(f"Required Actions ({len(action_names)}):\n")
        for act in action_names:
            display_name = catalog.get(act, {}).get("name", act)
            summary = catalog.get(act, {}).get("summary", "")
            print(f"  - {display_name:35} {summary[:75]}")
        return 0

    if args.action:
        act = args.action
        record = catalog.get(act)
        if not record:
            candidates = [
                key
                for key, candidate in catalog.items()
                if key.lower() == act.lower()
                or candidate.get("name", "").lower() == act.lower()
            ]
            if candidates:
                record = catalog[candidates[0]]
        if not record:
            print(f"Error: action '{act}' not found in catalog.", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(record, indent=2, ensure_ascii=False))
            return 0
        print(f"Action: {record.get('name')} (Key: {record.get('key')})")
        print(f"Summary: {record.get('summary')}")
        print(f"\nDescription:\n{record.get('description')}")
        return 0

    if args.search:
        query = args.search.lower()
        terms = query.split()
        matches = []
        for key, record in catalog.items():
            if record.get("removed"):
                continue
            content = f"{key} {record.get('name', '')} {record.get('description', '')}".lower()
            if all(term in content for term in terms):
                matches.append(record)

        if args.names_only:
            for m in matches:
                print(m["name"])
            return 0

        if args.json:
            print(json.dumps(matches, indent=2, ensure_ascii=False))
            return 0

        print(f"Found {len(matches)} action(s) matching '{args.search}':\n")
        for m in sorted(matches, key=lambda x: x["key"]):
            print(f"  - {m['name']:35} {m.get('summary', '')[:75]}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
