"""Tests for zim.core — Pydantic models, policy application, and trip assembly."""

from datetime import date, datetime

import pytest

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
    assemble_trip,
)


# ---------------------------------------------------------------------------
# Model construction tests
# ---------------------------------------------------------------------------


class TestTravelPreferences:
    def test_defaults(self) -> None:
        prefs = TravelPreferences()
        assert prefs.seat is None
        assert prefs.airlines == []
        assert prefs.no_red_eye is False
        assert prefs.hotel_stars_min == 3
        assert prefs.car_class is None

    def test_custom_values(self) -> None:
        prefs = TravelPreferences(
            seat="window",
            airlines=["EK", "SQ"],
            no_red_eye=True,
            hotel_style="luxury",
            hotel_stars_min=5,
            car_class="suv",
        )
        assert prefs.seat == "window"
        assert prefs.airlines == ["EK", "SQ"]
        assert prefs.no_red_eye is True
        assert prefs.hotel_style == "luxury"
        assert prefs.hotel_stars_min == 5
        assert prefs.car_class == "suv"


class TestTravelerProfile:
    def test_defaults(self) -> None:
        profile = TravelerProfile(name="Robin")
        assert profile.name == "Robin"
        assert profile.mode == "personal"
        assert isinstance(profile.preferences, TravelPreferences)

    def test_business_mode(self) -> None:
        profile = TravelerProfile(name="Robin", mode="business")
        assert profile.mode == "business"


class TestTrip:
    def test_one_way(self) -> None:
        trip = Trip(
            origin="LHR",
            destination="DXB",
            departure_date=date(2026, 4, 15),
        )
        assert trip.origin == "LHR"
        assert trip.destination == "DXB"
        assert trip.return_date is None

    def test_round_trip(self) -> None:
        trip = Trip(
            origin="JFK",
            destination="LHR",
            departure_date=date(2026, 5, 1),
            return_date=date(2026, 5, 8),
            purpose="conference",
        )
        assert trip.return_date == date(2026, 5, 8)
        assert trip.purpose == "conference"

    def test_iata_code_validation(self) -> None:
        with pytest.raises(Exception):
            Trip(
                origin="A",  # too short
                destination="DXB",
                departure_date=date(2026, 4, 15),
            )


class TestPolicy:
    def test_defaults(self) -> None:
        pol = Policy()
        assert pol.max_hotel_night == 300.0
        assert pol.max_flight == 2000.0
        assert pol.approval_threshold == 5000.0
        assert pol.direct_only is False

    def test_custom_policy(self) -> None:
        pol = Policy(
            max_hotel_night=500,
            max_flight=5000,
            approved_airlines=["EK", "QR"],
            direct_only=True,
        )
        assert pol.approved_airlines == ["EK", "QR"]
        assert pol.direct_only is True


class TestConstraints:
    def test_defaults(self) -> None:
        c = Constraints()
        assert c.cabin_class is None
        assert c.direct_only is False

    def test_departure_window(self) -> None:
        c = Constraints(preferred_departure_window=(8, 14))
        assert c.preferred_departure_window == (8, 14)


class TestFlightResult:
    def test_auto_id(self) -> None:
        f = FlightResult()
        assert len(f.id) == 12

    def test_default_status(self) -> None:
        f = FlightResult()
        assert f.policy_status == "approved"


class TestHotelResult:
    def test_construction(self) -> None:
        h = HotelResult(
            name="Four Seasons Dubai",
            stars=5,
            location="Dubai",
            nightly_rate_usd=450.0,
            link="https://example.com",
        )
        assert h.name == "Four Seasons Dubai"
        assert h.stars == 5


class TestCarResult:
    def test_construction(self) -> None:
        c = CarResult(
            provider="Hertz",
            vehicle_class="suv",
            price_usd_total=350.0,
            pickup_location="Dubai Airport",
            free_cancellation=True,
            link="https://example.com",
        )
        assert c.provider == "Hertz"
        assert c.free_cancellation is True


# ---------------------------------------------------------------------------
# Policy application tests
# ---------------------------------------------------------------------------


class TestApplyPolicyToFlight:
    def _make_flight(self, **kwargs) -> FlightResult:
        defaults = dict(
            airline="EK",
            origin="LHR",
            destination="DXB",
            price_usd=800.0,
            transfers=0,
            refundable=False,
        )
        defaults.update(kwargs)
        return FlightResult(**defaults)

    def test_approved_within_policy(self) -> None:
        f = self._make_flight(price_usd=500)
        pol = Policy(max_flight=2000)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approved"

    def test_out_of_policy_price(self) -> None:
        f = self._make_flight(price_usd=3000)
        pol = Policy(max_flight=2000)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "out_of_policy"

    def test_out_of_policy_airline(self) -> None:
        f = self._make_flight(airline="RY")
        pol = Policy(approved_airlines=["EK", "BA"])
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "out_of_policy"

    def test_approved_airline_in_list(self) -> None:
        f = self._make_flight(airline="EK")
        pol = Policy(approved_airlines=["EK", "BA"])
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approved"

    def test_empty_approved_airlines_allows_all(self) -> None:
        f = self._make_flight(airline="XX")
        pol = Policy(approved_airlines=[])
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approved"

    def test_direct_only_with_transfers(self) -> None:
        f = self._make_flight(transfers=1)
        pol = Policy(direct_only=True)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "out_of_policy"

    def test_direct_only_no_transfers(self) -> None:
        f = self._make_flight(transfers=0)
        pol = Policy(direct_only=True)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approved"

    def test_refundable_preferred_not_refundable(self) -> None:
        f = self._make_flight(refundable=False)
        pol = Policy(refundable_preferred=True)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approval_required"

    def test_refundable_preferred_is_refundable(self) -> None:
        f = self._make_flight(refundable=True)
        pol = Policy(refundable_preferred=True)
        result = apply_policy_to_flight(f, pol)
        assert result.policy_status == "approved"


