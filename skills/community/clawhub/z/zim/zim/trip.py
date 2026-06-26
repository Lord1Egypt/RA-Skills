"""Trip orchestration module for Zim.

Coordinates flight, hotel, and car searches into a single coherent
itinerary with ranking, policy awareness, and approval state.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Optional

from zim.airports import normalize_airport
from zim.approval import ApprovalState, generate_approval_summary, save_approval_record
from zim.core import (
    CarResult,
    Constraints,
    FlightResult,
    HotelResult,
    Itinerary,
    Policy,
    TravelObject,
    TravelPreferences,
    TravelerProfile,
    Trip,
    apply_policy_to_car,
    apply_policy_to_flight,
    apply_policy_to_hotel,
)
from zim.ranking import ScoredResult, rank_cars, rank_flights, rank_hotels

logger = logging.getLogger(__name__)


def _compute_total_price(
    flights: list[FlightResult],
    hotels: list[HotelResult],
    cars: list[CarResult],
    nights: int,
) -> float:
    """Compute total trip price from the top result in each category."""
    flight_price = flights[0].price_usd if flights else 0.0
    hotel_price = (hotels[0].nightly_rate_usd * nights) if hotels else 0.0
    car_price = cars[0].price_usd_total if cars else 0.0
    return round(flight_price + hotel_price + car_price, 2)


def _determine_status(
    flights: list[FlightResult],
    hotels: list[HotelResult],
    cars: list[CarResult],
    total_price: float,
    policy: Policy,
) -> tuple[str, str | None]:
    """Determine the itinerary's approval status and reason.

    Approval is based on the recommended itinerary only: the top-ranked
    result in each category. Lower-ranked fallbacks should not force the
    whole itinerary into approval_required.

    Returns:
        Tuple of (status, approval_reason).
    """
    recommended_results: list[FlightResult | HotelResult | CarResult] = []
    if flights:
        recommended_results.append(flights[0])
    if hotels:
        recommended_results.append(hotels[0])
    if cars:
        recommended_results.append(cars[0])

    has_out_of_policy = any(
        r.policy_status == "out_of_policy" for r in recommended_results
    )
    has_approval_required = any(
        r.policy_status == "approval_required" for r in recommended_results
    )

    if has_out_of_policy:
        return "approval_required", "One or more recommended items exceed policy limits"
    if total_price > policy.approval_threshold:
        return (
            "approval_required",
            f"Total ${total_price:,.2f} exceeds approval threshold ${policy.approval_threshold:,.2f}",
        )
    if has_approval_required:
        return "approval_required", "One or more recommended items require manual approval"
    return "booking_ready", None


def plan_trip(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    mode: str = "personal",
    purpose: str | None = None,
    meeting_location: str | None = None,
    budget: float | None = None,
    traveler_id: str = "default",
) -> Itinerary:
    """Plan a complete trip with ranked flights, hotels, and cars.

    Orchestrates the full trip planning flow:
    1. Normalize origin/destination to IATA codes
    2. Load preferences and policy from memory
    3. Search flights, hotels, and cars
    4. Apply policy annotations to all results
    5. Rank results based on mode, preferences, and policy
    6. Assemble into a single Itinerary with approval state

    Args:
        origin: Origin city name or IATA code.
        destination: Destination city name or IATA code.
        departure: Departure date.
        return_date: Return date (optional for one-way trips).
        mode: Trip mode — "business" or "personal".
        purpose: Trip purpose (e.g., "conference", "vacation").
        meeting_location: Meeting address/area for hotel proximity ranking.
        budget: Optional budget override for approval threshold.
        traveler_id: Traveler profile ID for loading preferences/policy.

    Returns:
        Complete Itinerary with ranked results and approval state.
    """
    # Lazy imports to avoid circular dependencies
    from zim import car_search, flight_search, hotel_search, memory

    # 1. Normalize airports
    origin_iata = normalize_airport(origin)
    dest_iata = normalize_airport(destination)
    logger.info("Planning trip %s → %s (%s mode)", origin_iata, dest_iata, mode)

    # 2. Load preferences and policy
    preferences = memory.load_preferences(traveler_id)
    policy = memory.load_policy(traveler_id)

    # Apply budget override to policy if provided
    if budget is not None:
        policy.approval_threshold = budget

    # 3. Build constraints based on mode
    constraints = Constraints()
    if mode == "business":
        constraints.direct_only = policy.direct_only
        constraints.refundable_preferred = policy.refundable_preferred

    # 4. Search all categories
    logger.info("Searching flights %s → %s", origin_iata, dest_iata)
    flight_results = flight_search.search(
        origin=origin_iata,
        destination=dest_iata,
        departure=departure,
        return_date=return_date,
        policy=policy,
        constraints=constraints,
    )

    checkout = return_date or departure
    logger.info("Searching hotels in %s", destination)
    hotel_results = hotel_search.search(
        location=destination,
        checkin=departure,
        checkout=checkout,
        policy=policy,
    )

    logger.info("Searching cars in %s", destination)
    car_results = car_search.search(
        location=destination,
        pickup=departure,
        dropoff=checkout,
        car_class=preferences.car_class,
        policy=policy,
    )

    # 5. Apply policy annotations
    flight_results = [apply_policy_to_flight(f, policy) for f in flight_results]
    hotel_results = [apply_policy_to_hotel(h, policy) for h in hotel_results]
    car_results = [apply_policy_to_car(c, policy) for c in car_results]

    # 6. Rank results
    ranked_flights = rank_flights(flight_results, preferences, policy, mode)
    ranked_hotels = rank_hotels(hotel_results, preferences, policy, mode, meeting_location)
    ranked_cars = rank_cars(car_results, preferences)

    # Extract sorted results from rankings
    sorted_flights = [sr.result for sr in ranked_flights]  # type: ignore[arg-type]
    sorted_hotels = [sr.result for sr in ranked_hotels]  # type: ignore[arg-type]
    sorted_cars = [sr.result for sr in ranked_cars]  # type: ignore[arg-type]

    # 7. Compute totals and status
    nights = max((return_date - departure).days, 1) if return_date else 1
    total_price = _compute_total_price(sorted_flights, sorted_hotels, sorted_cars, nights)
    status, approval_reason = _determine_status(
        sorted_flights, sorted_hotels, sorted_cars, total_price, policy
    )

    # 8. Build dates dict
    dates: dict[str, str | int] = {
        "departure": departure.isoformat(),
    }
    if return_date:
        dates["return"] = return_date.isoformat()
        dates["nights"] = nights

    # 9. Assemble itinerary
    itinerary = Itinerary(
        destination=dest_iata,
        mode=mode,
        dates=dates,
        traveler_profile={
            "name": traveler_id,
            "mode": mode,
            "preferences": preferences.model_dump(),
        },
        policy=policy.model_dump(),
        flights=sorted_flights,
        hotels=sorted_hotels,
        cars=sorted_cars,
        status=status,
        approval_reason=approval_reason,
        total_price_usd=total_price,
    )

    logger.info(
        "Trip planned: %s → %s, total $%.2f, status: %s",
        origin_iata, dest_iata, total_price, status,
    )

    return itinerary


def plan_trip_with_scores(
    origin: str,
    destination: str,
    departure: date,
    return_date: date | None = None,
    mode: str = "personal",
    purpose: str | None = None,
    meeting_location: str | None = None,
    budget: float | None = None,
    traveler_id: str = "default",
) -> tuple[Itinerary, list[ScoredResult], list[ScoredResult], list[ScoredResult]]:
    """Plan a trip and also return ranking scores for each category.

    Same as plan_trip() but additionally returns the ScoredResult lists
    for use in approval summaries and human-readable output.

    Returns:
        Tuple of (itinerary, flight_scores, hotel_scores, car_scores).
    """
    from zim import car_search, flight_search, hotel_search, memory

    origin_iata = normalize_airport(origin)
    dest_iata = normalize_airport(destination)

    preferences = memory.load_preferences(traveler_id)
    policy = memory.load_policy(traveler_id)

    if budget is not None:
        policy.approval_threshold = budget

    constraints = Constraints()
    if mode == "business":
        constraints.direct_only = policy.direct_only
        constraints.refundable_preferred = policy.refundable_preferred

    flight_results = flight_search.search(
        origin=origin_iata,
        destination=dest_iata,
        departure=departure,
        return_date=return_date,
        policy=policy,
        constraints=constraints,
    )

    checkout = return_date or departure

    hotel_results = hotel_search.search(
        location=destination,
        checkin=departure,
        checkout=checkout,
        policy=policy,
    )

    car_results = car_search.search(
        location=destination,
        pickup=departure,
        dropoff=checkout,
        car_class=preferences.car_class,
        policy=policy,
    )

    flight_results = [apply_policy_to_flight(f, policy) for f in flight_results]
    hotel_results = [apply_policy_to_hotel(h, policy) for h in hotel_results]
    car_results = [apply_policy_to_car(c, policy) for c in car_results]

    ranked_flights = rank_flights(flight_results, preferences, policy, mode)
    ranked_hotels = rank_hotels(hotel_results, preferences, policy, mode, meeting_location)
    ranked_cars = rank_cars(car_results, preferences)

    sorted_flights = [sr.result for sr in ranked_flights]  # type: ignore[arg-type]
    sorted_hotels = [sr.result for sr in ranked_hotels]  # type: ignore[arg-type]
    sorted_cars = [sr.result for sr in ranked_cars]  # type: ignore[arg-type]

    nights = max((return_date - departure).days, 1) if return_date else 1
    total_price = _compute_total_price(sorted_flights, sorted_hotels, sorted_cars, nights)
    status, approval_reason = _determine_status(
        sorted_flights, sorted_hotels, sorted_cars, total_price, policy
    )

    dates: dict[str, str | int] = {"departure": departure.isoformat()}
    if return_date:
        dates["return"] = return_date.isoformat()
        dates["nights"] = nights

    itinerary = Itinerary(
        destination=dest_iata,
        mode=mode,
        dates=dates,
        traveler_profile={
            "name": traveler_id,
            "mode": mode,
            "preferences": preferences.model_dump(),
        },
        policy=policy.model_dump(),
        flights=sorted_flights,
        hotels=sorted_hotels,
        cars=sorted_cars,
        status=status,
        approval_reason=approval_reason,
        total_price_usd=total_price,
    )

    return itinerary, ranked_flights, ranked_hotels, ranked_cars
