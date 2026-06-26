from __future__ import annotations

from pathlib import Path

from zim.approval import ApprovalState, generate_approval_summary, load_approval_record, save_approval_record
from zim.core import CarResult, FlightResult, HotelResult, Itinerary


def test_generate_approval_summary_includes_key_sections() -> None:
    itinerary = Itinerary(
        destination="DXB",
        mode="business",
        dates={"departure": "2026-04-15", "return": "2026-04-20", "nights": 5},
        flights=[
            FlightResult(
                airline="EK",
                flight_number="EK202",
                origin="JFK",
                destination="DXB",
                price_usd=1200,
                refundable=True,
                link="https://flight.example",
            )
        ],
        hotels=[
            HotelResult(
                name="Four Seasons Dubai",
                stars=5,
                location="DIFC",
                nightly_rate_usd=400,
                refundable=True,
                link="https://hotel.example",
            )
        ],
        cars=[
            CarResult(
                provider="Rentalcars",
                vehicle_class="suv",
                price_usd_total=300,
                free_cancellation=True,
                link="https://car.example",
            )
        ],
        total_price_usd=3500,
        status="approval_required",
        approval_reason="Total exceeds policy threshold",
    )

    summary = generate_approval_summary(itinerary)
    assert "TRIP TO DXB" in summary
    assert "FLIGHT (recommended)" in summary
    assert "HOTEL (recommended)" in summary
    assert "CAR (recommended)" in summary
    assert "TOTAL: $3,500.00" in summary
    assert "APPROVAL REQUIRED" in summary
    assert "https://flight.example" in summary
    assert "Reply YES to approve" in summary


def test_save_and_load_approval_record(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr("zim.approval.APPROVALS_DIR", tmp_path)

    itinerary = Itinerary(
        destination="LHR",
        mode="personal",
        dates={"departure": "2026-05-01"},
        total_price_usd=999.0,
        status="booking_ready",
    )

    trip_id = save_approval_record(itinerary, ApprovalState.PENDING, trip_id="trip123")
    assert trip_id == "trip123"

    record = load_approval_record("trip123")
    assert record is not None
    assert record["trip_id"] == "trip123"
    assert record["state"] == "pending"
    assert record["destination"] == "LHR"