class TestApplyPolicyToHotel:
    def test_approved(self) -> None:
        h = HotelResult(nightly_rate_usd=200, refundable=True)
        pol = Policy(max_hotel_night=300)
        result = apply_policy_to_hotel(h, pol)
        assert result.policy_status == "approved"

    def test_out_of_policy_rate(self) -> None:
        h = HotelResult(nightly_rate_usd=500)
        pol = Policy(max_hotel_night=300)
        result = apply_policy_to_hotel(h, pol)
        assert result.policy_status == "out_of_policy"

    def test_refundable_approval_needed(self) -> None:
        h = HotelResult(nightly_rate_usd=200, refundable=False)
        pol = Policy(refundable_preferred=True)
        result = apply_policy_to_hotel(h, pol)
        assert result.policy_status == "approval_required"


class TestApplyPolicyToCar:
    def test_approved(self) -> None:
        c = CarResult(free_cancellation=True)
        pol = Policy()
        result = apply_policy_to_car(c, pol)
        assert result.policy_status == "approved"

    def test_refundable_preferred_no_cancellation(self) -> None:
        c = CarResult(free_cancellation=False)
        pol = Policy(refundable_preferred=True)
        result = apply_policy_to_car(c, pol)
        assert result.policy_status == "approval_required"


# ---------------------------------------------------------------------------
# Trip assembly tests
# ---------------------------------------------------------------------------


class TestAssembleTrip:
    def _make_travel_object(
        self, departure: date | None = None, return_date: date | None = None, **policy_kwargs
    ) -> TravelObject:
        dep = departure or date(2026, 4, 15)
        ret = return_date or date(2026, 4, 20)
        return TravelObject(
            trip=Trip(
                origin="LHR",
                destination="DXB",
                departure_date=dep,
                return_date=ret,
            ),
            traveler=TravelerProfile(name="Robin", mode="business"),
            policy=Policy(**policy_kwargs),
        )

    def test_basic_assembly(self) -> None:
        to = self._make_travel_object()
        flights = [FlightResult(price_usd=800, airline="EK")]
        hotels = [HotelResult(nightly_rate_usd=200)]
        cars = [CarResult(price_usd_total=300)]

        itinerary = assemble_trip(to, flights, hotels, cars)

        assert itinerary.type == "trip_package"
        assert itinerary.destination == "DXB"
        assert itinerary.mode == "business"
        # 5 nights * $200 + $800 + $300 = $2100
        assert itinerary.total_price_usd == 2100.0
        assert itinerary.status == "booking_ready"

    def test_approval_required_over_threshold(self) -> None:
        to = self._make_travel_object(approval_threshold=1000)
        flights = [FlightResult(price_usd=1500)]

        itinerary = assemble_trip(to, flights)
        assert itinerary.status == "approval_required"
        assert "exceeds approval threshold" in (itinerary.approval_reason or "")

    def test_approval_required_out_of_policy_item(self) -> None:
        to = self._make_travel_object(max_flight=500)
        flights = [FlightResult(price_usd=800)]

        itinerary = assemble_trip(to, flights)
        assert itinerary.status == "approval_required"
        assert "exceed policy" in (itinerary.approval_reason or "")

    def test_empty_results(self) -> None:
        to = self._make_travel_object()
        itinerary = assemble_trip(to)
        assert itinerary.total_price_usd == 0.0
        assert itinerary.status == "booking_ready"

    def test_dates_in_output(self) -> None:
        to = self._make_travel_object()
        itinerary = assemble_trip(to, [FlightResult(price_usd=100)])
        assert itinerary.dates["departure"] == "2026-04-15"
        assert itinerary.dates["return"] == "2026-04-20"
        assert itinerary.dates["nights"] == 5

    def test_one_way_trip(self) -> None:
        to = TravelObject(
            trip=Trip(
                origin="JFK",
                destination="LAX",
                departure_date=date(2026, 6, 1),
            ),
        )
        flights = [FlightResult(price_usd=300)]
        itinerary = assemble_trip(to, flights)
        assert itinerary.total_price_usd == 300.0
        assert "return" not in itinerary.dates

    def test_policy_annotations_propagated(self) -> None:
        to = self._make_travel_object(max_flight=500, refundable_preferred=True)
        flights = [
            FlightResult(price_usd=400, refundable=False),
            FlightResult(price_usd=600, refundable=True),
        ]
        itinerary = assemble_trip(to, flights)
        # First flight: under budget but not refundable → approval_required
        assert itinerary.flights[0].policy_status == "approval_required"
        # Second flight: over budget → out_of_policy
        assert itinerary.flights[1].policy_status == "out_of_policy"


class TestTravelObject:
    def test_minimal_construction(self) -> None:
        to = TravelObject(
            trip=Trip(
                origin="LHR",
                destination="DXB",
                departure_date=date(2026, 4, 15),
            ),
        )
        assert to.traveler.name == "default"
        assert to.policy.max_flight == 2000.0
        assert to.constraints.direct_only is False

    def test_full_construction(self) -> None:
        to = TravelObject(
            trip=Trip(
                origin="JFK",
                destination="LHR",
                departure_date=date(2026, 5, 1),
                return_date=date(2026, 5, 8),
            ),
            traveler=TravelerProfile(
                name="Robin",
                mode="business",
                preferences=TravelPreferences(seat="window", airlines=["BA"]),
            ),
            policy=Policy(max_flight=5000, direct_only=True),
            constraints=Constraints(cabin_class="business"),
        )
        assert to.traveler.preferences.seat == "window"
        assert to.policy.direct_only is True
        assert to.constraints.cabin_class == "business"
