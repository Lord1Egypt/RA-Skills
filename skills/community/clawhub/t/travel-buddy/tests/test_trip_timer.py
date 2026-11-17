#!/usr/bin/env python3
"""Regression tests for scripts/trip_timer.py.

The point of this tool is one distinction: compute time and traveller wait behave differently and
must not be summed into a single number. Compute is a fan-out, so its wall-clock is the slowest
agent rather than the sum of the agents; the traveller's wait is a round-trip with a human in it
and is unbounded. Every case here defends that split, or defends the failure paths -- a run that
died mid-phase is the run whose timing is most worth reading, and it is also the one an
average-shaped report would quietly drop.
"""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "trip_timer.py"


def load_timer():
    spec = importlib.util.spec_from_file_location("trip_timer", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def timeline(workspace: Path, run: str, spans: list[tuple[str, int, int]]) -> None:
    """Write a run whose phases start and stop at fixed minute offsets."""
    base = dt.datetime(2026, 8, 15, 10, 0, 0)
    events = []
    for phase, start, stop in spans:
        events.append({"phase": phase, "event": "start",
                       "at": (base + dt.timedelta(minutes=start)).isoformat(), "note": None})
        if stop is not None:
            events.append({"phase": phase, "event": "stop",
                           "at": (base + dt.timedelta(minutes=stop)).isoformat(), "note": None})
    directory = workspace / "timing"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{run}.json").write_text(
        json.dumps({"run": run, "events": events}, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    timer = load_timer()
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    # The split itself. A phase named checkpoint/wait is the traveller answering; everything else
    # is the machine working. Summing them would hide the only number worth acting on.
    check("a checkpoint counts as wait", timer.is_wait("checkpoint:dates"), "")
    check("a bare wait counts as wait", timer.is_wait("wait-for-traveller"), "")
    check("a research phase counts as compute", not timer.is_wait("feasibility"), "")
    check("the prefix match is case-insensitive", timer.is_wait("Checkpoint"), "")
    # 'checkpoint' must match as a prefix rather than a substring, or a phase legitimately named
    # 'design-after-checkpoint' would be filed as time the traveller spent.
    check("a compute phase merely mentioning a checkpoint stays compute",
          not timer.is_wait("design-after-checkpoint"), "")

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        timeline(workspace, "measured", [
            ("feasibility", 0, 6),
            ("checkpoint:dates", 6, 34),
            ("design", 34, 42),
            ("verification", 42, 55),
        ])
        data = json.loads((workspace / "timing" / "measured.json").read_text(encoding="utf-8"))
        spans, compute, wait = timer.durations(data["events"])
        check("every closed phase is paired", len(spans) == 4, str(spans))
        check("compute sums only the machine phases", compute == (6 + 8 + 13) * 60, str(compute))
        check("wait sums only the traveller phases", wait == 28 * 60, str(wait))
        # The finding the tool exists to surface: on a plausible run the single consolidated
        # checkpoint is about half the elapsed time, and no token count shows it.
        check("the traveller's own answering time is visible as a share",
              wait / (compute + wait) > 0.4, f"{wait} vs {compute}")

    # A run that died mid-phase must be reported, not dropped. Silently omitting the unclosed
    # phase would make a crashed run look like a fast one -- the same shape as a failed discovery
    # run saving a result file that reads like an answer.
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        timeline(workspace, "died", [("feasibility", 0, 6), ("design", 6, None)])
        data = json.loads((workspace / "timing" / "died.json").read_text(encoding="utf-8"))
        spans, compute, wait = timer.durations(data["events"])
        unfinished = [phase for phase, seconds, _ in spans if seconds < 0]
        check("an unclosed phase is reported", unfinished == ["design"], str(spans))
        check("an unclosed phase does not inflate the totals", compute == 6 * 60, str(compute))

    # Stamps, not durations: `now` is the only thing a caller can honestly assert, so the CLI
    # must record a time rather than accept one.
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        for action in ("start", "stop"):
            result = subprocess.run(
                [sys.executable, str(SCRIPT), action, "feasibility",
                 "--workspace", str(workspace), "--run", "cli"],
                capture_output=True, text=True)
            check(f"CLI {action} succeeds", result.returncode == 0, result.stdout + result.stderr)
        saved = json.loads((workspace / "timing" / "cli.json").read_text(encoding="utf-8"))
        check("both stamps were written", len(saved["events"]) == 2, str(saved))
        check("the stamps are ISO timestamps the tool generated",
              all(dt.datetime.fromisoformat(e["at"]) for e in saved["events"]), str(saved))

        report = subprocess.run(
            [sys.executable, str(SCRIPT), "report", "--workspace", str(workspace)],
            capture_output=True, text=True)
        check("report runs", report.returncode == 0, report.stdout + report.stderr)
        check("report names the phase", "feasibility" in report.stdout, report.stdout)

    # Failure paths produce a message, never a traceback: an operator who sees a stack trace
    # learns nothing and stops running the tool.
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        (workspace / "timing").mkdir()
        (workspace / "timing" / "broken.json").write_text("{not json", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "report", "--workspace", str(workspace)],
            capture_output=True, text=True)
        check("a corrupt record does not crash the report",
              result.returncode == 0 and "Traceback" not in result.stderr,
              result.stdout + result.stderr)

        missing = subprocess.run(
            [sys.executable, str(SCRIPT), "report", "--workspace", str(workspace / "nowhere")],
            capture_output=True, text=True)
        check("an unmeasured workspace says so rather than failing",
              missing.returncode == 0 and "Nothing has been measured" in missing.stdout,
              missing.stdout + missing.stderr)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all trip-timer regression cases passed")
    return 0


def test_trip_timer() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
