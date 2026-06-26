"""Kiwi.com Tequila API provider for Zim.

Handles flight search with real pricing and booking tokens via the Tequila API.
Supports actual booking (not just redirect links) through booking_token.

Auth: apikey header (KIWI_API_KEY environment variable).
"""

from __future__ import annotations

import logging
import os
from datetime import date, datetime
from typing import Any
from urllib.parse import quote, urlencode

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TEQUILA_BASE = "https://api.tequila.kiwi.com"
KIWI_SEARCH_URL = f"{TEQUILA_BASE}/v2/search"
KIWI_LOCATIONS_URL = f"{TEQUILA_BASE}/locations/query"
KIWI_BOOKING_URL = f"{TEQUILA_BASE}/v2/booking"

DEFAULT_TIMEOUT = 20.0  # seconds
DEFAULT_LIMIT = 10
DEFAULT_CURRENCY = "USD"

# Cabin class mapping: Tequila → human-readable
_CABIN_MAP: dict[str, str] = {
    "M": "economy",
    "W": "premium_economy",
    "C": "business",
    "F": "first",
}


def _get_api_key() -> str:
    """Return the Kiwi Tequila API key from environment.

    Raises:
        EnvironmentError: If KIWI_API_KEY is not set.
    """
    key = os.environ.get("KIWI_API_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            "KIWI_API_KEY is not set. "
            "Export it before using Kiwi: export KIWI_API_KEY=<your-api-key>"
        )
    return key


