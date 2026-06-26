"""WhatsApp agent for Zim — natural-language travel booking over WhatsApp.

Integrates with OpenClaw's WhatsApp channel. This module bridges
free-form WhatsApp messages to the structured Zim search + booking APIs.

Conversation flow
-----------------
1. User sends a free-form message ("Find me a flight from Dubai to CPH on May 1")
2. parse_travel_intent extracts structured fields
3. Agent searches flights/hotels/cars and presents up to 3 options
4. User picks a number → agent moves to CONFIRMING state, shows summary
5. User sends YES → confirmation text + booking deeplink returned; back to IDLE
   User sends NO  → options list shown again; back to search state

State is persisted via an injected StateStore (SQLite by default; swap for
Redis in multi-process / cloud deployments).

Usage:
    from zim.whatsapp_agent import ZimWhatsAppAgent
    from zim.state_store import SQLiteStateStore

    agent = ZimWhatsAppAgent(state_store=SQLiteStateStore())
    reply = agent.handle_message(
        "Find me a flight from Dubai to Copenhagen on May 1",
        user_id="whatsapp:+971501234567",
    )
"""

from __future__ import annotations

import logging
import re
from datetime import date
from enum import Enum
from typing import Any

import httpx

from zim.core import CarResult, FlightResult, HotelResult
from zim.intent_parser import parse_travel_intent
from zim.state_store import InMemoryStateStore, StateStore
from zim.trip import plan_trip

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Conversation state machine
# ---------------------------------------------------------------------------


class WhatsAppState(str, Enum):
    IDLE = "idle"
    FLIGHT_SEARCH = "flight_search"   # search results presented; awaiting selection
    HOTEL_SEARCH = "hotel_search"
    CAR_SEARCH = "car_search"
    CONFIRMING = "confirming"         # option selected; awaiting YES / NO


_SEARCH_STATES = {WhatsAppState.FLIGHT_SEARCH, WhatsAppState.HOTEL_SEARCH, WhatsAppState.CAR_SEARCH}


def _state_to_category(state: WhatsAppState) -> str:
    mapping = {
        WhatsAppState.FLIGHT_SEARCH: "flight",
        WhatsAppState.HOTEL_SEARCH: "hotel",
        WhatsAppState.CAR_SEARCH: "car",
    }
    return mapping.get(state, "")


# ---------------------------------------------------------------------------
# Per-user conversation context (serialisable)
# ---------------------------------------------------------------------------


class UserContext:
    """All per-user conversation state for one WhatsApp session.

    Fully serialisable to/from a plain dict so any StateStore backend
    (SQLite, Redis, etc.) can persist it.
    """

    def __init__(self) -> None:
        self.state: WhatsAppState = WhatsAppState.IDLE
        self.intent: dict[str, Any] = {}
        self.last_results: dict[str, list[dict[str, Any]]] = {}
        self.selected_index: int | None = None
        # Populated when the user picks an option (CONFIRMING state)
        self.pending_item: dict[str, Any] | None = None
        self.pending_category: str | None = None

    def reset(self) -> None:
        """Return context to its IDLE default."""
        self.state = WhatsAppState.IDLE
        self.intent = {}
        self.last_results = {}
        self.selected_index = None
        self.pending_item = None
        self.pending_category = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state.value,
            "intent": self.intent,
            "last_results": self.last_results,
            "selected_index": self.selected_index,
            "pending_item": self.pending_item,
            "pending_category": self.pending_category,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserContext":
        ctx = cls()
        ctx.state = WhatsAppState(data.get("state", WhatsAppState.IDLE.value))
        ctx.intent = data.get("intent", {})
        ctx.last_results = data.get("last_results", {})
        ctx.selected_index = data.get("selected_index")
        ctx.pending_item = data.get("pending_item")
        ctx.pending_category = data.get("pending_category")
        return ctx


# ---------------------------------------------------------------------------
# Result formatters — WhatsApp-friendly plain text, no markdown tables
# ---------------------------------------------------------------------------


