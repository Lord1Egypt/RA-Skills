"""Phase 3 tests: Admin Control Plane — tenants, policies, travelers, stats, auth."""

from __future__ import annotations

import os
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from zim.api import app
from zim.core import FlightResult, HotelResult, CarResult, Itinerary, Policy
from zim.policy_store import PolicyStore, StoredPolicy
from zim.ranking import ScoredResult
from zim.tenant import Tenant, TenantSettings
from zim.tenant_store import TenantStore
from zim.traveler_store import Traveler, TravelerStore


# ---------------------------------------------------------------------------
# Shared mock search data
# ---------------------------------------------------------------------------

_MOCK_FLIGHTS = [
    FlightResult(
        airline="TP", flight_number="TP101", origin="LIS", destination="CPH",
        price_usd=450.0, transfers=0, cabin="economy", link="https://example.com/f1",
        policy_status="approved",
    ),
]
_MOCK_HOTELS = [
    HotelResult(
        name="Hotel Copenhagen", location="Copenhagen",
        nightly_rate_usd=150.0, stars=4, link="https://example.com/h1",
        policy_status="approved",
    ),
]
_MOCK_CARS = [
    CarResult(
        provider="Hertz", vehicle_class="economy", pickup_location="CPH",
        price_usd_total=200.0, link="https://example.com/c1",
        free_cancellation=True, policy_status="approved",
    ),
]
_MOCK_ITINERARY = Itinerary(
    destination="CPH",
    mode="personal",
    dates={"departure": "2026-06-01", "return": "2026-06-05", "nights": 4},
    traveler_profile={"name": "default", "mode": "personal"},
    policy={},
    flights=_MOCK_FLIGHTS,
    hotels=_MOCK_HOTELS,
    cars=_MOCK_CARS,
    status="booking_ready",
    total_price_usd=1250.0,
)
_MOCK_SCORED = (
    _MOCK_ITINERARY,
    [ScoredResult(result=_MOCK_FLIGHTS[0], score=85.0, rank_reason="best price")],
    [ScoredResult(result=_MOCK_HOTELS[0], score=70.0, rank_reason="4 stars")],
    [ScoredResult(result=_MOCK_CARS[0], score=60.0, rank_reason="free cancel")],
)


def _mock_plan_trip(*args, **kwargs):
    return _MOCK_SCORED


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_all_stores(tmp_path):
    """Isolate every store with a fresh temp DB for each test."""
    import zim.api as api_module
    from zim.request_store import RequestStore
    from zim.trip_store import TripStore
    from zim.webhook_store import WebhookEventStore

    orig_store = api_module._store
    orig_trip = api_module._trip_store
    orig_webhook = api_module._webhook_store
    orig_tenant = api_module._tenant_store
    orig_policy = api_module._policy_store
    orig_traveler = api_module._traveler_store

    api_module._store = RequestStore(tmp_path / "requests.db")
    api_module._trip_store = TripStore(tmp_path / "trips.db")
    api_module._webhook_store = WebhookEventStore(tmp_path / "webhooks.db")
    api_module._tenant_store = TenantStore(tmp_path / "tenants.db")
    api_module._policy_store = PolicyStore(tmp_path / "policies.db")
    api_module._traveler_store = TravelerStore(tmp_path / "travelers.db")

    yield

    api_module._store = orig_store
    api_module._trip_store = orig_trip
    api_module._webhook_store = orig_webhook
    api_module._tenant_store = orig_tenant
    api_module._policy_store = orig_policy
    api_module._traveler_store = orig_traveler


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=True)


# ---------------------------------------------------------------------------
# Tenant model unit tests
# ---------------------------------------------------------------------------


