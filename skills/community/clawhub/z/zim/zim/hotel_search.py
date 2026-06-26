"""Hotel search module for Zim.

Searches multiple providers for hotels, merges and deduplicates results,
and returns structured HotelResult objects with affiliate deeplinks.

Provider priority:
  1. Booking.com Affiliate API (real prices via RapidAPI)
  2. SerpApi Google Hotels (real Google prices)
  3. Hotellook deeplink (Travelpayouts partner)
  4. Booking.com deeplink (always available)
  5. Google Hotels deeplink (always available)

Providers with missing API keys are skipped gracefully. Deeplink-based
results use destination-tier estimated nightly rates so that ranking,
policy checks (max_hotel_night), and total price calculation all function
correctly. Prices from real API results are actual rates; estimated prices
are clearly surfaced in the result name.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Optional
from urllib.parse import quote, urlencode

from zim.core import HotelResult, Policy, apply_policy_to_hotel
from zim.providers.travelpayouts import _get_marker
from zim.providers import booking_com as booking_com_provider
from zim.providers import serpapi as serpapi_provider

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Destination price tiers (median 3-4★ nightly rate USD)
# Used for deeplink-only results where real pricing is unavailable.
# ---------------------------------------------------------------------------

_HIGH_TIER: frozenset[str] = frozenset({
    # IATA codes
    "NYC", "JFK", "EWR", "LGA",
    "SFO", "OAK", "SJC",
    "LON", "LHR", "LGW", "STN",
    "PAR", "CDG", "ORY",
    "DXB",
    "SIN",
    "HKG",
    "TYO", "NRT", "HND",
    "SYD",
    "ZUR",
    "GVA",
    "BOS",
    "LAX",
    "SEA",
    "AMS",
    "CPH",
    # City names (title-case)
    "New York", "San Francisco", "London", "Paris", "Dubai",
    "Singapore", "Hong Kong", "Tokyo", "Sydney", "Zurich",
    "Geneva", "Boston", "Los Angeles", "Seattle", "Amsterdam",
    "Copenhagen",
})

_LOW_TIER: frozenset[str] = frozenset({
    # IATA codes
    "BKK", "DMK",
    "KUL",
    "MNL",
    "CGK", "JKT",
    "DPS",
    "HAN",
    "SGN", "HCM",
    "DAD",
    "CMB",
    "DEL",
    "BOM", "BDQ",
    "CCU",
    "HNL",
    # City names
    "Bangkok", "Kuala Lumpur", "Manila", "Jakarta", "Bali",
    "Hanoi", "Ho Chi Minh", "Da Nang", "Colombo",
    "Delhi", "Mumbai", "Calcutta",
})

_NIGHTLY_RATES = {
    "high": 225.0,
    "mid": 160.0,
    "low": 80.0,
}


def _estimate_nightly_rate(location: str) -> float:
    """Return a destination-tier estimated nightly rate (USD)."""
    for check in (location.upper(), location.title(), location):
        if check in _HIGH_TIER:
            return _NIGHTLY_RATES["high"]
        if check in _LOW_TIER:
            return _NIGHTLY_RATES["low"]
    return _NIGHTLY_RATES["mid"]


# ---------------------------------------------------------------------------
# Deeplink builders
# ---------------------------------------------------------------------------

def _build_hotellook_link(
    location: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
) -> str:
    """Build Hotellook affiliate search deeplink."""
    marker = _get_marker()
    params = urlencode({
        "destination": location,
        "checkIn": checkin.isoformat(),
        "checkOut": checkout.isoformat(),
        "adults": adults,
        "marker": marker,
    })
    return f"https://search.hotellook.com/search?{params}"


def _build_booking_link(
    location: str,
    checkin: date,
    checkout: date,
    adults: int = 2,
) -> str:
    """Build Booking.com affiliate search deeplink."""
    marker = _get_marker()
    params = urlencode({
        "ss": location,
        "checkin": checkin.isoformat(),
        "checkout": checkout.isoformat(),
        "group_adults": adults,
        "aid": marker,
    })
    return f"https://www.booking.com/searchresults.html?{params}"


def _build_google_hotels_link(
    location: str,
    checkin: date,
    checkout: date,
) -> str:
    """Build Google Hotels search deeplink."""
    encoded = quote(location)
    return (
        f"https://www.google.com/travel/hotels/{encoded}"
        f"?q={encoded}"
        f"&dates={checkin.isoformat()},{checkout.isoformat()}"
    )


# ---------------------------------------------------------------------------
# Result converters
# ---------------------------------------------------------------------------

def _booking_com_to_hotel_result(raw: dict, location: str) -> HotelResult | None:
    """Convert a Booking.com provider result dict to a HotelResult.

    Returns None if the rate is missing (0.0), so callers can skip
    placeholder results that would break ranking.
    """
    rate = raw.get("nightly_rate_usd", 0.0)
    stars = raw.get("stars", 3)
    name = raw.get("name", f"Hotel in {location}")
    link = raw.get("link", "")
    refundable = bool(raw.get("refundable", False))

    # Skip if no real price data (API returned a fallback deeplink result)
    if rate == 0.0:
        return None

    return HotelResult(
        name=name,
        location=raw.get("location", location),
        stars=stars,
        nightly_rate_usd=rate,
        refundable=refundable,
        link=link,
    )


def _serpapi_to_hotel_result(
    raw: dict,
    location: str,
    checkin: date,
    checkout: date,
) -> HotelResult | None:
    """Convert a SerpApi google_hotels property dict to a HotelResult.

    Returns None if no rate data is available.
    """
    fields = serpapi_provider.hotel_result_from_raw(raw, location, checkin, checkout)
    rate = fields["nightly_rate_usd"]
    if rate == 0.0:
        return None

    return HotelResult(
        name=fields["name"],
        location=fields["location"],
        stars=fields["stars"],
        nightly_rate_usd=rate,
        refundable=fields["refundable"],
        link=fields["link"],
    )


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _dedup_key(result: HotelResult) -> tuple:
    """Return a deduplication key for a HotelResult.

    Hotels with the same name and star rating within ±10 USD nightly rate
    are considered duplicates.
    """
    price_bucket = round(result.nightly_rate_usd / 10) * 10
    return (
        result.name.lower().strip()[:40],
        result.stars,
        price_bucket,
    )


def _merge_and_dedup(result_lists: list[list[HotelResult]]) -> list[HotelResult]:
    """Merge multiple result lists, removing duplicates.

    Earlier lists take precedence when deduplicating.
    """
    seen: set[tuple] = set()
    merged: list[HotelResult] = []
    for results in result_lists:
        for r in results:
            key = _dedup_key(r)
            if key not in seen:
                seen.add(key)
                merged.append(r)
    return merged


# ---------------------------------------------------------------------------
# Provider search functions
# ---------------------------------------------------------------------------

def _search_booking_com(
    location: str,
    checkin: date,
    checkout: date,
    currency: str,
    adults: int,
    stars_min: int,
) -> list[HotelResult]:
    """Fetch hotels from the Booking.com API and convert to HotelResults."""
    raw_results = booking_com_provider.search_hotels(
        location=location,
        checkin=checkin,
        checkout=checkout,
        currency=currency,
        adults=adults,
        stars_min=stars_min,
    )
    results: list[HotelResult] = []
    for raw in raw_results:
        hr = _booking_com_to_hotel_result(raw, location)
        if hr is not None:
            results.append(hr)
    logger.info("Booking.com: %d usable results for %s", len(results), location)
    return results


def _search_serpapi_hotels(
    location: str,
    checkin: date,
    checkout: date,
    currency: str,
    stars_min: int,
) -> list[HotelResult]:
    """Fetch hotels from SerpApi Google Hotels and convert to HotelResults."""
    raw_results = serpapi_provider.search_hotels(
        location=location,
        checkin=checkin,
        checkout=checkout,
        currency=currency,
        stars_min=stars_min,
    )
    results: list[HotelResult] = []
    for raw in raw_results:
        try:
            hr = _serpapi_to_hotel_result(raw, location, checkin, checkout)
            if hr is not None:
                if stars_min > 0 and hr.stars < stars_min:
                    continue
                results.append(hr)
        except Exception as exc:  # noqa: BLE001
            logger.debug("SerpApi hotel conversion error: %s", exc)
    logger.info("SerpApi Google Hotels: %d usable results for %s", len(results), location)
    return results


# ---------------------------------------------------------------------------
# Deeplink-based fallback results
# ---------------------------------------------------------------------------

def _build_deeplink_results(
    location: str,
    checkin: date,
    checkout: date,
    adults: int,
    stars_min: int,
) -> list[HotelResult]:
    """Build the three standard deeplink results with estimated pricing.

    These are always available regardless of API key configuration.
    """
    base_rate = _estimate_nightly_rate(location)
    logger.debug("Hotel deeplink fallback %s: base rate est. $%.0f/night", location, base_rate)

    candidates = [
        HotelResult(
            name=f"Hotels in {location} — Hotellook (est. ${base_rate:.0f}/night)",
            location=location,
            link=_build_hotellook_link(location, checkin, checkout, adults),
            stars=4,
            nightly_rate_usd=round(base_rate, 2),
            refundable=True,
        ),
        HotelResult(
            name=f"Hotels in {location} — Booking.com (est. ${base_rate * 0.85:.0f}/night)",
            location=location,
            link=_build_booking_link(location, checkin, checkout, adults),
            stars=3,
            nightly_rate_usd=round(base_rate * 0.85, 2),
            refundable=True,
        ),
        HotelResult(
            name=f"Hotels in {location} — Google Hotels (est. ${base_rate * 0.95:.0f}/night)",
            location=location,
            link=_build_google_hotels_link(location, checkin, checkout),
            stars=4,
            nightly_rate_usd=round(base_rate * 0.95, 2),
            refundable=False,
        ),
    ]
    if stars_min > 0:
        candidates = [r for r in candidates if r.stars >= stars_min]
    return candidates


# ---------------------------------------------------------------------------
# Public search entrypoint
# ---------------------------------------------------------------------------

def search(
    location: str,
    checkin: date,
    checkout: date,
    currency: str = "USD",
    adults: int = 2,
    policy: Policy | None = None,
    stars_min: int = 0,
) -> list[HotelResult]:
    """Search hotels across all configured providers and return merged results.

    Tries the Booking.com API and SerpApi Google Hotels for real pricing.
    Falls back to estimated-rate deeplinks if neither is configured.
    All returned results are ready for ranking and policy annotation.

    Args:
        location: City or destination name.
        checkin: Check-in date.
        checkout: Check-out date.
        currency: Price currency (for API calls).
        adults: Number of adult guests.
        policy: Optional travel policy for annotations.
        stars_min: Minimum star rating filter.

    Returns:
        List of HotelResult objects, deduplicated and policy-annotated.
    """
    all_results: list[list[HotelResult]] = []

    # 1. Booking.com API (real prices)
    booking_results = _search_booking_com(
        location=location,
        checkin=checkin,
        checkout=checkout,
        currency=currency,
        adults=adults,
        stars_min=stars_min,
    )
    if booking_results:
        all_results.append(booking_results)

    # 2. SerpApi Google Hotels (real prices)
    serp_results = _search_serpapi_hotels(
        location=location,
        checkin=checkin,
        checkout=checkout,
        currency=currency,
        stars_min=stars_min,
    )
    if serp_results:
        all_results.append(serp_results)

    # 3. Merge real results
    merged = _merge_and_dedup(all_results)

    # 4. Supplement with deeplink results when real results are sparse
    deeplink_results = _build_deeplink_results(
        location=location,
        checkin=checkin,
        checkout=checkout,
        adults=adults,
        stars_min=stars_min,
    )

    # Always include deeplinks so the user has something to click even
    # when real APIs return fewer results than the deeplinks would show.
    # Dedup against real results first so we don't surface duplicates.
    merged = _merge_and_dedup([merged, deeplink_results])

    # 5. Apply star floor filter
    if stars_min > 0:
        merged = [r for r in merged if r.stars >= stars_min]

    # 6. Apply policy annotations
    if policy:
        merged = [apply_policy_to_hotel(r, policy) for r in merged]

    logger.info(
        "Hotel search %s: %d total results after merge/dedup",
        location, len(merged),
    )
    return merged
