#!/usr/bin/env python3
"""Revert OpenClaw dist JS bundles from the latest telegram-footer backups."""

import argparse
import glob
import os
import pathlib
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True

MARKER_START = "/* OPENCLAW_TELEGRAM_STATUS_FOOTER_START */"
TARGET_GLOBS = [
    "agent-runner.runtime-*.js",
    "reply-*.js",
    "compact-*.js",
    "pi-embedded-*.js",
    "plugin-sdk/thread-bindings-*.js",
    "model-selection-*.js",
    "auth-profiles-*.js",
    "delivery-*.js",
]


def verify_node_syntax(path: pathlib.Path):
    result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        details = (result.stderr or result.stdout or "node --check failed").strip()
        raise RuntimeError(details)


def _is_backup_path(path: pathlib.Path) -> bool:
    return ".bak.telegram-footer." in path.name


def iter_target_files(dist: pathlib.Path) -> list[pathlib.Path]:
    files: set[pathlib.Path] = set()
    for pattern in TARGET_GLOBS:
        for fp in dist.glob(pattern):
            if fp.is_file() and not _is_backup_path(fp):
                files.add(fp)
    return sorted(files)


def revert_file(path: pathlib.Path, dry_run: bool) -> bool:
    content = path.read_text(encoding="utf-8")
    if MARKER_START not in content:
        print(f"[skip] not patched: {path}")
        return False

    backups = sorted(glob.glob(str(path) + ".bak.telegram-footer.*"))
    if not backups:
        print(f"[err] backup not found: {path}", file=sys.stderr)
        return False

    latest = pathlib.Path(backups[-1])
    if dry_run:
        print(f"[dry-run] would restore {path} <- {latest}")
        return True

    current_backup = path.with_suffix(path.suffix + ".bak.pre-revert")
    shutil.copy2(path, current_backup)
    try:
        shutil.copy2(latest, path)
        verify_node_syntax(path)
    except Exception as exc:
        shutil.copy2(current_backup, path)
        print(f"[err] restore failed, put current file back: {path}", file=sys.stderr)
        print(f"[err] reason: {exc}", file=sys.stderr)
        return False

    print(f"[ok] restored    : {path} <- {latest}")
    print(f"[ok] safety copy : {current_backup}")
    print(f"[ok] syntax check: node --check passed")
    return True


def preflight(dist: pathlib.Path, dry_run: bool) -> int:
    node_path = shutil.which("node")
    if not node_path:
        print("[err] node not found in PATH (required for syntax validation via node --check)", file=sys.stderr)
        return 2
    if not dist.exists() or not dist.is_dir():
        print(f"[err] dist directory not found: {dist}", file=sys.stderr)
        return 2
    if not dry_run and not os.access(dist, os.W_OK):
        print(f"[err] no write permission for dist directory: {dist}", file=sys.stderr)
        return 2
    if dry_run and not os.access(dist, os.R_OK):
        print(f"[err] no read permission for dist directory: {dist}", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Restore OpenClaw dist files from latest telegram-footer backups.")
    parser.add_argument("--dist", default="/usr/lib/node_modules/openclaw/dist", help="OpenClaw dist directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, do not write")
    args = parser.parse_args()

    dist = pathlib.Path(args.dist)
    rc = preflight(dist, dry_run=args.dry_run)
    if rc != 0:
        return rc

    files = iter_target_files(dist)
    if not files:
        print("[err] no target dist files found", file=sys.stderr)
        return 2

    changed = 0
    for f in files:
        if revert_file(f, args.dry_run):
            changed += 1

    print("[done] no files restored" if changed == 0 else f"[done] restored files: {changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
