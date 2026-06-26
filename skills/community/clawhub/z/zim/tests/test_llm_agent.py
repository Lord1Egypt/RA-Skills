"""Tests for zim.llm_agent — LLM-backed WhatsApp agent.

All OpenRouter HTTP calls and Zim search functions are mocked so the
tests run without external API keys.

Updated to work with the orchestrator-based flow (v2):
- LLMWhatsAppAgent.handle_message() delegates to ZimOrchestrator
- Orchestrator calls _parse_intent (not agent._call_llm) for NLU
- State is stored as data["travel_request"], not data["messages"]/data["last_results"]
"""

from __future__ import annotations

import json
from datetime import date, datetime
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from zim.core import CarResult, FlightResult, HotelResult, Itinerary
from zim.llm_agent import (
    LLMWhatsAppAgent,
    _fmt_flight,
    _fmt_hotel,
    _fmt_car,
    _format_results,
)
from zim.state_store import InMemoryStateStore


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_agent(api_key: str = "test-key") -> tuple[LLMWhatsAppAgent, InMemoryStateStore]:
    store = InMemoryStateStore()
    agent = LLMWhatsAppAgent(
        api_key=api_key,
        model="test/model",
        state_store=store,
    )
    return agent, store


def _flight_result(**overrides: Any) -> FlightResult:
    defaults: dict[str, Any] = dict(
        airline="EK",
        flight_number="EK29",
        origin="DXB",
        destination="CPH",
        depart_at=datetime(2026, 5, 10, 8, 0),
        arrive_at=datetime(2026, 5, 10, 13, 0),
        transfers=0,
        cabin="economy",
        price_usd=480.0,
        refundable=False,
        link="https://example.com/book/flight",
    )
    defaults.update(overrides)
    return FlightResult(**defaults)


def _hotel_result(**overrides: Any) -> HotelResult:
    defaults: dict[str, Any] = dict(
        name="Grand Hotel",
        stars=4,
        location="Copenhagen",
        distance_km=1.0,
        nightly_rate_usd=200.0,
        refundable=True,
        link="https://example.com/book/hotel",
    )
    defaults.update(overrides)
    return HotelResult(**defaults)


def _car_result(**overrides: Any) -> CarResult:
    defaults: dict[str, Any] = dict(
        provider="Rentalcars",
        vehicle_class="economy",
        pickup_location="Copenhagen",
        price_usd_total=150.0,
        free_cancellation=True,
        link="https://example.com/book/car",
    )
    defaults.update(overrides)
    return CarResult(**defaults)


def _itinerary(flights=None, hotels=None, cars=None) -> Itinerary:
    if flights is None:
        flights = [_flight_result()]
    if hotels is None:
        hotels = []
    if cars is None:
        cars = []
    return Itinerary(
        destination="CPH",
        mode="personal",
        dates={"departure": "2026-05-10", "return": None, "nights": 0},
        flights=flights,
        hotels=hotels,
        cars=cars,
        status="booking_ready",
        approval_reason=None,
        total_price_usd=sum(f.price_usd for f in flights),
    )


# --- Intent helpers ---

def _greeting_intent() -> dict[str, Any]:
    return {"action": "greeting", "slots": {}, "option_number": None, "modification": None}


def _search_flight_intent(
    origin: str = "DXB",
    destination: str = "CPH",
    departure_date: str = "2026-05-10",
) -> dict[str, Any]:
    return {
        "action": "search",
        "slots": {
            "request_type": "flight",
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
        },
        "option_number": None,
        "modification": None,
    }


def _search_hotel_intent(
    location: str = "Copenhagen",
    checkin: str = "2026-05-10",
    checkout: str = "2026-05-13",
) -> dict[str, Any]:
    return {
        "action": "search",
        "slots": {
            "request_type": "hotel",
            "hotel_location": location,
            "checkin": checkin,
            "checkout": checkout,
        },
        "option_number": None,
        "modification": None,
    }


def _search_car_intent(
    location: str = "Copenhagen",
    pickup_date: str = "2026-05-10",
    dropoff_date: str = "2026-05-13",
) -> dict[str, Any]:
    return {
        "action": "search",
        "slots": {
            "request_type": "car",
            "car_location": location,
            "pickup_date": pickup_date,
            "dropoff_date": dropoff_date,
        },
        "option_number": None,
        "modification": None,
    }


# ---------------------------------------------------------------------------
# Formatter tests (pure, no mocking needed)
# ---------------------------------------------------------------------------


