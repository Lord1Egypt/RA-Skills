from __future__ import annotations

import json
import re
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.settings import Settings
from app.db.bootstrap import resolve_sqlite_path

# NB: facts are stored in the `memory` table (there is no `facts` table); the
# previous "facts" entry never matched, so a real drop went undetected.
_REQUIRED_TABLES = ("reply_pairs", "draft_history", "memory")


@dataclass(slots=True)
class SafetyReport:
    db_path: str
    warnings: list[str]
    table_counts: dict[str, int]
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "db_path": self.db_path,
            "warnings": self.warnings,
            "table_counts": self.table_counts,
            "timestamp": self.timestamp,
        }


def _is_unsafe_path(path: Path) -> bool:
    unsafe_parts = {".Trash", "Trash"}
    return any(part in unsafe_parts for part in path.parts)


def validate_instance_paths(settings: Settings) -> None:
    db_path = resolve_sqlite_path(settings.database_url).expanduser().resolve()
    if _is_unsafe_path(db_path):
        raise RuntimeError(f"Unsafe database path detected: {db_path}")

    if settings.data_dir is not None:
        data_dir = Path(settings.data_dir).expanduser().resolve()
        expected_db = (data_dir / "var" / "youos.db").resolve()
        if db_path != expected_db:
            raise RuntimeError(
                "Database path mismatch for instance mode: "
                f"expected {expected_db}, got {db_path}. "
                "Set YOUOS_DATABASE_URL to match YOUOS_DATA_DIR/var/youos.db."
            )
        if not data_dir.exists():
            raise RuntimeError(f"Instance data directory does not exist: {data_dir}")
        if not (data_dir / "var").exists():
            raise RuntimeError(f"Missing required directory: {data_dir / 'var'}")
        if not settings.configs_dir.exists():
            raise RuntimeError(f"Missing required configs directory: {settings.configs_dir}")



def _load_prev_counts(state_path: Path) -> dict[str, int]:
    if not state_path.exists():
        return {}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
        return {str(k): int(v) for k, v in data.get("table_counts", {}).items()}
    except Exception:
        return {}



def run_startup_safety_checks(settings: Settings) -> SafetyReport:
    db_path = resolve_sqlite_path(settings.database_url).expanduser().resolve()
    warnings: list[str] = []
    counts: dict[str, int] = {}

    if not db_path.exists():
        warnings.append(f"Database file not found at startup: {db_path}")
    else:
        conn = sqlite3.connect(db_path)
        try:
            existing_tables = {
                row[0]
                for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            }
            for table in _REQUIRED_TABLES:
                if table not in existing_tables:
                    warnings.append(f"Required table missing: {table}")
                    counts[table] = 0
                    continue
                count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                counts[table] = int(count)
        finally:
            conn.close()

    var_dir = db_path.parent
    var_dir.mkdir(parents=True, exist_ok=True)
    state_path = var_dir / "startup_health_state.json"
    prev_counts = _load_prev_counts(state_path)

    for table in _REQUIRED_TABLES:
        prev = int(prev_counts.get(table, 0))
        curr = int(counts.get(table, 0))
        if prev > 0 and curr == 0:
            warnings.append(f"Regression detected: {table} dropped from {prev} to 0")

    timestamp = datetime.now(timezone.utc).isoformat()
    state_path.write_text(
        json.dumps({"timestamp": timestamp, "table_counts": counts}, indent=2),
        encoding="utf-8",
    )

    report = SafetyReport(
        db_path=str(db_path),
        warnings=warnings,
        table_counts=counts,
        timestamp=timestamp,
    )
    (var_dir / "startup_safety_report.json").write_text(
        json.dumps(report.to_dict(), indent=2),
        encoding="utf-8",
    )
    return report


def _snapshot_root(db_path: Path) -> Path:
    return db_path.parent / "snapshots"


_TIER_RE = re.compile(r"^[A-Za-z0-9_-]+$")


def _validate_tier(tier: str) -> str:
    """Reject tier values that aren't a single safe path component.

    Without this, ``tier="../../../tmp/x"`` would escape the snapshots dir and
    write a full DB copy to an arbitrary location (path traversal).
    """
    if not _TIER_RE.match(tier):
        raise ValueError(f"Invalid snapshot tier: {tier!r} (expected alphanumerics, '-' or '_')")
    return tier


