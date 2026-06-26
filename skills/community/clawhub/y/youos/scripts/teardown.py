#!/usr/bin/env python3
"""YouOS teardown — remove all user data while keeping the code."""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

# Resolve instance paths via settings so teardown honors YOUOS_DATA_DIR —
# without this, running `scripts/teardown.py` with an instance set would
# print "delete this" pointing at the repo dirs while the actual user data
# (DB, adapters, var/) sat untouched in the instance, and the rmtree below
# would scrub the repo's own dev artefacts instead.
from app.core.settings import get_instance_root, get_models_dir, get_var_dir  # noqa: E402
from app.db.bootstrap import resolve_sqlite_path  # noqa: E402


def _dir_size(path: Path) -> str:
    """Human-readable directory size."""
    if not path.exists():
        return "0 B"
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    for unit in ("B", "KB", "MB", "GB"):
        if total < 1024:
            return f"{total:.1f} {unit}"
        total /= 1024
    return f"{total:.1f} TB"


def _file_size(path: Path) -> str:
    if not path.exists():
        return "0 B"
    size = path.stat().st_size
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _feedback_count(db_path: Path) -> int:
    if not db_path.exists():
        return 0
    try:
        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM feedback_pairs").fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0


def _stop_server() -> None:
    """Stop any running uvicorn server."""
    import subprocess

    try:
        subprocess.run(
            ["pkill", "-f", "uvicorn.*app.main:app"],
            capture_output=True,
            timeout=5,
        )
        print("  Stopped running server.")
    except Exception:
        pass


def _remove_cron() -> None:
    """Remove nightly cron job if OpenClaw is available."""
    import subprocess

    try:
        if shutil.which("openclaw"):
            subprocess.run(
                ["openclaw", "cron", "remove", "--name", "youos:nightly"],
                capture_output=True,
                timeout=10,
            )
            print("  Removed nightly cron job.")
    except Exception:
        pass


def teardown(delete_all: bool = False) -> None:
    from app.core.settings import get_settings

    settings = get_settings()
    instance_root = get_instance_root()
    db_path = resolve_sqlite_path(settings.database_url)
    data_dir = instance_root / "data"
    models_dir = get_models_dir()
    var_dir = get_var_dir()

    print()
    print("YouOS Teardown")
    print("=" * 40)
    print(f"Target instance: {instance_root}")
    print()

    # Stop server
    _stop_server()

    # Show what will be deleted
    print("The following will be deleted:")
    print()
    print(f"  Database:        {db_path} ({_file_size(db_path)})")
    print(f"  Raw email cache: {data_dir}/ ({_dir_size(data_dir)})")
    print(f"  LoRA adapters:   {models_dir}/ ({_dir_size(models_dir)})")
    print(f"  Feedback pairs:  {_feedback_count(db_path)} pairs")
    print()

    if not delete_all:
        confirm = input("This will permanently delete your corpus and model. Type 'delete' to confirm: ")
        if confirm.strip().lower() != "delete":
            print("Aborted.")
            return

    # Delete data directories
    removed = []
    for d in [data_dir, models_dir, var_dir]:
        if d.exists():
            shutil.rmtree(d)
            removed.append(str(d))
            print(f"  Removed {d}/")

    # Remove analysis file (in the instance configs, not the repo)
    analysis = Path(settings.configs_dir) / "persona_analysis.json"
    if analysis.exists():
        analysis.unlink()
        print(f"  Removed {analysis}")

    # Optionally remove cron
    _remove_cron()

    print()
    print(f"YouOS data removed. The code remains at {ROOT_DIR}.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Remove all YouOS user data")
    parser.add_argument("--all", action="store_true", help="Delete everything without prompting")
    args = parser.parse_args()
    teardown(delete_all=args.all)


if __name__ == "__main__":
    main()
