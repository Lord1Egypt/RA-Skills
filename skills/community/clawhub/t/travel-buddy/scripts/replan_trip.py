#!/usr/bin/env python3
"""Move an existing Travel Buddy plan onto new dates, a new party size, or a new budget cap.

WHY THIS EXISTS
---------------
`references/research-budget.md` records the incident this script is built around: a measured run
moved the travel window by **one day**, the weekday map was redone by hand, and that manual redo
introduced an off-by-one in every ticket `day_number` and every anchor `planned_day`. The skill
wrote the lesson down and then shipped no tool for it, so the next date change was going to be
done by hand too.

Dates are the dangerous delta because almost every fact researched under a day is keyed to a
*weekday* rather than to a date: opening hours, closure days, market days, Sunday retail law, a
museum that shuts Mondays. Shift the window by one day and all of it quietly becomes a guess while
the plan still looks complete, still renders, and still passes every structural gate.

So this script splits the work at the only line that can be drawn safely:

  * **Rewritten mechanically** — everything that is a pure function of the shift: the trip window,
    every `days[].date`, day numbering, accommodation `check_in`/`check_out`, dated booking fields,
    and the trip dates prefilled into booking URLs. Code cannot get these wrong; a human redoing
    them by hand demonstrably can.
  * **Flagged, never rewritten** — every sentence. "Saturday is the only full shopping day of the
    trip" becomes false when the dates move, and silently swapping the weekday token inside it
    would turn a stale sentence into a confident lie, which is worse than a stale one because it
    reads as freshly checked. Each one lands in `replan_context.must_reverify`, and
    `check_plan_consistency.py` refuses the plan until every entry is resolved.

It also clears `verification_status` and drops `verification_report`, because a plan whose dates
moved was never verified on those dates -- the old report certified a different calendar.

Usage:
    python scripts/replan_trip.py <plan.json> --shift-days 1 --out <new.json>
    python scripts/replan_trip.py <plan.json> --start 2026-10-02 --end 2026-10-05
    python scripts/replan_trip.py <plan.json> --travellers 2 --cap 950 --out <new.json>

The new plan goes to --out, or to stdout when --out is absent. The change log -- what changed,
what was retained, what must be re-verified -- always goes to stderr, so `> new.json` still works.

Read references/replanning.md before using the output.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

# Imported rather than reimplemented so the two tools cannot disagree about what a weekday prefix
# is. `check_dining` decides "this venue is closed that day" with `_parse_weekday_prefix`; if this
# script parsed hours its own way, a card it called safe could be one that gate calls closed, and
# the author would be told two different stories about the same string. If this import ever breaks
# it fails loudly at startup, which is the correct place to find out.
from check_plan_consistency import WEEKDAYS, _parse_weekday_prefix

# Same reasoning as the import above, for the other thing a plan points at from outside itself.
# `imagery_sidecar` is a name RELATIVE to the plan, so a replan that writes the new plan into any
# other directory hands the traveller a plan naming a file that is not beside it -- and both
# consumers are required to refuse that rather than render silently. Reimplementing "where does
# this plan's payload live" here would be a second answer to a question that already has one.
from fetch_plan_imagery import (
    ImagerySidecarError,
    resolve_plan_imagery,
    sidecar_path_for,
    write_json_atomic,
)

# ----------------------------------------------------------------------------------------------
# What may be rewritten
# ----------------------------------------------------------------------------------------------

# Keys holding a date the TRAVELLER is at a place on. These move with the window.
TRAVELLER_DATE_KEYS = frozenset({
    "start_date", "end_date", "date", "check_in", "check_out",
    "departure_date", "return_date", "outbound_date", "inbound_date",
    "pickup_time", "dropoff_time", "valid_from", "valid_until", "travel_date",
})

# Keys holding a date SOMEONE LOOKED SOMETHING UP on. These must never move: shifting a
# `checked_at` would claim the research was redone, which is the one lie this script exists to
# avoid. The `_at` suffix is the convention across every template in this repo, so it is enforced
# as a suffix rule rather than a list nobody remembers to extend.
RESEARCH_STAMP_SUFFIX = "_at"

# Query parameters aside, a trip date inside a URL is the date the button searches for. Leaving it
# behind produces a "check availability" link that opens the OLD dates -- the traveller sees a
# prefilled search, trusts it, and books the wrong nights. Only an exact ISO date equal to one of
# the old window's dates is substituted, which is what keeps a `checked_at` in a URL (or any other
# number that merely looks like a date) out of reach.
_URL_PREFIX = ("http://", "https://")

# Weekday tokens as they appear in PROSE. Deliberately narrower than the set
# check_plan_consistency uses for hours strings: the two-letter German/Dutch forms (mo, di, wo, za)
# are safe at the head of an hours field and pure noise inside a sentence, and a noisy flag list
# gets bulk-resolved without being read, which is the same as no list at all.
_WEEKDAY_PROSE = re.compile(
    r"(?:周|星期|礼拜)[一二三四五六日天]"
    r"|(?<![A-Za-z])(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday"
    r"|mon|tues?|weds?|thurs?|thu|fri|sat|sun"
    r"|montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonnabend|sonntag"
    r"|maandag|dinsdag|woensdag|donderdag|vrijdag|zaterdag|zondag)\.?(?![A-Za-z])",
    re.IGNORECASE)

# An hours window in prose ("10:00-17:45", "10:00–18:00"). An activity that states one is making an
# opening-time claim, and opening times are weekday-keyed even when the sentence does not say so.
_HOURS_IN_PROSE = re.compile(r"\d{1,2}[:：]\d{2}\s*[-–—~～至到]\s*\d{1,2}[:：]\d{2}")

# "Closed on Tuesdays" written in the plan's own prose, next to a weekday token. This is the one
# case where the script can decide something a human would have to notice: if the text says a venue
# shuts on a weekday and the shift lands that stop ON that weekday, the day is already broken and
# nothing else in the pipeline will say so -- check_plan_consistency only reads weekday-prefixed
# `venue_hours`, and an attraction's closure day lives in prose.
#
# Two windows because the markers differ in how certain they are. The hard markers are unambiguous
# and are matched anywhere near the weekday; 休息 also means "sit down and rest", which this repo's
# plans say constantly about benches and cafés, so it counts only when it is glued to the weekday
# token. That is the difference between "closed Mondays" and "somewhere to rest".
_HARD_CLOSURE = re.compile(
    r"闭馆|休馆|停业|休业|不营业|打烊|关门|closed|geschlossen|gesloten|rest\s*day", re.IGNORECASE)
_SOFT_CLOSURE = re.compile(r"休息|不开门|不开放")
# Distance from the closure marker inside which a weekday token is taken to be the day that is
# shut. Punctuation already splits "周三至周一开放、周二闭馆" into its two statements; this handles the
# English form, which often has none: in "the museum is closed Mondays so we go Sunday" only Monday
# is near the marker, and without the distance rule Sunday would be reported as a closure too.
_CLOSURE_REACH = 15
_CLOSURE_GLUE = 4

# Subtrees the weekday scan skips, with the reason each one is exempt:
#   sources[]      - describes what a SOURCE says ("周日仅 13:30-16:30" is the venue's own weekly
#                    timetable, still true after the shift). Flagging it would be the noise that
#                    gets the whole list ignored. Sources are still scanned for the old trip DATES,
#                    which are trip-specific and do go stale.
#   ui_labels      - renderer vocabulary, not trip content.
#   profile_context, replan_context - bookkeeping about the run, not claims about the trip.
WEEKDAY_SCAN_EXEMPT_ROOTS = frozenset({"sources", "ui_labels", "profile_context", "replan_context"})
# The prose scan skips the same bookkeeping subtrees, and two more that are not prose at all:
#   imagery_sidecar - a FILE NAME, and one this script rewrites itself. fetch_plan_imagery.py
#                    derives that name from the plan's stem, and every plan in a real workspace is
#                    named for its start date, so the scan saw the old date inside the name, called
#                    it a sentence quoting a date that moved, and filed an entry at the same path
#                    the imagery block below writes to. The two merged into ONE entry telling the
#                    author to "re-read each sentence against the new calendar and edit it by hand"
#                    about a string the script had just rewritten correctly. Measured on a shift of
#                    a plan whose sidecar was `2026-09-28-chengdu-imagery.json`: one entry at
#                    `imagery_sidecar` carrying both the false prose demand and the real
#                    photograph one. A demand the author checks and finds already correct is how a
#                    must_reverify list stops being read.
#   imagery        - the pre-split inline payload. Its leaves are a label, a licence, an artist and
#                    a `data_uri`, and base64 is not prose: it has no weekday in it that means a
#                    weekday. Measured on the one plan in the real workspace that still carries the
#                    photographs inline (2,132,252 bytes, 7 slots), shifting it +5 days produced an
#                    entry at `imagery` naming five base64 blobs as "field(s) here [that] name a
#                    weekday", because a run of base64 lands "sun"/"mon"/"sat" between two digits
#                    often enough to be certain. What those photographs really need re-checked is
#                    what is IN the frame across a season, which the imagery block below says in
#                    its own sentence.
PROSE_SCAN_EXEMPT_ROOTS = frozenset({"ui_labels", "profile_context", "replan_context", "_contract",
                                     "imagery_sidecar", "imagery"})

# A dining card whose hours_status is one of these says a human went and looked -- on the OLD
# dates. Same set check_plan_consistency uses to decide whether a card claims research.
RESEARCHED_HOURS_STATUS = frozenset({"verified", "researched"})


def _weekday_name(date: dt.date) -> str:
    cn, _full, en = WEEKDAYS[date.weekday()]
    return f"{cn}/{en.title()}"


def _prose_weekday_tokens() -> dict[str, int]:
    """Every spelling `_WEEKDAY_PROSE` can match, mapped to Python's weekday index."""
    tokens: dict[str, int] = {}
    for index, (cn, _cn_full, en) in WEEKDAYS.items():
        for prefix in ("周", "星期", "礼拜"):
            tokens[prefix + cn[-1]] = index
        tokens[en] = index
        tokens[en[:3]] = index
    for prefix in ("周", "星期", "礼拜"):
        tokens[prefix + "天"] = 6  # 周天 is Sunday in speech and on shop signage
    tokens.update({"tues": 1, "weds": 2, "thur": 3, "thurs": 3})
    tokens.update({"montag": 0, "dienstag": 1, "mittwoch": 2, "donnerstag": 3, "freitag": 4,
                   "samstag": 5, "sonnabend": 5, "sonntag": 6,
                   "maandag": 0, "dinsdag": 1, "woensdag": 2, "donderdag": 3, "vrijdag": 4,
                   "zaterdag": 5, "zondag": 6})
    return tokens


