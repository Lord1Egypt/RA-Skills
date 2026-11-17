#!/usr/bin/env python3
"""Record real wall-clock for a planning run, split into compute and traveller wait.

Why this exists. references/research-budget.md is thorough about TOKENS -- 1.18M on a four-day
trip, 17 agents where 13 was the target, ~37k per research agent, all measured. About the thing
the traveller actually experiences, the minutes they sit waiting, it says one sentence and carries
no measurement at all. So every statement about planning speed in this skill has been a guess, and
"optimise the time" has had nothing to optimise against.

The two halves behave completely differently and must not be summed into one number:

  - COMPUTE is a fan-out, so its wall-clock is the slowest agent, not the sum of the agents. Adding
    a seventh research agent to a six-agent phase costs almost no time and a sixth of a token
    budget; removing one saves tokens and no time at all. Token thrift and time thrift point in
    different directions here, which is exactly why one number for both would mislead.
  - WAIT is a round-trip with a human in it, and it is unbounded. The measured run put four
    separate questions to the traveller at four different moments. If each of those cost ten
    minutes of their attention, the checkpoint rule in research-budget.md saved more real time than
    every token optimisation in that file combined.

This records stamps rather than durations. `now` is the only thing a caller can assert, so a
fabricated duration takes deliberately writing false files rather than typing an optimistic number.

Usage:
    python trip_timer.py start <phase> --workspace PATH --run RUN_ID
    python trip_timer.py stop  <phase> --workspace PATH --run RUN_ID [--note TEXT]
    python trip_timer.py report --workspace PATH [--run RUN_ID]

Phases are free text so the pipeline can name what it actually did, but four are conventional:
`feasibility`, `checkpoint` (a wait), `design`, `verification`. A phase whose name starts with
`checkpoint` or `wait` counts as traveller wait; everything else counts as compute.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

DEFAULT_WORKSPACE = Path.home() / "Travel Buddy"
WAIT_PREFIXES = ("checkpoint", "wait")


def timing_dir(workspace: Path) -> Path:
    return workspace / "timing"


def run_path(workspace: Path, run_id: str) -> Path:
    safe = "".join(ch for ch in run_id if ch.isalnum() or ch in "-_")[:80] or "run"
    return timing_dir(workspace) / f"{safe}.json"


def load_run(path: Path) -> dict:
    if not path.exists():
        return {"run": path.stem, "events": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"run": path.stem, "events": []}
    return data if isinstance(data, dict) else {"run": path.stem, "events": []}


def is_wait(phase: str) -> bool:
    return phase.casefold().startswith(WAIT_PREFIXES)


def durations(events: list[dict]) -> tuple[list[tuple[str, float, str]], float, float]:
    """Pair start/stop stamps into (phase, seconds, note) plus compute and wait totals.

    An unclosed phase is reported rather than dropped: a run that died mid-phase is the case most
    worth seeing, and silently omitting it would make a crashed run look like a fast one.

    The OPPOSITE case was silent, and it is the one that happened. A `stop` with no matching
    `start` fell through this loop entirely, so a real run that forgot one `start` around a
    traveller checkpoint reported `waiting on the traveller 0s (0%)` while the traveller had spent
    twenty-six minutes answering -- and the total read 15m17s against a real span of 41m16s. This
    file exists to measure exactly that number, and it printed a confident zero. Both directions
    are now spans: -1 means started and never stopped, -2 means stopped without a start, and the
    report refuses to present a percentage as a measurement while either is present. Nothing is
    inferred from the gap; a plausible duration written into a measurement is worse than a gap
    that says it is one.
    """

    open_phases: dict[str, tuple[str, str]] = {}
    spans: list[tuple[str, float, str]] = []
    compute = wait = 0.0
    for event in events:
        if not isinstance(event, dict):
            continue
        phase, kind, stamp = str(event.get("phase") or ""), event.get("event"), event.get("at")
        if not phase or not isinstance(stamp, str):
            continue
        if kind == "start":
            open_phases[phase] = (stamp, str(event.get("note") or ""))
        elif kind == "stop" and phase not in open_phases:
            spans.append((phase, -2.0,
                          f"stopped at {stamp} without a start — its duration is unmeasured"))
        elif kind == "stop":
            started, _ = open_phases.pop(phase)
            try:
                seconds = (dt.datetime.fromisoformat(stamp)
                           - dt.datetime.fromisoformat(started)).total_seconds()
            except ValueError:
                # Dropping it was the same silent failure as the orphaned stop above, one file
                # over: a phase whose stamps cannot be parsed vanished from the report entirely,
                # so a run with a corrupt record read as a run with fewer phases.
                spans.append((phase, -2.0,
                              f"stamps could not be read ({started!r} → {stamp!r})"))
                continue
            if seconds < 0:
                # A stop before its own start is not a negative duration, it is an unusable pair --
                # and summing it SUBTRACTED from the totals while printing as "unfinished". This
                # file's subject is honest measurement; a number that quietly shrinks the total is
                # worse than an admitted gap, which is the same rule the spine follows about
                # negative nights.
                spans.append((phase, -2.0,
                              f"stopped at {stamp} before it started at {started} — unusable"))
                continue
            spans.append((phase, seconds, str(event.get("note") or "")))
            if is_wait(phase):
                wait += seconds
            else:
                compute += seconds
    for phase, (started, _) in open_phases.items():
        spans.append((phase, -1.0, f"never stopped (started {started})"))
    return spans, compute, wait


def human(seconds: float) -> str:
    # Two different absences, two different words. -1 is a phase that started and never stopped
    # (the run died in it); -2 is one that stopped with no start (its duration was never captured).
    # Printing both as "unfinished" hid the second behind the first, which is how the case that
    # actually happened read as the case that had been thought about.
    if seconds == -2.0:
        return "unmeasured"
    if seconds < 0:
        return "unfinished"
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}m{secs:02d}s" if minutes else f"{secs}s"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("action", choices=("start", "stop", "report"))
    parser.add_argument("phase", nargs="?", default=None,
                        help="Phase name; a name starting with checkpoint/wait counts as traveller wait")
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--run", default=None, help="Run id, e.g. the plan slug")
    parser.add_argument("--note", default=None, help="What happened, e.g. agent count or the question asked")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser()
    if args.action == "report":
        directory = timing_dir(workspace)
        if not directory.is_dir():
            print(f"No timing records in {directory}. Nothing has been measured yet.")
            return 0
        paths = [run_path(workspace, args.run)] if args.run else sorted(directory.glob("*.json"))
        any_shown = False
        for path in paths:
            if not path.exists():
                continue
            any_shown = True
            data = load_run(path)
            spans, compute, wait = durations(data.get("events") or [])
            total = compute + wait
            print(f"\n{path.stem}")
            for phase, seconds, note in spans:
                tag = "wait   " if is_wait(phase) else "compute"
                share = f"{seconds / total * 100:4.0f}%" if total > 0 and seconds >= 0 else "   -"
                print(f"  {tag} {human(seconds):>9} {share}  {phase}"
                      + (f"   ({note})" if note else ""))
            unmeasured = [phase for phase, seconds, _ in spans if seconds < 0]
            # The real span of the run, from its first stamp to its last. A percentage computed
            # only from the phases that paired up says nothing about the ones that did not, and
            # the gap between the two numbers is the size of what was missed: on the run that
            # prompted this, 15m17s of paired phases inside 41m16s of elapsed time.
            stamps = sorted(str(e.get("at")) for e in (data.get("events") or [])
                            if isinstance(e, dict) and isinstance(e.get("at"), str))
            elapsed = None
            if len(stamps) >= 2:
                try:
                    elapsed = (dt.datetime.fromisoformat(stamps[-1])
                               - dt.datetime.fromisoformat(stamps[0])).total_seconds()
                except ValueError:
                    elapsed = None
            if total > 0:
                if unmeasured:
                    # Never a percentage while a phase is unmeasured. This file's whole subject is
                    # the traveller's time, and printing "0%" for a run that forgot one `start`
                    # is the confident zero it exists to prevent.
                    print(f"  ── compute {human(compute)} · waiting on the traveller "
                          f"AT LEAST {human(wait)}"
                          + (f", inside {human(elapsed)} of elapsed time" if elapsed else "")
                          + f". NOT a percentage: {len(unmeasured)} phase(s) "
                          f"({', '.join(unmeasured)}) have no duration, so what is missing from "
                          f"these totals is exactly the thing this file measures. Wrap the phase "
                          f"in both `start` and `stop` next time.")
                else:
                    print(f"  ── compute {human(compute)} · waiting on the traveller {human(wait)} "
                          f"({wait / total * 100:.0f}% of the elapsed time)")
                    if elapsed and elapsed - total > 60:
                        print(f"     note: {human(elapsed - total)} of the run sits outside any "
                              f"phase — elapsed {human(elapsed)} against {human(total)} measured.")
        if not any_shown:
            print(f"No timing records in {timing_dir(workspace)}.")
        return 0

    if not args.phase:
        parser.error("start and stop need a phase name")
    if not args.run:
        parser.error("start and stop need --run")
    path = run_path(workspace, args.run)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_run(path)
    data.setdefault("run", path.stem)
    data.setdefault("events", []).append({
        "phase": args.phase,
        "event": args.action,
        "at": dt.datetime.now().astimezone().isoformat(),
        "note": args.note,
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{args.action} {args.phase} → {path}")
    # Said HERE, not only at report time, because this is the moment it can still be fixed. A stop
    # with no start records a boundary and no duration, and on the run that prompted this the
    # missing one was around a traveller checkpoint -- so the number that vanished was the only
    # number this file exists to produce.
    if args.action == "stop":
        prior = [e for e in data["events"][:-1]
                 if isinstance(e, dict) and str(e.get("phase")) == args.phase]
        if not any(e.get("event") == "start" for e in prior):
            print(f"WARNING: '{args.phase}' was never started, so this stop records a boundary and "
                  f"no duration. The report will name it as unmeasured and will refuse to print a "
                  f"waiting percentage for this run"
                  + (" -- and a checkpoint is the one phase whose duration is the traveller's own "
                     "time." if is_wait(args.phase) else "."), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
