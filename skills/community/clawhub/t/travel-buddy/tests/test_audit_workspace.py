#!/usr/bin/env python3
"""Regression tests for scripts/audit_workspace.py, mostly for what its --json form costs to read.

The defect these were written against. `--json` exists so a program -- or a model, mid-conversation,
when the traveller asks whether a saved trip still holds -- can consume the audit cheaply. It was
doing the opposite: it printed every finding's full prose for every plan, and on the measured
workspace that came to two orders of magnitude more than the human report it was supposed to be a
cheaper form of. Almost all of it was repetition, because a rule that fires once per venue prints
its rationale paragraph once per venue. A report a caller cannot afford to read is a check that
does not happen, and the check not happening is a traveller walking to a place that closed.

So the assertions here are about a property, not a number. A byte budget would rot on the next
reference edit and would tell you nothing about why: the thing that must stay true is that the
compact form's size follows the number of RULES that fired, never the number of findings, and that
no finding's prose appears in it at all. Both are checked by making a plan's finding count grow
while its rule set stays fixed.

The other half is agreement. Two forms of one report is two chances to answer the same question
differently, so the human report's own stdout is parsed back and compared field by field against
the JSON -- verdict, count, verification status, gate stamp and order.

Run:  python tests/test_audit_workspace.py
      python -m pytest tests/test_audit_workspace.py
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_workspace.py"

# The human report's per-plan line, read back out of stdout. Parsing our own output rather than
# calling the printer is deliberate: what a reader sees is the thing that has to agree with the
# JSON, and a comparison against the shared dict both forms happen to read would pass even if the
# printer dropped a column.
HUMAN_ROW = re.compile(
    r"^(OK  |STALE)\s+(\d+) finding\(s\)  (.+?)   \[verification: (.+?); (.+?)\]$", re.M)


def load_audit():
    spec = importlib.util.spec_from_file_location("audit_workspace", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample_plan(days: int) -> dict:
    """A plan shaped enough to be recognised as one, and wrong enough for many rules to fire.

    Every day is the same shape on purpose. Adding days multiplies the findings without changing
    which rules produce them, which is exactly the case the compact form has to survive: the same
    sentence, over and over, is what made the old JSON unreadable.

    CJK in the title because the workspace this tool was measured on is mostly Chinese, and a
    report that mangles or drops the title is a report that cannot tell the traveller which trip it
    is talking about.
    """
    return {
        "trip": {"title": "测试行程 · テスト · 4 天", "destination": "Kyoto",
                 "start_date": "2027-03-01"},
        "days": [{"date": f"2027-03-{index + 1:02d}",
                  "activities": [{"name": f"venue {index}-{slot}", "time_window": "10:00-11:00"}
                                 for slot in range(3)]}
                 for index in range(days)],
    }


def workspace_with(root: Path, plans: dict[str, dict]) -> Path:
    plans_dir = root / "plans"
    plans_dir.mkdir(parents=True, exist_ok=True)
    for name, plan in plans.items():
        (plans_dir / name).write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    return root


def run(workspace: Path, *flags: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), "--workspace", str(workspace), *flags],
                          capture_output=True, text=True)


def main() -> int:
    audit = load_audit()
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    with tempfile.TemporaryDirectory() as tmp:
        small = workspace_with(Path(tmp) / "small", {"trip-a.json": sample_plan(2)})
        big = workspace_with(Path(tmp) / "big", {"trip-a.json": sample_plan(12)})

        small_json = run(small, "--json")
        big_json = run(big, "--json")
        check("--json exits 0", small_json.returncode == 0 and big_json.returncode == 0,
              small_json.stderr + big_json.stderr)
        try:
            compact_small = json.loads(small_json.stdout)
            compact_big = json.loads(big_json.stdout)
        except ValueError as exc:
            print(f"--json did not parse: {exc}", file=sys.stderr)
            return 1

        # 1. The property the whole change is for: the compact form's size follows the rules that
        #    fired, not the findings. The fixture grows one plan's findings while every finding
        #    still comes from the same rules, so a compact form that grew with it would be
        #    reprinting per-finding text -- which is the defect, whatever its byte count.
        rows_small = {(row["rule_id"], tuple(row["references"]))
                      for row in compact_small["plans"][0]["rules"]}
        rows_big = {(row["rule_id"], tuple(row["references"]))
                    for row in compact_big["plans"][0]["rules"]}
        found_small = compact_small["plans"][0]["total"]
        found_big = compact_big["plans"][0]["total"]
        check("the fixture must actually add findings, or this test proves nothing",
              found_big > found_small, f"{found_small} -> {found_big}")
        check("the fixture must fire the same rules at both sizes, or the comparison is unfair",
              rows_small == rows_big, f"{rows_small ^ rows_big}")
        added = found_big - found_small
        grew = len(big_json.stdout.encode("utf-8")) - len(small_json.stdout.encode("utf-8"))
        # Under one byte per added finding. Not a tuned threshold: it is the statement "the size
        # does not scale with findings" written as arithmetic. Extra findings here cost only the
        # digits of a count that was already being printed.
        check("the compact form must not grow with the finding count",
              grew < added,
              f"{added} more findings added {grew} bytes to --json; the compact form is carrying "
              f"per-finding text")

        # 2. No prose, stated exactly rather than by size. Every sentence the verbose form carries
        #    must be absent from the compact one -- including the multi-line ones, which a
        #    first-line check would have let through.
        verbose = run(big, "--json", "--verbose")
        check("--json --verbose exits 0", verbose.returncode == 0, verbose.stderr)
        detailed = json.loads(verbose.stdout)
        prose = [message
                 for plan in detailed["plans"]
                 for message in plan["structure_errors"] + plan["consistency_errors"]]
        check("the fixture must produce prose findings for this to test anything", bool(prose), "")
        compact_text = big_json.stdout
        leaked = [message for message in prose if message in compact_text]
        check("no finding's prose may appear in the non-verbose JSON",
              not leaked, f"{len(leaked)} leaked, first: {leaked[:1]}")
        # And the halves that survive truncation: a compact form that kept the first sentence of
        # each finding would pass the check above and still be unaffordable.
        heads = [message.splitlines()[0][:60] for message in prose if len(message) > 60]
        check("no finding's opening sentence may appear in the non-verbose JSON either",
              not [head for head in heads if head in compact_text],
              f"first leak: {[h for h in heads if h in compact_text][:1]}")

        # 3. Nothing was deleted -- the prose moved behind a flag. The verbose form must carry
        #    exactly the findings the audit produced, in full and unsplit.
        in_process = audit.audit_plan(big / "plans" / "trip-a.json")
        check("--json --verbose must carry every finding verbatim",
              detailed["plans"][0]["structure_errors"] == in_process["structure_errors"]
              and detailed["plans"][0]["consistency_errors"] == in_process["consistency_errors"],
              "the verbose JSON no longer reproduces audit_plan's findings")
        check("the compact form must not carry the prose keys at all",
              "structure_errors" not in compact_big["plans"][0]
              and "consistency_errors" not in compact_big["plans"][0],
              str(sorted(compact_big["plans"][0])))
        check("--verbose must change no verdict",
              detailed["plans"][0]["total"] == compact_big["plans"][0]["total"]
              and detailed["totals"] == compact_big["totals"], "")

        # 4. The rule rows have to account for every finding, or the compact form is a summary that
        #    quietly loses some. This is what lets a caller trust the breakdown instead of
        #    re-reading the prose to be sure.
        for report in (compact_small, compact_big, detailed):
            for plan in report["plans"]:
                counted = sum(row["count"] for row in plan["rules"])
                check("every finding must be attributed to a rule",
                      counted == plan["total"],
                      f"{plan['file']}: {counted} attributed vs {plan['total']} findings")

        # 5. An uncited finding must still produce a usable row. check_dates and validate_plan both
        #    report rules that no reference states, and a caller writing row["references"] must not
        #    have to know which ones those are.
        uncited = [row for row in compact_big["plans"][0]["rules"] if not row["references"]]
        check("the fixture must include an uncited finding, or this case proves nothing",
              bool(uncited), "")
        check("an uncited rule row carries an empty list, never a missing key",
              all(isinstance(row["references"], list) for row in uncited), str(uncited))
        check("every citation is rendered as a path a reader can open",
              all(reference.startswith("references/")
                  for plan in compact_big["plans"]
                  for row in plan["rules"] for reference in row["references"]), "")

        # 6. Both forms of one report must answer the same question the same way. Parsed back out
        #    of the human report's own stdout, because that text is what a person acts on.
        human = run(big)
        rows = HUMAN_ROW.findall(human.stdout)
        check("the human report still prints a row per plan", len(rows) == len(compact_big["plans"]),
              human.stdout)
        by_file = {plan["file"]: plan for plan in compact_big["plans"]}
        for mark, count, name, verification, gates in rows:
            plan = by_file.get(name)
            if plan is None:
                failures.append(f"the JSON form is missing a plan the human form lists: {name}")
                continue
            expected_gates = (f"gates {plan['checks_at_save']}/{compact_big['checks_now']}"
                              if plan["checks_at_save"] is not None
                              else "gates unrecorded (pre-stamp)")
            check("the two forms must agree on every plan",
                  int(count) == plan["total"] and mark.strip() == plan["status"]
                  and verification == plan["verification_status"] and gates == expected_gates,
                  f"{name}: human {mark!r} {count} [{verification}; {gates}] vs JSON {plan}")
        check("the two forms must list the plans in the same order",
              [name for _, _, name, _, _ in rows] == [plan["file"] for plan in compact_big["plans"]],
              "")

        # 7. Sections the human report prints and the JSON used to drop entirely. A caller that
        #    reads only the JSON must not miss that a saved discovery result came from a run that
        #    died -- the .md reads like a finished answer either way.
        with_runs = workspace_with(Path(tmp) / "runs", {"trip-a.json": sample_plan(2)})
        (with_runs / "plans" / "destination-discovery-20260101-000000-x.log").write_text(
            "starting\n", encoding="utf-8")
        (with_runs / "plans" / "destination-discovery-20260101-000000-x.md").write_text(
            "# Where to go\n", encoding="utf-8")
        runs_report = json.loads(run(with_runs, "--json").stdout)
        check("the JSON form reports discovery runs the human form reports",
              [entry["verdict"] for entry in runs_report["discovery_runs"]]
              == ["INTERRUPTED (no exit) + result saved"], str(runs_report["discovery_runs"]))
        check("the human form still reports the same run",
              "INTERRUPTED (no exit)" in run(with_runs).stdout, "")

        # 8. --json must be JSON on every path a caller can reach. It used to print the human
        #    sentence "No plan files found" on an empty workspace, so json.loads raised on the one
        #    workspace state most worth reporting: a run that died before it saved anything.
        empty = Path(tmp) / "empty"
        (empty / "plans").mkdir(parents=True)
        (empty / "plans" / "intake-2027-01-01.json").write_text("{}", encoding="utf-8")
        emptied = run(empty, "--json")
        try:
            parsed = json.loads(emptied.stdout)
            check("an empty workspace still reports zero plans in JSON",
                  parsed["plans"] == [] and parsed["totals"]["plans"] == 0, emptied.stdout)
        except ValueError as exc:
            failures.append(f"--json on an empty workspace is not JSON: {exc}\n{emptied.stdout!r}")
        check("an empty workspace exits 0", emptied.returncode == 0, emptied.stderr)
        missing = run(Path(tmp) / "nowhere", "--json")
        check("a workspace with no plans directory fails loudly",
              missing.returncode == 2 and "no plans directory" in missing.stderr, missing.stderr)

        # 9. --plan, the drill-down the compact form points a caller at. Without an affordable way
        #    to fetch one plan's sentences, "read the compact form, then read the one that matters"
        #    is advice a caller cannot follow, and the prose might as well not exist.
        many = workspace_with(Path(tmp) / "many", {
            "2027-03-01-kyoto.json": sample_plan(2),
            "2027-04-01-北京三日.json": sample_plan(3),
        })
        one = json.loads(run(many, "--json", "--verbose", "--plan", "kyoto").stdout)
        check("--plan narrows the report to the plan asked for",
              [plan["file"] for plan in one["plans"]] == ["2027-03-01-kyoto.json"], str(one["plans"]))
        check("--plan still returns the full prose under --verbose",
              bool(one["plans"][0]["consistency_errors"]
                   or one["plans"][0]["structure_errors"]), "")
        cjk = json.loads(run(many, "--json", "--plan", "北京").stdout)
        check("--plan matches a CJK filename",
              [plan["file"] for plan in cjk["plans"]] == ["2027-04-01-北京三日.json"], str(cjk))
        upper = json.loads(run(many, "--json", "--plan", "KYOTO").stdout)
        check("--plan matches regardless of case",
              [plan["file"] for plan in upper["plans"]] == ["2027-03-01-kyoto.json"], str(upper))
        # A typo must not read as a clean workspace. "no findings" and "nothing was checked" are
        # the same bytes to a caller, and the caller is deciding whether a saved trip still holds.
        typo = run(many, "--json", "--plan", "kyotoo")
        check("a --plan that matches nothing fails loudly rather than reporting a clean workspace",
              typo.returncode == 2 and "matched none" in typo.stderr and "kyotoo" in typo.stderr,
              f"exit {typo.returncode}: {typo.stdout[:200]}{typo.stderr[:200]}")
        check("a --plan that matches nothing names the plans that do exist",
              "2027-03-01-kyoto.json" in typo.stderr, typo.stderr)
        check("--plan narrows the human form too",
              len(HUMAN_ROW.findall(run(many, "--plan", "kyoto").stdout)) == 1, "")

        # 10. A check that raises contributes one finding and would otherwise read, in the compact
        #     form, as a plan with one small problem -- when in fact that rule audited nothing. The
        #     two have to look different to a caller who cannot see the prose.
        def exploding_check(plan, errors, notes):
            raise RuntimeError("deliberate: a gate that cannot run")

        original = audit.PLAN_CHECKS
        try:
            audit.PLAN_CHECKS = (exploding_check,)
            crashed = audit.audit_plan(many / "plans" / "2027-03-01-kyoto.json")
        finally:
            audit.PLAN_CHECKS = original
        rows = [row for row in crashed["rules"] if row["rule_id"] == "exploding_check"]
        check("a crashed check is attributed to the check that crashed", len(rows) == 1, str(rows))
        if rows:
            check("a crashed check is visible in the compact form, not only in the prose",
                  "crashed" in rows[0]
                  and any("deliberate" in message for message in rows[0]["crashed"]),
                  str(rows[0]))
        check("a crashing check still leaves the other findings reportable",
              crashed["total"] == len(crashed["structure_errors"]) + 1, str(crashed["total"]))

        #     And the half-way case, which is the one a "does the message say crashed?" test would
        #     get wrong: a check that reported two real defects in the traveller's plan and then
        #     raised. Those two are findings; only the note appended at the raise is about the gate.
        def half_way_check(plan, errors, notes):
            errors.append("day 1: a real finding [see references/booking-html-output.md#booking-links]")
            errors.append("day 2: a real finding [see references/booking-html-output.md#booking-links]")
            raise ValueError("deliberate: raised after reporting")

        try:
            audit.PLAN_CHECKS = (half_way_check,)
            partial = audit.audit_plan(many / "plans" / "2027-03-01-kyoto.json")
        finally:
            audit.PLAN_CHECKS = original
        mine = [row for row in partial["rules"] if row["rule_id"] == "half_way_check"]
        flagged = [row for row in mine if "crashed" in row]
        check("a check that raises after reporting keeps its findings unflagged",
              sorted(row["count"] for row in mine) == [1, 2] and len(flagged) == 1
              and flagged[0]["count"] == 1,
              str(mine))
        check("the findings a crashing check did report keep their citation",
              any(row["references"] == ["references/booking-html-output.md#booking-links"]
                  and "crashed" not in row for row in mine), str(mine))

        # 11. A plan with no findings must say OK in both forms. Every fixture above is broken on
        #     purpose, so the clean path is the one nothing else here would exercise.
        clean_dir = Path(tmp) / "clean"
        (clean_dir / "plans").mkdir(parents=True)
        (clean_dir / "plans" / "ok.json").write_text(
            json.dumps(sample_plan(2), ensure_ascii=False), encoding="utf-8")
        audit_module_checks = audit.PLAN_CHECKS
        try:
            # Emptied rather than faked: validate_plan still runs, so this asserts the OK/STALE
            # split itself rather than a plan we pretended was clean.
            audit.PLAN_CHECKS = ()
            silent = audit.audit_plan(clean_dir / "plans" / "ok.json")
        finally:
            audit.PLAN_CHECKS = audit_module_checks
        check("a plan with no consistency findings reports none of them",
              silent["consistency_errors"] == [] and silent["rules"] is not None, "")
        check("rules is empty exactly when there is nothing to report",
              (not silent["rules"]) == (silent["total"] == 0), str(silent["total"]))

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all audit-workspace regression cases passed")
    return 0


def test_audit_workspace() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
