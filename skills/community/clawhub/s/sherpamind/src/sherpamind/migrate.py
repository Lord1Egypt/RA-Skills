from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sqlite3

from .paths import ensure_path_layout


@dataclass
class MigrationResult:
    status: str
    message: str
    stats: dict | None = None


@dataclass
class LegacyArchiveResult:
    status: str
    message: str
    stats: dict | None = None


def _looks_empty_sqlite(path: Path) -> bool:
    if not path.exists():
        return True
    conn = sqlite3.connect(path)
    try:
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        user_tables = [row[0] for row in rows if row[0] != 'sqlite_sequence']
        return len(user_tables) == 0
    finally:
        conn.close()


def _copy_sqlite_via_backup(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        destination.unlink()
    src = sqlite3.connect(source)
    dst = sqlite3.connect(destination)
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()


def migrate_legacy_state(legacy_root: Path) -> MigrationResult:
    paths = ensure_path_layout()
    legacy_db = legacy_root / "state" / "sherpamind.sqlite3"
    legacy_watch = legacy_root / "state" / "watch_state.json"

    copied = []
    replaced = []
    skipped = []

    if legacy_db.exists():
        paths.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not paths.db_path.exists():
            _copy_sqlite_via_backup(legacy_db, paths.db_path)
            copied.append({"from": str(legacy_db), "to": str(paths.db_path), "method": "sqlite-backup"})
        elif _looks_empty_sqlite(paths.db_path):
            _copy_sqlite_via_backup(legacy_db, paths.db_path)
            replaced.append({"from": str(legacy_db), "to": str(paths.db_path), "reason": "destination sqlite was empty", "method": "sqlite-backup"})
        else:
            skipped.append({"path": str(legacy_db), "reason": "destination already contains data"})
    else:
        skipped.append({"path": str(legacy_db), "reason": "legacy db missing"})

    if legacy_watch.exists() and not paths.watch_state_path.exists():
        paths.watch_state_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(legacy_watch, paths.watch_state_path)
        copied.append({"from": str(legacy_watch), "to": str(paths.watch_state_path), "method": "copy2"})
    else:
        skipped.append({"path": str(legacy_watch), "reason": "missing or destination already exists"})

    return MigrationResult(
        status="ok",
        message="Legacy SherpaMind state migration evaluated.",
        stats={
            "copied": copied,
            "replaced": replaced,
            "skipped": skipped,
        },
    )


def archive_legacy_state(legacy_root: Path) -> LegacyArchiveResult:
    paths = ensure_path_layout()
    legacy_state_dir = legacy_root / "state"
    archive_root = paths.state_root / "legacy"
    moved = []
    skipped = []

    if not legacy_state_dir.exists():
        return LegacyArchiveResult(
            status="ok",
            message="No legacy state directory present.",
            stats={"moved": moved, "skipped": [{"path": str(legacy_state_dir), "reason": "missing"}]},
        )

    archive_root.mkdir(parents=True, exist_ok=True)
    for item in sorted(legacy_state_dir.iterdir()):
        destination = archive_root / item.name
        if destination.exists():
            skipped.append({"path": str(item), "reason": "archive destination already exists"})
            continue
        shutil.move(str(item), str(destination))
        moved.append({"from": str(item), "to": str(destination)})

    try:
        legacy_state_dir.rmdir()
    except OSError:
        pass

    return LegacyArchiveResult(
        status="ok",
        message="Legacy SherpaMind repo-local state archived into .SherpaMind/private/state/legacy.",
        stats={"moved": moved, "skipped": skipped, "archive_root": str(archive_root)},
    )