class TestTenantModel:
    def test_default_id_generated(self):
        t = Tenant(name="Acme Corp")
        assert len(t.id) == 16
        assert t.name == "Acme Corp"
        assert t.is_deleted is False

    def test_default_settings(self):
        t = Tenant(name="Acme")
        assert t.settings.default_currency == "USD"
        assert t.settings.approval_required is False
        assert t.settings.default_policy_id is None

    def test_custom_settings(self):
        settings = TenantSettings(
            default_currency="EUR",
            approval_required=True,
            max_trip_budget_usd=5000.0,
        )
        t = Tenant(name="EuroTenant", settings=settings)
        assert t.settings.default_currency == "EUR"
        assert t.settings.approval_required is True


class TestTenantStore:
    def test_create_and_get(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        t = Tenant(name="Test Corp", domain="test.com")
        store.create(t)
        loaded = store.get(t.id)
        assert loaded is not None
        assert loaded.name == "Test Corp"
        assert loaded.domain == "test.com"

    def test_get_missing_returns_none(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        assert store.get("nonexistent") is None

    def test_update(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        t = Tenant(name="Old Name")
        store.create(t)
        t.name = "New Name"
        store.update(t)
        loaded = store.get(t.id)
        assert loaded.name == "New Name"

    def test_soft_delete(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        t = Tenant(name="To Delete")
        store.create(t)
        store.soft_delete(t.id)
        loaded = store.get(t.id)
        assert loaded.is_deleted is True

    def test_list_excludes_deleted_by_default(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        t1 = Tenant(name="Active")
        t2 = Tenant(name="Deleted")
        store.create(t1)
        store.create(t2)
        store.soft_delete(t2.id)

        active = store.list_tenants()
        assert len(active) == 1
        assert active[0].name == "Active"

    def test_list_includes_deleted_when_requested(self, tmp_path):
        store = TenantStore(tmp_path / "tenants.db")
        t1 = Tenant(name="Active")
        t2 = Tenant(name="Deleted")
        store.create(t1)
        store.create(t2)
        store.soft_delete(t2.id)

        all_tenants = store.list_tenants(include_deleted=True)
        assert len(all_tenants) == 2


# ---------------------------------------------------------------------------
# StoredPolicy model and PolicyStore unit tests
# ---------------------------------------------------------------------------


class TestPolicyStore:
    def test_create_and_get(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        sp = StoredPolicy(tenant_id="t1", name="Standard", policy=Policy(max_flight=1500.0))
        store.create(sp)
        loaded = store.get(sp.id)
        assert loaded is not None
        assert loaded.name == "Standard"
        assert loaded.policy.max_flight == 1500.0

    def test_get_missing_returns_none(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        assert store.get("nope") is None

    def test_update(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        sp = StoredPolicy(tenant_id="t1", name="Old")
        store.create(sp)
        sp.name = "New"
        store.update(sp)
        assert store.get(sp.id).name == "New"

    def test_soft_delete(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        sp = StoredPolicy(tenant_id="t1", name="Del")
        store.create(sp)
        store.soft_delete(sp.id)
        assert store.get(sp.id).is_deleted is True

    def test_list_by_tenant(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        store.create(StoredPolicy(tenant_id="t1", name="P1"))
        store.create(StoredPolicy(tenant_id="t1", name="P2"))
        store.create(StoredPolicy(tenant_id="t2", name="P3"))
        assert len(store.list_policies(tenant_id="t1")) == 2
        assert len(store.list_policies(tenant_id="t2")) == 1

    def test_list_excludes_deleted(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        sp = StoredPolicy(tenant_id="t1", name="Del")
        store.create(sp)
        store.soft_delete(sp.id)
        assert store.list_policies(tenant_id="t1") == []
        assert len(store.list_policies(tenant_id="t1", include_deleted=True)) == 1

    def test_get_default_for_tenant(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        sp1 = StoredPolicy(tenant_id="t1", name="Default", is_default=True)
        sp2 = StoredPolicy(tenant_id="t1", name="Other", is_default=False)
        store.create(sp1)
        store.create(sp2)
        default = store.get_default_for_tenant("t1")
        assert default is not None
        assert default.name == "Default"

    def test_get_default_returns_none_when_absent(self, tmp_path):
        store = PolicyStore(tmp_path / "policies.db")
        assert store.get_default_for_tenant("t1") is None


# ---------------------------------------------------------------------------
# TravelerStore unit tests
# ---------------------------------------------------------------------------


class TestTravelerStore:
    def test_create_and_get(self, tmp_path):
        store = TravelerStore(tmp_path / "travelers.db")
        t = Traveler(tenant_id="t1", name="Jane Doe", email="jane@example.com")
        store.create(t)
        loaded = store.get(t.id)
        assert loaded is not None
        assert loaded.name == "Jane Doe"
        assert loaded.email == "jane@example.com"

    def test_get_missing_returns_none(self, tmp_path):
        store = TravelerStore(tmp_path / "travelers.db")
        assert store.get("nope") is None

    def test_update(self, tmp_path):
        store = TravelerStore(tmp_path / "travelers.db")
        t = Traveler(tenant_id="t1", name="Old", email="old@test.com")
        store.create(t)
        t.email = "new@test.com"
        store.update(t)
        assert store.get(t.id).email == "new@test.com"

    def test_list_by_tenant(self, tmp_path):
        store = TravelerStore(tmp_path / "travelers.db")
        store.create(Traveler(tenant_id="t1", name="A", email="a@x.com"))
        store.create(Traveler(tenant_id="t1", name="B", email="b@x.com"))
        store.create(Traveler(tenant_id="t2", name="C", email="c@x.com"))
        assert len(store.list_travelers(tenant_id="t1")) == 2
        assert len(store.list_travelers(tenant_id="t2")) == 1

    def test_passport_info_stored(self, tmp_path):
        store = TravelerStore(tmp_path / "travelers.db")
        t = Traveler(
            tenant_id="t1", name="Jane", email="jane@test.com",
            passport_info={"first_name": "Jane", "last_name": "Doe", "passport_number": "AB123456"},
        )
        store.create(t)
        loaded = store.get(t.id)
        assert loaded.passport_info["passport_number"] == "AB123456"


# ---------------------------------------------------------------------------
# Admin API: Tenant CRUD
# ---------------------------------------------------------------------------


class TestAdminTenantAPI:
    def test_create_tenant(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "Acme Corp", "domain": "acme.com"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Acme Corp"
        assert data["domain"] == "acme.com"
        assert "id" in data
        assert data["is_deleted"] is False

    def test_create_tenant_with_settings(self, client):
        resp = client.post("/v1/admin/tenants", json={
            "name": "Big Corp",
            "settings": {"approval_required": True, "max_trip_budget_usd": 8000.0},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["settings"]["approval_required"] is True
        assert data["settings"]["max_trip_budget_usd"] == 8000.0

    def test_get_tenant(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "Foo"})
        tenant_id = resp.json()["id"]
        resp2 = client.get(f"/v1/admin/tenants/{tenant_id}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == tenant_id

    def test_get_tenant_not_found(self, client):
        resp = client.get("/v1/admin/tenants/nonexistent")
        assert resp.status_code == 404

    def test_list_tenants(self, client):
        client.post("/v1/admin/tenants", json={"name": "T1"})
        client.post("/v1/admin/tenants", json={"name": "T2"})
        resp = client.get("/v1/admin/tenants")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_update_tenant(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "Original"})
        tenant_id = resp.json()["id"]
        resp2 = client.put(f"/v1/admin/tenants/{tenant_id}", json={"name": "Updated"})
        assert resp2.status_code == 200
        assert resp2.json()["name"] == "Updated"

    def test_update_tenant_settings(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "T"})
        tenant_id = resp.json()["id"]
        resp2 = client.put(
            f"/v1/admin/tenants/{tenant_id}",
            json={"settings": {"default_currency": "GBP"}},
        )
        assert resp2.status_code == 200
        assert resp2.json()["settings"]["default_currency"] == "GBP"

    def test_delete_tenant(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "ToDelete"})
        tenant_id = resp.json()["id"]
        resp2 = client.delete(f"/v1/admin/tenants/{tenant_id}")
        assert resp2.status_code == 200
        assert resp2.json()["deleted"] is True
        # Should now be 404
        assert client.get(f"/v1/admin/tenants/{tenant_id}").status_code == 404

    def test_delete_tenant_not_found(self, client):
        resp = client.delete("/v1/admin/tenants/nope")
        assert resp.status_code == 404

    def test_list_excludes_deleted_by_default(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "Del"})
        tenant_id = resp.json()["id"]
        client.delete(f"/v1/admin/tenants/{tenant_id}")
        resp2 = client.get("/v1/admin/tenants")
        assert len(resp2.json()) == 0

    def test_list_includes_deleted_when_requested(self, client):
        resp = client.post("/v1/admin/tenants", json={"name": "Del"})
        tenant_id = resp.json()["id"]
        client.delete(f"/v1/admin/tenants/{tenant_id}")
        resp2 = client.get("/v1/admin/tenants?include_deleted=true")
        assert len(resp2.json()) == 1


# ---------------------------------------------------------------------------
# Admin API: Policy CRUD
# ---------------------------------------------------------------------------


class TestAdminPolicyAPI:
    def test_create_policy(self, client):
        resp = client.post("/v1/admin/policies", json={
            "tenant_id": "t1",
            "name": "Standard Policy",
            "policy": {"max_flight": 1500.0, "max_hotel_night": 200.0},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Standard Policy"
        assert data["tenant_id"] == "t1"
        assert data["policy"]["max_flight"] == 1500.0

    def test_create_default_policy(self, client):
        resp = client.post("/v1/admin/policies", json={
            "tenant_id": "t1",
            "name": "Default",
            "is_default": True,
            "policy": {},
        })
        assert resp.status_code == 201
        assert resp.json()["is_default"] is True

    def test_get_policy(self, client):
        resp = client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "P1"})
        policy_id = resp.json()["id"]
        resp2 = client.get(f"/v1/admin/policies/{policy_id}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == policy_id

    def test_get_policy_not_found(self, client):
        assert client.get("/v1/admin/policies/nope").status_code == 404

    def test_list_policies(self, client):
        client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "P1"})
        client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "P2"})
        client.post("/v1/admin/policies", json={"tenant_id": "t2", "name": "P3"})

        resp = client.get("/v1/admin/policies?tenant_id=t1")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_list_all_policies(self, client):
        client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "P1"})
        client.post("/v1/admin/policies", json={"tenant_id": "t2", "name": "P2"})
        resp = client.get("/v1/admin/policies")
        assert len(resp.json()) == 2

    def test_update_policy(self, client):
        resp = client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "Old"})
        policy_id = resp.json()["id"]
        resp2 = client.put(f"/v1/admin/policies/{policy_id}", json={
            "name": "New",
            "policy": {"max_flight": 999.0},
        })
        assert resp2.status_code == 200
        data = resp2.json()
        assert data["name"] == "New"
        assert data["policy"]["max_flight"] == 999.0

    def test_delete_policy(self, client):
        resp = client.post("/v1/admin/policies", json={"tenant_id": "t1", "name": "Del"})
        policy_id = resp.json()["id"]
        resp2 = client.delete(f"/v1/admin/policies/{policy_id}")
        assert resp2.status_code == 200
        assert resp2.json()["deleted"] is True
        assert client.get(f"/v1/admin/policies/{policy_id}").status_code == 404

    def test_delete_policy_not_found(self, client):
        assert client.delete("/v1/admin/policies/nope").status_code == 404

    def test_invalid_policy_body(self, client):
        resp = client.post("/v1/admin/policies", json={
            "tenant_id": "t1",
            "name": "Bad",
            "policy": {"max_flight": "not-a-number"},
        })
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Admin API: Traveler CRUD
# ---------------------------------------------------------------------------


class TestAdminTravelerAPI:
    def test_create_traveler(self, client):
        resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+1234567890",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Jane Doe"
        assert data["email"] == "jane@example.com"
        assert data["tenant_id"] == "t1"

    def test_create_traveler_with_passport(self, client):
        resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "John",
            "email": "john@x.com",
            "passport_info": {
                "first_name": "John",
                "last_name": "Smith",
                "passport_number": "AB123456",
            },
        })
        assert resp.status_code == 201
        assert resp.json()["passport_info"]["passport_number"] == "AB123456"

    def test_create_traveler_with_preferences(self, client):
        resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "Alice",
            "email": "alice@x.com",
            "preferences": {"seat": "window", "no_red_eye": True, "hotel_stars_min": 4},
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["preferences"]["seat"] == "window"
        assert data["preferences"]["no_red_eye"] is True

    def test_get_traveler(self, client):
        resp = client.post("/v1/admin/travelers", json={"tenant_id": "t1", "name": "A", "email": "a@x.com"})
        tid = resp.json()["id"]
        resp2 = client.get(f"/v1/admin/travelers/{tid}")
        assert resp2.status_code == 200
        assert resp2.json()["id"] == tid

    def test_get_traveler_not_found(self, client):
        assert client.get("/v1/admin/travelers/nope").status_code == 404

    def test_list_travelers(self, client):
        client.post("/v1/admin/travelers", json={"tenant_id": "t1", "name": "A", "email": "a@x.com"})
        client.post("/v1/admin/travelers", json={"tenant_id": "t1", "name": "B", "email": "b@x.com"})
        client.post("/v1/admin/travelers", json={"tenant_id": "t2", "name": "C", "email": "c@x.com"})
        resp = client.get("/v1/admin/travelers?tenant_id=t1")
        assert len(resp.json()) == 2

    def test_update_traveler(self, client):
        resp = client.post("/v1/admin/travelers", json={"tenant_id": "t1", "name": "Old", "email": "old@x.com"})
        tid = resp.json()["id"]
        resp2 = client.put(f"/v1/admin/travelers/{tid}", json={"name": "New", "email": "new@x.com"})
        assert resp2.status_code == 200
        assert resp2.json()["email"] == "new@x.com"

    def test_update_traveler_passport(self, client):
        resp = client.post("/v1/admin/travelers", json={"tenant_id": "t1", "name": "A", "email": "a@x.com"})
        tid = resp.json()["id"]
        resp2 = client.put(f"/v1/admin/travelers/{tid}", json={
            "passport_info": {"passport_number": "XY999"}
        })
        assert resp2.status_code == 200
        assert resp2.json()["passport_info"]["passport_number"] == "XY999"

    def test_update_traveler_not_found(self, client):
        assert client.put("/v1/admin/travelers/nope", json={"name": "X"}).status_code == 404

    def test_invalid_preferences(self, client):
        resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "Bad",
            "email": "bad@x.com",
            "preferences": {"hotel_stars_min": "not-an-int"},
        })
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Admin API: Stats
# ---------------------------------------------------------------------------


