#!/usr/bin/env python3
"""Save a Discovery shortlist through its gate, the way Construction saves a plan.

Usage: python save_discovery_deliverables.py <shortlist.json> [--workspace PATH] [--slug NAME]
                                             (--intake PATH | --no-intake) [--overwrite]

WHY THIS FILE EXISTS, measured rather than argued. check_shortlist_consistency.py is the largest
gate in this skill after the plan checker -- it refuses a winner that fails a hard constraint, a winner named
when no candidate was feasible, a candidate scored with no evidence under it, a cost figure priced
per person beside one priced for the whole party, and an outcome.state that contradicts the pool it
claims to describe. In a real workspace holding fifteen saved intakes, the number of shortlist JSON
files is ZERO. That gate has never run on a single real Discovery, and none of what it refuses has
ever been refused.

The asymmetry that explains it is structural, not a matter of anyone forgetting. Construction has
exactly one mandatory door: save_trip_deliverables.py validates, runs every consistency check,
renders, validates the page, writes two files and PRINTS THEIR PATHS -- and those printed paths are
the only outward sign the gates ran at all, which is why SKILL.md makes a Construction task
incomplete without them. Discovery had no door. Its gate was a command in a paragraph, its output
was a JSON file nobody was told to write anywhere in particular, and the run that skipped both
looked exactly like the run that did neither. A shortlist presented as chat prose is not a worse
artifact than a saved one; it is an artifact no gate has ever seen.

So this is the smallest thing that makes a Discovery run observable: it takes the shortlist through
the same gate, records what ran, writes it where the traveller's other artifacts live, and prints
the path. That last part is not bookkeeping -- it is the receipt, and the reason SKILL.md's quality
gate can now name check_shortlist_consistency.py in a bullet a reader can check.

WHAT THIS DELIBERATELY DOES NOT DO. There is no HTML here. Construction renders a page because the
traveller books from it, standing in a city with a phone; a shortlist is a decision aid the
traveller reads once, in the conversation, and inventing a page for it would mean inventing a
renderer, a contract and a validator for an artifact nobody has asked to hold. The saved JSON is the
record; the comparison the traveller reads is the answer in the conversation. If that changes, the
place to add it is here, beside the gate that already knows the shape.

And it does not license deferring anything. Saving a shortlist says a Discovery ran and passed its
gate. It says nothing about whether the trip should now be built, which is the traveller's decision
and stays in the conversation where it belongs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from check_shortlist_consistency import (  # noqa: E402
    SHORTLIST_CHECKS,
    check_constraint_coverage,
)
from travel_workspace import DEFAULT_WORKSPACE  # noqa: E402


def gates_stamp(intake_used: bool) -> dict:
    """What this shortlist was checked against, recorded so a later audit can tell two things apart.

    The same reasoning as check_plan_consistency.gates_stamp, and the same deliberate absence of a
    wall-clock: two saves of one shortlist have to be diffable, so nothing here changes between
    runs. `constraint_coverage` is carried separately from the count because it is the one check
    that can be armed or not, and a stamp that said only "11 checks" would report the disarmed run
    and the armed one identically -- which is the shape of every hole this skill has had to close.
    """
    return {
        "checks": len(SHORTLIST_CHECKS) + 1,
        "checked_by": "check_shortlist_consistency.SHORTLIST_CHECKS",
        "constraint_coverage": "armed" if intake_used else "not run",
    }


def slug_for(doc: dict) -> str:
    """A stable name from the shortlist's own fields, so two saves of one run collide.

    Colliding is the point: --overwrite then has to be typed, which is how a second save announces
    itself instead of quietly becoming a second artifact. The measured version of that failure is
    in SKILL.md -- two plans in one workspace differing only by origin, one of them wrong, and
    nothing to tell a reader which was which.
    """
    context = doc.get("trip_context")
    context = context if isinstance(context, dict) else {}
    parts = [str(context.get(key) or "").strip()
             for key in ("start_date", "origin", "scope_label")]
    name = "-".join(part for part in parts if part)
    return name or "discovery-shortlist"


def safe_name(text: str) -> str:
    """Filesystem-safe without being ASCII-only: the workspace this runs on is majority CJK."""
    cleaned = "".join("-" if character in '/\\:*?"<>|' or character.isspace() else character
                      for character in text)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-. ") or "discovery-shortlist"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("shortlist", help="Discovery shortlist JSON path")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE),
                        help="Output root; the shortlist is written to its plans/ folder")
    parser.add_argument("--slug", default=None,
                        help="Stable output name; defaults to the shortlist's own trip_context")
    parser.add_argument("--intake", default=None,
                        help="Saved trip intake JSON. Supplying it arms the constraint-coverage "
                             "check against what the traveller actually declared.")
    parser.add_argument("--no-intake", action="store_true",
                        help="Save without that check, when no saved intake exists. Records the "
                             "gap in the saved file instead of leaving a silent exit 0.")
    parser.add_argument("--overwrite", action="store_true",
                        help="Replace an existing file of the same name")
    args = parser.parse_args()

    # Copied in shape from check_shortlist_consistency.py's own refusal, and for its reason: an
    # exit 0 is what an assistant reads, so the one check that catches a winner never tested
    # against a stated constraint must not be skippable by saying nothing.
    if not args.intake and not args.no_intake:
        print(
            "ERROR: No --intake. Pass the saved intake JSON "
            "(<workspace>/plans/intake-<stamp>-<slug>.json) so the hard-constraint roster is "
            "computed from what the traveller actually declared, or pass --no-intake to save "
            "without it and record the gap in the file. A shortlist saved without it has NOT been "
            "tested against the traveller's own requirements, and nothing in the artifact would "
            "have said so.", file=sys.stderr)
        return 1
    if args.intake and args.no_intake:
        print("ERROR: --intake and --no-intake are two answers to one question. Pass one.",
              file=sys.stderr)
        return 1

    try:
        doc = json.loads(Path(args.shortlist).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: Could not read shortlist JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(doc, dict):
        print("ERROR: shortlist JSON must be an object.", file=sys.stderr)
        return 2

    intake = None
    if args.intake:
        try:
            intake = json.loads(Path(args.intake).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: Could not read intake JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(intake, dict):
            print("ERROR: intake JSON must be an object.", file=sys.stderr)
            return 2

    errors: list[str] = []
    notes: list[str] = []
    for check in SHORTLIST_CHECKS:
        check(doc, errors, notes)
    check_constraint_coverage(doc, errors, notes, intake=intake)

    for note in notes:
        print(f"note: {note}")
    if errors:
        print("SHORTLIST CONSISTENCY FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        print("Nothing was written. Fix these and run again -- a shortlist that cannot pass its "
              "own gate is not a comparison, it is a list.", file=sys.stderr)
        return 1

    # Stamped only after the gate passed, so the stamp cannot outlive the thing it attests. The
    # NO INTAKE case is recorded IN THE FILE and not merely printed, because the note scrolls past
    # and the file is what a later audit reads.
    doc["gates_passed"] = gates_stamp(intake is not None)

    workspace = Path(args.workspace).expanduser()
    plans = workspace / "plans"
    try:
        plans.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: Could not create {plans}: {exc}", file=sys.stderr)
        return 2

    name = safe_name(args.slug or slug_for(doc))
    destination = plans / f"shortlist-{name}.json"
    if destination.exists() and not args.overwrite:
        print(f"ERROR: {destination} already exists. Choose a new --slug or pass --overwrite.",
              file=sys.stderr)
        return 2
    try:
        destination.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    except OSError as exc:
        print(f"ERROR: Could not write {destination}: {exc}", file=sys.stderr)
        return 2

    # The receipt. This line is the only outward sign the gate ran, exactly as save_trip_
    # deliverables.py's two paths are for Construction -- report it rather than paraphrasing it.
    print(f"Shortlist JSON: {destination}")
    if intake is None:
        print("note: saved with --no-intake, and the file says so in gates_passed. This shortlist "
              "has NOT been tested against the hard constraints the traveller stated -- say that "
              "when you present it, and do not describe a winner as having cleared their "
              "requirements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
