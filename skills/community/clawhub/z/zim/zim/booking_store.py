"""Booking state persistence for Zim.

Stores booking records as JSON files in ~/.config/zim/bookings/.
Each booking has a unique ID and tracks the full state machine lifecycle.
"""

from __future__ import annotations

import json
import logging
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)

BOOKINGS_DIR = Path.home() / ".config" / "zim" / "bookings"


def _ensure_dir(directory: Path | None = None) -> Path:
    d = directory or BOOKINGS_DIR
    d.mkdir(parents=True, exist_ok=True)
    return d


def _booking_path(booking_id: str, directory: Path | None = None) -> Path:
    return _ensure_dir(directory) / f"{booking_id}.json"


def _atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=path.parent, suffix=".tmp", prefix=path.stem,
    )
    try:
        with open(tmp_fd, "w") as f:
            json.dump(data, f, indent=2, default=str)
        Path(tmp_path).replace(path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise


def save_booking(record: dict[str, Any], directory: Path | None = None) -> str:
    """Save a booking record. Returns the booking_id."""
    booking_id = record["booking_id"]
    now = datetime.now(UTC).isoformat()

    if "created_at" not in record:
        record["created_at"] = now
    record["updated_at"] = now

    path = _booking_path(booking_id, directory)
    _atomic_write(path, record)
    logger.info("Saved booking %s to %s", booking_id, path)
    return booking_id


def load_booking(booking_id: str, directory: Path | None = None) -> dict[str, Any] | None:
    """Load a booking record. Returns None if not found."""
    path = _booking_path(booking_id, directory)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Failed to load booking %s: %s", booking_id, exc)
        return None


def update_booking_field(
    booking_id: str,
    updates: dict[str, Any],
    directory: Path | None = None,
) -> bool:
    """Update specific fields on a booking record. Returns False if not found."""
    record = load_booking(booking_id, directory)
    if record is None:
        return False

    record.update(updates)
    record["updated_at"] = datetime.now(UTC).isoformat()

    path = _booking_path(booking_id, directory)
    _atomic_write(path, record)
    logger.info("Updated booking %s fields: %s", booking_id, list(updates.keys()))
    return True


def list_bookings(directory: Path | None = None) -> list[dict[str, Any]]:
    """List all booking records, sorted by updated_at descending."""
    d = _ensure_dir(directory)
    records: list[dict[str, Any]] = []
    for p in d.glob("*.json"):
        try:
            records.append(json.loads(p.read_text()))
        except Exception:
            continue
    records.sort(key=lambda r: r.get("updated_at", ""), reverse=True)
    return records