def _format_flight(flight: FlightResult | dict[str, Any], index: int) -> str:
    if isinstance(flight, dict):
        flight = FlightResult(**flight)

    segments: list[str] = []
    if flight.depart_at:
        segments.append(flight.depart_at.strftime("%d %b %H:%M"))
    if flight.arrive_at:
        segments.append(flight.arrive_at.strftime("%H:%M"))
    route = f"{flight.origin} → {flight.destination}"
    timing = " / ".join(segments) if segments else "—"

    status_note = ""
    if flight.policy_status == "out_of_policy":
        status_note = " [exceeds policy]"
    elif flight.policy_status == "approval_required":
        status_note = " [approval needed]"

    lines = [
        f"{index}. {flight.airline or 'Airline'} {flight.flight_number}",
        f"   Route: {route}",
        f"   Time: {timing}",
        f"   Class: {flight.cabin or 'economy'} | Transfers: {flight.transfers}",
        f"   Price: ${flight.price_usd:,.2f}{status_note}",
    ]
    return "\n".join(lines)


def _format_hotel(hotel: HotelResult | dict[str, Any], index: int) -> str:
    if isinstance(hotel, dict):
        hotel = HotelResult(**hotel)

    stars_str = f"{'★' * hotel.stars}" if hotel.stars else ""
    status_note = ""
    if hotel.policy_status == "out_of_policy":
        status_note = " [exceeds policy]"
    elif hotel.policy_status == "approval_required":
        status_note = " [approval needed]"

    price_str = (
        f"${hotel.nightly_rate_usd:,.2f}/night"
        if hotel.nightly_rate_usd
        else "Price on request"
    )

    lines = [
        f"{index}. {hotel.name} {stars_str}",
        f"   Location: {hotel.location}",
        f"   Price: {price_str}{status_note}",
    ]
    return "\n".join(lines)


def _format_car(car: CarResult | dict[str, Any], index: int) -> str:
    if isinstance(car, dict):
        car = CarResult(**car)

    free_cancel = "Free cancellation" if car.free_cancellation else ""
    status_note = ""
    if car.policy_status == "approval_required":
        status_note = " [approval needed]"

    lines = [
        f"{index}. {car.provider} — {car.vehicle_class or 'vehicle'}",
        f"   Pickup: {car.pickup_location}",
        f"   Price: ${car.price_usd_total:,.2f}{status_note}" if car.price_usd_total else f"   {car.provider} — see link to compare prices{status_note}",
    ]
    if free_cancel:
        lines.append(f"   {free_cancel}")
    return "\n".join(lines)


def _result_summary(category: str, results: list[dict[str, Any]], top_n: int = 3) -> str:
    formatted: list[str] = []
    for i, r in enumerate(results[:top_n], start=1):
        if category == "flight":
            formatted.append(_format_flight(r, i))
        elif category == "hotel":
            formatted.append(_format_hotel(r, i))
        elif category == "car":
            formatted.append(_format_car(r, i))
    return "\n\n".join(formatted)


def _build_confirmation_text(category: str, result: dict[str, Any]) -> str:
    """Build a one-line confirmation summary shown before the booking link."""
    if category == "flight":
        f = FlightResult(**result) if isinstance(result, dict) else result
        return (
            f"Flight: {f.airline} {f.flight_number} "
            f"{f.origin} → {f.destination} "
            f"({f.cabin or 'economy'}) at ${f.price_usd:,.2f}"
        )
    elif category == "hotel":
        h = HotelResult(**result) if isinstance(result, dict) else result
        price_str = (
            f"${h.nightly_rate_usd:,.2f}/night" if h.nightly_rate_usd else "on request"
        )
        return f"Hotel: {h.name} at {price_str}"
    elif category == "car":
        c = CarResult(**result) if isinstance(result, dict) else result
        price_note = f"at ${c.price_usd_total:,.2f}" if c.price_usd_total else "(compare prices via link)"
        return f"Car: {c.provider} {c.vehicle_class or ''} {price_note}"
    return "Selection confirmed."


# ---------------------------------------------------------------------------
# Main agent
# ---------------------------------------------------------------------------


