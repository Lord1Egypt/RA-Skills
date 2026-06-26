#!/usr/bin/env python3
"""Revert the responses prompt-cache patch from an OpenClaw dist bundle."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from _bundle_patch_common import (
    PATCH_MARKER,
    PatchError,
    ensure_dist_dir,
    format_paths,
    inspect_bundle,
    iter_candidate_bundles,
    latest_matching_backup,
    list_skill_backups,
    read_text,
    resolve_openclaw_root,
    run_node_check,
    write_text,
)


@dataclass
class RevertPlan:
    bundle_path: Path
    backup_path: Path
    current_text: str
    backup_text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Restore the latest pre-patch backup for any currently patched OpenClaw bundle "
            "that was modified by this skill."
        )
    )
    parser.add_argument(
        "--root",
        help="Path to the OpenClaw installation root (the directory that contains dist/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be restored without writing changes",
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
                    "Historical backups exist, but the current hashed bundle no longer exposes the original patch target. "
                    "This usually indicates an upgrade or bundle move; inspect the new dist layout before retrying."
                )
                for backup in historical_backups:
                    print(f"  historical backup: {backup}")
            return 1

        revertable: list[RevertPlan] = []
        already_clean: list[Path] = []
        unexpected: list[Path] = []

        for path in candidate_paths:
            inspection = inspect_bundle(path)
            if inspection.state == "patched":
                backup_path = latest_matching_backup(path)
                if backup_path is None:
                    unexpected.append(path)
                    continue
                revertable.append(
                    RevertPlan(
                        bundle_path=path,
                        backup_path=backup_path,
                        current_text=inspection.text,
                        backup_text=read_text(backup_path),
                    )
                )
                continue

            if PATCH_MARKER in inspection.text:
                unexpected.append(path)
                continue

            already_clean.append(path)

        print(f"OpenClaw root: {root}")
        for plan in revertable:
            print(f"REVERTABLE {plan.bundle_path} <= {plan.backup_path}")
        for path in already_clean:
            print(f"ALREADY_CLEAN {path}")
        for path in unexpected:
            print(f"MISSING_BACKUP {path}")

        if unexpected:
            raise PatchError(
                "Refusing to revert because at least one patched bundle does not have a matching backup: "
                f"{format_paths(unexpected)}"
            )

        if args.dry_run:
            if revertable:
                print("Dry run complete: the script would restore the latest matching backup for each patched bundle.")
            else:
                print("Dry run complete: no patched bundle was found; nothing would be restored.")
            return 0

        if not revertable:
            print("No currently patched bundle was found. Nothing to do.")
            return 0

        applied: list[RevertPlan] = []
        try:
            for plan in revertable:
                write_text(plan.bundle_path, plan.backup_text)
                applied.append(plan)
                print(f"Restored backup: {plan.bundle_path} <= {plan.backup_path}")

            for plan in applied:
                run_node_check(plan.bundle_path)
                print(f"node --check OK: {plan.bundle_path}")
        except PatchError as exc:
            for plan in reversed(applied):
                write_text(plan.bundle_path, plan.current_text)
                print(f"Reinstated patched content after failed rollback validation: {plan.bundle_path}")
            raise PatchError(f"Rollback aborted and current files were restored. {exc}") from exc

        print("Rollback completed successfully.")
        print("Restart the gateway to load the restored bundle: openclaw gateway restart")
        return 0

    except PatchError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
