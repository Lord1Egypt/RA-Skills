#!/usr/bin/env python3
"""Which time zone each timed thing in a plan happens in, as rules the gate and the calendar share.

The calendar file is read by Google Calendar and Outlook as well as Apple Calendar, and only Apple
shows a floating (zone-less) time as written: Outlook converts it to the phone's zone at import
([MS-STANOICAL]) and Google does not support it, so a Tokyo dinner imported at home in Amsterdam
showed at the Amsterdam hour once the phone was in Tokyo. A plan therefore names its zones --
trip.timezone and trip.origin_timezone, days[].timezone where a trip crosses zones, an itinerary's
departure_timezone / arrival_timezone -- and plan_to_calendar.py writes UTC from them.

An itinerary end takes a default only when the plan names one zone throughout. "The outbound
leaves from home" would be a guess: a ground option's outbound_itinerary is also how a one-way leg
INSIDE the trip is written (Edinburgh -> Inverness). Zones are checked by arithmetic wherever a
duration exists: departure + duration_minutes must land on the stated arrival in the arrival zone,
so a zone off by whole hours is caught instead of trusted.

[MS-STANOICAL]: https://learn.microsoft.com/en-us/openspecs/exchange_standards/ms-stanoical/72ce09ef-bad3-43c4-8f59-ed5e93b82887
"""

from __future__ import annotations

import datetime as dt
import functools
import re
import zoneinfo

ITINERARY_KINDS = ("flights", "ground_transport")
LEGS = (("outbound_itinerary", "outbound_date"), ("return_itinerary", "return_date"))
ZONE_KEYS = ("departure_timezone", "arrival_timezone")
DURATION_TOLERANCE_MINUTES = 30
_STAMP = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})[ T](\d{1,2}):(\d{2})")
_CLOCK = re.compile(r"^\s*(\d{1,2}):(\d{2})\s*$")


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def _placeholder(value: object) -> bool:
    return _text(value).upper().startswith("TODO")


def _filled(value: object) -> bool:
    return bool(_text(value)) and not _placeholder(value)


def _number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _trip(plan: dict) -> dict:
    return plan.get("trip") if isinstance(plan.get("trip"), dict) else {}


def _days(plan: dict) -> list[dict]:
    days = plan.get("days")
    return [d for d in days if isinstance(d, dict)] if isinstance(days, list) else []


@functools.lru_cache(maxsize=1)
def _known() -> frozenset[str]:
    try:
        return frozenset(zoneinfo.available_timezones())
    except Exception:  # noqa: BLE001 - no tz database is a state the callers report, not a crash
        return frozenset()


def database_available() -> bool:
    return bool(_known())


def zone(name: object) -> zoneinfo.ZoneInfo | None:
    """The zone for an IANA name this machine's tz database lists, else None (never a path)."""
    text = _text(name)
    return zoneinfo.ZoneInfo(text) if text and text in _known() else None


def local_moment(value: object, fallback_date: object) -> tuple[dt.datetime | None, bool]:
    """'2026-11-20 21:55' (dated), or '08:00' on `fallback_date` (not dated). Else (None, False)."""
    text = _text(value)
    match = _STAMP.match(text)
    if match:
        year, month, day, hour, minute = map(int, match.groups())
        try:
            return dt.datetime(year, month, day, hour, minute), True
        except ValueError:
            return None, True
    match = _CLOCK.match(text)
    if match and _text(fallback_date):
        try:
            day = dt.date.fromisoformat(_text(fallback_date)[:10])
            return dt.datetime.combine(day, dt.time(int(match.group(1)), int(match.group(2)))), False
        except ValueError:
            return None, False
    return None, False


def to_utc(moment: dt.datetime, name: str) -> dt.datetime:
    return moment.replace(tzinfo=zone(name)).astimezone(dt.timezone.utc)


def plan_zone_names(plan: dict) -> set[str]:
    trip = _trip(plan)
    names = {_text(trip.get(key)) for key in ("timezone", "origin_timezone") if _filled(trip.get(key))}
    return names | {_text(day.get("timezone")) for day in _days(plan) if _filled(day.get("timezone"))}


def _one_zone(plan: dict) -> bool:
    trip = _trip(plan)
    return _filled(trip.get("timezone")) and _filled(trip.get("origin_timezone")) and len(plan_zone_names(plan)) == 1


def single_zone(plan: dict) -> str | None:
    if not _one_zone(plan):
        return None
    name = next(iter(plan_zone_names(plan)))
    return name if zone(name) else None


def day_zone(plan: dict, day: dict) -> str | None:
    name = _text(day.get("timezone")) or _text(_trip(plan).get("timezone"))
    return name if zone(name) else None


def zone_on(plan: dict, date: dt.date) -> str | None:
    for day in _days(plan):
        if _text(day.get("date"))[:10] == date.isoformat():
            return day_zone(plan, day)
    name = _text(_trip(plan).get("timezone"))
    return name if zone(name) else None


def itinerary_zones(plan: dict, itin: dict) -> tuple[str | None, str | None]:
    single = single_zone(plan)
    departure = _text(itin.get("departure_timezone")) or single or ""
    arrival = _text(itin.get("arrival_timezone")) or single or ""
    return (departure if zone(departure) else None, arrival if zone(arrival) else None)


