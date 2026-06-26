from pathlib import Path

from sherpamind.ingest import sync_cold_closed_audit, sync_hot_open_tickets, sync_warm_closed_tickets
from sherpamind.settings import Settings
from sherpamind.sync_state import get_json_state
from sherpamind.db import connect


class FakeClient:
    def __init__(self, open_rows=None, closed_rows=None, closed_pages=None):
        self.open_rows = open_rows or []
        self.closed_rows = closed_rows or []
        self.closed_pages = closed_pages or {}

    def list_paginated(self, path, *, page_size=100, max_pages=None, extra_params=None):
        extra_params = extra_params or {}
        if extra_params.get("status") == "open":
            return self.open_rows
        if extra_params.get("status") == "closed":
            return self.closed_rows
        return []

    def get(self, path, params=None):
        params = params or {}
        return self.closed_pages.get(params.get("page"), [])


def make_settings(tmp_path: Path) -> Settings:
    return Settings(
        api_base_url="https://api.sherpadesk.com",
        api_key="secret",
        api_user=None,
        org_key="org",
        instance_key="inst",
        db_path=tmp_path / "sherpamind.sqlite3",
        watch_state_path=tmp_path / "watch_state.json",
        notify_channel=None,
        request_min_interval_seconds=0,
        request_timeout_seconds=30,
        seed_page_size=2,
        seed_max_pages=None,
        hot_open_pages=2,
        warm_closed_pages=2,
        warm_closed_days=7,
        cold_closed_pages_per_run=2,
        service_cold_bootstrap_every_seconds=1800,
        service_enrichment_bootstrap_every_seconds=900,
        service_enrichment_bootstrap_limit=240,
        cold_closed_bootstrap_pages_per_run=10,
    )


def test_sync_hot_open_tickets_persists_open_ids(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    rows = [{"id": 11, "subject": "Open", "status": "Open", "created_time": "2026-03-19T10:00:00", "updated_time": "2026-03-19T10:05:00"}]
    monkeypatch.setattr("sherpamind.ingest._build_client", lambda settings: FakeClient(open_rows=rows))
    result = sync_hot_open_tickets(settings)
    assert result.status == "ok"
    state = get_json_state(settings.db_path, "sync.hot_open.last_state")
    assert state["open_ticket_ids"] == [11]


def test_sync_warm_closed_filters_by_cutoff(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    rows = [
        {"id": 21, "subject": "Warm", "status": "Closed", "closed_time": "2999-03-18T10:00:00.0000000"},
        {"id": 22, "subject": "Cold", "status": "Closed", "closed_time": "2000-03-01T10:00:00.0000000"},
    ]
    monkeypatch.setattr("sherpamind.ingest._build_client", lambda settings: FakeClient(closed_rows=rows))
    result = sync_warm_closed_tickets(settings)
    assert result.status == "ok"
    assert result.stats["warm_ticket_count"] == 1
    with connect(settings.db_path) as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM tickets").fetchone()["c"]
    assert count == 1


def test_sync_cold_closed_audit_advances_page_pointer(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    fake = FakeClient(closed_pages={0: [{"id": 31, "subject": "Cold A", "status": "Closed"}, {"id": 32, "subject": "Cold B", "status": "Closed"}], 1: [{"id": 33, "subject": "Cold C", "status": "Closed"}]})
    monkeypatch.setattr("sherpamind.ingest._build_client", lambda settings: fake)
    result = sync_cold_closed_audit(settings)
    assert result.status == "ok"
    state = get_json_state(settings.db_path, "sync.cold_closed.last_state")
    assert state["start_page"] == 0
    assert state["next_page"] == 0
