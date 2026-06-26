"""Service fee configuration and calculation for Zim bookings.

Zim charges a service fee on every booking. Fees are always shown as a
separate line item — never hidden inside travel prices.

Fee types:
    flat                 — fixed dollar amount per booking
    percentage           — percentage of subtotal booking value
    flat_plus_percentage — flat fee + percentage (default)

Default schedule:
    flat_fee_usd = 5.00
    percentage   = 3.0 %
    min_fee_usd  = 2.00   (floor — tiny bookings still generate revenue)
    max_fee_usd  = 50.00  (cap   — expensive trips don't get fee-shocked)

Tenant overrides:
    Pass a custom FeeSchedule to calculate_fee() for per-tenant rates.
"""

from __future__ import annotations

import logging
from typing import Literal, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

FeeType = Literal["flat", "percentage", "flat_plus_percentage"]


class FeeSchedule(BaseModel):
    """Fee schedule — used as default or overridden per tenant."""

    fee_type: FeeType = "flat_plus_percentage"
    flat_fee_usd: float = Field(default=5.00, ge=0, description="Flat fee per booking (USD)")
    percentage: float = Field(default=3.0, ge=0, le=100, description="Percentage of subtotal (0–100)")
    min_fee_usd: float = Field(default=2.00, ge=0, description="Minimum fee floor (USD)")
    max_fee_usd: float = Field(default=50.00, ge=0, description="Maximum fee cap (USD)")

    # Future waiver hooks (not yet active)
    first_booking_free: bool = False


class FeeBreakdown(BaseModel):
    """Transparent fee breakdown returned alongside every booking quote."""

    subtotal_usd: float
    fee_type: FeeType
    fee_amount_usd: float
    total_usd: float
    fee_label: str = "Zim Service Fee"


# Singleton default schedule — all tenants without an override use this
DEFAULT_FEE_SCHEDULE = FeeSchedule()


def calculate_fee(
    subtotal_usd: float,
    schedule: Optional[FeeSchedule] = None,
) -> FeeBreakdown:
    """Calculate the Zim service fee for a given subtotal.

    Applies the schedule's fee type, then clamps to [min_fee_usd, max_fee_usd].

    Args:
        subtotal_usd: Total booking value before Zim fee (USD).
        schedule: Fee schedule to apply; defaults to DEFAULT_FEE_SCHEDULE.

    Returns:
        FeeBreakdown with subtotal, fee amount, and total.
    """
    s = schedule or DEFAULT_FEE_SCHEDULE

    if s.fee_type == "flat":
        raw_fee = s.flat_fee_usd
    elif s.fee_type == "percentage":
        raw_fee = subtotal_usd * (s.percentage / 100.0)
    else:  # flat_plus_percentage
        raw_fee = s.flat_fee_usd + subtotal_usd * (s.percentage / 100.0)

    # Clamp to [min, max]
    fee = max(s.min_fee_usd, min(s.max_fee_usd, raw_fee))
    fee = round(fee, 2)

    logger.debug(
        "Fee calc: subtotal=$%.2f type=%s raw=$%.2f clamped=$%.2f",
        subtotal_usd, s.fee_type, raw_fee, fee,
    )

    return FeeBreakdown(
        subtotal_usd=round(subtotal_usd, 2),
        fee_type=s.fee_type,
        fee_amount_usd=fee,
        total_usd=round(subtotal_usd + fee, 2),
    )
