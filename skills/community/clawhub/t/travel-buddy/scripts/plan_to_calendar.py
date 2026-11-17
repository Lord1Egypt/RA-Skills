#!/usr/bin/env python3
"""The trip as calendar events, because a plan that stays on a laptop is a plan nobody consults.

Usage: python plan_to_calendar.py --from-plan <plan.json> [--out <trip.ics>]

WHY THIS EXISTS. The delivered artifact is a self-contained HTML file averaging 331 KB, and the
traveller reads it standing in a city they do not know, on a phone. Nothing carried it there. Every
gate in this skill is about the page being TRUE; none of them is about the page being WHERE THE
TRAVELLER IS. A calendar is the one channel that already solves that: the file lands in the
traveller's own calendar account and their phone syncs it, with no server, no link, and no account
of ours.

It also carries the two things a page cannot: a reminder that fires, and a time the traveller has
to be somewhere. "Only 24 seats, call ahead" is a sentence on a page; it is an alarm in a calendar.

UTC FROM THE PLAN'S OWN ZONES. Only Apple Calendar shows a floating (zone-less) time as written:
Outlook converts it to the phone's zone at import ([MS-STANOICAL]) and Google Calendar does not
support it, so a Tokyo dinner imported at home in Amsterdam showed at the Amsterdam hour. Where
scripts/trip_zones.py resolves an event's zone it is written in UTC, which every client converts to
the phone's zone, and the description states the local time and zone. Where it cannot (a plan saved
before zones existed) the event is floating as before, and the summary says so.

ONLY WHAT THE TRAVELLER DECIDED. A flight, rail leg or rental car enters once scripts/bookings.py
records it as chosen or booked; the undecided groups are counted, never exported as candidates.

WHAT IT DOES NOT DO. It invents nothing. An event exists only where the plan already carries a
time: flight and rail itineraries, dining windows, timed activities, accommodation windows, and a
ticket whose sale opens at a stated moment. A day with no times contributes one all-day entry with
its own title, and nothing else.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookings  # noqa: E402 - which option the traveller decided
import trip_zones as tz  # noqa: E402 - which zone each event happens in

PRODID = "-//travel-buddy//trip plan//EN"


def _obj(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def _seq(value: object) -> list:
    return value if isinstance(value, list) else []


def _text(value: object) -> str:
    """One TEXT value, escaped per RFC 5545 §3.3.11.

    Backslash first, or escaping a comma would then have its own backslash escaped again.
    """
    s = str(value or "")
    s = s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,")
    return s.replace("\r\n", "\\n").replace("\n", "\\n").replace("\r", "\\n")


def fold(line: str) -> str:
    """Fold to 75 OCTETS per RFC 5545 §3.1, without splitting a UTF-8 character.

    Counting characters instead of octets is the trap this skill has hit before in another form:
    a rule tuned on Latin text, applied to a document that is mostly Chinese. A split multi-byte
    sequence does not merely look wrong -- it makes the file unparseable, and a calendar that
    refuses to open is worse than no calendar.
    """
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    out, chunk, limit = [], bytearray(), 75
    for char in line:
        encoded = char.encode("utf-8")
        if len(chunk) + len(encoded) > limit:
            out.append(chunk.decode("utf-8"))
            chunk = bytearray()
            limit = 74            # continuation lines carry a leading space
        chunk += encoded
    out.append(chunk.decode("utf-8"))
    return "\r\n ".join(out)


def _stamp(value: object) -> str | None:
    """'2027-05-07 09:45' or '2027-05-07T09:45' → '20270507T094500'. Anything else → None."""
    text = str(value or "").strip().replace("T", " ")
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})[ ]?(\d{2}):(\d{2})", text)
    if not match:
        return None
    return "{}{}{}T{}{}00".format(*match.groups())


def _plus_minutes(stamp: str, minutes: float) -> str:
    """A floating-time stamp moved forward by a duration."""
    moment = dt.datetime.strptime(stamp, "%Y%m%dT%H%M%S") + dt.timedelta(minutes=minutes)
    return moment.strftime("%Y%m%dT%H%M%S")


WORDS = {
    "en": {"local": "Local time: ", "booked": "Booked via {via} on {on}", "chosen": "Chosen — not booked yet",
           "pickup": "Pick up car — {provider}", "dropoff": "Return car — {provider}"},
    "zh": {"local": "当地时间：", "booked": "已订：{via}，{on}", "chosen": "已选，尚未预订",
           "pickup": "取车 — {provider}", "dropoff": "还车 — {provider}"},
}
TRANSPORT_KINDS = ("flights", "ground_transport", "rental_cars")
_MERIDIEM = re.compile(r"\s*(a\.?m\.?|p\.?m\.?)(?![a-z])", re.IGNORECASE)
_CLOCK_SPAN = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*(?:[–—\-~至]\s*(\d{1,2}):(\d{2}))?")


def _utc(moment: dt.datetime) -> str:
    return moment.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _floating(moment: dt.datetime) -> str:
    return moment.strftime("%Y%m%dT%H%M%S")


def _on(day_date: object, hour: str, minute: str) -> dt.datetime | None:
    date = _date(day_date)
    try:
        return dt.datetime.strptime(f"{date}{int(hour):02d}{minute}", "%Y%m%d%H%M") if date else None
    except ValueError:
        return None


def _clock_span(day_date: object, text: object, *, whole: bool = True) -> tuple[dt.datetime, dt.datetime] | None:
    """'9:30', '09:30' or '09:30–11:00' on the day's date; an end not after the start is the start.

    A meal's window may trail words ("19:00–20:30, early sitting"), as it always could (whole=False);
    an activity's time must be only a time or a range, or it is reported as not understood.
    """
    raw = str(text or "")
    match = _CLOCK_SPAN.match(raw)
    if not match or (whole and raw[match.end():].strip()) or _MERIDIEM.match(raw[match.end():]):
        return None  # "7:00 PM" read as 07:00 would be a confident lie, with a reminder on it
    start = _on(day_date, match.group(1), match.group(2))
    end = _on(day_date, match.group(3), match.group(4)) if match.group(3) else None
    if start is None:
        return None
    return start, end if end is not None and end > start else start


def _aware(value: object) -> dt.datetime | None:
    """An ISO date-time that carries its own offset ('…+09:00', '…Z'), else None."""
    text = str(value or "").strip()
    if not re.search(r"(Z|[+-]\d{2}:?\d{2})$", text):
        return None
    try:
        moment = dt.datetime.fromisoformat(text[:-1] + "+00:00" if text.endswith("Z") else text)
    except ValueError:
        return None
    return moment if moment.tzinfo is not None else None


def _booking_line(record: dict, words: dict) -> str:
    if record.get("state") == "booked":
        return words["booked"].format(via=record.get("booked_via") or "?", on=record.get("booked_on") or "?")
    return words["chosen"]


_NO_BOOKING = re.compile(
    r"(无需|不需|不用|不接受|不可|不能)\s*(提前)?\s*(预订|订位|预约)"
    r"|\bno (booking|reservation)s?\b|\bno need to book\b|walk-?ins? only"
    r"|\b(booking|reservation)s? (are |is )?(not|aren't|isn't) (required|needed|accepted|taken)\b",
    re.IGNORECASE)  # negation tied to the booking noun: "walk-ins not accepted" is a must-book note
_BOOKING = re.compile(r"订位|预订|预约|致电|提前订|\bbook(ing|ed)?\b|reserv|call ahead|phone ahead", re.IGNORECASE)


def _date(value: object) -> str | None:
    match = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(value or "").strip())
    return "".join(match.groups()) if match else None


def _window(day_date: object, window: object) -> tuple[str, str] | None:
    """A dining card's '19:00–20:30' against its day's date. En dash or hyphen, both seen."""
    date = _date(day_date)
    match = re.match(r"^\s*(\d{1,2}):(\d{2})\s*[–—\-~至]\s*(\d{1,2}):(\d{2})",
                     str(window or ""))
    if not date or not match:
        return None
    h1, m1, h2, m2 = match.groups()
    start = f"{date}T{int(h1):02d}{m1}00"
    end = f"{date}T{int(h2):02d}{m2}00"
    return (start, end) if end > start else (start, start)


def event(uid_seed: str, summary: str, start: str, end: str | None, *,
          description: str = "", location: str = "", all_day: bool = False,
          alarm_minutes: int | None = None, stamp: str) -> list[str]:
    uid = hashlib.sha256(uid_seed.encode("utf-8")).hexdigest()[:20] + "@travel-buddy"
    lines = ["BEGIN:VEVENT", f"UID:{uid}", f"DTSTAMP:{stamp}"]
    if all_day:
        lines.append(f"DTSTART;VALUE=DATE:{start}")
        if end:
            lines.append(f"DTEND;VALUE=DATE:{end}")
    else:
        lines.append(f"DTSTART:{start}")
        lines.append(f"DTEND:{end or start}")
    lines.append(f"SUMMARY:{_text(summary)}")
    if description:
        lines.append(f"DESCRIPTION:{_text(description)}")
    if location:
        lines.append(f"LOCATION:{_text(location)}")
    if alarm_minutes is not None:
        # A reminder is the one thing a page cannot do. "Only 24 seats, call ahead" is a sentence
        # on paper and an alarm here.
        lines += ["BEGIN:VALARM", "ACTION:DISPLAY",
                  f"TRIGGER:-PT{alarm_minutes}M",
                  f"DESCRIPTION:{_text(summary)}", "END:VALARM"]
    lines.append("END:VEVENT")
    return lines


def _needs_booking(note: object) -> bool:
    """Does this card's note say the traveller has to do something in advance? Negation first:
    "Reservations not accepted" names a reservation and needs none."""
    text = str(note or "")
    return not _NO_BOOKING.search(text) and bool(_BOOKING.search(text))


def _meal_alarm(card: dict) -> int | None:
    need = card.get("reservation_need")
    if need in ("required", "recommended"):
        return 1440
    if need in ("walk_in", "not_accepted"):
        return None
    return 1440 if _needs_booking(card.get("reservation_or_queue_note")) else None


def _dtstamp(plan: dict) -> str:
    """DTSTAMP, derived from the plan rather than from the clock.

    RFC 5545 wants the moment the iCalendar object was created, and `datetime.now()` is the
    obvious reading of that. It is also what made the delivered page IRREPRODUCIBLE: the calendar
    is embedded in the HTML as a base64 `data:` URI, so rendering the same plan twice one second
    apart produced two different pages. That surfaced as an intermittent ~20% failure in
    tests/test_plan_imagery.py's "the pages are byte-identical" case -- a test that is right, about
    a defect in here rather than in imagery, and whose flakiness was the only thing reporting it.

    `generated_at` is the honest answer anyway: the calendar is created from the plan, so the
    plan's own research timestamp is when its contents came into being, and a re-render is not a
    new creation. The clock stays as the fallback for a plan that carries no usable timestamp,
    which keeps the property a bonus rather than a new way to fail.
    """
    raw = str(plan.get("generated_at") or "").strip()
    if raw:
        try:
            parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            parsed = None
        if parsed is not None:
            if parsed.tzinfo is None:            # a naive stamp is read as UTC, not as local
                parsed = parsed.replace(tzinfo=dt.timezone.utc)
            return parsed.astimezone(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def build_with_summary(plan: dict) -> tuple[str, dict[str, int], dict]:
    trip = _obj(plan.get("trip"))
    stamp = _dtstamp(plan)
    words = WORDS["zh" if str(trip.get("language") or "").lower().startswith("zh") else "en"]
    title = str(trip.get("title") or trip.get("destination") or "Trip")
    body: list[str] = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:{PRODID}",
                       "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
                       f"X-WR-CALNAME:{_text(title)}"]
    counts = {"flight": 0, "rail": 0, "car": 0, "stay": 0, "meal": 0, "activity": 0, "ticket": 0, "day": 0}
    unparsed: list[str] = []
    floating = False

    def timed(moment: dt.datetime, zone_name: str | None) -> str:
        nonlocal floating
        if zone_name:
            return _utc(tz.to_utc(moment, zone_name))
        floating = True
        return _floating(moment)

    def local_line(text: str, zone_name: str | None) -> str:
        return f"{words['local']}{text} {zone_name}" if zone_name else ""

    index = bookings.option_index(plan)
    decided = {oid: r for oid, r in bookings.record_by_option(plan).items()
               if r.get("state") in bookings.RECORD_STATES and oid in index}
    decided_groups = {bookings.group_key(*index[oid]) for oid in decided}
    undecided = sorted({bookings.group_key(kind, option) for kind, option in index.values()
                        if kind in TRANSPORT_KINDS} - decided_groups)

    booking = _obj(plan.get("booking_options"))
    for kind, key in (("flight", "flights"), ("rail", "ground_transport")):
        for number, item in enumerate(_seq(booking.get(key))):
            item = _obj(item)
            record = decided.get(str(item.get("id") or ""))
            if record is None:
                continue
            for leg, date_key in tz.LEGS:
                itin = _obj(item.get(leg))
                start_local, _ = tz.local_moment(itin.get("departure_local"), item.get(date_key))
                if start_local is None:
                    continue
                duration = itin.get("duration_minutes")
                has_duration = isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration > 0
                span = tz.itinerary_span(plan, item, leg, date_key)
                if span is not None:
                    start_utc, end_utc = span
                    if end_utc is None or end_utc < start_utc:
                        end_utc = start_utc + dt.timedelta(minutes=duration) if has_duration else start_utc
                    departure_zone, arrival_zone = tz.itinerary_zones(plan, itin)
                    start, end = _utc(start_utc), _utc(end_utc)
                    arrives = end_utc.astimezone(tz.zone(arrival_zone)).strftime("%H:%M")
                    local = f"{words['local']}{start_local:%H:%M} {departure_zone} → {arrives} {arrival_zone}"
                else:
                    # Floating, as before zones existed -- including the date-line patch: RFC 5545
                    # forbids DTEND before DTSTART, so start + duration gives the right length.
                    floating = True
                    start = _floating(start_local)
                    end_local, _ = tz.local_moment(itin.get("arrival_local"), start_local.date().isoformat())
                    end = _floating(end_local) if end_local else start
                    if end < start:
                        end = _plus_minutes(start, duration) if has_duration else start
                    local = ""
                service = str(itin.get("service_identifier") or "")
                where = " → ".join(x for x in (item.get("origin_airport") or item.get("origin_station"),
                                               item.get("destination_airport") or item.get("destination_station"))
                                   if x)
                if leg == "return_itinerary":
                    # NOT the outbound pair reversed: on an open-jaw trip the return's real airports
                    # are in no structured field, only in connection_or_terminal_note. Reversing
                    # produced "KL1924 GVA → AMS" for a flight that leaves ZURICH.
                    where = ""
                description = "\n".join(x for x in (local, _booking_line(record, words),
                                                    str(itin.get("connection_or_terminal_note") or "")) if x)
                body += event(f"{kind}{number}{leg}{start}", f"{service} {where}".strip(),
                              start, end, location=where, description=description,
                              alarm_minutes=180 if kind == "flight" else 45, stamp=stamp)
                counts[kind] += 1

    for number, car in enumerate(_seq(booking.get("rental_cars"))):
        car = _obj(car)
        record = decided.get(str(car.get("id") or ""))
        if record is None:
            continue
        provider = str(car.get("provider") or car.get("direct_provider") or "")
        for which, time_key, place_key in (("pickup", "pickup_time", "pickup_location"),
                                           ("dropoff", "dropoff_time", "dropoff_location")):
            moment, _ = tz.local_moment(car.get(time_key), None)
            if moment is None:
                if car.get(time_key):
                    unparsed.append(f"{provider or 'rental car'} {time_key} ({car.get(time_key)})")
                continue
            zone_name = tz.zone_on(plan, moment.date())
            start = timed(moment, zone_name)
            description = "\n".join(x for x in (local_line(f"{moment:%H:%M}", zone_name), _booking_line(record, words)) if x)
            body += event(f"car{number}{which}{start}", words[which].format(provider=provider).rstrip(" —"),
                          start, start, location=str(car.get(place_key) or ""), description=description,
                          alarm_minutes=60, stamp=stamp)
            counts["car"] += 1

    stays = {str(_obj(a).get("id")): _obj(a) for a in _seq(booking.get("accommodations"))}
    used: set[str] = set()
    for day in _seq(plan.get("days")):
        chosen = str(_obj(day).get("accommodation_option_id") or "")
        if chosen and chosen in stays and chosen not in used:
            used.add(chosen)
            stay = stays[chosen]
            start, end = _date(stay.get("check_in")), _date(stay.get("check_out"))
            if start and end:
                body += event(f"stay{chosen}", str(stay.get("property_name") or "Accommodation"),
                              start, end, all_day=True,
                              location=str(stay.get("address_or_location_reference") or ""),
                              description=str(stay.get("cancellation_terms") or ""), stamp=stamp)
                counts["stay"] += 1

    for day in _seq(plan.get("days")):
        day = _obj(day)
        date = _date(day.get("date"))
        if not date:
            continue
        zone_name = tz.day_zone(plan, day)
        body += event(f"day{date}", str(day.get("title") or f"Day {day.get('number')}"),
                      date, None, all_day=True,
                      description=str(day.get("focus") or ""),
                      location=str(day.get("base_location") or ""), stamp=stamp)
        counts["day"] += 1
        for number, card in enumerate(_seq(day.get("dining"))):
            card = _obj(card)
            span = _clock_span(day.get("date"), card.get("time_window"), whole=False)
            if not span:
                if str(card.get("time_window") or "").strip():
                    unparsed.append(f"day {day.get('number')}: {card.get('venue_name') or 'meal'} ({card.get('time_window')})")
                continue
            note = str(card.get("reservation_or_queue_note") or "")
            local = local_line(f"{span[0]:%H:%M}–{span[1]:%H:%M}", zone_name)
            body += event(f"meal{date}{number}", str(card.get("venue_name") or "Meal"),
                          timed(span[0], zone_name), timed(span[1], zone_name),
                          location=str(card.get("neighborhood") or ""),
                          description="\n".join(x for x in (local, note) if x),
                          alarm_minutes=_meal_alarm(card), stamp=stamp)
            counts["meal"] += 1
        for number, act in enumerate(_seq(day.get("activities"))):
            act = _obj(act)
            raw = str(act.get("time") or "").strip()
            if not raw:
                continue
            span = _clock_span(day.get("date"), raw)
            if span is None:
                unparsed.append(f"day {day.get('number')}: {act.get('name') or 'activity'} ({raw})")
                continue
            local = local_line(f"{span[0]:%H:%M}" + (f"–{span[1]:%H:%M}" if span[1] > span[0] else ""), zone_name)
            body += event(f"act{date}{number}", str(act.get("name") or "Activity"),
                          timed(span[0], zone_name), timed(span[1], zone_name),
                          description="\n".join(x for x in (local, str(act.get("detail") or "")) if x), stamp=stamp)
            counts["activity"] += 1

    days_by_number = {_obj(d).get("number"): _obj(d) for d in _seq(plan.get("days"))}
    for number, ticket in enumerate(_seq(booking.get("attraction_tickets"))):
        ticket = _obj(ticket)
        if decided.get(str(ticket.get("id") or ""), {}).get("state") == "booked":
            continue  # bought: a "tickets on sale" alarm would send the traveller to buy it again
        sale = _obj(ticket.get("sale_opens_at"))
        opens = sale.get("opens_at") if str(sale.get("status")) == "scheduled_release" else None
        aware = _aware(opens)
        if aware is not None:
            start = _utc(aware)  # the value states its own offset: that instant, whatever the day's zone
        else:
            moment, _ = tz.local_moment(opens, None)
            if moment is None:
                continue
            day = days_by_number.get(ticket.get("day_number"))
            zone_name = tz.day_zone(plan, day) if day else tz.zone_on(plan, moment.date())
            start = timed(moment, zone_name)
        body += event(f"ticket{number}{start}",
                      f"{ticket.get('attraction_name')} — tickets on sale",
                      start, start, description=str(sale.get("basis") or ""),
                      alarm_minutes=60, stamp=stamp)
        counts["ticket"] += 1

    body.append("END:VCALENDAR")
    summary = {"undecided": undecided, "unparsed": unparsed, "floating": floating}
    return "\r\n".join(fold(line) for line in body) + "\r\n", counts, summary


def build(plan: dict) -> tuple[str, dict[str, int]]:
    text, counts, _ = build_with_summary(plan)
    return text, counts


def summary_notes(summary: dict) -> list[str]:
    """What the terminal should say about a calendar, in the order worth reading."""
    notes = []
    if summary.get("undecided"):
        notes.append(f"{len(summary['undecided'])} transport group(s) have no recorded choice and are not in the "
                     f"calendar ({', '.join(summary['undecided'])}); record one with scripts/record_booking.py "
                     f"and save again.")
    if summary.get("floating"):
        notes.append("calendar times are floating (the plan names no time zones): Apple Calendar shows them as "
                     "written, Google Calendar and Outlook shift them to the phone's zone. Add trip.timezone and "
                     "trip.origin_timezone.")
    if summary.get("unparsed"):
        notes.append("these times were not understood and are not in the calendar: " + "; ".join(summary["unparsed"]))
    return notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--from-plan", required=True)
    parser.add_argument("--out", default="-")
    args = parser.parse_args()
    try:
        plan = json.loads(Path(args.from_plan).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not read {args.from_plan}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("ERROR: the plan must be a JSON object.", file=sys.stderr)
        return 2
    body, counts, summary = build_with_summary(plan)
    if args.out == "-":
        sys.stdout.write(body)
    else:
        Path(args.out).write_bytes(body.encode("utf-8"))
        print(f"Calendar: {args.out}")
    print("  " + ", ".join(f"{n} {k}" for k, n in counts.items() if n), file=sys.stderr)
    for note in summary_notes(summary) or ["Times are written in UTC from the plan's own zones, so every calendar "
                                           "app shows them at the right local hour."]:
        print(f"  {note}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
