from __future__ import annotations

from datetime import date, datetime

from zim.core import CarResult, FlightResult, HotelResult, Policy, TravelPreferences
from zim.trip import plan_trip


def test_plan_trip_business_mode_ranks_and_assembles(monkeypatch) -> None:
    monkeypatch.setattr(
        "zim.memory.load_preferences",
        lambda traveler_id="default": TravelPreferences(
            airlines=["EK"],
            hotel_style="business",
            hotel_stars_min=4,
            car_class="suv",
            no_red_eye=True,
        ),
    )
    monkeypatch.setattr(
        "zim.memory.load_policy",
        lambda traveler_id="default": Policy(
            max_hotel_night=350,
            max_flight=2000,
            approval_threshold=5000,
            refundable_preferred=True,
        ),
    )

    monkeypatch.setattr(
        "zim.flight_search.search",
        lambda **kwargs: [
            FlightResult(
                airline="XX",
                flight_number="XX1",
                origin="JFK",
                destination="DXB",
                depart_at=datetime(2026, 4, 15, 1, 0),
                transfers=1,
                refundable=False,
                price_usd=900,
                link="https://bad-flight",
            ),
            FlightResult(
                airline="EK",
                flight_number="EK202",
                origin="JFK",
                destination="DXB",
                depart_at=datetime(2026, 4, 15, 10, 0),
                transfers=0,
                refundable=True,
                price_usd=1200,
                link="https://good-flight",
            ),
        ],
    )
    monkeypatch.setattr(
        "zim.hotel_search.search",
        lambda **kwargs: [
            HotelResult(
                name="Cheap Stay Inn",
                stars=3,
                location="Dubai",
                distance_km=8.0,
                nightly_rate_usd=100,
                refundable=False,
                link="https://cheap-hotel",
            ),
            HotelResult(
                name="Business Grand Hotel",
                stars=5,
                location="Dubai",
                distance_km=0.8,
                nightly_rate_usd=300,
                refundable=True,
                link="https://good-hotel",
            ),
        ],
    )
    monkeypatch.setattr(
        "zim.car_search.search",
        lambda **kwargs: [
            CarResult(
                provider="UnknownCars",
                vehicle_class="economy",
                price_usd_total=200,
                free_cancellation=False,
                link="https://bad-car",
            ),
            CarResult(
                provider="Rentalcars",
                vehicle_class="suv",
                price_usd_total=250,
                free_cancellation=True,
                link="https://good-car",
            ),
        ],
    )

    itinerary = plan_trip(
        origin="New York",
        destination="Dubai",
        departure=date(2026, 4, 15),
        return_date=date(2026, 4, 20),
        mode="business",
        meeting_location="DIFC",
    )

    assert itinerary.destination == "DXB"
    assert itinerary.flights[0].airline == "EK"
    assert itinerary.hotels[0].name == "Business Grand Hotel"
    assert itinerary.cars[0].provider == "Rentalcars"
    assert itinerary.total_price_usd == 2950.0
    assert itinerary.status == "booking_ready"


def test_plan_trip_sets_approval_required_when_over_budget(monkeypatch) -> None:
    monkeypatch.setattr("zim.memory.load_preferences", lambda traveler_id="default": TravelPreferences())
    monkeypatch.setattr("zim.memory.load_policy", lambda traveler_id="default": Policy(approval_threshold=1000))
    monkeypatch.setattr(
        "zim.flight_search.search",
        lambda **kwargs: [FlightResult(airline="EK", origin="JFK", destination="LHR", price_usd=1500)],
    )
    monkeypatch.setattr("zim.hotel_search.search", lambda **kwargs: [])
    monkeypatch.setattr("zim.car_search.search", lambda **kwargs: [])

    itinerary = plan_trip(
        origin="JFK",
        destination="London",
        departure=date(2026, 5, 1),
        mode="personal",
    )

    assert itinerary.status == "approval_required"
    assert itinerary.approval_reason is not None
    assert "threshold" in itinerary.approval_reason