class ZimWhatsAppAgent:
    """Natural-language WhatsApp interface for Zim travel booking.

    Flow
    ----
    1. parse_travel_intent → structured fields
    2. search flights / hotels / cars
    3. present up to 3 options (plain text, WhatsApp-friendly)
    4. user picks 1–3 → CONFIRMING state (show summary, ask YES/NO)
    5. YES → confirmation + booking deeplink; NO → show options again

    Args:
        default_traveler_id: Used for policy lookups (single-user MVP).
        state_store:         Where user context is persisted.
                             Defaults to InMemoryStateStore.
    """

    def __init__(
        self,
        default_traveler_id: str = "default",
        state_store: StateStore | None = None,
    ) -> None:
        self.default_traveler_id = default_traveler_id
        self._store: StateStore = state_store or InMemoryStateStore()

    # ------------------------------------------------------------------
    # State persistence helpers
    # ------------------------------------------------------------------

    def _load_ctx(self, user_id: str) -> UserContext:
        raw = self._store.get(user_id)
        return UserContext.from_dict(raw) if raw else UserContext()

    def _save_ctx(self, user_id: str, ctx: UserContext) -> None:
        self._store.save(user_id, ctx.to_dict())

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def handle_message(self, message: str, user_id: str) -> str:
        """Process an inbound WhatsApp message and return a text reply.

        Entry point for the OpenClaw WhatsApp integration.
        State is loaded before and saved after every call.
        """
        ctx = self._load_ctx(user_id)
        text = message.strip()

        try:
            reply = self._dispatch(text, ctx)
        except Exception:
            # Ensure context is not left in a broken state
            ctx.reset()
            raise
        finally:
            self._save_ctx(user_id, ctx)

        return reply

    def _dispatch(self, text: str, ctx: UserContext) -> str:
        """Route the message to the appropriate handler based on current state."""

        # Cancel / start over always works regardless of state
        if self._is_cancel(text):
            return self._handle_cancel(ctx)

        # Awaiting YES/NO confirmation after option selection
        if ctx.state == WhatsAppState.CONFIRMING:
            return self._handle_confirmation(text, ctx)

        # Active search results visible — numeric selection
        if ctx.state in _SEARCH_STATES and self._is_selection(text):
            return self._handle_selection(text, ctx)

        # Parse a fresh intent and run a new search
        intent = parse_travel_intent(text)

        if intent["type"] is None:
            return (
                "I'm not sure what you're looking for.\n\n"
                "Try something like:\n"
                "- Find me a flight from Dubai to Copenhagen on May 1\n"
                "- Book a hotel in London for 3 nights from May 5\n"
                "- I need a car rental in Dubai next Monday"
            )

        missing: list[str] = []
        if intent["type"] == "flight":
            missing = self._missing_flight_fields(intent)
        elif intent["type"] == "hotel":
            missing = self._missing_hotel_fields(intent)

        if missing:
            fields_str = "\n- ".join(missing)
            return (
                "I can help with that! I just need a bit more info:\n"
                f"- {fields_str}\n\n"
                "Could you add those details?"
            )

        return self._run_search(intent, ctx)

    # ------------------------------------------------------------------
    # Search phase — find options and present them
    # ------------------------------------------------------------------

    def _run_search(self, intent: dict[str, Any], ctx: UserContext) -> str:
        """Run the appropriate search and store results in context."""
        travel_type = intent["type"]
        ctx.intent = intent
        ctx.last_results = {}
        ctx.selected_index = None
        ctx.pending_item = None
        ctx.pending_category = None

        try:
            if travel_type == "flight":
                return self._search_flights(intent, ctx)
            elif travel_type == "hotel":
                return self._search_hotels(intent, ctx)
            elif travel_type == "car":
                return self._search_cars(intent, ctx)
            else:
                return "I can help with flights, hotels, and car rentals. What are you looking for?"
        except httpx.TimeoutException:
            logger.warning("Search timed out for user intent: %s", travel_type)
            return "The search took a bit too long. Please try again in a moment."
        except httpx.HTTPStatusError as exc:
            logger.warning("Search API error %s for %s", exc.response.status_code, travel_type)
            return "We're having trouble reaching the search provider right now. Please try again shortly."
        except EnvironmentError:
            logger.error("Missing API token for %s search", travel_type)
            return "Zim isn't fully configured yet. Please contact support."
        except ValueError as exc:
            logger.warning("Value error during %s search: %s", travel_type, exc)
            return (
                f"I couldn't understand the location. Could you rephrase?\n\n"
                "Try something like:\n"
                "- Flight from Stockholm to Ibiza on Friday\n"
                "- Hotels in London from May 5 for 3 nights\n"
                "- Car rental in Dubai next Monday"
            )
        except Exception:
            logger.exception("Unhandled error during %s search", travel_type)
            return "Something went wrong on our end. Please try again, or start a new search."

    def _search_flights(self, intent: dict[str, Any], ctx: UserContext) -> str:
        origin = intent["origin"]
        destination = intent["destination"]
        departure_str = intent["departure_date"]
        return_str = intent["return_date"]

        # Clean up destination — intent parser may include trailing NL text
        if destination:
            # Take only the first word/phrase before common NL connectors
            import re as _re
            destination = _re.split(
                r"\s+(?:are|is|do|does|can|will|would|should|any|on|for|from|with|what|how|please)\b",
                destination, maxsplit=1, flags=_re.IGNORECASE,
            )[0].strip()
            intent["destination"] = destination

        if not origin or not destination or not departure_str:
            return "I need the origin, destination, and departure date to search for flights."

        departure = date.fromisoformat(departure_str)
        return_date = date.fromisoformat(return_str) if return_str else None

        itinerary = plan_trip(
            origin=origin,
            destination=destination,
            departure=departure,
            return_date=return_date,
            mode="personal",
            traveler_id=self.default_traveler_id,
        )

        ctx.last_results["flight"] = [f.model_dump() for f in itinerary.flights]
        ctx.state = WhatsAppState.FLIGHT_SEARCH

        if not itinerary.flights:
            return (
                f"No flights found from {origin} to {destination} on {departure_str}. "
                "Try different dates or nearby airports."
            )

        summary = _result_summary("flight", ctx.last_results["flight"])
        return (
            f"Found {len(itinerary.flights)} flight(s) {origin} → {destination}:\n\n"
            f"{summary}\n\n"
            f"Total: ${itinerary.total_price_usd:,.2f} | Status: {itinerary.status}\n\n"
            "Reply 1, 2, or 3 to select, or describe a change."
        )

    def _search_hotels(self, intent: dict[str, Any], ctx: UserContext) -> str:
        from zim import hotel_search

        location = intent["hotel_destination"]
        checkin_str = intent["check_in"]
        checkout_str = intent["check_out"]
        guests = intent.get("guests", 2)

        if not location or not checkin_str:
            return "I need the hotel destination and check-in date to search."

        checkin = date.fromisoformat(checkin_str)
        checkout = (
            date.fromisoformat(checkout_str)
            if checkout_str
            else checkin
        )

        results = hotel_search.search(
            location=location,
            checkin=checkin,
            checkout=checkout,
            adults=guests,
        )

        ctx.last_results["hotel"] = [h.model_dump() for h in results]
        ctx.state = WhatsAppState.HOTEL_SEARCH

        if not results:
            return f"No hotels found in {location}. Try a different location or dates."

        summary = _result_summary("hotel", ctx.last_results["hotel"])
        return (
            f"Hotels in {location} ({checkin.strftime('%d %b')} → {checkout.strftime('%d %b')}):\n\n"
            f"{summary}\n\n"
            "Reply 1, 2, or 3 to select, or tell me what to change."
        )

    def _search_cars(self, intent: dict[str, Any], ctx: UserContext) -> str:
        from zim import car_search

        # Prefer explicit car_location extracted by the intent parser,
        # fall back to generic destination only if needed.
        location = intent.get("car_location") or intent.get("destination") or ""
        pickup_str = intent.get("check_in")
        dropoff_str = intent.get("check_out")

        if not location:
            return "I need the pickup location to search for car rentals. Which city?"

        pickup = date.fromisoformat(pickup_str) if pickup_str else date.today()
        dropoff = date.fromisoformat(dropoff_str) if dropoff_str else pickup

        results = car_search.search(
            location=location,
            pickup=pickup,
            dropoff=dropoff,
        )

        ctx.last_results["car"] = [c.model_dump() for c in results]
        ctx.state = WhatsAppState.CAR_SEARCH

        if not results:
            return f"No car rentals found in {location}. Try a different city."

        summary = _result_summary("car", ctx.last_results["car"])
        return (
            f"Car rentals in {location} ({pickup.strftime('%d %b')} → {dropoff.strftime('%d %b')}):\n\n"
            f"{summary}\n\n"
            "Reply 1, 2, or 3 to select, or tell me what to change."
        )

    # ------------------------------------------------------------------
    # Booking/checkout phase — selection → confirmation → link
    # ------------------------------------------------------------------

    def _handle_selection(self, text: str, ctx: UserContext) -> str:
        """User picked a numbered option.  Move to CONFIRMING state."""
        match = re.search(r"\b([123])\b", text)
        if not match:
            return "I didn't catch that — reply 1, 2, or 3 to choose an option."

        idx = int(match.group(1)) - 1
        category = _state_to_category(ctx.state)
        results = ctx.last_results.get(category, [])

        if idx >= len(results):
            return f"I only have {len(results)} option(s). Please reply 1–{len(results)}."

        ctx.pending_item = results[idx]
        ctx.pending_category = category
        ctx.selected_index = idx

        summary = _build_confirmation_text(category, ctx.pending_item)
        ctx.state = WhatsAppState.CONFIRMING

        return (
            f"You selected:\n{summary}\n\n"
            "Reply YES to get the booking link, or NO to see other options."
        )

    def _handle_confirmation(self, text: str, ctx: UserContext) -> str:
        """Handle YES / NO after option selection."""
        lowered = text.lower().strip()

        if any(word in lowered for word in ("yes", "yep", "yeah", "confirm", "book", "ok", "go")):
            return self._complete_booking(ctx)

        if any(word in lowered for word in ("no", "nope", "back", "different", "other", "change")):
            return self._reshow_results(ctx)

        return (
            "Reply YES to proceed with this selection, or NO to see other options.\n"
            "(Or type CANCEL to start over.)"
        )

    def _complete_booking(self, ctx: UserContext) -> str:
        """User confirmed — return final confirmation text and deeplink."""
        item = ctx.pending_item
        category = ctx.pending_category

        if not item or not category:
            ctx.reset()
            return "Something went wrong with your selection. Please start a new search."

        summary = _build_confirmation_text(category, item)
        raw_link = item.get("link", "") if isinstance(item, dict) else ""
        link_text = f"\n\nBook here: {raw_link}" if raw_link else ""

        ctx.reset()

        return (
            f"Confirmed! {summary}{link_text}\n\n"
            "Is there anything else I can help with? "
            "Search another flight, hotel, or car rental."
        )

    def _reshow_results(self, ctx: UserContext) -> str:
        """User said NO — restore results and go back to the search state."""
        # Restore search state from pending_category so the user can re-select
        category_to_state = {
            "flight": WhatsAppState.FLIGHT_SEARCH,
            "hotel": WhatsAppState.HOTEL_SEARCH,
            "car": WhatsAppState.CAR_SEARCH,
        }
        category = ctx.pending_category or ""
        ctx.state = category_to_state.get(category, WhatsAppState.IDLE)
        ctx.pending_item = None
        ctx.pending_category = None

        results = ctx.last_results.get(category, [])
        if not results:
            ctx.reset()
            return "I've lost track of those results. Please start a new search."

        summary = _result_summary(category, results)
        return (
            f"Here are your options again:\n\n{summary}\n\n"
            "Reply 1, 2, or 3 to select."
        )

    # ------------------------------------------------------------------
    # Cancel
    # ------------------------------------------------------------------

    def _handle_cancel(self, ctx: UserContext) -> str:
        ctx.reset()
        return (
            "Search cancelled. What would you like to search for?\n\n"
            "Examples:\n"
            "- Flight from Dubai to London on May 10\n"
            "- Hotel in Paris from May 5 for 3 nights\n"
            "- Car rental in Dubai next week"
        )

    # ------------------------------------------------------------------
    # Input classifiers
    # ------------------------------------------------------------------

    @staticmethod
    def _is_selection(text: str) -> bool:
        cleaned = text.strip().lower()
        return bool(
            re.match(r"^(option |#|no\.?)\s*[123]\b", cleaned)
            or re.match(r"^[123]$", cleaned)
            or re.match(r"^\([123]\)$", cleaned)
        )

    @staticmethod
    def _is_cancel(text: str) -> bool:
        lowered = text.lower()
        return any(
            phrase in lowered
            for phrase in ("cancel", "start over", "new search", "never mind", "forget it")
        )

    # ------------------------------------------------------------------
    # Field validators
    # ------------------------------------------------------------------

    @staticmethod
    def _missing_flight_fields(intent: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        if not intent.get("origin"):
            missing.append("origin city or airport")
        if not intent.get("destination"):
            missing.append("destination city or airport")
        if not intent.get("departure_date"):
            missing.append("departure date")
        return missing

    @staticmethod
    def _missing_hotel_fields(intent: dict[str, Any]) -> list[str]:
        missing: list[str] = []
        if not intent.get("hotel_destination"):
            missing.append("hotel city or location")
        if not intent.get("check_in"):
            missing.append("check-in date")
        # check_out is optional — inferred from nights if present
        return missing
