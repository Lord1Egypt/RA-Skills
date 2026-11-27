"""refresh_plan.py: dated facts by age, and a plan's flights against what is on sale now. Offline."""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import refresh_plan as R  # noqa: E402


def card(provider, out, ret, fare, checked="2026-08-09"):
    return {"id": f"fl-{provider}", "provider": provider, "fare_low": fare, "price_checked_at": checked,
            "outbound_itinerary": {"departure_local": out}, "return_itinerary": {"departure_local": ret}}


PLAN = {
    "trip": {"currency": "EUR"},
    "booking_options": {"flights": [
        card("Transavia", "AMS 10:00（CET）", "ALC 20:15（CET）", 154),
        card("Vueling（经 KAYAK 比价）", "AMS 14:35（CET）", "ALC 11:00（CET）", 132),
    ]},
    "days": [{"route": {"map_checked_at": "2026-08-09"}}],
    "entry_context": {"checked_at": "2026-11-20"},
}

NOW = [
    card("Transavia", "2027-02-12 10:00", "2027-02-16 20:15", 159),
    card("Transavia", "2027-02-12 06:45", "2027-02-16 20:15", 141),
    card("Vueling", "2027-02-12 15:25", "2027-02-16 11:00", 157),
]


def test_flight_diff_names_what_changed() -> None:
    lines = R.flight_diff(PLAN, NOW)
    assert any("Transavia 10:00/20:15: still on sale, now 159" in l and "+5" in l for l in lines)
    vueling = next(l for l in lines if "Vueling 14:35/11:00" in l)
    assert "NOT on sale" in vueling and "15:25/11:00 157" in vueling
    assert any(l.startswith("CHEAPEST NOW: Transavia 06:45/20:15 141") for l in lines)


def test_age_report_flags_old_sections_only() -> None:
    rows = {sec: age for sec, _, age, _ in R.age_report(PLAN, dt.date(2026, 11, 25))}
    assert rows["days[0]"] == 108 and rows["booking_options.flights[0]"] == 108
    assert rows["entry_context"] == 5


def test_no_airports_no_search() -> None:
    plan = {"trip": {"start_date": "2027-02-12", "end_date": "2027-02-16"},
            "booking_options": {"flights": [card("X", "10:00", "20:15", 1)]}}
    cards, why = R.live_cards(plan, dt.date(2026, 11, 25), client=object())
    assert cards is None and "names no airports" in why