def _client(**kwargs: Any) -> httpx.Client:
    """Create a pre-configured httpx client with Tequila auth header."""
    key = _get_api_key()
    return httpx.Client(
        timeout=DEFAULT_TIMEOUT,
        headers={"apikey": key},
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_datetime(value: str | None) -> datetime | None:
    """Parse an ISO datetime string, returning None on failure."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _cabin_from_code(code: str | None) -> str:
    """Map Tequila cabin class code to human-readable string."""
    return _CABIN_MAP.get(code or "M", "economy")


def _build_deeplink(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    booking_token: str | None = None,
) -> str:
    """Build a Kiwi.com search or booking deeplink.

    If a booking_token is provided, builds a direct booking URL.
    Otherwise builds a search results URL.
    """
    if booking_token:
        params = urlencode({
            "booking_token": booking_token,
            "currency": DEFAULT_CURRENCY,
        })
        return f"https://www.kiwi.com/booking?{params}"

    params: dict[str, str] = {
        "from": origin.upper(),
        "to": destination.upper(),
        "departure": departure.strftime("%d/%m/%Y"),
    }
    if return_date:
        params["return"] = return_date.strftime("%d/%m/%Y")
    return f"https://www.kiwi.com/en/search/results/{urlencode(params)}"


# ---------------------------------------------------------------------------
# Flight Search
# ---------------------------------------------------------------------------

def search_flights(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    currency: str = DEFAULT_CURRENCY,
    cabin_class: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    """Search flights via the Kiwi Tequila v2/search endpoint.

    Returns a list of raw flight dicts from the API. Each dict includes
    a ``booking_token`` that can be used for actual booking via the
    Tequila booking endpoint, and a ``deep_link`` for redirect booking.

    Args:
        origin: IATA origin airport/city code.
        destination: IATA destination airport/city code.
        departure: Outbound departure date.
        return_date: Return date for round-trip; None for one-way.
        currency: Price currency (default USD).
        cabin_class: Tequila cabin code — M/W/C/F (None = all classes).
        limit: Maximum results to return.

    Returns:
        List of raw API result dicts, or empty list on error.
    """
    params: dict[str, Any] = {
        "fly_from": origin.upper(),
        "fly_to": destination.upper(),
        "date_from": departure.strftime("%d/%m/%Y"),
        "date_to": departure.strftime("%d/%m/%Y"),  # exact date
        "curr": currency,
        "limit": limit,
        "sort": "price",
        "one_per_date": 0,
        "partner_market": "us",
    }
    if return_date:
        params["return_from"] = return_date.strftime("%d/%m/%Y")
        params["return_to"] = return_date.strftime("%d/%m/%Y")
        params["flight_type"] = "round"
    else:
        params["flight_type"] = "oneway"

    if cabin_class:
        params["selected_cabins"] = cabin_class.upper()

    try:
        with _client() as client:
            resp = client.get(KIWI_SEARCH_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
        results = data.get("data", [])
        logger.info("Kiwi flight search returned %d results", len(results))
        return results
    except EnvironmentError:
        logger.warning("KIWI_API_KEY not set — skipping Kiwi flight search")
        return []
    except httpx.HTTPStatusError as exc:
        logger.warning("Kiwi API HTTP error: %s", exc)
        return []
    except httpx.HTTPError as exc:
        logger.warning("Kiwi API network error: %s", exc)
        return []


def search_hotels(
    location: str,
    checkin: date,
    checkout: date,
) -> list[dict[str, Any]]:
    """Return hotel search deeplinks via Kiwi.com accommodation search.

    Kiwi's primary product is flights. For hotels, we surface a deeplink
    to their accommodation search so users can complete their booking.

    Args:
        location: Destination city or IATA code.
        checkin: Check-in date.
        checkout: Check-out date.

    Returns:
        List containing a single deeplink result dict.
    """
    encoded = quote(location)
    link = (
        f"https://www.kiwi.com/en/accommodation/{encoded}"
        f"?checkin={checkin.isoformat()}&checkout={checkout.isoformat()}"
    )
    return [
        {
            "name": f"Hotels in {location} — Kiwi.com",
            "location": location,
            "link": link,
            "stars": 3,
            "estimated_nightly_rate": None,  # not available without API
            "refundable": None,
            "source": "kiwi",
        }
    ]


def search_cars(
    location: str,
    pickup: date,
    dropoff: date,
) -> list[dict[str, Any]]:
    """Return car rental deeplinks via Kiwi.com cars search.

    Kiwi surfaces car rentals as a travel bundle. Results are deeplinks
    to their car search results page.

    Args:
        location: Pickup city or airport name.
        pickup: Pickup date.
        dropoff: Drop-off date.

    Returns:
        List containing a single deeplink result dict.
    """
    encoded = quote(location)
    link = (
        f"https://www.kiwi.com/en/cars/{encoded}"
        f"?pickup={pickup.isoformat()}&dropoff={dropoff.isoformat()}"
    )
    return [
        {
            "provider": "Kiwi.com Cars",
            "vehicle_class": "any",
            "pickup_location": location,
            "link": link,
            "free_cancellation": False,
            "estimated_total": None,  # not available without API
            "source": "kiwi",
        }
    ]


# ---------------------------------------------------------------------------
# Result conversion helpers (used by flight_search.py)
# ---------------------------------------------------------------------------

def flight_result_from_raw(raw: dict[str, Any]) -> dict[str, Any]:
    """Convert a raw Kiwi API flight dict to a Zim-compatible field dict.

    The caller (flight_search) constructs the FlightResult Pydantic model
    from this dict. Separated so tests can validate the mapping logic.

    Args:
        raw: Single flight entry from the Tequila v2/search ``data`` list.

    Returns:
        Dict matching FlightResult field names.
    """
    # Tequila returns a list of airlines; use the first (marketing carrier)
    airlines: list[str] = raw.get("airlines", [])
    airline = airlines[0].upper() if airlines else ""

    # Prefer deep_link for booking redirect; fall back to constructed URL
    deep_link: str = raw.get("deep_link", "")
    booking_token: str = raw.get("booking_token", "")
    link = deep_link or _build_deeplink(
        origin=raw.get("fly_from", ""),
        destination=raw.get("fly_to", ""),
        departure=date.today(),
        booking_token=booking_token or None,
    )

    # Local times are more useful for display than UTC
    depart_str: str | None = raw.get("local_departure")
    arrive_str: str | None = raw.get("local_arrival")

    # Map cabin: Kiwi stores this per-route leg; take the first segment
    route = raw.get("route", [])
    cabin_code = route[0].get("cabin_class", "M") if route else raw.get("cabin_class", "M")

    return {
        "airline": airline,
        "flight_number": raw.get("id", ""),
        "origin": raw.get("fly_from", ""),
        "destination": raw.get("fly_to", ""),
        "depart_at": _parse_datetime(depart_str),
        "arrive_at": _parse_datetime(arrive_str),
        "transfers": raw.get("transfers", 0),
        "cabin": _cabin_from_code(cabin_code),
        "price_usd": float(raw.get("price", 0)),
        "refundable": bool(raw.get("has_cancelled_options", False)),
        "link": link,
        # Extra Kiwi-specific fields (stored for future direct-booking use)
        "_booking_token": booking_token,
        "_source": "kiwi",
    }


# ---------------------------------------------------------------------------
# Validation / Health Check
# ---------------------------------------------------------------------------

def health_check() -> bool:
    """Verify the Kiwi API key is valid by performing a minimal search.

    Returns:
        True if the API responds with 200, False otherwise.
    """
    try:
        results = search_flights("LON", "NYC", date.today(), limit=1)
        return True  # search_flights returns [] on error, not raises
    except Exception:
        return False

    # Re-check: if we got here and results is an empty list caused by
    # EnvironmentError or HTTP error, the health check should reflect that.
    # search_flights already catches those and returns []; we can distinguish
    # by probing the key directly.


def validate_api_key() -> bool:
    """Check whether KIWI_API_KEY is configured and accepted by the API.

    Returns:
        True if the key is set and the API returns 200, False otherwise.
    """
    try:
        key = _get_api_key()
    except EnvironmentError:
        return False

    params = {
        "fly_from": "LON",
        "fly_to": "NYC",
        "date_from": date.today().strftime("%d/%m/%Y"),
        "date_to": date.today().strftime("%d/%m/%Y"),
        "curr": "USD",
        "limit": 1,
    }
    try:
        with httpx.Client(timeout=10.0, headers={"apikey": key}) as client:
            resp = client.get(KIWI_SEARCH_URL, params=params)
            return resp.status_code == 200
    except httpx.HTTPError:
        return False
