#!/usr/bin/env python3
"""Which parts of a plan a verification pass covered, fingerprinted so a later edit is visible.

A verified plan edited afterwards used to keep its verified status: the report bound the plan by
file name and date, never by content. Measured 2026-09-24 on a copy of the one verified real plan
in the author's workspace: a day's 13:30 moved to 14:00, re-saved with the same report -- saved, no
banner, and the page printed 14:00 under a verification that never saw it.

The fingerprint is per SECTION rather than per file, and that is the design decision, not a detail.
A whole-file fingerprint would close the hole by making every edit cost the full seven-block pass
again -- which is exactly what a traveller asking to swap one dinner should not have to buy. Per
section, the gate can say which part moved, the verifier can recheck that part alone, and every
other part keeps the verification it already has.

Sections are keyed by identity, not by position: a day by its date, a booking option by its id,
every other content block by its name. Reordering the hotels, or inserting a day, therefore changes
only what actually changed. Keys the skill's own scripts write -- the verification status, the gate
stamp, the imagery sidecar name, this receipt -- describe the run rather than the trip, and are
never part of a fingerprint.
"""

from __future__ import annotations

import hashlib
import json
import re
import shlex
import sys
from pathlib import Path

META_KEYS = frozenset({
    "verification_status", "verification_report", "verification_receipt", "gates_passed",
    "generated_at", "imagery_sidecar", "imagery", "intake_context", "ui_labels", "_contract",
    "_enums", "plan_status", "replan_context", "profile_context",
    # bookings: the traveller's decisions (scripts/bookings.py) -- not research, never re-verified.
    "bookings",
})
BOOKING_KINDS = ("flights", "ground_transport", "accommodations", "attraction_tickets",
                 "rental_cars")

# The trip facts each kind of section was verified against. Walked on 2026-09-24: a party that
# grew from four to five after a verified save was rechecked as "trip" alone and re-saved verified,
# every hotel card still roomed and priced for four and its search link still for 2 adults + 2
# children. No card's own text had changed, so no card's fingerprint had either. Folding these
# facts into the fingerprint of each section that depends on them moves that section when they
# change, and the gate then asks for its recheck like any other edit.
#   traveler_count        -- rooms, fares, seats, tickets and tables are bought for a number of people,
#                            and the entry answer is about who travels: one more person is one more
#                            passport to check
#   traveler_constraints  -- a new allergy or walking limit re-opens every meal, walk and room
DEPENDS_ON = {
    "days": ("traveler_count", "traveler_constraints"),
    "booking_options": ("traveler_count", "traveler_constraints"),
    "budget": ("traveler_count",),
    "transport_overview": ("traveler_count", "traveler_constraints"),
    "entry_context": ("traveler_count",),
}
# Every digest names the scheme that made it. A receipt stamped before the dependencies existed
# holds plain digests of each section alone, and is compared the way it was made (see
# changed_sections) rather than reported as "changed" everywhere on its next save.
SCHEME = "v2:"


def _digest(value: object) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _root(section: str) -> str:
    return re.split(r"[.\[]", section, maxsplit=1)[0]


def _depends_on(plan: dict, section: str) -> dict | None:
    fields = DEPENDS_ON.get(_root(section))
    if not fields:
        return None
    trip = plan.get("trip") if isinstance(plan.get("trip"), dict) else {}
    return {field: trip.get(field) for field in fields}


def _empty(value: object) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _day_key(day: object, index: int) -> str:
    date = day.get("date") if isinstance(day, dict) else None
    return f"days[{date.strip()}]" if isinstance(date, str) and date.strip() else f"days[#{index}]"


def _option_key(kind: str, option: object, index: int) -> str:
    option_id = option.get("id") if isinstance(option, dict) else None
    if isinstance(option_id, str) and option_id.strip():
        return f"booking_options.{kind}[{option_id.strip()}]"
    return f"booking_options.{kind}[#{index}]"


