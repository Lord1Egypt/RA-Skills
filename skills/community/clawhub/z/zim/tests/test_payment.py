"""Tests for zim.payment — Stripe checkout session creation and line item building."""

from __future__ import annotations

import pytest

from zim.payment import (
    CheckoutLineItem,
    CheckoutResult,
    StripeConfig,
    build_line_items_from_itinerary,
)


class TestCheckoutLineItem:
    def test_construction(self) -> None:
        item = CheckoutLineItem(
            description="Flight: JFK → DXB (EK)",
            amount_cents=120000,
            category="flight",
        )
        assert item.amount_cents == 120000
        assert item.quantity == 1
        assert item.category == "flight"

    def test_amount_must_be_positive(self) -> None:
        with pytest.raises(Exception):
            CheckoutLineItem(description="Bad", amount_cents=0)


class TestCheckoutResult:
    def test_construction(self) -> None:
        result = CheckoutResult(
            session_id="cs_test_abc123",
            checkout_url="https://checkout.stripe.com/pay/cs_test_abc123",
            payment_status="unpaid",
            amount_total_cents=350000,
        )
        assert result.session_id == "cs_test_abc123"
        assert result.currency == "usd"


class TestStripeConfig:
    def test_from_env_empty(self, monkeypatch) -> None:
        monkeypatch.delenv("STRIPE_SECRET_KEY", raising=False)
        monkeypatch.delenv("STRIPE_WEBHOOK_SECRET", raising=False)
        config = StripeConfig.from_env()
        assert config.is_configured is False

    def test_from_env_with_key(self, monkeypatch) -> None:
        monkeypatch.setenv("STRIPE_SECRET_KEY", "sk_test_abc")
        config = StripeConfig.from_env()
        assert config.is_configured is True
        assert config.secret_key == "sk_test_abc"


class TestBuildLineItems:
    def test_builds_from_all_categories(self) -> None:
        flights = [{"origin": "JFK", "destination": "DXB", "airline": "EK", "price_usd": 1200}]
        hotels = [{"name": "Four Seasons", "nightly_rate_usd": 400}]
        cars = [{"provider": "Hertz", "vehicle_class": "SUV", "price_usd_total": 300}]

        items = build_line_items_from_itinerary(flights, hotels, cars, nights=5)

        assert len(items) == 3
        assert items[0].category == "flight"
        assert items[0].amount_cents == 120000
        assert items[1].category == "hotel"
        assert items[1].amount_cents == 40000
        assert items[1].quantity == 5
        assert items[2].category == "car"
        assert items[2].amount_cents == 30000

    def test_empty_categories(self) -> None:
        items = build_line_items_from_itinerary([], [], [])
        assert items == []

    def test_zero_price_excluded(self) -> None:
        flights = [{"origin": "JFK", "destination": "DXB", "price_usd": 0}]
        items = build_line_items_from_itinerary(flights, [], [])
        assert items == []

    def test_only_top_result_included(self) -> None:
        flights = [
            {"origin": "JFK", "destination": "DXB", "airline": "EK", "price_usd": 1200},
            {"origin": "JFK", "destination": "DXB", "airline": "BA", "price_usd": 900},
        ]
        items = build_line_items_from_itinerary(flights, [], [])
        assert len(items) == 1
        assert "EK" in items[0].description