class TestAdminStats:
    def test_stats_empty(self, client):
        resp = client.get("/v1/admin/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_requests"] == 0
        assert data["total_trips_completed"] == 0
        assert data["total_spend_usd"] == 0.0
        assert data["requests_last_7_days"] == 0
        assert data["requests_last_30_days"] == 0
        assert data["top_destinations"] == []

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_stats_with_data(self, mock_search, client):
        # Create a request
        resp = client.post("/v1/requests", json={
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
                "return_date": "2026-06-05",
            },
        })
        assert resp.status_code == 201

        stats = client.get("/v1/admin/stats").json()
        assert stats["total_requests"] == 1
        assert "options_ready" in stats["requests_by_state"]
        assert stats["requests_last_7_days"] == 1
        assert stats["requests_last_30_days"] == 1

    def test_stats_tenant_filter(self, client):
        # Create requests for different tenants directly in store
        import zim.api as api_module
        from zim.request_state import TravelRequest
        req1 = TravelRequest(tenant_id="t1", traveler_id="default")
        req2 = TravelRequest(tenant_id="t2", traveler_id="default")
        api_module._store.create(req1)
        api_module._store.create(req2)

        stats_t1 = client.get("/v1/admin/stats?tenant_id=t1").json()
        assert stats_t1["total_requests"] == 1

        stats_all = client.get("/v1/admin/stats").json()
        assert stats_all["total_requests"] == 2

    def test_stats_top_destinations(self, client):
        import zim.api as api_module
        from zim.trip_store import TripRecord
        for dest in ["CPH", "CPH", "NYC", "LHR"]:
            api_module._trip_store.create(TripRecord(
                request_id=f"req-{dest}-{id(dest)}",
                tenant_id="t1",
                traveler_id="default",
                destination=dest,
                total_cost=1000.0,
            ))

        stats = client.get("/v1/admin/stats").json()
        assert stats["top_destinations"][0]["destination"] == "CPH"
        assert stats["top_destinations"][0]["count"] == 2

    def test_stats_spend(self, client):
        import zim.api as api_module
        from zim.trip_store import TripRecord
        api_module._trip_store.create(TripRecord(
            request_id="req1", tenant_id="t1", traveler_id="d",
            destination="NYC", total_cost=1500.0,
        ))
        api_module._trip_store.create(TripRecord(
            request_id="req2", tenant_id="t1", traveler_id="d",
            destination="LHR", total_cost=2500.0,
        ))
        stats = client.get("/v1/admin/stats").json()
        assert stats["total_spend_usd"] == 4000.0
        assert stats["total_trips_completed"] == 2