def _roots(plan: dict):
    """(pointer, section key, value) for every section, in plan order."""
    for key, value in plan.items():
        if key in META_KEYS:
            continue
        if key == "days" and isinstance(value, list):
            for index, day in enumerate(value):
                yield f"days[{index}]", _day_key(day, index), day
        elif key == "booking_options" and isinstance(value, dict):
            for kind, items in value.items():
                if kind in BOOKING_KINDS and isinstance(items, list):
                    for index, option in enumerate(items):
                        yield (f"booking_options.{kind}[{index}]",
                               _option_key(kind, option, index), option)
                else:
                    yield f"booking_options.{kind}", f"booking_options.{kind}", items
        else:
            yield key, key, value


def sections(plan: dict) -> dict[str, object]:
    return {section: value for _, section, value in _roots(plan)}


def section_digests(plan: dict) -> dict[str, str]:
    digests = {}
    for section, value in sections(plan).items():
        # An empty section depends on nothing: there is nothing in it to have been checked.
        context = None if _empty(value) else _depends_on(plan, section)
        body = value if context is None else {"section": value, "depends_on": context}
        digests[section] = SCHEME + _digest(body)
    return digests


def digest_is_current(plan: dict, section: str, digest: object) -> bool:
    """Whether `digest` -- stamped in a receipt or carried by a recheck -- still describes the
    section as it is now. A plain digest predates SCHEME and covered the section alone."""
    if not isinstance(digest, str) or not digest.strip():
        return False
    digest = digest.strip()
    if digest.startswith(SCHEME):
        return section_digests(plan).get(section) == digest
    # A plain digest saw the section alone, so it cannot vouch for a section that depends on the
    # party or the constraints: those may have changed since, and nothing it recorded would show.
    if _root(section) in DEPENDS_ON:
        return False
    value = sections(plan).get(section)
    return value is not None and _digest(value) == digest


def changed_sections(stamped: dict, plan: dict) -> tuple[list[str], list[str]]:
    """(changed or added, removed) between a stamped receipt and the plan as it is now.

    A section emptied since the stamp counts as removed: nothing in it is left to verify, and a
    recheck of it could cite no pointer -- the gate refused exactly that recheck as "checked
    nothing", which left a full re-verification as the only way out.
    """
    current = sections(plan)
    digests = section_digests(plan)
    plain_trip = stamped.get("trip")
    # For a receipt made before the dependencies: the whole trip block is all it can say about the
    # facts a section depends on, so a changed trip moves every dependent section.
    trip_moved = (isinstance(plain_trip, str) and not plain_trip.startswith(SCHEME)
                  and plain_trip != _digest(current.get("trip")))
    changed: list[str] = []
    removed = [key for key in stamped if key not in current]
    for key, value in current.items():
        stamp = stamped.get(key)
        plain = isinstance(stamp, str) and bool(stamp) and not stamp.startswith(SCHEME)
        same = stamp == (_digest(value) if plain else digests[key])
        if _empty(value):
            if stamp is not None and not same:
                removed.append(key)
            continue
        if not same or (plain and trip_moved and _root(key) in DEPENDS_ON):
            changed.append(key)
    return sorted(changed), sorted(removed)


_INDEXED = re.compile(r"^(days|booking_options\.([A-Za-z_]+))\[(\d+)\]")


def section_of_pointer(plan: dict, pointer: str) -> str | None:
    """The section a claims_checked pointer falls in: days[2].dining[1] -> days[2026-10-14]."""
    match = _INDEXED.match(pointer)
    if match:
        index = int(match.group(3))
        if match.group(1) == "days":
            days = plan.get("days") if isinstance(plan.get("days"), list) else []
            return _day_key(days[index], index) if index < len(days) else None
        kind = match.group(2)
        options = plan.get("booking_options") if isinstance(plan.get("booking_options"), dict) else {}
        items = options.get(kind)
        if kind in BOOKING_KINDS and isinstance(items, list) and index < len(items):
            return _option_key(kind, items[index], index)
        return None
    head = re.split(r"[.\[]", pointer, maxsplit=1)[0]
    if head == "booking_options":
        kind = re.split(r"[.\[]", pointer[len("booking_options."):], maxsplit=1)[0]
        return f"booking_options.{kind}" if kind else None
    return head if head and head not in META_KEYS else None


