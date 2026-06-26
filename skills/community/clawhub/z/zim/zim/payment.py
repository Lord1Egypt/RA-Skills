"""Stripe checkout session creation for Zim bookings.

Creates Stripe Checkout Sessions in **test mode** for the MVP.
The real payment flow:
1. Agent builds an itinerary and gets user approval
2. Zim creates a Stripe Checkout Session with the trip line items
3. User is redirected to Stripe's hosted checkout page
4. On success, webhook or redirect confirms payment
5. Booking executor is triggered after payment confirmation

Environment:
    STRIPE_SECRET_KEY  — sk_test_... for test mode
    STRIPE_WEBHOOK_SECRET — whsec_... for webhook signature verification
    ZIM_BASE_URL — base URL for success/cancel redirects (default: http://localhost:8000)
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

from pydantic import BaseModel, Field

from zim.fees import FeeBreakdown, FeeSchedule, calculate_fee

logger = logging.getLogger(__name__)


class CheckoutLineItem(BaseModel):
    """A single line item for the Stripe checkout session."""

    description: str
    amount_cents: int = Field(..., gt=0, description="Amount in cents (USD)")
    quantity: int = 1
    category: str = ""  # flight / hotel / car


class CheckoutResult(BaseModel):
    """Result of creating a Stripe checkout session."""

    session_id: str
    checkout_url: str
    payment_status: str = "unpaid"
    amount_total_cents: int = 0
    currency: str = "usd"
    metadata: dict[str, str] = Field(default_factory=dict)


class StripeConfig(BaseModel):
    """Stripe configuration — loaded from environment."""

    secret_key: str = ""
    webhook_secret: str = ""
    base_url: str = "http://localhost:8000"

    @classmethod
    def from_env(cls) -> "StripeConfig":
        return cls(
            secret_key=os.environ.get("STRIPE_SECRET_KEY", ""),
            webhook_secret=os.environ.get("STRIPE_WEBHOOK_SECRET", ""),
            base_url=os.environ.get("ZIM_BASE_URL", "http://localhost:8000"),
        )

    @property
    def is_configured(self) -> bool:
        return bool(self.secret_key)


def create_checkout_session(
    booking_id: str,
    line_items: list[CheckoutLineItem],
    customer_email: Optional[str] = None,
    config: Optional[StripeConfig] = None,
    metadata: Optional[dict[str, str]] = None,
) -> CheckoutResult:
    """Create a Stripe Checkout Session for a booking.

    Uses Stripe's hosted checkout page — we never touch raw card data.

    Args:
        booking_id: Zim booking ID to attach as metadata.
        line_items: Items to charge for.
        customer_email: Pre-fill the email on checkout.
        config: Stripe config (loads from env if not provided).
        metadata: Extra metadata to attach to the session.

    Returns:
        CheckoutResult with session_id and checkout_url.

    Raises:
        EnvironmentError: If STRIPE_SECRET_KEY is not set.
        stripe.error.StripeError: On Stripe API failures.
    """
    import stripe

    cfg = config or StripeConfig.from_env()
    if not cfg.is_configured:
        raise EnvironmentError(
            "STRIPE_SECRET_KEY is not set. "
            "Set it to sk_test_... for test mode."
        )

    stripe.api_key = cfg.secret_key

    # Build Stripe line items
    stripe_items = []
    for item in line_items:
        stripe_items.append({
            "price_data": {
                "currency": "usd",
                "unit_amount": item.amount_cents,
                "product_data": {
                    "name": item.description,
                    "metadata": {"category": item.category},
                },
            },
            "quantity": item.quantity,
        })

    session_metadata = {"booking_id": booking_id}
    if metadata:
        session_metadata.update(metadata)

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=stripe_items,
        success_url=f"{cfg.base_url}/booking/{booking_id}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{cfg.base_url}/booking/{booking_id}/cancel",
        customer_email=customer_email,
        metadata=session_metadata,
        payment_intent_data={
            "metadata": session_metadata,
        },
    )

    logger.info(
        "Created Stripe checkout session %s for booking %s (total: %d cents)",
        session.id, booking_id, session.amount_total or 0,
    )

    return CheckoutResult(
        session_id=session.id,
        checkout_url=session.url or "",
        payment_status=session.payment_status or "unpaid",
        amount_total_cents=session.amount_total or 0,
        currency=session.currency or "usd",
        metadata=session_metadata,
    )


def retrieve_session_status(
    session_id: str,
    config: Optional[StripeConfig] = None,
) -> dict[str, Any]:
    """Retrieve the current status of a Stripe checkout session.

    Returns a dict with payment_status, amount_total, and customer_email.
    """
    import stripe

    cfg = config or StripeConfig.from_env()
    if not cfg.is_configured:
        raise EnvironmentError("STRIPE_SECRET_KEY is not set.")

    stripe.api_key = cfg.secret_key
    session = stripe.checkout.Session.retrieve(session_id)

    return {
        "session_id": session.id,
        "payment_status": session.payment_status,
        "amount_total_cents": session.amount_total,
        "currency": session.currency,
        "customer_email": session.customer_details.email if session.customer_details else None,
        "status": session.status,
    }


def build_line_items_from_itinerary(
    itinerary_flights: list[dict],
    itinerary_hotels: list[dict],
    itinerary_cars: list[dict],
    nights: int = 1,
    fee_schedule: Optional[FeeSchedule] = None,
) -> tuple[list[CheckoutLineItem], FeeBreakdown]:
    """Build Stripe line items from the top-ranked result in each category.

    Only the recommended (first) item in each category is included.
    A 'Zim Service Fee' line item is always appended as a transparent
    separate charge — never hidden inside travel prices.

    Args:
        itinerary_flights: Ranked flight results from the itinerary.
        itinerary_hotels:  Ranked hotel results from the itinerary.
        itinerary_cars:    Ranked car results from the itinerary.
        nights:            Number of hotel nights for rate multiplication.
        fee_schedule:      Override fee schedule; uses default if None.

    Returns:
        Tuple of (line_items, fee_breakdown). line_items includes the
        service fee as the final entry.
    """
    items: list[CheckoutLineItem] = []
    subtotal_cents = 0

    if itinerary_flights:
        f = itinerary_flights[0]
        price = f.get("price_usd", 0)
        if price > 0:
            desc = f"Flight: {f.get('origin', '?')} → {f.get('destination', '?')}"
            airline = f.get("airline", "")
            if airline:
                desc += f" ({airline})"
            amount = int(price * 100)
            items.append(CheckoutLineItem(
                description=desc,
                amount_cents=amount,
                category="flight",
            ))
            subtotal_cents += amount

    if itinerary_hotels:
        h = itinerary_hotels[0]
        rate = h.get("nightly_rate_usd", 0)
        if rate > 0:
            desc = f"Hotel: {h.get('name', 'Hotel')} ({nights} night{'s' if nights > 1 else ''})"
            amount = int(rate * 100)
            items.append(CheckoutLineItem(
                description=desc,
                amount_cents=amount,
                quantity=nights,
                category="hotel",
            ))
            subtotal_cents += amount * nights

    if itinerary_cars:
        c = itinerary_cars[0]
        price = c.get("price_usd_total", 0)
        if price > 0:
            desc = f"Car rental: {c.get('provider', 'Rental')} {c.get('vehicle_class', '')}"
            amount = int(price * 100)
            items.append(CheckoutLineItem(
                description=desc,
                amount_cents=amount,
                category="car",
            ))
            subtotal_cents += amount

    # Always append the Zim service fee as a visible line item
    subtotal_usd = subtotal_cents / 100.0
    breakdown = calculate_fee(subtotal_usd, fee_schedule)
    fee_cents = int(round(breakdown.fee_amount_usd * 100))

    if fee_cents > 0:
        items.append(CheckoutLineItem(
            description=breakdown.fee_label,
            amount_cents=fee_cents,
            category="service_fee",
        ))
        logger.info(
            "Service fee: $%.2f on $%.2f subtotal (type=%s)",
            breakdown.fee_amount_usd, subtotal_usd, breakdown.fee_type,
        )

    return items, breakdown
