#!/usr/bin/env python3
"""Which option the traveller chose or booked, as rules every other script asks.

A plan was "booking-ready" and then stopped: nothing recorded a decision, so the page kept offering
both candidates and the calendar exported both. The plan's top-level `bookings` list now records
one decision per group -- `chosen` (decided, not paid) or `booked` (paid and confirmed, with the
date, where, and optionally what was paid). Never a booking reference, a document or a payment
detail. The block is outside verification's fingerprints (verification_sections.META_KEYS): a
decision is the traveller's fact, not research, and recording it must not re-open a verification.

Groups come from fields plans already carry: flights and ground transport by leg_group_id,
accommodations by stay_group_id, all rental cars as one group, each attraction ticket alone.
"""

from __future__ import annotations

import datetime as dt
import re
from urllib.parse import unquote_plus

RECORD_STATES = ("chosen", "booked")
# Blocks where naming a hotel the traveller did not take is not an instruction to go there: the
# option cards themselves, the records, the evidence cited, the replan log, and what the traveller
# typed. Everything else -- days, arrival notes, the overview -- tells the traveller where to go.
NOT_DIRECTIONS = frozenset({"booking_options", "bookings", "sources", "replan_context", "intake_context",
                            "profile_context", "ui_labels", "_contract", "_enums"})
BOOKING_KINDS = ("flights", "ground_transport", "accommodations", "attraction_tickets", "rental_cars")


def _text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def group_key(kind: str, option: dict) -> str:
    if kind in ("flights", "ground_transport"):
        return f"{kind}:{_text(option.get('leg_group_id'))}"
    if kind == "accommodations":
        return f"accommodations:{_text(option.get('stay_group_id'))}"
    if kind == "rental_cars":
        return "rental_cars"
    return f"{kind}:{_text(option.get('id'))}"


def option_index(plan: dict) -> dict[str, tuple[str, dict]]:
    index: dict[str, tuple[str, dict]] = {}
    options = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    for kind in BOOKING_KINDS:
        for option in options.get(kind) or []:
            if isinstance(option, dict) and _text(option.get("id")):
                index[_text(option["id"])] = (kind, option)
    return index


def records(plan: dict) -> list[dict]:
    value = plan.get("bookings")
    return [r for r in value if isinstance(r, dict)] if isinstance(value, list) else []


def record_by_option(plan: dict) -> dict[str, dict]:
    return {_text(r.get("option_id")): r for r in records(plan) if _text(r.get("option_id"))}


def stay_days(plan: dict, group: str) -> list[int]:
    index = option_index(plan)
    numbers = []
    for day in plan.get("days") or []:
        if not isinstance(day, dict):
            continue
        found = index.get(_text(day.get("accommodation_option_id")))
        if found and found[0] == "accommodations" and group_key("accommodations", found[1]) == group:
            numbers.append(day.get("number"))
    return numbers


