"""Travelpayouts API client for Zim.

Handles flight price lookups, deeplink construction, and token validation.
All HTTP calls use httpx with sensible timeouts.
"""

from __future__ import annotations

import logging
import os
from datetime import date
from typing import Any
from urllib.parse import quote, urlencode

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = "https://api.travelpayouts.com"
AVIASALES_BASE = "https://www.aviasales.com"
HOTELLOOK_BASE = "https://search.hotellook.com"

DEFAULT_CURRENCY = "USD"
DEFAULT_TIMEOUT = 15.0  # seconds
DEFAULT_LIMIT = 10

MARKER_FALLBACK = os.environ.get("TRAVELPAYOUTS_MARKER", "")  # Account marker from env


def _get_token() -> str:
    """Return the Travelpayouts API token from environment.

    Raises:
        EnvironmentError: If TRAVELPAYOUTS_TOKEN is not set.
    """
    token = os.environ.get("TRAVELPAYOUTS_TOKEN", "").strip()
    if not token:
        raise EnvironmentError(
            "TRAVELPAYOUTS_TOKEN is not set. "
            "Export it before using Zim: export TRAVELPAYOUTS_TOKEN=<your-token>"
        )
    return token


def _get_marker() -> str:
    """Return the affiliate marker (defaults to account ID)."""
    return os.environ.get("TRAVELPAYOUTS_MARKER", MARKER_FALLBACK)


def _client(**kwargs: Any) -> httpx.Client:
    """Create a pre-configured httpx client."""
    return httpx.Client(timeout=DEFAULT_TIMEOUT, **kwargs)


# ---------------------------------------------------------------------------
# Flight Price Endpoints
# ---------------------------------------------------------------------------

def get_flight_prices_for_dates(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    currency: str = DEFAULT_CURRENCY,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    """Fetch flight prices for specific dates via the Travelpayouts v1 API.

    Endpoint: /v1/prices/direct (or /aviasales/v3/prices_for_dates)
    Returns the raw JSON response dict.
    """
    token = _get_token()

    params: dict[str, Any] = {
        "origin": origin.upper(),
        "destination": destination.upper(),
        "departure_at": departure.isoformat(),
        "currency": currency,
        "sorting": "price",
        "limit": limit,
        "token": token,
        "unique": "false",
    }
    if return_date:
        params["return_at"] = return_date.isoformat()

    url = f"{API_BASE}/aviasales/v3/prices_for_dates"

    with _client() as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    logger.debug("prices_for_dates returned %d results", len(data.get("data", [])))
    return data


def get_cheap_prices(
    origin: str,
    destination: str,
    departure_month: str | None = None,
    currency: str = DEFAULT_CURRENCY,
) -> dict[str, Any]:
    """Fetch cached cheap flight prices (month-level granularity).

    Endpoint: /aviasales/v3/prices_for_dates with month-level query.
    Useful as a fallback when exact-date search returns empty.
    """
    token = _get_token()

    params: dict[str, Any] = {
        "origin": origin.upper(),
        "destination": destination.upper(),
        "currency": currency,
        "sorting": "price",
        "limit": 30,
        "token": token,
    }
    if departure_month:
        # API accepts YYYY-MM format for month-level queries
        params["departure_at"] = departure_month

    url = f"{API_BASE}/aviasales/v3/prices_for_dates"

    with _client() as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Deeplink Builders
# ---------------------------------------------------------------------------

def build_flight_deeplink(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
) -> str:
    """Build an Aviasales affiliate search deeplink.

    Format: https://www.aviasales.com/search/ORIDDMM-DSTDDMM1?marker=MARKER
    """
    marker = _get_marker()
    dep_str = f"{departure.strftime('%d%m')}"
    route = f"{origin.upper()}{dep_str}"

    if return_date:
        ret_str = f"{return_date.strftime('%d%m')}"
        route = f"{route}{destination.upper()}{ret_str}1"
    else:
        route = f"{route}{destination.upper()}1"

    return f"{AVIASALES_BASE}/search/{route}?marker={marker}"


def build_hotel_deeplink(
    location: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
) -> str:
    """Build a Hotellook affiliate search deeplink."""
    marker = _get_marker()
    params = urlencode({
        "destination": location,
        "checkIn": checkin.isoformat(),
        "checkOut": checkout.isoformat(),
        "adults": adults,
        "marker": marker,
    })
    return f"{HOTELLOOK_BASE}/search?{params}"


def build_car_deeplinks(
    location: str,
    pickup: date,
    dropoff: date,
) -> dict[str, str]:
    """Build car rental affiliate deeplinks for multiple providers.

    Returns a dict mapping provider name to search URL.
    """
    marker = _get_marker()
    encoded_loc = quote(location)
    pickup_str = pickup.isoformat()
    dropoff_str = dropoff.isoformat()

    return {
        "rentalcars": (
            f"https://www.rentalcars.com/search"
            f"?location={encoded_loc}"
            f"&puDay={pickup.day}&puMonth={pickup.month}&puYear={pickup.year}"
            f"&doDay={dropoff.day}&doMonth={dropoff.month}&doYear={dropoff.year}"
            f"&driversAge=30"
            f"&affiliateCode={marker}"
        ),
        "kayak": (
            f"https://www.kayak.com/cars/{encoded_loc}/{pickup_str}/{dropoff_str}"
            f"?sort=price_a"
        ),
        "discover_cars": (
            f"https://www.discovercars.com/search"
            f"?location={encoded_loc}"
            f"&pick_up_date={pickup_str}&drop_off_date={dropoff_str}"
            f"&marker={marker}"
        ),
    }


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_token() -> bool:
    """Check whether the configured token is valid by making a test API call.

    Returns True if the token is accepted, False otherwise.
    """
    try:
        token = _get_token()
    except EnvironmentError:
        return False

    url = f"{API_BASE}/aviasales/v3/prices_for_dates"
    params = {
        "origin": "LON",
        "destination": "NYC",
        "currency": "USD",
        "limit": 1,
        "token": token,
    }

    try:
        with _client() as client:
            resp = client.get(url, params=params)
            return resp.status_code == 200
    except httpx.HTTPError:
        return False
