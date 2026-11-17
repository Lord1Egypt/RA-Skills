#!/usr/bin/env python3
"""Project a plan down to what ONE verification domain reads, before the fan-out.

references/verification.md sends five truth-domain verifiers at the same file: "Each verifier gets
the plan path and this instruction." Five agents then read one plan five times. Measured on
2026-08-30 over the 15 plans in a real workspace, that file is 28,943 bytes at the smallest,
85,836 at the median and 2,132,252 at the largest, and references/research-budget.md prices the
full verification pass at ~700k tokens -- so the re-reads are a real line in that budget, and on
the largest plan they are the dominant one. This script hands each domain a projection instead.

WHAT THIS IS NOT, because the obvious version of it is wrong and was refuted three times.

The five domains are not a partition of the plan's fields, and the prose table in
verification.md is not a schema. `booking_and_lodging` is told to answer "for every ticket a day
actually schedules, when do the seats go on sale, and where does the plan have the traveller at
that moment?" -- which needs `days`. `entry` must check transit visas for the actual connection
airports, which are in the itinerary and the flight cards, not in `entry_context`. `seasonality`
must check daylight against scheduled times, which is `days`. An allow-list built from the table's
prose would take exactly those fields away, and each of them is where a measured trip-breaking
defect lived.

So this is a SUBTRACTIVE deny list. Every slice keeps `trip`, `days` and `budget` unconditionally;
a block is dropped from a domain only when that domain's duties cannot be expressed by any field
in it, and every drop carries the reason in IRRELEVANT_TO below. A top-level key this file has
never heard of is KEPT and reported, which is the whole reason to write the rule subtractively:
an allow-list silently starves a domain when the schema grows, and a deny list only gets less
efficient. tests/test_plan_slice.py pins the two tables to templates/final-trip-plan.json, so a
key added to the contract fails that test until somebody classifies it -- and while nobody has,
the key travels with every slice rather than disappearing from all five.

Accept the smaller saving. The big blocks are mostly kept, on purpose, and
KEPT_EVERYWHERE_BECAUSE records why for each one -- that dict is the argument, not decoration.

THE AUDITORS ARE OUT OF SCOPE. `consistency` and `completeness` check the plan against ITSELF:
which stated preference is served only by a token anchor, whether a day's pacing is physically
plausible, which collected field never reaches the page. Every one of those questions is a
comparison between two parts of the plan, so removing either part does not make the auditor
cheaper, it makes it wrong. They get the whole plan, and passing their names as --domain is
refused with that reason rather than with an argparse usage line.

Pointers survive. check_plan_consistency requires every `claims_checked` entry to resolve against
the real plan, so a projection that renumbered a list or flattened a block would make a verifier's
honest citation fail the gate. This slices by top-level key only: kept blocks are the same objects
in the same order, so `days[2].dining[1].venue_hours` means the same thing in the slice as in the
plan, and the only pointers that stop resolving are the ones rooted at a key this file printed as
dropped.

Usage:
    python scripts/plan_slice.py <plan.json> --domain entry
    python scripts/plan_slice.py <plan.json> --domain seasonality --out /tmp/seasonality.json
    python scripts/plan_slice.py <plan.json> --domain transport --stdout | pbcopy

The slice is written to `slices/<plan-stem>.slice-<domain>.json` beside the plan -- a
subdirectory, because audit_workspace.py recognises a plan by its shape over a non-recursive
plans/*.json glob and would audit a slice sitting in there as an itinerary. What was dropped is
BOTH printed and recorded inside the file, so the projection is an artifact somebody can check
rather than a stderr line nobody keeps. It is written in the plan's own indentation, so the
saving printed on the summary line is a saving in the file a verifier actually opens.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import textwrap
from pathlib import Path

# The five truth domains of references/verification.md#verify-domains, in the order that reference
# lists them. Anything else is refused by name below. Cited against an explicit <a id> rather than
# a heading slug on purpose: a slug moves the moment somebody rewords the heading, and a citation
# that quietly stops resolving teaches the next author that the citations are not worth following.
DOMAINS = ("entry", "transport", "sights_and_hours", "booking_and_lodging", "seasonality")
ALL_FIVE = frozenset(DOMAINS)

# Named so the refusal can explain itself. An operator who types --domain consistency has read the
# reference and found seven blocks in the report schema; a bare "invalid choice" would read as a
# typo and invite a retry with a slice, which is the one outcome this file exists to prevent.
AUDITORS = {
    "consistency": "it duplicates what check_plan_consistency.py decides plus the judgements the "
                   "script cannot express, and every one of those compares two parts of the plan "
                   "to each other",
    "completeness": "its question is 'what is missing?' -- which stated preference is served only "
                    "by a token anchor, which collected field never reaches the page -- and a "
                    "block removed from the file is indistinguishable from a block the plan never "
                    "had",
}

# Kept by every domain, no exceptions, because each of the five was measured to need them. `days`
# is the itinerary every domain dates its claims against; `trip` carries the dates, destination,
# traveller count and constraints; `budget` is where a fare, a nightly rate and a ticket price are
# reconciled, and three of the five verify one of those numbers.
ALWAYS_KEEP = ("trip", "days", "budget")

# The deny list: block -> (domains that DROP it, why they can).
#
# Read every reason as a claim about the DOMAIN'S DUTIES in verification.md's table, not about how
# interesting the block looks. Where two rows of that table overlap, the table itself assigns the
# question -- route seasons belong to `transport` because its row says "on the planned weekday, in
# the planned season", venue closure days belong to `sights_and_hours` because its row says so --
# and these reasons follow that assignment rather than re-litigating it.
IRRELEVANT_TO: dict[str, tuple[frozenset[str], str]] = {
    "imagery": (
        ALL_FIVE,
        "base64 photo payloads and Wikimedia credits. It carries no fare, opening time, entry "
        "rule, sale window or climate figure, and it is the single biggest win here: measured "
        "2026-08-30, this block was 96% of the largest plan in the workspace, so dropping it "
        "turns a five-times re-read of a multi-megabyte file into a five-times re-read of an "
        "ordinary one. Attribution and licensing are the renderer's contract, not a truth domain's."),
    "imagery_sidecar": (
        ALL_FIVE,
        "the file name of the imagery payload, for the same reason as imagery. It is a path, not "
        "a claim, and the renderer is the only thing that opens it."),
    "ui_labels": (
        ALL_FIVE,
        "localized chrome strings for the rendered page. Nothing in it is a claim about the "
        "world, and the domain that would care whether a label reaches the page is the "
        "completeness auditor, which is not sliced."),
    "_enums": (
        ALL_FIVE,
        "the closed vocabularies templates/final-trip-plan.json publishes so an author can read "
        "them before a gate rejects a value. Like `_contract` it is documentation about the file "
        "format, addressed to whoever fills the template in, and it says nothing about the trip."),
    "_contract": (
        ALL_FIVE,
        "the note block templates/final-trip-plan.json carries to explain its own optional "
        "fields. It is documentation about the file format, addressed to whoever fills the "
        "template in, and it says nothing about the trip."),
    "intake_context": (
        ALL_FIVE,
        "how the traveller's requirements were collected -- the form, their own words, or the "
        "note saying why neither -- and the evidence for it. save_trip_deliverables.py refuses a "
        "plan that will not say, and the completeness auditor reads it to ask which collected "
        "field never reached the page. None of the five checks a fare, an hour or an entry rule "
        "against it."),
    "gates_passed": (
        ALL_FIVE,
        "a record of which deterministic checks ran. verification.md opens by saying those gates "
        "prove the plan is well-formed and prove nothing in it is true, so handing this stage the "
        "structural verdict adds bytes and no evidence."),
    "verification_status": (
        ALL_FIVE,
        "this stage's own prior verdict. The prompt shape at references/verification.md#prompt-shape "
        "exists because an agent asked to check a claim tends to find support for it; telling a "
        "verifier the plan is already 'verified' is the cheapest possible way to buy that bias."),
    "verification_report": (
        ALL_FIVE,
        "the filename of the previous report, for the same reason as verification_status. The "
        "gate binds report to plan itself; a verifier does not need the last answer to write "
        "this one."),
    "entry_context": (
        ALL_FIVE - {"entry"},
        "the visa conclusion, its basis, source and date -- the entry row's whole subject. No "
        "other row turns on it: a fare, an opening time, a sale window and a sunset are the same "
        "whether the traveller needs a visa or not."),
    "bookings": (
        ALL_FIVE - {"booking_and_lodging"},
        "the traveller's own decisions -- which option was chosen or booked, when, where, and what "
        "was paid. None of it is research and none of it is verified: the block sits outside the "
        "verification fingerprints (verification_sections.META_KEYS). booking_and_lodging keeps it "
        "so its verifier can skip re-checking whether something already bought is still sellable; "
        "no other row turns on it."),
    "arrival_essentials": (
        ALL_FIVE - {"entry"},
        "can the traveller pay, get online, call for help, and are they insured. Every one of the "
        "four is keyed to NATIONALITY x DESTINATION, which is the entry row's own axis: the "
        "consulate is a fact about one passport in one country, and travel medical insurance is a "
        "condition of a Schengen visa rather than only a prudent purchase. `entry` is also the "
        "only row whose verifier already holds the traveller's nationality and residence status, "
        "and without those the block cannot be checked at all -- a Dutch EHIC is valid across the "
        "EU and worthless in Switzerland for a third-country national, and nothing but nationality "
        "separates those two answers.\n"
        "        The edge worth naming, because it is the one that could make this wrong: card "
        "acceptance is arguably a `transport` fact the moment a tram ticket machine refuses the "
        "traveller's card. It is dropped there anyway. The transport row checks fares, routes and "
        "durations against operators, and each claim in this block carries its own source and "
        "date -- so a transport verifier handed it would be re-checking a sourced fact outside its "
        "own evidence base. If a real report is ever seen citing arrival_essentials from the "
        "transport domain, this entry is wrong and the precedent for fixing it is "
        "regional_service_context directly below."),
    "profile_context": (
        ALL_FIVE - {"entry"},
        "provenance for which saved profile fields fed which decision. `entry` keeps it because "
        "this is where nationality and residence status enter the plan at all -- the table asks "
        "for a verdict per nationality x residence status and `trip` carries neither. For the "
        "other four the values it feeds are already materialized in trip.traveler_constraints and "
        "in the day cards, and whether a collected field reached the page is the completeness "
        "auditor's question."),
    "regional_service_context": (
        ALL_FIVE - {"transport", "booking_and_lodging", "entry"},
        "service routing: which map provider works where the traveller stands, which local "
        "transport operators the plan drew on, and whether each booking channel is reachable and "
        "what it demands. `transport` keeps it for the map-provider rule its row states, and "
        "`booking_and_lodging` for booking_access_checks, which is that row's 'whether search "
        "URLs load' question one level up.\n"
        "        `entry` keeps it too, and the reason is a correction rather than a design: this "
        "entry read 'Entry rules, opening hours and climate do not read it', which is a claim "
        "about what a verifier WOULD cite, and the workspace already holds five real verification "
        "reports that answer it. The Alicante report's `entry` domain cites "
        "`regional_service_context.booking_access_checks[1].requirement` in its claims_checked. "
        "Under the dropped version that pointer would not resolve against the slice, so the "
        "verifier could not have made a claim it demonstrably made -- and the loss would be "
        "silent, because a domain that cannot see a block simply reports nothing about it. "
        "Opening hours and climate stay out; a booking channel that demands a local phone or an "
        "in-country card is an entry question the moment the traveller cannot satisfy it."),
    "transport_overview": (
        ALL_FIVE - {"transport"},
        "the primary leg: its map link, duration, distance and cost. Every field is a transport "
        "claim, and the transport row already owns route seasons, so `seasonality` gains nothing "
        "by holding it either."),
    "destination_experience_anchors": (
        ALL_FIVE - {"sights_and_hours", "seasonality"},
        "the recommended places, with the day each is planned for and a paragraph on why it "
        "matters. `sights_and_hours` keeps it because 'whether each recommended venue exists at "
        "the name the plan uses' is exactly this list. `seasonality` keeps it on measurement, not "
        "on theory: scanning the 15 workspace plans on 2026-08-30, two of them state a "
        "season-dependent fact inside why_it_matters -- a winter closing time in one, a January "
        "sea temperature in the other -- and a climate figure nobody checks is the defect this "
        "whole stage exists to catch. Entry, transport and booking do not read it."),
}

# The blocks NOT in the deny list, and why each survived the argument. This dict is load-bearing:
# _validate_table() below refuses to import unless every key this file knows about appears in
# exactly one of the two dicts, so a block added to the schema cannot be quietly dropped from all
# five domains, and one cannot be quietly kept with no reason on record either. That is the same
# "silence is not a decision" rule tests/test_packaging.py applies to the gates' citations.
KEPT_EVERYWHERE_BECAUSE = {
    "booking_options": (
        "the obvious candidate, kept by all five, and the reason the saving here is measured in "
        "single-digit percents on an ordinary plan. `booking_and_lodging` owns it. "
        "`sights_and_hours` needs attraction_tickets for timed-entry rules and combo-ticket "
        "splitting. `entry` needs the flight cards, because the transit-visa question is about "
        "the actual connection airports. `transport` needs the leg durations and the airport "
        "transfer fare quoted in the flight card. `seasonality` keeps it on measurement: 3 of the "
        "15 workspace plans state a sunset time inside booking_options (scanned 2026-08-30), "
        "twice as the stated reason for choosing one flight over another -- so a slice that took "
        "this block away from seasonality would create a hole exactly where the reference says "
        "the defects live."),
    "sources": (
        "the plan's evidence base, one entry per claim with the decision it supports. It is the "
        "largest block deliberately left in place. Every domain is told to be adversarial and to "
        "prefer official sources, and the first move in refuting a claim is opening the source "
        "the plan leaned on; taking it away would make each verifier re-research from zero, which "
        "spends more tokens than the block costs. It also cannot be filtered per domain -- "
        "dropping entries would renumber sources[n] and break the pointers the gate resolves."),
    "assumptions": (
        "a list of sentences the plan states as fact. 'Stated as fact while unverifiable' is a "
        "verdict every one of the five can return, and these sentences span all five subjects."),
    "recheck_before_purchase": (
        "the warnings about what may change before the traveller pays -- inventory, price, hours, "
        "weather. Same argument as assumptions: cross-domain by construction, and small."),
    "replan_context": (
        "the one block whose name reads like bookkeeping and is not. `must_reverify` is the list "
        "of facts the change invalidated -- move a trip window by a day and every opening hour, "
        "closure day and market day keyed to a weekday quietly becomes a guess -- which is the "
        "re-verification worklist for all five domains at once. Taking it away would hand each "
        "verifier a plan that looks freshly checked."),
    "transport_preference": (
        "self-drive versus public transit changes what each domain is even looking for: an "
        "International Driving Permit is a document `entry` would flag, a car park is a cost "
        "`booking_and_lodging` would price. Two hundred bytes, and no domain where it is provably "
        "irrelevant."),
    "plan_status": (
        "whether the plan calls itself a draft or researched. It sets what counts as 'stated as "
        "fact' for every domain, and it is one scalar."),
    "generated_at": (
        "the plan's own date. The gate rejects a report dated before it, and every domain "
        "compares a checked_at against it. One scalar."),
}

# Derived, never restated, so the two dicts above are the only place a block is named.
KNOWN_TOP_LEVEL_KEYS = frozenset(IRRELEVANT_TO) | frozenset(KEPT_EVERYWHERE_BECAUSE) | frozenset(ALWAYS_KEEP)

# The provenance block this script adds to every slice. Named as a key no plan carries, and
# refused as input below, so a slice can never be sliced again.
RECORD_KEY = "plan_slice"


def _validate_table() -> None:
    """Refuse to load on a self-contradicting table. Raises rather than degrading.

    Every failure here is a silent-wrong-output failure if it is allowed through: a block in both
    dicts means the file disagrees with itself about whether it is dropped, a mandatory keep
    appearing in the deny list means a domain gets a plan with no itinerary, and a typo in a
    domain name inside IRRELEVANT_TO means a block is dropped from a domain that does not exist
    while staying in one that does. None of those show up in the output -- the slice just quietly
    contains the wrong thing -- so they are asserted at import, where they stop the run.
    """
    both = sorted(set(IRRELEVANT_TO) & set(KEPT_EVERYWHERE_BECAUSE))
    if both:
        raise AssertionError(
            f"plan_slice: {both} appear in both IRRELEVANT_TO and KEPT_EVERYWHERE_BECAUSE, so the "
            f"table disagrees with itself about whether they are dropped. Pick one.")
    mandatory = sorted(set(ALWAYS_KEEP) & (set(IRRELEVANT_TO) | set(KEPT_EVERYWHERE_BECAUSE)))
    if mandatory:
        raise AssertionError(
            f"plan_slice: {mandatory} are in ALWAYS_KEEP and also in the per-block table. "
            f"trip, days and budget are kept unconditionally and must be named in one place only.")
    for block, (droppers, reason) in IRRELEVANT_TO.items():
        unknown = sorted(droppers - ALL_FIVE)
        if unknown:
            raise AssertionError(
                f"plan_slice: IRRELEVANT_TO[{block!r}] names {unknown}, which are not among the "
                f"five domains {list(DOMAINS)}. A misspelled domain drops the block from nobody "
                f"and reports nothing.")
        if not droppers:
            raise AssertionError(
                f"plan_slice: IRRELEVANT_TO[{block!r}] is dropped by no domain. A block every "
                f"domain keeps belongs in KEPT_EVERYWHERE_BECAUSE, where its reason is read.")
        if not reason.strip():
            raise AssertionError(
                f"plan_slice: IRRELEVANT_TO[{block!r}] has no reason. A drop with no reason on "
                f"record is the one thing a reader of the slice cannot check.")
    for block, reason in KEPT_EVERYWHERE_BECAUSE.items():
        if not reason.strip():
            raise AssertionError(
                f"plan_slice: KEPT_EVERYWHERE_BECAUSE[{block!r}] has no reason. The argument for "
                f"keeping a block is the only defence against someone dropping it next release.")


_validate_table()


def dropped_for(domain: str, plan_keys) -> list[str]:
    """Which of THIS plan's top-level keys this domain drops, in the plan's own order.

    Driven by the keys the plan actually has, never by the table's keys, so the script never
    reports dropping a block the file did not carry. A drop list padded with absent blocks is a
    saving that did not happen, and this list is printed as evidence.
    """
    return [key for key in plan_keys
            if key in IRRELEVANT_TO and domain in IRRELEVANT_TO[key][0]]


def slice_plan(plan: dict, domain: str) -> tuple[dict, dict]:
    """Return (slice, report). The slice is built by key selection only.

    Kept blocks are the SAME objects in the SAME order -- no copy, no renumbering, no reordering,
    no filtering inside a block -- because check_plan_consistency resolves every claims_checked
    pointer against the plan, and a verifier that cites days[2].dining[1] must be citing the same
    card the gate will look up. Nothing here mutates `plan`.
    """
    dropped = dropped_for(domain, plan.keys())
    kept = [key for key in plan if key not in set(dropped)]
    unrecognised = [key for key in kept if key not in KNOWN_TOP_LEVEL_KEYS]
    # Absent, so not dropped -- but worth printing, because "this plan had no imagery" and "this
    # domain keeps imagery" look identical in a drop list and mean opposite things.
    absent = sorted(key for key, (droppers, _) in IRRELEVANT_TO.items()
                    if domain in droppers and key not in plan)

    sliced = {key: plan[key] for key in kept}
    report = {
        "domain": domain,
        "kept": kept,
        "dropped": dropped,
        "unrecognised_kept": unrecognised,
        "absent_from_plan": absent,
        "missing_mandatory": [key for key in ALWAYS_KEEP if key not in plan],
    }
    return sliced, report


def _record(domain: str, source: Path, digest: str, source_bytes: int, report: dict) -> dict:
    """The provenance block written into the slice, so the projection travels with the file.

    Printed output is lost the moment the fan-out's logs are. The verifier reading this file needs
    to know it is holding a projection, what was taken out, and where the whole plan is -- and the
    person auditing the report afterwards needs the same, from the artifact rather than from a
    scrollback nobody kept.
    """
    # Absolute, not the path as typed. The reader of this field is a different process -- usually
    # a verifier agent in its own working directory -- and "open the full plan at source_plan" is
    # advice a relative path cannot be followed on. Falls back to the path as given if the
    # filesystem will not resolve it, because a slightly worse provenance line beats a crash.
    try:
        recorded_path = str(source.resolve())
    except OSError:
        recorded_path = str(source)
    return {
        "domain": domain,
        "source_plan": recorded_path,
        "source_plan_sha256": digest,
        "source_plan_bytes": source_bytes,
        "kept_top_level_keys": report["kept"],
        "dropped_top_level_keys": report["dropped"],
        "unrecognised_keys_kept": report["unrecognised_kept"],
        "made_by": "scripts/plan_slice.py",
        # A pointer, not a copy. The reasons are a fixed property of the script -- byte-identical
        # in every slice of every plan -- and inlining them measured, on the median workspace
        # plan, at more than a third of the saving the slice had just bought. That is the same
        # waste this repo has already measured elsewhere: 31.3% of one check_plan_consistency
        # report was a single 140-character rationale tail reprinted 48 times. The drop LIST is
        # what a reader has to be able to check against the plan, and it is right above this line.
        "why_each_key_was_dropped":
            "printed in full by scripts/plan_slice.py when the slice is made, and kept in that "
            "script's IRRELEVANT_TO table; the protocol is references/verification.md#plan-slice",
        "read_this_first":
            f"This file is a PROJECTION of a Travel Buddy plan for the {domain!r} verification "
            f"domain, not the plan. Top-level blocks listed in dropped_top_level_keys were "
            f"removed; everything kept is byte-identical and in its original order, so a "
            f"claims_checked pointer into a kept block resolves against the real plan too. If a "
            f"claim you need to check lives in a dropped block, open the full plan at "
            f"source_plan and say so in your findings rather than reporting it unverifiable. Do "
            f"not run check_plan_consistency.py on this file -- that gate reads the whole plan. "
            f"The consistency and completeness auditors are never given a slice.",
    }


def detect_indent(text: str) -> int | str | None:
    """How is this file indented? An int, "\\t", or None for compact.

    The slice is written the way its plan is written, and this is not cosmetics -- it was a
    measured bug. Hardcoded at indent=2, this script re-indented a real workspace plan written at
    indent=1 and the slice came out 92,233 bytes against the plan's 85,836 on disk: a "-7.1%
    saving" against a re-serialised baseline, while the file a verifier would actually open grew
    by 7.5%. A saving that only exists in the tool's own encoding is not a saving, and the
    operator has no way to see the difference from the summary line.

    Heuristic, deliberately, and it degrades to indent=2 rather than raising: the whitespace after
    the opening brace is what json.dump would have written, and any file this does not recognise
    is one where the like-for-like number below is reported separately anyway.
    """
    match = re.match(r"^[\s﻿]*[{\[]\r?\n([ \t]*)\S", text)
    if not match:
        # No newline after the opening brace: either compact, or a single-line file. Compact is
        # the only reading that reproduces it, and getting this wrong is visible in the
        # re-serialised size the summary prints beside the disk size.
        return None if re.match(r"^[\s﻿]*[{\[]\S", text) else 2
    lead = match.group(1)
    if "\t" in lead:
        return "\t"
    # A newline with nothing after it is indent=0, which json.dump writes and which is NOT the
    # same as compact: returning None there would strip every newline out of the slice and make
    # it undiffable against the plan it came from. Zero is falsy, so this must not be written as
    # `len(lead) if lead else ...`.
    return len(lead)


def _dumps(obj: object, indent: int | str | None = 2) -> str:
    """One serialiser for both sides of every size comparison, in the source plan's own format.

    The trailing newline matches what the skill's own writers produce. `separators` is set
    explicitly for the compact case because json.dumps defaults to ", " / ": " when indent is
    None, which is neither pretty nor compact.
    """
    if indent is None:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n"
    return json.dumps(obj, ensure_ascii=False, indent=indent) + "\n"


def _human(count: int) -> str:
    return f"{count:,}"


def _keys(count: int) -> str:
    """"1 top-level key" / "3 top-level keys". A gate that cannot count in its own summary line
    is a gate people stop reading closely, and this summary is the artifact a reader checks."""
    return f"{count} top-level key" + ("" if count == 1 else "s")


def _wrap(text: str, indent: str) -> str:
    return textwrap.fill(text, width=96, initial_indent=indent, subsequent_indent=indent)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", help="Plan JSON path")
    # No `choices=`: the two auditor names need an explanation, not a usage line. See AUDITORS.
    parser.add_argument("--domain", required=True,
                        help="One of: " + ", ".join(DOMAINS))
    parser.add_argument("--out", default=None,
                        help="Where to write the slice (default: "
                             "slices/<plan-stem>.slice-<domain>.json, in a slices/ directory "
                             "beside the plan)")
    parser.add_argument("--stdout", action="store_true",
                        help="Write the slice JSON to stdout and the summary to stderr, for "
                             "piping. Without it the slice goes to a file and the summary to "
                             "stdout.")
    args = parser.parse_args()

    domain = str(args.domain).strip()
    if domain in AUDITORS:
        print(f"ERROR: {domain!r} is an AUDITOR, not one of the five truth domains, and it is "
              f"never given a slice: {AUDITORS[domain]}. Removing a block would not make that "
              f"cheaper, it would make it wrong. Hand both auditors the plan path itself. "
              f"[see references/verification.md#plan-slice]", file=sys.stderr)
        return 2
    if domain not in ALL_FIVE:
        print(f"ERROR: unknown domain {domain!r}. The five truth domains are: "
              f"{', '.join(DOMAINS)}. They are fixed by the report schema -- "
              f"check_plan_consistency.py rejects a report naming any other domain. "
              f"[see references/verification.md#report-schema]", file=sys.stderr)
        return 2

    source = Path(args.plan)
    try:
        raw = source.read_bytes()
    except Exception as exc:  # noqa: BLE001 - surfaced verbatim to the operator
        print(f"ERROR: could not read plan {args.plan!r}: {exc}", file=sys.stderr)
        return 2
    try:
        plan = json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: could not parse plan JSON: {exc}", file=sys.stderr)
        return 2

    if not isinstance(plan, dict):
        print(f"ERROR: plan JSON must be an object, got {type(plan).__name__}. A bare list is not "
              f"a plan, and slicing one by top-level key is meaningless.", file=sys.stderr)
        return 2

    # Slicing a slice would compound one projection on another and record a source_plan that is
    # itself already missing blocks -- a provenance chain that reads as if the full plan had been
    # consulted. Refuse, and say which file to use instead.
    if RECORD_KEY in plan:
        existing = plan.get(RECORD_KEY)
        origin = existing.get("source_plan") if isinstance(existing, dict) else None
        print(f"ERROR: {args.plan!r} already carries a {RECORD_KEY!r} block, so it is a slice, not "
              f"a plan. Slicing it again would drop blocks that were already dropped and claim "
              f"this file as the source."
              + (f" Slice the plan it came from: {origin!r}." if origin else ""), file=sys.stderr)
        return 2

    # A plan with no itinerary is the wrong file, and this is how that mistake arrives: the
    # workspace's plans/ directory also holds intake JSON, discovery shortlists and next-action
    # files, and every one of them parses as an object. Every domain dates its claims against the
    # day cards, so a slice built from a file with no days would hand a verifier something it
    # cannot check and no error would say why.
    days = plan.get("days")
    if not isinstance(days, list) or not days:
        kind = "missing" if "days" not in plan else f"{type(days).__name__}, length " \
            f"{len(days) if isinstance(days, (list, dict, str)) else 'n/a'}"
        print(f"ERROR: this plan has no day cards (days is {kind}). Every verification domain "
              f"dates its claims against the itinerary -- an entry rule against the arrival date, "
              f"a fare against the planned weekday, an opening time against the day it is "
              f"scheduled -- so a slice of a file with no days is not something a verifier can "
              f"work from. If this is an intake, a shortlist or a next-action file rather than a "
              f"plan, it is the wrong input.", file=sys.stderr)
        return 2

    sliced, report = slice_plan(plan, domain)
    digest = hashlib.sha256(raw).hexdigest()
    record = _record(domain, source, digest, len(raw), report)
    # First key, so an agent that reads the top of the file learns it is holding a projection
    # before it reads a single claim. Everything after it is in the plan's own order.
    payload = {RECORD_KEY: record, **sliced}

    plan_text = raw.decode("utf-8")
    indent = detect_indent(plan_text)
    slice_text = _dumps(payload, indent)
    # Two baselines, both printed, because they answer different questions. The disk size is what
    # the verifier would otherwise have opened -- the honest cost comparison. The re-serialised
    # size is the like-for-like one: if the two differ, the plan on disk is not written the way
    # json.dump writes it, and part of any percentage against the disk size would be formatting.
    disk_size = len(raw)
    full_size = len(_dumps(plan, indent).encode("utf-8"))
    slice_size = len(slice_text.encode("utf-8"))
    # Signed as a delta from the full plan, so the two figures never disagree about direction. A
    # slice can legitimately be BIGGER: on a plan whose droppable blocks are all absent, the
    # provenance block is added and nothing comes out, and a "+430 bytes (-0.5%)" line would be
    # the tool lying about its own result.
    delta = slice_size - full_size
    percent = (100.0 * delta / full_size) if full_size else 0.0

    beside_the_plan = False
    if args.stdout:
        out_path = None
        sys.stdout.write(slice_text)
        summary = sys.stderr
    else:
        # Default into a slices/ SUBDIRECTORY, not beside the plan, and the reason is a defect
        # this would otherwise ship: audit_workspace.py identifies a plan by its shape -- a dict
        # with a `days` list and a `trip` key -- over a non-recursive plans/*.json glob, and its
        # filename filter is a prefix list a slice does not match. A slice has both of those keys,
        # so five slices dropped beside a plan become five extra "plans" in every later audit,
        # each reported as an itinerary missing blocks it was never supposed to have. A
        # subdirectory is invisible to that glob and to trip_timer.py's.
        out_path = Path(args.out) if args.out else (
            source.parent / "slices" / f"{source.stem}.slice-{domain}.json")
        try:
            out_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: could not create the directory for {out_path}: {exc}", file=sys.stderr)
            return 2
        # The one destructive mistake available here, and it destroys the input: --out pointed at
        # the plan would overwrite a booking-ready itinerary with a projection of itself, and the
        # blocks it dropped would be gone from the only copy.
        try:
            same = out_path.resolve() == source.resolve()
        except OSError:  # a path that cannot be resolved is not the source file
            same = False
        if same:
            print(f"ERROR: --out points at the plan itself ({out_path}). Writing the slice there "
                  f"would overwrite the plan with a projection of itself and lose every dropped "
                  f"block. Pick another path.", file=sys.stderr)
            return 2
        # An explicit --out into the plan's own directory reopens the hole the default avoids, and
        # it is the caller's decision, so it is warned about rather than refused.
        try:
            beside_the_plan = out_path.resolve().parent == source.resolve().parent
        except OSError:
            beside_the_plan = False
        try:
            out_path.write_text(slice_text, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: could not write slice to {out_path}: {exc}", file=sys.stderr)
            return 2
        summary = sys.stdout

    print(f"plan slice for domain '{domain}'", file=summary)
    print(f"  source   {source} ({_human(len(raw))} bytes on disk, sha256 {digest[:12]}...)",
          file=summary)
    print(f"  wrote    {out_path if out_path else '<stdout>'}", file=summary)
    print("", file=summary)
    print(f"  kept     {_keys(len(report['kept']))}: {', '.join(report['kept'])}",
          file=summary)

    if report["dropped"]:
        print(f"  dropped  {_keys(len(report['dropped']))} that this plan carried:",
              file=summary)
        for key in report["dropped"]:
            block_size = len(_dumps({key: plan[key]}).encode("utf-8"))
            print(f"    - {key}  ({_human(block_size)} bytes)", file=summary)
            print(_wrap(IRRELEVANT_TO[key][1], "        "), file=summary)
    else:
        print(f"  dropped  nothing: every block this plan carries is read by '{domain}'.",
              file=summary)

    if report["absent_from_plan"]:
        print(f"  n/a      dropped by '{domain}' but absent from this plan (no saving): "
              f"{', '.join(report['absent_from_plan'])}", file=summary)

    # Loud, not silent, and on the summary stream rather than buried: a key nobody has classified
    # is kept, which is safe, but it is also the signal that this table is behind the schema.
    if report["unrecognised_kept"]:
        print("", file=summary)
        print(f"  NOTE     kept {_keys(len(report['unrecognised_kept']))} this script "
              f"does not recognise: {', '.join(report['unrecognised_kept'])}", file=summary)
        print(_wrap("A deny list keeps what it has not classified, so these travel with every "
                    "slice and no domain is starved by a schema that grew. If one of them is "
                    "provably irrelevant to a domain, add it to IRRELEVANT_TO in this script with "
                    "the reason; if every domain reads it, add it to KEPT_EVERYWHERE_BECAUSE.",
                    "           "), file=summary)

    if beside_the_plan:
        print("", file=summary)
        print(f"  WARNING  this slice is being written into the plan's own directory.",
              file=summary)
        print(_wrap("A slice carries a `days` list and a `trip` key, which is exactly how "
                    "audit_workspace.py recognises a plan -- so a slice sitting in plans/ is "
                    "audited as an itinerary and reported as one missing blocks it was never "
                    "supposed to have. The default location, slices/ beside the plan, is outside "
                    "that non-recursive glob.", "           "), file=summary)

    if report["missing_mandatory"]:
        print("", file=summary)
        print(f"  WARNING  this plan has no {', '.join(report['missing_mandatory'])} block. Those "
              f"are kept unconditionally by every domain, so nothing was dropped on their "
              f"account -- but a plan missing one of them is a plan the verifier cannot fully "
              f"check, and that is worth knowing before the fan-out rather than after.",
              file=summary)

    shown_indent = "compact" if indent is None else (
        "tabs" if indent == "\t" else f"indent={indent}")
    print("", file=summary)
    print(f"  size     {_human(disk_size)} bytes on disk -> {_human(slice_size)} bytes of slice, "
          f"{slice_size - disk_size:+,} ({100.0 * (slice_size - disk_size) / disk_size:+.1f}%) "
          f"for the file a verifier opens", file=summary)
    print(_wrap(f"The slice is written the way this plan is written ({shown_indent}), so the "
                f"figure is a content difference and not a re-indent. Serialised through this "
                f"script the plan is {_human(full_size)} bytes"
                # A byte or two apart is a trailing newline, not a formatting mismatch worth
                # warning about; a real mismatch means part of any percentage against the disk
                # size would be re-indentation, and then the like-for-like number has to be shown.
                + (", the same as on disk." if full_size == disk_size else
                   f", matching the {_human(disk_size)} on disk to within "
                   f"{abs(full_size - disk_size)} bytes."
                   if abs(full_size - disk_size) <= max(8, disk_size // 1000) else
                   f" against {_human(disk_size)} on disk, so the plan carries formatting this "
                   f"script does not reproduce exactly; the like-for-like difference is "
                   f"{delta:+,} ({percent:+.1f}%).")
                + " Token counts fall in the same proportion for text of the same composition; "
                  "this script prints bytes because it has no tokenizer and will not print a "
                  "number it cannot measure.", "           "), file=summary)

    # A projection that costs more than it saves, said out loud. Measured 2026-08-30 across the
    # 15 workspace plans x 5 domains: 13 of those 75 slices came out LARGER than the plan on
    # disk -- all five domains on each of the two smallest plans, and single domains on two more
    # -- because the provenance block is a fixed cost and a small plan carries almost none of the
    # droppable blocks. The slice is still correct, every kept pointer resolves, but handing it
    # to a verifier spends tokens to save none, and a tool that reports a null result in the
    # same shape as a real saving is how a null result gets quoted as a win.
    #
    # Triggered on the DISK comparison, not the like-for-like one, because the disk file is what a
    # verifier would otherwise have opened and therefore what the fan-out actually pays.
    if slice_size >= disk_size:
        print("", file=summary)
        print(f"  WARNING  this slice is NOT smaller than the plan.", file=summary)
        print(_wrap(f"This file carries little or none of what '{domain}' drops, so the "
                    f"projection adds {_human(slice_size - disk_size)} bytes and saves nothing. Hand "
                    f"this domain the plan path itself and spend the tokens on the fan-out "
                    f"instead. The slice was still written and every kept pointer in it still "
                    f"resolves, in case you want one shape for all five.", "           "),
              file=summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
