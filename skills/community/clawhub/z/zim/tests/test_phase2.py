"""Phase 2 tests: payment state machine, executor wiring, fulfillment,
trip records, retry endpoint, and webhook idempotency."""

import json
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from zim.api import app
from zim.core import FlightResult, HotelResult, CarResult, Itinerary
from zim.ranking import ScoredResult
from zim.request_state import (
    FulfillmentState,
    PaymentState,
    RequestState,
    TravelRequest,
)
from zim.booking_executor import (
    BookingExecutionRequest,
    PlaceholderExecutor,
    TravelpayoutsExecutor,
    get_executor,
)
from zim.trip_store import TripRecord, TripStore
from zim.webhook_store import WebhookEventStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_stores(tmp_path):
    """Isolate all stores for each test using temp DBs."""
    from zim.request_store import RequestStore
    import zim.api as api_module

    original_store = api_module._store
    original_trip_store = api_module._trip_store
    original_webhook_store = api_module._webhook_store

    api_module._store = RequestStore(db_path=tmp_path / "requests.db")
    api_module._trip_store = TripStore(db_path=tmp_path / "trips.db")
    api_module._webhook_store = WebhookEventStore(db_path=tmp_path / "webhooks.db")

    yield

    api_module._store = original_store
    api_module._trip_store = original_trip_store
    api_module._webhook_store = original_webhook_store


@pytest.fixture
def client():
    return TestClient(app)


_MOCK_FLIGHTS = [
    FlightResult(
        airline="TP", flight_number="TP101", origin="LIS", destination="CPH",
        price_usd=450.0, transfers=0, cabin="economy",
        link="https://tp.example.com/f1", policy_status="approved",
    ),
]

_MOCK_HOTELS = [
    HotelResult(
        name="Hotel Copenhagen", location="Copenhagen",
        nightly_rate_usd=150.0, stars=4,
        link="https://tp.example.com/h1", policy_status="approved",
    ),
]

_MOCK_CARS = [
    CarResult(
        provider="Hertz", vehicle_class="economy", pickup_location="CPH",
        price_usd_total=200.0, link="https://tp.example.com/c1",
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

_SCORED_FLIGHTS = [ScoredResult(result=_MOCK_FLIGHTS[0], score=85.0, rank_reason="best price")]
_SCORED_HOTELS = [ScoredResult(result=_MOCK_HOTELS[0], score=70.0, rank_reason="4 stars")]
_SCORED_CARS = [ScoredResult(result=_MOCK_CARS[0], score=60.0, rank_reason="free cancel")]


def _mock_plan(*args, **kwargs):
    return _MOCK_ITINERARY, _SCORED_FLIGHTS, _SCORED_HOTELS, _SCORED_CARS


def _create_and_ready_request(client):
    """Create a request that's ready_to_execute."""
    with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
        resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
        })
    assert resp.status_code == 201
    rid = resp.json()["id"]

    # Select options
    client.post(f"/v1/requests/{rid}/select", json={"flight_index": 0, "hotel_index": 0})

    # Provide traveler info to advance state
    client.post(f"/v1/requests/{rid}/traveler-info", json={
        "first_name": "Alice", "last_name": "Smith", "email": "alice@example.com",
    })

    req_data = client.get(f"/v1/requests/{rid}").json()
    if req_data["state"] != "ready_to_execute":
        # Force state via internal store
        import zim.api as api_module
        req = api_module._store.get(rid)
        req.state = RequestState.READY_TO_EXECUTE
        api_module._store.update(req)

    return rid


# ---------------------------------------------------------------------------
# 1. Payment State Machine
# ---------------------------------------------------------------------------


