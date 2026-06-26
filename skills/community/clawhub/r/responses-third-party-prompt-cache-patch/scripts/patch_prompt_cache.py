#!/usr/bin/env python3
"""Patch OpenClaw so third-party Responses endpoints keep prompt-cache hints."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from _bundle_patch_common import (
    PatchError,
    build_patched_text,
    create_backup,
    ensure_dist_dir,
    format_paths,
    inspect_bundle,
    iter_candidate_bundles,
    list_skill_backups,
    resolve_openclaw_root,
    run_node_check,
    write_text,
)


@dataclass
class AppliedChange:
    bundle_path: Path
    backup_path: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Patch an installed OpenClaw dist bundle so third-party OpenAI-compatible "
            "Responses endpoints no longer strip prompt_cache_key and prompt_cache_retention."
        )
    )
    parser.add_argument(
        "--root",
        help="Path to the OpenClaw installation root (the directory that contains dist/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the bundles that would be patched without writing changes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        root = resolve_openclaw_root(args.root)
        dist_dir = ensure_dist_dir(root)
        candidate_paths = iter_candidate_bundles(dist_dir)
        historical_backups = list_skill_backups(dist_dir)

        if not candidate_paths:
            print(f"No current bundle with shouldStripResponsesPromptCache(model) was found under {dist_dir}.")
            if historical_backups:
                print(
                    "Found historical skill backups in dist/. This usually means OpenClaw was upgraded, "
                    "the hashed bundle changed, or the target function moved. Update the skill markers and re-run."
                )
                for backup in historical_backups:
                    print(f"  historical backup: {backup}")
            return 1

        inspections = [inspect_bundle(path) for path in candidate_paths]
        patchable = [item for item in inspections if item.state == "patchable"]
        already_patched = [item for item in inspections if item.state == "patched"]
        unexpected = [item for item in inspections if item.state == "unexpected"]

        print(f"OpenClaw root: {root}")
        if historical_backups and patchable:
            print(
                "Detected older skill backups alongside an unpatched current bundle. "
                "This looks like an upgrade or bundle refresh; the script will reapply the patch to the current target."
            )

        for item in patchable:
            print(f"PATCHABLE {item.path}")
        for item in already_patched:
            print(f"ALREADY_PATCHED {item.path}")
        for item in unexpected:
            print(f"UNEXPECTED_SHAPE {item.path}")

        if unexpected:
            raise PatchError(
                "Refusing to continue because at least one target bundle no longer matches the expected narrow patch point: "
                f"{format_paths(item.path for item in unexpected)}"
            )

        if args.dry_run:
            if patchable:
                print("Dry run complete: the script would replace the return line inside shouldStripResponsesPromptCache(model).")
            else:
                print("Dry run complete: all matching bundles are already patched; nothing would be written.")
            return 0

        if not patchable:
            print("All matching bundles are already patched. Nothing to do.")
            return 0

        applied_changes: list[AppliedChange] = []
        for item in patchable:
            new_text = build_patched_text(item)
            backup_path = create_backup(item.path)
            write_text(item.path, new_text)
            applied_changes.append(AppliedChange(bundle_path=item.path, backup_path=backup_path))
            print(f"Created backup: {backup_path}")
            print(f"Patched bundle: {item.path}")

        try:
            for change in applied_changes:
                run_node_check(change.bundle_path)
                print(f"node --check OK: {change.bundle_path}")
        except PatchError as exc:
            for change in reversed(applied_changes):
                write_text(change.bundle_path, change.backup_path.read_text(encoding='utf-8'))
                print(f"Restored backup after failed syntax check: {change.bundle_path}")
            raise PatchError(f"Patch aborted and backups restored. {exc}") from exc

        print("Patch applied successfully.")
        print("Restart the gateway to load the patched bundle: openclaw gateway restart")
        return 0

    except PatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