# ---------------------------------------------------------------------------
# Admin Auth
# ---------------------------------------------------------------------------


class TestAdminAuth:
    def test_admin_key_required_when_set(self, client):
        with patch.dict(os.environ, {"ZIM_ADMIN_KEY": "secret-admin"}):
            resp = client.post("/v1/admin/tenants", json={"name": "T"})
            assert resp.status_code == 401

    def test_admin_key_accepted(self, client):
        with patch.dict(os.environ, {"ZIM_ADMIN_KEY": "secret-admin"}):
            resp = client.post(
                "/v1/admin/tenants",
                json={"name": "T"},
                headers={"Authorization": "Bearer secret-admin"},
            )
            assert resp.status_code == 201

    def test_wrong_admin_key_rejected(self, client):
        with patch.dict(os.environ, {"ZIM_ADMIN_KEY": "secret-admin"}):
            resp = client.post(
                "/v1/admin/tenants",
                json={"name": "T"},
                headers={"Authorization": "Bearer wrong-key"},
            )
            assert resp.status_code == 401

    def test_admin_falls_back_to_api_key(self, client):
        """When ZIM_ADMIN_KEY is not set, admin routes accept ZIM_API_KEY."""
        env = {"ZIM_API_KEY": "api-key"}
        # Clear ZIM_ADMIN_KEY if it's set
        env_without_admin = {k: v for k, v in os.environ.items() if k != "ZIM_ADMIN_KEY"}
        env_without_admin["ZIM_API_KEY"] = "api-key"
        with patch.dict(os.environ, env_without_admin, clear=True):
            resp = client.post(
                "/v1/admin/tenants",
                json={"name": "T"},
                headers={"Authorization": "Bearer api-key"},
            )
            assert resp.status_code == 201

    def test_admin_key_does_not_affect_regular_routes(self, client):
        """Regular routes still accept ZIM_API_KEY when ZIM_ADMIN_KEY is set."""
        with patch.dict(os.environ, {"ZIM_ADMIN_KEY": "admin-key", "ZIM_API_KEY": "api-key"}):
            resp = client.get(
                "/v1/requests",
                headers={"Authorization": "Bearer api-key"},
            )
            assert resp.status_code == 200

    def test_admin_key_rejected_on_regular_route(self, client):
        """Admin key alone should not work for regular routes when API key is set."""
        with patch.dict(os.environ, {"ZIM_ADMIN_KEY": "admin-key", "ZIM_API_KEY": "api-key"}):
            resp = client.get(
                "/v1/requests",
                headers={"Authorization": "Bearer admin-key"},
            )
            assert resp.status_code == 401

    def test_no_auth_required_when_no_keys_set(self, client):
        env_without_keys = {
            k: v for k, v in os.environ.items()
            if k not in ("ZIM_API_KEY", "ZIM_ADMIN_KEY")
        }
        with patch.dict(os.environ, env_without_keys, clear=True):
            resp = client.post("/v1/admin/tenants", json={"name": "T"})
            assert resp.status_code == 201


