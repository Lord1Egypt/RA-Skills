"""Flight search module for Zim.

Searches multiple providers for flights, merges and deduplicates results,
and returns structured FlightResult objects with affiliate deeplinks.

Provider priority:
  1. Travelpayouts (exact-date API → cheap-prices fallback)
  2. Kiwi Tequila API (real prices + direct booking tokens)
  3. SerpApi Google Flights (real Google prices)
  4. Pure deeplink fallback (always available)

Results from all available providers are merged and deduplicated before
being returned to the caller for ranking and policy annotation.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Optional

import httpx

from zim.core import Constraints, FlightResult, Policy, apply_policy_to_flight
from zim.providers import travelpayouts
from zim.providers import kiwi as kiwi_provider
from zim.providers import serpapi as serpapi_provider

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers shared across providers
# ---------------------------------------------------------------------------

def _parse_datetime(value: str | None) -> datetime | None:
    """Parse an ISO-ish datetime string, returning None on failure."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _cabin_from_trip_class(trip_class: int | str) -> str:
    """Map Travelpayouts trip_class int to human-readable cabin."""
    mapping = {0: "economy", 1: "business", 2: "first"}
    if isinstance(trip_class, int):
        return mapping.get(trip_class, "economy")
    return str(trip_class) if trip_class else "economy"


# ---------------------------------------------------------------------------
# Per-provider result converters
# ---------------------------------------------------------------------------

def _api_result_to_flight(raw: dict, marker: str) -> FlightResult:
    """Convert a single Travelpayouts API result dict into a FlightResult."""
    link = raw.get("link", "")
    if link and not link.startswith("http"):
        link = f"https://www.aviasales.com{link}&marker={marker}"
    elif not link:
        link = ""

    return FlightResult(
        airline=raw.get("airline", ""),
        flight_number=raw.get("flight_number", ""),
        origin=raw.get("origin", ""),
        destination=raw.get("destination", ""),
        depart_at=_parse_datetime(raw.get("departure_at")),
        arrive_at=_parse_datetime(raw.get("return_at")),
        transfers=raw.get("transfers", 0),
        cabin=_cabin_from_trip_class(raw.get("trip_class", 0)),
        price_usd=float(raw.get("price", 0)),
        refundable=False,  # Travelpayouts doesn't expose this field
        link=link,
    )


def _kiwi_result_to_flight(raw: dict) -> FlightResult:
    """Convert a Kiwi Tequila API result dict into a FlightResult."""
    fields = kiwi_provider.flight_result_from_raw(raw)
    # Strip internal _-prefixed keys before constructing the model
    return FlightResult(
        airline=fields["airline"],
        flight_number=fields["flight_number"],
        origin=fields["origin"],
        destination=fields["destination"],
        depart_at=fields["depart_at"],
        arrive_at=fields["arrive_at"],
        transfers=fields["transfers"],
        cabin=fields["cabin"],
        price_usd=fields["price_usd"],
        refundable=fields["refundable"],
        link=fields["link"],
    )


def _serpapi_result_to_flight(
    raw: dict,
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None,
) -> FlightResult:
    """Convert a SerpApi Google Flights result dict into a FlightResult."""
    fields = serpapi_provider.flight_result_from_raw(
        raw, origin, destination, departure, return_date
    )
    return FlightResult(
        airline=fields["airline"],
        flight_number=fields["flight_number"],
        origin=fields["origin"],
        destination=fields["destination"],
        depart_at=fields["depart_at"],
        arrive_at=fields["arrive_at"],
        transfers=fields["transfers"],
        cabin=fields["cabin"],
        price_usd=fields["price_usd"],
        refundable=fields["refundable"],
        link=fields["link"],
    )


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _dedup_key(result: FlightResult) -> tuple:
    """Return a deduplication key for a FlightResult.

    Two results are considered duplicates when they share the same airline,
    route, and price bucket (within ±5 USD). We round to the nearest 5 to
    handle minor per-provider price variations.
    """
    price_bucket = round(result.price_usd / 5) * 5
    return (
        result.airline.upper(),
        result.origin.upper(),
        result.destination.upper(),
        result.transfers,
        price_bucket,
    )


