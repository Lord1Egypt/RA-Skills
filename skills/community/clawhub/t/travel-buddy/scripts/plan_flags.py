#!/usr/bin/env python3
"""The HTML gate settings, derived from the plan instead of chosen by hand.

Every setting in this file used to be a command-line flag a model picked per run, and four of
them defaulted to off. `validate_trip_html.py page.html` printed "VALID: booking-ready HTML
structure passed." and exited 0 with the day-count check, the booking-type check, the car-link
rule and the "not fact-checked" banner check all disarmed at once -- and an exit 0 is what an
assistant reads. Worse, three of the four were derivable from JSON keys SKILL.md never names
(trip.arrival_transport_mode, booking_options.attraction_tickets, booking_options.ground_transport),
so arming them by hand required knowing to go looking for fields no document mentions. The banner
flag was never named in a single .md file in this repository.

This module is the one definition of that derivation. It lives in its own file rather than in
either caller because save_trip_deliverables.py already does
`from validate_trip_html import validate as validate_html` -- so putting the helper in
save_trip_deliverables.py and importing it from validate_trip_html.py is an import cycle, and the
failure would land on whoever ran the validator directly, as an ImportError out of a
half-initialised module rather than anything about travel plans. save_trip_deliverables.py's own
comment on the booking-type list already called it "the same list, kept in step by hand in three
files". This is the file where it stops being three.

Everything here refuses loudly. A deriver that quietly substitutes a plausible default for a
malformed plan rebuilds the exact defect it was written to delete: the old flags were dangerous
precisely because "nobody said anything" and "nothing is required here" were indistinguishable
from outside. A plan this module cannot read is a plan whose gate settings nobody knows, and that
has to look different from a plan that needs no gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import json

# The closed enum render_final_trip_html.validate_plan already enforces
# ("transport_preference.mode must be self-drive or public-transit"), repeated here because this
# module is reachable without that gate: `validate_trip_html.py --plan` reads a plan straight off
# disk. It matters more than it looks. validate_trip_html.py keys BOTH car rules off equality with
# these two strings -- self-drive requires a rental-car link, public-transit forbids one -- so a
# plan carrying "mixed", "rail", "" or None does not get a different rule, it gets neither rule,
# silently. That is the same shape as the opt-in defaults this whole change exists to remove, so
# an unrecognised mode is refused rather than passed through.
ALLOWED_TRANSPORT_MODES = ("public-transit", "self-drive")

# The other closed enum this module reads, and it was missed on the first pass for an instructive
# reason: `transport_preference.mode` got its guard because BOTH car rules key off equality with
# its two strings, so a wrong value visibly turns two rules off. `arrival_transport_mode` looked
# safer because only one rule keys off it -- and that is exactly what makes it worse. A wrong value
# here does not turn a rule off in a way anyone notices; it answers "does this trip need a flight
# booking card?" with "no", which is the same answer a rail trip gives. Measured: with the bare
# `== "flight"` test, a flight plan written "air", "Flight" or "" derived `hotel` alone, the
# flight-link check never ran, and the page printed VALID carrying no flight card at all. The
# renderer's validate_plan does enforce this enum -- but `validate_trip_html.py --plan` reads a
# plan straight off disk without it, which is the whole reason this module repeats both lists.
ALLOWED_ARRIVAL_MODES = ("flight", "rail", "road", "other")

# The booking-link type that is required of every trip regardless of what the plan says. Kept as a
# named constant so the answer to "why does a plan with no booking_options still require one link"
# is readable at the point it is applied.
ALWAYS_REQUIRED_BOOKING_TYPES = ("hotel",)


class PlanFlagsError(ValueError):
    """A plan whose gate settings cannot be derived.

    Separate from ValueError so callers can catch exactly this and print a plan-shaped message
    instead of a traceback, and so a genuine bug in this module (a TypeError, an AttributeError)
    is never mistaken for "the plan was malformed" and swallowed by the same handler.
    """


@dataclass(frozen=True)
class HtmlFlags:
    """What validate_trip_html.validate() must be told, for one specific plan.

    Frozen because these are the armed checks. A caller that mutates one after deriving it has
    reintroduced hand-tuning through the back door, and the whole point of the type is that the
    plan is the only thing that decides.
    """

    expected_days: int
    required_booking_types: frozenset[str]
    transport_mode: str
    require_unverified_banner: bool
    # Not a gate setting -- the one field here that exists to check the PAIRING rather than the
    # page. `--plan` derives four checks from a plan the operator named on the command line, and
    # nothing established that the plan and the page were the same trip: `validate_trip_html.py
    # tripA.html --plan tripB.json` printed VALID, having compared the page against another trip's
    # day count, booking types, transport mode and verification status, and printed "derived from
    # plan: ..." as though the two had been checked against each other. Two trips open at once, or
    # one stale path in a wrapper, is all it takes. A flag whose whole purpose is "derive the truth
    # from the plan" has to establish first that it is holding the right plan.
    trip_title: str
    # Not read from the plan like the other four -- true whenever a plan was supplied at all.
    # SUPERSEDED, kept because it records what this field was for: "save_trip_deliverables.py
    # stamps every page it renders, so a page with no stamp beside a plan being delivered was
    # assembled by hand, which is the one thing SKILL.md forbids outright." The field is gone
    # because the stamp cannot carry that weight -- it is rendered from `plan["gates_passed"]`, a
    # key an author types, so a hand-assembled plan stamps its own forgery, while every page from
    # this repo's own renderer and every already-delivered page carries no stamp at all. It stayed
    # a note in validate_trip_html.py; the comment there records the measurement.
    # Every jurisdiction the plan answers entry for, each owed its own row on the page. Defaulted,
    # so the manual-flag path -- which has no plan to read it from -- needs no new flag, and every
    # caller that builds HtmlFlags without it keeps working.
    entry_jurisdictions: tuple[str, ...] = ()

    def summary(self) -> str:
        """One line naming every check this plan arms, printed by the validator before it runs.

        The defect being fixed was invisibility: four checks could be off and the output said
        nothing about it. Deriving them correctly and still printing nothing would fix the flags
        and keep the silence, so the armed set is stated out loud on every run.
        """
        types = ", ".join(sorted(self.required_booking_types)) or "none"
        entry_rows = (f"; entry rows required: {', '.join(self.entry_jurisdictions)}"
                      if self.entry_jurisdictions else "")
        return (
            f"derived from plan: {self.expected_days} day card(s); "
            f"booking types required: {types}; transport mode: {self.transport_mode}; "
            f"unverified banner: {'required' if self.require_unverified_banner else 'not required'}"
            f"{entry_rows}"
        )


def _describe(value: object, present: bool) -> str:
    """How to name a bad value in a refusal: absent and null are different mistakes.

    "got NoneType" is what a missing key and an explicit null both used to read as, and they need
    different fixes -- one is a field nobody filled in, the other is a field somebody blanked.
    """
    return type(value).__name__ if present else "no such key"


def _mapping(container: dict, key: str, plan_label: str, *, optional: bool = False) -> dict:
    """Return container[key] as a dict or refuse, naming the key that was wrong.

    `plan.get("booking_options", {}).get("attraction_tickets")` -- the line this replaces -- raises
    AttributeError on a plan whose booking_options is a list, which is a stack trace naming
    'list' and no JSON key. The traveller-facing cost of that is nil; the cost is that whoever
    hits it cannot tell a broken plan from a broken script.

    `optional` covers the one key that is legitimately allowed to be absent. It means absent or
    null, and nothing else. The first version of this wrote `plan.get("booking_options") or {}`,
    which is the same shape and reads the same way -- and an adversarial probe caught it exiting 0
    on `"booking_options": []`, because an empty list is falsy, so a wrong TYPE was silently
    rewritten into "this trip books nothing" and the ticket and ground checks came off. That is
    precisely the defect this module exists to delete, rebuilt inside the deleter by an `or`.
    """
    if optional and container.get(key, None) is None:
        return {}
    value = container.get(key)
    if not isinstance(value, dict):
        raise PlanFlagsError(
            f"{plan_label}: {key} must be a JSON object, got "
            f"{_describe(value, key in container)}. The HTML gate settings are read from it, so "
            f"they cannot be derived from this plan.")
    return value


def derive_html_flags(plan: object, plan_label: str = "plan") -> HtmlFlags:
    """Derive every HTML gate setting from the plan itself.

    plan_label names the file in every refusal, because both callers reach this with a plan the
    operator chose by path and "plan: days must be a non-empty list" is unactionable when three
    plans are open.
    """
    if not isinstance(plan, dict):
        raise PlanFlagsError(
            f"{plan_label}: the plan must be a JSON object, got {type(plan).__name__}. The HTML "
            f"gate settings are read from it, so they cannot be derived from this plan.")
    doc = plan
    trip = _mapping(doc, "trip", plan_label)

    days = doc.get("days")
    if not isinstance(days, list) or not days:
        raise PlanFlagsError(
            f"{plan_label}: days must be a non-empty list; got "
            f"{_describe(days, 'days' in doc)}"
            f"{' of length 0' if isinstance(days, list) else ''}. The day-count check compares the "
            f"page against this length, and a plan with no days cannot say how many cards the page "
            f"owes.")
    expected_days = len(days)

    transport = _mapping(doc, "transport_preference", plan_label)
    mode = transport.get("mode")
    if mode not in ALLOWED_TRANSPORT_MODES:
        raise PlanFlagsError(
            f"{plan_label}: transport_preference.mode is {mode!r}; it must be one of "
            f"{', '.join(ALLOWED_TRANSPORT_MODES)}. Both car-link rules are keyed on equality with "
            f"those two strings, so any other value does not select a different rule -- it turns "
            f"both of them off without saying so.")

    # Truthiness, not presence, and deliberately identical to the three lines this lifted from
    # save_trip_deliverables.py. An empty list under attraction_tickets means the plan researched
    # no ticketed attraction; requiring a ticket link for it would fail every museum-free trip.
    required = set(ALWAYS_REQUIRED_BOOKING_TYPES)
    # The renderer prints this verbatim as the page's only <h1>, so it is the binding marker that
    # already exists on every delivered page, including the ones saved before this check did. A new
    # data- attribute would have been cleaner to parse and would have failed every page in a real
    # workspace on the day it shipped.
    title = trip.get("title")
    if not isinstance(title, str) or not title.strip():
        raise PlanFlagsError(
            f"{plan_label}: trip.title is {_describe(title, 'title' in trip)}; it must be a "
            f"non-empty string. It is what identifies this plan to the page being validated, so "
            f"without it there is no way to tell that the two describe the same trip.")

    arrival = trip.get("arrival_transport_mode")
    if arrival not in ALLOWED_ARRIVAL_MODES:
        raise PlanFlagsError(
            f"{plan_label}: trip.arrival_transport_mode is {arrival!r}; it must be one of "
            f"{', '.join(ALLOWED_ARRIVAL_MODES)}. Only 'flight' requires a flight booking card, so "
            f"any other spelling of it -- 'air', 'Flight', an empty string, a missing key -- does "
            f"not ask a different question, it answers this one with 'no flight card needed' and "
            f"the page ships without the largest purchase on the trip.")
    if arrival == "flight":
        required.add("flight")
    booking_options = _mapping(doc, "booking_options", plan_label, optional=True)
    if booking_options.get("attraction_tickets"):
        required.add("ticket")
    # Carried verbatim from save_trip_deliverables.py, which is where this line used to live and
    # where it named its own problem:
    #
    #   "The same list, kept in step by hand in three files. Harmless today because validate_plan
    #   already forces the button on every ground option -- but that is a reason this line is
    #   cheap, not a reason to leave the third copy behind when the first two moved."
    #
    # This is the move it was asking for. There is one copy now, and both callers import it.
    if booking_options.get("ground_transport"):
        required.add("ground")

    # Carried verbatim from the call site in save_trip_deliverables.py:
    #
    #   "The banner is the only place an unverified plan announces itself to the person actually
    #   booking. Asserted here rather than trusted, because this is the exact point where the JSON
    #   gap and the page's silence would diverge."
    #
    # Anything that is not exactly "verified" requires the banner, including a typo, a None and a
    # bool. That asymmetry is on purpose: the failure it protects against is a page that is silent
    # about never having been fact-checked, so every ambiguous status has to fall toward showing
    # the warning. A plan really is verified only when it says so exactly. Measured on the 15
    # plans in a real workspace: 8 carry no verification_status key at all and 9 require the
    # banner. This is the branch that fires on the majority of real plans, not the exceptional
    # one -- which is exactly how much traveller-facing warning a default-off flag was suppressing.
    require_unverified_banner = doc.get("verification_status") != "verified"

    entry = doc.get("entry_context") if isinstance(doc.get("entry_context"), dict) else {}
    records = entry.get("per_jurisdiction") if isinstance(entry.get("per_jurisdiction"), list) else []
    entry_jurisdictions = tuple(
        str(record["jurisdiction"]).strip() for record in records
        if isinstance(record, dict) and isinstance(record.get("jurisdiction"), str)
        and record["jurisdiction"].strip())

    return HtmlFlags(
        expected_days=expected_days,
        required_booking_types=frozenset(required),
        transport_mode=mode,
        require_unverified_banner=require_unverified_banner,
        trip_title=title,
        entry_jurisdictions=entry_jurisdictions,
    )


def load_html_flags(plan_path: str | Path) -> HtmlFlags:
    """Read a plan JSON from disk and derive its gate settings.

    The read is here rather than in the validator so that both a missing file and an unparseable
    one refuse with the same plan-shaped wording as a malformed one, through the same exception
    type. A caller that has to catch OSError, JSONDecodeError and PlanFlagsError separately ends
    up catching two of the three and letting the last one print a traceback.
    """
    path = Path(plan_path)
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise PlanFlagsError(f"could not read plan {path}: {exc}") from exc
    try:
        plan = json.loads(raw)
    except ValueError as exc:
        raise PlanFlagsError(f"plan {path} is not valid JSON: {exc}") from exc
    return derive_html_flags(plan, plan_label=str(path))


def stay_sequence(plan: object) -> list[dict]:
    """The trip's spine: where the traveller sleeps, in order, with the nights in each place.

    Derived, never declared. A multi-stop trip already carries everything this needs -- one
    `stay_group_id` per stop, each option's `check_in`/`check_out`, and a `stay_location` -- so
    asking the author to also write a summary of it would create a second copy to drift against
    the first. That is the same reason `derive_html_flags` exists one screen up.

    `base_location` is deliberately not consulted. It is free text and was found meaning "where
    today's activities are" on one delivered plan (four spellings, one hotel) and "where I sleep"
    on another, so a spine built from it would show four stops for a trip that never moved.

    Returns [] when the plan has fewer than two stay groups: a single-base trip has no sequence to
    show, and rendering a one-item spine would be furniture.
    """
    options = []
    if isinstance(plan, dict):
        booking = plan.get("booking_options")
        if isinstance(booking, dict) and isinstance(booking.get("accommodations"), list):
            options = [o for o in booking["accommodations"] if isinstance(o, dict)]

    groups: dict[str, dict] = {}
    for option in options:
        group = str(option.get("stay_group_id") or "").strip()
        if not group:
            continue
        try:
            start = date.fromisoformat(str(option.get("check_in")))
            end = date.fromisoformat(str(option.get("check_out")))
        except (TypeError, ValueError):
            continue
        if end < start:
            # A checkout before its check-in is a malformed window, and render_final_trip_html
            # refuses the plan for it. Skipping here keeps the spine from printing "-3 晚", which
            # is not a number a page should ever show; the gate that owns the field does the
            # complaining.
            continue
        entry = groups.setdefault(group, {"group_id": group, "check_in": start, "check_out": end,
                                          "labels": [], "option_count": 0})
        entry["check_in"] = min(entry["check_in"], start)
        entry["check_out"] = max(entry["check_out"], end)
        entry["option_count"] += 1
        label = str(option.get("stay_location") or "").strip()
        if label and label not in entry["labels"]:
            entry["labels"].append(label)

    if len(groups) < 2:
        return []
    spine = sorted(groups.values(), key=lambda g: (g["check_in"], g["check_out"]))
    for entry in spine:
        # The shortest label among the options in a group, because two hotels in one place are
        # routinely described at different precisions ("深圳南山区蛇口" and "蛇口海上世界"), and the
        # shorter one is the place they share rather than one property's address.
        entry["label"] = min(entry["labels"], key=len) if entry["labels"] else entry["group_id"]
        entry["nights"] = (entry["check_out"] - entry["check_in"]).days
    return spine


# The spellings that mean "the map rule for mainland China applies here". Explicit, and short on
# purpose: `destination_service_market` is free text and fifteen saved plans spell it nine ways, so
# a fuzzy match would be guessing about the one market whose links break when guessed wrong. A day
# whose jurisdiction is not in this set and not recognisably elsewhere keeps the trip-wide rule --
# see day_service_market, which fails strict rather than open.
MAINLAND_CHINA_MARKETS = frozenset({"mainland_china", "中国大陆", "中国内地", "mainland china"})


def is_mainland_market(value: object) -> bool:
    return str(value or "").strip().casefold() in MAINLAND_CHINA_MARKETS