# ---------------------------------------------------------------------------
# Policy wiring into request creation
# ---------------------------------------------------------------------------


class TestPolicyWiring:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_tenant_default_policy_applied_to_request(self, mock_search, client):
        """When a tenant has a default policy, it is stored in request metadata."""
        # Create policy
        pol_resp = client.post("/v1/admin/policies", json={
            "tenant_id": "corp",
            "name": "Corporate",
            "is_default": True,
            "policy": {"max_flight": 800.0, "approval_required": False},
        })
        pol_id = pol_resp.json()["id"]

        # Create tenant pointing to that policy
        tenant_resp = client.post("/v1/admin/tenants", json={
            "name": "Corp",
            "settings": {"default_policy_id": pol_id},
        })
        tenant_id = tenant_resp.json()["id"]

        # Create a request for that tenant
        resp = client.post("/v1/requests", json={
            "tenant_id": tenant_id,
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
            "auto_search": False,
        })
        assert resp.status_code == 201
        data = resp.json()
        # Policy should be embedded in metadata
        assert "_tenant_policy" in data["metadata"]
        assert data["metadata"]["_tenant_policy"]["max_flight"] == 800.0

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_no_policy_wired_for_default_tenant(self, mock_search, client):
        """Requests with tenant_id='default' skip policy lookup."""
        resp = client.post("/v1/requests", json={
            "tenant_id": "default",
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
            "auto_search": False,
        })
        assert resp.status_code == 201
        assert "_tenant_policy" not in resp.json()["metadata"]


