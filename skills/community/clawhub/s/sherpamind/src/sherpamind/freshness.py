from __future__ import annotations

from pathlib import Path

from .db import connect


def get_sync_freshness(db_path: Path) -> dict:
    with connect(db_path) as conn:
        latest_runs = {}
        for mode in [
            'seed',
            'sync_hot_open',
            'sync_warm_closed',
            'sync_cold_closed_audit',
            'enrich_priority_ticket_details',
        ]:
            row = conn.execute(
                "SELECT mode, status, started_at, finished_at, notes FROM ingest_runs WHERE mode = ? ORDER BY id DESC LIMIT 1",
                (mode,),
            ).fetchone()
            latest_runs[mode] = dict(row) if row else None
    return latest_runs