def _merge_and_dedup(result_lists: list[list[FlightResult]]) -> list[FlightResult]:
    """Merge multiple result lists, removing duplicates and sorting by price.

    Earlier lists in result_lists take precedence when deduplicating —
    the first occurrence of a key is kept.
    """
    seen: set[tuple] = set()
    merged: list[FlightResult] = []
    for results in result_lists:
        for r in results:
            key = _dedup_key(r)
            if key not in seen:
                seen.add(key)
                merged.append(r)

    # Sort cheapest first (ranking engine will re-sort by composite score)
    merged.sort(key=lambda r: r.price_usd)
    return merged


# ---------------------------------------------------------------------------
# Constraint filtering
# ---------------------------------------------------------------------------

def _apply_constraints(
    results: list[FlightResult],
    constraints: Constraints | None,
) -> list[FlightResult]:
    """Filter results based on per-search constraints."""
    if not constraints:
        return results

    filtered = results

    if constraints.direct_only:
        filtered = [r for r in filtered if r.transfers == 0]

    if constraints.cabin_class:
        cabin = constraints.cabin_class.lower()
        filtered = [r for r in filtered if r.cabin.lower() == cabin]

    if (
        constraints.preferred_departure_window
        and constraints.preferred_departure_window[0] is not None
    ):
        start_h, end_h = constraints.preferred_departure_window
        filtered = [
            r for r in filtered
            if r.depart_at and start_h <= r.depart_at.hour <= end_h
        ]

    return filtered


# ---------------------------------------------------------------------------
# Provider search functions
# ---------------------------------------------------------------------------

def _search_travelpayouts(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None,
    currency: str,
    limit: int,
) -> list[FlightResult]:
    """Attempt Travelpayouts exact-date search with cheap-prices fallback."""
    marker = travelpayouts._get_marker()
    results: list[FlightResult] = []

    try:
        data = travelpayouts.get_flight_prices_for_dates(
            origin=origin,
            destination=destination,
            departure=departure,
            return_date=return_date,
            currency=currency,
            limit=limit,
        )
        raw_results = data.get("data", [])
        results = [_api_result_to_flight(r, marker) for r in raw_results]
        logger.info("Travelpayouts prices_for_dates: %d results", len(results))
    except EnvironmentError:
        logger.info("TRAVELPAYOUTS_TOKEN not set — skipping Travelpayouts")
    except httpx.HTTPError as exc:
        logger.warning("Travelpayouts API error: %s — trying cheap prices", exc)

    if not results:
        try:
            month_str = departure.strftime("%Y-%m")
            data = travelpayouts.get_cheap_prices(
                origin=origin,
                destination=destination,
                departure_month=month_str,
                currency=currency,
            )
            raw_results = data.get("data", [])
            results = [_api_result_to_flight(r, marker) for r in raw_results[:limit]]
            logger.info("Travelpayouts cheap prices fallback: %d results", len(results))
        except (EnvironmentError, httpx.HTTPError) as exc:
            logger.warning("Travelpayouts cheap prices fallback failed: %s", exc)

    return results


def _search_kiwi(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None,
    currency: str,
    limit: int,
    constraints: Constraints | None,
) -> list[FlightResult]:
    """Search Kiwi Tequila API and convert to FlightResults."""
    cabin_code: str | None = None
    if constraints and constraints.cabin_class:
        # Map Zim cabin names back to Tequila codes
        cabin_map = {"economy": "M", "premium_economy": "W", "business": "C", "first": "F"}
        cabin_code = cabin_map.get(constraints.cabin_class.lower())

    raw = kiwi_provider.search_flights(
        origin=origin,
        destination=destination,
        departure=departure,
        return_date=return_date,
        currency=currency,
        cabin_class=cabin_code,
        limit=limit,
    )
    results = []
    for r in raw:
        try:
            results.append(_kiwi_result_to_flight(r))
        except Exception as exc:  # noqa: BLE001
            logger.debug("Kiwi result conversion error: %s", exc)
    logger.info("Kiwi Tequila: %d usable results", len(results))
    return results