def _ensure_within(root: Path, candidate: Path) -> Path:
    """Resolve ``candidate`` and confirm it lives inside ``root``.

    Guards the restore path so an attacker can't point it at an arbitrary file
    on disk (which would otherwise overwrite the live DB) or write outside the
    managed snapshots directory.
    """
    resolved = candidate.expanduser().resolve()
    root_resolved = root.expanduser().resolve()
    if not resolved.is_relative_to(root_resolved):
        raise ValueError(f"Path escapes the snapshots directory: {candidate}")
    return resolved


def create_snapshot(db_path: Path, *, tier: str = "manual") -> Path:
    _validate_tier(tier)
    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_dir = _snapshot_root(db_path) / tier
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"youos-{now}.db"

    conn = sqlite3.connect(db_path)
    try:
        conn.execute("PRAGMA wal_checkpoint(FULL)")
        backup_conn = sqlite3.connect(out_path)
        try:
            conn.backup(backup_conn)
        finally:
            backup_conn.close()
    finally:
        conn.close()

    return out_path


def _load_snapshot_retention(
    *,
    keep_hourly: int | None,
    keep_daily: int | None,
    keep_manual: int | None,
) -> tuple[int, int, int]:
    """Resolve retention limits from explicit args > config > historical defaults.

    Historical defaults: 72 hourly, 30 daily, 50 manual — preserved exactly
    so existing callers that don't pass kwargs see identical behaviour.
    YAML override key: ``snapshots: {keep_hourly: N, keep_daily: N, keep_manual: N}``.
    """
    cfg: dict[str, Any] = {}
    if keep_hourly is None or keep_daily is None or keep_manual is None:
        try:
            from app.core.config import load_config

            raw = load_config() or {}
            cfg = raw.get("snapshots", {}) if isinstance(raw, dict) else {}
            if not isinstance(cfg, dict):
                cfg = {}
        except Exception:
            cfg = {}

    def _resolve(arg: int | None, key: str, default: int) -> int:
        if arg is not None:
            return int(arg)
        val = cfg.get(key)
        if isinstance(val, int) and val >= 0:
            return val
        return default

    return (
        _resolve(keep_hourly, "keep_hourly", 72),
        _resolve(keep_daily, "keep_daily", 30),
        _resolve(keep_manual, "keep_manual", 50),
    )


def prune_snapshots(
    db_path: Path,
    *,
    keep_hourly: int | None = None,
    keep_daily: int | None = None,
    keep_manual: int | None = None,
) -> dict[str, int]:
    """Prune snapshots beyond per-tier retention limits.

    Returns a per-tier count of files removed so callers (the nightly,
    the CLI) can report what they did. Limits resolve from explicit
    kwargs > YAML config (``snapshots.keep_*``) > historical defaults
    (72 / 30 / 50). Existing callers that don't pass kwargs see exactly
    the same behaviour they always did.
    """
    hourly, daily, manual = _load_snapshot_retention(
        keep_hourly=keep_hourly, keep_daily=keep_daily, keep_manual=keep_manual,
    )
    root = _snapshot_root(db_path)
    removed: dict[str, int] = {"hourly": 0, "daily": 0, "manual": 0}
    for tier, keep in (("hourly", hourly), ("daily", daily), ("manual", manual)):
        tier_dir = root / tier
        if not tier_dir.exists():
            continue
        files = sorted(tier_dir.glob("youos-*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
        for old in files[keep:]:
            old.unlink(missing_ok=True)
            removed[tier] += 1
    return removed


def list_snapshots(db_path: Path) -> list[Path]:
    root = _snapshot_root(db_path)
    if not root.exists():
        return []
    files = sorted(root.glob("*/*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    return files


def restore_snapshot(db_path: Path, snapshot_path: Path, *, dry_run: bool = False) -> Path:
    # Only allow restoring from inside the managed snapshots directory. Without
    # this, an arbitrary path would let a caller overwrite the live DB with any
    # readable file on disk.
    snapshot_path = _ensure_within(_snapshot_root(db_path), snapshot_path)
    if not snapshot_path.exists():
        raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

    backup_path = db_path.parent / f"youos.pre-restore-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.db"
    if dry_run:
        return backup_path

    db_path.parent.mkdir(parents=True, exist_ok=True)
    if db_path.exists():
        # Use the SQLite backup API so the pre-restore copy is consistent even
        # when the DB is in WAL mode (a plain file copy can miss WAL contents).
        src = sqlite3.connect(db_path)
        try:
            dst = sqlite3.connect(backup_path)
            try:
                src.backup(dst)
            finally:
                dst.close()
        finally:
            src.close()
    shutil.copy2(snapshot_path, db_path)
    return backup_path