_PROSE_WEEKDAY_INDEX = _prose_weekday_tokens()
# Sentences are judged clause by clause. "周三至周一开放、周二闭馆" says the venue OPENS Wed-Mon and
# SHUTS Tuesday; read as one blob, the closure marker sits within a dozen characters of 周三 and the
# rule would announce the museum is closed on the day it is open. Splitting on the punctuation that
# separates the two statements is what makes the finding trustworthy, and a finding nobody trusts
# is one the next author switches off.
_CLAUSE_SPLIT = re.compile(r"[，。；、,;!?！？\n]+|——|--")
_RANGE_BETWEEN = re.compile(r"^\s*(?:[-–—~～]|至|到|through|thru|to)\s*$", re.IGNORECASE)


def _closure_weekdays(text: str) -> set[int]:
    """Weekday indices this text says a venue is SHUT on.

    Only what the plan states outright. A complement is never inferred: "周六 07:00-14:30" probably
    does mean a Saturday-only market, and probably is not what an author meant to promise, so
    turning it into six closure days would invent six facts per sentence.
    """
    shut: set[int] = set()
    for clause in _CLAUSE_SPLIT.split(text):
        matches = list(_WEEKDAY_PROSE.finditer(clause))
        if not matches:
            continue
        markers = [m.span() for m in _HARD_CLOSURE.finditer(clause)]
        indices: list[int | None] = [
            _PROSE_WEEKDAY_INDEX.get(m.group(0).rstrip(".").lower()) for m in matches]
        for position, (match, index) in enumerate(zip(matches, indices)):
            if index is None:
                continue
            near = any(start - match.end() <= _CLOSURE_REACH and match.start() - end <= _CLOSURE_REACH
                       for start, end in markers)
            glued = clause[match.start():match.end() + _CLOSURE_GLUE]
            if not (near or _SOFT_CLOSURE.search(glued)):
                continue
            shut.add(index)
            # "Tue-Sun closed" shuts the whole run, not just its ends.
            if position + 1 < len(matches) and indices[position + 1] is not None:
                gap = clause[match.end():matches[position + 1].start()]
                if _RANGE_BETWEEN.match(gap):
                    cursor = index
                    while cursor != indices[position + 1]:
                        cursor = (cursor + 1) % 7
                        shut.add(cursor)
    return shut


def _refuse(headline: str, *lines: str) -> "None":
    """Every refusal names what is wrong and what the author should do instead.

    Refusals print and exit rather than raising: an operator who gets a traceback learns nothing
    about their plan, and this script's whole audience is someone whose dates just moved.
    """
    print(f"REPLAN REFUSED: {headline}", file=sys.stderr)
    for line in lines:
        print(f"  {line}", file=sys.stderr)
    raise SystemExit(2)


# ----------------------------------------------------------------------------------------------
# Walking the plan
# ----------------------------------------------------------------------------------------------

