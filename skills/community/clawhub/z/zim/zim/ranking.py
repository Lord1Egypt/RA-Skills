"""Ranking logic for Zim trip orchestration.

Provides scoring and sorting of flight, hotel, and car search results
based on traveler preferences, policy constraints, and trip mode
(business vs personal).

Each result gets a numeric score (higher = better) and a human-readable
rank_reason explaining the scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from zim.core import (
    CarResult,
    FlightResult,
    HotelResult,
    Policy,
    TravelPreferences,
)


@dataclass
class ScoredResult:
    """A search result paired with a numeric score and explanation."""

    result: FlightResult | HotelResult | CarResult
    score: float
    rank_reason: str


# ---------------------------------------------------------------------------
# Flight Ranking
# ---------------------------------------------------------------------------

def rank_flights(
    results: list[FlightResult],
    preferences: TravelPreferences | None = None,
    policy: Policy | None = None,
    mode: str = "personal",
) -> list[ScoredResult]:
    """Rank flight results by composite score.

    Scoring factors:
    - Price (lower is better, normalized to 0-40 points)
    - Directness (non-stop = +20, each transfer = -5)
    - Policy compliance (approved = +15, approval_required = +5, out_of_policy = 0)
    - Airline preference match (+10 if airline in preferences)
    - Refundability (+5 if refundable, +10 in business mode)
    - Timing: business mode prefers daytime departures (+5)

    Args:
        results: Flight search results to rank.
        preferences: Traveler preferences (optional).
        policy: Travel policy (optional).
        mode: Trip mode — "business" or "personal".

    Returns:
        Sorted list of ScoredResult (highest score first).
    """
    if not results:
        return []

    prefs = preferences or TravelPreferences()

    # Normalize price scoring: cheapest gets max points
    prices = [r.price_usd for r in results if r.price_usd > 0]
    min_price = min(prices) if prices else 1.0
    max_price = max(prices) if prices else 1.0
    price_range = max_price - min_price if max_price > min_price else 1.0

    scored: list[ScoredResult] = []

    for flight in results:
        score = 0.0
        reasons: list[str] = []

        # Price score (0-40 points, lower price = higher score)
        if flight.price_usd > 0:
            price_score = 40.0 * (1.0 - (flight.price_usd - min_price) / price_range)
            score += price_score
            if price_score >= 35:
                reasons.append("excellent price")
            elif price_score >= 20:
                reasons.append("competitive price")
            else:
                reasons.append("premium price")
        else:
            reasons.append("price unavailable")

        # Directness (0-20 points)
        if flight.transfers == 0:
            score += 20.0
            reasons.append("non-stop")
        else:
            penalty = max(0.0, 20.0 - flight.transfers * 5.0)
            score += penalty
            reasons.append(f"{flight.transfers} stop{'s' if flight.transfers > 1 else ''}")

        # In business mode, direct flights get extra weight
        if mode == "business" and flight.transfers == 0:
            score += 10.0
            reasons.append("direct (business priority)")

        # Policy compliance (0-15 points)
        if flight.policy_status == "approved":
            score += 15.0
            reasons.append("within policy")
        elif flight.policy_status == "approval_required":
            score += 5.0
            reasons.append("needs approval")
        else:
            reasons.append("out of policy")

        # Airline preference match (+10)
        if prefs.airlines and flight.airline.upper() in [a.upper() for a in prefs.airlines]:
            score += 10.0
            reasons.append(f"preferred airline ({flight.airline})")

        # Refundability
        if flight.refundable:
            refund_bonus = 10.0 if mode == "business" else 5.0
            score += refund_bonus
            reasons.append("refundable")

        # Timing bonus for business mode (daytime departures 7:00-18:59)
        if mode == "business" and flight.depart_at:
            hour = flight.depart_at.hour
            if 7 <= hour < 19:
                score += 5.0
                reasons.append("daytime departure")
            elif prefs.no_red_eye and (hour >= 23 or hour < 5):
                score -= 25.0
                reasons.append("red-eye (penalized)")
            elif prefs.no_red_eye:
                score -= 10.0
                reasons.append("late/early departure (penalized)")

        scored.append(ScoredResult(
            result=flight,
            score=round(score, 1),
            rank_reason="; ".join(reasons),
        ))

    # Sort by score descending
    scored.sort(key=lambda s: s.score, reverse=True)
    return scored


# ---------------------------------------------------------------------------
# Hotel Ranking
# ---------------------------------------------------------------------------

def rank_hotels(
    results: list[HotelResult],
    preferences: TravelPreferences | None = None,
    policy: Policy | None = None,
    mode: str = "personal",
    meeting_location: str | None = None,
) -> list[ScoredResult]:
    """Rank hotel results by composite score.

    Scoring factors:
    - Price (lower nightly rate is better, normalized to 0-30 points)
    - Star rating (0-20 points based on stars, business mode weights higher)
    - Policy compliance (approved = +15, approval_required = +5, out_of_policy = 0)
    - Proximity to meeting location (closer = better, if distance available)
    - Hotel style match (+10 if style matches preference)
    - Refundability (+5, +10 in business mode)

    Args:
        results: Hotel search results to rank.
        preferences: Traveler preferences (optional).
        policy: Travel policy (optional).
        mode: Trip mode — "business" or "personal".
        meeting_location: Address/area of meeting (for proximity scoring).

    Returns:
        Sorted list of ScoredResult (highest score first).
    """
    if not results:
        return []

    prefs = preferences or TravelPreferences()

    # Normalize price scoring
    prices = [r.nightly_rate_usd for r in results if r.nightly_rate_usd > 0]
    min_price = min(prices) if prices else 1.0
    max_price = max(prices) if prices else 1.0
    price_range = max_price - min_price if max_price > min_price else 1.0

    scored: list[ScoredResult] = []

    for hotel in results:
        score = 0.0
        reasons: list[str] = []

        # Price score (0-30 points)
        if hotel.nightly_rate_usd > 0:
            if mode == "personal":
                # Personal mode: price matters more
                price_score = 30.0 * (1.0 - (hotel.nightly_rate_usd - min_price) / price_range)
            else:
                # Business mode: price matters less
                price_score = 20.0 * (1.0 - (hotel.nightly_rate_usd - min_price) / price_range)
            score += price_score
            if price_score >= 25:
                reasons.append("great value")
            elif price_score >= 15:
                reasons.append("fair price")
            else:
                reasons.append("premium rate")
        else:
            reasons.append("price unavailable")

        # Star rating (0-20 points)
        if hotel.stars > 0:
            star_score = min(hotel.stars * 4.0, 20.0)
            if mode == "business":
                star_score = min(hotel.stars * 5.0, 25.0)  # Business values quality more
            score += star_score
            reasons.append(f"{hotel.stars}-star")
        else:
            reasons.append("stars unknown")

        # Policy compliance (0-15 points)
        if hotel.policy_status == "approved":
            score += 15.0
            reasons.append("within policy")
        elif hotel.policy_status == "approval_required":
            score += 5.0
            reasons.append("needs approval")
        else:
            reasons.append("out of policy")

        # Proximity to meeting location (0-15 points)
        if hotel.distance_km is not None:
            if hotel.distance_km <= 1.0:
                score += 15.0
                reasons.append("very close to meeting")
            elif hotel.distance_km <= 3.0:
                score += 10.0
                reasons.append("near meeting area")
            elif hotel.distance_km <= 5.0:
                score += 5.0
                reasons.append("moderate distance")
            else:
                reasons.append(f"{hotel.distance_km:.1f}km from meeting")
        elif meeting_location:
            # Can't score proximity without distance data
            reasons.append("distance unknown")

        # Hotel style match (+10)
        if prefs.hotel_style and hotel.name:
            style = prefs.hotel_style.lower()
            name_lower = hotel.name.lower()
            # Simple heuristic: check if the style keyword appears in name
            if style in name_lower:
                score += 10.0
                reasons.append(f"matches '{style}' style")

        # Stars meet minimum preference — hard floor in business mode
        if hotel.stars > 0 and hotel.stars >= prefs.hotel_stars_min:
            score += 5.0
            reasons.append("meets star minimum")
        elif hotel.stars > 0 and hotel.stars < prefs.hotel_stars_min:
            penalty = -30.0 if mode == "business" else -10.0
            score += penalty
            reasons.append(f"below {prefs.hotel_stars_min}-star minimum")

        # Refundability
        if hotel.refundable:
            refund_bonus = 10.0 if mode == "business" else 5.0
            score += refund_bonus
            reasons.append("refundable")

        scored.append(ScoredResult(
            result=hotel,
            score=round(score, 1),
            rank_reason="; ".join(reasons),
        ))

    scored.sort(key=lambda s: s.score, reverse=True)
    return scored


# ---------------------------------------------------------------------------
# Car Ranking
# ---------------------------------------------------------------------------

def rank_cars(
    results: list[CarResult],
    preferences: TravelPreferences | None = None,
) -> list[ScoredResult]:
    """Rank car rental results by composite score.

    Scoring factors:
    - Price (lower is better, normalized to 0-40 points)
    - Free cancellation (+15)
    - Vehicle class preference match (+10)
    - Provider reliability (known providers get small bonus)

    Args:
        results: Car search results to rank.
        preferences: Traveler preferences (optional).

    Returns:
        Sorted list of ScoredResult (highest score first).
    """
    if not results:
        return []

    prefs = preferences or TravelPreferences()

    # Normalize price scoring
    prices = [r.price_usd_total for r in results if r.price_usd_total > 0]
    min_price = min(prices) if prices else 1.0
    max_price = max(prices) if prices else 1.0
    price_range = max_price - min_price if max_price > min_price else 1.0

    scored: list[ScoredResult] = []

    for car in results:
        score = 0.0
        reasons: list[str] = []

        # Price score (0-40 points)
        if car.price_usd_total > 0:
            price_score = 40.0 * (1.0 - (car.price_usd_total - min_price) / price_range)
            score += price_score
            if price_score >= 35:
                reasons.append("best price")
            elif price_score >= 20:
                reasons.append("competitive price")
            else:
                reasons.append("premium price")
        else:
            reasons.append("price unavailable")

        # Free cancellation (+20)
        if car.free_cancellation:
            score += 20.0
            reasons.append("free cancellation")
        else:
            reasons.append("no free cancellation")

        # Vehicle class match (+20)
        if prefs.car_class and car.vehicle_class.lower() == prefs.car_class.lower():
            score += 20.0
            reasons.append(f"matches preferred class ({prefs.car_class})")
        elif car.vehicle_class:
            reasons.append(f"{car.vehicle_class} class")

        # Provider bonus (known reliable providers)
        reliable_providers = {"hertz", "avis", "enterprise", "sixt", "europcar", "rentalcars"}
        if car.provider.lower() in reliable_providers:
            score += 5.0
            reasons.append("established provider")

        scored.append(ScoredResult(
            result=car,
            score=round(score, 1),
            rank_reason="; ".join(reasons),
        ))

    scored.sort(key=lambda s: s.score, reverse=True)
    return scored
