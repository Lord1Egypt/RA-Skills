from __future__ import annotations

from datetime import datetime

from zim.core import CarResult, FlightResult, HotelResult, Policy, TravelPreferences
from zim.ranking import rank_cars, rank_flights, rank_hotels


def test_rank_flights_business_prefers_direct_refundable_and_preferred_airline() -> None:
    prefs = TravelPreferences(airlines=["EK"], no_red_eye=True)
    policy = Policy()

    flights = [
        FlightResult(
            airline="EK",
            flight_number="EK202",
            origin="JFK",
            destination="DXB",
            depart_at=datetime(2026, 4, 15, 10, 0),
            transfers=0,
            refundable=True,
            price_usd=1200,
            policy_status="approved",
        ),
        FlightResult(
            airline="XX",
            flight_number="XX100",
            origin="JFK",
            destination="DXB",
            depart_at=datetime(2026, 4, 15, 1, 0),
            transfers=1,
            refundable=False,
            price_usd=900,
            policy_status="approved",
        ),
    ]

    ranked = rank_flights(flights, prefs, policy, mode="business")
    assert ranked[0].result.airline == "EK"
    assert ranked[0].score > ranked[1].score
    assert "preferred airline" in ranked[0].rank_reason
    assert "non-stop" in ranked[0].rank_reason


def test_rank_hotels_business_prefers_close_refundable_quality() -> None:
    prefs = TravelPreferences(hotel_style="business", hotel_stars_min=4)
    policy = Policy()

    hotels = [
        HotelResult(
            name="Business Grand Hotel",
            stars=5,
            location="Dubai",
            distance_km=0.8,
            nightly_rate_usd=280,
            refundable=True,
            policy_status="approved",
        ),
        HotelResult(
            name="Cheap Stay Inn",
            stars=3,
            location="Dubai",
            distance_km=8.0,
            nightly_rate_usd=120,
            refundable=False,
            policy_status="approved",
        ),
    ]

    ranked = rank_hotels(hotels, prefs, policy, mode="business", meeting_location="DIFC")
    assert ranked[0].result.name == "Business Grand Hotel"
    assert ranked[0].score > ranked[1].score
    assert "very close to meeting" in ranked[0].rank_reason


def test_rank_cars_prefers_price_cancellation_and_class_match() -> None:
    prefs = TravelPreferences(car_class="suv")

    cars = [
        CarResult(
            provider="Rentalcars",
            vehicle_class="suv",
            price_usd_total=250,
            free_cancellation=True,
        ),
        CarResult(
            provider="UnknownCars",
            vehicle_class="economy",
            price_usd_total=200,
            free_cancellation=False,
        ),
    ]

    ranked = rank_cars(cars, prefs)
    assert ranked[0].result.provider == "Rentalcars"
    assert ranked[0].score > ranked[1].score
    assert "matches preferred class" in ranked[0].rank_reason
