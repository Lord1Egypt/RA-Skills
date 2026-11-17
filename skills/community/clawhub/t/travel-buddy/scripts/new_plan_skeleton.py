#!/usr/bin/env python3
"""Emit a structurally valid final-trip-plan skeleton, so authoring fills content not structure.

Usage:
  python new_plan_skeleton.py --start 2026-09-11 --end 2026-09-14 \
      --origin "阿姆斯特丹" --destination "马拉加" --language zh --currency EUR \
      --travellers 1 --mode public-transit --stops-per-day 4 > plan.json

  python new_plan_skeleton.py --from-intake <workspace>/plans/intake-<stamp>-<slug>.json > plan.json

WHY THIS EXISTS
---------------
`templates/final-trip-plan.json` lists every field but cannot express the rules that relate them,
so an author discovers those by failing the renderer. Measured on one real run, the first render
returned 21 errors and every one was structural, not factual:

  * segments must mirror consecutive pairs in stops_in_order, exactly, by string equality --
    a stop written "老城 Calle Larios 街区" and a segment ending "老城 Calle Larios 街区（午餐）"
    is a mismatch;
  * `service_or_line` must be non-empty even on a walking leg;
  * booking-access categories are `attraction_ticket` / `rail_or_ground`, not the budget
    spellings `attractions` / `local_transport`;
  * a departure day still needs a breakfast card;
  * two flight candidates must not share a review_url.

Three edit-render round-trips went into rediscovering that. This script encodes it once: the
skeleton it prints renders on the first try, so the whole of that loop is spent on facts.

IT CANNOT BE SHIPPED HALF-FILLED
--------------------------------
Free-text values an author must supply are the string "TODO: ...". Those survive rendering --
the renderer only requires fields to be non-empty -- and are then rejected by
`validate_trip_html.py`, which fails any page still carrying a TODO. So the skeleton speeds up
authoring without becoming a way to deliver a hollow page.

Typed fields cannot hold that prose, so they take type-valid sentinels. URLs keep the property:
https://example.invalid/TODO-... is HTTPS enough for the renderer, still trips the TODO scan,
and can never resolve, so `check_link_targets.py` objects too. Dates do not: 1970-01-01 is
conspicuous on the page but no gate rejects it. Neither does `on_foot_minutes: 0`, which is
indistinguishable from an author who measured the day and found no walking in it. Those two are
the holes in this design, and they are stated rather than papered over -- check every
`checked_at`, and every activity's on-foot minutes, before delivery.

A third hole was the same shape and worse, because it paid. `allergy_severity: "none"` and
`max_continuous_walking_minutes: null` are not sentinels at all: they are answers, and they were
being written by a script that cannot know either one. Measured on a real five-day plan, with
those defaults untouched, deleting EVERY activity's `on_foot_minutes` changed the finding count
from 2 to 2 -- every walking check no-ops when the cap is null -- while the same deletion against a
typed cap of 25 produced five precise findings. And SKILL.md allows the light verification tier
only when the severity is none/preference AND the cap is null, so those two defaults were also
exactly what bought the cheaper pass: never typing them switched the walking checks off and
skipped four verification domains at once. Neither field can hold a TODO string (validate_plan
would refuse to render the skeleton at all), so the marker lives beside them in
`trip.traveler_constraints[UNTYPED_CONSTRAINTS_MARKER]`, one entry per untyped field, and
`check_untyped_constraints` refuses the plan until the author deletes it. That is a hole closed,
not another one stated.

--from-intake
-------------
The traveller already answered these questions once. Copying their answers by hand is where they
get lost: the measured run planned from the wrong origin city and a superseded budget cap while
both sat correct in the intake file, and `budget.cap_per_person` -- hardcoded None here until now
-- meant the cap-overrun check silently passed every skeleton-produced plan, so nothing objected.
`--from-intake` copies the mapped fields and prints every one of them to stderr, because a copy
nobody sees is how the wrong city survived a whole planning run. Command-line flags still win: an
operator naming a value on the command line is correcting the file, which is the one case where
the file is not the authority.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

# The gate owns the name of the marker this script writes, and this script imports it rather than
# restating the string. save_trip_deliverables.py learned the same lesson about its copy of the
# check list: a duplicated constant is a gate that silently falls behind, and here the failure
# would be the quietest kind -- the skeleton writing `untyped_constraints` while the checker reads
# `untyped_constraint`, every test in the suite green, and the marker never firing on a real plan.
# Python puts the script's own directory on sys.path, which is how save_trip_deliverables.py
# imports the same module when run as `python scripts/...`.
from check_plan_consistency import UNTYPED_CONSTRAINTS_MARKER
from intake_language import normalize_language

TODO = "TODO: "
# Typed fields cannot hold prose, so they get type-valid sentinels instead. The URL sentinel is
# chosen so three separate gates still object: it is HTTPS (renderer accepts it), it contains
# TODO (validate_trip_html rejects the page), and .invalid is a reserved TLD that can never
# resolve (check_link_targets reports it). The date sentinel has no such backstop -- 1970 is
# merely conspicuous on the page -- and that is a stated limit, not an oversight.
URL = "https://example.invalid/TODO-replace-with-a-researched-url"
DATE = "1970-01-01"

# The third sentinel, and the one the two above could not express. `allergy_severity` and
# `max_continuous_walking_minutes` are the fields the walking and dining gates MEASURE, and this
# script cannot know either: the intake form collects both as prose and nothing turns a sentence
# into an enum or a number. Neither field can hold a TODO string -- validate_plan requires the
# severity to be an ALLERGY_SEVERITIES member or null and the cap to be a positive whole number or
# null, so prose in either one stops the skeleton rendering at all, and the enum's "must be one of:
# none, preference, intolerance, severe" would then be reported about a placeholder, which reads as
# a typo rather than as an unanswered question. Null cannot carry the meaning either: for the cap,
# null IS the documented answer "the traveller stated no limit".
#
# So the marker sits beside them, keyed by the field it stands for and carrying the same TODO prose
# every other unfilled value here carries. Deleting an entry is how an author says they typed that
# field; check_untyped_constraints refuses the plan until both are gone, and required_domains_for
# refuses the light verification tier while either remains.
UNSET_CONSTRAINTS = {
    "allergy_severity": (
        f"{TODO}type the traveller's allergy severity -- none | preference | intolerance | severe "
        f"-- from their own words, then delete this entry. 'none' asserts there is nothing to "
        f"avoid, so it has to be a claim somebody made rather than the value that was here."),
    "max_continuous_walking_minutes": (
        f"{TODO}type the minutes the traveller said they can walk at a stretch, or set the field "
        f"to null if they stated no limit, then delete this entry. Null switches every per-leg and "
        f"per-activity walking check off: measured on a real five-day plan, deleting every "
        f"activity's on_foot_minutes changed the finding count from 2 to 2 with the cap null, and "
        f"produced five precise findings with it typed as 25."),
}

# Which intake flag each required trip field can arrive from, named in the error when neither the
# flag nor the file carries it. "--start is required" sends the operator back to the command line;
# naming the intake key sends them to the file that already has the answer.
REQUIRED_FROM_INTAKE = {
    "--start": "travel_window.start_date",
    "--end": "travel_window.end_date",
    "--origin": "origin.home_city",
    "--destination": "destination_scope.named_places[0]",
}


class IntakeError(Exception):
    """A --from-intake file that cannot be used. Carries the sentence the operator reads."""


def dig(node, *path):
    """Read intake[a][b]. A missing key, a null, and a wrongly-shaped parent all mean 'absent'.

    Intake is written by a form the traveller may leave half-answered, so almost every key is
    optional and many that exist are null. Collapsing those three cases into one is what stops
    a partial intake -- the normal kind -- from turning --from-intake into a traceback.
    """
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
    return node


def read_intake(path: str) -> dict:
    """Load an intake file, or raise IntakeError with something the operator can act on."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise IntakeError(
            f"could not read --from-intake file '{path}': {exc.strerror or exc}. Pass the saved "
            f"intake JSON, which start_intake_workflow.py writes to "
            f"<workspace>/plans/intake-<stamp>-<slug>.json.") from exc
    try:
        intake = json.loads(text)
    except json.JSONDecodeError as exc:
        raise IntakeError(
            f"--from-intake file '{path}' is not valid JSON: {exc}. Open it at that line, or "
            f"re-run the intake form to write a fresh one.") from exc
    if not isinstance(intake, dict):
        raise IntakeError(
            f"--from-intake file '{path}' holds a {type(intake).__name__}, not an object. Pass an "
            f"intake JSON, not a plan or a list of them.")
    # A plan, a profile, or a verification report handed here by mistake is valid JSON in which
    # every copy below skips silently, and the run then looks exactly like a traveller who answered
    # nothing -- the same silence this flag exists to end. Refuse instead. The blocks named here
    # are the ones only an intake has: a plan also carries a top-level `budget`, so sniffing for
    # that would wave a plan file straight through.
    if not any(isinstance(intake.get(block), dict)
               for block in ("origin", "travel_window", "party", "destination_scope")):
        raise IntakeError(
            f"'{path}' is valid JSON but does not look like a trip intake: none of origin, "
            f"travel_window, party or destination_scope is an object. Check the path -- an intake "
            f"file is named intake-<stamp>-<slug>.json.")
    return intake


