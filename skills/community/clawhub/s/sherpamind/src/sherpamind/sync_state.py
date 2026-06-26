from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .db import connect


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_sync_state(db_path: Path, key: str) -> str | None:
    with connect(db_path) as conn:
        row = conn.execute('SELECT value FROM sync_state WHERE key = ?', (key,)).fetchone()
        return row['value'] if row else None


def set_sync_state(db_path: Path, key: str, value: str) -> None:
    with connect(db_path) as conn:
        conn.execute(
            '''
            INSERT INTO sync_state(key, value, updated_at)
            VALUES(?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            ''',
            (key, value, now_iso())
        )
        conn.commit()


def get_json_state(db_path: Path, key: str, default: Any = None) -> Any:
    raw = get_sync_state(db_path, key)
    if raw is None:
        return default
    return json.loads(raw)


def set_json_state(db_path: Path, key: str, value: Any) -> None:
    set_sync_state(db_path, key, json.dumps(value, sort_keys=True))