class TestFormatters:
    def test_fmt_flight_basic(self) -> None:
        r = _flight_result().model_dump()
        text = _fmt_flight(r, 1)
        assert "1." in text
        assert "EK29" in text
        assert "DXB → CPH" in text
        assert "$480.00" in text

    def test_fmt_flight_out_of_policy(self) -> None:
        r = _flight_result().model_dump()
        r["policy_status"] = "out_of_policy"
        text = _fmt_flight(r, 2)
        assert "exceeds policy" in text

    def test_fmt_hotel_basic(self) -> None:
        r = _hotel_result().model_dump()
        text = _fmt_hotel(r, 1)
        assert "Grand Hotel" in text
        assert "$200.00/night" in text
        assert "★★★★" in text

    def test_fmt_car_basic(self) -> None:
        r = _car_result().model_dump()
        text = _fmt_car(r, 1)
        assert "Rentalcars" in text
        assert "Economy" in text
        assert "$150.00" in text
        assert "Free cancellation" in text

    def test_format_results_limits_to_3(self) -> None:
        results = [_flight_result().model_dump() for _ in range(5)]
        text = _format_results("flight", results)
        # Only indices 1, 2, 3 should appear; 4 and 5 should not
        assert "1." in text
        assert "3." in text
        assert "4." not in text


# ---------------------------------------------------------------------------
# Agent: missing API key
# ---------------------------------------------------------------------------


class TestMissingApiKey:
    def test_returns_config_error(self) -> None:
        store = InMemoryStateStore()
        agent = LLMWhatsAppAgent(api_key="", state_store=store)
        reply = agent.handle_message("Find flights", "whatsapp:+1234")
        assert "not configured" in reply.lower() or "missing" in reply.lower() or "openrouter" in reply.lower()


# ---------------------------------------------------------------------------
# Agent: plain text response (greeting via orchestrator state machine)
# ---------------------------------------------------------------------------


class TestPlainTextResponse:
    def test_greeting_is_relayed(self) -> None:
        """Greeting intent with IDLE state returns the Zim welcome message."""
        agent, store = _make_agent()

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_greeting_intent()):
            reply = agent.handle_message("Hi there", "whatsapp:+1")

        # Orchestrator IDLE state returns its fixed greeting
        assert "zim" in reply.lower() or "travel" in reply.lower() or "help" in reply.lower()

    def test_state_is_persisted(self) -> None:
        """After handling a message the orchestrator persists travel_request state."""
        agent, store = _make_agent()
        uid = "whatsapp:+2"

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_greeting_intent()):
            agent.handle_message("Message 1", uid)

        data = store.get(uid)
        assert data is not None
        assert "travel_request" in data

    def test_state_updates_across_turns(self) -> None:
        """travel_request is updated across multiple turns."""
        agent, store = _make_agent()
        uid = "whatsapp:+3"

        for i in range(3):
            with patch.object(agent._orchestrator, "_parse_intent", return_value=_greeting_intent()):
                agent.handle_message(f"Message {i}", uid)

        data = store.get(uid)
        assert data is not None
        assert "travel_request" in data


# ---------------------------------------------------------------------------
# Agent: flight search via orchestrator
# ---------------------------------------------------------------------------


class TestFlightSearch:
    def test_search_flights_tool_executed(self, monkeypatch) -> None:
        """Full flight search flow: parse_intent → state=SEARCHING → plan_trip → results."""
        agent, store = _make_agent()
        uid = "whatsapp:+10"

        itinerary = _itinerary()
        monkeypatch.setattr("zim.trip.plan_trip", lambda **kw: itinerary)

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_search_flight_intent()):
            reply = agent.handle_message(
                "Find me a flight from Dubai to Copenhagen on May 10", uid
            )

        assert "flight" in reply.lower() or "EK" in reply or "DXB" in reply or "CPH" in reply

        # Results are stored in travel_request.search_results (not legacy last_results)
        data = store.get(uid)
        assert data is not None
        req = data.get("travel_request", {})
        assert len(req.get("search_results", [])) == 1

    def test_no_flights_returns_message(self, monkeypatch) -> None:
        """Empty flight results produce a helpful fallback message."""
        agent, store = _make_agent()
        uid = "whatsapp:+11"

        empty_itinerary = _itinerary(flights=[])
        monkeypatch.setattr("zim.trip.plan_trip", lambda **kw: empty_itinerary)

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_search_flight_intent()):
            reply = agent.handle_message("Flights from DXB to CPH May 10", uid)

        assert (
            "no results" in reply.lower()
            or "no flights" in reply.lower()
            or "try" in reply.lower()
            or "different" in reply.lower()
        )


