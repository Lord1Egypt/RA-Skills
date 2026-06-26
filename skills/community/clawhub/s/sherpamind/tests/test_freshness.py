from pathlib import Path

from sherpamind.db import initialize_db, start_ingest_run, finish_ingest_run
from sherpamind.freshness import get_sync_freshness


def test_get_sync_freshness_returns_latest_runs(tmp_path: Path) -> None:
    db = tmp_path / 'sherpamind.sqlite3'
    initialize_db(db)
    run_id = start_ingest_run(db, mode='sync_hot_open', notes='test')
    finish_ingest_run(db, run_id, status='success', notes='done')
    freshness = get_sync_freshness(db)
    assert freshness['sync_hot_open']['status'] == 'success'
    assert freshness['sync_hot_open']['notes'] == 'done'
