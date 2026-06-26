"""Tests for direct search endpoints and improved hotel/car structured results."""

from __future__ import annotations

from datetime import date, timedelta
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from zim.api import app
from zim.car_search import _estimate_total, search as car_search
from zim.hotel_search import _estimate_nightly_rate, search as hotel_search


@pytest.fixture
def client():
    return TestClient(app)


# ---------------------------------------------------------------------------
# Hotel structured results
# ---------------------------------------------------------------------------


class TestHotelStructuredResults:

    def test_stars_are_positive(self):
        results = hotel_search(
            location="Copenhagen",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
        )
        assert all(r.stars > 0 for r in results), "All hotel results must have stars > 0"

    def test_nightly_rate_is_positive(self):
        results = hotel_search(
            location="London",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
        )
        assert all(r.nightly_rate_usd > 0 for r in results)

    def test_returns_three_providers(self):
        results = hotel_search(
            location="Paris",
            checkin=date(2026, 7, 10),
            checkout=date(2026, 7, 14),
        )
        assert len(results) == 3
        providers = {r.name for r in results}
        # Each result name is distinct
        assert len(providers) == 3

    def test_links_are_valid_urls(self):
        results = hotel_search(
            location="Bangkok",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 3),
        )
        for r in results:
            assert r.link.startswith("https://"), f"Invalid link: {r.link}"

    def test_location_is_set(self):
        results = hotel_search(
            location="New York",
            checkin=date(2026, 8, 1),
            checkout=date(2026, 8, 5),
        )
        for r in results:
            assert r.location == "New York"

    def test_high_tier_city_rate(self):
        rate = _estimate_nightly_rate("London")
        assert rate >= 200.0, f"Expected high-tier rate >= 200, got {rate}"

    def test_high_tier_iata_rate(self):
        rate = _estimate_nightly_rate("LHR")
        assert rate >= 200.0

    def test_low_tier_city_rate(self):
        rate = _estimate_nightly_rate("Bangkok")
        assert rate <= 100.0

    def test_low_tier_iata_rate(self):
        rate = _estimate_nightly_rate("BKK")
        assert rate <= 100.0

    def test_default_tier_rate(self):
        rate = _estimate_nightly_rate("Smallville")
        assert 100.0 <= rate <= 180.0

    def test_providers_have_different_rates(self):
        results = hotel_search(
            location="Berlin",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
        )
        rates = [r.nightly_rate_usd for r in results]
        assert len(set(rates)) > 1, "Providers should have distinct estimated rates"

    def test_stars_min_filter_respected(self):
        results = hotel_search(
            location="Berlin",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
            stars_min=4,
        )
        assert all(r.stars >= 4 for r in results)

    def test_stars_min_4_excludes_3_star_result(self):
        # Booking.com result is 3 stars, so stars_min=4 should remove it
        results = hotel_search(
            location="Berlin",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
            stars_min=4,
        )
        assert all("Booking.com" not in r.name for r in results)

    def test_refundable_mix(self):
        results = hotel_search(
            location="Berlin",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
        )
        refundable_flags = {r.refundable for r in results}
        # At least one refundable and one non-refundable result
        assert True in refundable_flags
        assert False in refundable_flags

    def test_policy_annotation_applied(self):
        from zim.core import Policy
        policy = Policy(max_hotel_night=50.0)  # Very low limit
        results = hotel_search(
            location="New York",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
            policy=policy,
        )
        # NYC is high-tier (>$200/night), so all should be out_of_policy
        for r in results:
            assert r.policy_status == "out_of_policy"

    def test_policy_approved_when_within_limit(self):
        from zim.core import Policy
        policy = Policy(max_hotel_night=500.0)  # Very generous limit
        results = hotel_search(
            location="Bangkok",
            checkin=date(2026, 6, 1),
            checkout=date(2026, 6, 5),
            policy=policy,
        )
        for r in results:
            assert r.policy_status == "approved"


# ---------------------------------------------------------------------------
# Car structured results
# ---------------------------------------------------------------------------


