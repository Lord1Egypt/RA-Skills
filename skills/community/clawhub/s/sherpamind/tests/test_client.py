import base64
from pathlib import Path

from sherpamind.client import SherpaDeskClient
from sherpamind.db import connect, initialize_db


def test_build_headers_uses_basic_auth_for_org_instance() -> None:
    client = SherpaDeskClient(
        api_base_url="https://api.sherpadesk.com",
        api_key="secret",
        org_key="org1",
        instance_key="main1",
        min_interval_seconds=0,
    )
    headers = client._build_headers()
    expected = base64.b64encode(b"org1-main1:secret").decode("ascii")
    assert headers["Authorization"] == f"Basic {expected}"
    assert headers["Accept"] == "application/json"


def test_build_headers_can_use_discovery_identity() -> None:
    client = SherpaDeskClient(
        api_base_url="https://api.sherpadesk.com",
        api_key="secret",
        min_interval_seconds=0,
    )
    headers = client._build_headers()
    expected = base64.b64encode(b"x:secret").decode("ascii")
    assert headers["Authorization"] == f"Basic {expected}"


def test_build_url_normalizes_slashes() -> None:
    client = SherpaDeskClient(
        api_base_url="https://api.sherpadesk.com/",
        api_key="secret",
        min_interval_seconds=0,
    )
    assert client._build_url("/tickets") == "https://api.sherpadesk.com/tickets"


def test_list_paginated_aggregates_pages() -> None:
    client = SherpaDeskClient(api_base_url="https://api.sherpadesk.com", api_key="secret", min_interval_seconds=0)
    seen = []

    def fake_get(path, params=None):
        seen.append((path, params))
        if params["page"] == 0:
            return [{"id": 1}, {"id": 2}]
        return [{"id": 3}]

    client.get = fake_get  # type: ignore[method-assign]
    rows = client.list_paginated("tickets", page_size=2)
    assert [row["id"] for row in rows] == [1, 2, 3]
    assert seen[0][1] == {"limit": 2, "page": 0}
    assert seen[1][1] == {"limit": 2, "page": 1}


def test_client_request_tracking_records_http_responses(tmp_path: Path, monkeypatch) -> None:
    db = tmp_path / "requests.sqlite3"
    initialize_db(db)
    client = SherpaDeskClient(
        api_base_url="https://api.sherpadesk.com",
        api_key="secret",
        min_interval_seconds=0,
        request_tracking_db_path=db,
    )

    class FakeResponse:
        status_code = 200
        headers = {"content-type": "application/json"}

        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": True}

    class FakeHttpClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def get(self, url, params=None):
            return FakeResponse()

    monkeypatch.setattr("sherpamind.client.httpx.Client", FakeHttpClient)
    result = client.get("tickets", params={"limit": 1})
    assert result == {"ok": True}
    with connect(db) as conn:
        row = conn.execute("SELECT method, path, status_code, outcome FROM api_request_events ORDER BY id DESC LIMIT 1").fetchone()
    assert row["method"] == "GET"
    assert row["path"] == "tickets"
    assert row["status_code"] == 200
    assert row["outcome"] == "http_response"
