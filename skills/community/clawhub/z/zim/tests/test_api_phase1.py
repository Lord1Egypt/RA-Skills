"""Phase 1 API tests: webhook, auth, search endpoint, logging."""

from __future__ import annotations

import json
import os
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from zim.api import app, _store
from zim.core import CarResult, FlightResult, HotelResult, Itinerary
from zim.ranking import ScoredResult
from zim.request_state import RequestState, TravelRequest


# ---------------------------------------------------------------------------
# Fixtures (mirror test_api.py setup)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_store(tmp_path):
    """Fresh DB per test, restore original after."""
    from zim.request_store import RequestStore
    import zim.api as api_module

    original = api_module._store
    api_module._store = RequestStore(db_path=tmp_path / "test_requests.db")
    yield
    api_module._store = original


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=True)


# ---------------------------------------------------------------------------
# Shared mock data
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


def _mock_plan(*_args, **_kwargs):
    return _MOCK_SCORED


def _create_options_ready(client) -> str:
    """Create a request that is already in options_ready state."""
    with patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan):
        resp = client.post("/v1/requests", json={
            "intent": {
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            },
        })
    assert resp.status_code == 201
    return resp.json()["id"]


# ---------------------------------------------------------------------------
# Auth middleware tests
# ---------------------------------------------------------------------------