class TestCarStructuredResults:

    def test_price_is_positive(self):
        results = car_search(
            location="Copenhagen",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
        )
        assert all(r.price_usd_total > 0 for r in results)

    def test_returns_four_providers(self):
        results = car_search(
            location="London",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
        )
        assert len(results) == 4
        providers = {r.provider for r in results}
        assert providers == {"Rentalcars", "Kayak", "Discover Cars", "Economy Bookings"}

    def test_vehicle_class_set(self):
        results = car_search(
            location="Berlin",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
            car_class="economy",
        )
        for r in results:
            assert r.vehicle_class == "economy"

    def test_links_are_valid_urls(self):
        results = car_search(
            location="Paris",
            pickup=date(2026, 7, 1),
            dropoff=date(2026, 7, 4),
        )
        for r in results:
            assert r.link.startswith("https://")

    def test_providers_have_different_prices(self):
        results = car_search(
            location="NYC",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
        )
        prices = [r.price_usd_total for r in results]
        assert len(set(prices)) > 1, "Providers should have distinct estimated prices"

    def test_free_cancellation_mix(self):
        results = car_search(
            location="NYC",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
        )
        flags = {r.free_cancellation for r in results}
        assert True in flags
        assert False in flags

    def test_economy_class_rate(self):
        total = _estimate_total("economy", date(2026, 6, 1), date(2026, 6, 4))
        # 3 days × $35/day = $105
        assert total == pytest.approx(105.0)

    def test_suv_class_rate(self):
        total = _estimate_total("suv", date(2026, 6, 1), date(2026, 6, 6))
        # 5 days × $75/day = $375
        assert total == pytest.approx(375.0)

    def test_unknown_class_uses_default(self):
        total = _estimate_total("unicycle", date(2026, 6, 1), date(2026, 6, 3))
        # 2 days × $50/day = $100
        assert total == pytest.approx(100.0)

    def test_minimum_one_day(self):
        total = _estimate_total("economy", date(2026, 6, 1), date(2026, 6, 1))
        # Same-day: minimum 1 day
        assert total == pytest.approx(35.0)

    def test_policy_refundable_annotation(self):
        from zim.core import Policy
        policy = Policy(refundable_preferred=True)
        results = car_search(
            location="London",
            pickup=date(2026, 6, 1),
            dropoff=date(2026, 6, 5),
            policy=policy,
        )
        # Non-free-cancellation providers should be approval_required
        for r in results:
            if not r.free_cancellation:
                assert r.policy_status == "approval_required"
            else:
                assert r.policy_status == "approved"


# ---------------------------------------------------------------------------
# Direct search API endpoints
# ---------------------------------------------------------------------------


