import json
from pathlib import Path

from sherpamind.settings import Settings
from sherpamind.watch import watch_new_tickets


class FakeClient:
    def __init__(self, rows):
        self.rows = rows

    def list_paginated(self, path, *, page_size=100, max_pages=None, extra_params=None):
        return self.rows


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
        seed_page_size=100,
        seed_max_pages=None,
        hot_open_pages=3,
        warm_closed_pages=10,
        warm_closed_days=7,
        cold_closed_pages_per_run=2,
    )


def test_watch_new_tickets_tracks_new_and_removed_ids(tmp_path: Path, monkeypatch) -> None:
    settings = make_settings(tmp_path)
    settings.watch_state_path.write_text(json.dumps({"known_open_ticket_ids": [2, 3], "last_watch_at": None, "open_ticket_snapshot": {"2": {"updated_time": "old"}}}))
    rows = [
        {"id": 1, "subject": "New one", "account_name": "Acme", "created_time": "2026-03-19T10:00:00", "updated_time": "2026-03-19T10:01:00", "priority_name": "High", "status": "Open", "is_new_user_post": False, "is_new_tech_post": False, "next_step_date": None},
        {"id": 2, "subject": "Existing", "account_name": "Acme", "created_time": "2026-03-19T09:00:00", "updated_time": "2026-03-19T09:10:00", "priority_name": "Low", "status": "Open", "is_new_user_post": True, "is_new_tech_post": False, "next_step_date": None},
    ]
    monkeypatch.setattr("sherpamind.watch._build_client", lambda settings: FakeClient(rows))

    result = watch_new_tickets(settings)

    assert result.status == "ok"
    assert result.stats["new_ticket_count"] == 1
    assert result.stats["changed_open_ticket_count"] == 1
    assert result.stats["removed_open_ticket_count"] == 1
    assert result.stats["new_tickets"][0]["id"] == 1
    assert result.stats["changed_tickets"][0]["id"] == 2
    saved = json.loads(settings.watch_state_path.read_text())
    assert saved["known_open_ticket_ids"] == [1, 2]
