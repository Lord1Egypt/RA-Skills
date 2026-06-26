"""Booking state machine for Zim.

Manages the full lifecycle of a travel booking:

    draft
      → needs_traveler_info
        → ready_for_payment
          → payment_pending
            → paid
              → booking_in_progress
                → booked | failed

Each state transition is explicit and validated. The booking record
persists to disk at every transition so the agent can resume after
restarts.
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

from zim.booking_executor import (
    BookingExecutionRequest,
    BookingExecutionResult,
    PlaceholderExecutor,
    get_executor,
)
from zim.booking_store import load_booking, save_booking, update_booking_field
from zim.core import Itinerary
from zim.payment import (
    CheckoutLineItem,
    CheckoutResult,
    StripeConfig,
    build_line_items_from_itinerary,
    create_checkout_session,
)
from zim.traveler_info import TravelerInfo

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State enum
# ---------------------------------------------------------------------------

class BookingState(str, Enum):
    """All possible booking states."""

    DRAFT = "draft"
    NEEDS_TRAVELER_INFO = "needs_traveler_info"
    READY_FOR_PAYMENT = "ready_for_payment"
    PAYMENT_PENDING = "payment_pending"
    PAID = "paid"
    BOOKING_IN_PROGRESS = "booking_in_progress"
    BOOKED = "booked"
    FAILED = "failed"
    CANCELLED = "cancelled"


# Valid transitions: current_state → set of allowed next states
_TRANSITIONS: dict[BookingState, set[BookingState]] = {
    BookingState.DRAFT: {BookingState.NEEDS_TRAVELER_INFO, BookingState.CANCELLED},
    BookingState.NEEDS_TRAVELER_INFO: {
        BookingState.READY_FOR_PAYMENT,
        BookingState.NEEDS_TRAVELER_INFO,  # re-enter with updated info
        BookingState.CANCELLED,
    },
    BookingState.READY_FOR_PAYMENT: {
        BookingState.PAYMENT_PENDING,
        BookingState.NEEDS_TRAVELER_INFO,  # back if info changed
        BookingState.CANCELLED,
    },
    BookingState.PAYMENT_PENDING: {
        BookingState.PAID,
        BookingState.FAILED,
        BookingState.CANCELLED,
    },
    BookingState.PAID: {
        BookingState.BOOKING_IN_PROGRESS,
        BookingState.FAILED,
    },
    BookingState.BOOKING_IN_PROGRESS: {
        BookingState.BOOKED,
        BookingState.FAILED,
    },
    BookingState.BOOKED: set(),  # terminal
    BookingState.FAILED: {BookingState.DRAFT},  # allow retry
    BookingState.CANCELLED: set(),  # terminal
}


class InvalidTransitionError(Exception):
    """Raised when a state transition is not allowed."""
    pass


# ---------------------------------------------------------------------------
# Booking model
# ---------------------------------------------------------------------------

class Booking(BaseModel):
    """A booking moving through the state machine.

    This is the in-memory representation. It is serialized to/from
    the booking store as a dict.
    """

    booking_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    state: BookingState = BookingState.DRAFT
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())

    # Trip / itinerary snapshot (set at creation)
    itinerary: Optional[dict[str, Any]] = None
    trip_id: Optional[str] = None  # links back to approval record

    # Traveler info (populated during needs_traveler_info)
    traveler_info: Optional[dict[str, Any]] = None
    traveler_info_missing: list[str] = Field(default_factory=list)

    # Approval
    approved_by: Optional[str] = None
    approved_at: Optional[str] = None

    # Payment (populated during payment_pending / paid)
    stripe_session_id: Optional[str] = None
    stripe_checkout_url: Optional[str] = None
    payment_status: Optional[str] = None
    amount_total_cents: int = 0

    # Booking execution (populated during booking_in_progress / booked)
    provider_confirmation_code: Optional[str] = None
    provider_status: Optional[str] = None
    provider_raw_response: Optional[dict[str, Any]] = None
    execution_results: list[dict[str, Any]] = Field(default_factory=list)

    # Errors
    error_message: Optional[str] = None
    state_history: list[dict[str, str]] = Field(default_factory=list)

    def _record_transition(self, from_state: BookingState, to_state: BookingState) -> None:
        self.state_history.append({
            "from": from_state.value,
            "to": to_state.value,
            "at": datetime.now(UTC).isoformat(),
        })
        self.updated_at = datetime.now(UTC).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Booking":
        return cls.model_validate(data)


# ---------------------------------------------------------------------------
# State machine operations
# ---------------------------------------------------------------------------

def _validate_transition(current: BookingState, target: BookingState) -> None:
    """Raise if the transition is not allowed."""
    allowed = _TRANSITIONS.get(current, set())
    if target not in allowed:
        raise InvalidTransitionError(
            f"Cannot transition from {current.value} to {target.value}. "
            f"Allowed: {[s.value for s in allowed]}"
        )


def create_booking(
    itinerary: Itinerary,
    trip_id: str | None = None,
    approved_by: str | None = None,
    store_dir=None,
) -> Booking:
    """Create a new booking from an approved itinerary.

    Starts in DRAFT and immediately transitions to NEEDS_TRAVELER_INFO.
    """
    booking = Booking(
        itinerary=itinerary.model_dump(),
        trip_id=trip_id,
        approved_by=approved_by,
        approved_at=datetime.now(UTC).isoformat() if approved_by else None,
    )

    # Persist initial draft
    save_booking(booking.to_dict(), directory=store_dir)

    # Transition to needs_traveler_info
    _validate_transition(booking.state, BookingState.NEEDS_TRAVELER_INFO)
    booking._record_transition(booking.state, BookingState.NEEDS_TRAVELER_INFO)
    booking.state = BookingState.NEEDS_TRAVELER_INFO
    save_booking(booking.to_dict(), directory=store_dir)

    logger.info("Created booking %s (state: %s)", booking.booking_id, booking.state.value)
    return booking


def submit_traveler_info(
    booking_id: str,
    traveler_info: TravelerInfo,
    require_passport: bool = True,
    store_dir=None,
) -> Booking:
    """Submit traveler information for a booking.

    If all required fields are present, transitions to READY_FOR_PAYMENT.
    Otherwise stays in NEEDS_TRAVELER_INFO with the missing fields listed.
    """
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        raise ValueError(f"Booking {booking_id} not found")

    booking = Booking.from_dict(record)

    if booking.state not in (BookingState.NEEDS_TRAVELER_INFO, BookingState.READY_FOR_PAYMENT):
        raise InvalidTransitionError(
            f"Cannot submit traveler info in state {booking.state.value}"
        )

    missing = traveler_info.missing_required_fields(require_passport=require_passport)
    booking.traveler_info = traveler_info.model_dump()
    booking.traveler_info_missing = missing

    if missing:
        # Stay in needs_traveler_info
        if booking.state != BookingState.NEEDS_TRAVELER_INFO:
            booking._record_transition(booking.state, BookingState.NEEDS_TRAVELER_INFO)
            booking.state = BookingState.NEEDS_TRAVELER_INFO
        logger.info("Booking %s: still needs traveler info: %s", booking_id, missing)
    else:
        # Transition to ready_for_payment
        target = BookingState.READY_FOR_PAYMENT
        _validate_transition(booking.state, target)
        booking._record_transition(booking.state, target)
        booking.state = target
        logger.info("Booking %s: traveler info complete → ready_for_payment", booking_id)

    save_booking(booking.to_dict(), directory=store_dir)
    return booking


def initiate_payment(
    booking_id: str,
    stripe_config: StripeConfig | None = None,
    store_dir=None,
) -> Booking:
    """Create a Stripe checkout session and transition to PAYMENT_PENDING.

    Requires the booking to be in READY_FOR_PAYMENT state.
    """
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        raise ValueError(f"Booking {booking_id} not found")

    booking = Booking.from_dict(record)
    _validate_transition(booking.state, BookingState.PAYMENT_PENDING)

    # Build line items from itinerary
    itin = booking.itinerary or {}
    nights = itin.get("dates", {}).get("nights", 1)
    line_items = build_line_items_from_itinerary(
        itinerary_flights=[f for f in (itin.get("flights") or [])],
        itinerary_hotels=[h for h in (itin.get("hotels") or [])],
        itinerary_cars=[c for c in (itin.get("cars") or [])],
        nights=nights if isinstance(nights, int) else 1,
    )

    if not line_items:
        raise ValueError("No line items to charge — itinerary has no priced items")

    # Get customer email from traveler info
    trav = booking.traveler_info or {}
    customer_email = trav.get("email")

    # Create Stripe session
    checkout = create_checkout_session(
        booking_id=booking_id,
        line_items=line_items,
        customer_email=customer_email,
        config=stripe_config,
        metadata={"trip_id": booking.trip_id or ""},
    )

    # Update booking
    booking.stripe_session_id = checkout.session_id
    booking.stripe_checkout_url = checkout.checkout_url
    booking.payment_status = checkout.payment_status
    booking.amount_total_cents = checkout.amount_total_cents
    booking._record_transition(booking.state, BookingState.PAYMENT_PENDING)
    booking.state = BookingState.PAYMENT_PENDING

    save_booking(booking.to_dict(), directory=store_dir)
    logger.info(
        "Booking %s: payment initiated (session %s, url %s)",
        booking_id, checkout.session_id, checkout.checkout_url,
    )
    return booking


def confirm_payment(
    booking_id: str,
    payment_status: str = "paid",
    stripe_session_id: str | None = None,
    store_dir=None,
) -> Booking:
    """Confirm that payment was received. Transitions to PAID.

    Called by the Stripe webhook handler or manual confirmation.
    """
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        raise ValueError(f"Booking {booking_id} not found")

    booking = Booking.from_dict(record)
    _validate_transition(booking.state, BookingState.PAID)

    booking.payment_status = payment_status
    if stripe_session_id:
        booking.stripe_session_id = stripe_session_id
    booking._record_transition(booking.state, BookingState.PAID)
    booking.state = BookingState.PAID

    save_booking(booking.to_dict(), directory=store_dir)
    logger.info("Booking %s: payment confirmed → paid", booking_id)
    return booking


def execute_booking(
    booking_id: str,
    executor_name: str = "placeholder",
    store_dir=None,
) -> Booking:
    """Attempt to execute the booking with provider(s).

    Transitions PAID → BOOKING_IN_PROGRESS → BOOKED or FAILED.
    """
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        raise ValueError(f"Booking {booking_id} not found")

    booking = Booking.from_dict(record)
    _validate_transition(booking.state, BookingState.BOOKING_IN_PROGRESS)

    booking._record_transition(booking.state, BookingState.BOOKING_IN_PROGRESS)
    booking.state = BookingState.BOOKING_IN_PROGRESS
    save_booking(booking.to_dict(), directory=store_dir)

    executor = get_executor(executor_name)
    itin = booking.itinerary or {}
    trav = booking.traveler_info or {}

    results: list[BookingExecutionResult] = []
    all_confirmed = True
    has_failure = False

    # Execute for each category that has items
    categories = [
        ("flight", itin.get("flights", [])),
        ("hotel", itin.get("hotels", [])),
        ("car", itin.get("cars", [])),
    ]

    for category, items in categories:
        if not items:
            continue
        top_item = items[0]

        request = BookingExecutionRequest(
            booking_id=booking_id,
            category=category,
            provider_name=top_item.get("airline", "") or top_item.get("provider", "") or top_item.get("name", ""),
            provider_link=top_item.get("link", ""),
            search_result_id=top_item.get("id", ""),
            traveler_first_name=trav.get("first_name", ""),
            traveler_last_name=trav.get("last_name", ""),
            traveler_email=trav.get("email", ""),
            traveler_phone=trav.get("phone", ""),
            traveler_passport_number=trav.get("passport_number"),
            stripe_session_id=booking.stripe_session_id or "",
            amount_cents=booking.amount_total_cents,
            origin=itin.get("flights", [{}])[0].get("origin", "") if category == "flight" else "",
            destination=itin.get("destination", ""),
            departure_date=itin.get("dates", {}).get("departure"),
            return_date=itin.get("dates", {}).get("return"),
        )

        result = executor.execute(request)
        results.append(result)

        if not result.is_confirmed and result.provider_status != "pending_provider_integration":
            has_failure = True
        if result.provider_status != "confirmed":
            all_confirmed = False

    # Store results
    booking.execution_results = [r.model_dump() for r in results]

    # Determine final state
    if has_failure:
        booking._record_transition(booking.state, BookingState.FAILED)
        booking.state = BookingState.FAILED
        booking.error_message = "One or more booking executions failed"
    elif all_confirmed:
        booking._record_transition(booking.state, BookingState.BOOKED)
        booking.state = BookingState.BOOKED
        # Take the first confirmation code
        for r in results:
            if r.provider_confirmation_code:
                booking.provider_confirmation_code = r.provider_confirmation_code
                break
    else:
        # Placeholder executor returns pending_provider_integration,
        # which is not a failure — the booking stays in booking_in_progress
        # until manual confirmation. For the MVP, we move to BOOKED with
        # a note that provider integration is pending.
        booking._record_transition(booking.state, BookingState.BOOKED)
        booking.state = BookingState.BOOKED
        booking.provider_status = "pending_provider_integration"

    for r in results:
        if r.provider_raw_response:
            booking.provider_raw_response = r.provider_raw_response
            break

    save_booking(booking.to_dict(), directory=store_dir)
    logger.info("Booking %s: execution complete → %s", booking_id, booking.state.value)
    return booking


def cancel_booking(
    booking_id: str,
    reason: str | None = None,
    store_dir=None,
) -> Booking:
    """Cancel a booking. Only allowed from certain states."""
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        raise ValueError(f"Booking {booking_id} not found")

    booking = Booking.from_dict(record)
    _validate_transition(booking.state, BookingState.CANCELLED)

    booking._record_transition(booking.state, BookingState.CANCELLED)
    booking.state = BookingState.CANCELLED
    booking.error_message = reason

    save_booking(booking.to_dict(), directory=store_dir)
    logger.info("Booking %s: cancelled (%s)", booking_id, reason or "no reason")
    return booking


def get_booking(booking_id: str, store_dir=None) -> Booking | None:
    """Load a booking by ID. Returns None if not found."""
    record = load_booking(booking_id, directory=store_dir)
    if record is None:
        return None
    return Booking.from_dict(record)
