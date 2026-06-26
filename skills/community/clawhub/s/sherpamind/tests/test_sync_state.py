from pathlib import Path

from sherpamind.db import initialize_db
from sherpamind.sync_state import get_json_state, get_sync_state, set_json_state, set_sync_state


def test_sync_state_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / 'sherpamind.sqlite3'
    initialize_db(db)
    assert get_sync_state(db, 'tickets.updated_after') is None
    set_sync_state(db, 'tickets.updated_after', '2026-03-19T00:00:00Z')
    assert get_sync_state(db, 'tickets.updated_after') == '2026-03-19T00:00:00Z'


def test_json_state_roundtrip(tmp_path: Path) -> None:
    db = tmp_path / 'sherpamind.sqlite3'
    initialize_db(db)
    set_json_state(db, 'watch.last_state', {'open_ids': [1, 2, 3]})
    assert get_json_state(db, 'watch.last_state') == {'open_ids': [1, 2, 3]}
