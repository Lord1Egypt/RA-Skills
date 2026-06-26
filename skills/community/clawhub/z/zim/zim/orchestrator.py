"""Stateful travel orchestration engine for Zim.

The LLM handles NLU (understanding user intent via structured JSON output).
This module handles everything else: state transitions, validation, search
execution, result formatting, and payment creation.

Architecture
------------
ZimOrchestrator.handle_message()
  └─ _load_request()          restore TravelRequest from store
  └─ _parse_intent()          LLM → structured JSON {action, slots, ...}
  └─ _apply_intent()          fill slots, validate, transition state machine
  └─ _execute()               run action for current state → WhatsApp reply
  └─ _save_request()          persist updated TravelRequest
"""

from __future__ import annotations

import json
import logging
import os
import random
from datetime import date, datetime, timedelta
from typing import Any

import httpx

from zim.state_store import SQLiteStateStore, StateStore
from zim.travel_request import FlowState, RequestType, TravelRequest

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-3-haiku"

_NLU_SYSTEM_PROMPT = """\
You are Zim's NLU parser. Extract the user's intent from their message.

Current request state:
{current_state_json}

Return a JSON object with:
- action: one of [search, select, confirm, modify, cancel, new_search, greeting, offtopic, help, info_question]
- slots: object with any new/updated travel details:
  - origin: city name or IATA code (ONLY if the user explicitly stated it)
  - destination: city name or IATA code (ONLY if the user explicitly stated it)
  - departure_date: ISO date string YYYY-MM-DD (resolve relative dates against today: {today}).
    Supported relative phrases: 'tomorrow', 'next friday', 'this weekend' (→ next Saturday),
    'end of month' (→ last day of current month), 'in N days', 'in N weeks',
    'early <Month>' (→ 5th), 'mid <Month>' (→ 15th), 'late <Month>' (→ 25th).
  - return_date: ISO date string (if mentioned)
  - cabin_class: economy/business/first (if mentioned)
  - travelers: integer (if mentioned)
  - hotel_location: city name (if mentioned)
  - checkin: ISO date string (if mentioned)
  - checkout: ISO date string (if mentioned)
  - budget: number (if mentioned)
  - request_type: flight/hotel/car/trip (if the user is clearly asking for a specific type)
- option_number: integer if user selected a numbered option (1-based), else null
- modification: {{"field": "<field>", "value": "<value>"}} if user wants to change a specific field, else null

RULES:
- CRITICAL: Only extract what the user EXPLICITLY states. Do NOT guess or infer origin,
  destination, or dates if the user has not mentioned them. Leave those slots absent.
- CRITICAL: If a required field is missing (origin for flights, destination, dates), set
  action to "search" but do NOT fill in guessed values — leave those slots absent entirely.
  The state machine will handle asking the user for the missing information.
- For relative dates, resolve against today ({today}) using the patterns described above.
- "ASAP", "next available", "as soon as possible", "immediately", "today" → departure_date: today ({today})
- "yes", "confirm", "go ahead", "book it", "sounds good" after a summary → action: confirm
- A bare number like "2" or "option 3" after results are shown → action: select, option_number: N
- If user switches intent mid-conversation (e.g. from hotel to flight, or mentions a new travel type), set request_type accordingly AND set action to "new_search" to reset state while preserving new slots.
- If origin and destination are the same city/airport, set a slot "same_origin_dest" to true.
- If the message is gibberish, emojis only, or completely unintelligible, set action to "greeting" so the bot introduces itself.
- Correct obvious city name typos: "dubii"→"Dubai", "londin"→"London", "pais"→"Paris" etc. Extract the corrected city name.
- "KL" as a city abbreviation means Kuala Lumpur (airport: KUL).
- "none of these", "don't like these", "not interested" after results → action: "modify" (triggers re-search prompt)
- "anything cheaper", "cheaper options", "lower price" after results → action: "modify" with modification: {{"field": "budget", "value": "lower"}}
- Questions like "does option X include baggage?", "what airline is option X?", "is option X refundable?" → action: "info_question" with option_number: X. These are informational, NOT selections.
- Return ONLY valid JSON, no explanation\
"""


