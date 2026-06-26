"""Tests for zim.booking_store — booking persistence."""

from pathlib import Path

from zim.booking_store import (
    list_bookings,
    load_booking,
    save_booking,
    update_booking_field,
)


def test_save_and_load(tmp_path: Path) -> None:
    record = {
        "booking_id": "bk_001",
        "state": "draft",
        "itinerary": {"destination": "DXB"},
    }
    save_booking(record, directory=tmp_path)
    loaded = load_booking("bk_001", directory=tmp_path)
    assert loaded is not None
    assert loaded["booking_id"] == "bk_001"
    assert loaded["state"] == "draft"
    assert "created_at" in loaded
    assert "updated_at" in loaded


def test_load_missing_returns_none(tmp_path: Path) -> None:
    assert load_booking("nonexistent", directory=tmp_path) is None


def test_update_booking_field(tmp_path: Path) -> None:
    record = {"booking_id": "bk_002", "state": "draft"}
    save_booking(record, directory=tmp_path)

    result = update_booking_field("bk_002", {"state": "paid", "amount": 999}, directory=tmp_path)
    assert result is True

    loaded = load_booking("bk_002", directory=tmp_path)
    assert loaded is not None
    assert loaded["state"] == "paid"
    assert loaded["amount"] == 999


def test_update_nonexistent_returns_false(tmp_path: Path) -> None:
    assert update_booking_field("nope", {"state": "x"}, directory=tmp_path) is False


def test_list_bookings(tmp_path: Path) -> None:
    save_booking({"booking_id": "bk_a", "state": "draft"}, directory=tmp_path)
    save_booking({"booking_id": "bk_b", "state": "paid"}, directory=tmp_path)

    records = list_bookings(directory=tmp_path)
    assert len(records) == 2
    ids = {r["booking_id"] for r in records}
    assert ids == {"bk_a", "bk_b"}
