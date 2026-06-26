#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import DEFAULT_LIBRARY_PATH, format_value, load_yaml_if_exists, resolve_path


def build_pretty_output(payload: dict) -> str:
    lines = [
        "Pending voice reviews",
        f"- library: {payload['library_path']}",
        f"- review: {payload['review_path']}",
        f"- effective: {payload['effective_library_path']}",
        f"- mode: {payload['mode']}",
        f"- count: {payload['count']}",
    ]

    if not payload["items"]:
        lines.append("")
        lines.append("没有需要显示的音色条目。")
        return "\n".join(lines) + "\n"

    for item in payload["items"]:
        lines.append("")
        lines.append(f"* {item['asset_id']} | {item['display_name']}")
        lines.append(f"  review_status: {item['review_status']}")
        lines.append(f"  source_file: {format_value(item['source_file'])}")
        lines.append(f"  analysis_file: {format_value(item['analysis_file'])}")
        lines.append(f"  edit_target: {payload['review_edit_target']} -> clones.{item['asset_id']}.manual")
        lines.append(f"  manual: {format_value(item['manual_description'])}")
        lines.append(f"  archived: {format_value(item['archived_description'])}")
        lines.append(f"  effective: {format_value(item['effective_description'])}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="List pending clone voice reviews.")
    parser.add_argument("--library", default=str(DEFAULT_LIBRARY_PATH), help="Path to voice-library.yaml")
    parser.add_argument("--asset-id", dest="asset_id", help="Filter by asset id")
    parser.add_argument("--all", action="store_true", help="Show all entries, not only pending ones")
    parser.add_argument("--pretty", action="store_true", help="Render pretty text output")
    parser.add_argument("--json", action="store_true", help="Render JSON output")
    return parser.parse_args()


def display_review_target(library_dir: Path, review_path: Path) -> str:
    try:
        return str(review_path.resolve().relative_to(library_dir.resolve()))
    except ValueError:
        return str(review_path.resolve())


def main() -> None:
    args = parse_args()
    library_path = Path(args.library).resolve()
    library_dir = library_path.parent
    show_all = args.all
    pretty = args.pretty or (sys.stdout.isatty() and not args.json)

    library = load_yaml_if_exists(library_path, {}) or {}
    paths = library.get("paths") or {}

    review_path = resolve_path(library_dir, paths.get("review_file", "voice-reviews.yaml"))
    effective_library_path = resolve_path(
        library_dir,
        paths.get("effective_library_file", ".audiobook/effective-voice-library.yaml"),
    )

    review_store = load_yaml_if_exists(review_path, {"clones": {}}) or {"clones": {}}
    effective_library = load_yaml_if_exists(effective_library_path, {"clones": {}}) or {"clones": {}}

    asset_ids = sorted(
        {
            *list((library.get("clones") or {}).keys()),
            *list((review_store.get("clones") or {}).keys()),
            *list((effective_library.get("clones") or {}).keys()),
        }
    )

    items = []
    for asset_id in asset_ids:
        if args.asset_id and asset_id != args.asset_id:
            continue

        meta = (library.get("clones") or {}).get(asset_id) or {}
        review_entry = (review_store.get("clones") or {}).get(asset_id) or {}
        effective_entry = (effective_library.get("clones") or {}).get(asset_id) or {}
        review_status = (
            ((review_entry.get("review") or {}).get("status"))
            or ((meta.get("review_ref") or {}).get("last_status"))
            or "pending_manual_confirmation"
        )
        if not show_all and review_status == "manual_override_present":
            continue

        items.append(
            {
                "asset_id": asset_id,
                "display_name": review_entry.get("display_name")
                or meta.get("display_name")
                or effective_entry.get("display_name")
                or asset_id,
                "review_status": review_status,
                "source_file": meta.get("source_file") or effective_entry.get("source_file") or "",
                "manual_description": ((review_entry.get("manual") or {}).get("description")) or "",
                "archived_description": ((review_entry.get("archived_analysis") or {}).get("description")) or "",
                "effective_description": effective_entry.get("description") or "",
                "analysis_file": ((meta.get("analysis") or {}).get("analysis_file"))
                or ((review_entry.get("model_analysis") or {}).get("analysis_file"))
                or "",
            }
        )

    payload = {
        "library_path": str(library_path),
        "review_path": str(review_path),
        "effective_library_path": str(effective_library_path),
        "review_edit_target": display_review_target(library_dir, review_path),
        "mode": "all" if show_all else "pending_only",
        "count": len(items),
        "items": items,
    }

    if pretty:
        sys.stdout.write(build_pretty_output(payload))
        return

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # pragma: no cover - CLI error path
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