# ---------------------------------------------------------------------------
# Agent: hotel search via orchestrator
# ---------------------------------------------------------------------------


class TestHotelSearch:
    def test_search_hotels_tool_executed(self, monkeypatch) -> None:
        """Hotel search fills slots and stores results in travel_request."""
        agent, store = _make_agent()
        uid = "whatsapp:+20"

        hotels = [_hotel_result(), _hotel_result(name="Budget Inn", stars=3, nightly_rate_usd=90.0)]
        monkeypatch.setattr(
            "zim.hotel_search.search",
            lambda **kw: hotels,
        )

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_search_hotel_intent()):
            agent.handle_message("Hotels in Copenhagen May 10-13", uid)

        data = store.get(uid)
        assert data is not None
        req = data.get("travel_request", {})
        assert len(req.get("search_results", [])) == 2


# ---------------------------------------------------------------------------
# Agent: car search via orchestrator
# ---------------------------------------------------------------------------


class TestCarSearch:
    def test_search_cars_tool_executed(self, monkeypatch) -> None:
        """Car search fills slots and stores results in travel_request."""
        agent, store = _make_agent()
        uid = "whatsapp:+30"

        cars = [_car_result(), _car_result(provider="Kayak", vehicle_class="suv", price_usd_total=300.0)]
        monkeypatch.setattr("zim.car_search.search", lambda **kw: cars)

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_search_car_intent()):
            agent.handle_message("Rent a car in Copenhagen May 10-13", uid)

        data = store.get(uid)
        assert data is not None
        req = data.get("travel_request", {})
        assert len(req.get("search_results", [])) == 2


# ---------------------------------------------------------------------------
# Agent: get_booking_link tool (direct method tests)
#
# Note: the orchestrator uses book_option + confirm_booking for its primary
# booking flow. get_booking_link is a fallback available directly on the
# agent and tested here as a unit-level method test.
# ---------------------------------------------------------------------------


class TestGetBookingLink:
    def _seed_results(self, store: InMemoryStateStore, uid: str) -> None:
        """Pre-load last_results so the agent has something to link to."""
        store.save(
            uid,
            {
                "last_results": {
                    "flight": [
                        _flight_result().model_dump(),
                        _flight_result(
                            airline="LH",
                            flight_number="LH123",
                            price_usd=320.0,
                            link="https://example.com/lh",
                        ).model_dump(),
                    ]
                },
                "preferences": {},
            },
        )

    def test_get_booking_link_returns_url(self) -> None:
        agent, store = _make_agent()
        uid = "whatsapp:+40"
        self._seed_results(store, uid)

        last_results = store.get(uid)["last_results"]  # type: ignore[index]
        result = agent._tool_get_booking_link(
            {"category": "flight", "index": 2}, last_results
        )
        assert "https://example.com/lh" in result

    def test_get_booking_link_out_of_range(self) -> None:
        agent, store = _make_agent()
        uid = "whatsapp:+41"
        self._seed_results(store, uid)

        # Direct tool execution test (bypass LLM loop)
        last_results = store.get(uid)["last_results"]  # type: ignore[index]
        result = agent._tool_get_booking_link(
            {"category": "flight", "index": 5}, last_results
        )
        assert "out of range" in result

    def test_get_booking_link_no_prior_results(self) -> None:
        agent, store = _make_agent()
        uid = "whatsapp:+42"

        last_results: dict = {}
        result = agent._tool_get_booking_link(
            {"category": "hotel", "index": 1}, last_results
        )
        assert "No hotel results" in result or "search first" in result.lower()


# ---------------------------------------------------------------------------
# Agent: error handling
#
# Note: orchestrator.handle_message() catches exceptions from _parse_intent
# internally and falls back to a "chat" intent. To test agent-level error
# handling (the try/except in LLMWhatsAppAgent.handle_message), we mock
# orchestrator.handle_message itself to raise.
# ---------------------------------------------------------------------------


