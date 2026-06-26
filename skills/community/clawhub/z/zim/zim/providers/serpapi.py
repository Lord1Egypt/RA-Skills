"""SerpApi provider for Zim.

Fetches real Google Flights and Google Hotels pricing data via SerpApi's
Google-backed search scrapers.

Supported engines:
  - google_flights  — real flight prices from Google Flights
  - google_hotels   — real hotel prices from Google Hotels

Environment variable:
  SERPAPI_KEY — Your SerpApi API key
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any
from urllib.parse import quote

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SERPAPI_BASE = "https://serpapi.com/search"
DEFAULT_TIMEOUT = 25.0  # SerpApi can be slow on cold searches
DEFAULT_CURRENCY = "USD"
DEFAULT_LANGUAGE = "en"
DEFAULT_COUNTRY = "us"
MAX_FLIGHT_RESULTS = 10
MAX_HOTEL_RESULTS = 10

# Google Flights travel class codes
_TRAVEL_CLASS_MAP: dict[str, str] = {
    "1": "economy",
    "2": "premium_economy",
    "3": "business",
    "4": "first",
}


def _get_api_key() -> str:
    """Return the SerpApi API key from environment.

    Raises:
        EnvironmentError: If SERPAPI_KEY is not set.
    """
    key = os.environ.get("SERPAPI_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            "SERPAPI_KEY is not set. "
            "Export it before using SerpApi: export SERPAPI_KEY=<your-api-key>"
        )
    return key


def _client(**kwargs: Any) -> httpx.Client:
    """Create a pre-configured httpx client for SerpApi."""
    return httpx.Client(timeout=DEFAULT_TIMEOUT, **kwargs)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_serpapi_time(time_str: str | None, ref_date: date) -> datetime | None:
    """Parse a SerpApi time string like '10:30 AM' into a datetime.

    SerpApi returns times without dates, so we attach the reference date.
    Falls back to None on any parse error.
    """
    if not time_str:
        return None
    try:
        t = datetime.strptime(time_str.strip(), "%I:%M %p")
        return datetime(ref_date.year, ref_date.month, ref_date.day, t.hour, t.minute)
    except (ValueError, TypeError):
        return None


def _parse_price(value: str | int | float | None) -> float:
    """Parse a price value from SerpApi, stripping currency symbols."""
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return round(float(value), 2)
    # Strip leading currency symbols / commas (e.g. "$1,234")
    cleaned = str(value).replace(",", "").lstrip("$£€¥₹").strip()
    try:
        return round(float(cleaned), 2)
    except (ValueError, TypeError):
        return 0.0


def _parse_stars_from_class(hotel_class: str | None) -> int:
    """Extract star count from hotel_class string like '4-star hotel'."""
    if not hotel_class:
        return 3
    try:
        return min(max(int(hotel_class.split("-")[0].strip()), 1), 5)
    except (ValueError, IndexError):
        return 3


def _cabin_from_travel_class(tc: str | int | None) -> str:
    """Convert a Google Flights travel_class code to a readable cabin name."""
    if tc is None:
        return "economy"
    return _TRAVEL_CLASS_MAP.get(str(tc), "economy")


def _extract_airline_and_flight(leg: dict[str, Any]) -> tuple[str, str]:
    """Extract airline code and flight number from a flight leg dict."""
    airline = leg.get("airline", "")
    flight_no = leg.get("flight_number", "")
    return airline, flight_no


def _build_google_flights_link(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
) -> str:
    """Build a Google Flights search deeplink as a fallback."""
    if return_date:
        return (
            f"https://www.google.com/travel/flights"
            f"?q=Flights+from+{quote(origin)}+to+{quote(destination)}"
            f"&hl=en"
        )
    return (
        f"https://www.google.com/travel/flights"
        f"?q=Flights+from+{quote(origin)}+to+{quote(destination)}"
        f"&hl=en"
    )


def _build_google_hotels_link(
    location: str,
    checkin: date,
    checkout: date,
) -> str:
    """Build a Google Hotels search deeplink."""
    encoded = quote(location)
    return (
        f"https://www.google.com/travel/hotels/{encoded}"
        f"?q={encoded}"
        f"&dates={checkin.isoformat()},{checkout.isoformat()}"
    )


# ---------------------------------------------------------------------------
# Flight Search
# ---------------------------------------------------------------------------

def search_flights(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    currency: str = DEFAULT_CURRENCY,
    travel_class: int = 1,
) -> list[dict[str, Any]]:
    """Search Google Flights via SerpApi's google_flights engine.

    Args:
        origin: IATA origin airport code.
        destination: IATA destination airport code.
        departure: Outbound departure date.
        return_date: Return date for round-trip; None for one-way.
        currency: Price currency code.
        travel_class: 1=economy, 2=premium_economy, 3=business, 4=first.

    Returns:
        List of raw flight group dicts from SerpApi, or empty list on error.
    """
    params: dict[str, Any] = {
        "engine": "google_flights",
        "departure_id": origin.upper(),
        "arrival_id": destination.upper(),
        "outbound_date": departure.isoformat(),
        "currency": currency,
        "hl": DEFAULT_LANGUAGE,
        "gl": DEFAULT_COUNTRY,
        "travel_class": travel_class,
        "api_key": _get_api_key(),
    }
    if return_date:
        params["return_date"] = return_date.isoformat()
        params["type"] = "1"  # round trip
    else:
        params["type"] = "2"  # one way

    try:
        with _client() as client:
            resp = client.get(SERPAPI_BASE, params=params)
            resp.raise_for_status()
            data = resp.json()

        # SerpApi returns best_flights + other_flights
        best = data.get("best_flights", [])
        others = data.get("other_flights", [])
        combined = (best + others)[:MAX_FLIGHT_RESULTS]
        logger.info(
            "SerpApi google_flights returned %d results (%d best, %d other)",
            len(combined), len(best), len(others),
        )
        return combined

    except EnvironmentError:
        logger.warning("SERPAPI_KEY not set — skipping SerpApi flight search")
        return []
    except httpx.HTTPStatusError as exc:
        logger.warning("SerpApi HTTP error (flights): %s", exc)
        return []
    except httpx.HTTPError as exc:
        logger.warning("SerpApi network error (flights): %s", exc)
        return []


def flight_result_from_raw(
    raw: dict[str, Any],
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
) -> dict[str, Any]:
    """Convert a raw SerpApi google_flights result dict to Zim-compatible fields.

    SerpApi groups an itinerary as a nested structure where ``flights`` is a
    list of legs. We flatten to a single FlightResult using the first leg's
    departure and the last leg's arrival.

    Args:
        raw: Single entry from ``best_flights`` or ``other_flights``.
        origin: Requested origin IATA code (fallback when leg data is absent).
        destination: Requested destination IATA code.
        departure: Requested departure date (used for time parsing).
        return_date: Return date if round-trip.

    Returns:
        Dict matching FlightResult field names.
    """
    legs: list[dict[str, Any]] = raw.get("flights", [])
    first_leg = legs[0] if legs else {}
    last_leg = legs[-1] if legs else {}

    airline, flight_no = _extract_airline_and_flight(first_leg)
    dep_airport = first_leg.get("departure_airport", {})
    arr_airport = last_leg.get("arrival_airport", {})

    dep_time_str: str | None = dep_airport.get("time")
    arr_time_str: str | None = arr_airport.get("time")
    arrive_date = return_date if return_date else departure

    depart_at = _parse_serpapi_time(dep_time_str, departure)
    arrive_at = _parse_serpapi_time(arr_time_str, arrive_date)

    # Count stops: total legs minus 1 = transfers
    transfers = max(len(legs) - 1, 0)

    # Travel class: from first leg
    cabin_code = str(first_leg.get("travel_class", "1"))
    cabin = _cabin_from_travel_class(cabin_code)

    # Price: top-level field on the itinerary dict
    price = _parse_price(raw.get("price"))

    # Booking link — use the departure_token URL or fall back to Google search
    booking_token = raw.get("departure_token", "")
    if booking_token:
        link = (
            f"https://www.google.com/travel/flights"
            f"?token={quote(booking_token)}&hl=en"
        )
    else:
        link = _build_google_flights_link(origin, destination, departure, return_date)

    return {
        "airline": airline,
        "flight_number": flight_no,
        "origin": dep_airport.get("id", origin),
        "destination": arr_airport.get("id", destination),
        "depart_at": depart_at,
        "arrive_at": arrive_at,
        "transfers": transfers,
        "cabin": cabin,
        "price_usd": price,
        "refundable": False,  # SerpApi doesn't expose refundability
        "link": link,
        "_source": "serpapi_google_flights",
    }


# ---------------------------------------------------------------------------
# Hotel Search
# ---------------------------------------------------------------------------

def search_hotels(
    location: str,
    checkin: date,
    checkout: date,
    currency: str = DEFAULT_CURRENCY,
    stars_min: int = 0,
) -> list[dict[str, Any]]:
    """Search Google Hotels via SerpApi's google_hotels engine.

    Args:
        location: Destination city name or IATA code.
        checkin: Check-in date.
        checkout: Check-out date.
        currency: Price currency code.
        stars_min: Minimum star rating (0 = no filter).

    Returns:
        List of raw hotel property dicts from SerpApi, or empty list on error.
    """
    params: dict[str, Any] = {
        "engine": "google_hotels",
        "q": location,
        "check_in_date": checkin.isoformat(),
        "check_out_date": checkout.isoformat(),
        "currency": currency,
        "hl": DEFAULT_LANGUAGE,
        "gl": DEFAULT_COUNTRY,
        "api_key": _get_api_key(),
    }
    if stars_min > 0:
        # Google Hotels doesn't support star filter directly in query,
        # but we filter on our side after fetching.
        pass

    try:
        with _client() as client:
            resp = client.get(SERPAPI_BASE, params=params)
            resp.raise_for_status()
            data = resp.json()

        properties = data.get("properties", [])[:MAX_HOTEL_RESULTS]
        logger.info("SerpApi google_hotels returned %d results for %s", len(properties), location)
        return properties

    except EnvironmentError:
        logger.warning("SERPAPI_KEY not set — skipping SerpApi hotel search")
        return []
    except httpx.HTTPStatusError as exc:
        logger.warning("SerpApi HTTP error (hotels): %s", exc)
        return []
    except httpx.HTTPError as exc:
        logger.warning("SerpApi network error (hotels): %s", exc)
        return []


def hotel_result_from_raw(
    raw: dict[str, Any],
    location: str,
    checkin: date,
    checkout: date,
) -> dict[str, Any]:
    """Convert a raw SerpApi google_hotels property dict to Zim-compatible fields.

    Args:
        raw: Single entry from ``properties`` in the SerpApi response.
        location: Requested location (used as fallback).
        checkin: Check-in date.
        checkout: Check-out date.

    Returns:
        Dict matching HotelResult field names.
    """
    name: str = raw.get("name", f"Hotel in {location}")
    stars = _parse_stars_from_class(raw.get("hotel_class"))

    # Rate per night: prefer structured rate_per_night, fall back to total_rate
    rate_per_night: dict[str, Any] = raw.get("rate_per_night", {})
    price_raw = rate_per_night.get("lowest") or rate_per_night.get("before_taxes_and_fees")
    if price_raw is None:
        total_rate: dict[str, Any] = raw.get("total_rate", {})
        price_raw = total_rate.get("lowest")

    nightly_rate = _parse_price(price_raw)

    # Link — SerpApi provides a direct booking link on the property
    link: str = raw.get("link", _build_google_hotels_link(location, checkin, checkout))

    return {
        "name": name,
        "location": raw.get("neighborhood", location),
        "stars": stars,
        "nightly_rate_usd": nightly_rate,
        "refundable": False,  # SerpApi doesn't expose this consistently
        "link": link,
        "_source": "serpapi_google_hotels",
        "_overall_rating": raw.get("overall_rating"),
        "_review_count": raw.get("reviews"),
    }


# ---------------------------------------------------------------------------
# Validation / Health Check
# ---------------------------------------------------------------------------

def health_check() -> bool:
    """Verify the SerpApi key is configured and accepted.

    Returns:
        True if SERPAPI_KEY is set and a minimal API call succeeds.
    """
    try:
        key = _get_api_key()
    except EnvironmentError:
        return False

    params = {
        "engine": "google_flights",
        "departure_id": "LON",
        "arrival_id": "NYC",
        "outbound_date": date.today().isoformat(),
        "type": "2",
        "currency": "USD",
        "api_key": key,
        "num": 1,
    }
    try:
        with _client() as client:
            resp = client.get(SERPAPI_BASE, params=params)
            return resp.status_code == 200
    except httpx.HTTPError:
        return False


def validate_api_key() -> bool:
    """Check whether SERPAPI_KEY is configured and accepted by the API.

    Returns:
        True if the key is set and the API responds with 200, False otherwise.
    """
    return health_check()
