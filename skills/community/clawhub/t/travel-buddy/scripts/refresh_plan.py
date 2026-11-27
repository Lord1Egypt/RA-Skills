#!/usr/bin/env python3
"""Before booking from a saved plan: what has gone stale, and have its flights changed.

Usage: python refresh_plan.py <plan.json> [--today YYYY-MM-DD] [--no-flights]

WHY THIS EXISTS
---------------
A plan is checked once and booked from weeks or months later. The Alicante plan was checked on
2026-08-09; by 2026-11-25 the airport-bus fare, the city-bus fare, one flight's departure time,
the hotel prices and the cheapest flight had all changed, and nothing in the skill re-asked.
`replan_trip.py` moves dates, party and budget; nothing re-checked a plan whose inputs had not
moved but whose world had.

WHAT IT DOES (no model, read-only)
----------------------------------
1. Lists every dated fact in the plan by section with how many days old it is.
2. Re-runs the plan's round trip on Kiwi.com and compares it with each flight card: still on sale
   at the same times and what it costs now, or no longer sold at those times and what that
   carrier sells instead; and the cheapest direct option now.
3. Prints the next steps: the place check, then the transport and booking_and_lodging verifiers
   in fresh processes on their slices, then the usual recheck save for whatever was edited.

The plan file is never written. Changes go in through the normal edit-and-recheck path, so the
page records what was rechecked and when.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STALE_DAYS = 30
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
CLOCK = re.compile(r"\b(\d{1,2}:\d{2})\b")
IATA = re.compile(r"\b([A-Z]{3})\b")


def dated_facts(node: object, path: str = "") -> list[tuple[str, str]]:
    """(pointer, date) for every *checked_at field in the plan."""
    out: list[tuple[str, str]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if key.endswith("checked_at") and isinstance(value, str) and DATE.match(value):
                out.append((here, value[:10]))
            elif key not in ("place_check", "verification_receipt", "_contract"):
                out.extend(dated_facts(value, here))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out.extend(dated_facts(value, f"{path}[{i}]"))
    return out


def section_of(pointer: str) -> str:
    m = re.match(r"(days\[\d+\]|booking_options\.\w+\[\d+\]|[a-z_]+)", pointer)
    return m.group(1) if m else pointer


def age_report(plan: dict, today: dt.date) -> list[tuple[str, str, int, int]]:
    """(section, oldest date, age in days, facts) per section, oldest first."""
    oldest: dict[str, str] = {}
    count: dict[str, int] = {}
    for pointer, date in dated_facts(plan):
        sec = section_of(pointer)
        count[sec] = count.get(sec, 0) + 1
        if sec not in oldest or date < oldest[sec]:
            oldest[sec] = date
    rows = [(sec, d, (today - dt.date.fromisoformat(d)).days, count[sec]) for sec, d in oldest.items()]
    return sorted(rows, key=lambda r: r[1])


def _clock(text: object) -> str | None:
    m = CLOCK.search(str(text or ""))
    return m.group(1).zfill(5) if m else None


def _carrier(card: dict) -> str:
    return re.split(r"[（(]", str(card.get("provider") or ""))[0].strip()


def flight_diff(plan: dict, cards_now: list[dict]) -> list[str]:
    """One line per plan flight card, plus the cheapest option on sale now."""
    lines = []
    currency = str(plan.get("trip", {}).get("currency") or "")
    for card in plan.get("booking_options", {}).get("flights") or []:
        out, ret = card.get("outbound_itinerary") or {}, card.get("return_itinerary") or {}
        want = (_clock(out.get("departure_local")), _clock(ret.get("departure_local")))
        carrier = _carrier(card)
        label = f"{card.get('id')} {carrier} {want[0]}/{want[1]}"
        same = [c for c in cards_now
                if (_clock(c["outbound_itinerary"]["departure_local"]),
                    _clock(c["return_itinerary"]["departure_local"])) == want]
        if same:
            now = min(c["fare_low"] for c in same)
            was = card.get("fare_low")
            delta = f" ({'+' if now >= was else ''}{now - was:g} since {card.get('price_checked_at') or card.get('checked_at')})" \
                if isinstance(was, (int, float)) else ""
            lines.append(f"FLIGHT {label}: still on sale, now {now:g} {currency} per person, plan says "
                         f"{was} {currency}{delta}")
            continue
        alt = [c for c in cards_now if carrier and _carrier(c).casefold() == carrier.casefold()] or \
              [c for c in cards_now if carrier and carrier.casefold() in _carrier(c).casefold()]
        alt_text = "; ".join(sorted({
            f"{_clock(c['outbound_itinerary']['departure_local'])}/{_clock(c['return_itinerary']['departure_local'])} "
            f"{c['fare_low']:g} {currency}" for c in alt})) or "no itinerary from this carrier at all"
        lines.append(f"FLIGHT {label}: NOT on sale at these times now. {carrier} now sells: {alt_text}")
    if cards_now:
        best = min(cards_now, key=lambda c: c["fare_low"])
        lines.append(f"CHEAPEST NOW: {_carrier(best)} {_clock(best['outbound_itinerary']['departure_local'])}/"
                     f"{_clock(best['return_itinerary']['departure_local'])} {best['fare_low']:g} {currency} per person "
                     f"(compare any 'cheapest option' claim in the plan's notes)")
    return lines


def live_cards(plan: dict, today: dt.date, client=None) -> tuple[list[dict] | None, str]:
    """Every usable round-trip itinerary for the plan's own flight, as flight cards."""
    import kiwi_flights as K  # noqa: PLC0415 - only when flights are refreshed
    trip = plan.get("trip") or {}
    flights = (plan.get("booking_options") or {}).get("flights") or []
    if not flights:
        return None, "no flight cards"
    card = flights[0]
    first = card.get("outbound_itinerary") or {}
    # Kiwi-made cards carry the codes as fields; hand-written ones lead their times with them
    # ("AMS 10:00（CET）"), and the zone after the time is not an airport.
    codes = [str(card.get("origin_airport") or ""), str(card.get("destination_airport") or "")]
    if not all(IATA.fullmatch(c) for c in codes):
        codes = [m.group(1) if (m := re.match(r"\s*([A-Z]{3})\b", str(first.get(k) or ""))) else ""
                 for k in ("departure_local", "arrival_local")]
    if not all(codes):
        return None, "the first flight card names no airports (origin_airport, or a code before its times)"
    start, end = str(trip.get("start_date") or "")[:10], str(trip.get("end_date") or "")[:10]
    if not (DATE.match(start) and DATE.match(end)):
        return None, "trip has no start_date/end_date"
    if dt.date.fromisoformat(start) < today:
        return None, "the trip has already started"
    request = {"origin": codes[0], "destination": codes[1], "depart": start, "return": end,
               "adults": int(trip.get("traveler_count") or 1), "children": 0, "infants": 0,
               "cabin": None, "currency": str(trip.get("currency") or "EUR").upper(),
               "language": "zh" if str(trip.get("language") or "").startswith("zh") else "en"}
    client = client or K.KiwiClient()
    try:
        payload = client.search(K.search_arguments(request))
        itineraries = K.usable_itineraries(payload, [])
    except K.KiwiUnavailable as exc:
        return None, f"Kiwi unavailable: {exc}"
    cards = [K.itinerary_to_card(it, request, n, today.isoformat(), single=False)
             for n, it in enumerate(itineraries)]
    return cards, f"{codes[0]}→{codes[1]} {start}/{end}, {len(cards)} itineraries on sale"