class TestAuthMiddleware:
    def test_health_no_auth_required(self, client):
        """Health endpoint is always public."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "secret123"}):
            resp = client.get("/v1/health")
        assert resp.status_code == 200

    def test_no_api_key_env_allows_all(self, client):
        """When ZIM_API_KEY is unset, all requests are allowed."""
        env = {k: v for k, v in os.environ.items() if k != "ZIM_API_KEY"}
        with patch.dict(os.environ, env, clear=True):
            resp = client.get("/v1/requests")
        assert resp.status_code == 200

    def test_valid_bearer_token(self, client):
        """Correct Bearer token is accepted."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "testkey"}):
            resp = client.get(
                "/v1/requests",
                headers={"Authorization": "Bearer testkey"},
            )
        assert resp.status_code == 200

    def test_missing_auth_header_rejected(self, client):
        """Missing Authorization header returns 401 when key is configured."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "testkey"}):
            resp = client.get("/v1/requests")
        assert resp.status_code == 401
        assert "detail" in resp.json()

    def test_wrong_token_rejected(self, client):
        """Wrong Bearer token returns 401."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "testkey"}):
            resp = client.get(
                "/v1/requests",
                headers={"Authorization": "Bearer wrongkey"},
            )
        assert resp.status_code == 401

    def test_non_bearer_scheme_rejected(self, client):
        """Non-Bearer auth scheme is rejected."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "testkey"}):
            resp = client.get(
                "/v1/requests",
                headers={"Authorization": "Basic dGVzdDp0ZXN0"},
            )
        assert resp.status_code == 401

    def test_webhook_endpoint_skips_auth(self, client):
        """Stripe webhook endpoint is exempt from API key auth."""
        with patch.dict(os.environ, {"ZIM_API_KEY": "testkey"}):
            resp = client.post(
                "/v1/webhooks/stripe",
                content=json.dumps({"type": "ping", "data": {"object": {}}}),
                headers={"Content-Type": "application/json"},
            )
        # Should not be 401 (may be 200 or other status from processing)
        assert resp.status_code != 401


# ---------------------------------------------------------------------------
# Search endpoint tests
# ---------------------------------------------------------------------------


class TestSearchEndpoint:
    @patch("zim.trip.plan_trip_with_scores", side_effect=_mock_plan)
    def test_search_intent_received(self, mock_search, client):
        """Search endpoint triggers search on an intent_received request."""
        # Create without auto_search
        resp = client.post("/v1/requests", json={
            "intent": {"origin": "LIS", "destination": "CPH", "departure_date": "2026-06-01"},
            "auto_search": False,
        })
        assert resp.status_code == 201
        rid = resp.json()["id"]
        assert resp.json()["state"] == "intent_received"

        # Trigger search
        resp = client.post(f"/v1/requests/{rid}/search")
        assert resp.status_code == 200
        data = resp.json()
        assert data["state"] == "options_ready"
        assert data["itinerary"] is not None
        mock_search.assert_called_once()

    def test_search_wrong_state(self, client):
        """Search endpoint rejects requests not in intent_received state."""
        rid = _create_options_ready(client)
        resp = client.post(f"/v1/requests/{rid}/search")
        assert resp.status_code == 409
        assert "intent_received" in resp.json()["detail"]

    def test_search_not_found(self, client):
        """Search on unknown request_id returns 404."""
        resp = client.post("/v1/requests/doesnotexist/search")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Stripe webhook tests
# ---------------------------------------------------------------------------


class TestStripeWebhook:
    def test_webhook_no_secret_checkout_completed(self, client):
        """checkout.session.completed updates payment_state to paid."""
        # Create a request and store it, simulating a booking in progress
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING)
        api_module._store.create(req)

        event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {"booking_id": req.id},
                    "payment_status": "paid",
                }
            },
        }

        with patch.dict(os.environ, {}, clear=False):
            # Ensure no webhook secret so we skip sig verification
            env_no_secret = {k: v for k, v in os.environ.items()
                            if k != "STRIPE_WEBHOOK_SECRET"}
            with patch.dict(os.environ, env_no_secret, clear=True):
                resp = client.post(
                    "/v1/webhooks/stripe",
                    content=json.dumps(event),
                    headers={"Content-Type": "application/json"},
                )

        assert resp.status_code == 200
        data = resp.json()
        assert data["received"] is True
        assert data["booking_id"] == req.id
        assert data["event_type"] == "checkout.session.completed"

        # Verify payment_state was updated in the store
        updated = api_module._store.get(req.id)
        assert updated is not None
        from zim.request_state import PaymentState
        assert updated.payment_state == PaymentState.PAID

    def test_webhook_payment_intent_succeeded(self, client):
        """payment_intent.succeeded also updates payment_state to paid."""
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING)
        api_module._store.create(req)

        event = {
            "type": "payment_intent.succeeded",
            "data": {
                "object": {
                    "metadata": {"booking_id": req.id},
                }
            },
        }

        env_no_secret = {k: v for k, v in os.environ.items()
                        if k != "STRIPE_WEBHOOK_SECRET"}
        with patch.dict(os.environ, env_no_secret, clear=True):
            resp = client.post(
                "/v1/webhooks/stripe",
                content=json.dumps(event),
                headers={"Content-Type": "application/json"},
            )

        assert resp.status_code == 200
        updated = api_module._store.get(req.id)
        from zim.request_state import PaymentState
        assert updated.payment_state == PaymentState.PAID

    def test_webhook_unknown_event_type(self, client):
        """Unrecognised event types are ignored gracefully."""
        event = {
            "type": "customer.created",
            "data": {"object": {}},
        }

        env_no_secret = {k: v for k, v in os.environ.items()
                        if k != "STRIPE_WEBHOOK_SECRET"}
        with patch.dict(os.environ, env_no_secret, clear=True):
            resp = client.post(
                "/v1/webhooks/stripe",
                content=json.dumps(event),
                headers={"Content-Type": "application/json"},
            )

        assert resp.status_code == 200
        assert resp.json()["received"] is True
        assert resp.json()["booking_id"] is None

    def test_webhook_unknown_booking_id(self, client):
        """Webhook with unknown booking_id is accepted but does nothing."""
        event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {"booking_id": "nonexistent_booking"},
                    "payment_status": "paid",
                }
            },
        }

        env_no_secret = {k: v for k, v in os.environ.items()
                        if k != "STRIPE_WEBHOOK_SECRET"}
        with patch.dict(os.environ, env_no_secret, clear=True):
            resp = client.post(
                "/v1/webhooks/stripe",
                content=json.dumps(event),
                headers={"Content-Type": "application/json"},
            )

        assert resp.status_code == 200

    def test_webhook_invalid_json(self, client):
        """Invalid JSON payload returns 400."""
        env_no_secret = {k: v for k, v in os.environ.items()
                        if k != "STRIPE_WEBHOOK_SECRET"}
        with patch.dict(os.environ, env_no_secret, clear=True):
            resp = client.post(
                "/v1/webhooks/stripe",
                content=b"not json at all",
                headers={"Content-Type": "application/json"},
            )

        assert resp.status_code == 400

    def test_webhook_with_signature_verification(self, client):
        """When STRIPE_WEBHOOK_SECRET is set, invalid signature is rejected."""
        event = {"type": "ping", "data": {"object": {}}}

        with patch.dict(os.environ, {"STRIPE_WEBHOOK_SECRET": "whsec_test"}):
            with patch("stripe.Webhook.construct_event") as mock_construct:
                import stripe as _stripe
                mock_construct.side_effect = _stripe.error.SignatureVerificationError(
                    "Invalid signature", "sig_header"
                )
                resp = client.post(
                    "/v1/webhooks/stripe",
                    content=json.dumps(event),
                    headers={
                        "Content-Type": "application/json",
                        "stripe-signature": "t=1,v1=invalid",
                    },
                )

        assert resp.status_code == 400
        assert "signature" in resp.json()["detail"].lower()

    def test_webhook_with_valid_signature(self, client):
        """When signature verification passes, event is processed normally."""
        import zim.api as api_module
        req = TravelRequest(state=RequestState.EXECUTING)
        api_module._store.create(req)

        # Mock construct_event to return a valid dict
        mock_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "metadata": {"booking_id": req.id},
                    "payment_status": "paid",
                }
            },
        }

        with patch.dict(os.environ, {"STRIPE_WEBHOOK_SECRET": "whsec_test"}):
            with patch("stripe.Webhook.construct_event", return_value=mock_event):
                resp = client.post(
                    "/v1/webhooks/stripe",
                    content=json.dumps(mock_event),
                    headers={
                        "Content-Type": "application/json",
                        "stripe-signature": "t=1,v1=valid",
                    },
                )

        assert resp.status_code == 200
        assert resp.json()["booking_id"] == req.id


# ---------------------------------------------------------------------------
# Logging / request_id tests
# ---------------------------------------------------------------------------


class TestLoggingMiddleware:
    def test_response_has_request_id_header(self, client):
        """Every response includes X-Request-ID."""
        resp = client.get("/v1/health")
        assert "x-request-id" in resp.headers

    def test_request_id_echoed_back(self, client):
        """Client-supplied X-Request-ID is echoed in response."""
        resp = client.get("/v1/health", headers={"X-Request-ID": "my-trace-42"})
        assert resp.headers.get("x-request-id") == "my-trace-42"

    def test_server_generates_request_id(self, client):
        """Server generates a request_id when none is supplied."""
        resp = client.get("/v1/health")
        rid = resp.headers.get("x-request-id", "")
        assert len(rid) > 0


# ---------------------------------------------------------------------------
# Improved validation tests
# ---------------------------------------------------------------------------


class TestValidation:
    def test_list_requests_invalid_state_filter(self, client):
        """Invalid state value in list filter returns 422."""
        resp = client.get("/v1/requests?state=notastate")
        assert resp.status_code == 422

    def test_select_no_options_returns_422(self, client):
        """Selecting with no indices returns 422."""
        rid = _create_options_ready(client)
        resp = client.post(f"/v1/requests/{rid}/select", json={})
        assert resp.status_code == 422

    def test_select_negative_index_returns_422(self, client):
        """Negative flight_index returns 422."""
        rid = _create_options_ready(client)
        resp = client.post(f"/v1/requests/{rid}/select", json={"flight_index": -1})
        assert resp.status_code == 422
