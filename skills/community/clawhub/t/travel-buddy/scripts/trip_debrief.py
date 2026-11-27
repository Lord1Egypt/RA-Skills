#!/usr/bin/env python3
"""After the trip: ask how it went, keep what it teaches in the profile, move the plan aside.

Usage:
    python trip_debrief.py list   [--workspace PATH] [--today YYYY-MM-DD]
    python trip_debrief.py record <plan.json> --profile <profile.json> --answers <answers.json>
                                  [--workspace PATH] [--today YYYY-MM-DD]
    python trip_debrief.py skip   --profile <profile.json> [--workspace PATH] [--today YYYY-MM-DD]

WHY THIS EXISTS
---------------
A workspace held 14 saved plans and no record of how any of them went. Trips to Tokyo, Beijing,
Malaga and Cologne had ended weeks earlier and still sat beside the upcoming ones. Nothing asked
whether 30 minutes of walking had been too much or the hotel too far out, so the next plan was
built on the same guesses. The intake form already pre-fills from the profile (pace, places not
to revisit, things to avoid), so a lesson written there reaches the next trip with no other change.

WHAT IT DOES (no model, no network)
-----------------------------------
`list` prints the most recent saved plan whose end date has passed and that no profile has a
debrief for, as one `ASK:` line, and counts the older ones. Ask about that one trip once, in the
first reply of the session, and offer to skip the rest: twelve finished trips in one workspace
would otherwise mean twelve rounds of questions. `skip` records a skip for every one of them
except the most recent (record that one with `"went": "skip"` if the traveller skips it too).

`record` reads the answers (templates/trip-debrief.json) and, in the profile:
- appends the debrief to `travel_history.trip_debriefs`;
- records the destination in `visited_places` with the traveller's `revisit` answer
  (`no` keeps it off future shortlists);
- adds `new_avoid` to `recurring_preferences.avoid_list` and `new_comfort` to
  `comfort_and_safety_preferences`, and sets `pace` when the traveller named a new one.
Then it moves the plan's files (plans/<stem>*, html/<stem>*) into `past/` folders, unless the
traveller chose to skip. An answer of `skip` is recorded too, so the trip is not asked about again.
The profile is validated before and after; nothing is written if it would fail.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from travel_workspace import DEFAULT_WORKSPACE, validate_profile  # noqa: E402

WENT = {"yes", "no", "skip"}
REVISIT = {"yes", "no", "maybe", "unknown"}
PACES = {"慢游/深度", "适中", "高密度多点"}   # the profile form's own values (assets/traveler-profile-intake.html)


def _plan_trip(path: Path) -> dict | None:
    """The `trip` block of a final plan, or None for intake, shortlist and report files."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict) or not isinstance(data.get("trip"), dict) or not isinstance(data.get("days"), list):
        return None
    return data["trip"]


def debriefed(workspace: Path) -> set[str]:
    done: set[str] = set()
    for profile in sorted((workspace / "profiles").glob("*.json")):
        try:
            history = json.loads(profile.read_text(encoding="utf-8")).get("travel_history") or {}
        except (OSError, ValueError, AttributeError):
            continue
        done |= {str(d.get("plan")) for d in history.get("trip_debriefs") or [] if isinstance(d, dict)}
    return done


def past_trips(workspace: Path, today: dt.date) -> list[tuple[Path, dict]]:
    out = []
    for path in sorted((workspace / "plans").glob("*.json")):
        trip = _plan_trip(path)
        end = str((trip or {}).get("end_date") or "")[:10]
        try:
            ended = dt.date.fromisoformat(end) < today
        except ValueError:
            continue
        if ended:
            out.append((path, trip))
    return out


def cmd_list(workspace: Path, today: dt.date) -> int:
    done = debriefed(workspace)
    ask = waiting(workspace, today)
    if not ask:
        print("No finished trip is waiting for a debrief.")
        return 0
    path, trip = ask[0]
    print(f"ASK: {path} ({trip.get('destination')}, {trip.get('start_date')} to {trip.get('end_date')})")
    if len(ask) > 1:
        print(f"OLDER: {len(ask) - 1} more finished trip(s) without a debrief; not asked about. "
              f"Offer 'skip the rest': python scripts/trip_debrief.py skip --profile <profile.json>")
    print("Ask once, briefly, and accept 'skip': did you go, would you go back, what worked, what did "
          "not (pace, walking, hotel, food, budget). Record with: python scripts/trip_debrief.py record "
          "<plan.json> --profile <profile.json> --answers <answers.json> (templates/trip-debrief.json)")
    return 0


def waiting(workspace: Path, today: dt.date) -> list[tuple[Path, dict]]:
    """Finished trips no profile has a debrief for, most recent first."""
    done = debriefed(workspace)
    ask = [(p, t) for p, t in past_trips(workspace, today) if p.stem not in done]
    return sorted(ask, key=lambda pt: str(pt[1].get("end_date")), reverse=True)


def cmd_skip(args, today: dt.date) -> int:
    workspace = Path(args.workspace).expanduser()
    profile_path = Path(args.profile)
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    errors = validate_profile(profile)
    if errors:
        print("ERROR: the profile is not valid: " + " ".join(errors), file=sys.stderr)
        return 2
    trips = waiting(workspace, today)[1:]   # the most recent one is the one being asked about
    for path, trip in trips:
        apply(profile, path.stem, trip, {"went": "skip"}, today)
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PROFILE travel_history.trip_debriefs: {len(trips)} older finished trip(s) recorded as skipped")
    return 0


