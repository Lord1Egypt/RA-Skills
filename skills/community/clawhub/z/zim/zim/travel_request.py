"""Pydantic model for accumulating travel request state.

Tracks the user's travel intent, collected slots, search results,
and booking state through the orchestration flow.
"""

from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class RequestType(str, Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    CAR = "car"
    TRIP = "trip"  # flight + hotel combo


class FlowState(str, Enum):
    IDLE = "idle"
    COLLECTING = "collecting"                    # gathering required fields
    SEARCHING = "searching"                      # search in progress
    RESULTS_SHOWN = "results_shown"              # results displayed, awaiting selection
    OPTION_SELECTED = "option_selected"          # user picked one, showing summary
    AWAITING_CONFIRMATION = "awaiting_confirmation"  # user needs to say YES
    PAYMENT_SENT = "payment_sent"                # Stripe link sent
    COMPLETED = "completed"                      # booking done


class TravelRequest(BaseModel):
    request_type: RequestType = RequestType.FLIGHT
    state: FlowState = FlowState.IDLE

    # Flight slots
    origin: Optional[str] = None           # IATA code
    destination: Optional[str] = None      # IATA code
    departure_date: Optional[date] = None
    return_date: Optional[date] = None
    travelers: int = 1
    cabin_class: str = "economy"

    # Hotel slots
    hotel_location: Optional[str] = None
    checkin: Optional[date] = None
    checkout: Optional[date] = None
    guests: int = 1
    hotel_budget: Optional[float] = None

    # Car slots
    car_location: Optional[str] = None
    pickup_date: Optional[date] = None
    dropoff_date: Optional[date] = None

    # Preferences (persisted across sessions)
    preferences: dict = Field(default_factory=dict)  # seat_type, avoid_airlines, etc.

    # Results & selection
    search_results: list[dict] = Field(default_factory=list)
    selected_index: Optional[int] = None   # 0-based
    selected_item: Optional[dict] = None

    # Booking
    booking_id: Optional[str] = None
    base_price: Optional[float] = None
    fee: Optional[float] = None
    total_price: Optional[float] = None
    payment_url: Optional[str] = None

    def missing_slots(self) -> list[str]:
        """Return list of required but unfilled slots for current request type."""
        missing = []
        if self.request_type in (RequestType.FLIGHT, RequestType.TRIP):
            if not self.origin:
                missing.append("origin")
            if not self.destination:
                missing.append("destination")
            if not self.departure_date:
                missing.append("departure_date")
        if self.request_type in (RequestType.HOTEL, RequestType.TRIP):
            if not self.hotel_location and not self.destination:
                missing.append("hotel_location")
            if not self.checkin and not self.departure_date:
                missing.append("checkin")
            if not self.checkout:
                missing.append("checkout")
        if self.request_type == RequestType.CAR:
            if not self.car_location:
                missing.append("car_location")
            if not self.pickup_date:
                missing.append("pickup_date")
            if not self.dropoff_date:
                missing.append("dropoff_date")
        return missing

    def next_question(self) -> str:
        """Return the ONE most important missing slot to ask about."""
        missing = self.missing_slots()
        if not missing:
            return ""
        slot = missing[0]
        questions = {
            "origin": "Where are you flying from? ✈️",
            "destination": "Where would you like to go? 🌍",
            "departure_date": "When are you looking to fly? 📅",
            "hotel_location": "Which city are you staying in? 🏨",
            "checkin": "What's your check-in date? 📅",
            "checkout": "And your check-out date? 📅",
            "car_location": "Where do you need the car? 🚗",
            "pickup_date": "When do you need to pick it up? 📅",
            "dropoff_date": "And when will you return it? 📅",
        }
        return questions.get(slot, f"Could you share your {slot}?")
