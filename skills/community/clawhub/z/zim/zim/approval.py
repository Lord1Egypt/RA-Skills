"""Approval flow for Zim trip orchestration.

Generates human-readable approval summaries (WhatsApp-ready),
manages approval state persistence, and provides the ApprovalState enum.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from zim.core import (
    CarResult,
    FlightResult,
    HotelResult,
    Itinerary,
)
from zim.ranking import ScoredResult

logger = logging.getLogger(__name__)

APPROVALS_DIR = Path.home() / ".config" / "zim" / "approvals"


class ApprovalState(str, Enum):
    """Approval workflow states."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_CHANGES = "needs_changes"


# ---------------------------------------------------------------------------
# Approval Summary Generation
# ---------------------------------------------------------------------------

def _format_price(amount: float) -> str:
    """Format a price as USD string."""
    if amount <= 0:
        return "N/A"
    return f"${amount:,.2f}"


def _format_flight_line(flight: FlightResult, score: float | None = None) -> str:
    """Format a single flight for the approval summary."""
    parts: list[str] = []

    airline_info = flight.airline or "Unknown airline"
    if flight.flight_number:
        airline_info += f" {flight.flight_number}"

    parts.append(airline_info)

    route = f"{flight.origin} → {flight.destination}"
    parts.append(route)

    if flight.depart_at:
        parts.append(flight.depart_at.strftime("%b %d, %H:%M"))

    if flight.transfers == 0:
        parts.append("non-stop")
    else:
        parts.append(f"{flight.transfers} stop{'s' if flight.transfers > 1 else ''}")

    parts.append(f"{flight.cabin}")
    parts.append(_format_price(flight.price_usd))

    if flight.refundable:
        parts.append("refundable")

    line = " | ".join(parts)

    if flight.policy_status != "approved":
        line += f" [{flight.policy_status.replace('_', ' ')}]"

    return line


def _format_hotel_line(hotel: HotelResult, score: float | None = None) -> str:
    """Format a single hotel for the approval summary."""
    parts: list[str] = []

    name = hotel.name or "Hotel"
    if hotel.stars > 0:
        name += f" ({hotel.stars}*)"
    parts.append(name)

    if hotel.location:
        parts.append(hotel.location)

    parts.append(f"{_format_price(hotel.nightly_rate_usd)}/night")

    if hotel.refundable:
        parts.append("refundable")

    if hotel.distance_km is not None:
        parts.append(f"{hotel.distance_km:.1f}km to meeting")

    line = " | ".join(parts)

    if hotel.policy_status != "approved":
        line += f" [{hotel.policy_status.replace('_', ' ')}]"

    return line


def _format_car_line(car: CarResult, score: float | None = None) -> str:
    """Format a single car rental for the approval summary."""
    parts: list[str] = []

    parts.append(car.provider or "Car rental")

    if car.vehicle_class:
        parts.append(car.vehicle_class)

    parts.append(_format_price(car.price_usd_total))

    if car.free_cancellation:
        parts.append("free cancellation")

    line = " | ".join(parts)

    if car.policy_status != "approved":
        line += f" [{car.policy_status.replace('_', ' ')}]"

    return line