def is_text(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_count(value) -> bool:
    # bool is an int in Python and True would silently become 1 traveller.
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def is_amount(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def text_list(value) -> list[str]:
    return [item.strip() for item in value if is_text(item)] if isinstance(value, list) else []


def stop_name(day_number: int, index: int, total: int, day_type: str) -> str:
    if day_type == "arrival" and index == 0:
        return f"{TODO}day {day_number} arrival point (airport/station)"
    if day_type == "departure" and index == total - 1:
        return f"{TODO}day {day_number} departure point (airport/station)"
    return f"{TODO}day {day_number} stop {index + 1}"


def english_plan(language: object) -> bool:
    return str(language or "").casefold().startswith("en")


def segment(origin: str, destination: str, english: bool = False) -> dict:
    """Walking legs still need service_or_line; the renderer rejects an empty one.

    In the plan's own language. They were always written 「步行」, and an English page then
    printed 「步行 · 步行（无线路）」 with both gates calling it VALID -- the i18n gate looks for
    English on a Chinese page, never the reverse.
    """
    return {
        "from": origin,
        "to": destination,
        "mode": "walk" if english else "步行",
        "service_or_line": (f'{TODO}line or operator (write "Walk (no line)" for a walking leg)'
                            if english else
                            f"{TODO}line or operator (write 步行（无线路） for a walking leg)"),
        "duration_minutes": 0,
        "distance_km": 0,
        "walking_minutes": 0,
        "transfer_count": 0,
        "cost_low": 0,
        "cost_high": 0,
        "currency": f"{TODO}currency",
        "journey_instruction": f"{TODO}how to board / which way to walk",
        "arrival_instruction": f"{TODO}what the traveller sees on arrival",
        "fare_basis": f"{TODO}fare and its source, or 'walking, no fare'",
        "fallback_note": f"{TODO}what to do if this leg fails",
        # Set only when geography forces a way round far longer than the straight line --
        # a canyon with no crossing, a fjord. Without it such a leg is refused, because
        # nothing else separates a real detour from an endpoint wired to the wrong stop.
        "detour_reason": None,
        "verified_map_url": URL,
        "map_checked_at": DATE,
        "map_provider": f"{TODO}map provider (must own the URL above)",
        "map_link_kind": "directions",
        "alternative_map_links": [],
    }


def dining_card(meal: str, anchor: str) -> dict:
    return {
        "meal": meal,
        "time_window": f"{TODO}HH:MM-HH:MM",
        # Researched, not unverified, because a card that names a seating time is claiming the
        # venue is open then; check_plan_consistency refuses the pair "unverified" + a clock.
        "venue_hours": f"{TODO}Mon-Sun HH:MM-HH:MM (the days it is OPEN)", "venue_hours_by_weekday": None,
        "hours_status": "researched",
        # Opening the venue's map page hands you all five of these in one read, plus the
        # coordinates the route segments need.
        "rating_status": "verified",
        "rating_value": 0,
        "rating_scale": 5,
        "rating_count": 0,
        "rating_source": f"{TODO}where the rating was read",
        "rating_url": f"{TODO}https://…the venue's page on that provider",
        "rating_checked_at": "1970-01-01",
        "rating_absence_reason": None,
        # Only when the score is below the floor and the venue still earns the evening --
        # the one kitchen serving a dietary need, a stall whose reviews are all queue.
        "rating_below_floor_reason": None,
        "venue_name": f"{TODO}venue for {meal}",
        "cuisine_or_style": f"{TODO}cuisine or style",
        "neighborhood": f"{TODO}neighbourhood",
        "route_anchor": anchor,
        "off_route_justification": None,
        "why_this_stop": f"{TODO}why it fits the stop before or after it",
        "price_per_person_low": 0,
        "price_per_person_high": 0,
        "currency": f"{TODO}currency",
        "reservation_or_queue_note": f"{TODO}queue or reservation note",
        "reservation_need": f"{TODO}required | recommended | walk_in | not_accepted",
        "venue_url": URL,
        "map_provider": f"{TODO}map provider (must own venue_url)",
        "checked_at": DATE,
        "reservation_provider": None,
        "reservation_url": None,
        "backup_venue_name": f"{TODO}backup venue",
        "backup_note": f"{TODO}when to switch to the backup",
    }


def build_day(number: int, date: dt.date, day_type: str, stops_per_day: int, mode: str,
              english: bool = False) -> dict:
    total = max(2, stops_per_day)
    stops = [stop_name(number, i, total, day_type) for i in range(total)]
    segments = [segment(stops[i], stops[i + 1], english) for i in range(total - 1)]

    meals = {"arrival": ["dinner"], "departure": ["breakfast", "lunch"]}.get(day_type, ["lunch", "dinner"])
    return {
        "number": number,
        "date": date.isoformat(),
        "day_type": day_type,
        "title": f"{TODO}day {number} title",
        "focus": f"{TODO}what this day is for",
        "base_location": f"{TODO}base location",
        "accommodation_option_id": "acc-1",
        # on_foot_minutes is the time THIS activity is spent on foot or standing. Segment
        # walking_minutes covers only the walk between stops, so a page can truthfully print
        # "42 minutes on foot" for a day that schedules three and a half hours of it inside
        # museums and markets -- that shipped, against a stated mobility limit, and the walking
        # gate certified the number. 0 is the type-valid sentinel and is also a real answer,
        # so unlike a TODO it cannot be detected; measure it before delivery.
        "activities": [
            {"time": "09:00", "name": f"{TODO}day {number} first activity", "detail": f"{TODO}detail",
             "ticket_option_id": None, "meal_or_rest_buffer": None, "on_foot_minutes": 0},
            {"time": "14:00", "name": f"{TODO}day {number} second activity", "detail": f"{TODO}detail",
             "ticket_option_id": None, "meal_or_rest_buffer": None, "on_foot_minutes": 0},
        ],
        "dining": [dining_card(meal, stops[min(1, len(stops) - 1)]) for meal in meals],
        "route": {
            "start": stops[0],
            "stops_in_order": stops,
            "end": stops[-1],
            "mode": mode,
            "route_logic": f"{TODO}why this order",
            "fallback_plan": f"{TODO}what to do if the day breaks",
            "duration_minutes": 0,
            "distance_km": 0,
            "transfer_count": 0,
            # Both totals, in digits: the segments' walking_minutes and the activities'
            # on_foot_minutes. One number for both is how a 3.5-hour day got printed as 42 minutes.
            "walking_burden": f"{TODO}quote both computed walking totals in digits "
                              f"(between stops, and on foot at stops)",
            "cost_low": 0,
            "cost_high": 0,
            "currency": f"{TODO}currency",
            "fare_basis_or_fuel_toll_parking_note": f"{TODO}fare or fuel/toll/parking basis",
            "service_or_driving_caveat": f"{TODO}service caveat",
            "verified_map_url": URL,
            "map_checked_at": DATE,
            "map_provider": f"{TODO}map provider",
            "map_link_kind": "directions",
            "route_map_scope": "multi_stop" if total > 2 else "primary_leg",
            "alternative_map_links": [],
            "segments": segments,
            "schematic_svg": None,
        },
        "contingency": f"{TODO}day-level contingency",
    }


# Where a plan stops being one itinerary and starts being a project. Warn at the first pair,
# refuse past the second unless --oversize says the author means it.
WARN_DAYS, WARN_STOPS = 7, 6
OVERSIZE_DAYS, OVERSIZE_STOPS = 21, 10


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    # These four were required flags. They stay required as values -- the check moved below, so
    # --from-intake can supply them -- and the error names the intake key as well as the flag.
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--origin")
    parser.add_argument("--destination")
    # No argparse default, for the same reason as --currency: "the operator asked for zh" and
    # "nobody said" must stay distinguishable, or zh would outrank the language the traveller chose.
    parser.add_argument("--language", default=None,
                        help="zh or en; default: the intake's preferred_output_language, else its "
                             "form_language, else zh")
    # No argparse default: it has to stay possible to tell "the operator asked for EUR" from
    # "nobody said", or the default would silently outrank the currency the traveller stated.
    parser.add_argument("--currency", default=None,
                        help="default: EUR, or the intake's budget.currency")
    parser.add_argument("--travellers", type=int, default=None,
                        help="default: 1, or the intake's party.traveler_count")
    parser.add_argument("--mode", choices=("public-transit", "self-drive"), default="public-transit")
    parser.add_argument("--stops-per-day", type=int, default=4)
    parser.add_argument("--from-intake", default=None, metavar="INTAKE.JSON",
                        help="copy the traveller's own answers out of a saved intake file")
    parser.add_argument("--oversize", action="store_true",
                        help="Allow a plan past the size limits (see the refusal message for what that costs)")
    parser.add_argument("--intake-method", choices=("html_form", "user_supplied", "chat_fallback"),
                        default=None,
                        help="How the traveller's requirements were collected. --from-intake sets "
                             "html_form on its own; use this only for the other two routes")
    parser.add_argument("--source-note", default=None,
                        help="With --intake-method user_supplied: what the traveller supplied instead")
    parser.add_argument("--declined-verbatim", default=None,
                        help="With --intake-method chat_fallback: the traveller's OWN WORDS "
                             "declining the loopback form")
    parser.add_argument("--declined-at", default=None, metavar="YYYY-MM-DD",
                        help="With --intake-method chat_fallback: the date they declined it. "
                             "Left out, this stays the 1970-01-01 sentinel, which the save gate "
                             "rejects rather than shipping an invented date")
    args = parser.parse_args()

    intake: dict = {}
    if args.from_intake:
        try:
            intake = read_intake(args.from_intake)
        except IntakeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2

    # Each route has to arrive with its own evidence, or it is not that route. chat_fallback is the
    # one the traveller has to authorise, so it needs their words rather than a summary: a
    # paraphrase reads identically whether they declined the form or an assistant never offered it.
    method = args.intake_method or ("html_form" if args.from_intake else None)
    if args.from_intake and method != "html_form":
        print(f"ERROR: --from-intake names the file the intake server writes, so the form WAS "
              f"filled; --intake-method {method} says it was not. Emitting both produced a "
              f"provenance record that contradicts itself, which reads as evidence rather than as "
              f"the gap it is. Drop one of the two flags.", file=sys.stderr)
        return 2
    if method == "html_form" and not args.from_intake:
        print("ERROR: --intake-method html_form needs --from-intake, which names the file the "
              "intake server wrote. Claiming the form ran without the file it produces is the one "
              "thing this field exists to prevent.", file=sys.stderr)
        return 2
    if method == "user_supplied" and not (args.source_note or "").strip():
        print("ERROR: --intake-method user_supplied needs --source-note saying what the traveller "
              "supplied instead of the form.", file=sys.stderr)
        return 2
    if method == "chat_fallback" and not (args.declined_verbatim or "").strip():
        print("ERROR: --intake-method chat_fallback needs --declined-verbatim, the traveller's own "
              "words declining the loopback form. Chat intake is theirs to choose, not yours: it "
              "loses the form server's rejection of document/payment/address fields, its "
              "scope-versus-work-mode check, the profile's never_recommend and dietary prefill, "
              "and the saved intake the shortlist gate reads. If they have not declined it, run "
              "`python scripts/start_intake_workflow.py --assistant auto` in the background "
              "instead.", file=sys.stderr)
        return 2
    intake_context = {
        "method": method,
        "intake_file": str(Path(args.from_intake).resolve()) if args.from_intake else None,
        "source_note": args.source_note,
        "declined_verbatim": args.declined_verbatim,
        # DATE is the epoch sentinel, and here it is deliberately not silent: a made-up date on
        # the record that says the traveller authorised chat intake is a fabricated fact, so
        # intake_context_errors rejects it at save time instead of letting it through the way the
        # skeleton's other date sentinels go through.
        "declined_at": (args.declined_at or DATE) if method == "chat_fallback" else None,
    } if method else None

    report: list[str] = []

    def pick(field: str, source: str, cli_value, valid, expected: str):
        """Resolve one field from the intake and record, for the operator, what happened to it.

        Every outcome except 'the intake never carried it' prints. A silent copy is what let a
        plan get built on the wrong origin city while the right one sat in the file.
        """
        value = dig(intake, *source.split("."))
        if value is None:
            return cli_value
        if not valid(value):
            report.append(f"  {source} -> {field}: NOT copied, expected {expected}, found "
                          f"{value!r}. Fill {field} by hand.")
            return cli_value
        if cli_value is not None and cli_value != value:
            report.append(f"  {source} -> {field}: NOT copied, {cli_value!r} came from the command "
                          f"line and wins (the intake says {value!r}).")
            return cli_value
        report.append(f"  {source} -> {field}: {value!r}")
        return value

    origin = pick("trip.origin", "origin.home_city", args.origin, is_text, "a non-empty string")
    start_text = pick("trip.start_date", "travel_window.start_date", args.start, is_text, "a YYYY-MM-DD string")
    end_text = pick("trip.end_date", "travel_window.end_date", args.end, is_text, "a YYYY-MM-DD string")
    travellers = pick("trip.traveler_count", "party.traveler_count", args.travellers, is_count, "a positive integer")
    currency = pick("trip.currency", "budget.currency", args.currency, is_text, "a currency code")
    cap_per_person = pick("budget.cap_per_person", "budget.hard_cap_amount", None, is_amount, "a positive number")

    # The plan starts in the traveller's language. Since 2026-09-24 the intake records the one they
    # asked for (their profile's preference, else the language they filled the form in) and the
    # form's own; before that this defaulted to zh whatever the file said -- the last place the
    # answer was collected and then dropped. Reported like every other copied field, including
    # when the file is too old to say.
    language = args.language
    if args.from_intake:
        found = None
        for source in ("preferred_output_language", "form_language"):
            raw = intake.get(source) if isinstance(intake, dict) else None
            if raw is None:
                continue
            code = normalize_language(raw)
            if code is None:
                report.append(f"  {source} -> trip.language: NOT copied, expected zh or en, found {raw!r}.")
                continue
            found = (source, code)
            break
        if found and language is not None and normalize_language(language) != found[1]:
            report.append(f"  {found[0]} -> trip.language: NOT copied, {language!r} came from the "
                          f"command line and wins (the intake says {found[1]!r}).")
        elif found:
            language = language or found[1]
            report.append(f"  {found[0]} -> trip.language: {found[1]!r}")
        elif language is None:
            report.append("  trip.language: 'zh' -- the intake records no language (it predates "
                          "2026-09-24); pass --language en for an English plan.")
    language = language or "zh"

    def pick_list(field: str, source: str) -> list[str]:
        """Copy a list of free-text constraints. An empty list is silence; anything else is not.

        A dietary need written as a bare string instead of a list is the shape that must never
        pass quietly -- dropping it produces a plan that asserts the traveller has no allergy.
        """
        value = dig(intake, *source.split("."))
        items = text_list(value)
        if items:
            report.append(f"  {source} -> {field}: {items!r}")
        elif value is not None and value != []:
            report.append(f"  {source} -> {field}: NOT copied, expected a list of strings, found "
                          f"{value!r}. Fill {field} by hand.")
        return items

    # destination_scope.named_places is a list, so it cannot go through pick()'s dotted path.
    destination = args.destination
    named_places = dig(intake, "destination_scope", "named_places")
    places = text_list(named_places)
    if places:
        first = places[0]
        if destination is not None and destination != first:
            report.append(f"  destination_scope.named_places[0] -> trip.destination: NOT copied, "
                          f"{destination!r} came from the command line and wins (the intake says {first!r}).")
        else:
            destination = first
            report.append(f"  destination_scope.named_places[0] -> trip.destination: {first!r}")
            # The one question the intake cannot answer for itself, asked where it is cheap.
            #
            # `destination_scope.state` used to offer "已固定城市/国家" as a single option, which is
            # two different answers -- a settled CITY is a Construction trip, a settled COUNTRY is
            # constrained discovery, and the skill's own work-mode table says so. A real run
            # answered it with the single word 「美国」, the form recorded mode=construction, and
            # the next step would have been an eight-day itinerary for a whole country. The form's
            # wording is fixed; this line is the backstop, because a skeleton is built from a file
            # somebody may have filled in before that fix, or in another language, or wrongly.
            #
            # Deliberately a QUESTION and not a check: deciding whether a string names a country
            # needs a list of every country in every language a traveller might type, and a list
            # like that is only current on the day it is written -- the same losing bet this
            # repository has already made twice with assistant names and tty detection. The author
            # can answer it in one second; no list can.
            # Only an EXPLICIT discovery declaration silences the question. An absent, misspelled
            # or differently-cased mode is not a statement that this is not Construction -- and
            # this script only ever emits a Construction artifact, so silence on the intake's part
            # is a reason to ask rather than a reason to assume. `== "construction"` missed
            # "Construction" and every hand-written intake that omits the field.
            declared = str(intake.get("mode") or "").strip().casefold()
            if declared not in ("discovery", "constrained_discovery"):
                report.append(f"  CHECK THE WORK MODE: this intake says construction and names "
                              f"{first!r} as the destination. If that is a CITY or a small area, "
                              f"carry on. If it is a country or a whole region, the city has not "
                              f"been chosen yet -- that is constrained discovery, and the shortlist "
                              f"comes before this skeleton (references/decision-and-research.md).")
        if len(places) > 1:
            report.append(f"  destination_scope.named_places: {len(places)} places named; only the "
                          f"first became trip.destination. Plan the rest by hand, or run one "
                          f"skeleton per place.")
    elif named_places is not None and named_places != []:
        report.append(f"  destination_scope.named_places[0] -> trip.destination: NOT copied, expected "
                      f"a list of place names, found {named_places!r}. Pass --destination.")

    dietary = pick_list("trip.traveler_constraints.dietary_or_religious_needs",
                        "feasibility.dietary_or_religious_needs")
    mobility = pick_list("trip.traveler_constraints.mobility_notes",
                         "party.mobility_or_access_needs")
    # What the traveller asked FOR. Carried across the same way the constraints are, because the
    # form collects both and only the constraints used to survive: the plan remembered the allergy
    # and forgot the reason for the trip. must_haves is the binding one -- every entry has to be
    # answered by an anchor or excused in unmet_preferences before the plan will save.
    must_haves = pick_list("trip.traveler_preferences.ranked_must_haves",
                           "experience.ranked_must_haves")
    natural = pick_list("trip.traveler_preferences.natural_subtypes",
                        "experience.natural_subtypes")
    cultural = pick_list("trip.traveler_preferences.human_cultural_subtypes",
                         "experience.human_cultural_subtypes")
    avoid = pick_list("trip.traveler_preferences.avoid_list", "experience.avoid_list")

    # Printed before the checks below, so that a run which then fails on a bad date still shows
    # the operator what was read out of the file and what the file said.
    if args.from_intake:
        print(f"--from-intake {args.from_intake}", file=sys.stderr)
        for line in report or ["  nothing copied: the intake carried none of the mapped keys."]:
            print(line, file=sys.stderr)

        # Not copied into the plan -- there is no field for it -- but printed, because it is one of
        # the three questions references/research-budget.md rule 1 says to settle before any
        # research at all, and each answer deletes a whole branch. It used to be asked in chat even
        # though the intake now carries it, so an author who never opens the intake file would ask
        # the traveller a question they have already answered. A booked flight also fixes dates and
        # origin airport that the design stage would otherwise treat as open.
        # The trip's SHAPE, which decides how many stay groups the plan has, whether there is a
        # ticketed intercity leg to compare, and where the return leg starts. Nothing derives it --
        # "one country" is equally true of one base and of five stops -- and it is not copied into
        # the plan either, because the plan expresses shape through stay groups rather than a
        # declaration about itself. So it is printed, the way bookings are.
        scope = intake.get("destination_scope") if isinstance(intake, dict) else None
        shape = (scope or {}).get("trip_shape") if isinstance(scope, dict) else None
        if isinstance(shape, dict) and shape.get("state"):
            state = shape.get("state")
            if state == "single_base":
                print("  TRIP SHAPE: one base, day trips out. One stay group; no intercity leg to "
                      "compare.", file=sys.stderr)
            else:
                stops, nights = shape.get("max_stops"), shape.get("min_nights_per_stop")
                back = {"yes": "returns to the first stop to leave",
                        "no": "leaves from the last stop",
                        "either": "return airport is yours to choose on price and time"
                        }.get(shape.get("return_to_first_stop"), "return leg unstated")
                print(f"  TRIP SHAPE: {state}, at most {stops} stops, at least {nights} night(s) "
                      f"each, {back}. Give each stop its OWN stay_group_id and its own compared "
                      f"accommodation options, and give every intercity leg its own leg_group_id "
                      f"with two compared options or a researched single_option_reason.",
                      file=sys.stderr)
        else:
            print("  TRIP SHAPE: the intake does not say whether this is one base or several "
                  "stops. Ask ONCE, with the other checkpoint questions.", file=sys.stderr)

        booked = intake.get("existing_bookings") if isinstance(intake, dict) else None
        if isinstance(booked, dict) and booked.get("state"):
            state = booked.get("state")
            if state == "nothing":
                print("  ALREADY BOOKED: nothing. Dates and transport are still open.",
                      file=sys.stderr)
            else:
                print(f"  ALREADY BOOKED: {state} — {booked.get('details') or 'no detail given'}. "
                      f"Treat these as fixed and do not research alternatives for them; "
                      f"do not ask the traveller again.", file=sys.stderr)
        else:
            print("  ALREADY BOOKED: the intake does not say. Ask ONCE, with the other "
                  "checkpoint questions, before any research — not after.", file=sys.stderr)

    missing = [flag for flag, value in (("--start", start_text), ("--end", end_text),
                                        ("--origin", origin), ("--destination", destination))
               if not value]
    if missing:
        print("ERROR: no value for " + ", ".join(
            f"{flag} (intake {REQUIRED_FROM_INTAKE[flag]})" for flag in missing)
            + ". Pass the flag, or point --from-intake at an intake file that carries the key.",
            file=sys.stderr)
        return 2

    # Name which date and where it came from: a date can now arrive from the intake file, and
    # "month must be in 1..12" alone leaves the operator hunting through two possible sources.
    def as_date(flag: str, text: str):
        try:
            return dt.date.fromisoformat(text)
        except ValueError as exc:
            source = flag if text == getattr(args, flag.lstrip("-")) else \
                f"the intake's {REQUIRED_FROM_INTAKE[flag]}"
            print(f"ERROR: {flag} value {text!r} is not a YYYY-MM-DD date ({exc}). "
                  f"Fix it in {source}.", file=sys.stderr)
            return None

    start, end = as_date("--start", start_text), as_date("--end", end_text)
    if start is None or end is None:
        return 2
    if end < start:
        print(f"ERROR: --end {end.isoformat()} is before --start {start.isoformat()}.", file=sys.stderr)
        return 2

    travellers = travellers if travellers is not None else 1
    currency = currency if currency is not None else "EUR"

    span = (end - start).days + 1

    # A skeleton nobody can fill is not a favour. `--start 2027-03-01 --end 2027-05-30
    # --stops-per-day 12` emitted 91 days, 181 dining cards, 1001 segments and 1.4 MB, exit 0, no
    # word of warning -- and every value in it is a TODO that validate_trip_html.py refuses to
    # ship, so the operator must research all of it before anything renders. The verification pass
    # scales with the number of claims, not with nights, so the cost lands later and larger than
    # anyone expects at this prompt. Warn where it starts to hurt, refuse where it is certainly a
    # mistake, and let --oversize through for the person who genuinely means it.
    dining_estimate = max(0, span - 2) * 2 + 2
    # Whether a second city exists at all, which decides what the size advice below can honestly
    # recommend. Absent an intake there is nothing to read, so the flag-only path is unchanged.
    single_base = (str(dig(intake, "destination_scope", "trip_shape", "state") or "")
                   == "single_base") if intake else False
    if span > OVERSIZE_DAYS or args.stops_per_day > OVERSIZE_STOPS:
        if not args.oversize:
            print(
                f"ERROR: {span} days x {args.stops_per_day} stops/day is past the point where a "
                f"skeleton can be filled honestly (limits: {OVERSIZE_DAYS} days, {OVERSIZE_STOPS} "
                f"stops/day).\n"
                f"  It would carry about {dining_estimate} dining cards and "
                f"{span * (args.stops_per_day + 1)} route segments, each needing researched hours, "
                f"a fare basis and a map link, and the mandatory verification pass scales with all "
                f"of them.\n"
                f"  Split it into one plan per city or per leg -- that is also how a traveller "
                f"reads it -- or pass --oversize if you really mean one file.",
                file=sys.stderr)
            return 2
        print(f"NOTE: --oversize accepted: {span} days x {args.stops_per_day} stops/day.",
              file=sys.stderr)
    elif span > WARN_DAYS or args.stops_per_day > WARN_STOPS:
        print(
            f"NOTE: {span} days x {args.stops_per_day} stops/day is a large plan -- roughly "
            f"{dining_estimate} dining cards and {span * (args.stops_per_day + 1)} route segments "
            f"to research, and the verification pass scales with the number of claims rather than "
            f"the number of nights. "
            # "Consider one plan per city" is only advice if there is a second city. On a
            # single-base trip -- which the intake states outright -- it names a split that cannot
            # be made, and advice a reader cannot act on teaches them to skip the next note. The
            # lever on a long stay in one place is stops per day, not cities.
            + ("Cut --stops-per-day rather than splitting the plan: the intake says this trip "
               "keeps one base, so there is no second city to split off."
               if single_base else
               "Consider one plan per city."),
            file=sys.stderr)

    days = []
    for offset in range(span):
        date = start + dt.timedelta(days=offset)
        day_type = "arrival" if offset == 0 else "departure" if offset == span - 1 else "full"
        days.append(build_day(offset + 1, date, day_type, args.stops_per_day, args.mode,
                              english_plan(language)))

    plan = {
        "plan_status": "researched",
        "verification_status": None,
        "verification_report": None,
        "generated_at": DATE,
        # Filled for free on the path this skill requires, and only there. --from-intake proves a
        # traveller filled the loopback HTML form, because that file is what the intake server
        # writes -- so html_form costs the author nothing, and the routes that skipped the form are
        # the ones that have to stop and name themselves (--intake-method, and for chat_fallback
        # the traveller's own words declining it). Omitted entirely when the author says nothing:
        # a guess here would be the skeleton asserting something it cannot know, and
        # save_trip_deliverables.py refuses the plan until someone answers.
        **({"intake_context": intake_context} if intake_context else {}),
        "ui_labels": None,
        "trip": {
            "title": f"{TODO}trip title", "language": language, "currency": currency,
            "origin": origin, "destination": destination, "destination_type": "city",
            "timezone": f"{TODO}IANA time zone of the destination, e.g. Europe/London",
            "origin_timezone": f"{TODO}IANA time zone the traveller leaves from, e.g. Europe/Amsterdam",
            # Declared once so every map endpoint can be checked absolutely: a lat/lon pair
            # written in the wrong order keeps its partner the right distance away while
            # pointing at another continent, which no leg-length rule can see.
            "destination_coords": {"lat": 0, "lon": 0},
            "start_date": start.isoformat(), "end_date": end.isoformat(),
            "traveler_count": travellers, "pace": f"{TODO}pace",
            "budget_basis": f"{TODO}what the per-person total includes",
            "arrival_transport_mode": "flight",
            # Empty is a claim here, not a placeholder: it says the traveller stated no dietary,
            # allergy or mobility constraint. Leave it empty only when that is true. A TODO would
            # be worse -- these are the fields the dining and walking gates read, and a gate that
            # reads a sentence measures nothing. --from-intake fills the two list fields; the
            # severity, the card text and the walking cap have no intake key and are authored here.
            #
            # That paragraph was right about the list fields and wrong about the other two, and the
            # measurement says how wrong: with `allergy_severity: "none"` and
            # `max_continuous_walking_minutes: null` left untouched, deleting EVERY activity's
            # on_foot_minutes from a real five-day plan changed the error count from 2 to 2 --
            # every walking check silently no-ops, because check_walking_budget arms itself off
            # `cap is not None`. And SKILL.md's light verification tier is allowed only when the
            # severity is none/preference AND the cap is null, so those two defaults did not merely
            # fail to enforce anything: they were exactly what bought the cheaper pass. A model that
            # never typed them switched the walking checks off and skipped four verification domains
            # in one move, and no gate said a word.
            #
            # "A TODO would be worse" stays true OF THESE FIELDS -- prose in either one fails
            # validate_plan and the skeleton stops rendering at all -- which is why the marker sits
            # beside them instead of in them. The severity now starts as null rather than "none":
            # null is the one value the enum validator accepts that is not an answer, so the page
            # prints no allergy row and required_domains_for already reads it as unsettled, while
            # "none" was the plan asserting on the traveller's behalf that there was nothing to
            # avoid. Empty is still a claim for the two LIST fields; leave them empty only when the
            # traveller stated nothing.
            "traveler_constraints": {
                "dietary_or_religious_needs": dietary,
                "allergy_severity": None,
                "allergy_card_text": None,
                "max_continuous_walking_minutes": None,
                "mobility_notes": mobility,
                UNTYPED_CONSTRAINTS_MARKER: dict(UNSET_CONSTRAINTS),
            },
            # The other half of the same form. traveler_constraints is what the traveller cannot
            # have; this is what they came for, and until it existed nothing downstream could tell
            # whether the itinerary delivered it -- a delivered plan had every anchor deleted and
            # all nineteen checks stayed green. Each must-have needs an anchor naming it in
            # satisfies_preference, or an unmet_preferences entry saying what makes it impossible.
            "traveler_preferences": {
                "ranked_must_haves": must_haves,
                "natural_subtypes": natural,
                "human_cultural_subtypes": cultural,
                "pace": None,
                "avoid_list": avoid,
                "avoid_list_handling": [
                    {"item": item, "how_avoided": f"{TODO}what in this plan keeps it out"}
                    for item in avoid
                ],
                "unmet_preferences": [],
            },
            # Empty unless the traveller changes one of their limits after the form. The four
            # limits above are compared with the intake file, and a difference is accepted only
            # when an entry here says what changed and why; the page prints it.
            "intake_changes": [],
        },
        "profile_context": {"profile_id": None, "profile_last_reviewed_at": None,
                            "applied_saved_fields": [], "excluded_places_checked": []},
        # SKILL.md's quality gate requires the entry conclusion to reach the page through
        # entry_context, and the template, this skeleton and the HTML template all omitted it --
        # so a real cross-border plan shipped with no entry section at all while Schengen border
        # checks were reintroduced. Emitting it means the author deletes it deliberately on a
        # domestic trip instead of never meeting it. traveler_basis is the status CATEGORY the
        # conclusion rests on: it lands on a page the traveller may forward, where a document
        # number is unsafe and, a month later, less use than the category anyway.
        "entry_context": {
            "status": "unverified",
            "summary": f"{TODO}what the entry rules mean for this traveller on these dates",
            "traveler_basis": f"{TODO}status category the conclusion rests on, never a document number or expiry",
            "source_url": URL,
            "checked_at": DATE,
        },
        # The four questions a traveller has walking out of an arrivals hall, which nothing else in
        # this scaffold asks. Emitted as `unverified` with TODO text rather than omitted, for the
        # reason entry_context is emitted directly above: a block that has to be remembered is a
        # block that gets skipped, and the renderer refuses a plan without it -- so the author who
        # never opens this scaffold meets the requirement as a gate failure instead of as a form.
        # Every entry may legitimately become `not_applicable` WITH a reason (a domestic trip needs
        # no consulate); none of them may stay silent.
        "arrival_essentials": {
            "payment": {
                "status": "unverified",
                "summary": f"{TODO}will the traveller's cards work, and how much cash to carry",
                "cards_accepted": None, "cash_customary": None, "atm_or_fx_note": None,
                "not_applicable_reason": None, "source_url": None, "checked_at": None,
            },
            "connectivity": {
                "status": "unverified",
                "summary": f"{TODO}SIM/eSIM or roaming, and what the sockets take",
                "sim_or_esim": None, "roaming_note": None, "plug_types": None, "voltage": None,
                "not_applicable_reason": None, "source_url": None, "checked_at": None,
            },
            "emergency": {
                "status": "unverified",
                # The number is the field somebody dials while something is going wrong, so the
                # renderer refuses a `researched` emergency entry that leaves it empty.
                "summary": f"{TODO}who to call, and the consulate for this passport if abroad",
                "local_emergency_number": None, "consulate_or_embassy": None,
                "consulate_contact": None,
                "not_applicable_reason": None, "source_url": None, "checked_at": None,
            },
            "health_and_insurance": {
                "status": "unverified",
                "summary": f"{TODO}cover the traveller stated, and what the destination expects",
                "cover_stated_by_traveller": None, "destination_requirement": None,
                "not_applicable_reason": None, "source_url": None, "checked_at": None,
            },
        },
        "regional_service_context": {
            "destination_service_market": f"{TODO}service market",
            "selection_basis": f"{TODO}why these providers suit this market",
            "google_services_access": "unknown",
            "primary_map_provider": f"{TODO}primary map provider",
            "primary_map_exception_reason": None, "alternative_map_providers": [],
            "local_transport_sources": [], "booking_platform_selection_note": f"{TODO}platform rationale",
            # These categories are NOT the budget spellings. attraction_ticket / rail_or_ground.
            "booking_access_checks": [
                {"category": category, "access_status": "unknown",
                 # Never interpolate the category enum into prose: on a non-Latin page the
                 # validator rejects the surviving English, and it is right to.
                 "provider_or_channel": f"{TODO}booking channel for this category",
                 "requirements_note": f"{TODO}non-sensitive requirement or caveat",
                 "source_url": URL, "checked_at": DATE}
                # rental_car is required only when the self-drive branch shows a car option.
                for category in (("flight", "accommodation", "attraction_ticket", "rail_or_ground")
                                 + (("rental_car",) if args.mode == "self-drive" else ()))
            ],
        },
        "budget": {
            # cap_per_person was hardcoded None, so the cap-overrun check no-opped on every plan
            # this script produced and the traveller's own stated cap never reached the page.
            "calculation_basis": "per_person", "cap_per_person": cap_per_person,
            "overrun_acknowledged": None,
            "estimated_per_person_low": 0, "estimated_per_person_high": 0,
            "included_categories": ["flight", "accommodation"],
            "unverified_categories": [],
            "breakdown": [
                {"category": category, "description": f"{TODO}what this covers",
                 "per_person_low": 0, "per_person_high": 0, "currency": currency,
                 "price_status": "estimate", "checked_at": DATE,
                 "note": f"{TODO}basis for this figure"}
                for category in ("flight", "accommodation")
            ],
        },
        "transport_preference": {"mode": args.mode,
                                 "self_drive_selected": args.mode == "self-drive",
                                 "public_transit_selected": args.mode == "public-transit"},
        "booking_options": {
            # Two candidates, and their review_urls must differ.
            "flights": [
                # leg_group_id names the JOURNEY these options are alternatives FOR, so the
                # "two comparable candidates" rule counts within a leg instead of across legs. A
                # single-leg trip needs only this one value; a multi-stop trip gives each journey
                # its own, exactly as accommodations give each stop its own stay_group_id.
                {"id": f"fl-{n}", "leg_group_id": "leg-1",
                 "provider": f"{TODO}provider {n} (must own review_url)",
                 "comparison_platform": f"{TODO}comparison platform {n}",
                 "comparison_checked_at": DATE,
                 "direct_provider": None, "direct_review_url": None,
                 "source_type": "airline_and_comparison_platform", "checked_at": DATE,
                 "review_url": f"{URL}-flight-{n}",
                 "round_trip_search_provider": f"{TODO}search platform {n}",
                 "round_trip_search_checked_at": DATE,
                 "round_trip_search_url": f"{URL}-search-{n}",
                 "round_trip_prefilled_fields": ["origin", "destination", "outbound_date",
                                                 "return_date", "travellers"],
                 "origin_airport": f"{TODO}origin airport", "destination_airport": f"{TODO}destination airport",
                 "outbound_date": start.isoformat(), "return_date": end.isoformat(),
                 "outbound_itinerary": {"service_identifier": f"{TODO}service", "departure_local": f"{TODO}local time",
                                        "arrival_local": f"{TODO}local time", "duration_minutes": 1, "stops": 0,
                                        "connection_or_terminal_note": f"{TODO}connection note"},
                 "return_itinerary": {"service_identifier": f"{TODO}service", "departure_local": f"{TODO}local time",
                                      "arrival_local": f"{TODO}local time", "duration_minutes": 1, "stops": 0,
                                      "connection_or_terminal_note": f"{TODO}connection note"},
                 "cabin": f"{TODO}cabin", "baggage_assumption": f"{TODO}baggage assumption",
                 "connection_summary": f"{TODO}connection summary", "fare_currency": currency,
                 "fare_low": 0, "fare_high": 0, "price_basis": "per_person_round_trip",
                 "price_status": "estimate", "material_conditions": f"{TODO}fare conditions",
                 "availability_status": "unknown", "price_checked_at": DATE,
                 "airport_transfer_note": f"{TODO}airport-to-city burden", "single_option_reason": None}
                for n in (1, 2)
            ],
            "accommodations": [
                {"id": f"acc-{n}", "stay_group_id": "stay-1",
                 # Which entry rules and local services apply to THIS stop. One stay group per
                 # stop on a multi-stop trip, and one jurisdiction each: a trip that enters two
                 # places needs two entry answers, and an answer for one country is wrong about
                 # the other.
                 "jurisdiction": (f"{TODO}jurisdiction (e.g. Japan / Mainland China / Hong Kong / Schengen Area)"
                                  if english_plan(language) else
                                  f"{TODO}jurisdiction (e.g. 日本 / 中国大陆 / 香港 / 申根区)"),
                 "stay_location": f"{TODO}stay area",
                 "neighborhood": f"{TODO}neighbourhood", "address_or_location_reference": f"{TODO}location reference",
                 "property_name": f"{TODO}property {n}", "provider": f"{TODO}provider (must own review_url)",
                 "comparison_platform": f"{TODO}comparison platform", "comparison_checked_at": DATE,
                 "direct_provider": None, "direct_review_url": None, "source_type": "comparison_platform",
                 "checked_at": DATE, "review_url": f"{URL}-property-{n}",
                 "check_in": start.isoformat(), "check_out": end.isoformat(),
                 "guest_count": travellers, "room_count": 1,
                 "comparison_searches": [{"platform": f"{TODO}platform", "search_url": URL,
                                          "checked_at": DATE,
                                          "prefilled_fields": ["destination", "check_in", "check_out", "guests", "rooms"]}],
                 "room_basis": f"{TODO}room basis", "nightly_cost_low": 0, "nightly_cost_high": 0,
                 "price_basis": "per_room_per_night", "price_status": "estimate",
                 "trip_cost_low": 0, "trip_cost_high": 0, "currency": currency,
                 "price_checked_at": DATE, "availability_status": "unknown", "availability_unknown_reason": None,
                 # The page you open to read the price publishes the score beside it, so these
                 # cost one read rather than a second errand.
                 "guest_rating_status": "verified", "guest_rating_value": 0,
                 "guest_rating_scale": 10, "guest_rating_count": 0,
                 "guest_rating_source": f"{TODO}where the score was read",
                 "guest_rating_url": f"{TODO}https://…the property on that platform",
                 "guest_rating_checked_at": DATE, "guest_rating_absence_reason": None,
                 "guest_rating_below_floor_reason": None,
                 "taxes_and_fees_status": f"{TODO}taxes and fees", "cancellation_terms": f"{TODO}cancellation",
                 "accessibility_or_location_note": f"{TODO}access note", "arrival_access_note": f"{TODO}arrival access",
                 "key_area_access_note": f"{TODO}access to planned areas",
                 "selection_rationale": f"{TODO}why this one", "single_option_reason": None}
                for n in (1, 2)
            ],
            "attraction_tickets": [],
            # Only the self-drive branch requires this; the renderer rejects a self-drive plan
            # with no rental option, and an empty list on a transit plan is correct.
            "rental_cars": ([
                {"id": "car-1", "provider": f"{TODO}rental provider (must own review_url)",
                 "comparison_platform": f"{TODO}comparison platform", "comparison_checked_at": DATE,
                 "direct_provider": None, "direct_review_url": None, "source_type": "comparison_platform",
                 "checked_at": DATE, "review_url": f"{URL}-rental",
                 "pickup_location": f"{TODO}pickup place", "dropoff_location": f"{TODO}dropoff place",
                 "pickup_time": f"{TODO}YYYY-MM-DD HH:MM", "dropoff_time": f"{TODO}YYYY-MM-DD HH:MM",
                 "vehicle_class": f"{TODO}vehicle class", "transmission": f"{TODO}transmission",
                 "capacity_note": f"{TODO}luggage and party capacity",
                 "price_low": 0, "price_high": 0, "currency": currency,
                 "price_basis": "per_vehicle_per_day", "price_status": "estimate",
                 "price_checked_at": DATE, "availability_status": "unknown",
                 "rental_search_prefilled_fields": ["pickup_location", "dropoff_location",
                                                    "pickup_time", "dropoff_time"],
                 "insurance_excess": f"{TODO}insurance excess", "fuel_policy": f"{TODO}fuel policy",
                 "mileage_policy": f"{TODO}mileage policy",
                 "cross_border_or_restriction_note": f"{TODO}restrictions"}
            ] if args.mode == "self-drive" else []),
        },
        "transport_overview": {
            "map_link_kind": "directions", "overall_map_scope": "primary_leg",
            "overall_route_map_url": URL,
            "overall_map_checked_at": DATE, "overall_map_provider": f"{TODO}map provider",
            "overall_alternative_map_links": [], "overall_duration_minutes": 0, "overall_distance_km": 0,
            "cost_low": 0, "cost_high": 0, "notes": [f"{TODO}overall transport note"],
        },
        "days": days,
        "destination_experience_anchors": [
            {"name": f"{TODO}anchor {n}", "category": f"{TODO}category",
             "neighborhood_or_area": f"{TODO}area", "planned_day": min(n, span),
             "why_it_matters": f"{TODO}why it matters", "source_url": URL,
             "checked_at": DATE} for n in (1, 2, 3)
        ],
        "sources": [{"name": f"{TODO}source", "url": URL, "source_type": f"{TODO}type",
                     "accessed_at": DATE, "claim_or_decision_supported": f"{TODO}what it supports",
                     "confidence": "medium"}],
        "assumptions": [f"{TODO}state every assumption you carried"],
        "recheck_before_purchase": [f"{TODO}what must be rechecked before booking"],
    }

    json.dump(plan, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")

    # Two constraints arrive from intake as prose and stay unmeasured until someone turns them
    # into the typed fields the gates read. Both are named because both went missing in the
    # measured run: a severe dairy allergy that reached no dining card, and a 20-30 minute
    # walking limit against a day that scheduled hours of it.
    #
    # The wording tracks what the file now says: both fields carry an entry in
    # trip.traveler_constraints[UNTYPED_CONSTRAINTS_MARKER] instead of a value that reads as an
    # answer, so the note names the marker the author has to clear. A note that described a value
    # the skeleton no longer writes would send them to the wrong line.
    if mobility:
        print("  NOTE: trip.traveler_constraints.max_continuous_walking_minutes is still null and "
              f"marked untyped in {UNTYPED_CONSTRAINTS_MARKER}. Set it to the number those "
              "mobility notes state and delete the marker entry, or no gate measures the limit.",
              file=sys.stderr)
    if dietary:
        print("  NOTE: trip.traveler_constraints.allergy_severity is still null and marked untyped "
              f"in {UNTYPED_CONSTRAINTS_MARKER}, and allergy_card_text is null. Set the severity "
              "(none | preference | intolerance | severe), write the card, and delete the marker "
              "entry, or nothing on the page or in the gates knows there is anything to avoid.",
              file=sys.stderr)
    # The chain's first link. An assistant that has just produced a skeleton needs to know the
    # loop it is now in, and the field-name pass is the cheapest thing to run first.
    print("NEXT: fill it in, then python scripts/check_plan_contract.py <plan.json>",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
