"""Intent parsing helpers for the Zim WhatsApp agent.

This module uses lightweight keyword and pattern matching to extract
structured travel intent from free-form user messages. It intentionally
avoids any LLM dependency so it can run deterministically inside the
Zim package.
"""

from __future__ import annotations

import re
from datetime import UTC, date, datetime, timedelta
from typing import Any

from dateutil import parser as date_parser

from zim.airports import normalize_airport

_TRAVEL_TYPE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "flight": (
        "flight",
        "fly",
        "plane",
        "airfare",
        "ticket",
        "business class",
        "economy",
        "first class",
        "roundtrip",
        "one way",
    ),
    "hotel": (
        "hotel",
        "stay",
        "room",
        "accommodation",
        "resort",
        "check in",
        "check-in",
        "check out",
        "check-out",
    ),
    "car": (
        "car",
        "rental",
        "rent a car",
        "hire a car",
        "suv",
        "pickup",
        "pick up",
        "dropoff",
        "drop off",
    ),
}

_CABIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "first": ("first class", "first"),
    "business": ("business class", "business"),
    "premium_economy": ("premium economy",),
    "economy": ("economy class", "economy", "coach"),
}

_CITY_PATTERN = r"[A-Za-z][A-Za-z .'-]{1,40}"

# Matches any phrase that is likely a date rather than a city/route name.
# Used to guard the roundtrip date regex from matching route patterns like
# "from Dubai to Copenhagen".
_DATE_INDICATOR = re.compile(
    r"\b(\d{1,2}|\d{4}"
    r"|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?"
    r"|jul(?:y)?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
    r"|monday|tuesday|wednesday|thursday|friday|saturday|sunday"
    r"|today|tomorrow|next|this\s+\w+)\b",
    re.IGNORECASE,
)


def _today() -> date:
    return datetime.now(UTC).date()


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _detect_type(message: str) -> str | None:
    lowered = message.lower()
    scores: dict[str, int] = {key: 0 for key in _TRAVEL_TYPE_KEYWORDS}
    for travel_type, keywords in _TRAVEL_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                scores[travel_type] += 1

    best_type = max(scores, key=scores.get)
    return best_type if scores[best_type] > 0 else None


def _detect_cabin_class(message: str) -> str | None:
    lowered = message.lower()
    for cabin, keywords in _CABIN_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return cabin
    return None


def _extract_travelers(message: str) -> int:
    lowered = message.lower()

    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
    }
    for word, value in number_words.items():
        if re.search(rf"\b{word}\s+(traveler|travelers|passenger|passengers|adult|adults|guest|guests)\b", lowered):
            return value

    match = re.search(r"\b(\d+)\s+(traveler|travelers|passenger|passengers|adult|adults|guest|guests)\b", lowered)
    if match:
        return int(match.group(1))

    if "for me and" in lowered or "for 2" in lowered or "for two" in lowered:
        return 2

    return 1


def _extract_hotel_nights(message: str) -> int | None:
    lowered = message.lower()
    match = re.search(r"\b(\d+)\s+night[s]?\b", lowered)
    if match:
        return int(match.group(1))

    word_match = re.search(r"\b(one|two|three|four|five|six|seven)\s+night[s]?\b", lowered)
    if word_match:
        return {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
        }[word_match.group(1)]
    return None