def _leaves(node: object, path: str = ""):
    """Every scalar leaf of the plan with its pointer path, in `days[0].dining[1].venue_hours` form.

    The same syntax check_plan_consistency's `resolve_pointer` reads, on purpose: every path this
    script writes into must_reverify has to resolve there, or the gate reports a pointer nobody can
    follow back to the plan.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _leaves(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _leaves(value, f"{path}[{index}]")
    else:
        yield path, node


def _key_of(path: str) -> str:
    return re.sub(r"\[\d+\]$", "", path.rsplit(".", 1)[-1])


def _root_of(path: str) -> str:
    return re.sub(r"\[\d+\].*$", "", path.split(".", 1)[0])


def _container_of(path: str) -> str:
    """The unit an author fixes in one editing pass: a day, or a top-level block.

    Prose findings are grouped onto this rather than raised one per field. A day's narrative is
    rewritten as one pass against the new weekday, not as seventeen independent decisions, and a
    list long enough to skim past is a list that gets bulk-marked resolved. Every individual path
    still appears inside the entry's reason, so nothing is hidden -- only gathered.
    """
    day = re.match(r"days\[\d+\]", path)
    if day:
        return day.group(0)
    return _root_of(path)


def _set_at(plan: object, path: str, value: object) -> None:
    """Assign through a pointer path produced by `_leaves`, so a rewrite lands where it was read."""
    steps = re.findall(r"([^.\[\]]+)|\[(\d+)\]", path)
    current = plan
    for position, (key, index) in enumerate(steps):
        last = position == len(steps) - 1
        if key:
            if last:
                current[key] = value
            else:
                current = current[key]
        else:
            slot = int(index)
            if last:
                current[slot] = value
            else:
                current = current[slot]


# ----------------------------------------------------------------------------------------------
# The mechanical rewrite
# ----------------------------------------------------------------------------------------------

_ISO_HEAD = re.compile(r"^(\d{4})-(\d{2})-(\d{2})(.*)$", re.DOTALL)


def _shift_dated_fields(plan: dict, delta: int, window: set[dt.date],
                        changes: list[tuple[str, str]], skipped: list[str]) -> None:
    """Move every traveller-facing date by `delta` days, and nothing else.

    Two guards decide what is touched, and both must pass:
      1. the key names a date the traveller travels on (never a `*_at` research stamp), and
      2. the value falls inside the OLD trip window.

    The second guard is what keeps a ticket's `valid_until` -- the venue's own rule, which did not
    move because the traveller's calendar did -- from being silently rewritten, and it is also why
    a research stamp that somehow escaped the first guard still cannot be shifted. Anything the
    guards reject is reported rather than dropped.
    """
    # A checkout is the morning AFTER the last night, so it is the one traveller date that
    # legitimately sits a day outside the trip window -- and a window guard alone therefore skips
    # exactly the field that turns a three-night booking into a different stay. Widen the window
    # for that key only, rather than loosening the guard for every key, which is what protects a
    # ticket's valid_until from being dragged along by a calendar it does not follow.
    checkout_window = window | {max(window) + dt.timedelta(days=1)} if window else window

    for path, value in list(_leaves(plan)):
        if not isinstance(value, str):
            continue
        key = _key_of(path)
        if key.endswith(RESEARCH_STAMP_SUFFIX):
            continue
        if key not in TRAVELLER_DATE_KEYS and not key.endswith("_date"):
            continue
        head = _ISO_HEAD.match(value.strip())
        if not head:
            continue
        try:
            old = dt.date(int(head.group(1)), int(head.group(2)), int(head.group(3)))
        except ValueError:
            continue
        permitted = checkout_window if key == "check_out" else window
        if old not in permitted:
            skipped.append(f"{path} = {value!r} (outside the old trip window; left as it was)")
            continue
        new_value = (old + dt.timedelta(days=delta)).isoformat() + head.group(4)
        _set_at(plan, path, new_value)
        changes.append((path, f"{value} -> {new_value}"))


def _shift_urls(plan: dict, delta: int, window: list[dt.date],
                changes: list[tuple[str, str]]) -> None:
    """Re-date the trip dates prefilled into booking and search URLs.

    A hotel button carrying `checkin=2026-09-18` after the window moved to the 19th opens a search
    for nights the traveller is not there. The page still renders, the gate still passes, and the
    defect surfaces at the payment screen. Only exact ISO dates equal to a date in the old window
    are substituted, so a `checked_at` embedded in a URL, or any other digits that merely look like
    a date, are out of range by construction.
    """
    # Include the checkout day for the same reason _shift_dated_fields does: a hotel search URL
    # carries checkin AND checkout, and the checkout is the morning after the last night. Leaving
    # it behind produces a button that opens a search for a stay one night shorter than the plan --
    # visibly wrong only at the payment screen, which is the worst place to find out.
    span = list(window) + ([max(window) + dt.timedelta(days=1)] if window else [])
    mapping = {d.isoformat(): (d + dt.timedelta(days=delta)).isoformat() for d in span}
    pattern = re.compile("|".join(re.escape(d) for d in mapping))
    for path, value in list(_leaves(plan)):
        if not isinstance(value, str) or not value.startswith(_URL_PREFIX):
            continue
        found = pattern.findall(value)
        if not found:
            continue
        _set_at(plan, path, pattern.sub(lambda m: mapping[m.group(0)], value))
        moved = ", ".join(f"{old}->{mapping[old]}" for old in dict.fromkeys(found))
        changes.append((path, f"prefilled dates {moved}"))


def _renumber_days(plan: dict, changes: list[tuple[str, str]]) -> list[str]:
    """Re-derive day numbering from position, and check every day link still lands.

    This is the off-by-one guard. In the measured incident the weekday map was redone by hand and
    every `day_number` and `planned_day` slipped by one, so tickets pointed at the wrong day and
    nothing objected. A pure shift keeps position -> day number identical, so the correct output
    here is *no change at all* -- and saying so out loud, with the link count, is the point. A tool
    that stays silent about the thing that broke last time is not reassuring, it is quiet.
    """
    warnings: list[str] = []
    days = plan.get("days") if isinstance(plan.get("days"), list) else []

    # Build old -> new BEFORE mutating anything. The first version of this function renumbered days
    # by position and then only range-checked the links, on the reasoning that a pure shift leaves
    # position -> number identical. That holds only when the source is already numbered 1..n. Given
    # a plan numbered 2,3,4 -- which every gate accepts, because they check dates and ranges, not
    # the numbering's origin -- renumbering to 1,2,3 silently rebinds every link: a ticket reading
    # day_number 3 meant the middle day before and means the last day after. That is the off-by-one
    # references/research-budget.md records, reintroduced by the tool written to prevent it, while
    # the change log asserted the links had been re-derived. They had not been touched.
    renumber: dict[int, int] = {}
    for index, day in enumerate(days):
        if not isinstance(day, dict):
            continue
        old_number = day.get("number")
        if old_number != index + 1:
            if isinstance(old_number, int):
                renumber[old_number] = index + 1
            changes.append((f"days[{index}].number", f"{old_number} -> {index + 1}"))
            day["number"] = index + 1

    count = len(days)
    booking = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    tickets = booking.get("attraction_tickets") if isinstance(booking.get("attraction_tickets"), list) else []
    anchors = plan.get("destination_experience_anchors")
    anchors = anchors if isinstance(anchors, list) else []
    for index, ticket in enumerate(tickets):
        if not isinstance(ticket, dict):
            continue
        target = ticket.get("day_number")
        if isinstance(target, int) and target in renumber:
            ticket["day_number"] = renumber[target]
            changes.append((f"booking_options.attraction_tickets[{index}].day_number",
                            f"{target} -> {renumber[target]} (follows its day, which was renumbered)"))
            continue
        if isinstance(target, int) and not 1 <= target <= count:
            warnings.append(
                f"booking_options.attraction_tickets[{index}].day_number={target} is outside "
                f"1..{count}. That link was already broken before the shift; fix it in the source "
                f"plan -- check_plan_consistency.py reports it too.")
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            continue
        target = anchor.get("planned_day")
        if isinstance(target, int) and target in renumber:
            anchor["planned_day"] = renumber[target]
            changes.append((f"destination_experience_anchors[{index}].planned_day",
                            f"{target} -> {renumber[target]} (follows its day, which was renumbered)"))
            continue
        if isinstance(target, int) and not 1 <= target <= count:
            warnings.append(
                f"destination_experience_anchors[{index}].planned_day={target} is outside "
                f"1..{count}. No gate checks this field, so it would ship silently; fix it in the "
                f"source plan.")
    return warnings


# ----------------------------------------------------------------------------------------------
# What the shift invalidated
# ----------------------------------------------------------------------------------------------

class Findings:
    """must_reverify entries, deduplicated by path, reasons merged.

    Deduplication matters because the classes overlap by design: a dining card can be researched
    AND carry a weekday prefix that no longer matches. Two entries for one field would be two
    things to resolve and one thing to check.
    """

    def __init__(self) -> None:
        self.by_path: dict[str, list[str]] = {}
        self.order: list[str] = []

    def add(self, path: str, reason: str) -> None:
        if path not in self.by_path:
            self.by_path[path] = []
            self.order.append(path)
        if reason not in self.by_path[path]:
            self.by_path[path].append(reason)

    def paths(self) -> set[str]:
        return set(self.by_path)

    def entries(self) -> list[dict]:
        # The trailing full stop is dropped because check_plan_consistency prints the reason
        # mid-sentence -- "... -- {reason}. Re-check that field" -- and a stored period turns every
        # one of those lines into "..".
        return [{"path": path, "reason": re.sub(r"\.\s*$", "", " ".join(self.by_path[path])),
                 "resolved": False, "resolution": None}
                for path in self.order]


def _day_dates(plan: dict) -> list[tuple[int, dt.date | None]]:
    out: list[tuple[int, dt.date | None]] = []
    days = plan.get("days") if isinstance(plan.get("days"), list) else []
    for index, day in enumerate(days):
        value = day.get("date") if isinstance(day, dict) else None
        try:
            out.append((index, dt.date.fromisoformat(str(value))))
        except (TypeError, ValueError):
            out.append((index, None))
    return out


def _flag_dining(plan: dict, delta: int, findings: Findings) -> None:
    """Opening hours are weekday-keyed, so a shift invalidates the CLAIM, not just the schedule.

    Two rules, and the second is the broad one on purpose. A card whose venue_hours names weekdays
    that no longer include this day is an outright conflict. A card that merely says its hours were
    researched is a card someone checked against a calendar that no longer applies -- and that is
    exactly the defect the adversarial pass found: a restaurant self-declared "researched" with
    hours wrong by 90 minutes at the front and an hour at the back, scheduled on the venue's rest
    day.
    """
    for index, date in _day_dates(plan):
        if date is None:
            continue
        old = date - dt.timedelta(days=delta)
        moved = delta % 7 != 0
        day = plan["days"][index]
        for position, card in enumerate(day.get("dining") or []):
            if not isinstance(card, dict):
                continue
            venue = card.get("venue_name") or "this venue"
            hours = card.get("venue_hours")
            path = f"days[{index}].dining[{position}].venue_hours"
            if isinstance(hours, str) and hours.strip():
                open_days, _rest = _parse_weekday_prefix(hours)
                if open_days is not None and date.weekday() not in open_days:
                    covered = ", ".join(WEEKDAYS[i][2].title() for i in sorted(open_days))
                    findings.add(path, (
                        f"'{venue}' now falls on {_weekday_name(date)} ({date}) but its "
                        f"venue_hours {hours!r} cover only {covered}. The venue is shut on the new "
                        f"day: move the meal, take the backup venue, or re-research the hours."))
                elif open_days is None and _WEEKDAY_PROSE.search(hours):
                    findings.add(path, (
                        f"'{venue}' has weekday-keyed venue_hours {hours!r} that this script "
                        f"cannot decide (per-day hours, or a closed-day marker), and the day moved "
                        f"{_weekday_name(old)} -> {_weekday_name(date)}. Read them by hand."))
            status = str(card.get("hours_status") or "").strip().lower()
            if status in RESEARCHED_HOURS_STATUS:
                findings.add(path, (
                    f"hours_status='{status}' claims someone checked '{venue}' -- for "
                    f"{old} ({_weekday_name(old)}), which this day no longer is"
                    + (f"; it is now {date} ({_weekday_name(date)}) and opening hours are "
                       f"weekday-keyed. " if moved else
                       f"; it is now {date}, and hours researched for a different week are not a "
                       f"current fact. ")
                    + f"Re-check the hours and the closure day, or set hours_status='unverified'."))


def _flag_activities(plan: dict, delta: int, findings: Findings) -> None:
    """Ticket notes and opening-time claims: priced, timed, and gated by the day they sit on."""
    for index, date in _day_dates(plan):
        if date is None:
            continue
        old = date - dt.timedelta(days=delta)
        day = plan["days"][index]
        for position, activity in enumerate(day.get("activities") or []):
            if not isinstance(activity, dict):
                continue
            name = activity.get("name") or "this stop"
            note = activity.get("ticket_note")
            if isinstance(note, str) and note.strip():
                findings.add(f"days[{index}].activities[{position}].ticket_note", (
                    f"'{name}' carries a ticket note researched for {old} "
                    f"({_weekday_name(old)}); the stop is now on {date} ({_weekday_name(date)}). "
                    f"Timed entry, weekday pricing and same-day availability are all keyed to the "
                    f"day -- re-check the ticket before this note goes on the page."))
            detail = activity.get("detail")
            if isinstance(detail, str) and _HOURS_IN_PROSE.search(detail):
                findings.add(f"days[{index}].activities[{position}].detail", (
                    f"'{name}' states opening hours in its detail text. Hours are weekday-keyed "
                    f"and this stop moved {_weekday_name(old)} -> {_weekday_name(date)}; confirm "
                    f"the venue opens at all, and at those hours, on the new day."))


def _day_owned_leaves(plan: dict, index: int):
    """Every prose leaf that belongs to day `index`: the day card, plus the tickets and anchors
    that link to it. A museum's closure day is written in `attraction_tickets[].booking_note`, not
    in the day card, so scanning the day alone would miss the field that states the defect."""
    yield from _leaves(plan["days"][index], f"days[{index}]")
    number = index + 1
    booking = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    for position, ticket in enumerate(booking.get("attraction_tickets") or []):
        if isinstance(ticket, dict) and ticket.get("day_number") == number:
            yield from _leaves(ticket, f"booking_options.attraction_tickets[{position}]")
    for position, anchor in enumerate(plan.get("destination_experience_anchors") or []):
        if isinstance(anchor, dict) and anchor.get("planned_day") == number:
            yield from _leaves(anchor, f"destination_experience_anchors[{position}]")


def _flag_closure_conflicts(plan: dict, delta: int, findings: Findings) -> list[str]:
    """The plan's own text says this venue shuts on a weekday, and the shift lands the day on it.

    This is the whole reason the script exists rather than a checklist. Nothing else in the
    pipeline can see it: `check_dining` only reads a weekday prefix on a dining card's
    `venue_hours`, and an attraction's closure day is prose in an activity detail or a ticket note.
    Measured on the Leiden->Cologne plan, a +1 day shift produced two of these -- the Ludwig
    Museum's Monday closure and the Roemisch-Germanisches Museum's Tuesday one -- and each would
    have been a locked door the traveller found by standing in front of it.

    Raised loudly and separately from the generic weekday flag, because the answer is not "check
    this" but "this day no longer works".
    """
    headlines: list[str] = []
    for index, date in _day_dates(plan):
        if date is None:
            continue
        old = date - dt.timedelta(days=delta)
        for path, value in _day_owned_leaves(plan, index):
            if not isinstance(value, str) or not value.strip():
                continue
            key = _key_of(path)
            if key.endswith("_url") or value.startswith(_URL_PREFIX):
                continue
            shut = _closure_weekdays(value)
            if date.weekday() not in shut or old.weekday() in shut:
                continue
            quoted = re.sub(r"\s+", " ", value.strip())
            quoted = quoted if len(quoted) <= 90 else quoted[:87] + "..."
            headline = (
                f"day {index + 1} now falls on {_weekday_name(date)} ({date}), and {path} states a "
                f"closure on that weekday: \"{quoted}\"")
            headlines.append(headline)
            findings.add(path, (
                f"CLOSED ON THE NEW DAY. {headline}. The day used to be {_weekday_name(old)}, "
                f"which this text does not close. Whatever this sentence promises is now behind a "
                f"locked door: move it to another day, take the fallback the plan already names, "
                f"or drop it. Do not re-check this one and tick it off -- the plan already carries "
                f"its own refutation."))
    return headlines


def _flag_prose(plan: dict, delta: int, old_window: list[dt.date],
                findings: Findings) -> dict[str, list[str]]:
    """Every sentence naming a weekday, or quoting a date that moved. Flagged, never rewritten.

    This is the class the script refuses to touch. "Saturday is the only full shopping day of the
    trip" is a *conclusion* about the trip, not a token: after a one-day shift the sentence may
    need a different day, a different activity, or deleting outright, and only a human knows
    which. Rewriting the weekday inside it would produce a sentence that is confidently wrong and
    looks freshly checked -- strictly worse than one that is visibly stale.

    Returns the grouped paths so the change log can print every one of them.
    """
    weekdays_moved = delta % 7 != 0
    groups: dict[str, list[str]] = {}
    already = findings.paths()
    old_dates = {d.isoformat() for d in old_window}

    for path, value in _leaves(plan):
        if not isinstance(value, str) or not value.strip():
            continue
        key = _key_of(path)
        if key.endswith(RESEARCH_STAMP_SUFFIX) or key.endswith("_url") or value.startswith(_URL_PREFIX):
            continue
        if key in TRAVELLER_DATE_KEYS or key.endswith("_date"):
            continue  # already rewritten; the value is current
        root = _root_of(path)
        if root in PROSE_SCAN_EXEMPT_ROOTS:
            continue

        quotes_old_date = any(d in value for d in old_dates)
        names_weekday = (weekdays_moved
                         and root not in WEEKDAY_SCAN_EXEMPT_ROOTS
                         and bool(_WEEKDAY_PROSE.search(value)))
        if not (quotes_old_date or names_weekday):
            continue
        if path in already:
            # This field already has its own entry (researched hours, a ticket note, a closure
            # conflict). Adding the prose warning to that entry keeps one field to one thing to
            # resolve, instead of asking the author to fix the same sentence in two places.
            findings.add(path, "The sentence itself names a weekday or quotes a date that moved, "
                               "and the script never rewrites prose -- edit it by hand too.")
            continue
        groups.setdefault(_container_of(path), []).append(path)

    for container, paths in groups.items():
        day = re.match(r"days\[(\d+)\]$", container)
        if day:
            index = int(day.group(1))
            date = dict(_day_dates(plan)).get(index)
            if date is None:
                moved = "this day moved"
            else:
                old = date - dt.timedelta(days=delta)
                moved = (f"day {index + 1} moved {old} ({_weekday_name(old)}) -> "
                         f"{date} ({_weekday_name(date)})")
        else:
            moved = f"the trip window moved by {delta:+d} day(s)"
        listed = ", ".join(sorted(paths))
        findings.add(container, (
            f"{moved}; {len(paths)} field(s) here name a weekday or quote a date that changed, and "
            f"prose is never rewritten by the script: {listed}. Re-read each sentence against the "
            f"new calendar and edit it by hand -- swapping the weekday token would turn a stale "
            f"sentence into a confident lie."))
    return groups


def _flag_party(plan: dict, old_count: object, new_count: int, findings: Findings) -> None:
    """A party-size change moves money and rooms, and neither is a pure function of the number."""
    booking = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
    stays = booking.get("accommodations") if isinstance(booking.get("accommodations"), list) else []
    for index, stay in enumerate(stays):
        if not isinstance(stay, dict):
            continue
        findings.add(f"booking_options.accommodations[{index}].room_count", (
            f"the party changed {old_count} -> {new_count}, and rooms are not a pure function of "
            f"heads: '{stay.get('property_name')}' still holds guest_count="
            f"{stay.get('guest_count')}, room_count={stay.get('room_count')}, its room_basis, its "
            f"per-night price and a search URL prefilled for the old party. Re-price the stay and "
            f"confirm the room product sleeps {new_count}."))
    if isinstance(plan.get("budget"), dict):
        findings.add("budget", (
            f"the party changed {old_count} -> {new_count}. Per-person rows built from a "
            f"per-room or per-vehicle cost do not survive that division; re-derive every "
            f"breakdown row and the per-person totals."))
    if isinstance(plan.get("transport_overview"), dict):
        findings.add("transport_overview", (
            f"the party changed {old_count} -> {new_count}: group fares, seat reservations and "
            f"any per-vehicle cost need re-pricing for {new_count} traveller(s)."))


def _flag_bookings(plan: dict, what_moved: str, findings: Findings) -> None:
    """A purchase does not move with the plan. The option card is shifted like any other, but the
    ticket or room the traveller paid for is still for the old dates and the old party, and the
    page would keep calling it Booked. A `chosen` record is a decision, not a purchase, and stays."""
    records = plan.get("bookings") if isinstance(plan.get("bookings"), list) else []
    for index, record in enumerate(records):
        if not isinstance(record, dict) or record.get("state") != "booked":
            continue
        option = record.get("option_id")
        findings.add(f"bookings[{index}]", (
            f"'{option}' was recorded as booked (on {record.get('booked_on')}, via "
            f"{record.get('booked_via')}) for the plan before {what_moved}; the purchase did not move "
            f"with it. Change or rebook it with the provider, then record the result with "
            f"python scripts/record_booking.py <plan.json> --option {option} --booked ..., or remove "
            f"the record with --clear {option} if it was cancelled"))


def _flag_cap(plan: dict, old_cap: object, new_cap: float, findings: Findings) -> None:
    """A lowered cap re-opens choices that were made under the old one."""
    budget = plan.get("budget") if isinstance(plan.get("budget"), dict) else {}
    findings.add("budget.estimated_per_person_high", (
        f"the budget cap moved {old_cap} -> {new_cap:g}, below the plan's high case "
        f"{budget.get('estimated_per_person_high')}. Lodging tier, paid activities and fare class "
        f"were all chosen under the old cap; re-select them, or get the traveller to acknowledge "
        f"the overrun explicitly (budget.overrun_acknowledged)."))


def _carry_forward(plan: dict, findings: Findings) -> int:
    """Unresolved entries from a previous replan survive this one.

    Replanning twice is normal -- the dates move, then the party changes -- and the second run
    overwrites replan_context. Without this, every fact the first replan flagged and nobody
    resolved would vanish at exactly the moment the plan looked freshly generated.
    """
    previous = plan.get("replan_context")
    if not isinstance(previous, dict):
        return 0
    source = previous.get("replanned_from") or "the previous replan"
    carried = 0
    for entry in previous.get("must_reverify") or []:
        if not isinstance(entry, dict) or entry.get("resolved") is True:
            continue
        path = entry.get("path")
        if not isinstance(path, str) or not path.strip():
            continue
        findings.add(path.strip(), f"[carried over unresolved from {source}] {entry.get('reason')}")
        carried += 1
    return carried


# ----------------------------------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------------------------------

def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move a Travel Buddy plan onto new dates, party size, or budget cap.")
    parser.add_argument("plan", help="Existing plan JSON")
    parser.add_argument("--shift-days", type=int, default=None, metavar="N",
                        help="Move the whole window N days later (negative moves it earlier)")
    parser.add_argument("--start", default=None, metavar="DATE",
                        help="New start date; requires --end and the same day count")
    parser.add_argument("--end", default=None, metavar="DATE", help="New end date")
    parser.add_argument("--travellers", type=int, default=None, metavar="N", help="New party size")
    parser.add_argument("--cap", type=float, default=None, metavar="AMOUNT",
                        help="New per-person budget cap")
    parser.add_argument("--change-request", default=None, metavar="TEXT",
                        help="What the traveller asked for, in their words")
    parser.add_argument("--today", default=None, metavar="DATE",
                        help="Treat this as today when refusing a trip in the past")
    parser.add_argument("--out", default=None, metavar="PATH",
                        help="Write the new plan here (default: stdout)")
    return parser.parse_args(argv)


def _read_plan(path: str) -> dict:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        _refuse(f"could not read {path}: {exc}",
                "Give the path of an existing plan JSON.")
    try:
        plan = json.loads(raw)
    except json.JSONDecodeError as exc:
        _refuse(f"{path} is not valid JSON: {exc}",
                "Fix the JSON first -- a replan of a file nothing can parse would be a new plan, "
                "not a revision. `python -m json.tool <file>` points at the character.")
    if not isinstance(plan, dict):
        _refuse(f"{path} holds a {type(plan).__name__}, not a plan object.",
                "Pass the final-trip-plan JSON, whose top level is an object with a `trip` key.")
    return plan


def _iso(value: object, label: str) -> dt.date:
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError):
        _refuse(f"{label} is {value!r}, which is not an ISO date (YYYY-MM-DD).",
                "Every date check downstream reads ISO dates; fix it in the source plan first.")


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    plan = _read_plan(args.plan)

    trip = plan.get("trip") if isinstance(plan.get("trip"), dict) else {}
    old_start = _iso(trip.get("start_date"), "trip.start_date")
    old_end = _iso(trip.get("end_date"), "trip.end_date")
    if old_end < old_start:
        _refuse(f"trip.start_date {old_start} is after trip.end_date {old_end}.",
                "Run `python scripts/check_plan_consistency.py` on the source plan and fix the "
                "window before shifting it.")
    days = plan.get("days") if isinstance(plan.get("days"), list) else []
    span = (old_end - old_start).days + 1
    if len(days) != span:
        _refuse(f"the plan has {len(days)} day card(s) but its window {old_start}..{old_end} is "
                f"{span} day(s) long.",
                "A shift preserves the day count, so it cannot fix a plan that already disagrees "
                "with itself. Run `python scripts/check_plan_consistency.py` on the source plan "
                "first.")

    today = _iso(args.today, "--today") if args.today else dt.date.today()

    # --- work out the delta -------------------------------------------------------------------
    if args.shift_days is not None and (args.start or args.end):
        _refuse("--shift-days and --start/--end both given.",
                "Name the window one way: --shift-days N, or --start DATE --end DATE.")
    if bool(args.start) != bool(args.end):
        _refuse("--start and --end must be given together.",
                "A new window needs both ends, so the day count can be checked against the plan.")

    delta = 0
    if args.shift_days is not None:
        delta = args.shift_days
    elif args.start:
        new_start = _iso(args.start, "--start")
        new_end = _iso(args.end, "--end")
        new_span = (new_end - new_start).days + 1
        if new_end < new_start:
            _refuse(f"--start {new_start} is after --end {new_end}.", "Swap them.")
        if new_span != span:
            _refuse(f"--start/--end is {new_span} day(s) but the plan holds {span} day(s) "
                    f"({old_start}..{old_end}).",
                    "That is a re-plan, not a shift: this script moves an itinerary, it cannot "
                    "invent a day's route or delete one and keep the budget honest. Add or remove "
                    f"the day(s) deliberately in the plan first, then shift the {new_span}-day "
                    "window, or start a fresh plan with "
                    "`python scripts/new_plan_skeleton.py --start ... --end ...`.")
        delta = (new_start - old_start).days

    if delta == 0 and args.travellers is None and args.cap is None:
        _refuse("no change was requested.",
                "Give at least one delta: --shift-days N, --start DATE --end DATE, --travellers N, "
                "or --cap AMOUNT.")

    new_start, new_end = old_start + dt.timedelta(days=delta), old_end + dt.timedelta(days=delta)
    if delta and new_start < today:
        _refuse(f"that shift starts the trip on {new_start}, before today ({today}).",
                "A plan cannot be moved into the past. Choose a future window, or pass --today "
                "DATE if the machine clock is wrong.")

    old_window = [old_start + dt.timedelta(days=n) for n in range(span)]

    # --- rewrite what code can rewrite correctly ----------------------------------------------
    changes: list[tuple[str, str]] = []
    skipped: list[str] = []
    if delta:
        _shift_dated_fields(plan, delta, set(old_window), changes, skipped)
        _shift_urls(plan, delta, old_window, changes)
    link_warnings = _renumber_days(plan, changes)

    old_travellers = trip.get("traveler_count")
    if args.travellers is not None and args.travellers != old_travellers:
        trip["traveler_count"] = args.travellers
        changes.append(("trip.traveler_count", f"{old_travellers} -> {args.travellers}"))

    budget = plan.get("budget") if isinstance(plan.get("budget"), dict) else None
    old_cap = budget.get("cap_per_person") if budget else None
    cap_lowered = False
    if args.cap is not None and budget is not None and old_cap != args.cap:
        budget["cap_per_person"] = args.cap
        changes.append(("budget.cap_per_person", f"{old_cap} -> {args.cap:g}"))
        # An acknowledgement of the OLD cap is not an acknowledgement of the new one. Left in
        # place it would let a fresh cap be broken by exactly the flag the traveller set for a
        # different number, and check_budget would stay green while doing it.
        if budget.get("overrun_acknowledged") is True:
            budget["overrun_acknowledged"] = None
            changes.append(("budget.overrun_acknowledged",
                            "true -> null (it was agreed against the old cap)"))
        high = budget.get("estimated_per_person_high")
        cap_lowered = isinstance(high, (int, float)) and high > args.cap

    # --- collect what it must not rewrite ------------------------------------------------------
    findings = Findings()
    carried = _carry_forward(plan, findings)
    closures: list[str] = []
    if delta:
        closures = _flag_closure_conflicts(plan, delta, findings)
        _flag_dining(plan, delta, findings)
        _flag_activities(plan, delta, findings)
    if args.travellers is not None and args.travellers != old_travellers:
        _flag_party(plan, old_travellers, args.travellers, findings)
    moved = [f"the dates moved {delta:+d} day(s)"] if delta else []
    if args.travellers is not None and args.travellers != old_travellers:
        moved.append(f"the party changed {old_travellers} -> {args.travellers}")
    if moved:
        _flag_bookings(plan, " and ".join(moved), findings)
    if cap_lowered:
        _flag_cap(plan, old_cap, args.cap, findings)
    prose_groups = _flag_prose(plan, delta, old_window, findings) if delta else {}

    # The verification covered the old calendar and the old party. Nothing in it survives a delta,
    # so it is cleared rather than carried -- a stale "verified" is the single most expensive
    # thing this file can leave behind, because the page prints no warning for it.
    old_status = plan.get("verification_status")
    old_report = plan.get("verification_report")
    plan["verification_status"] = None
    plan["verification_report"] = None
    findings.add("verification_status", (
        "the plan's verification was cleared by this replan. It certified the OLD "
        f"{'window ' + old_start.isoformat() + '..' + old_end.isoformat() if delta else 'plan'}, "
        "so entry, transport, hours, lodging and seasonality were all checked against conditions "
        "this plan no longer has. Re-run the five-domain pass in references/verification.md and "
        "save with a fresh report."))

    # The same argument, one field over, and it was missed on the first pass because this one is
    # not about facts in the world -- it is about checks that ran. `gates_passed` records that the
    # deterministic gates passed, and save_trip_deliverables.py renders it onto the page as a
    # visible "Structure checks passed: N" line. Those gates ran on the OLD dates, against the old
    # day-to-weekday mapping, the old accommodation windows and the old ticket day links, which is
    # precisely what a delta invalidates. Carried forward it produced the worst shape this file can
    # emit: a shifted plan that `check_plan_consistency.py` REFUSES -- unresolved must_reverify
    # entries, exit 1 -- rendering a page that tells the traveller in plain text that two dozen
    # structure checks passed on it. The verification banner would not have covered for it either,
    # because the two are separate claims and only one of them was being cleared.
    old_gates = plan.get("gates_passed")
    if old_gates is not None:
        plan["gates_passed"] = None
        findings.add("gates_passed", (
            "the structure-gate stamp was cleared by this replan. It recorded gates that ran on "
            "the OLD calendar, and this plan's dates, weekdays, accommodation windows and ticket "
            "day links are not the ones they checked. save_trip_deliverables.py stamps it again "
            "when the gates actually pass on the new dates."))

    # The photographs travel WITH the plan, and the key naming them is rewritten to where they
    # landed. Two different questions, and this script had been answering neither:
    #
    #   * What stays true. A photograph is of a place, and a date change moves no places. This
    #     script's own retained_note says route order, stop selection and venue choices are
    #     unchanged, so every slot in the payload still depicts the thing its caption names -- the
    #     hero is still the destination, `anchor:2` is still the same anchor at the same index.
    #     Dropping them would delete verified, licence-checked work that the delta did not touch,
    #     and re-fetching costs a network the traveller may not have.
    #   * What does not. What is IN the frame is seasonal: shift a trip from September to January
    #     and a photograph of a beach in full sun is still honest about the place and misleading
    #     about the visit. And slot keys are positional, so if re-verification adds, drops or
    #     reorders an anchor, every anchor photograph after it moves to a heading it is not of.
    #     Both go into must_reverify rather than being silently accepted or silently discarded.
    #
    # Measured before this existed: `replan_trip.py <plan.json> --shift-days 5 --out <other
    # dir>/new.json` -- the flow the module docstring documents -- copied `imagery_sidecar`
    # verbatim, so the new plan named a file that was not beside it and BOTH
    # `render_final_trip_html.py` and `save_trip_deliverables.py` exited 2 on it. A replan that
    # produces a plan nothing can read is not a replan.
    #
    # A PRE-SPLIT plan reaches all of that too, and until it did the one plan in the real workspace
    # holding photographs was the one this block ignored. It carries them under `imagery` inline
    # with no `imagery_sidecar` key at all, so the sidecar-only gate below used to skip it and the
    # 2MB rode into the new plan inline: measured on a copy of
    # `plans/2026-11-16-拉纳卡-...json` (2,132,252 bytes, 7 inline slots), `--shift-days 5 --out`
    # produced a 2,146,960-byte new plan, no sidecar beside it, and not one imagery entry in
    # must_reverify. Two things were wrong with that and both are fixed here:
    #
    #   * The bytes. `fetch_plan_imagery.py`'s own docstring measures what they cost a reader --
    #     ~576k tokens for one read of that plan against ~42k for its siblings -- and a replan is a
    #     WRITE, which is the moment the split is supposed to happen. resolve_plan_imagery's
    #     docstring already says so: a read has no business rewriting the file it read, so the
    #     inline payload is migrated "on the next write instead". This is that write. The payload
    #     goes beside --out under the new plan's own stem, exactly where a sidecar plan's does, so
    #     ONE code path serves both and render_final_trip_html.py and save_trip_deliverables.py
    #     find it by the same rule they already use.
    #   * The silence. Seasonality and positional slot keys are facts about photographs, not about
    #     which file they sit in, so the pre-split plan needs the same must_reverify entry.
    #
    # Without --out there is nowhere to put a sidecar, and the two cases part company there. A
    # plan that NAMES a sidecar still refuses -- copying a relative name into a plan going to an
    # unknown redirect names a file that is not beside it, which both consumers must refuse. A
    # plan carrying the payload INLINE does not refuse: the bytes are in the document itself, so
    # whatever the redirect lands on is self-contained and readable by both consumers. Refusing it
    # would break a flow that works today to save bytes the operator can save by passing --out,
    # which the note printed at the end tells them.
    inline_imagery = plan.get("imagery")
    declared_sidecar = plan.get("imagery_sidecar")
    names_sidecar = isinstance(declared_sidecar, str) and bool(declared_sidecar.strip())
    # `is not None` rather than a truth test, so a plan whose `imagery` is a string, a list, or any
    # other shape no renderer can read still reaches resolve_plan_imagery and is refused by name.
    # Skipping it would copy the broken shape into the new plan and hand the failure to whoever
    # opens it next.
    payload, new_sidecar, kept_inline = None, None, False
    if names_sidecar or inline_imagery is not None:
        if names_sidecar and not args.out:
            _refuse("this plan's photographs are in a sidecar, and the new plan is going to stdout.",
                    "`imagery_sidecar` is a name relative to the plan, so a plan with no path of "
                    "its own cannot say where its photographs are -- and a copy of the key would "
                    "name a file that is not beside wherever you redirect this.",
                    "Pass --out <new.json>: the payload is copied beside it under the new plan's "
                    "own stem and the key is rewritten to match.")
        try:
            carried_imagery, _source = resolve_plan_imagery(plan, args.plan)
            new_sidecar = sidecar_path_for(args.out) if args.out else None
        except ImagerySidecarError as exc:
            _refuse(f"this plan's photographs could not be read: {exc}",
                    "A replan cannot carry photographs it cannot open, and writing the new plan "
                    "with the key copied over would hand you a plan both consumers refuse.",
                    "Rebuild them with `python scripts/fetch_plan_imagery.py <plan.json>`, or "
                    "delete the 'imagery_sidecar' key if this plan is meant to carry none.")
        # The photograph sentence, shared by both destinations because it is about the frames and
        # not about the file they live in. Only the path it is filed under differs.
        def _imagery_finding(count: int) -> str:
            return (
                f"{count} photograph(s) were carried onto the new dates unchanged. They are "
                f"still OF the same places -- the delta moved no venues -- but what is IN them is "
                f"not date-free: a frame shot in one season shows light, foliage and crowds the "
                f"traveller will not meet in another, and the licence and author printed beside "
                f"each one were checked against the old plan's slots. Look at every image against "
                f"the new "
                f"{'window ' + new_start.isoformat() + '..' + new_end.isoformat() if delta else 'plan'}"
                f", and if re-verification adds, removes or reorders any anchor, re-run "
                f"`python scripts/fetch_plan_imagery.py <plan.json>`: slot keys are positional, so "
                f"a changed anchor list moves every later photograph under a heading it is not of")

        if not carried_imagery:
            # A reference to no photographs: an empty inline dict, or a sidecar file holding `{}`.
            # Both keys are dropped rather than reproduced, because writing an empty sidecar and a
            # key pointing at it manufactures a payload of record where there is none -- and the
            # next tool to see that key would report a plan whose photographs went missing. Said
            # out loud so a key disappearing is never something the operator finds later.
            dropped_keys = [key for key in ("imagery", "imagery_sidecar") if key in plan]
            for key in dropped_keys:
                plan.pop(key, None)
            if dropped_keys:
                print(f"note: {' and '.join(dropped_keys)} named no photograph at all, so the new "
                      f"plan carries neither key rather than a reference to an empty payload.",
                      file=sys.stderr)
        elif args.out:
            # Dropped from the new plan for the same reason fetch_plan_imagery.py drops it: the
            # bytes are in the file named on the next line, and a copy inline is the 2MB plan all
            # over again. This is also the line that MIGRATES a pre-split plan -- `imagery` goes
            # out, `imagery_sidecar` comes in -- so the shifted plan is the small document every
            # gate, verifier and reader was promised.
            payload = carried_imagery
            plan.pop("imagery", None)
            plan["imagery_sidecar"] = new_sidecar.name
            findings.add("imagery_sidecar", _imagery_finding(len(payload)))
        else:
            # Inline, to stdout. The payload stays exactly where it already is -- resolve returns a
            # copy, and rewriting the key with it would only churn the file -- and the entry is
            # filed under `imagery`, the field that actually holds them in THIS output. A path in
            # must_reverify has to resolve in the plan it ships with (see _leaves), and
            # `imagery_sidecar` would not: this plan has no sidecar.
            kept_inline = True
            findings.add("imagery", _imagery_finding(len(carried_imagery)))

    plan["generated_at"] = today.isoformat()

    # A synthesised request describes the flags, not the traveller. It is a placeholder, and the
    # change log says so -- replan_context.change_request is the only record of what was actually
    # asked for, and "shift +1 day" does not say whether the wedding moved or the flight was
    # cancelled.
    if args.change_request:
        request = args.change_request
    else:
        parts = []
        if delta:
            parts.append(f"move the trip window {delta:+d} day(s)")
        if args.travellers is not None and args.travellers != old_travellers:
            parts.append(f"party {old_travellers} -> {args.travellers}")
        if args.cap is not None and old_cap != args.cap:
            parts.append(f"budget cap {old_cap} -> {args.cap:g}")
        request = "; ".join(parts)

    plan["replan_context"] = {
        "replanned_from": Path(args.plan).name,
        "replanned_at": today.isoformat(),
        "change_request": request,
        "changed_fields": [path for path, _ in changes],
        "retained_note": (
            f"Route order, stop selection, segment modes, fare bases, accommodation and venue "
            f"choices, and the {span}-day structure are unchanged: none of them is a function of "
            f"the calendar, and the traveller asked for a different date, not a different trip. "
            f"Day numbering and every ticket/anchor day link were re-derived from the dates rather "
            f"than re-typed."),
        "must_reverify": findings.entries(),
    }

    # --- output --------------------------------------------------------------------------------
    text = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        # Photographs first, plan second -- fetch_plan_imagery.py's ordering and its reason: a
        # failure here leaves an orphan sidecar that nothing points at, while the other order
        # leaves a new plan naming a file that does not exist, which every reader must refuse.
        if payload is not None:
            try:
                write_json_atomic(new_sidecar, payload)
            except OSError as exc:
                _refuse(f"could not write the photographs to {new_sidecar}: {exc}",
                        "The new plan names that file, so writing the plan without it would "
                        "produce a plan both consumers refuse to read.",
                        "Choose a writable --out directory.")
        try:
            Path(args.out).write_text(text, encoding="utf-8")
        except OSError as exc:
            _refuse(f"could not write {args.out}: {exc}", "Choose a writable path.")
    else:
        sys.stdout.write(text)

    _print_change_log(args, plan, delta, old_start, old_end, new_start, new_end, span,
                      changes, skipped, link_warnings, prose_groups, findings,
                      old_status, old_report, carried, closures)
    # Said out loud, after the change log, because a second file was written that the operator did
    # not name on the command line. A file that appears without being asked for is a file somebody
    # will later find and not recognise.
    if payload is not None:
        print(f"\nPHOTOGRAPHS  {len(payload)} slot(s) copied to {new_sidecar}", file=sys.stderr)
        print(f"  the new plan's imagery_sidecar now names {new_sidecar.name}; the source plan "
              f"still points at its own payload and is untouched.", file=sys.stderr)
    return 0


def _print_change_log(args, plan, delta, old_start, old_end, new_start, new_end, span,
                      changes, skipped, link_warnings, prose_groups, findings,
                      old_status, old_report, carried, closures) -> None:
    """The three things SKILL.md section 5 promises a replan returns: what changed, what was
    retained, and what must be re-verified. Printed to stderr so `> new.json` still works, and
    printed in full: a summary that hides the field list is how a hand-redone weekday map got
    trusted in the first place."""
    out = sys.stderr
    destination = args.out or "(stdout)"
    print(f"REPLAN  {Path(args.plan).name}  ->  {destination}", file=out)
    if delta:
        print(f"  window   {old_start}..{old_end}  ->  {new_start}..{new_end}  "
              f"({span} days, unchanged)", file=out)
        print(f"  weekdays {_weekday_name(old_start)}..{_weekday_name(old_end)}  ->  "
              f"{_weekday_name(new_start)}..{_weekday_name(new_end)}"
              + ("   <- every weekday-keyed fact below is now a guess"
                 if delta % 7 else "   (whole weeks: weekdays unchanged)"), file=out)

    print(f"\nCHANGED  {len(changes)} field(s), each mechanically derived from the request", file=out)
    for path, how in changes:
        print(f"  {path:<58} {how}", file=out)
    print(f"  {'verification_status':<58} {json.dumps(old_status)} -> null", file=out)
    print(f"  {'verification_report':<58} {json.dumps(old_report)} -> null "
          f"(it certified the old plan)", file=out)
    for line in skipped:
        print(f"  not shifted: {line}", file=out)

    if closures:
        # First, before the field list, because this is the class that ends a day rather than
        # merely dating it.
        print(f"\nCLOSED ON THE NEW DAY  {len(closures)} -- the plan's own text refutes the "
              f"shifted schedule", file=out)
        for line in closures:
            print(f"  * {line}", file=out)

    print("\nRETAINED  untouched, and still valid", file=out)
    print(f"  {span} day cards in the same order, numbered 1..{span}; every ticket day_number and "
          f"anchor planned_day re-derived", file=out)
    print("  from the dates rather than re-typed -- that hand re-typing is the off-by-one "
          "references/research-budget.md records.", file=out)
    print("  Route order, stops, segment modes, fare bases, venue and accommodation choices, "
          "budget rows: unchanged.", file=out)
    for warning in link_warnings:
        print(f"  WARNING: {warning}", file=out)

    entries = findings.entries()
    print(f"\nMUST RE-VERIFY  {len(entries)} entr{'y' if len(entries) == 1 else 'ies'} written to "
          f"replan_context.must_reverify", file=out)
    if carried:
        print(f"  ({carried} carried over unresolved from the previous replan)", file=out)
    for position, entry in enumerate(entries):
        print(f"  [{position}] {entry['path']}", file=out)
        print(f"       {entry['reason']}", file=out)
    if prose_groups:
        total = sum(len(v) for v in prose_groups.values())
        print(f"\n  {total} of those are prose fields, never rewritten by this script. "
              f"Each is listed by path inside its entry.", file=out)

    print(f"\nNEXT", file=out)
    print(f"  1. Fix or re-research each must_reverify entry, then set its \"resolved\": true and "
          f"write what you found in \"resolution\".", file=out)
    # `--no-verification-yet` and not a bare invocation, which is what this line printed until the
    # flag became mandatory. A bare call now exits 1 out of argparse having run ZERO of the checks,
    # and it exits 1 for the same reason an open must_reverify entry does -- so a caller reading
    # the exit code could not tell "the gate refused your plan" from "the gate never ran", and step
    # 2 silently stopped being the step it says it is. The waiver is right here rather than a
    # report path: this plan's verification was just cleared two hundred lines above, so there is
    # no report to name, and step 3 is where one gets made.
    print(f"  2. python scripts/check_plan_consistency.py {destination} --no-verification-yet   "
          f"# refuses while any entry is open", file=out)
    print(f"  3. Re-run the five-domain verification (references/verification.md) and save with "
          f"scripts/save_trip_deliverables.py.", file=out)
    if not args.change_request:
        print("\n  NOTE: replan_context.change_request was synthesised from the flags. Replace it "
              "with the traveller's own words -- it is the only record of what they actually "
              "asked for.", file=out)
    print("  NOTE: replan_context.retained_note is a default. Say what YOU deliberately kept and "
          "why it is still valid.", file=out)


if __name__ == "__main__":
    raise SystemExit(main())
