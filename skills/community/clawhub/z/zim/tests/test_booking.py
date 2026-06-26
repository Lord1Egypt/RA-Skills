"""Tests for zim.booking — the booking state machine.

Tests the full lifecycle: create → submit_traveler_info → confirm_payment →
execute_booking, plus invalid transition checks and cancellation.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from zim.booking import (
    Booking,
    BookingState,
    InvalidTransitionError,
    cancel_booking,
    confirm_payment,
    create_booking,
    execute_booking,
    get_booking,
    submit_traveler_info,
)
from zim.core import FlightResult, HotelResult, CarResult, Itinerary
from zim.traveler_info import TravelerInfo


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_itinerary(**kwargs) -> Itinerary:
    defaults = dict(
        destination="DXB",
        mode="business",
        dates={"departure": "2026-04-15", "return": "2026-04-20", "nights": 5},
        flights=[
            FlightResult(
                airline="EK", flight_number="EK202",
                origin="JFK", destination="DXB",
                price_usd=1200, refundable=True,
                link="https://flight.example",
            )
        ],
        hotels=[
            HotelResult(
                name="Four Seasons Dubai", stars=5,
                location="DIFC", nightly_rate_usd=400,
                refundable=True, link="https://hotel.example",
            )
        ],
        cars=[
            CarResult(
                provider="Hertz", vehicle_class="suv",
                price_usd_total=300, free_cancellation=True,
                link="https://car.example",
            )
        ],
        total_price_usd=3500,
        status="booking_ready",
    )
    defaults.update(kwargs)
    return Itinerary(**defaults)


def _make_complete_traveler() -> TravelerInfo:
    return TravelerInfo(
        first_name="Robin",
        last_name="Zieme",
        date_of_birth=date(1990, 5, 15),
        gender="M",
        passport_number="AB1234567",
        passport_expiry=date(2030, 12, 31),
        passport_country="DE",
        email="robin@example.com",
        phone="+971544042230",
    )


# ---------------------------------------------------------------------------
# State machine tests
# ---------------------------------------------------------------------------

class TestCreateBooking:
    def test_creates_in_needs_traveler_info(self, tmp_path: Path) -> None:
        itinerary = _make_itinerary()
        booking = create_booking(itinerary, trip_id="trip_001", approved_by="Robin", store_dir=tmp_path)

        assert booking.state == BookingState.NEEDS_TRAVELER_INFO
        assert booking.trip_id == "trip_001"
        assert booking.approved_by == "Robin"
        assert booking.approved_at is not None
        assert booking.itinerary is not None
        assert len(booking.state_history) == 1
        assert booking.state_history[0]["from"] == "draft"
        assert booking.state_history[0]["to"] == "needs_traveler_info"

    def test_persists_to_store(self, tmp_path: Path) -> None:
        itinerary = _make_itinerary()
        booking = create_booking(itinerary, store_dir=tmp_path)

        loaded = get_booking(booking.booking_id, store_dir=tmp_path)
        assert loaded is not None
        assert loaded.state == BookingState.NEEDS_TRAVELER_INFO


class TestSubmitTravelerInfo:
    def test_complete_info_transitions_to_ready_for_payment(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        traveler = _make_complete_traveler()

        updated = submit_traveler_info(booking.booking_id, traveler, store_dir=tmp_path)

        assert updated.state == BookingState.READY_FOR_PAYMENT
        assert updated.traveler_info is not None
        assert updated.traveler_info["first_name"] == "Robin"
        assert updated.traveler_info_missing == []

    def test_incomplete_info_stays_in_needs_traveler_info(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        traveler = TravelerInfo(first_name="Robin")  # missing most fields

        updated = submit_traveler_info(booking.booking_id, traveler, store_dir=tmp_path)

        assert updated.state == BookingState.NEEDS_TRAVELER_INFO
        assert "last_name" in updated.traveler_info_missing
        assert "email" in updated.traveler_info_missing

    def test_domestic_no_passport_required(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        traveler = TravelerInfo(
            first_name="Robin",
            last_name="Zieme",
            date_of_birth=date(1990, 1, 1),
            email="r@example.com",
            phone="+1234",
        )

        updated = submit_traveler_info(
            booking.booking_id, traveler, require_passport=False, store_dir=tmp_path,
        )
        assert updated.state == BookingState.READY_FOR_PAYMENT

    def test_resubmit_with_updates(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)

        # First submit: incomplete
        submit_traveler_info(
            booking.booking_id,
            TravelerInfo(first_name="Robin"),
            store_dir=tmp_path,
        )

        # Second submit: complete
        updated = submit_traveler_info(
            booking.booking_id,
            _make_complete_traveler(),
            store_dir=tmp_path,
        )
        assert updated.state == BookingState.READY_FOR_PAYMENT


class TestConfirmPayment:
    def test_transitions_to_paid(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        submit_traveler_info(booking.booking_id, _make_complete_traveler(), store_dir=tmp_path)

        # Skip Stripe (initiate_payment needs real Stripe) — manually set state
        from zim.booking_store import load_booking as load_raw, save_booking as save_raw
        record = load_raw(booking.booking_id, directory=tmp_path)
        record["state"] = "payment_pending"
        record["stripe_session_id"] = "cs_test_fake"
        save_raw(record, directory=tmp_path)

        confirmed = confirm_payment(booking.booking_id, store_dir=tmp_path)
        assert confirmed.state == BookingState.PAID
        assert confirmed.payment_status == "paid"

    def test_invalid_transition_from_draft(self, tmp_path: Path) -> None:
        """Cannot confirm payment directly from needs_traveler_info."""
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)

        with pytest.raises(InvalidTransitionError):
            confirm_payment(booking.booking_id, store_dir=tmp_path)


class TestExecuteBooking:
    def test_placeholder_executor_moves_to_booked(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        submit_traveler_info(booking.booking_id, _make_complete_traveler(), store_dir=tmp_path)

        # Manually move to paid
        from zim.booking_store import load_booking as load_raw, save_booking as save_raw
        record = load_raw(booking.booking_id, directory=tmp_path)
        record["state"] = "paid"
        record["payment_status"] = "paid"
        save_raw(record, directory=tmp_path)

        executed = execute_booking(booking.booking_id, store_dir=tmp_path)

        assert executed.state == BookingState.BOOKED
        assert executed.provider_status == "pending_provider_integration"
        assert len(executed.execution_results) >= 1
        assert executed.provider_raw_response is not None
        assert executed.provider_raw_response.get("manual_action_required") is True

    def test_invalid_transition_from_needs_info(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        with pytest.raises(InvalidTransitionError):
            execute_booking(booking.booking_id, store_dir=tmp_path)


class TestCancelBooking:
    def test_cancel_from_needs_traveler_info(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        cancelled = cancel_booking(booking.booking_id, reason="Changed plans", store_dir=tmp_path)
        assert cancelled.state == BookingState.CANCELLED
        assert cancelled.error_message == "Changed plans"

    def test_cancel_from_ready_for_payment(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        submit_traveler_info(booking.booking_id, _make_complete_traveler(), store_dir=tmp_path)
        cancelled = cancel_booking(booking.booking_id, store_dir=tmp_path)
        assert cancelled.state == BookingState.CANCELLED

    def test_cannot_cancel_booked(self, tmp_path: Path) -> None:
        booking = create_booking(_make_itinerary(), store_dir=tmp_path)
        submit_traveler_info(booking.booking_id, _make_complete_traveler(), store_dir=tmp_path)

        # Move to booked
        from zim.booking_store import load_booking as load_raw, save_booking as save_raw
        record = load_raw(booking.booking_id, directory=tmp_path)
        record["state"] = "booked"
        save_raw(record, directory=tmp_path)

        with pytest.raises(InvalidTransitionError):
            cancel_booking(booking.booking_id, store_dir=tmp_path)


class TestBookingModel:
    def test_round_trip_serialization(self) -> None:
        booking = Booking(
            booking_id="bk_test",
            state=BookingState.DRAFT,
            itinerary={"destination": "DXB"},
        )
        data = booking.to_dict()
        restored = Booking.from_dict(data)
        assert restored.booking_id == "bk_test"
        assert restored.state == BookingState.DRAFT
        assert restored.itinerary == {"destination": "DXB"}

    def test_state_history_tracking(self) -> None:
        booking = Booking(state=BookingState.DRAFT)
        booking._record_transition(BookingState.DRAFT, BookingState.NEEDS_TRAVELER_INFO)
        booking.state = BookingState.NEEDS_TRAVELER_INFO

        assert len(booking.state_history) == 1
        assert booking.state_history[0]["from"] == "draft"
        assert booking.state_history[0]["to"] == "needs_traveler_info"


class TestFullLifecycle:
    """Test the complete booking lifecycle end to end (sans real Stripe)."""

    def test_draft_through_booked(self, tmp_path: Path) -> None:
        # 1. Create booking
        itinerary = _make_itinerary()
        booking = create_booking(itinerary, trip_id="t1", approved_by="Robin", store_dir=tmp_path)
        assert booking.state == BookingState.NEEDS_TRAVELER_INFO

        # 2. Submit traveler info
        booking = submit_traveler_info(
            booking.booking_id, _make_complete_traveler(), store_dir=tmp_path
        )
        assert booking.state == BookingState.READY_FOR_PAYMENT

        # 3. Simulate payment (skip Stripe)
        from zim.booking_store import load_booking as load_raw, save_booking as save_raw
        record = load_raw(booking.booking_id, directory=tmp_path)
        record["state"] = "payment_pending"
        record["stripe_session_id"] = "cs_test_lifecycle"
        save_raw(record, directory=tmp_path)

        booking = confirm_payment(booking.booking_id, store_dir=tmp_path)
        assert booking.state == BookingState.PAID

        # 4. Execute booking (placeholder)
        booking = execute_booking(booking.booking_id, store_dir=tmp_path)
        assert booking.state == BookingState.BOOKED
        assert booking.provider_status == "pending_provider_integration"

        # 5. Verify full state history
        assert len(booking.state_history) >= 4
        states = [h["to"] for h in booking.state_history]
        assert "needs_traveler_info" in states
        assert "ready_for_payment" in states
        assert "paid" in states
        assert "booked" in states