class TestFlightSearchEndpoint:

    @patch("zim.flight_search.travelpayouts.get_flight_prices_for_dates")
    def test_basic_flight_search(self, mock_api, client):
        mock_api.return_value = {
            "data": [
                {
                    "origin": "LHR",
                    "destination": "DXB",
                    "departure_at": "2026-06-01T08:00:00",
                    "return_at": "2026-06-05T18:00:00",
                    "price": 450,
                    "airline": "EK",
                    "flight_number": "EK001",
                    "transfers": 0,
                    "trip_class": 0,
                    "link": "/search/LHR0106DXB05061?marker=123",
                }
            ]
        }
        resp = client.get("/v1/search/flights", params={
            "origin": "LHR",
            "destination": "DXB",
            "departure_date": "2026-06-01",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["airline"] == "EK"
        assert data[0]["price_usd"] == 450.0

    @patch("zim.flight_search.travelpayouts.get_flight_prices_for_dates")
    @patch("zim.flight_search.travelpayouts.get_cheap_prices")
    def test_flight_search_fallback_to_deeplink(self, mock_cheap, mock_api, client):
        """When API raises EnvironmentError (no token), fallback deeplink is returned."""
        mock_api.side_effect = EnvironmentError("no token")
        mock_cheap.side_effect = EnvironmentError("no token")
        resp = client.get("/v1/search/flights", params={
            "origin": "LIS",
            "destination": "CPH",
            "departure_date": "2026-06-01",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["link"].startswith("https://")

    def test_flight_search_invalid_departure_date(self, client):
        resp = client.get("/v1/search/flights", params={
            "origin": "LHR",
            "destination": "DXB",
            "departure_date": "not-a-date",
        })
        assert resp.status_code == 422

    def test_flight_search_invalid_return_date(self, client):
        resp = client.get("/v1/search/flights", params={
            "origin": "LHR",
            "destination": "DXB",
            "departure_date": "2026-06-01",
            "return_date": "bad-date",
        })
        assert resp.status_code == 422

    def test_flight_search_missing_required_params(self, client):
        resp = client.get("/v1/search/flights", params={"origin": "LHR"})
        assert resp.status_code == 422

    def test_flight_search_result_fields(self, client):
        """Response objects have the expected FlightResult fields."""
        with patch("zim.flight_search.travelpayouts.get_flight_prices_for_dates",
                   side_effect=EnvironmentError("no token")), \
             patch("zim.flight_search.travelpayouts.get_cheap_prices",
                   side_effect=EnvironmentError("no token")):
            resp = client.get("/v1/search/flights", params={
                "origin": "LIS",
                "destination": "CPH",
                "departure_date": "2026-06-01",
            })
        assert resp.status_code == 200
        r = resp.json()[0]
        for field in ("id", "airline", "origin", "destination", "price_usd", "link", "policy_status"):
            assert field in r, f"Missing field: {field}"


class TestHotelSearchEndpoint:

    def test_basic_hotel_search(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "Copenhagen",
            "checkin": "2026-06-01",
            "checkout": "2026-06-05",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 3

    def test_hotel_results_have_stars(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "London",
            "checkin": "2026-06-01",
            "checkout": "2026-06-05",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["stars"] > 0

    def test_hotel_results_have_price(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "Paris",
            "checkin": "2026-07-01",
            "checkout": "2026-07-05",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["nightly_rate_usd"] > 0

    def test_hotel_stars_min_filter(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "Berlin",
            "checkin": "2026-06-01",
            "checkout": "2026-06-05",
            "stars_min": "4",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["stars"] >= 4

    def test_hotel_invalid_checkin(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "London",
            "checkin": "not-a-date",
            "checkout": "2026-06-05",
        })
        assert resp.status_code == 422

    def test_hotel_checkout_before_checkin(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "London",
            "checkin": "2026-06-05",
            "checkout": "2026-06-01",
        })
        assert resp.status_code == 422

    def test_hotel_missing_required_params(self, client):
        resp = client.get("/v1/search/hotels", params={"location": "London"})
        assert resp.status_code == 422

    def test_hotel_result_fields(self, client):
        resp = client.get("/v1/search/hotels", params={
            "location": "Amsterdam",
            "checkin": "2026-06-01",
            "checkout": "2026-06-05",
        })
        assert resp.status_code == 200
        r = resp.json()[0]
        for field in ("id", "name", "stars", "location", "nightly_rate_usd", "link", "policy_status"):
            assert field in r


class TestCarSearchEndpoint:

    def test_basic_car_search(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "Copenhagen",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 4

    def test_car_results_have_price(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "London",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["price_usd_total"] > 0

    def test_car_results_have_links(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "Paris",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-04",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["link"].startswith("https://")

    def test_car_class_filter(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "Berlin",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
            "car_class": "suv",
        })
        assert resp.status_code == 200
        for r in resp.json():
            assert r["vehicle_class"] == "suv"

    def test_car_invalid_pickup_date(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "London",
            "pickup": "not-a-date",
            "dropoff": "2026-06-05",
        })
        assert resp.status_code == 422

    def test_car_dropoff_before_pickup(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "London",
            "pickup": "2026-06-05",
            "dropoff": "2026-06-01",
        })
        assert resp.status_code == 422

    def test_car_missing_required_params(self, client):
        resp = client.get("/v1/search/cars", params={"location": "London"})
        assert resp.status_code == 422

    def test_car_result_fields(self, client):
        resp = client.get("/v1/search/cars", params={
            "location": "Amsterdam",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
        })
        assert resp.status_code == 200
        r = resp.json()[0]
        for field in ("id", "provider", "vehicle_class", "price_usd_total",
                      "pickup_location", "free_cancellation", "link", "policy_status"):
            assert field in r

    def test_suv_more_expensive_than_economy(self, client):
        """SUV rate should be higher than economy for same dates."""
        economy = client.get("/v1/search/cars", params={
            "location": "Berlin",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
            "car_class": "economy",
        }).json()

        suv = client.get("/v1/search/cars", params={
            "location": "Berlin",
            "pickup": "2026-06-01",
            "dropoff": "2026-06-05",
            "car_class": "suv",
        }).json()

        # Compare the same provider (Rentalcars, index 0)
        assert suv[0]["price_usd_total"] > economy[0]["price_usd_total"]


# ---------------------------------------------------------------------------
# Trip assembly uses non-zero hotel/car prices in total
# ---------------------------------------------------------------------------


class TestTripAssemblyWithPrices:
    """Ensure plan_trip_with_scores produces a non-zero total_price_usd
    when hotel/car prices are now estimated rather than zero."""

    def test_trip_total_includes_hotel_and_car(self):
        from zim.trip import plan_trip_with_scores
        from unittest.mock import patch as _patch

        # Mock flight search to return a known price; let hotel/car use real code
        from zim.core import FlightResult
        mock_flight = FlightResult(
            airline="TP", origin="LIS", destination="CPH",
            price_usd=500.0, link="https://example.com", policy_status="approved",
        )

        with _patch("zim.flight_search.search", return_value=[mock_flight]):
            itin, flights, hotels, cars = plan_trip_with_scores(
                origin="LIS",
                destination="Copenhagen",
                departure=date(2026, 6, 1),
                return_date=date(2026, 6, 5),
            )

        assert itin.total_price_usd > 500.0, (
            f"Total ${itin.total_price_usd} should exceed flight price "
            "once hotel and car prices are non-zero"
        )
        assert len(itin.hotels) > 0
        assert itin.hotels[0].nightly_rate_usd > 0
        assert len(itin.cars) > 0
        assert itin.cars[0].price_usd_total > 0