# ---------------------------------------------------------------------------
# Traveler wiring into request creation
# ---------------------------------------------------------------------------


class TestTravelerWiring:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_stored_traveler_info_auto_populated(self, mock_search, client):
        """When traveler_id matches a stored traveler, traveler_info is pre-filled."""
        # Create traveler
        trav_resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "+1234567890",
            "passport_info": {
                "first_name": "Jane",
                "last_name": "Doe",
                "passport_number": "AB123456",
            },
        })
        traveler_id = trav_resp.json()["id"]

        # Create request using that traveler_id
        resp = client.post("/v1/requests", json={
            "traveler_id": traveler_id,
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
            "auto_search": False,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["traveler_info"] is not None
        assert data["traveler_info"]["first_name"] == "Jane"
        assert data["traveler_info"]["passport_number"] == "AB123456"
        assert data["traveler_info"]["email"] == "jane@example.com"

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_default_traveler_id_skips_lookup(self, mock_search, client):
        """traveler_id='default' does not trigger directory lookup."""
        resp = client.post("/v1/requests", json={
            "traveler_id": "default",
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
            "auto_search": False,
        })
        assert resp.status_code == 201
        # traveler_info should be empty (not auto-populated from a non-existent default traveler)
        data = resp.json()
        assert not data.get("traveler_info")

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_frequent_flyer_auto_populated(self, mock_search, client):
        """Frequent flyer numbers are propagated from the traveler directory."""
        trav_resp = client.post("/v1/admin/travelers", json={
            "tenant_id": "t1",
            "name": "FF Traveler",
            "email": "ff@example.com",
            "frequent_flyer": {"TP": "FF123456"},
        })
        traveler_id = trav_resp.json()["id"]

        resp = client.post("/v1/requests", json={
            "traveler_id": traveler_id,
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
            "auto_search": False,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["traveler_info"]["frequent_flyer"]["TP"] == "FF123456"