def _search_serpapi(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None,
    currency: str,
    constraints: Constraints | None,
) -> list[FlightResult]:
    """Search SerpApi Google Flights and convert to FlightResults."""
    # Map cabin class to Google Flights travel_class integer
    travel_class = 1  # default economy
    if constraints and constraints.cabin_class:
        tc_map = {"economy": 1, "premium_economy": 2, "business": 3, "first": 4}
        travel_class = tc_map.get(constraints.cabin_class.lower(), 1)

    raw = serpapi_provider.search_flights(
        origin=origin,
        destination=destination,
        departure=departure,
        return_date=return_date,
        currency=currency,
        travel_class=travel_class,
    )
    results = []
    for r in raw:
        try:
            results.append(
                _serpapi_result_to_flight(r, origin, destination, departure, return_date)
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("SerpApi result conversion error: %s", exc)
    logger.info("SerpApi Google Flights: %d usable results", len(results))
    return results


# ---------------------------------------------------------------------------
# Public search entrypoint
# ---------------------------------------------------------------------------

def search(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    currency: str = "USD",
    limit: int = 10,
    policy: Policy | None = None,
    constraints: Constraints | None = None,
) -> list[FlightResult]:
    """Search for flights across all configured providers.

    Tries each provider independently and merges the results. Providers
    are skipped gracefully when their API key is absent. A deeplink-only
    fallback guarantees at least one result is always returned.

    Provider order:
      1. Travelpayouts (exact-date → cheap-prices fallback)
      2. Kiwi Tequila (real prices + booking tokens)
      3. SerpApi Google Flights (real Google pricing)
      4. Aviasales deeplink (always-available fallback)

    Args:
        origin: IATA origin code.
        destination: IATA destination code.
        departure: Departure date.
        return_date: Return date for round-trips; None for one-way.
        currency: Price currency.
        limit: Max results per provider.
        policy: Optional travel policy for annotations.
        constraints: Optional per-search constraints (cabin, direct-only, etc.).

    Returns:
        Merged, deduplicated, policy-annotated list of FlightResult objects.
    """
    all_results: list[list[FlightResult]] = []

    # 1. Travelpayouts
    tp_results = _search_travelpayouts(
        origin, destination, departure, return_date, currency, limit
    )
    if tp_results:
        all_results.append(tp_results)

    # 2. Kiwi Tequila
    kiwi_results = _search_kiwi(
        origin, destination, departure, return_date, currency, limit, constraints
    )
    if kiwi_results:
        all_results.append(kiwi_results)

    # 3. SerpApi Google Flights
    serp_results = _search_serpapi(
        origin, destination, departure, return_date, currency, constraints
    )
    if serp_results:
        all_results.append(serp_results)

    # 4. Merge and deduplicate
    merged = _merge_and_dedup(all_results)

    # 5. Pure deeplink fallback — always provide at least one result
    if not merged:
        deeplink = travelpayouts.build_flight_deeplink(
            origin=origin,
            destination=destination,
            departure=departure,
            return_date=return_date,
        )
        merged = [
            FlightResult(
                airline="",
                origin=origin.upper(),
                destination=destination.upper(),
                link=deeplink,
                policy_status="approved",
            )
        ]
        logger.info("Using deeplink-only fallback for %s → %s", origin, destination)

    # 6. Apply constraints filtering
    if constraints:
        merged = _apply_constraints(merged, constraints)
        # Re-check: if constraints filtered everything, keep at least the cheapest
        if not merged and all_results:
            merged = [all_results[0][0]] if all_results[0] else merged

    # 7. Apply policy annotations
    if policy:
        merged = [apply_policy_to_flight(r, policy) for r in merged]

    logger.info(
        "Flight search %s → %s: %d total results after merge/dedup",
        origin, destination, len(merged),
    )
    return merged