def generate_approval_summary(
    itinerary: Itinerary,
    flight_scores: list[ScoredResult] | None = None,
    hotel_scores: list[ScoredResult] | None = None,
    car_scores: list[ScoredResult] | None = None,
) -> str:
    """Generate a human-readable, WhatsApp-ready approval summary.

    The summary includes:
    - Trip overview (destination, dates, mode)
    - Recommended flight (top-ranked or first)
    - Recommended hotel (top-ranked or first)
    - Recommended car (top-ranked or first)
    - Total estimated cost
    - Policy compliance status
    - Booking links
    - Action required

    Args:
        itinerary: The assembled trip itinerary.
        flight_scores: Optional ranked flight results for score display.
        hotel_scores: Optional ranked hotel results for score display.
        car_scores: Optional ranked car results for score display.

    Returns:
        Formatted string ready for WhatsApp delivery.
    """
    lines: list[str] = []

    # Header
    dep_date = itinerary.dates.get("departure", "TBD")
    ret_date = itinerary.dates.get("return", "")
    nights = itinerary.dates.get("nights", "")
    date_str = dep_date
    if ret_date:
        date_str += f" → {ret_date}"
    if nights:
        date_str += f" ({nights} nights)"

    mode_label = itinerary.mode.upper()
    lines.append(f"TRIP TO {itinerary.destination} ({mode_label})")
    lines.append(f"Dates: {date_str}")
    lines.append("")

    # Flight
    if itinerary.flights:
        top_flight = itinerary.flights[0]
        lines.append("FLIGHT (recommended)")
        lines.append(f"  {_format_flight_line(top_flight)}")
        if flight_scores and flight_scores[0].rank_reason:
            lines.append(f"  Why: {flight_scores[0].rank_reason}")
        if top_flight.link:
            lines.append(f"  Book: {top_flight.link}")
        if len(itinerary.flights) > 1:
            lines.append(f"  +{len(itinerary.flights) - 1} more option{'s' if len(itinerary.flights) > 2 else ''}")
        lines.append("")
    else:
        lines.append("FLIGHT: No results found")
        lines.append("")

    # Hotel
    if itinerary.hotels:
        top_hotel = itinerary.hotels[0]
        lines.append("HOTEL (recommended)")
        lines.append(f"  {_format_hotel_line(top_hotel)}")
        if hotel_scores and hotel_scores[0].rank_reason:
            lines.append(f"  Why: {hotel_scores[0].rank_reason}")
        if top_hotel.link:
            lines.append(f"  Book: {top_hotel.link}")
        if len(itinerary.hotels) > 1:
            lines.append(f"  +{len(itinerary.hotels) - 1} more option{'s' if len(itinerary.hotels) > 2 else ''}")
        lines.append("")
    else:
        lines.append("HOTEL: No results found")
        lines.append("")

    # Car
    if itinerary.cars:
        top_car = itinerary.cars[0]
        lines.append("CAR (recommended)")
        lines.append(f"  {_format_car_line(top_car)}")
        if car_scores and car_scores[0].rank_reason:
            lines.append(f"  Why: {car_scores[0].rank_reason}")
        if top_car.link:
            lines.append(f"  Book: {top_car.link}")
        if len(itinerary.cars) > 1:
            lines.append(f"  +{len(itinerary.cars) - 1} more option{'s' if len(itinerary.cars) > 2 else ''}")
        lines.append("")
    else:
        lines.append("CAR: No results found")
        lines.append("")

    # Total cost
    lines.append(f"TOTAL: {_format_price(itinerary.total_price_usd)}")
    lines.append("")

    # Policy status
    if itinerary.status == "booking_ready":
        lines.append("STATUS: Within policy - ready to book")
    elif itinerary.status == "approval_required":
        reason = itinerary.approval_reason or "Manual approval needed"
        lines.append(f"STATUS: APPROVAL REQUIRED - {reason}")
    else:
        lines.append(f"STATUS: {itinerary.status.replace('_', ' ').upper()}")
    lines.append("")

    # Action
    if itinerary.status == "approval_required":
        lines.append("Reply YES to approve, or tell me what to change.")
    elif itinerary.status == "booking_ready":
        lines.append("Reply YES to confirm, or tell me what to change.")
    else:
        lines.append("Please provide missing details.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Approval Record Persistence
# ---------------------------------------------------------------------------

def _ensure_approvals_dir() -> Path:
    """Create the approvals directory if it doesn't exist."""
    APPROVALS_DIR.mkdir(parents=True, exist_ok=True)
    return APPROVALS_DIR


def _approval_path(trip_id: str) -> Path:
    """Return the file path for an approval record."""
    return _ensure_approvals_dir() / f"{trip_id}.json"


def save_approval_record(
    itinerary: Itinerary,
    state: ApprovalState,
    trip_id: str | None = None,
    notes: str | None = None,
) -> str:
    """Save an approval record to disk.

    Args:
        itinerary: The trip itinerary.
        state: Current approval state.
        trip_id: Unique trip identifier. Auto-generated if not provided.
        notes: Optional notes about the approval decision.

    Returns:
        The trip_id used for the record.
    """
    if not trip_id:
        trip_id = uuid.uuid4().hex[:16]

    now = datetime.now(UTC).isoformat()
    record = {
        "trip_id": trip_id,
        "state": state.value,
        "destination": itinerary.destination,
        "mode": itinerary.mode,
        "dates": itinerary.dates,
        "total_price_usd": itinerary.total_price_usd,
        "status": itinerary.status,
        "approval_reason": itinerary.approval_reason,
        "notes": notes,
        "created_at": now,
        "updated_at": now,
        "itinerary": itinerary.model_dump(),
    }

    path = _approval_path(trip_id)
    path.write_text(json.dumps(record, indent=2, default=str))
    logger.info("Saved approval record %s to %s", trip_id, path)

    return trip_id


def load_approval_record(trip_id: str) -> dict[str, Any] | None:
    """Load an approval record from disk.

    Args:
        trip_id: The unique trip identifier.

    Returns:
        The approval record dict, or None if not found.
    """
    path = _approval_path(trip_id)
    if not path.exists():
        logger.debug("No approval record found at %s", path)
        return None

    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, Exception) as exc:
        logger.warning("Failed to load approval record from %s: %s", path, exc)
        return None


def update_approval_state(
    trip_id: str,
    new_state: ApprovalState,
    notes: str | None = None,
) -> bool:
    """Update the state of an existing approval record.

    Args:
        trip_id: The unique trip identifier.
        new_state: New approval state to set.
        notes: Optional notes about the state change.

    Returns:
        True if updated successfully, False if record not found.
    """
    record = load_approval_record(trip_id)
    if record is None:
        return False

    record["state"] = new_state.value
    record["updated_at"] = datetime.now(UTC).isoformat()
    if notes:
        record["notes"] = notes

    path = _approval_path(trip_id)
    path.write_text(json.dumps(record, indent=2, default=str))
    logger.info("Updated approval record %s to state %s", trip_id, new_state.value)

    return True