class ZimOrchestrator:
    """Stateful travel orchestration engine.

    The LLM handles NLU (understanding user intent).
    This class handles everything else: state, validation, execution.
    """

    def __init__(
        self,
        store: StateStore | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.store: StateStore = store or SQLiteStateStore()
        self._api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")
        self._model = model or os.environ.get("ZIM_LLM_MODEL", "") or DEFAULT_MODEL

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def handle_message(self, text: str, user_id: str) -> str:
        """Process an inbound WhatsApp message and return a text reply."""
        request = self._load_request(user_id)

        try:
            intent = self._parse_intent(text, request)
        except Exception as exc:
            logger.warning("NLU parse failed for user %s: %s", user_id[:12], exc)
            intent = {"action": "chat", "slots": {}, "option_number": None, "modification": None}

        request = self._apply_intent(intent, request)
        reply = self._execute(request, user_id)
        self._save_request(user_id, request)
        return reply

    # ------------------------------------------------------------------
    # State persistence
    # ------------------------------------------------------------------

    def _load_request(self, user_id: str) -> TravelRequest:
        data = self.store.get(user_id) or {}
        req_data = data.get("travel_request")
        if req_data:
            try:
                return TravelRequest.model_validate(req_data)
            except Exception as exc:
                logger.warning("Could not deserialize TravelRequest: %s", exc)
        return TravelRequest()

    def _save_request(self, user_id: str, request: TravelRequest) -> None:
        data = self.store.get(user_id) or {}
        data["travel_request"] = request.model_dump(mode="json")
        self.store.save(user_id, data)

    # ------------------------------------------------------------------
    # NLU: LLM extracts intent as structured JSON
    # ------------------------------------------------------------------

    def _parse_intent(self, text: str, request: TravelRequest) -> dict[str, Any]:
        """Call OpenRouter with structured output to extract intent."""
        today = date.today().isoformat()
        current_state = {
            "state": request.state.value,
            "request_type": request.request_type.value,
            "origin": request.origin,
            "destination": request.destination,
            "departure_date": request.departure_date.isoformat() if request.departure_date else None,
            "return_date": request.return_date.isoformat() if request.return_date else None,
            "cabin_class": request.cabin_class,
            "travelers": request.travelers,
            "hotel_location": request.hotel_location,
            "checkin": request.checkin.isoformat() if request.checkin else None,
            "checkout": request.checkout.isoformat() if request.checkout else None,
            "has_results": len(request.search_results) > 0,
            "results_count": len(request.search_results),
        }

        system_content = _NLU_SYSTEM_PROMPT.format(
            current_state_json=json.dumps(current_state, indent=2),
            today=today,
        )

        with httpx.Client(timeout=20.0) as client:
            resp = client.post(
                OPENROUTER_API_URL,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "HTTP-Referer": "https://zim.travel",
                    "X-Title": "Zim NLU",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self._model,
                    "messages": [
                        {"role": "system", "content": system_content},
                        {"role": "user", "content": text},
                    ],
                    "response_format": {"type": "json_object"},
                    "temperature": 0,
                },
            )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    # ------------------------------------------------------------------
    # State machine: apply intent → update TravelRequest
    # ------------------------------------------------------------------

    def _apply_intent(self, intent: dict[str, Any], request: TravelRequest) -> TravelRequest:
        """Apply parsed intent to the travel request state."""
        action = intent.get("action", "chat")
        slots = intent.get("slots") or {}
        option_number = intent.get("option_number")
        modification = intent.get("modification")

        # --- Reset on cancel / new search ---
        if action in ("cancel", "new_search"):
            prefs = request.preferences
            request = TravelRequest()
            request.preferences = prefs
            if action == "new_search":
                # Fall through to fill any slots provided with the new search
                pass
            else:
                return request  # cancel → IDLE, nothing more to do

        # --- Set request type from slots ---
        if "request_type" in slots and slots["request_type"]:
            try:
                request.request_type = RequestType(slots["request_type"])
            except ValueError:
                pass
        elif action in ("search", "new_search") and request.state == FlowState.IDLE:
            # Infer type from which slots are present
            has_hotel = "hotel_location" in slots or ("checkin" in slots and "origin" not in slots)
            has_car = "car_location" in slots or "pickup_date" in slots
            if has_hotel and not has_car:
                request.request_type = RequestType.HOTEL
            elif has_car:
                request.request_type = RequestType.CAR
            else:
                request.request_type = RequestType.FLIGHT

        # --- Fill slots ---
        self._fill_slots(slots, request)

        # --- Same origin/destination check ---
        if (slots.get("same_origin_dest") or
            (request.origin and request.destination and
             request.origin.upper() == request.destination.upper())):
            request.origin = None
            request.destination = None
            request.state = FlowState.COLLECTING
            request._same_origin_dest_error = True
            return request

        # Apply modification (e.g. user says "make it business class")
        if modification and isinstance(modification, dict):
            mod_field = modification.get("field")
            mod_value = modification.get("value")
            if mod_field and mod_value is not None:
                if mod_field == "budget" and mod_value == "lower":
                    # User wants cheaper — re-search with note
                    request._wants_cheaper = True
                else:
                    self._fill_slots({mod_field: mod_value}, request)

        # --- State transitions ---
        if action in ("search", "modify", "new_search"):
            missing = request.missing_slots()
            if missing:
                request.state = FlowState.COLLECTING
            else:
                # If user wants cheaper or declined results, re-search
                if getattr(request, '_wants_cheaper', False):
                    request.state = FlowState.SEARCHING
                    request.search_results = []
                    request.selected_index = None
                    request.selected_item = None
                elif action == "modify" and request.state == FlowState.RESULTS_SHOWN:
                    # If modification has a real field change, re-search
                    if modification and isinstance(modification, dict) and modification.get("field") and modification.get("value") != "lower":
                        request.state = FlowState.SEARCHING
                        request.search_results = []
                        request.selected_index = None
                        request.selected_item = None
                    else:
                        # User declined or wants different options
                        request.state = FlowState.COLLECTING
                        request._declined_results = True
                else:
                    request.state = FlowState.SEARCHING
                    request.search_results = []
                    request.selected_index = None
                    request.selected_item = None

        elif action == "select" and option_number is not None:
            results = request.search_results
            idx = int(option_number) - 1
            if 0 <= idx < len(results):
                request.selected_index = idx
                request.selected_item = results[idx]
                request.state = FlowState.OPTION_SELECTED
            # else: invalid selection — stay in RESULTS_SHOWN, _execute will prompt

        elif action == "confirm":
            # Only meaningful in AWAITING_CONFIRMATION (or OPTION_SELECTED)
            # _execute handles the actual payment creation
            pass

        elif action == "info_question":
            # User is asking about a specific option but NOT selecting it
            # Stay in RESULTS_SHOWN, _execute will prompt them
            if option_number is not None:
                request._info_question_option = option_number
            pass

        elif action == "greeting":
            if request.state == FlowState.IDLE:
                pass  # _execute returns greeting
            # else: in mid-flow, just keep state

        return request

    def _fill_slots(self, slots: dict[str, Any], request: TravelRequest) -> None:
        """Fill TravelRequest slots from a dict. Normalizes airports and dates."""
        from zim.airports import normalize_airport

        if "origin" in slots and slots["origin"]:
            try:
                request.origin = normalize_airport(str(slots["origin"]))
            except ValueError:
                v = str(slots["origin"])
                request.origin = v.upper() if len(v) == 3 else v

        if "destination" in slots and slots["destination"]:
            try:
                request.destination = normalize_airport(str(slots["destination"]))
            except ValueError:
                v = str(slots["destination"])
                request.destination = v.upper() if len(v) == 3 else v

        if "departure_date" in slots and slots["departure_date"]:
            d = self._parse_date(str(slots["departure_date"]))
            if d and d >= date.today():
                request.departure_date = d

        if "return_date" in slots and slots["return_date"]:
            d = self._parse_date(str(slots["return_date"]))
            if d:
                request.return_date = d

        if "cabin_class" in slots and slots["cabin_class"]:
            cc = str(slots["cabin_class"]).lower()
            if cc in ("economy", "business", "first"):
                request.cabin_class = cc

        if "travelers" in slots and slots["travelers"] is not None:
            try:
                request.travelers = max(1, int(slots["travelers"]))
            except (ValueError, TypeError):
                pass

        if "hotel_location" in slots and slots["hotel_location"]:
            request.hotel_location = str(slots["hotel_location"])

        if "checkin" in slots and slots["checkin"]:
            d = self._parse_date(str(slots["checkin"]))
            if d and d >= date.today():
                request.checkin = d

        if "checkout" in slots and slots["checkout"]:
            d = self._parse_date(str(slots["checkout"]))
            if d:
                request.checkout = d

        if "budget" in slots and slots["budget"] is not None:
            try:
                request.hotel_budget = float(slots["budget"])
            except (ValueError, TypeError):
                pass

        if "car_location" in slots and slots["car_location"]:
            request.car_location = str(slots["car_location"])

        if "pickup_date" in slots and slots["pickup_date"]:
            d = self._parse_date(str(slots["pickup_date"]))
            if d and d >= date.today():
                request.pickup_date = d

        if "dropoff_date" in slots and slots["dropoff_date"]:
            d = self._parse_date(str(slots["dropoff_date"]))
            if d:
                request.dropoff_date = d

    def _parse_date(self, value: str) -> date | None:
        """Parse an ISO date string or common relative phrases."""
        if not value:
            return None
        # ISO format
        try:
            return date.fromisoformat(value[:10])
        except (ValueError, TypeError):
            pass
        # Relative phrases
        import calendar
        import re
        lower = value.strip().lower()
        today = date.today()

        if lower == "tomorrow":
            return today + timedelta(days=1)

        # 'in N days'
        m = re.search(r"\bin\s+(\d+)\s+days?\b", lower)
        if m:
            return today + timedelta(days=int(m.group(1)))

        # 'in N weeks'
        m = re.search(r"\bin\s+(\d+)\s+weeks?\b", lower)
        if m:
            return today + timedelta(weeks=int(m.group(1)))

        # 'this weekend' → next Saturday
        if re.search(r"\bthis\s+weekend\b|\bweekend\b", lower):
            delta = (5 - today.weekday()) % 7
            if delta == 0:
                delta = 7
            return today + timedelta(days=delta)

        # 'end of month'
        if re.search(r"\bend\s+of\s+(the\s+)?month\b", lower):
            last_day = calendar.monthrange(today.year, today.month)[1]
            return today.replace(day=last_day)

        # 'early/mid/late <Month>' → 5th / 15th / 25th
        _months = {
            "january": 1, "february": 2, "march": 3, "april": 4,
            "may": 5, "june": 6, "july": 7, "august": 8,
            "september": 9, "october": 10, "november": 11, "december": 12,
        }
        m = re.search(
            r"\b(early|mid|late)\s+"
            r"(january|february|march|april|may|june|july|august|september|october|november|december)\b",
            lower,
        )
        if m:
            period_day = {"early": 5, "mid": 15, "late": 25}[m.group(1)]
            month_num = _months[m.group(2)]
            year = today.year
            target = date(year, month_num, period_day)
            if target < today:
                target = date(year + 1, month_num, period_day)
            return target

        # Named weekdays: 'next friday', 'friday', etc.
        weekdays = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6,
        }
        m = re.search(r"\b(next\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", lower)
        if m:
            is_next = bool(m.group(1))
            wd_name = m.group(2)
            target_wd = weekdays[wd_name]
            delta = (target_wd - today.weekday()) % 7
            if delta == 0:
                delta = 7
            if is_next:
                delta += 7
            return today + timedelta(days=delta)

        return None

    # ------------------------------------------------------------------
    # Executor: produce WhatsApp reply based on current state
    # ------------------------------------------------------------------

    def _execute(self, request: TravelRequest, user_id: str) -> str:
        """Execute action for current state. Returns WhatsApp message."""
        state = request.state

        if state == FlowState.IDLE:
            return (
                "Hey! 👋 I'm Zim, your travel assistant. "
                "I can help you find flights, hotels, and car rentals. "
                "Where would you like to go? 🌍"
            )

        elif state == FlowState.COLLECTING:
            # Check for same origin/dest error
            if getattr(request, '_same_origin_dest_error', False):
                request._same_origin_dest_error = False
                return (
                    "Your origin and destination can't be the same city! "
                    "Where would you like to fly to? 🌍"
                )
            # Check if user declined results
            if getattr(request, '_declined_results', False):
                request._declined_results = False
                return (
                    "No worries! Would you like to try different dates, "
                    "a different destination, or search for something else? 😊"
                )
            return request.next_question()

        elif state == FlowState.SEARCHING:
            # Check if user wants cheaper
            wants_cheaper = getattr(request, '_wants_cheaper', False)
            if wants_cheaper:
                request._wants_cheaper = False
            try:
                results = self._search(request)
            except Exception as exc:
                # Retry once after a short delay (handles transient API errors)
                import time as _time
                logger.warning("Search failed for user %s, retrying: %s", user_id[:12], exc)
                _time.sleep(2)
                try:
                    results = self._search(request)
                except Exception as exc2:
                    logger.exception("Search retry also failed for user %s: %s", user_id[:12], exc2)
                    request.state = FlowState.COLLECTING
                    return "Hmm, I had trouble searching just now. Could you try again? 🙏"

            request.search_results = results
            if not results:
                request.state = FlowState.COLLECTING
                return (
                    "No results found for those dates — "
                    "want to try different dates or a nearby airport? 😊"
                )
            request.state = FlowState.RESULTS_SHOWN
            prefix = ""
            if wants_cheaper:
                prefix = "These are the cheapest options I found for this route:\n\n"
            return prefix + self._format_results(request)

        elif state == FlowState.RESULTS_SHOWN:
            info_opt = getattr(request, '_info_question_option', None)
            if info_opt is not None:
                request._info_question_option = None
                results = request.search_results
                idx = int(info_opt) - 1
                if 0 <= idx < len(results):
                    r = results[idx]
                    airline = r.get('airline', 'the airline')
                    return (
                        f"Option {info_opt} is with {airline}. "
                        "For details like baggage and refund policies, "
                        "you'd check with the airline after booking. "
                        f"Want to go with option {info_opt}, or pick another? 😊"
                    )
            count = len(request.search_results)
            return f"Which one would you like? Just pick a number (1–{count}) 😊"

        elif state == FlowState.OPTION_SELECTED:
            summary = self._format_booking_summary(request)
            request.state = FlowState.AWAITING_CONFIRMATION
            return summary

        elif state == FlowState.AWAITING_CONFIRMATION:
            return self._create_payment(request)

        elif state == FlowState.PAYMENT_SENT:
            return (
                "Your payment link is on its way! 🎉 "
                "Complete payment to lock in your booking. "
                f"Reference: {request.booking_id}"
            )

        elif state == FlowState.COMPLETED:
            return (
                f"Your booking {request.booking_id} is confirmed! 🎉 "
                "Need anything else? I'm here to help! ✈️"
            )

        return "What else can I help you with? ✈️🏨🚗"

    # ------------------------------------------------------------------
    # Search execution
    # ------------------------------------------------------------------

    def _search(self, request: TravelRequest) -> list[dict]:
        rt = request.request_type
        if rt == RequestType.FLIGHT:
            return self._search_flights(request)
        elif rt == RequestType.HOTEL:
            return self._search_hotels(request)
        elif rt == RequestType.CAR:
            return self._search_cars(request)
        elif rt == RequestType.TRIP:
            return self._search_flights(request)
        return []

    def _search_flights(self, request: TravelRequest) -> list[dict]:
        from zim.trip import plan_trip

        itinerary = plan_trip(
            origin=request.origin,
            destination=request.destination,
            departure=request.departure_date,
            return_date=request.return_date,
            mode="personal",
        )
        raw = [f.model_dump() for f in itinerary.flights]
        return self._normalize_results(raw, "flight")

    def _search_hotels(self, request: TravelRequest) -> list[dict]:
        from zim import hotel_search

        location = request.hotel_location or request.destination
        checkin = request.checkin or request.departure_date
        checkout = request.checkout

        if not location or not checkin or not checkout:
            return []

        results = hotel_search.search(
            location=location,
            checkin=checkin,
            checkout=checkout,
            adults=request.guests,
        )
        return self._normalize_results([h.model_dump() for h in results], "hotel")

    def _search_cars(self, request: TravelRequest) -> list[dict]:
        from zim import car_search

        results = car_search.search(
            location=request.car_location,
            pickup=request.pickup_date,
            dropoff=request.dropoff_date,
        )
        return self._normalize_results([c.model_dump() for c in results], "car")

    def _normalize_results(self, results: list[dict], category: str) -> list[dict]:
        """Filter out bad results, deduplicate, sort by price, cap at 5."""
        seen: set[str] = set()
        normalized = []

        for r in results:
            if category == "flight":
                price = float(r.get("price_usd", 0) or 0)
                if price <= 0:
                    continue
                if not r.get("origin") or not r.get("destination"):
                    continue
                dep_str = str(r.get("depart_at", ""))[:10]
                fn = r.get("flight_number", "")
                route = f"{r.get('origin', '')}_{r.get('destination', '')}"
                # Dedup by flight number + route (not date — same flight at different prices is a dupe)
                key = f"{fn}_{route}" if fn else f"{route}_{dep_str}_{price}"
                # Ensure display fields exist
                r.setdefault("airline", "Airline")
                r.setdefault("flight_number", "")
                r.setdefault("cabin", "economy")
                r.setdefault("transfers", 0)
                r.setdefault("depart_at", None)
                r.setdefault("arrive_at", None)
            elif category == "hotel":
                price = float(r.get("nightly_rate_usd", 0) or 0)
                if price <= 0:
                    continue
                key = f"{r.get('name', '')}_{r.get('location', '')}"
            else:  # car
                price = float(r.get("price_usd_total", 0) or 0)
                key = f"{r.get('provider', '')}_{r.get('vehicle_class', '')}"

            if key in seen:
                continue
            seen.add(key)
            normalized.append(r)

        # Sort by price ascending
        def price_key(r: dict) -> float:
            if category == "flight":
                return float(r.get("price_usd", 0) or 0)
            elif category == "hotel":
                return float(r.get("nightly_rate_usd", 0) or 0)
            return float(r.get("price_usd_total", 0) or 0)

        normalized.sort(key=price_key)
        return normalized[:5]

    # ------------------------------------------------------------------
    # Result formatting (deterministic, no LLM)
    # ------------------------------------------------------------------

    def _format_results(self, request: TravelRequest) -> str:
        results = request.search_results
        rt = request.request_type

        lines = []
        for i, r in enumerate(results, 1):
            if rt in (RequestType.FLIGHT, RequestType.TRIP):
                lines.append(self._fmt_flight(r, i, request.departure_date))
            elif rt == RequestType.HOTEL:
                lines.append(self._fmt_hotel(r, i))
            elif rt == RequestType.CAR:
                lines.append(self._fmt_car(r, i))

        body = "\n\n".join(lines)

        if rt in (RequestType.FLIGHT, RequestType.TRIP):
            dep_str = ""
            if request.departure_date:
                dep_str = f" on {request.departure_date.strftime('%b %d, %Y')}"
            header = f"✈️ Flights from {request.origin} to {request.destination}{dep_str}:"
        elif rt == RequestType.HOTEL:
            loc = request.hotel_location or request.destination or "your destination"
            date_range = ""
            if request.checkin and request.checkout:
                date_range = f" ({request.checkin.strftime('%b %d')} – {request.checkout.strftime('%b %d')})"
            header = f"🏨 Hotels in {loc}{date_range}:"
        else:
            header = f"🚗 Car rentals in {request.car_location}:"

        return f"{header}\n\n{body}\n\nWhich one catches your eye? Just reply with a number 😊"

    def _fmt_flight(self, r: dict, idx: int, travel_date: date | None = None) -> str:
        def hhmm(v: Any) -> str:
            if v is None:
                return "TBC"
            if hasattr(v, "strftime"):
                return v.strftime("%H:%M")
            s = str(v)
            return s[11:16] if len(s) > 10 else s

        airline = r.get("airline") or "Airline"
        fn = r.get("flight_number") or ""
        origin = r.get("origin", "")
        dest = r.get("destination", "")
        dep = hhmm(r.get("depart_at"))
        arr = hhmm(r.get("arrive_at"))
        cabin = (r.get("cabin") or "economy").capitalize()
        transfers = r.get("transfers", 0)
        price = float(r.get("price_usd", 0) or 0)

        # Date display
        date_str = ""
        if travel_date:
            date_str = f" · {travel_date.strftime('%b %d')}"

        # Clean timing display: show departure only if arrival unknown
        if dep != "TBC" and arr != "TBC":
            timing = f"{dep} → {arr}"
        elif dep != "TBC":
            timing = dep
        else:
            timing = "Time TBC"
        stops = "Direct" if transfers == 0 else f"{transfers} stop{'s' if transfers > 1 else ''}"

        return (
            f"{idx}. ✈️ {airline} {fn}".strip() + "\n"
            f"   {origin} → {dest} | {timing}{date_str}\n"
            f"   {cabin} · {stops} · ${price:,.2f}"
        )

    def _fmt_hotel(self, r: dict, idx: int) -> str:
        name = r.get("name", "Hotel")
        stars = r.get("stars", 0)
        stars_str = "★" * int(stars) if stars else ""
        location = r.get("location", "")
        rate = float(r.get("nightly_rate_usd", 0) or 0)
        refundable = r.get("refundable", False)

        amenity_str = " · Free cancellation" if refundable else ""

        return (
            f"{idx}. 🏨 {name} {stars_str}".strip() + "\n"
            f"   {location}\n"
            f"   ${rate:,.2f}/night{amenity_str}"
        )

    def _fmt_car(self, r: dict, idx: int) -> str:
        provider = r.get("provider", "Provider")
        cls = (r.get("vehicle_class") or "vehicle").capitalize()
        location = r.get("pickup_location", "")
        total = float(r.get("price_usd_total", 0) or 0)
        free_cancel = r.get("free_cancellation", False)

        cancel_str = " · Free cancellation" if free_cancel else ""

        return (
            f"{idx}. 🚗 {provider} — {cls}\n"
            f"   Pickup: {location}\n"
            f"   ${total:,.2f} est. total{cancel_str}"
        )

    # ------------------------------------------------------------------
    # Booking summary (deterministic)
    # ------------------------------------------------------------------

    def _format_booking_summary(self, request: TravelRequest) -> str:
        from zim.fees import calculate_fee

        item = request.selected_item
        if not item:
            return "No option selected. Please choose from the results."

        rt = request.request_type
        booking_id = f"ZIM-{date.today().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"

        if rt in (RequestType.FLIGHT, RequestType.TRIP):
            base_price = float(item.get("price_usd", 0) or 0)
            airline = item.get("airline", "")
            fn = item.get("flight_number", "")
            origin = item.get("origin", "")
            dest = item.get("destination", "")
            cabin = (item.get("cabin") or "economy").capitalize()
            transfers = item.get("transfers", 0)
            stops = "Direct" if transfers == 0 else f"{transfers} stop(s)"

            depart_raw = item.get("depart_at")
            if depart_raw:
                try:
                    dt = datetime.fromisoformat(str(depart_raw)[:19])
                    date_str = dt.strftime("%b %d, %Y")
                except (ValueError, TypeError):
                    date_str = str(depart_raw)[:10]
            else:
                date_str = request.departure_date.strftime("%b %d, %Y") if request.departure_date else ""

            breakdown = calculate_fee(base_price)
            request.booking_id = booking_id
            request.base_price = base_price
            request.fee = breakdown.fee_amount_usd
            request.total_price = breakdown.total_usd

            return (
                f"✈️ *Booking Summary*\n\n"
                f"{airline} {fn} | {origin} → {dest}\n"
                f"{date_str} | {cabin} | {stops}\n\n"
                f"Base fare: ${base_price:,.2f}\n"
                f"Zim service fee: ${breakdown.fee_amount_usd:,.2f}\n"
                f"*Total: ${breakdown.total_usd:,.2f}*\n\n"
                f"Looks good? Reply *YES* to confirm and I'll send your payment link! 🎉"
            )

        elif rt == RequestType.HOTEL:
            base_per_night = float(item.get("nightly_rate_usd", 0) or 0)
            name = item.get("name", "Hotel")
            location = item.get("location", "")
            stars = item.get("stars", 0)
            stars_str = "★" * int(stars) if stars else ""

            checkin = request.checkin or request.departure_date
            checkout = request.checkout
            nights = max((checkout - checkin).days, 1) if checkin and checkout else 1
            total_base = base_per_night * nights

            breakdown = calculate_fee(total_base)
            request.booking_id = booking_id
            request.base_price = total_base
            request.fee = breakdown.fee_amount_usd
            request.total_price = breakdown.total_usd

            return (
                f"🏨 *Booking Summary*\n\n"
                f"{name} {stars_str} | {location}\n"
                f"{nights} night(s) · ${base_per_night:,.2f}/night\n\n"
                f"Base total: ${total_base:,.2f}\n"
                f"Zim service fee: ${breakdown.fee_amount_usd:,.2f}\n"
                f"*Total: ${breakdown.total_usd:,.2f}*\n\n"
                f"Looks good? Reply *YES* to confirm and I'll send your payment link! 🎉"
            )

        else:  # CAR
            base_price = float(item.get("price_usd_total", 0) or 0)
            provider = item.get("provider", "")
            cls = (item.get("vehicle_class") or "vehicle").capitalize()
            pickup = item.get("pickup_location", "")

            breakdown = calculate_fee(base_price)
            request.booking_id = booking_id
            request.base_price = base_price
            request.fee = breakdown.fee_amount_usd
            request.total_price = breakdown.total_usd

            return (
                f"🚗 *Booking Summary*\n\n"
                f"{provider} — {cls}\n"
                f"Pickup: {pickup}\n\n"
                f"Base total: ${base_price:,.2f}\n"
                f"Zim service fee: ${breakdown.fee_amount_usd:,.2f}\n"
                f"*Total: ${breakdown.total_usd:,.2f}*\n\n"
                f"Looks good? Reply *YES* to confirm and I'll send your payment link! 🎉"
            )

    # ------------------------------------------------------------------
    # Payment creation
    # ------------------------------------------------------------------

    def _create_payment(self, request: TravelRequest) -> str:
        """Create Stripe checkout session and return payment link."""
        item = request.selected_item
        if not item:
            return "No booking pending. Please select an option from the results first."

        booking_id = request.booking_id or f"ZIM-{date.today().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        base_price = request.base_price or 0.0
        fee = request.fee or 0.0
        rt = request.request_type

        if rt in (RequestType.FLIGHT, RequestType.TRIP):
            desc = (
                f"Flight: {item.get('origin', '?')} → {item.get('destination', '?')} "
                f"({item.get('airline', '')} {item.get('flight_number', '')})".strip()
            )
        elif rt == RequestType.HOTEL:
            desc = f"Hotel: {item.get('name', 'Hotel')}"
        else:
            desc = f"Car rental: {item.get('provider', 'Rental')} {item.get('vehicle_class', '')}".strip()

        try:
            from zim.payment import CheckoutLineItem, StripeConfig, create_checkout_session

            cfg = StripeConfig.from_env()
            if not cfg.is_configured:
                raise EnvironmentError("STRIPE_SECRET_KEY not set")

            line_items = [
                CheckoutLineItem(
                    description=desc,
                    amount_cents=int(round(base_price * 100)),
                    category=rt.value,
                ),
                CheckoutLineItem(
                    description="Zim Service Fee",
                    amount_cents=int(round(fee * 100)),
                    category="service_fee",
                ),
            ]

            result = create_checkout_session(
                booking_id=booking_id,
                line_items=line_items,
            )
            checkout_url = result.checkout_url
            request.payment_url = checkout_url
            request.booking_id = booking_id
            request.state = FlowState.PAYMENT_SENT

            return (
                "Payment link ready! 💳\n\n"
                f"Click here to complete your booking:\n{checkout_url}\n\n"
                "This link expires in 30 minutes.\n"
                f"Your booking reference: {booking_id}\n\n"
                "Once payment is confirmed, I'll send you the booking details!"
            )

        except Exception as exc:
            logger.warning("Stripe checkout failed for %s: %s", booking_id, exc)
            request.state = FlowState.PAYMENT_SENT
            deeplink = item.get("link", "")
            if deeplink:
                return (
                    "Booking is almost ready! Our payment system is being set up. "
                    f"In the meantime, here's a link to book directly:\n{deeplink}"
                )
            return (
                "Booking is almost ready! Our payment system is being set up. "
                "Please try again in a moment or contact robin@skylerlabs.ai for help."
            )
