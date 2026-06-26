"""Core Pydantic v2 models and business logic for Zim travel middleware.

Defines the full data model: traveler preferences, trip definitions,
policy constraints, search results, and itinerary assembly.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Traveler & Preferences
# ---------------------------------------------------------------------------

class TravelPreferences(BaseModel):
    """Traveler-level preferences that inform search and ranking."""

    seat: Optional[str] = None  # window / aisle / any
    airlines: list[str] = Field(default_factory=list, description="Preferred airline IATA codes")
    no_red_eye: bool = False
    hotel_style: Optional[str] = None  # luxury / boutique / business / budget
    hotel_stars_min: int = 3
    car_class: Optional[str] = None  # economy / compact / suv / luxury / van


class TravelerProfile(BaseModel):
    """A named traveler with a travel mode and preferences."""

    name: str
    mode: Literal["business", "personal"] = "personal"
    preferences: TravelPreferences = Field(default_factory=TravelPreferences)


# ---------------------------------------------------------------------------
# Trip Definition
# ---------------------------------------------------------------------------

class Trip(BaseModel):
    """A travel intent: where, when, and why."""

    origin: str = Field(..., min_length=3, max_length=3, description="IATA origin code")
    destination: str = Field(..., min_length=3, max_length=3, description="IATA destination code")
    departure_date: date
    return_date: Optional[date] = None
    purpose: Optional[str] = None
    meeting_location: Optional[str] = None  # for hotel proximity ranking


# ---------------------------------------------------------------------------
# Policy & Constraints
# ---------------------------------------------------------------------------

class Policy(BaseModel):
    """Corporate / personal travel policy that gates approval."""

    max_hotel_night: float = 300.0
    max_flight: float = 2000.0
    approval_threshold: float = 5000.0
    business_long_haul_class: str = "business"
    approved_airlines: list[str] = Field(default_factory=list)
    direct_only: bool = False
    refundable_preferred: bool = False


class Constraints(BaseModel):
    """Per-search constraints layered on top of policy."""

    cabin_class: Optional[str] = None  # economy / business / first
    direct_only: bool = False
    refundable_preferred: bool = False
    preferred_departure_window: Optional[tuple[int, int]] = None  # (start_hour, end_hour)


# ---------------------------------------------------------------------------
# Search Results
# ---------------------------------------------------------------------------

PolicyStatus = Literal["approved", "out_of_policy", "approval_required"]


class FlightResult(BaseModel):
    """A single flight search result with affiliate link and policy annotation."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    airline: str = ""
    flight_number: str = ""
    origin: str = ""
    destination: str = ""
    depart_at: Optional[datetime] = None
    arrive_at: Optional[datetime] = None
    transfers: int = 0
    cabin: str = "economy"
    price_usd: float = 0.0
    refundable: bool = False
    link: str = ""
    policy_status: PolicyStatus = "approved"


class HotelResult(BaseModel):
    """A single hotel search result."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str = ""
    stars: int = 0
    location: str = ""
    distance_km: Optional[float] = None
    nightly_rate_usd: float = 0.0
    refundable: bool = False
    link: str = ""
    policy_status: PolicyStatus = "approved"


class CarResult(BaseModel):
    """A single car rental search result."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    provider: str = ""
    vehicle_class: str = ""
    price_usd_total: float = 0.0
    pickup_location: str = ""
    free_cancellation: bool = False
    link: str = ""
    policy_status: PolicyStatus = "approved"


# ---------------------------------------------------------------------------
# Itinerary (assembled trip package)
# ---------------------------------------------------------------------------

ItineraryStatus = Literal["booking_ready", "approval_required", "missing_traveler_input"]


class Itinerary(BaseModel):
    """An assembled trip itinerary with policy-gated approval state."""

    type: Literal["trip_package"] = "trip_package"
    destination: str = ""
    mode: str = "personal"
    dates: dict = Field(default_factory=dict)
    traveler_profile: dict = Field(default_factory=dict)
    policy: dict = Field(default_factory=dict)
    flights: list[FlightResult] = Field(default_factory=list)
    hotels: list[HotelResult] = Field(default_factory=list)
    cars: list[CarResult] = Field(default_factory=list)
    status: ItineraryStatus = "booking_ready"
    approval_reason: Optional[str] = None
    total_price_usd: float = 0.0


# ---------------------------------------------------------------------------
# TravelObject — the top-level input/output envelope
# ---------------------------------------------------------------------------

