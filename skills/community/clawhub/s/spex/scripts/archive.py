#!/usr/bin/env python3
"""Archive completed specs.

Moves spec directories whose todo.json items are all completed
into the archives directory.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from cli import ArgumentParser
from common import (
    find_completed_specs,
    find_matching_specs,
    get_archives_dir,
    get_specs_dir,
    has_active_branch,
    is_spec_completed,
    load_meta,
    logger,
    resolve_spec_dir,
)
from config import get_project_context
from debug_log import DEBUG_LOG_NAME

_DEBUG_ORPHAN_ALLOWED = frozenset({
    DEBUG_LOG_NAME,
    f"{DEBUG_LOG_NAME}.prev_end",
})


def is_debug_orphan_stub(spec_dir: Path) -> bool:
    """Return True if ``spec_dir`` only contains debug tee artifacts.

    A debug orphan stub is a directory whose entries are a subset of
    ``{debug.log, debug.log.prev_end}`` and that contains ``debug.log``.
    Directories with any other file (e.g. ``.DS_Store``) are not stubs.
    """
    if not spec_dir.is_dir():
        return False
    if not (spec_dir / DEBUG_LOG_NAME).is_file():
        return False
    names = {p.name for p in spec_dir.iterdir()}
    return names <= _DEBUG_ORPHAN_ALLOWED


def remove_debug_orphan_stub(
    spec_dir: Path,
    archives_dir: Path,
    *,
    dry_run: bool = False,
) -> bool:
    """Remove a debug-only stub when archives already has the same name.

    Returns True if the stub was removed, or would be removed in dry-run.
    Returns False when ``spec_dir`` is not a stub or no archives sibling
    exists (stub is left untouched).
    """
    if not is_debug_orphan_stub(spec_dir):
        return False
    if not (archives_dir / spec_dir.name).is_dir():
        return False
    if dry_run:
        logger.info("Would remove orphan stub: %s", spec_dir.name)
        return True
    shutil.rmtree(spec_dir)
    logger.info("Removed orphan stub: %s", spec_dir.name)
    return True


def move_spec_with_conflict(source_dir: Path, dest_dir: Path) -> Path:
    """Move source_dir into dest_dir, appending suffix on conflict.

    Returns the final destination path.
    """
    dest = dest_dir / source_dir.name
    if not dest.exists():
        shutil.move(str(source_dir), str(dest))
        return dest

    counter = 2
    while True:
        candidate = dest_dir / f"{source_dir.name}-{counter}"
        if not candidate.exists():
            shutil.move(str(source_dir), str(candidate))
            return candidate
        counter += 1


def move_spec(spec_dir: Path, archives_dir: Path) -> Path:
    """Move spec_dir into archives_dir, appending suffix on conflict.

    Thin wrapper around move_spec_with_conflict for backward compatibility.
    Returns the final destination path.
    """
    return move_spec_with_conflict(spec_dir, archives_dir)


def archive_single_spec(
    spec_name: str,
    specs_dir: Path,
    archives_dir: Path,
    force: bool = False,
    dry_run: bool = False,
) -> Path | None:
    """Archive a single spec by name. Supports partial name matching.

    Returns the destination path, or None if skipped due to active branch.
    When a debug-only stub is cleaned because archives already has the
    same name, returns the existing archives path (success, no ``-2``).
    """
    spec_dir = resolve_spec_dir(spec_name, specs_dir)
    if remove_debug_orphan_stub(spec_dir, archives_dir, dry_run=dry_run):
        return archives_dir / spec_dir.name
    if not force and not is_spec_completed(spec_dir):
        logger.info(
            "Skipping: spec is not completed (use --force to archive)"
        )
        return None
    if not force and has_active_branch(spec_dir):
        meta = load_meta(spec_dir)
        spex_branch = meta.spex_branch if meta else ""
        logger.info(
            "Skipping: spex branch '%s' still exists"
            " (use --force to archive)", spex_branch
        )
        return None
    if dry_run:
        logger.info("Would archive: %s", spec_dir.name)
        return archives_dir / spec_dir.name
    archives_dir.mkdir(parents=True, exist_ok=True)
    dest = move_spec(spec_dir, archives_dir)
    logger.info("Archived: %s -> %s", spec_dir.name, dest)
    return dest


def restore_single_spec(
    spec_name: str,
    specs_dir: Path,
    archives_dir: Path,
    dry_run: bool = False,
) -> Path | None:
    """Restore a single spec from archives back to specs.

    Uses fuzzy substring matching against archives_dir. Exits with error
    if no match or multiple matches.

    Returns the destination path in specs_dir, or None on error.
    """
    if not archives_dir.is_dir():
        logger.error(
            "Error: archives directory does not exist: %s", archives_dir
        )
        sys.exit(1)

    matches = find_matching_specs(spec_name, archives_dir)
    if not matches:
        logger.error(
            "Error: no spec matching '%s' found in archives.", spec_name
        )
        sys.exit(1)
    if len(matches) > 1:
        names = "\n  ".join(m.name for m in matches)
        logger.error(
            "Error: multiple specs match '%s' in archives:\n  %s",
            spec_name, names
        )
        sys.exit(1)

    if dry_run:
        logger.info("Would restore: %s", matches[0].name)
        return specs_dir / matches[0].name
    specs_dir.mkdir(parents=True, exist_ok=True)
    dest = move_spec_with_conflict(matches[0], specs_dir)
    logger.info("Restored: %s -> %s", matches[0].name, dest)
    return dest


def main(argv=None):
    parser = ArgumentParser(
        prog="spex archive",
        description="Archive completed specs.",
    )
    parser.add_argument("--name", help="Archive a single spec by name")
    parser.add_argument("-n", "--dry-run", action="store_true",
                        help="Preview without moving")
    parser.add_argument("-f", "--force", action="store_true",
                        help="Bypass spex_branch existence check")
    parser.add_argument("--restore", action="store_true",
                        help="Restore a spec from archives back to specs")
    parser.add_argument("--not", action="store_true", dest="restore",
                        help=argparse.SUPPRESS)
    parser.add_argument("--all-projects", action="store_true",
                        help="Archive specs from all projects")
    args = parser.parse(argv)

    specs_dir = get_specs_dir()
    archives_dir = get_archives_dir()

    if args.restore:
        if not args.name:
            logger.error(
                "Error: --restore requires --name to specify what to restore."
            )
            sys.exit(1)
        restore_single_spec(args.name, specs_dir, archives_dir,
                             dry_run=args.dry_run)
        return

    if args.name:
        archive_single_spec(args.name, specs_dir, archives_dir, args.force,
                             dry_run=args.dry_run)
        return

    ctx = get_project_context()

    if not ctx.in_git_workdir() and not args.all_projects:
        logger.info(
            "Not in a git workdir. Use --all-projects to archive"
            " specs from all projects."
        )
        return

    completed = find_completed_specs(
        specs_dir, ctx, args.force, all_projects=args.all_projects,
    )

    def _cleanup_orphan_stubs(*, dry_run: bool) -> int:
        count = 0
        if not specs_dir.is_dir():
            return 0
        for entry in sorted(specs_dir.iterdir()):
            if entry.is_dir() and remove_debug_orphan_stub(
                entry, archives_dir, dry_run=dry_run
            ):
                count += 1
        return count

    if args.dry_run:
        # Show specs that would be skipped due to active branches
        skipped = [
            d for d in sorted(specs_dir.iterdir())
            if d.is_dir() and is_spec_completed(d) and has_active_branch(d)
        ]
        if completed:
            logger.info("Would archive %d spec(s):", len(completed))
            for spec_dir in completed:
                logger.info("  %s", spec_dir.name)
        else:
            logger.info("No completed specs to archive.")
        if skipped:
            logger.info(
                "Would skip %d spec(s) (active spex_branch):", len(skipped)
            )
            for spec_dir in skipped:
                meta = load_meta(spec_dir)
                branch = meta.spex_branch if meta else ""
                logger.info("  %s (%s)", spec_dir.name, branch)
        _cleanup_orphan_stubs(dry_run=True)
        return

    cleaned = _cleanup_orphan_stubs(dry_run=False)
    if not completed:
        if cleaned == 0:
            logger.info("No completed specs to archive.")
        return

    archives_dir.mkdir(parents=True, exist_ok=True)
    for spec_dir in completed:
        dest = move_spec(spec_dir, archives_dir)
        logger.info("Archived: %s -> %s", spec_dir.name, dest)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