def itinerary_span(plan: dict, option: dict, leg: str, date_key: str) -> tuple[dt.datetime, dt.datetime | None] | None:
    """(start, end) in UTC for an itinerary whose zones resolve, else None.

    A dated arrival is taken as written. A clock-only arrival is put on the first day, from the
    departure date on, that lands it after the start -- a sleeper's 07:05 is the next morning.
    """
    itin = option.get(leg) if isinstance(option.get(leg), dict) else {}
    start, _ = local_moment(itin.get("departure_local"), option.get(date_key))
    departure, arrival = itinerary_zones(plan, itin)
    if start is None or departure is None or arrival is None:
        return None
    start_utc = to_utc(start, departure)
    end, dated = local_moment(itin.get("arrival_local"), start.date().isoformat())
    if end is None:
        return start_utc, None
    end_utc = to_utc(end, arrival)
    if not dated:
        for _ in range(2):
            if end_utc > start_utc:
                break
            end += dt.timedelta(days=1)
            end_utc = to_utc(end, arrival)
    return start_utc, end_utc


def itineraries(plan: dict):
    """(kind, index, leg, date_key, option, itinerary) for every itinerary that states a departure."""
    options = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    for kind in ITINERARY_KINDS:
        for index, option in enumerate(options.get(kind) or []):
            if not isinstance(option, dict):
                continue
            for leg, date_key in LEGS:
                itin = option.get(leg)
                if isinstance(itin, dict) and _filled(itin.get("departure_local")):
                    yield kind, index, leg, date_key, option, itin


def named_zones(plan: dict) -> list[tuple[str, object]]:
    found: list[tuple[str, object]] = []
    trip = _trip(plan)
    for key in ("timezone", "origin_timezone"):
        if trip.get(key) is not None:
            found.append((f"trip.{key}", trip[key]))
    for index, day in enumerate(plan.get("days") if isinstance(plan.get("days"), list) else []):
        if isinstance(day, dict) and day.get("timezone") is not None:
            found.append((f"days[{index}].timezone", day["timezone"]))
    options = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    for kind in ITINERARY_KINDS:
        for index, option in enumerate(options.get(kind) or []):
            for leg, _ in LEGS:
                itin = option.get(leg) if isinstance(option, dict) else None
                for key in ZONE_KEYS:
                    if isinstance(itin, dict) and itin.get(key) is not None:
                        found.append((f"booking_options.{kind}[{index}].{leg}.{key}", itin[key]))
    return found


def _duration_problem(plan: dict, where: str, option: dict, leg: str, date_key: str) -> str | None:
    itin = option[leg]
    minutes = itin.get("duration_minutes")
    if not _number(minutes) or minutes <= 0:
        return None
    span = itinerary_span(plan, option, leg, date_key)
    if span is None or span[1] is None:
        return None
    apart = (span[1] - span[0]).total_seconds() / 60
    if abs(apart - minutes) <= DURATION_TOLERANCE_MINUTES:
        return None
    departure, arrival = itinerary_zones(plan, itin)
    return (f"{where}: departs {_text(itin.get('departure_local'))} {departure} and arrives "
            f"{_text(itin.get('arrival_local'))} {arrival}, which is {apart:.0f} minutes, but "
            f"duration_minutes is {minutes:g}. A time zone off by whole hours is the usual cause: "
            f"check both ends' zones, then the duration.")


def zone_problems(plan: dict) -> list[str]:
    """Every zone that is not a zone, every leg that cannot be placed, every zone a duration refutes."""
    problems: list[str] = []
    known = database_available()
    placeholders = [path for path, value in named_zones(plan) if _placeholder(value)]
    if placeholders:
        # Refused here because nothing else can: the page never prints a zone, so the HTML gate's
        # TODO scan does not see it, and a plan saved with one gets a floating calendar.
        problems.append(f"{', '.join(placeholders)} still hold a TODO placeholder: write each IANA time "
                        f"zone (Europe/London, Asia/Tokyo).")
    for path, value in named_zones(plan):
        if _placeholder(value):
            continue
        if not _text(value):
            problems.append(f"{path} must be an IANA time zone name such as Europe/London, or null.")
        elif known and zone(value) is None:
            problems.append(f"{path} {value!r} is not an IANA time zone name (Europe/London, "
                            f"Asia/Tokyo, America/New_York). A UTC offset cannot follow daylight saving.")
    if not known:
        return problems
    opted_in = _filled(_trip(plan).get("timezone"))
    one_zone = _one_zone(plan)
    for kind, index, leg, date_key, option, itin in itineraries(plan):
        where = f"booking_options.{kind}[{index}].{leg}"
        missing = [key for key in ZONE_KEYS if not _text(itin.get(key))]
        if opted_in and not one_zone and missing:
            label = _text(itin.get("service_identifier")) or _text(option.get("id")) or "this leg"
            names = ", ".join(sorted(plan_zone_names(plan)))
            if not _filled(_trip(plan).get("origin_timezone")):
                names += "; trip.origin_timezone is not set, so where the traveller leaves from is unknown"
            problems.append(
                f"{where} ({label}) needs {' and '.join(missing)}: this plan names more than one time "
                f"zone ({names}), or cannot tell, so neither end of a "
                f"leg can be assumed -- a one-way leg inside the trip is written the same way as the "
                f"flight from home. Write each end's IANA zone.")
            continue
        problem = _duration_problem(plan, where, option, leg, date_key)
        if problem:
            problems.append(problem)
    return problems


def zone_notes(plan: dict) -> list[str]:
    if database_available() or not any(_filled(value) for _, value in named_zones(plan)):
        return []
    return ["this machine has no time-zone database (Python's zoneinfo lists none; on Windows "
            "`pip install tzdata`), so the plan's time zones were not checked and its calendar is "
            "written in floating time."]
