"""Booking.com Affiliate API provider for Zim.

Searches for hotels via the Booking.com partner API (RapidAPI gateway).
Commission-based affiliate model — approximately 15–25% per booking.

Required environment variables:
  BOOKING_COM_API_KEY       — RapidAPI key granting access to the Booking.com API
  BOOKING_COM_AFFILIATE_ID  — Your Booking.com affiliate ID (aid parameter)

The RapidAPI host used is: booking-com.p.rapidapi.com
"""

from __future__ import annotations

import logging
import os
from datetime import date
from typing import Any
from urllib.parse import urlencode

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAPIDAPI_HOST = "booking-com.p.rapidapi.com"
RAPIDAPI_BASE = f"https://{RAPIDAPI_HOST}"

SEARCH_ENDPOINT = f"{RAPIDAPI_BASE}/v1/hotels/search"
LOCATION_ENDPOINT = f"{RAPIDAPI_BASE}/v1/hotels/locations"

DEFAULT_TIMEOUT = 20.0  # seconds
DEFAULT_CURRENCY = "USD"
DEFAULT_LOCALE = "en-gb"
DEFAULT_ADULTS = 2
DEFAULT_ROOM_COUNT = 1
MAX_RESULTS = 10

# Fallback affiliate ID for deeplink construction when full API is not used
_AFFILIATE_ID_FALLBACK = "1897277"


def _get_api_key() -> str:
    """Return the RapidAPI key for Booking.com from environment.

    Raises:
        EnvironmentError: If BOOKING_COM_API_KEY is not set.
    """
    key = os.environ.get("BOOKING_COM_API_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            "BOOKING_COM_API_KEY is not set. "
            "Export it before using Booking.com search: "
            "export BOOKING_COM_API_KEY=<your-rapidapi-key>"
        )
    return key


def _get_affiliate_id() -> str:
    """Return the Booking.com affiliate ID from environment or fallback."""
    return os.environ.get("BOOKING_COM_AFFILIATE_ID", _AFFILIATE_ID_FALLBACK).strip()


