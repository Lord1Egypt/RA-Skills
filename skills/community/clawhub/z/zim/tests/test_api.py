"""Tests for the Zim FastAPI middleware API."""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from zim.api import app, _store
from zim.core import FlightResult, HotelResult, CarResult, Itinerary
from zim.ranking import ScoredResult
from zim.request_state import RequestState, TravelRequest


@pytest.fixture(autouse=True)
def clean_store(tmp_path):
    """Use a fresh temp DB for each test."""
    from zim.request_store import RequestStore
    import zim.api as api_module
    original = api_module._store
    api_module._store = RequestStore(db_path=tmp_path / "test_requests.db")
    yield
    api_module._store = original


@pytest.fixture
def client():
    return TestClient(app)


# Fixture data for mocked search results
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

_MOCK_SCORED_FLIGHTS = [ScoredResult(result=_MOCK_FLIGHTS[0], score=85.0, rank_reason="best price")]
_MOCK_SCORED_HOTELS = [ScoredResult(result=_MOCK_HOTELS[0], score=70.0, rank_reason="4 stars")]
_MOCK_SCORED_CARS = [ScoredResult(result=_MOCK_CARS[0], score=60.0, rank_reason="free cancel")]


def _mock_plan_trip(*args, **kwargs):
    return _MOCK_ITINERARY, _MOCK_SCORED_FLIGHTS, _MOCK_SCORED_HOTELS, _MOCK_SCORED_CARS


class TestHealth:
    def test_health(self, client):
        resp = client.get("/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestCreateRequest:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_create_with_structured_intent(self, mock_search, client):
        resp = client.post("/v1/requests", json={
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
                "return_date": "2026-06-05",
            },
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["state"] == "options_ready"
        assert data["itinerary"] is not None
        assert data["itinerary"]["destination"] == "CPH"

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_create_with_raw_message(self, mock_search, client):
        resp = client.post("/v1/requests", json={
            "raw_message": "Find me a flight from Lisbon to Copenhagen on June 1 returning June 5",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["raw_message"] is not None

    def test_create_no_intent_or_message(self, client):
        resp = client.post("/v1/requests", json={})
        assert resp.status_code == 422

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_create_no_auto_search(self, mock_search, client):
        resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
            "auto_search": False,
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["state"] == "intent_received"
        mock_search.assert_not_called()


class TestGetRequest:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_get_existing(self, mock_search, client):
        create_resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        rid = create_resp.json()["id"]

        resp = client.get(f"/v1/requests/{rid}")
        assert resp.status_code == 200
        assert resp.json()["id"] == rid

    def test_get_not_found(self, client):
        resp = client.get("/v1/requests/nonexistent")
        assert resp.status_code == 404


class TestListRequests:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_list_all(self, mock_search, client):
        client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        resp = client.get("/v1/requests")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_list_filter_by_tenant(self, mock_search, client):
        client.post("/v1/requests", json={
            "tenant_id": "acme",
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        resp = client.get("/v1/requests?tenant_id=acme")
        assert resp.status_code == 200
        for r in resp.json():
            assert r["tenant_id"] == "acme"


class TestSelectOptions:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_select_options(self, mock_search, client):
        create_resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        rid = create_resp.json()["id"]

        resp = client.post(f"/v1/requests/{rid}/select", json={"flight_index": 0})
        assert resp.status_code == 200
        data = resp.json()
        assert data["selected_options"]["flight_index"] == 0
        # Should advance past option_selected — traveler info missing so awaiting_info
        assert data["state"] in ("awaiting_info", "ready_to_execute", "awaiting_approval")

    def test_select_wrong_state(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.INTENT_RECEIVED)
        api_module._store.create(req)

        resp = client.post(f"/v1/requests/{req.id}/select", json={"flight_index": 0})
        assert resp.status_code == 409


class TestCancel:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_cancel(self, mock_search, client):
        create_resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        rid = create_resp.json()["id"]

        resp = client.post(f"/v1/requests/{rid}/cancel")
        assert resp.status_code == 200
        assert resp.json()["state"] == "cancelled"

    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan_trip)
    def test_cancel_already_cancelled(self, mock_search, client):
        create_resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
        rid = create_resp.json()["id"]
        client.post(f"/v1/requests/{rid}/cancel")

        resp = client.post(f"/v1/requests/{rid}/cancel")
        assert resp.status_code == 409