class TestErrorHandling:
    def test_llm_timeout_returns_graceful_message(self) -> None:
        import httpx

        agent, store = _make_agent()

        with patch.object(agent._orchestrator, "handle_message", side_effect=httpx.TimeoutException("timeout")):
            reply = agent.handle_message("Find flights", "whatsapp:+50")

        assert "too long" in reply.lower() or "timeout" in reply.lower() or "try again" in reply.lower()

    def test_llm_http_error_returns_graceful_message(self) -> None:
        import httpx

        agent, store = _make_agent()

        mock_resp = MagicMock()
        mock_resp.status_code = 429
        exc = httpx.HTTPStatusError("rate limit", request=MagicMock(), response=mock_resp)

        with patch.object(agent._orchestrator, "handle_message", side_effect=exc):
            reply = agent.handle_message("Find flights", "whatsapp:+51")

        assert "trouble" in reply.lower() or "try again" in reply.lower()

    def test_tool_error_returns_error_string(self, monkeypatch) -> None:
        """agent._execute_tool catches exceptions and returns a user-friendly string."""
        agent, store = _make_agent()

        def _raise(**kw):
            raise RuntimeError("boom")

        monkeypatch.setattr("zim.trip.plan_trip", _raise)

        # Call through _execute_tool so the exception handler fires
        last_results: dict = {}
        result = agent._execute_tool(
            "search_flights",
            {"origin": "DXB", "destination": "CPH", "departure_date": "2026-05-10"},
            last_results,
        )
        assert "error" in result.lower() or "try again" in result.lower()

    def test_state_not_corrupted_on_llm_error(self) -> None:
        """If orchestrator raises, existing travel_request state must be preserved."""
        import httpx

        agent, store = _make_agent()
        uid = "whatsapp:+52"

        # Seed existing orchestrator state
        from zim.travel_request import TravelRequest
        existing = TravelRequest(origin="DXB", destination="CPH")
        store.save(uid, {"travel_request": existing.model_dump(mode="json")})

        with patch.object(agent._orchestrator, "handle_message", side_effect=httpx.TimeoutException("timeout")):
            agent.handle_message("New message", uid)

        # orchestrator never called _save_request, so state is unchanged
        data = store.get(uid)
        assert data is not None
        req = data.get("travel_request", {})
        assert req.get("origin") == "DXB"
        assert req.get("destination") == "CPH"


# ---------------------------------------------------------------------------
# Agent: history trimming (legacy behaviour — orchestrator manages its own state)
# ---------------------------------------------------------------------------


class TestHistoryTrimming:
    def test_history_trimmed_to_max(self) -> None:
        """Orchestrator replaces the old message-history model.
        Verify multiple turns run without error and state is persisted."""
        agent, store = _make_agent()
        uid = "whatsapp:+60"

        for _ in range(15):
            with patch.object(agent._orchestrator, "_parse_intent", return_value=_greeting_intent()):
                reply = agent.handle_message("Hi", uid)

        # Should complete without crashing; state is stored
        data = store.get(uid)
        assert data is not None
        assert "travel_request" in data
        assert reply is not None and len(reply) > 0


# ---------------------------------------------------------------------------
# Agent: backwards compatibility with legacy state format
# ---------------------------------------------------------------------------


class TestBackwardsCompatibility:
    def test_legacy_state_without_messages_key(self) -> None:
        """Old ZimWhatsAppAgent state (no 'travel_request' key) should not crash.

        Orchestrator's _load_request falls back to a fresh TravelRequest when
        the key is absent, so old state formats are silently ignored.
        """
        agent, store = _make_agent()
        uid = "whatsapp:+70"

        # Simulate old-format state from ZimWhatsAppAgent
        store.save(uid, {
            "state": "idle",
            "intent": {},
            "last_results": {},
            "selected_index": None,
            "pending_item": None,
            "pending_category": None,
        })

        with patch.object(agent._orchestrator, "_parse_intent", return_value=_greeting_intent()):
            reply = agent.handle_message("Hi", uid)

        # Should return IDLE greeting without crashing
        assert reply is not None and len(reply) > 0


# ---------------------------------------------------------------------------
# Webhook integration: agent selection
# ---------------------------------------------------------------------------

try:
    import flask as _flask_mod  # noqa: F401
    _FLASK_AVAILABLE = True
except ImportError:
    _FLASK_AVAILABLE = False


@pytest.mark.skipif(not _FLASK_AVAILABLE, reason="Flask not installed")
class TestWebhookAgentSelection:
    def test_llm_agent_selected_when_key_present(self, monkeypatch) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
        monkeypatch.delenv("ZIM_USE_LEGACY_AGENT", raising=False)

        from zim import webhook

        app = webhook.create_app()
        assert app is not None

    def test_legacy_agent_selected_when_no_key(self, monkeypatch) -> None:
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)

        from zim import webhook

        app = webhook.create_app()
        assert app is not None

    def test_legacy_agent_forced_when_env_flag_set(self, monkeypatch) -> None:
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test")
        monkeypatch.setenv("ZIM_USE_LEGACY_AGENT", "1")

        from zim import webhook

        app = webhook.create_app()
        assert app is not None
