"""Workspace schema versions and the migration between them.

An update of the skill may need a newer workspace layout. ``migrate`` backs the workspace up, runs
the steps in order, and puts everything back if any step fails. Running it again is a no-op.
"""

from __future__ import annotations

import shutil
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from tn_assist.config import SCHEMA_VERSION, load_config, save_config
from tn_assist.paths import Workspace
from tn_assist.timeutil import utc_iso

Step = Callable[[Workspace], None]
MIGRATIONS: dict[int, Step] = {}  # from-version -> function that produces from-version + 1


class WorkspaceTooNew(Exception):
    """The workspace was written by a newer skill; this one must not touch it."""


class MigrationFailed(Exception):
    """A step failed; the workspace was restored."""


@dataclass(frozen=True)
class MigrationReport:
    from_version: int
    to_version: int
    backup: Path | None


def _snapshot_name(now: datetime, version: int) -> str:
    return f"{utc_iso(now).replace(':', '').replace('-', '')}-schema{version}"


def _restore(ws: Workspace, backup: Path) -> None:
    for entry in ws.root.iterdir():
        if entry.name == "backup":
            continue
        shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    for entry in backup.iterdir():
        target = ws.root / entry.name
        shutil.copytree(entry, target) if entry.is_dir() else shutil.copy2(entry, target)


def migrate(
    ws: Workspace,
    *,
    now: datetime,
    backup: bool = True,
    target: int = SCHEMA_VERSION,
    migrations: Mapping[int, Step] | None = None,
) -> MigrationReport:
    steps = MIGRATIONS if migrations is None else migrations
    current = int(load_config(ws).get("schema", 1))
    if current > target:
        raise WorkspaceTooNew(f"workspace schema {current} is newer than {target}")
    if current == target:
        return MigrationReport(current, current, None)
    saved: Path | None = None
    if backup:
        saved = ws.root / "backup" / _snapshot_name(now, current)
        saved.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        shutil.copytree(
            ws.root, saved, ignore=shutil.ignore_patterns("backup"), copy_function=shutil.copy2
        )
    try:
        version = current
        while version < target:
            step = steps.get(version)
            if step is None:
                raise MigrationFailed(f"no migration from schema {version}")
            step(ws)
            version += 1
            config = load_config(ws)
            config["schema"] = version
            save_config(ws, config)
    except Exception as error:
        if saved is not None:
            _restore(ws, saved)
        raise MigrationFailed(str(error)) from error
    return MigrationReport(current, target, saved)