def _strings(value: object, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ValueError(f"{field} must be a list of strings")
    return [v.strip() for v in value if v.strip()]


def apply(profile: dict, plan_stem: str, trip: dict, answers: dict, today: dt.date) -> list[str]:
    """Write the debrief into the profile; returns what changed, one line each."""
    went = answers.get("went")
    if went not in WENT:
        raise ValueError(f"went must be one of {sorted(WENT)}, not {went!r}")
    revisit = answers.get("revisit")
    if revisit is not None and revisit not in REVISIT:
        raise ValueError(f"revisit must be one of {sorted(REVISIT)} or null, not {revisit!r}")
    pace = answers.get("pace")
    if pace is not None and pace not in PACES:
        raise ValueError(f"pace must be one of {sorted(PACES)} or null, not {pace!r}")
    avoid, comfort = _strings(answers.get("new_avoid"), "new_avoid"), _strings(answers.get("new_comfort"), "new_comfort")
    history = profile.setdefault("travel_history", {})
    prefs = profile.setdefault("recurring_preferences", {})
    changes = []
    entry = {"plan": plan_stem, "destination": trip.get("destination"),
             "dates": f"{trip.get('start_date')} to {trip.get('end_date')}", "went": went,
             "recorded_at": today.isoformat()}
    if went != "skip":
        entry.update({k: answers.get(k) for k in ("revisit", "worked", "did_not_work", "spent_per_person", "currency")
                      if answers.get(k) not in (None, "")})
    history.setdefault("trip_debriefs", []).append(entry)
    changes.append(f"travel_history.trip_debriefs: + {plan_stem} ({went})")
    if went == "yes":
        place = str(trip.get("destination") or "").strip()
        visited = [v for v in history.setdefault("visited_places", []) if isinstance(v, dict)]
        history["visited_places"] = visited
        row = next((v for v in visited if str(v.get("place") or "").strip() == place), None)
        if row is None:
            row = {"place": place, "scope": "city_or_region", "visit_period": None,
                   "revisit_interest": "unknown", "notes": None}
            visited.append(row)
        row["visit_period"] = entry["dates"]
        if revisit:
            row["revisit_interest"] = revisit
        note = "; ".join(str(answers[k]) for k in ("worked", "did_not_work") if answers.get(k))
        if note:
            row["notes"] = note
        changes.append(f"travel_history.visited_places: {place} (revisit: {row['revisit_interest']})")
    for key, items in (("avoid_list", avoid), ("comfort_and_safety_preferences", comfort)):
        current = prefs.setdefault(key, [])
        added = [i for i in items if i not in current]
        current.extend(added)
        if added:
            changes.append(f"recurring_preferences.{key}: + {', '.join(added)}")
    if pace and prefs.get("pace") != pace:
        changes.append(f"recurring_preferences.pace: {prefs.get('pace')} -> {pace}")
        prefs["pace"] = pace
    profile.setdefault("data_controls", {})["last_reviewed_at"] = today.isoformat()
    return changes


def archive(workspace: Path, stem: str) -> list[Path]:
    moved = []
    for folder in ("plans", "html"):
        for path in sorted((workspace / folder).glob(f"{stem}*")):
            if path.is_file() and (path.name[len(stem):][:1] in (".", "-")):
                target = workspace / folder / "past" / path.name
                target.parent.mkdir(exist_ok=True)
                shutil.move(str(path), str(target))
                moved.append(target)
    return moved


def cmd_record(args, today: dt.date) -> int:
    plan_path, profile_path = Path(args.plan), Path(args.profile)
    trip = _plan_trip(plan_path)
    if trip is None:
        print(f"ERROR: {plan_path} is not a saved final plan", file=sys.stderr)
        return 2
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    errors = validate_profile(profile)
    if errors:
        print("ERROR: the profile is not valid before the debrief: " + " ".join(errors), file=sys.stderr)
        return 2
    answers = json.loads(Path(args.answers).read_text(encoding="utf-8"))
    try:
        changes = apply(profile, plan_path.stem, trip, answers, today)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate_profile(profile)
    if errors:
        print("ERROR: the debrief would make the profile invalid, nothing written: " + " ".join(errors), file=sys.stderr)
        return 2
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for line in changes:
        print(f"PROFILE {line}")
    if answers.get("went") != "skip":
        workspace = Path(args.workspace).expanduser() if args.workspace else plan_path.resolve().parent.parent
        for path in archive(workspace, plan_path.stem):
            print(f"MOVED {path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("list")
    ls.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    rec = sub.add_parser("record")
    rec.add_argument("plan")
    rec.add_argument("--profile", required=True)
    rec.add_argument("--answers", required=True)
    rec.add_argument("--workspace", help="default: the folder above the plan's plans/ folder")
    sk = sub.add_parser("skip")
    sk.add_argument("--profile", required=True)
    sk.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    for p in (ls, rec, sk):
        p.add_argument("--today", help="treat this date as today (YYYY-MM-DD)")
    args = parser.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    if args.command == "list":
        return cmd_list(Path(args.workspace).expanduser(), today)
    if args.command == "skip":
        return cmd_skip(args, today)
    return cmd_record(args, today)


if __name__ == "__main__":
    sys.exit(main())