class TravelObject(BaseModel):
    """Top-level travel request envelope combining all context."""

    trip: Trip
    traveler: TravelerProfile = Field(default_factory=lambda: TravelerProfile(name="default"))
    policy: Policy = Field(default_factory=Policy)
    constraints: Constraints = Field(default_factory=Constraints)


# ---------------------------------------------------------------------------
# Business Logic
# ---------------------------------------------------------------------------

def apply_policy_to_flight(result: FlightResult, policy: Policy) -> FlightResult:
    """Annotate a FlightResult with its policy compliance status.

    Rules:
    - Price above max_flight → out_of_policy
    - Airline not in approved_airlines (if list is non-empty) → out_of_policy
    - Policy requires direct_only but flight has transfers → out_of_policy
    - Policy prefers refundable but flight is not → approval_required
    - Otherwise → approved
    """
    if policy.max_flight > 0 and result.price_usd > policy.max_flight:
        result.policy_status = "out_of_policy"
        return result

    if policy.approved_airlines and result.airline not in policy.approved_airlines:
        result.policy_status = "out_of_policy"
        return result

    if policy.direct_only and result.transfers > 0:
        result.policy_status = "out_of_policy"
        return result

    if policy.refundable_preferred and not result.refundable:
        result.policy_status = "approval_required"
        return result

    result.policy_status = "approved"
    return result


def apply_policy_to_hotel(result: HotelResult, policy: Policy) -> HotelResult:
    """Annotate a HotelResult with its policy compliance status."""
    if policy.max_hotel_night > 0 and result.nightly_rate_usd > policy.max_hotel_night:
        result.policy_status = "out_of_policy"
        return result

    if policy.refundable_preferred and not result.refundable:
        result.policy_status = "approval_required"
        return result

    result.policy_status = "approved"
    return result


def apply_policy_to_car(result: CarResult, policy: Policy) -> CarResult:
    """Annotate a CarResult with its policy compliance status."""
    if policy.refundable_preferred and not result.free_cancellation:
        result.policy_status = "approval_required"
        return result

    result.policy_status = "approved"
    return result


def assemble_trip(
    travel_object: TravelObject,
    flight_results: list[FlightResult] | None = None,
    hotel_results: list[HotelResult] | None = None,
    car_results: list[CarResult] | None = None,
) -> Itinerary:
    """Assemble search results into a policy-gated Itinerary.

    Computes total price from the best (first) result in each category,
    then determines overall approval status.
    """
    flights = flight_results or []
    hotels = hotel_results or []
    cars = car_results or []

    trip = travel_object.trip
    policy = travel_object.policy
    traveler = travel_object.traveler

    # Apply policy annotations
    flights = [apply_policy_to_flight(f, policy) for f in flights]
    hotels = [apply_policy_to_hotel(h, policy) for h in hotels]
    cars = [apply_policy_to_car(c, policy) for c in cars]

    # Calculate total from the best (first) option in each category
    nights = 1
    if trip.return_date and trip.departure_date:
        nights = max((trip.return_date - trip.departure_date).days, 1)

    flight_price = flights[0].price_usd if flights else 0.0
    hotel_price = (hotels[0].nightly_rate_usd * nights) if hotels else 0.0
    car_price = cars[0].price_usd_total if cars else 0.0
    total = flight_price + hotel_price + car_price

    # Determine approval status
    all_results: list[FlightResult | HotelResult | CarResult] = [
        *flights, *hotels, *cars
    ]
    has_out_of_policy = any(r.policy_status == "out_of_policy" for r in all_results)
    has_approval_required = any(r.policy_status == "approval_required" for r in all_results)

    if has_out_of_policy:
        status: ItineraryStatus = "approval_required"
        approval_reason = "One or more items exceed policy limits"
    elif total > policy.approval_threshold:
        status = "approval_required"
        approval_reason = f"Total ${total:,.2f} exceeds approval threshold ${policy.approval_threshold:,.2f}"
    elif has_approval_required:
        status = "approval_required"
        approval_reason = "One or more items require manual approval"
    else:
        status = "booking_ready"
        approval_reason = None

    dates = {
        "departure": trip.departure_date.isoformat(),
    }
    if trip.return_date:
        dates["return"] = trip.return_date.isoformat()
        dates["nights"] = nights

    return Itinerary(
        destination=trip.destination,
        mode=traveler.mode,
        dates=dates,
        traveler_profile=traveler.model_dump(),
        policy=policy.model_dump(),
        flights=flights,
        hotels=hotels,
        cars=cars,
        status=status,
        approval_reason=approval_reason,
        total_price_usd=round(total, 2),
    )