def main(argv: list[str] | None = None, client=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan")
    parser.add_argument("--today", help="treat this date as today (YYYY-MM-DD)")
    parser.add_argument("--no-flights", action="store_true", help="skip the live flight search")
    args = parser.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))

    rows = age_report(plan, today)
    stale = [r for r in rows if r[2] > STALE_DAYS]
    print(f"AGE: {len(rows)} sections carry dated facts; {len(stale)} were last checked more than "
          f"{STALE_DAYS} days ago")
    for sec, date, age, n in rows:
        mark = "STALE" if age > STALE_DAYS else "ok   "
        print(f"  {mark} {sec}: oldest of {n} fact(s) checked {date} ({age} days)")

    if not args.no_flights:
        cards, how = live_cards(plan, today, client)
        print(f"FLIGHTS: {how}")
        for line in flight_diff(plan, cards or []) if cards else []:
            print(line)

    stem = Path(args.plan)
    print("NEXT: python scripts/check_places.py " + str(stem) + " --into")
    for domain in ("transport", "booking_and_lodging"):
        print(f"NEXT: python scripts/plan_slice.py {stem} --domain {domain}   "
              f"(then one fresh verifier on that slice: every fare, time and price above)")
    print("NEXT: edit what changed, then save with the plan's report; the save names each edited "
          "section and new_verification_report.py --recheck writes the entries to fill "
          "(references/verification.md, rechecks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