def _client(**kwargs: Any) -> httpx.Client:
    """Create a pre-configured httpx client with RapidAPI auth headers."""
    key = _get_api_key()
    return httpx.Client(
        timeout=DEFAULT_TIMEOUT,
        headers={
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        },
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_deeplink(
    location: str,
    checkin: date,
    checkout: date,
    adults: int = DEFAULT_ADULTS,
) -> str:
    """Build a Booking.com affiliate search deeplink.

    Args:
        location: Destination city or hotel name.
        checkin: Check-in date.
        checkout: Check-out date.
        adults: Number of adult guests.

    Returns:
        Full Booking.com search URL with affiliate ID.
    """
    aid = _get_affiliate_id()
    params = urlencode({
        "ss": location,
        "checkin": checkin.isoformat(),
        "checkout": checkout.isoformat(),
        "group_adults": adults,
        "no_rooms": DEFAULT_ROOM_COUNT,
        "aid": aid,
    })
    return f"https://www.booking.com/searchresults.html?{params}"


def _build_hotel_deeplink(
    hotel_id: str | None,
    location: str,
    checkin: date,
    checkout: date,
    adults: int = DEFAULT_ADULTS,
) -> str:
    """Build a Booking.com property-level deeplink when hotel_id is known."""
    aid = _get_affiliate_id()
    if hotel_id:
        params = urlencode({
            "aid": aid,
            "hotel_id": hotel_id,
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
            "group_adults": adults,
        })
        return f"https://www.booking.com/hotel/gb/property.html?{params}"
    return _build_deeplink(location, checkin, checkout, adults)


def _parse_stars(raw_class: str | int | None) -> int:
    """Parse hotel star class from various API formats."""
    if raw_class is None:
        return 3
    if isinstance(raw_class, int):
        return min(max(raw_class, 1), 5)
    # API sometimes returns "4" or "4.0" as string
    try:
        return min(max(int(float(str(raw_class))), 1), 5)
    except (ValueError, TypeError):
        return 3


def _parse_nightly_rate(raw: dict[str, Any]) -> float:
    """Extract a USD nightly rate from an API result dict.

    Tries several field names used across API versions.
    """
    for field in (
        "price_breakdown.gross_price",
        "min_total_price",
        "composite_price_breakdown.gross_amount.value",
    ):
        parts = field.split(".")
        val = raw
        for part in parts:
            if isinstance(val, dict):
                val = val.get(part)
            else:
                val = None
                break
        if val is not None:
            try:
                return round(float(val), 2)
            except (ValueError, TypeError):
                pass

    # Flat field fallbacks
    for key in ("price_breakdown", "min_total_price", "price"):
        if key in raw:
            v = raw[key]
            if isinstance(v, (int, float)):
                return round(float(v), 2)
            if isinstance(v, dict):
                for sub in ("gross_price", "value", "amount"):
                    if sub in v:
                        try:
                            return round(float(v[sub]), 2)
                        except (ValueError, TypeError):
                            pass

    return 0.0


# ---------------------------------------------------------------------------
# Location lookup
# ---------------------------------------------------------------------------

def get_dest_id(location: str) -> str | None:
    """Resolve a location name to a Booking.com dest_id for search.

    Args:
        location: City, airport name, or IATA code.

    Returns:
        dest_id string if found, or None if lookup fails.
    """
    try:
        with _client() as client:
            resp = client.get(
                LOCATION_ENDPOINT,
                params={
                    "name": location,
                    "locale": DEFAULT_LOCALE,
                },
            )
            resp.raise_for_status()
            results = resp.json()
            if results:
                return str(results[0].get("dest_id", ""))
    except EnvironmentError:
        logger.warning("BOOKING_COM_API_KEY not set — cannot resolve dest_id")
    except httpx.HTTPError as exc:
        logger.warning("Booking.com location lookup failed: %s", exc)

    return None


# ---------------------------------------------------------------------------
# Hotel Search
# ---------------------------------------------------------------------------

def search_hotels(
    location: str,
    checkin: date,
    checkout: date,
    currency: str = DEFAULT_CURRENCY,
    adults: int = DEFAULT_ADULTS,
    stars_min: int = 0,
) -> list[dict[str, Any]]:
    """Search hotels via the Booking.com RapidAPI.

    Attempts a full structured search; falls back to a single deeplink result
    if the API key is absent or the call fails.

    Args:
        location: Destination city or IATA code.
        checkin: Check-in date.
        checkout: Check-out date.
        currency: Price currency code.
        adults: Number of adult guests.
        stars_min: Minimum star rating (0 = no filter).

    Returns:
        List of hotel result dicts with Zim-compatible field names.
    """
    # --- Attempt full API search ---
    dest_id: str | None = None
    try:
        dest_id = get_dest_id(location)
    except Exception as exc:  # noqa: BLE001
        logger.debug("Could not resolve dest_id for %s: %s", location, exc)

    if dest_id:
        try:
            results = _search_by_dest_id(
                dest_id=dest_id,
                checkin=checkin,
                checkout=checkout,
                currency=currency,
                adults=adults,
                stars_min=stars_min,
            )
            if results:
                logger.info(
                    "Booking.com search returned %d results for %s", len(results), location
                )
                return results
        except Exception as exc:  # noqa: BLE001
            logger.warning("Booking.com structured search failed: %s", exc)

    # --- Fallback: single deeplink result ---
    logger.info("Booking.com falling back to deeplink result for %s", location)
    return [
        {
            "name": f"Hotels in {location} — Booking.com",
            "location": location,
            "stars": max(stars_min, 3),
            "nightly_rate_usd": 0.0,  # unknown without API
            "refundable": True,
            "link": _build_deeplink(location, checkin, checkout, adults),
            "_source": "booking_com",
        }
    ]


def _search_by_dest_id(
    dest_id: str,
    checkin: date,
    checkout: date,
    currency: str,
    adults: int,
    stars_min: int,
) -> list[dict[str, Any]]:
    """Run a hotel search given a resolved dest_id.

    Internal helper — raises on HTTP errors so the caller can catch and fall back.
    """
    params: dict[str, Any] = {
        "dest_id": dest_id,
        "dest_type": "city",
        "checkin_date": checkin.isoformat(),
        "checkout_date": checkout.isoformat(),
        "adults_number": adults,
        "room_number": DEFAULT_ROOM_COUNT,
        "currency": currency,
        "locale": DEFAULT_LOCALE,
        "order_by": "popularity",
        "filter_by_currency": currency,
        "page_number": 0,
        "units": "imperial",
        "include_adjacency": "true",
    }
    if stars_min > 0:
        params["star_rating_filter"] = str(stars_min)

    with _client() as client:
        resp = client.get(SEARCH_ENDPOINT, params=params)
        resp.raise_for_status()
        data = resp.json()

    hotels = data.get("result", [])[:MAX_RESULTS]
    results: list[dict[str, Any]] = []
    for h in hotels:
        rate = _parse_nightly_rate(h)
        stars = _parse_stars(h.get("class"))
        if stars_min > 0 and stars < stars_min:
            continue

        hotel_id = str(h.get("hotel_id", ""))
        results.append(
            {
                "name": h.get("hotel_name", f"Hotel in {dest_id}"),
                "location": h.get("city_name_en", h.get("address", "")),
                "stars": stars,
                "nightly_rate_usd": rate,
                "refundable": h.get("is_free_cancellable", False),
                "link": _build_hotel_deeplink(
                    hotel_id, dest_id, checkin, checkout, adults
                ),
                "_source": "booking_com",
                "_hotel_id": hotel_id,
            }
        )
    return results


# ---------------------------------------------------------------------------
# Validation / Health Check
# ---------------------------------------------------------------------------

def health_check() -> bool:
    """Verify the Booking.com API key is configured and accepted.

    Returns:
        True if the API responds successfully, False otherwise.
    """
    try:
        _get_api_key()
    except EnvironmentError:
        return False

    try:
        result = get_dest_id("London")
        return result is not None
    except Exception:  # noqa: BLE001
        return False


def validate_api_key() -> bool:
    """Explicitly validate BOOKING_COM_API_KEY via a minimal API call.

    Returns:
        True if the key is set and the API responds with 200, False otherwise.
    """
    try:
        key = _get_api_key()
    except EnvironmentError:
        return False

    try:
        with httpx.Client(
            timeout=10.0,
            headers={
                "X-RapidAPI-Key": key,
                "X-RapidAPI-Host": RAPIDAPI_HOST,
            },
        ) as client:
            resp = client.get(LOCATION_ENDPOINT, params={"name": "London", "locale": "en-gb"})
            return resp.status_code == 200
    except httpx.HTTPError:
        return False