def _safe_normalize_airport(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return normalize_airport(value)
    except ValueError:
        return value.strip().upper() if len(value.strip()) == 3 else value.strip()


def _extract_route(message: str) -> tuple[str | None, str | None]:
    normalized = _normalize_whitespace(message)

    patterns = [
        rf"\bfrom\s+(?P<origin>{_CITY_PATTERN})\s+to\s+(?P<destination>{_CITY_PATTERN})(?:\s+on\b|\s+for\b|\s+next\b|\s+this\b|$)",
        rf"\bto\s+(?P<destination>{_CITY_PATTERN})\s+from\s+(?P<origin>{_CITY_PATTERN})(?:\s+on\b|\s+for\b|\s+next\b|\s+this\b|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            origin = _safe_normalize_airport(match.group("origin"))
            destination = _safe_normalize_airport(match.group("destination"))
            return origin, destination

    destination_match = re.search(rf"\bflight\s+to\s+(?P<destination>{_CITY_PATTERN})(?:\s+on\b|\s+for\b|\s+next\b|\s+this\b|$)", normalized, flags=re.IGNORECASE)
    if destination_match:
        return None, _safe_normalize_airport(destination_match.group("destination"))

    return None, None


def _extract_hotel_destination(message: str) -> str | None:
    normalized = _normalize_whitespace(message)
    patterns = [
        rf"\bhotel\s+in\s+(?P<destination>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
        rf"\bstay\s+in\s+(?P<destination>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
        rf"\broom\s+in\s+(?P<destination>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            return match.group("destination").strip()
    return None


def _extract_car_location(message: str) -> str | None:
    normalized = _normalize_whitespace(message)
    patterns = [
        rf"\bcar\s+in\s+(?P<location>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
        rf"\brent\s+a\s+car\s+in\s+(?P<location>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
        rf"\bpick\s*up\s+in\s+(?P<location>{_CITY_PATTERN})(?:\s+for\b|\s+on\b|\s+next\b|\s+this\b|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if match:
            return match.group("location").strip()
    return None


def _parse_date_phrase(phrase: str, base: date) -> date | None:
    cleaned = phrase.strip(" ,.?!").lower()
    if not cleaned:
        return None

    if cleaned == "today":
        return base
    if cleaned == "tomorrow":
        return base + timedelta(days=1)

    weekday_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }

    if cleaned.startswith("next "):
        target_name = cleaned.replace("next ", "", 1)
        if target_name in weekday_map:
            delta = (weekday_map[target_name] - base.weekday()) % 7
            delta = 7 if delta == 0 else delta
            return base + timedelta(days=delta)
        if target_name == "week":
            return base + timedelta(days=7)

    if cleaned.startswith("this "):
        target_name = cleaned.replace("this ", "", 1)
        if target_name in weekday_map:
            delta = (weekday_map[target_name] - base.weekday()) % 7
            return base + timedelta(days=delta)

    if cleaned in weekday_map:
        delta = (weekday_map[cleaned] - base.weekday()) % 7
        return base + timedelta(days=delta)

    if cleaned == "next week":
        return base + timedelta(days=7)

    try:
        parsed = date_parser.parse(cleaned, default=datetime.combine(base, datetime.min.time()))
        parsed_date = parsed.date()
        if parsed_date < base and re.search(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", cleaned):
            parsed_date = parsed_date.replace(year=base.year + 1)
        return parsed_date
    except (ValueError, OverflowError, TypeError):
        return None


def _extract_explicit_dates(message: str) -> tuple[date | None, date | None]:
    base = _today()
    normalized = _normalize_whitespace(message)

    roundtrip_match = re.search(
        r"\bfrom\s+(?P<departure>[^,]+?)\s+to\s+(?P<return>[^,]+?)(?:$|\s+for\b|\s+with\b)",
        normalized,
        flags=re.IGNORECASE,
    )
    if roundtrip_match:
        dep_phrase = roundtrip_match.group("departure")
        ret_phrase = roundtrip_match.group("return")
        # Only treat as date range if at least one phrase looks like a date.
        # Without this guard, "from Dubai to Copenhagen" is misread as
        # departure="Dubai", return="Copenhagen".
        if _DATE_INDICATOR.search(dep_phrase) or _DATE_INDICATOR.search(ret_phrase):
            departure_date = _parse_date_phrase(dep_phrase, base)
            return_date = _parse_date_phrase(ret_phrase, base)
            if departure_date:
                return departure_date, return_date

    departure_date: date | None = None
    return_date: date | None = None

    on_match = re.search(r"\bon\s+([^,]+?)(?:$|\s+for\b|\s+returning\b|\s+back\b)", normalized, flags=re.IGNORECASE)
    if on_match:
        departure_date = _parse_date_phrase(on_match.group(1), base)

    leaving_match = re.search(r"\b(?:leaving|departing)\s+([^,]+?)(?:$|\s+and\b|\s+for\b|\s+returning\b)", normalized, flags=re.IGNORECASE)
    if leaving_match and departure_date is None:
        departure_date = _parse_date_phrase(leaving_match.group(1), base)

    return_match = re.search(r"\b(?:returning|return|back)\s+(?:on\s+)?([^,]+?)(?:$|\s+for\b|\s+with\b)", normalized, flags=re.IGNORECASE)
    if return_match:
        return_date = _parse_date_phrase(return_match.group(1), base)

    if departure_date is None and "next week" in normalized.lower():
        departure_date = base + timedelta(days=7)

    return departure_date, return_date


def parse_travel_intent(message: str) -> dict[str, Any]:
    """Parse a free-form travel message into a structured dict.

    Returns a stable schema suitable for the WhatsApp agent:
    {
      type, origin, destination, departure_date, return_date,
      travelers, cabin_class, hotel_destination, check_in,
      check_out, guests
    }
    """
    travel_type = _detect_type(message)
    travelers = _extract_travelers(message)
    cabin_class = _detect_cabin_class(message)
    departure_date, return_date = _extract_explicit_dates(message)

    result: dict[str, Any] = {
        "type": travel_type,
        "origin": None,
        "destination": None,
        "departure_date": departure_date.isoformat() if departure_date else None,
        "return_date": return_date.isoformat() if return_date else None,
        "travelers": travelers,
        "cabin_class": cabin_class,
        "hotel_destination": None,
        "check_in": None,
        "check_out": None,
        "guests": travelers,
        "car_location": None,  # explicit pickup city/location for car searches
    }

    if travel_type == "flight":
        origin, destination = _extract_route(message)
        result["origin"] = origin
        result["destination"] = destination

    elif travel_type == "hotel":
        hotel_destination = _extract_hotel_destination(message)
        result["hotel_destination"] = hotel_destination

        check_in = departure_date
        check_out = return_date
        nights = _extract_hotel_nights(message)
        if check_in and nights and not check_out:
            check_out = check_in + timedelta(days=nights)
        elif check_in is None and "next week" in message.lower():
            check_in = _today() + timedelta(days=7)
            if nights:
                check_out = check_in + timedelta(days=nights)

        result["check_in"] = check_in.isoformat() if check_in else None
        result["check_out"] = check_out.isoformat() if check_out else None

    elif travel_type == "car":
        car_location = _extract_car_location(message)
        result["car_location"] = car_location
        result["destination"] = car_location  # keep for backwards compatibility
        result["check_in"] = departure_date.isoformat() if departure_date else None
        result["check_out"] = return_date.isoformat() if return_date else None

    return result
