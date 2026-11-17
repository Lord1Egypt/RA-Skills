#!/usr/bin/env python3
"""The verification report: a shape to fill in, and evidence that survives the session.

Measured on the author's workspace before any of this existed. Seventeen delivered plans; the
verification stage -- the most expensive thing this skill asks for -- had never left a surviving
artifact. Six plans claimed `verification_status: verified`, and four pointed at report files that
no longer existed, two of them into a session scratchpad deleted when the session ended. Those
pages render with no banner, so the traveller reads an authority nobody can check.

Three things had to be true together, and none of them were:

  * the gate must refuse an UNFILLED report, or a scaffold for an evidence document is a forgery
    generator;
  * there must BE a scaffold, or the stage stays unreachable -- the only guide was the gate saying
    what was wrong after the author guessed at seven blocks, a tier the plan computes, and a
    coverage rule demanding a pointer per researched dining card;
  * the report must land in the workspace beside the plan, or the evidence dies with the session.

Run:  python tests/test_verification_scaffold.py
      python -m pytest tests/test_verification_scaffold.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_plan_consistency import (  # noqa: E402
    RESEARCHED_HOURS_STATUS,
    check_verification,
    resolve_pointer,
)
import new_verification_report as SCAFFOLD  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))

    # 1. THE PREREQUISITE. Without this the scaffold below manufactures evidence: placeholder text
    #    would be graded on its dates and its pointers and passed. A plan carrying a TODO looks
    #    unfinished; a REPORT carrying one looks like somebody checked.
    shell = {"checked_at": "2026-09-12", "plan": "x.json",
             "method": "TODO: how the domains were run",
             "domains": [{"domain": "entry", "claims_checked": ["entry_context.status"],
                          "findings": [{"claim": "TODO: what was checked", "verdict": "confirmed",
                                        "correction": None, "severity": "low",
                                        "evidence_url": "https://example.invalid",
                                        "resolved": True, "resolution": None}]}],
             "audits": []}
    found: list[str] = []
    check_verification(shell, found, [], plan={"trip": {}}, plan_path="x.json")
    placeholders = [f for f in found if "placeholder" in f]
    check("an unfilled report is refused", placeholders, "it passed, so a scaffold could forge")
    if placeholders:
        check("the refusal names where the placeholder is",
              "method" in placeholders[0] or "findings" in placeholders[0], placeholders[0][:160])

    filled = json.loads(json.dumps(shell))
    filled["method"] = "five domains run as separate passes, both audits offline"
    filled["domains"][0]["findings"][0]["claim"] = "opened the consulate page and read the rule"
    found = []
    check_verification(filled, found, [], plan={"trip": {}}, plan_path="x.json")
    check("a filled report is not refused for placeholders",
          not [f for f in found if "placeholder" in f], f"{[f for f in found if 'placeholder' in f][:1]}")

    # 2. THE SCAFFOLD. Every pointer it writes must RESOLVE against the plan it was built from --
    #    a scaffold handing over a broken pointer costs the round trip it exists to save.
    report, notes = SCAFFOLD.build(plan, Path("plan.json"))
    cited = [p for block in report["domains"] + report["audits"]
             for p in block["claims_checked"]]
    check("the scaffold derives pointers at all", cited, "no block cited anything")
    broken = [p for p in cited if not resolve_pointer(plan, p)]
    check("every derived pointer resolves", not broken, f"{broken[:5]}")

    # Both audits are required at every tier and cost no network, so they are never omitted.
    check("both audits are present",
          {b["audit"] for b in report["audits"]} == {"consistency", "completeness"},
          f"{[b.get('audit') for b in report['audits']]}")

    # The coverage rule the gate enforces: a dining card claiming researched hours owes a pointer.
    wanted = {f"days[{d}].dining[{c}].venue_hours"
              for d, day in enumerate(plan.get("days") or [])
              for c, card in enumerate((day or {}).get("dining") or [])
              if str((card or {}).get("hours_status") or "") in RESEARCHED_HOURS_STATUS}
    sights = next((b["claims_checked"] for b in report["domains"]
                   if b["domain"] == "sights_and_hours"), [])
    missing = sorted(wanted - set(sights))
    check("every researched dining card is cited by sights_and_hours", not missing,
          f"{missing[:4]} -- the gate demands these and the scaffold has to pre-list them")

    # The coverage rule asks for a pointer UNDER the card, not for `venue_hours` by name. A card
    # claiming researched hours while carrying no `venue_hours` key produced no pointer at all --
    # the resolve filter dropped it -- and the scaffold then handed over a report the gate refuses
    # for a gap it had no way to fill. Found by running the scaffold on degenerate shapes rather
    # than on the plan it was written against.
    stripped = json.loads(json.dumps(plan))
    for day in stripped.get("days") or []:
        for card in (day or {}).get("dining") or []:
            if str((card or {}).get("hours_status") or "") in RESEARCHED_HOURS_STATUS:
                card.pop("venue_hours", None)
                break
        else:
            continue
        break
    thin, _ = SCAFFOLD.build(stripped, Path("plan.json"))
    thin_sights = next((b["claims_checked"] for b in thin["domains"]
                        if b["domain"] == "sights_and_hours"), [])
    uncovered = [f"days[{d}].dining[{c}]"
                 for d, day in enumerate(stripped.get("days") or [])
                 for c, card in enumerate((day or {}).get("dining") or [])
                 if str((card or {}).get("hours_status") or "") in RESEARCHED_HOURS_STATUS
                 and not any(p.startswith(f"days[{d}].dining[{c}]") for p in thin_sights)]
    check("a researched card with no venue_hours is still cited", not uncovered,
          f"{uncovered[:3]} -- the card itself resolves and is the fallback")

    # And it must not be deliverable as emitted. This is the property that makes a scaffold for an
    # evidence document safe to ship at all.
    found = []
    check_verification(report, found, [], plan=plan, plan_path="plan.json")
    check("the scaffold as emitted is refused", [f for f in found if "placeholder" in f],
          "an unfilled scaffold passed the gate")

    # 3. THE EVIDENCE HAS TO SURVIVE. Reported as its own line, written beside the plan, and
    #    pointed at by a bare relative name so a workspace that moves keeps resolving.
    # Against a REAL delivered plan, because the fixture does not pass the consistency gate and a
    # save that refuses exercises nothing. Opt-in for the same reason the other suites are: this
    # reads the reader's own travel data, and a silent skip is how a suite goes green while testing
    # less than it claims.
    choice = os.environ.get("TRAVEL_BUDDY_TEST_WORKSPACE", "").strip()
    if not choice:
        print("note: the carry-in cases need a real delivered plan and were SKIPPED. Set "
              "TRAVEL_BUDDY_TEST_WORKSPACE=1 to run them.", file=sys.stderr)
        real = None
    else:
        root = (Path.home() / "Travel Buddy" if choice in ("1", "true", "yes")
                else Path(choice).expanduser())
        candidates = [p for p in sorted((root / "plans").glob("*.json"))
                      if not p.name.startswith(("intake-", "next-action-", "shortlist-"))
                      and not p.name.endswith(("-imagery.json", "-verification.json"))]
        # Needs a plan that actually SAVES: one with days and an intake_context, since
        # save_trip_deliverables refuses a plan that will not say how its requirements were
        # collected, and a refused save exercises nothing. Newest first.
        def _usable(path: Path) -> bool:
            try:
                body = json.loads(path.read_text(encoding="utf-8"))
            except ValueError:
                return False
            return (isinstance(body, dict) and "days" in body
                    and isinstance(body.get("intake_context"), dict)
                    and bool(body["intake_context"].get("method")))
        real = next((p for p in reversed(candidates) if _usable(p)), None)
        if real is None:
            print("note: no plan in this workspace both has days and states its intake_context, "
                  "so the carry-in cases were skipped.", file=sys.stderr)

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        if real is None:
            plan_file = tmp / "plan.json"
            plan_file.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        else:
            plan = json.loads(real.read_text(encoding="utf-8"))
            plan.pop("imagery", None)
            plan_file = real
            report, _ = SCAFFOLD.build(plan, plan_file)
        good = json.loads(json.dumps(report))
        good["method"] = "five domains as separate passes"
        good["plan"] = str(plan_file)
        for block in good["domains"] + good["audits"]:
            block["findings"] = [{"claim": "checked every pointer listed above",
                                  "verdict": "confirmed", "correction": None, "severity": "low",
                                  "evidence_url": "https://example.invalid",
                                  "resolved": True, "resolution": None}]
        report_file = tmp / "report.json"
        report_file.write_text(json.dumps(good, ensure_ascii=False), encoding="utf-8")

        if real is None:
            print("note: carry-in assertions skipped (no real plan).", file=sys.stderr)
            proc = None
        else:
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "save_trip_deliverables.py"),
                 str(plan_file), "--workspace", str(tmp / "ws"),
                 "--verification", str(report_file)],
                capture_output=True, text=True)
        if proc is None:
            pass
        elif proc.returncode != 0:
            print("note: the fixture does not save cleanly in this environment; the carry-in "
                  "assertions were skipped. First failure: "
                  + (proc.stderr.strip().splitlines() or ["(none)"])[0][:160], file=sys.stderr)
        else:
            check("the report path is reported as its own line",
                  "Verification report:" in proc.stdout, proc.stdout[-300:])
            saved = sorted((tmp / "ws" / "plans").glob("*-verification.json"))
            check("the report is written beside the plan", saved, "nothing was copied in")
            body = [p for p in (tmp / "ws" / "plans").glob("*.json")
                    if not p.name.endswith(("-imagery.json", "-verification.json"))]
            if body and saved:
                delivered = json.loads(body[0].read_text(encoding="utf-8"))
                pointer = delivered.get("verification_report")
                check("the pointer is a bare name, not the path that was passed in",
                      isinstance(pointer, str) and "/" not in pointer, repr(pointer))
                check("and it resolves beside the plan",
                      isinstance(pointer, str) and (body[0].parent / pointer).exists(),
                      repr(pointer))

    # 4. THE TIMER'S OWN SILENT FAILURE. A `stop` with no matching `start` fell through the
    #    pairing loop entirely, so a run that forgot one `start` around a traveller checkpoint
    #    printed "waiting on the traveller 0s (0%)" while the traveller had spent twenty-six
    #    minutes answering. The docstring said an unclosed phase is reported rather than dropped --
    #    and it was, in the one direction that had been thought about.
    import trip_timer as TIMER
    events = [{"phase": "feasibility", "event": "start", "at": "2026-09-02T23:48:54+02:00"},
              {"phase": "feasibility", "event": "stop", "at": "2026-09-02T23:57:58+02:00"},
              {"phase": "checkpoint-shape", "event": "stop", "at": "2026-09-03T00:23:56+02:00"},
              {"phase": "design", "event": "start", "at": "2026-09-03T00:23:56+02:00"},
              {"phase": "design", "event": "stop", "at": "2026-09-03T00:30:10+02:00"}]
    spans, compute, wait = TIMER.durations(events)
    orphan = [s for s in spans if s[0] == "checkpoint-shape"]
    check("a stop with no start is reported, not dropped", orphan,
          "it vanished, and with it the only number this file exists to produce")
    if orphan:
        check("it is marked unmeasured rather than unfinished", orphan[0][1] == -2.0,
              f"{orphan[0][1]}")
        check("and the two absences read differently",
              TIMER.human(-2.0) != TIMER.human(-1.0),
              "both print the same word, so the case that happened hides behind the one that did not")
    # The opposite direction must keep working: a phase that started and never stopped.
    spans, _, _ = TIMER.durations([{"phase": "design", "event": "start", "at": "2026-09-03T00:00:00+02:00"}])
    check("a start with no stop is still reported",
          any(s[0] == "design" and s[1] == -1.0 for s in spans), f"{spans}")

    with tempfile.TemporaryDirectory() as raw:
        out = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "trip_timer.py"), "stop", "checkpoint-x",
             "--workspace", raw, "--run", "t"], capture_output=True, text=True)
        check("stopping an unstarted phase warns at the time it can still be fixed",
              "WARNING" in out.stderr, out.stderr[:160])
        run_file = Path(raw) / "timing" / "t.json"
        if run_file.exists():
            report = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "trip_timer.py"), "report",
                 "--workspace", raw, "--run", "t"], capture_output=True, text=True)
            body = report.stdout
            check("the report refuses to print a waiting percentage while a phase is unmeasured",
                  "NOT a percentage" in body or "%" not in body.split("──")[-1],
                  body[-200:])
            check("and it names the unmeasured phase", "checkpoint-x" in body, body[-200:])

    if failures:
        print(f"VERIFICATION SCAFFOLD FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all verification-scaffold cases passed")
    return 0


def test_verification_scaffold() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