def section_pointers(plan: dict, section: str) -> list[str]:
    """One pointer per direct child of a section: where a recheck of it starts looking."""
    for pointer, key, value in _roots(plan):
        if key != section:
            continue
        if isinstance(value, dict):
            return [f"{pointer}.{child}" for child in value]
        if isinstance(value, list):
            return [f"{pointer}[{index}]" for index in range(len(value))]
        return [pointer]
    return []


# ----------------------------------------------------------------------------------------------
# The recheck loop's next steps, printed as commands that run as printed.
#
# Walked literally on 2026-09-24 with nothing but what the scripts said: re-saving the delivered
# copy was told to buy a full verification, the gate's recheck command carried <plan.json> and
# <report.json> placeholders, the scaffold it named wrote the amended report to standard output and
# saved nothing, and the line after that pointed at the checker instead of the save that closes the
# loop. An assistant that cannot hold the whole skill in view rebuilds the order from whatever the
# last command printed, so what it prints has to run: this interpreter, each script by absolute
# path, every argument quoted -- the default workspace, ~/Travel Buddy, has a space in it.
SCRIPTS = Path(__file__).resolve().parent
_DATED_STEM = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")


def command_line(script: str, *args: object) -> str:
    return shlex.join([sys.executable, str(SCRIPTS / script), *(str(arg) for arg in args)])


def delivered_workspace(path: object) -> Path | None:
    """The workspace a delivered plan lives in -- <workspace>/plans/<start>-<slug>.json -- or None.

    A delivered plan's workspace also holds its page in html/: any other folder that happens to be
    called "plans" is not one, and a save printed for it would deliver a second copy there.
    """
    if not path or str(path) == "-":
        return None
    resolved = Path(str(path)).expanduser().resolve()
    if resolved.parent.name != "plans" or not (resolved.parent.parent / "html").is_dir():
        return None
    return resolved.parent.parent


def delivered_slug(path: object) -> str | None:
    """The slug of a delivered plan, read from its own file name (<start date>-<slug>.json)."""
    if delivered_workspace(path) is None:
        return None
    match = _DATED_STEM.match(Path(str(path)).stem)
    return match.group(1) if match else None


def recheck_command(plan_path: object, report_path: object, receipt_from: object = None) -> str:
    """The scaffold that appends this plan's rechecks to the report, amending it in place."""
    plan = Path(str(plan_path)).expanduser().resolve()
    report = Path(str(report_path)).expanduser().resolve()
    extra: list[object] = []
    if receipt_from and Path(str(receipt_from)).expanduser().resolve() != plan:
        extra = ["--receipt-from", Path(str(receipt_from)).expanduser().resolve()]
    return command_line("new_verification_report.py", "--recheck", "--from-plan", plan,
                        "--report", report, "--out", report, *extra)


def resave_command(plan_path: object, report_path: object, receipt_from: object = None) -> str:
    """The save that replaces the delivered copy and closes the loop, or "" when this cannot tell
    which workspace the plan was delivered to."""
    plan = Path(str(plan_path)).expanduser().resolve()
    delivered = receipt_from or plan
    workspace = delivered_workspace(delivered)
    if workspace is None:
        return ""
    args: list[object] = [plan, "--workspace", workspace]
    # Always named when known: a working copy inside plans/ under an undated name infers no slug,
    # and without one the save wrote the edit as a second plan beside the verified one.
    slug = delivered_slug(delivered)
    if slug:
        args += ["--slug", slug]
    args += ["--overwrite", "--verification", Path(str(report_path)).expanduser().resolve()]
    return command_line("save_trip_deliverables.py", *args)
