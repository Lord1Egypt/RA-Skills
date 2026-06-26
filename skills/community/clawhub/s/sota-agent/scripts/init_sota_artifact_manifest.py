#!/usr/bin/env python3
"""Create a machine-readable artifact manifest for a SOTA export bundle."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_path


def path_record(
    path: Path,
    role: str,
    *,
    alias_roots: list[tuple[Path | None, str]],
    allow_absolute_paths: bool,
) -> dict[str, object]:
    record: dict[str, object] = {
        "role": role,
        "path": sanitize_path(
            path,
            alias_roots=alias_roots,
            allow_absolute_paths=allow_absolute_paths,
        ),
        "exists": path.exists(),
    }
    if not path.exists():
        return record
    record["type"] = "dir" if path.is_dir() else "file"
    return record


def parse_item(item: str) -> tuple[str, Path]:
    if "=" not in item:
        raise SystemExit(f"invalid --item value: {item!r}, expected role=path")
    role, raw_path = item.split("=", 1)
    role = role.strip()
    raw_path = raw_path.strip()
    if not role or not raw_path:
        raise SystemExit(f"invalid --item value: {item!r}, expected role=path")
    return role, Path(raw_path).expanduser().resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--bundle-root", required=True, help="Root directory of the exported bundle.")
    parser.add_argument(
        "--item",
        action="append",
        default=[],
        help="Repeatable role=path pair for important artifacts inside or outside the bundle.",
    )
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    bundle_root = Path(args.bundle_root).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    alias_roots = [(bundle_root, "$BUNDLE_ROOT")]

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "bundle_root": sanitize_path(
            bundle_root,
            alias_roots=alias_roots,
            allow_absolute_paths=False,
        ),
        "bundle_exists": bundle_root.exists(),
        "artifacts": [
            path_record(
                path,
                role,
                alias_roots=alias_roots,
                allow_absolute_paths=False,
            )
            for role, path in (parse_item(item) for item in args.item)
        ],
        "notes": [],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