def record_problems(plan: dict, today: dt.date) -> list[str]:
    """Everything wrong with the bookings block, as sentences naming the record."""
    problems: list[str] = []
    raw = plan.get("bookings")
    if raw is not None and not isinstance(raw, list):
        return ["bookings must be a list of records."]
    index = option_index(plan)
    seen_groups: dict[str, str] = {}
    for position, record in enumerate(raw or []):
        if not isinstance(record, dict):
            problems.append(f"bookings[{position}] is not an object.")
            continue
        option_id = _text(record.get("option_id"))
        where = f"booking record for {option_id or f'bookings[{position}]'}"
        if option_id not in index:
            problems.append(f"{where}: option_id {option_id!r} names no option in booking_options -- "
                            f"the card was removed or renamed; clear the record or restore the card.")
            continue
        kind, option = index[option_id]
        state = record.get("state")
        if state not in RECORD_STATES:
            problems.append(f"{where}: state {state!r} must be one of {', '.join(RECORD_STATES)}.")
        if state == "booked":
            booked_on = _text(record.get("booked_on"))
            try:
                when = dt.date.fromisoformat(booked_on) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", booked_on) else None
            except ValueError:
                when = None
            if when is None:
                problems.append(f"{where}: booked_on must be the booking date as YYYY-MM-DD.")
            elif when > today:
                problems.append(f"{where}: booked_on {booked_on} is after today ({today}).")
            if not _text(record.get("booked_via")):
                problems.append(f"{where}: booked_via must say where it was booked.")
        has_total = record.get("paid_total") is not None
        has_currency = record.get("paid_currency") is not None
        if (has_total or has_currency) and state == "chosen":
            problems.append(f"{where}: a chosen record carries no payment; record it as booked once paid.")
        elif has_total or has_currency:
            total = record.get("paid_total")
            if not isinstance(total, (int, float)) or isinstance(total, bool) or total < 0:
                problems.append(f"{where}: paid_total must be a number of zero or more.")
            currency = record.get("paid_currency")
            if not (isinstance(currency, str) and re.fullmatch(r"[A-Z]{3}", currency)):
                problems.append(f"{where}: paid_currency must be a three-letter upper-case code and "
                                f"come with paid_total.")
        group = group_key(kind, option)
        if group in seen_groups:
            problems.append(f"{where}: {seen_groups[group]} is already recorded in the same group "
                            f"({group}); one decision per group.")
        seen_groups.setdefault(group, option_id)
        if kind == "accommodations":
            for day in plan.get("days") or []:
                if not isinstance(day, dict):
                    continue
                current = index.get(_text(day.get("accommodation_option_id")))
                if current and current[0] == "accommodations" and \
                        group_key("accommodations", current[1]) == group and _text(current[1].get("id")) != option_id:
                    problems.append(f"{where}: day {day.get('number')} still has accommodation_option_id "
                                    f"{_text(current[1].get('id'))!r}; the recorded stay must be the one the "
                                    f"group's days sleep at (record_booking.py re-points them).")
                    break
    return problems


def _strings(node: object, path: str):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _strings(value, f"{path}.{key}" if path else str(key))
    elif isinstance(node, list):
        for position, value in enumerate(node):
            yield from _strings(value, f"{path}[{position}]")
    elif isinstance(node, str):
        yield path, node


def stale_stay_mentions(plan: dict) -> list[str]:
    """Places that still send the traveller to a hotel of a decided stay that they did not take.

    A hotel switch re-points the days' accommodation_option_id, which is all code can do: the
    check-in line, the route stops, the directions and the next morning's check-out are prose that
    still names the old property, and the page navigates the traveller there. So once a stay is
    decided, the name of every other hotel in its group is looked for outside the option cards, with
    URLs decoded and the recorded hotel's own name taken out first (a sibling called "Hydro" is not
    mentioned by "Pitlochry Hydro Hotel"). One sentence per day or block, naming every field.
    """
    index = option_index(plan)
    decided: list[tuple[str, str, list[str]]] = []
    for record in records(plan):
        found = index.get(_text(record.get("option_id")))
        if not found or found[0] != "accommodations":
            continue
        group = group_key("accommodations", found[1])
        name = _text(found[1].get("property_name"))
        others = sorted({_text(o.get("property_name")) for kind, o in index.values()
                         if kind == "accommodations" and group_key(kind, o) == group
                         and _text(o.get("property_name")) and _text(o.get("property_name")).casefold() != name.casefold()})
        if name and others:
            decided.append((group.split(":", 1)[1] or "the unnamed stay", name, others))
    findings: dict[str, tuple[str, str, list[str]]] = {}
    for key, value in plan.items():
        if key in NOT_DIRECTIONS:
            continue
        for path, text in _strings(value, key):
            folded = unquote_plus(text).casefold()
            for group, name, others in decided:
                searched = folded.replace(name.casefold(), " ")
                for other in others:
                    if other.casefold() in searched:
                        day = re.match(r"days\[(\d+)\]", path)
                        unit = f"day {plan['days'][int(day.group(1))].get('number', int(day.group(1)) + 1)}" \
                            if day and isinstance(plan["days"][int(day.group(1))], dict) else path.split(".")[0]
                        entry = findings.setdefault(f"{unit}\0{other}\0{name}", (group, unit, []))
                        if path not in entry[2]:
                            entry[2].append(path)
    sentences = []
    for label, (group, unit, paths) in findings.items():
        _, other, name = label.split("\0")
        sentences.append(f"{unit}: {len(paths)} field(s) still name {other}, but the traveller's recorded "
                         f"stay for {group} is {name} -- edit them to the recorded stay: {', '.join(paths)}.")
    return sentences
