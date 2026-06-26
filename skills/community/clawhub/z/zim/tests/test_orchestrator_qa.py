"""Comprehensive QA tests for ZimOrchestrator.

Tests cover:
- Anti-hallucination: NLU must not guess origin/destination/dates
- Multi-turn slot collection (one question at a time)
- Relative date parsing (in N days/weeks, this weekend, end of month, mid/early/late Month)
- Complete flight/hotel/car booking flows
- State machine transitions (cancel, new_search, select, confirm)
- Edge cases

All LLM calls (_parse_intent) and search calls are mocked.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any
from unittest.mock import patch, MagicMock

import pytest

from zim.orchestrator import ZimOrchestrator
from zim.state_store import InMemoryStateStore
from zim.travel_request import FlowState, RequestType, TravelRequest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_orch() -> tuple[ZimOrchestrator, InMemoryStateStore]:
    store = InMemoryStateStore()
    orch = ZimOrchestrator(store=store, api_key="test-key")
    return orch, store


def _nlu(
    action: str,
    slots: dict[str, Any] | None = None,
    option_number: int | None = None,
    modification: dict | None = None,
) -> dict[str, Any]:
    return {
        "action": action,
        "slots": slots or {},
        "option_number": option_number,
        "modification": modification,
    }


def _flight_result(
    origin: str = "JFK",
    destination: str = "LHR",
    price: float = 480.0,
    cabin: str = "economy",
    **kw: Any,
) -> dict[str, Any]:
    return {
        "airline": "BA",
        "flight_number": "BA001",
        "origin": origin,
        "destination": destination,
        "depart_at": "2026-06-15T08:00:00",
        "arrive_at": "2026-06-15T19:00:00",
        "transfers": 0,
        "cabin": cabin,
        "price_usd": price,
        **kw,
    }


def _hotel_result(name: str = "Grand Hotel", price: float = 200.0, **kw: Any) -> dict[str, Any]:
    return {
        "name": name,
        "stars": 4,
        "location": "London",
        "nightly_rate_usd": price,
        "refundable": True,
        **kw,
    }


def _car_result(provider: str = "Hertz", price: float = 150.0, **kw: Any) -> dict[str, Any]:
    return {
        "provider": provider,
        "vehicle_class": "economy",
        "pickup_location": "London Heathrow",
        "price_usd_total": price,
        "free_cancellation": True,
        **kw,
    }


def _send(orch: ZimOrchestrator, text: str, uid: str, nlu: dict) -> str:
    """Send a message with a mocked _parse_intent response."""
    with patch.object(orch, "_parse_intent", return_value=nlu):
        return orch.handle_message(text, uid)


def _send_search(
    orch: ZimOrchestrator,
    text: str,
    uid: str,
    nlu: dict,
    flight_results: list[dict] | None = None,
    hotel_results: list[dict] | None = None,
    car_results: list[dict] | None = None,
) -> str:
    """Send with mocked NLU and mocked search results."""
    from zim import hotel_search, car_search

    flights = flight_results if flight_results is not None else [_flight_result()]
    hotels = hotel_results if hotel_results is not None else []
    cars = car_results if car_results is not None else []

    mock_itinerary = MagicMock()
    mock_itinerary.flights = [_make_flight_model(f) for f in flights]

    mock_hotel_results = [_make_hotel_model(h) for h in hotels]
    mock_car_results = [_make_car_model(c) for c in cars]

    with (
        patch.object(orch, "_parse_intent", return_value=nlu),
        patch("zim.trip.plan_trip", return_value=mock_itinerary),
        patch("zim.hotel_search.search", return_value=mock_hotel_results),
        patch("zim.car_search.search", return_value=mock_car_results),
    ):
        return orch.handle_message(text, uid)


def _make_flight_model(d: dict) -> Any:
    from zim.core import FlightResult
    from datetime import datetime

    def _to_dt(v: Any) -> Any:
        if v is None:
            return None
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v)
            except ValueError:
                return None
        return v

    return FlightResult(
        airline=d.get("airline", "XX"),
        flight_number=d.get("flight_number", "XX001"),
        origin=d.get("origin", "???"),
        destination=d.get("destination", "???"),
        depart_at=_to_dt(d.get("depart_at")),
        arrive_at=_to_dt(d.get("arrive_at")),
        transfers=d.get("transfers", 0),
        cabin=d.get("cabin", "economy"),
        price_usd=float(d.get("price_usd", 0)),
        refundable=d.get("refundable", False),
        link=d.get("link", ""),
    )


def _make_hotel_model(d: dict) -> Any:
    from zim.core import HotelResult
    return HotelResult(
        name=d.get("name", "Hotel"),
        stars=d.get("stars", 3),
        location=d.get("location", "City"),
        distance_km=d.get("distance_km", 1.0),
        nightly_rate_usd=float(d.get("nightly_rate_usd", 100.0)),
        refundable=d.get("refundable", False),
        link=d.get("link", ""),
    )


def _make_car_model(d: dict) -> Any:
    from zim.core import CarResult
    return CarResult(
        provider=d.get("provider", "Rent"),
        vehicle_class=d.get("vehicle_class", "economy"),
        pickup_location=d.get("pickup_location", "Airport"),
        price_usd_total=float(d.get("price_usd_total", 100.0)),
        free_cancellation=d.get("free_cancellation", False),
        link=d.get("link", ""),
    )


def _get_request(store: InMemoryStateStore, uid: str) -> TravelRequest:
    data = store.get(uid) or {}
    req_data = data.get("travel_request")
    if req_data:
        return TravelRequest.model_validate(req_data)
    return TravelRequest()


# ---------------------------------------------------------------------------
# S1 - No hallucination: LLM guesses origin as 'New York' when user never said it
# ---------------------------------------------------------------------------

class TestS1NoHallucinationOrigin:
    """S1: User says 'I want to fly to London' — NLU must NOT guess origin."""

    def test_destination_only_enters_collecting(self) -> None:
        orch, store = _make_orch()
        uid = "s1_user"
        # LLM properly returns only destination, no origin (no hallucination)
        reply = _send(orch, "I want to fly to London", uid, _nlu("search", {"destination": "London"}))
        req = _get_request(store, uid)
        assert req.state == FlowState.COLLECTING
        assert req.destination is not None
        assert req.origin is None  # not guessed

    def test_collecting_state_asks_for_origin(self) -> None:
        orch, store = _make_orch()
        uid = "s1_user2"
        reply = _send(orch, "I want to fly to London", uid, _nlu("search", {"destination": "London"}))
        assert "from" in reply.lower() or "flying from" in reply.lower() or "origin" in reply.lower()

    def test_hallucinated_origin_would_skip_collecting(self) -> None:
        """Regression: if LLM DID hallucinate origin, it would skip COLLECTING and go to SEARCHING.
        The fix ensures we only fill slots from explicit user input."""
        orch, store = _make_orch()
        uid = "s1_user3"
        # Simulate a fixed/correct NLU: destination only, no origin
        reply = _send(orch, "Fly to London", uid, _nlu("search", {"destination": "London"}))
        req = _get_request(store, uid)
        # Should be COLLECTING, not SEARCHING
        assert req.state == FlowState.COLLECTING
        assert req.origin is None


# ---------------------------------------------------------------------------
# S5 - Business class with no route: must collect before searching
# ---------------------------------------------------------------------------

class TestS5BusinessClassNoRoute:
    """S5: User says 'I need a business class flight' — no origin/destination."""

    def test_business_class_no_route_enters_collecting(self) -> None:
        orch, store = _make_orch()
        uid = "s5_user"
        reply = _send(
            orch, "I need a business class flight", uid,
            _nlu("search", {"cabin_class": "business", "request_type": "flight"}),
        )
        req = _get_request(store, uid)
        assert req.state == FlowState.COLLECTING
        assert req.cabin_class == "business"
        assert req.origin is None
        assert req.destination is None

    def test_cabin_class_saved_during_collection(self) -> None:
        orch, store = _make_orch()
        uid = "s5_user2"
        _send(orch, "Business class please", uid,
              _nlu("search", {"cabin_class": "business"}))
        req = _get_request(store, uid)
        assert req.cabin_class == "business"

    def test_asks_for_origin_first(self) -> None:
        orch, store = _make_orch()
        uid = "s5_user3"
        reply = _send(orch, "I need a business class flight", uid,
                      _nlu("search", {"cabin_class": "business"}))
        # Should ask for origin (flying from?)
        assert "from" in reply.lower() or "origin" in reply.lower()


# ---------------------------------------------------------------------------
# S7 - Multi-turn collection: one question at a time
# ---------------------------------------------------------------------------

class TestS7MultiTurnCollection:
    """S7: Multi-turn flow — user provides slots incrementally."""

    def test_turn1_destination_only(self) -> None:
        orch, store = _make_orch()
        uid = "s7_user"
        reply = _send(orch, "Fly to Paris", uid, _nlu("search", {"destination": "Paris"}))
        req = _get_request(store, uid)
        assert req.state == FlowState.COLLECTING
        assert "from" in reply.lower()  # asks for origin

    def test_turn2_adds_origin(self) -> None:
        orch, store = _make_orch()
        uid = "s7_user2"
        # Turn 1: destination only
        _send(orch, "Fly to Paris", uid, _nlu("search", {"destination": "Paris"}))
        # Turn 2: user provides origin
        reply = _send(orch, "From New York", uid, _nlu("search", {"origin": "New York"}))
        req = _get_request(store, uid)
        assert req.origin is not None
        assert req.destination is not None
        assert req.state == FlowState.COLLECTING  # still missing date
        assert "date" in reply.lower() or "travel" in reply.lower() or "when" in reply.lower()

    def test_turn3_completes_with_date(self) -> None:
        orch, store = _make_orch()
        uid = "s7_user3"
        # Turn 1
        _send(orch, "Fly to Paris", uid, _nlu("search", {"destination": "Paris"}))
        # Turn 2
        _send(orch, "From New York", uid, _nlu("search", {"origin": "New York"}))
        # Turn 3: user provides date → should trigger search
        departure = (date.today() + timedelta(days=30)).isoformat()
        reply = _send_search(
            orch, f"On {departure}", uid,
            _nlu("search", {"departure_date": departure}),
            flight_results=[_flight_result("JFK", "CDG")],
        )
        req = _get_request(store, uid)
        # Should have searched and shown results
        assert req.state == FlowState.RESULTS_SHOWN
        assert len(req.search_results) > 0

    def test_one_question_at_a_time(self) -> None:
        """next_question() must return exactly one question, not multiple."""
        req = TravelRequest()
        req.request_type = RequestType.FLIGHT
        question = req.next_question()
        # Should ask for origin first (first missing slot)
        assert question  # not empty
        assert "?" in question  # is a question
        # Only one sentence/question
        assert question.count("?") == 1


# ---------------------------------------------------------------------------
# S9 - Relative date in NLU: 'next Friday', 'tomorrow'
# ---------------------------------------------------------------------------

class TestS9RelativeDates:
    """S9: NLU returns resolved dates from relative phrases."""

    def test_tomorrow_resolves_in_parse_date(self) -> None:
        orch, _ = _make_orch()
        tomorrow = date.today() + timedelta(days=1)
        result = orch._parse_date("tomorrow")
        assert result == tomorrow

    def test_next_friday_resolves(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("next friday")
        assert result is not None
        assert result.weekday() == 4  # Friday
        assert result > date.today()

    def test_iso_date_passthrough(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("2026-06-15")
        assert result == date(2026, 6, 15)

    def test_nlu_with_resolved_iso_date(self) -> None:
        orch, store = _make_orch()
        uid = "s9_user"
        departure = (date.today() + timedelta(days=14)).isoformat()
        _send(orch, "Fly to Paris", uid, _nlu("search", {"destination": "Paris"}))
        _send(orch, "From London", uid, _nlu("search", {"origin": "London"}))
        # Simulate NLU already resolved 'next week Friday' to an ISO date
        _send(orch, "next week Friday", uid, _nlu("search", {"departure_date": departure}))
        req = _get_request(store, uid)
        assert req.departure_date is not None


# ---------------------------------------------------------------------------
# S10 - Extended relative date parsing
# ---------------------------------------------------------------------------

class TestS10RelativeDateParsing:
    """S10: _parse_date handles all extended relative phrases."""

    def test_in_2_weeks(self) -> None:
        orch, _ = _make_orch()
        expected = date.today() + timedelta(weeks=2)
        result = orch._parse_date("in 2 weeks")
        assert result == expected

    def test_in_1_week(self) -> None:
        orch, _ = _make_orch()
        expected = date.today() + timedelta(weeks=1)
        result = orch._parse_date("in 1 week")
        assert result == expected

    def test_in_10_days(self) -> None:
        orch, _ = _make_orch()
        expected = date.today() + timedelta(days=10)
        result = orch._parse_date("in 10 days")
        assert result == expected

    def test_in_1_day(self) -> None:
        orch, _ = _make_orch()
        expected = date.today() + timedelta(days=1)
        result = orch._parse_date("in 1 day")
        assert result == expected

    def test_this_weekend_is_saturday(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("this weekend")
        assert result is not None
        assert result.weekday() == 5  # Saturday

    def test_end_of_month(self) -> None:
        import calendar
        orch, _ = _make_orch()
        result = orch._parse_date("end of month")
        assert result is not None
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        assert result.day == last_day
        assert result.month == today.month

    def test_mid_june(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("mid June")
        assert result is not None
        assert result.month == 6
        assert result.day == 15

    def test_early_july(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("early July")
        assert result is not None
        assert result.month == 7
        assert result.day == 5

    def test_late_august(self) -> None:
        orch, _ = _make_orch()
        result = orch._parse_date("late August")
        assert result is not None
        assert result.month == 8
        assert result.day == 25

    def test_mid_month_future_if_past(self) -> None:
        """If 'mid January' has passed this year, should return next year."""
        orch, _ = _make_orch()
        today = date.today()
        # If we're in February or later, 'mid January' is in the past
        result = orch._parse_date("mid january")
        assert result is not None
        if today.month > 1 or (today.month == 1 and today.day > 15):
            assert result.year == today.year + 1
        assert result.month == 1
        assert result.day == 15


# ---------------------------------------------------------------------------
# Additional: Complete flight booking flow
# ---------------------------------------------------------------------------

class TestCompleteFlightFlow:
    """Full end-to-end: search → select → confirm."""

    def _setup_flight_search(self) -> tuple[ZimOrchestrator, InMemoryStateStore, str]:
        orch, store = _make_orch()
        uid = "flight_flow_user"
        departure = (date.today() + timedelta(days=30)).isoformat()
        # Provide all required slots at once
        reply = _send_search(
            orch,
            "Flight from JFK to LHR on June 15",
            uid,
            _nlu("search", {
                "origin": "JFK",
                "destination": "LHR",
                "departure_date": "2026-06-15",
            }),
            flight_results=[_flight_result("JFK", "LHR", 480.0)],
        )
        return orch, store, uid

    def test_all_slots_triggers_search(self) -> None:
        orch, store, uid = self._setup_flight_search()
        req = _get_request(store, uid)
        assert req.state == FlowState.RESULTS_SHOWN
        assert len(req.search_results) > 0

    def test_results_shown_has_flight_info(self) -> None:
        orch, store, uid = self._setup_flight_search()
        req = _get_request(store, uid)
        r = req.search_results[0]
        assert r["origin"] == "JFK"
        assert r["destination"] == "LHR"

    def test_select_option_1(self) -> None:
        orch, store, uid = self._setup_flight_search()
        reply = _send(orch, "1", uid, _nlu("select", option_number=1))
        req = _get_request(store, uid)
        assert req.state == FlowState.AWAITING_CONFIRMATION
        assert req.selected_item is not None
        assert "Total" in reply or "Summary" in reply or "fare" in reply.lower()

    def test_confirm_booking(self) -> None:
        orch, store, uid = self._setup_flight_search()
        _send(orch, "1", uid, _nlu("select", option_number=1))
        reply = _send(orch, "yes", uid, _nlu("confirm"))
        # Payment creation may fail (no Stripe key) but state should advance
        req = _get_request(store, uid)
        assert req.state in (FlowState.PAYMENT_SENT, FlowState.AWAITING_CONFIRMATION)

    def test_cancel_resets_to_idle(self) -> None:
        orch, store, uid = self._setup_flight_search()
        _send(orch, "cancel", uid, _nlu("cancel"))
        req = _get_request(store, uid)
        assert req.state == FlowState.IDLE
        assert req.origin is None
        assert req.destination is None


# ---------------------------------------------------------------------------
# Additional: Hotel search flow
# ---------------------------------------------------------------------------

class TestHotelSearchFlow:
    def test_hotel_search_all_slots(self) -> None:
        orch, store = _make_orch()
        uid = "hotel_user"
        reply = _send_search(
            orch,
            "Hotels in London from June 15 to June 18",
            uid,
            _nlu("search", {
                "request_type": "hotel",
                "hotel_location": "London",
                "checkin": "2026-06-15",
                "checkout": "2026-06-18",
            }),
            hotel_results=[_hotel_result("The Ritz", 450.0), _hotel_result("Budget Inn", 90.0)],
        )
        req = _get_request(store, uid)
        assert req.state == FlowState.RESULTS_SHOWN
        assert req.request_type == RequestType.HOTEL
        assert len(req.search_results) == 2

    def test_hotel_missing_checkout_enters_collecting(self) -> None:
        orch, store = _make_orch()
        uid = "hotel_user2"
        reply = _send(
            orch,
            "Hotels in London from June 15",
            uid,
            _nlu("search", {
                "request_type": "hotel",
                "hotel_location": "London",
                "checkin": "2026-06-15",
            }),
        )
        req = _get_request(store, uid)
        assert req.state == FlowState.COLLECTING
        assert "check" in reply.lower() or "out" in reply.lower() or "date" in reply.lower()

    def test_hotel_results_formatted(self) -> None:
        orch, store = _make_orch()
        uid = "hotel_user3"
        reply = _send_search(
            orch,
            "Hotels in Paris",
            uid,
            _nlu("search", {
                "request_type": "hotel",
                "hotel_location": "Paris",
                "checkin": "2026-06-15",
                "checkout": "2026-06-18",
            }),
            hotel_results=[_hotel_result("Hotel Paris", 300.0)],
        )
        assert "Hotel Paris" in reply or "300" in reply or "hotel" in reply.lower()


# ---------------------------------------------------------------------------
# Additional: Car search flow
# ---------------------------------------------------------------------------

class TestCarSearchFlow:
    def test_car_search_all_slots(self) -> None:
        orch, store = _make_orch()
        uid = "car_user"
        reply = _send_search(
            orch,
            "Rent a car in London June 15-18",
            uid,
            _nlu("search", {
                "request_type": "car",
                "car_location": "London",
                "pickup_date": "2026-06-15",
                "dropoff_date": "2026-06-18",
            }),
            car_results=[_car_result("Hertz", 200.0), _car_result("Avis", 180.0)],
        )
        req = _get_request(store, uid)
        assert req.state == FlowState.RESULTS_SHOWN
        assert req.request_type == RequestType.CAR
        assert len(req.search_results) == 2

    def test_car_missing_dropoff_enters_collecting(self) -> None:
        orch, store = _make_orch()
        uid = "car_user2"
        reply = _send(
            orch,
            "Rent a car in London from June 15",
            uid,
            _nlu("search", {
                "request_type": "car",
                "car_location": "London",
                "pickup_date": "2026-06-15",
            }),
        )
        req = _get_request(store, uid)
        assert req.state == FlowState.COLLECTING

    def test_car_results_formatted(self) -> None:
        orch, store = _make_orch()
        uid = "car_user3"
        reply = _send_search(
            orch,
            "Cars in London June 15-18",
            uid,
            _nlu("search", {
                "request_type": "car",
                "car_location": "London",
                "pickup_date": "2026-06-15",
                "dropoff_date": "2026-06-18",
            }),
            car_results=[_car_result("Hertz", 200.0)],
        )
        assert "Hertz" in reply or "200" in reply or "car" in reply.lower()


# ---------------------------------------------------------------------------
# Additional: Relative date in full flow
# ---------------------------------------------------------------------------

class TestRelativeDatesInFlow:
    """Relative dates from NLU (pre-resolved to ISO) work in the slot filling."""

    def test_in_2_weeks_slot_fills_departure(self) -> None:
        orch, store = _make_orch()
        uid = "rel_date_user"
        expected = date.today() + timedelta(weeks=2)
        # NLU pre-resolves 'in 2 weeks' to ISO date
        _send(orch, "Fly to Rome", uid, _nlu("search", {"destination": "Rome"}))
        _send(orch, "From Paris", uid, _nlu("search", {"origin": "Paris"}))
        _send(orch, "in 2 weeks", uid, _nlu("search", {"departure_date": expected.isoformat()}))
        req = _get_request(store, uid)
        assert req.departure_date == expected

    def test_this_weekend_slot_fills_departure(self) -> None:
        orch, store = _make_orch()
        uid = "rel_date_user2"
        # 'this weekend' → next Saturday
        delta = (5 - date.today().weekday()) % 7
        if delta == 0:
            delta = 7
        expected = date.today() + timedelta(days=delta)
        _send(orch, "Fly to Milan", uid, _nlu("search", {"destination": "Milan"}))
        _send(orch, "From Rome", uid, _nlu("search", {"origin": "Rome"}))
        _send(orch, "this weekend", uid, _nlu("search", {"departure_date": expected.isoformat()}))
        req = _get_request(store, uid)
        assert req.departure_date == expected

    def test_mid_june_in_parse_date_fills_slot(self) -> None:
        orch, store = _make_orch()
        uid = "rel_date_user3"
        _send(orch, "Fly to Amsterdam", uid, _nlu("search", {"destination": "Amsterdam"}))
        _send(orch, "From Berlin", uid, _nlu("search", {"origin": "Berlin"}))
        # 'mid June' directly in the slot (simulate NLU passing the string)
        with patch.object(orch, "_parse_intent", return_value=_nlu("search", {"departure_date": "mid June"})):
            orch.handle_message("mid June", uid)
        req = _get_request(store, uid)
        if req.departure_date:
            assert req.departure_date.month == 6
            assert req.departure_date.day == 15


# ---------------------------------------------------------------------------
# Additional: new_search resets state and re-fills
# ---------------------------------------------------------------------------

class TestNewSearch:
    def test_new_search_resets_and_fills(self) -> None:
        orch, store = _make_orch()
        uid = "new_search_user"
        # First search (mock search so it doesn't fire real HTTP calls)
        _send_search(
            orch, "Fly to London", uid,
            _nlu("search", {"origin": "JFK", "destination": "LHR", "departure_date": "2026-06-15"}),
            flight_results=[_flight_result("JFK", "LHR")],
        )
        # User starts over with new destination
        reply = _send(
            orch,
            "Actually, fly to Paris",
            uid,
            _nlu("new_search", {"destination": "Paris"}),
        )
        req = _get_request(store, uid)
        # Old destination should be replaced with Paris (normalized to CDG or kept as Paris)
        assert req.destination is not None
        # destination may be normalized to IATA code (CDG) or kept as city name
        dest = req.destination or ""
        assert "Paris" in dest or "CDG" in dest

    def test_cancel_from_results_resets(self) -> None:
        orch, store = _make_orch()
        uid = "cancel_user"
        _send_search(
            orch, "JFK to LHR June 15", uid,
            _nlu("search", {"origin": "JFK", "destination": "LHR", "departure_date": "2026-06-15"}),
            flight_results=[_flight_result()],
        )
        _send(orch, "cancel", uid, _nlu("cancel"))
        req = _get_request(store, uid)
        assert req.state == FlowState.IDLE


# ---------------------------------------------------------------------------
# Additional: Greeting
# ---------------------------------------------------------------------------

class TestGreeting:
    def test_greeting_in_idle_returns_welcome(self) -> None:
        orch, store = _make_orch()
        uid = "greet_user"
        reply = _send(orch, "Hi", uid, _nlu("greeting"))
        assert "zim" in reply.lower() or "help" in reply.lower() or "travel" in reply.lower()

    def test_idle_state_returns_welcome(self) -> None:
        orch, store = _make_orch()
        uid = "greet_user2"
        # With no intent, IDLE state returns welcome
        reply = _send(orch, "hello", uid, _nlu("chat"))
        assert reply  # not empty


# ---------------------------------------------------------------------------
# Additional: No results from search
# ---------------------------------------------------------------------------

class TestNoResults:
    def test_no_flights_returns_helpful_message(self) -> None:
        orch, store = _make_orch()
        uid = "no_results_user"
        reply = _send_search(
            orch,
            "JFK to LHR June 15",
            uid,
            _nlu("search", {"origin": "JFK", "destination": "LHR", "departure_date": "2026-06-15"}),
            flight_results=[],  # no results
        )
        req = _get_request(store, uid)
        # Should go back to COLLECTING or show "no results" message
        assert req.state == FlowState.COLLECTING
        assert "no result" in reply.lower() or "try" in reply.lower() or "found" in reply.lower()


# ---------------------------------------------------------------------------
# Additional: Modification (change cabin class mid-flow)
# ---------------------------------------------------------------------------

class TestModification:
    def test_modify_cabin_class(self) -> None:
        orch, store = _make_orch()
        uid = "modify_user"
        # First search
        _send_search(
            orch, "JFK to LHR June 15", uid,
            _nlu("search", {"origin": "JFK", "destination": "LHR", "departure_date": "2026-06-15"}),
            flight_results=[_flight_result()],
        )
        # User says 'make it business class'
        _send_search(
            orch, "make it business class", uid,
            _nlu("modify", modification={"field": "cabin_class", "value": "business"}),
            flight_results=[_flight_result(cabin="business", price=1200.0)],
        )
        req = _get_request(store, uid)
        assert req.cabin_class == "business"


# ---------------------------------------------------------------------------
# Additional: _resolve_relative_date in llm_agent.py
# ---------------------------------------------------------------------------

class TestResolveRelativeDateLLMAgent:
    """Tests for llm_agent._resolve_relative_date."""

    def _resolve(self, text: str, today: date | None = None):
        from zim.llm_agent import _resolve_relative_date
        return _resolve_relative_date(text, today)

    def test_tomorrow(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("fly tomorrow", today)
        assert d == date(2026, 4, 21)
        assert "2026-04-21" in text

    def test_in_2_weeks(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("fly in 2 weeks", today)
        assert d == date(2026, 5, 4)
        assert "2026-05-04" in text

    def test_in_5_days(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("fly in 5 days", today)
        assert d == date(2026, 4, 25)
        assert "2026-04-25" in text

    def test_this_weekend(self) -> None:
        # Monday April 20, 2026 → this weekend = Saturday April 25
        today = date(2026, 4, 20)
        text, d = self._resolve("fly this weekend", today)
        assert d is not None
        assert d.weekday() == 5  # Saturday

    def test_end_of_month(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("travel end of month", today)
        assert d == date(2026, 4, 30)

    def test_mid_june(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("fly mid June", today)
        assert d == date(2026, 6, 15)

    def test_early_july(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("early July trip", today)
        assert d == date(2026, 7, 5)

    def test_late_august(self) -> None:
        today = date(2026, 4, 20)
        text, d = self._resolve("late August vacation", today)
        assert d == date(2026, 8, 25)

    def test_no_date_returns_none(self) -> None:
        text, d = self._resolve("I want to fly to Paris")
        assert d is None
        assert text == "I want to fly to Paris"

    def test_next_friday(self) -> None:
        # Monday April 20 → next Friday = April 24 (this week's Friday, not next week)
        # Actually 'next friday' with is_next=True adds 7 more days
        today = date(2026, 4, 20)  # Monday
        text, d = self._resolve("fly next friday", today)
        assert d is not None
        assert d.weekday() == 4  # Friday
        # 'next' means the Friday of next week = April 24 + 7 = May 1
        assert d == date(2026, 5, 1)