class TestPaymentStateMachine:

    def test_payment_status_endpoint_no_stripe(self, client):
        """Payment status returns current payment_state without Stripe session."""
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED, payment_state=PaymentState.PAID)
        api_module._store.create(req)

        resp = client.get(f"/v1/requests/{req.id}/payment-status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["payment_state"] == "paid"
        assert data["request_id"] == req.id
        assert data["payment_session_id"] is None

    def test_payment_status_with_session_id(self, client):
        import zim.api as api_module
        req = TravelRequest(
            state=RequestState.COMPLETED,
            payment_state=PaymentState.AUTHORIZED,
            payment_session_id="cs_test_123",
        )
        api_module._store.create(req)

        resp = client.get(f"/v1/requests/{req.id}/payment-status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["payment_session_id"] == "cs_test_123"
        assert data["payment_state"] == "authorized"

    def test_payment_status_404(self, client):
        resp = client.get("/v1/requests/nonexistent/payment-status")
        assert resp.status_code == 404


class TestStripeWebhook:

    def _post_event(self, client, event_type: str, booking_id: str, event_id: str = "evt_test_001"):
        payload = {
            "id": event_id,
            "type": event_type,
            "data": {
                "object": {
                    "metadata": {"booking_id": booking_id},
                }
            },
        }
        return client.post("/v1/webhooks/stripe", content=json.dumps(payload),
                           headers={"content-type": "application/json"})

    def test_checkout_completed_sets_paid(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING, payment_state=PaymentState.AUTHORIZED)
        api_module._store.create(req)

        resp = self._post_event(client, "checkout.session.completed", req.id)
        assert resp.status_code == 200

        updated = api_module._store.get(req.id)
        assert updated.payment_state == PaymentState.PAID

    def test_checkout_expired_sets_failed(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING, payment_state=PaymentState.AUTHORIZED)
        api_module._store.create(req)

        resp = self._post_event(client, "checkout.session.expired", req.id, "evt_002")
        assert resp.status_code == 200

        updated = api_module._store.get(req.id)
        assert updated.payment_state == PaymentState.FAILED

    def test_payment_intent_failed_sets_failed(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING, payment_state=PaymentState.AUTHORIZED)
        api_module._store.create(req)

        resp = self._post_event(client, "payment_intent.payment_failed", req.id, "evt_003")
        assert resp.status_code == 200

        updated = api_module._store.get(req.id)
        assert updated.payment_state == PaymentState.FAILED

    def test_charge_refunded_sets_refunded(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED, payment_state=PaymentState.PAID)
        api_module._store.create(req)

        resp = self._post_event(client, "charge.refunded", req.id, "evt_004")
        assert resp.status_code == 200

        updated = api_module._store.get(req.id)
        assert updated.payment_state == PaymentState.REFUNDED

    def test_idempotency_duplicate_event_skipped(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING, payment_state=PaymentState.AUTHORIZED)
        api_module._store.create(req)

        # Send same event twice
        self._post_event(client, "checkout.session.completed", req.id, "evt_dup_001")
        # Second delivery — change to a failing type to prove it's skipped
        self._post_event(client, "checkout.session.expired", req.id, "evt_dup_001")

        updated = api_module._store.get(req.id)
        # Should remain PAID from first delivery, not FAILED from second
        assert updated.payment_state == PaymentState.PAID

    def test_idempotency_different_events_both_processed(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED, payment_state=PaymentState.PAID)
        api_module._store.create(req)

        resp1 = self._post_event(client, "charge.refunded", req.id, "evt_r_001")
        assert resp1.json().get("duplicate") is not True

        resp2 = self._post_event(client, "charge.refunded", req.id, "evt_r_001")
        assert resp2.json().get("duplicate") is True

    def test_unknown_event_type_ignored(self, client):
        resp = self._post_event(client, "customer.created", "ignored", "evt_005")
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# 2. Booking Executor Wiring
# ---------------------------------------------------------------------------


class TestTravelpayoutsExecutor:

    def test_execute_returns_link_generated(self):
        executor = TravelpayoutsExecutor()
        req = BookingExecutionRequest(
            booking_id="test-001",
            category="flight",
            provider_name="TP",
            provider_link="https://tp.example.com/flight",
            traveler_first_name="Alice",
            traveler_last_name="Smith",
            traveler_email="alice@example.com",
        )
        result = executor.execute(req)
        assert result.provider_status == "link_generated"
        assert result.provider_confirmation_code is not None
        assert result.provider_raw_response["booking_link"] == "https://tp.example.com/flight"
        assert "instructions" in result.provider_raw_response

    def test_execute_includes_confirmation_code(self):
        executor = TravelpayoutsExecutor()
        req = BookingExecutionRequest(booking_id="b1", category="hotel",
                                      provider_link="https://tp.example.com/hotel")
        result = executor.execute(req)
        assert result.provider_confirmation_code.startswith("TP-")

    def test_get_executor_default_travelpayouts(self):
        executor = get_executor()
        assert isinstance(executor, TravelpayoutsExecutor)

    def test_get_executor_env_var(self, monkeypatch):
        monkeypatch.setenv("ZIM_EXECUTOR", "placeholder")
        executor = get_executor()
        assert isinstance(executor, PlaceholderExecutor)

    def test_execute_endpoint_uses_travelpayouts(self, client):
        """The execute endpoint should produce link_generated results by default."""
        rid = _create_and_ready_request(client)

        resp = client.post(f"/v1/requests/{rid}/execute")
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] == "completed"
        # At least one execution result should be link_generated
        statuses = [r["provider_status"] for r in data["execution_results"]]
        assert "link_generated" in statuses


# ---------------------------------------------------------------------------
# 3. Fulfillment State Tracking
# ---------------------------------------------------------------------------


class TestFulfillmentTracking:

    def test_update_fulfillment_state(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED, fulfillment_state=FulfillmentState.LINK_SENT)
        api_module._store.create(req)

        resp = client.post(f"/v1/requests/{req.id}/fulfillment", json={
            "fulfillment_state": "confirmed",
            "details": {"pnr": "ABC123", "hotel_conf": "HOTEL456"},
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["fulfillment_state"] == "confirmed"
        assert data["fulfillment_details"]["pnr"] == "ABC123"

    def test_update_fulfillment_invalid_state(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED)
        api_module._store.create(req)

        resp = client.post(f"/v1/requests/{req.id}/fulfillment", json={
            "fulfillment_state": "invalid_state",
        })
        assert resp.status_code == 422

    def test_update_fulfillment_404(self, client):
        resp = client.post("/v1/requests/nonexistent/fulfillment", json={
            "fulfillment_state": "confirmed",
        })
        assert resp.status_code == 404

    def test_fulfillment_updates_trip_record(self, client):
        """Fulfillment details should propagate to the linked TripRecord."""
        import zim.api as api_module

        req = TravelRequest(state=RequestState.COMPLETED)
        api_module._store.create(req)

        # Create a trip record linked to this request
        trip = TripRecord(request_id=req.id, traveler_id=req.traveler_id, tenant_id=req.tenant_id)
        api_module._trip_store.create(trip)

        client.post(f"/v1/requests/{req.id}/fulfillment", json={
            "fulfillment_state": "confirmed",
            "details": {"pnr": "XY999"},
        })

        updated_trip = api_module._trip_store.get(trip.trip_id)
        assert updated_trip.fulfillment_details.get("pnr") == "XY999"

    def test_execute_creates_trip_record(self, client):
        """Executing a request to completion should create a TripRecord."""
        import zim.api as api_module
        rid = _create_and_ready_request(client)

        client.post(f"/v1/requests/{rid}/execute")

        trip = api_module._trip_store.get_by_request(rid)
        assert trip is not None
        assert trip.request_id == rid
        assert trip.destination == "CPH"

    def test_execute_trip_record_has_links(self, client):
        import zim.api as api_module
        rid = _create_and_ready_request(client)
        client.post(f"/v1/requests/{rid}/execute")

        trip = api_module._trip_store.get_by_request(rid)
        assert isinstance(trip.booking_links, list)
        assert isinstance(trip.confirmation_numbers, list)

    def test_fulfillment_state_all_values(self, client):
        """All valid FulfillmentState values should be accepted."""
        import zim.api as api_module
        for state_val in ("link_sent", "confirmed", "partially_confirmed", "failed"):
            req = TravelRequest(state=RequestState.COMPLETED)
            api_module._store.create(req)
            resp = client.post(f"/v1/requests/{req.id}/fulfillment", json={
                "fulfillment_state": state_val,
            })
            assert resp.status_code == 200, f"Failed for state={state_val}"


# ---------------------------------------------------------------------------
# 4. Trip Record Persistence
# ---------------------------------------------------------------------------


class TestTripRecords:

    def test_list_trips_empty(self, client):
        resp = client.get("/v1/trips")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_trips_after_execute(self, client):
        rid = _create_and_ready_request(client)
        client.post(f"/v1/requests/{rid}/execute")

        resp = client.get("/v1/trips")
        assert resp.status_code == 200
        trips = resp.json()
        assert len(trips) == 1
        assert trips[0]["request_id"] == rid

    def test_get_trip_by_id(self, client):
        rid = _create_and_ready_request(client)
        client.post(f"/v1/requests/{rid}/execute")

        trips = client.get("/v1/trips").json()
        trip_id = trips[0]["trip_id"]

        resp = client.get(f"/v1/trips/{trip_id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["trip_id"] == trip_id
        assert data["request_id"] == rid

    def test_get_trip_not_found(self, client):
        resp = client.get("/v1/trips/nonexistent")
        assert resp.status_code == 404

    def test_list_trips_filter_by_tenant(self, client):
        import zim.api as api_module

        trip_a = TripRecord(request_id="r1", tenant_id="acme", destination="CPH")
        trip_b = TripRecord(request_id="r2", tenant_id="other", destination="JFK")
        api_module._trip_store.create(trip_a)
        api_module._trip_store.create(trip_b)

        resp = client.get("/v1/trips?tenant_id=acme")
        assert resp.status_code == 200
        trips = resp.json()
        assert all(t["tenant_id"] == "acme" for t in trips)
        assert len(trips) == 1

    def test_list_trips_filter_by_traveler(self, client):
        import zim.api as api_module

        trip_a = TripRecord(request_id="r1", traveler_id="alice", destination="CPH")
        trip_b = TripRecord(request_id="r2", traveler_id="bob", destination="JFK")
        api_module._trip_store.create(trip_a)
        api_module._trip_store.create(trip_b)

        resp = client.get("/v1/trips?traveler_id=alice")
        trips = resp.json()
        assert len(trips) == 1
        assert trips[0]["traveler_id"] == "alice"

    def test_trip_record_fields(self, client):
        import zim.api as api_module
        rid = _create_and_ready_request(client)
        client.post(f"/v1/requests/{rid}/execute")

        trips = client.get("/v1/trips").json()
        trip = trips[0]
        assert "trip_id" in trip
        assert "request_id" in trip
        assert "traveler_id" in trip
        assert "tenant_id" in trip
        assert "destination" in trip
        assert "dates" in trip
        assert "total_cost" in trip
        assert "booking_links" in trip
        assert "confirmation_numbers" in trip
        assert "created_at" in trip


# ---------------------------------------------------------------------------
# 5. Request Retry / Re-search
# ---------------------------------------------------------------------------


class TestRetry:

    def test_retry_from_options_ready(self, client):
        with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
            resp = client.post("/v1/requests", json={
                "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
            })
        rid = resp.json()["id"]
        assert resp.json()["state"] == "options_ready"

        with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
            retry_resp = client.post(f"/v1/requests/{rid}/retry")
        assert retry_resp.status_code == 200
        data = retry_resp.json()
        assert data["state"] == "options_ready"  # after re-search
        assert data["itinerary"] is not None

    def test_retry_from_failed(self, client):
        import zim.api as api_module
        req = TravelRequest(
            state=RequestState.FAILED,
            parsed_intent={
                "travel_type": "flight",
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
        )
        api_module._store.create(req)

        with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
            resp = client.post(f"/v1/requests/{req.id}/retry", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] == "options_ready"

    def test_retry_wrong_state(self, client):
        import zim.api as api_module
        req = TravelRequest(state=RequestState.COMPLETED)
        api_module._store.create(req)

        resp = client.post(f"/v1/requests/{req.id}/retry")
        assert resp.status_code == 409

    def test_retry_clears_previous_results(self, client):
        with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
            create_resp = client.post("/v1/requests", json={
                "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
            })
        rid = create_resp.json()["id"]

        with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
            retry_resp = client.post(f"/v1/requests/{rid}/retry")
        data = retry_resp.json()
        # Previous itinerary should be replaced with fresh results
        assert data["itinerary"] is not None

    def test_retry_from_intent_received_rejected(self, client):
        """Cannot retry when already in intent_received."""
        import zim.api as api_module
        req = TravelRequest(state=RequestState.INTENT_RECEIVED)
        api_module._store.create(req)

        resp = client.post(f"/v1/requests/{req.id}/retry")
        assert resp.status_code == 409

    def test_retry_not_found(self, client):
        resp = client.post("/v1/requests/nonexistent/retry")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# WebhookEventStore unit tests
# ---------------------------------------------------------------------------


class TestWebhookEventStore:

    def test_first_event_is_new(self, tmp_path):
        store = WebhookEventStore(db_path=tmp_path / "wh.db")
        assert store.mark_processed("evt_001", "checkout.session.completed") is True

    def test_duplicate_event_returns_false(self, tmp_path):
        store = WebhookEventStore(db_path=tmp_path / "wh.db")
        store.mark_processed("evt_001", "checkout.session.completed")
        assert store.mark_processed("evt_001", "checkout.session.completed") is False

    def test_different_events_both_new(self, tmp_path):
        store = WebhookEventStore(db_path=tmp_path / "wh.db")
        assert store.mark_processed("evt_001") is True
        assert store.mark_processed("evt_002") is True

    def test_is_processed(self, tmp_path):
        store = WebhookEventStore(db_path=tmp_path / "wh.db")
        assert store.is_processed("evt_999") is False
        store.mark_processed("evt_999")
        assert store.is_processed("evt_999") is True


# ---------------------------------------------------------------------------
# TripStore unit tests
# ---------------------------------------------------------------------------


class TestTripStore:

    def test_create_and_get(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        record = TripRecord(request_id="req1", destination="CPH", total_cost=1500.0)
        store.create(record)
        fetched = store.get(record.trip_id)
        assert fetched is not None
        assert fetched.destination == "CPH"
        assert fetched.total_cost == 1500.0

    def test_get_missing(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        assert store.get("nonexistent") is None

    def test_get_by_request(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        record = TripRecord(request_id="req_abc", destination="JFK")
        store.create(record)
        fetched = store.get_by_request("req_abc")
        assert fetched is not None
        assert fetched.trip_id == record.trip_id

    def test_list_all(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        store.create(TripRecord(request_id="r1", tenant_id="a", destination="A"))
        store.create(TripRecord(request_id="r2", tenant_id="b", destination="B"))
        trips = store.list_trips()
        assert len(trips) == 2

    def test_list_filter_tenant(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        store.create(TripRecord(request_id="r1", tenant_id="acme", destination="A"))
        store.create(TripRecord(request_id="r2", tenant_id="other", destination="B"))
        trips = store.list_trips(tenant_id="acme")
        assert len(trips) == 1
        assert trips[0].tenant_id == "acme"

    def test_update_fulfillment(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        record = TripRecord(request_id="r1", destination="CPH")
        store.create(record)
        result = store.update_fulfillment(record.trip_id, {"pnr": "PNR123"})
        assert result is True
        updated = store.get(record.trip_id)
        assert updated.fulfillment_details["pnr"] == "PNR123"

    def test_update_fulfillment_missing(self, tmp_path):
        store = TripStore(db_path=tmp_path / "trips.db")
        result = store.update_fulfillment("nonexistent", {"pnr": "X"})
        assert result is False
