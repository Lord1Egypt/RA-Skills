#!/usr/bin/env python3
"""Regression tests for scripts/plan_slice.py.

The tool exists to make the verification fan-out cheaper, and there is exactly one way for it to
be cheap and wrong: a verifier cites a field it really opened, the pointer no longer resolves
against the plan, and `check_plan_consistency.py --verification` refuses the report -- or, worse,
the verifier never sees the field at all and reports the claim `unverifiable` when the plan states
it plainly. So most of what is below is the pointer guarantee, asserted against the repo's own
booking-ready fixture and against the per-domain `claims_checked` lists that
templates/verification-report.json already ships: those are, literally, the pointers each domain
is expected to cite.

The rest defends the parts a saving would otherwise be taken out of: the deny list is pinned to
templates/final-trip-plan.json so a new contract block cannot be silently dropped from all five
domains, the two auditors are refused by name rather than sliced, and a slice that comes out
LARGER than the plan has to say so instead of reporting a null result in the shape of a win.

Run:  python tests/test_plan_slice.py
      python -m pytest tests/test_plan_slice.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "plan_slice.py"
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"
PLAN_TEMPLATE = ROOT / "templates" / "final-trip-plan.json"
REPORT_TEMPLATE = ROOT / "templates" / "verification-report.json"

# Both modules are loaded by path, so the code under test is the file the CLI runs rather than
# whatever an import path resolves to. scripts/ goes on sys.path first because
# check_plan_consistency._provider_owns lazily imports validate_trip_html and silently degrades to
# "undecidable" on ImportError -- a harness that omits this loses findings without saying so.
sys.path.insert(0, str(ROOT / "scripts"))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SLICE = _load("_slice_under_test", SCRIPT)
CHECKER = _load("_checker_for_pointers", ROOT / "scripts" / "check_plan_consistency.py")


def pointers(obj: object, prefix: str = ""):
    """Every path in `obj` that can be WRITTEN as a claims_checked pointer.

    Keys carrying a dot or a bracket are skipped rather than emitted, because the gate's own
    _POINTER_STEP cannot parse them: a test that asserted on paths the gate can never be handed
    would be measuring this walker instead of the slice.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if not isinstance(key, str) or CHECKER._POINTER_STEP.match(key) is None:
                continue
            path = f"{prefix}.{key}" if prefix else key
            yield path
            yield from pointers(value, path)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            path = f"{prefix}[{index}]"
            yield path
            yield from pointers(value, path)


def value_at(obj: object, pointer: str):
    """Follow a pointer to its value. Raises on a pointer that does not resolve -- callers only
    pass pointers they have already asserted resolve, so an exception here is a real defect."""
    current = obj
    for part in pointer.split("."):
        step = CHECKER._POINTER_STEP.match(part)
        current = current[step.group(1)]
        for index in CHECKER._POINTER_INDEX.findall(step.group(2)):
            current = current[int(index)]
    return current


def root_of(pointer: str) -> str:
    return pointer.split(".")[0].split("[")[0]


def run_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


def main() -> int:
    failures: list[str] = []

    def check(name: str, condition: bool, detail: object = "") -> None:
        if not condition:
            failures.append(f"{name}\n{detail}")

    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))

    # ---------------------------------------------------------------- the table is a decision
    #
    # A block that is in neither dict is not a choice anybody made, and it is indistinguishable
    # from forgetting -- the same rule tests/test_packaging.py applies to the gates' citations.
    # Pinned to the shipped contract rather than to a hand-written list, so the failure arrives
    # when the schema grows rather than the next time somebody thinks to look.
    contract_keys = set(json.loads(PLAN_TEMPLATE.read_text(encoding="utf-8")))
    unclassified = sorted(contract_keys - SLICE.KNOWN_TOP_LEVEL_KEYS)
    check("every top-level key of templates/final-trip-plan.json is classified",
          not unclassified,
          f"unclassified: {unclassified}. Add each to IRRELEVANT_TO with the domains that can "
          f"drop it and why, or to KEPT_EVERYWHERE_BECAUSE with the argument for keeping it. "
          f"Until then it is kept by every domain, which is safe but is not a decision.")

    check("the five domains are the five the gate accepts",
          set(SLICE.DOMAINS) == set(CHECKER.REQUIRED_DOMAINS),
          f"plan_slice.DOMAINS={sorted(SLICE.DOMAINS)} vs "
          f"check_plan_consistency.REQUIRED_DOMAINS={sorted(CHECKER.REQUIRED_DOMAINS)}. A domain "
          f"name that drifts here produces a slice for a block the report gate will reject.")

    check("the auditors are not sliceable domains",
          not (set(SLICE.AUDITORS) & set(SLICE.DOMAINS)),
          f"{sorted(set(SLICE.AUDITORS) & set(SLICE.DOMAINS))} is in both lists.")

    # _validate_table has to RAISE, not warn: every case it catches produces a slice that is
    # quietly wrong rather than an error anybody sees.
    for label, mutate in (
            ("a block in both dicts",
             lambda: SLICE.KEPT_EVERYWHERE_BECAUSE.__setitem__("imagery", "contradiction")),
            ("a mandatory keep in the deny list",
             lambda: SLICE.IRRELEVANT_TO.__setitem__("days", (SLICE.ALL_FIVE, "wrong"))),
            ("a misspelled domain name",
             lambda: SLICE.IRRELEVANT_TO.__setitem__("ui_labels",
                                                     (frozenset({"entrry"}), "typo"))),
            ("a drop with no reason",
             lambda: SLICE.IRRELEVANT_TO.__setitem__("ui_labels", (SLICE.ALL_FIVE, "   "))),
            ("a block dropped by nobody",
             lambda: SLICE.IRRELEVANT_TO.__setitem__("ui_labels", (frozenset(), "nobody"))),
    ):
        saved_irrelevant = dict(SLICE.IRRELEVANT_TO)
        saved_kept = dict(SLICE.KEPT_EVERYWHERE_BECAUSE)
        try:
            mutate()
            raised = False
            try:
                SLICE._validate_table()
            except AssertionError:
                raised = True
            check(f"_validate_table refuses {label}", raised,
                  "the table validated a state that produces a silently wrong slice")
        finally:
            SLICE.IRRELEVANT_TO.clear()
            SLICE.IRRELEVANT_TO.update(saved_irrelevant)
            SLICE.KEPT_EVERYWHERE_BECAUSE.clear()
            SLICE.KEPT_EVERYWHERE_BECAUSE.update(saved_kept)
    SLICE._validate_table()  # the restored table must still be valid

    # ------------------------------------------------- the slice is written the plan's own way
    #
    # Hardcoding indent=2 was a measured bug, not a style question: on a real workspace plan
    # written at indent=1 the slice came out 92,233 bytes against the plan's 85,836 on disk, and
    # the summary called that a 7.1% saving because it compared against its own re-indented
    # baseline. The file a verifier would actually open had grown by 7.5%.
    for label, text, expected in (
            ("two spaces", '{\n  "a": 1\n}', 2),
            ("one space", '{\n "a": 1\n}', 1),
            ("four spaces", '{\n    "a": 1\n}', 4),
            ("tabs", '{\n\t"a": 1\n}', "\t"),
            ("compact", '{"a":1}', None),
            # Newlines but no indentation. Not the same as compact, and the difference is a
            # falsy zero: `len(lead) if lead else None` reads this as compact and strips every
            # newline out of the slice.
            ("newlines with no indent", '{\n"a": 1\n}', 0),
            ("a leading BOM", '﻿{\n  "a": 1\n}', 2),
            ("a list at the top", '[\n   1\n]', 3),
            ("an empty object", "{}", None),
            ("not JSON at all", "", 2),
    ):
        check(f"detect_indent reads {label}", SLICE.detect_indent(text) == expected,
              f"got {SLICE.detect_indent(text)!r}, expected {expected!r}")

    check("a detected indent round-trips the shape it was read from",
          all(SLICE.detect_indent(SLICE._dumps({"a": {"b": 1}}, i)) == i
              for i in (0, 1, 2, 4, "\t", None)),
          "the writer and the reader disagree, so a slice would silently change a plan's format")

    with tempfile.TemporaryDirectory() as tmp_indent:
        odd = Path(tmp_indent) / "one-space.json"
        odd.write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
        out = Path(tmp_indent) / "out.json"
        # `seasonality` and not `entry`, and the reason is worth writing down: on a fixture this
        # small the provenance block the slice carries costs more than most domains save, so four
        # of the five come out LARGER and the tool correctly says so. `transport` was already in
        # that group before this line was written; `entry` joined it when the entry domain was
        # corrected to keep regional_service_context (a real verification report cites that block
        # from `entry`, so slicing it out lost a claim). The rider below is about indentation
        # arithmetic, not about which domains save, so it needs a domain that saves on THIS input.
        written_run = run_cli([str(odd), "--domain", "seasonality", "--out", str(out)])
        produced = out.read_text(encoding="utf-8")
        check("the slice keeps the plan's indentation",
              SLICE.detect_indent(produced) == 1, f"got {SLICE.detect_indent(produced)!r}")
        check("and is therefore genuinely smaller than the file it replaces",
              len(produced.encode("utf-8")) < len(odd.read_bytes())
              and "NOT smaller" not in written_run.stdout,
              f"slice {len(produced.encode('utf-8')):,} vs plan {len(odd.read_bytes()):,}")
        check("the summary compares against the bytes on disk, not a re-indented baseline",
              f"{len(odd.read_bytes()):,} bytes on disk" in written_run.stdout,
              written_run.stdout[-400:])

    # ------------------------------------------------------------------ the pointer guarantee
    full_pointers = set(pointers(plan))
    check("the fixture yields pointers to check at all", len(full_pointers) > 100,
          f"only {len(full_pointers)} pointers -- a guarantee asserted over nothing is the "
          f"green-gate-over-unexamined-output defect this repo keeps paying for")

    report_claims = {block["domain"]: block.get("claims_checked", [])
                     for block in json.loads(REPORT_TEMPLATE.read_text(encoding="utf-8"))
                     .get("domains", [])}

    for domain in SLICE.DOMAINS:
        sliced, report = SLICE.slice_plan(plan, domain)
        dropped = set(report["dropped"])

        for key in SLICE.ALWAYS_KEEP:
            check(f"{domain}: {key} is kept unconditionally",
                  key in sliced or key not in plan,
                  f"{key} was dropped; every domain dates its claims against the itinerary and "
                  f"reconciles numbers against the budget")

        # Order is not a pointer property, so nothing above can see it break -- and this file
        # claims kept blocks arrive "in their original order", which is what makes a slice
        # diffable against the plan it came from. Asserted here because a claim no test holds is
        # the claim that quietly stops being true.
        check(f"{domain}: kept keys are in the plan's own order",
              report["kept"] == [k for k in plan if k in set(report["kept"])],
              f"{report['kept']} against the plan's {list(plan)}")

        survivors = {p for p in full_pointers if root_of(p) not in dropped}
        broken = sorted(p for p in survivors if not CHECKER.resolve_pointer(sliced, p))
        check(f"{domain}: every pointer outside a dropped block still resolves",
              not broken, f"{len(broken)} broke, e.g. {broken[:5]}")

        lost = {p for p in full_pointers if not CHECKER.resolve_pointer(sliced, p)}
        unexplained = sorted(p for p in lost if root_of(p) not in dropped)
        check(f"{domain}: nothing was lost that the printed drop list does not explain",
              not unexplained, f"{len(unexplained)} unexplained, e.g. {unexplained[:5]}")

        # Renumbering is the failure a "smaller file" would hide: days[2] still resolving while
        # pointing at what used to be days[3] passes every resolution check and sends a verifier's
        # finding to the wrong day.
        #
        # Computed over the pointers that DID resolve, never over `survivors` as a whole: a
        # mutation that truncates a kept list makes value_at raise, and a test that dies on the
        # defect it was written to catch reports a traceback instead of the sentence above -- the
        # broken-pointer check two lines up is the one that names that case.
        resolved = survivors - set(broken)
        moved = sorted(p for p in resolved if value_at(plan, p) != value_at(sliced, p))
        check(f"{domain}: no kept pointer reaches a different value",
              not moved, f"{len(moved)} moved, e.g. {moved[:5]}")

        # The pointers this domain is actually expected to cite, taken from the shipped report
        # template rather than invented here.
        for pointer in report_claims.get(domain, []):
            if not CHECKER.resolve_pointer(plan, pointer):
                continue  # the template cites fields the fixture may not carry; not this test's job
            check(f"{domain}: template claims_checked pointer {pointer} survives the slice",
                  CHECKER.resolve_pointer(sliced, pointer),
                  "a verifier citing what the template tells it to cite would fail the gate")

        if domain == "sights_and_hours":
            # The one coverage rule check_verification enforces: this domain must cite every
            # dining card claiming researched or verified hours. If the slice cannot resolve one,
            # the domain cannot legally file a report at all.
            for i, day in enumerate(plan.get("days", [])):
                for j, _card in enumerate((day or {}).get("dining", []) or []):
                    pointer = f"days[{i}].dining[{j}]"
                    check(f"sights_and_hours: required dining pointer {pointer} resolves",
                          CHECKER.resolve_pointer(sliced, pointer),
                          "the hours-coverage rule cannot be satisfied from this slice")

    # slice_plan must not touch the plan it was handed: the caller still needs it, and the CLI
    # writes the slice beside it.
    before = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for domain in SLICE.DOMAINS:
        SLICE.slice_plan(before, domain)
    check("slicing does not mutate the plan it was given",
          before == json.loads(FIXTURE.read_text(encoding="utf-8")),
          "slice_plan modified its input")

    # ------------------------------------------------------------------------ the CLI contract
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        plan_path = tmp / "plan.json"
        plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

        # See the note on the indentation case below: on this fixture the provenance block costs
        # more than `entry` saves, and the "NOT smaller" contrast further down needs a run where
        # the saving is real. `seasonality` drops the most on this input.
        out = tmp / "seasonality.json"
        result = run_cli([str(plan_path), "--domain", "seasonality", "--out", str(out)])
        check("a domain slice is written and reported", result.returncode == 0 and out.exists(),
              result.stdout + result.stderr)
        written = json.loads(out.read_text(encoding="utf-8"))
        record = written.get("plan_slice", {})

        # Asserted as an EQUALITY against what actually came out, and with a floor. Written first
        # as "every recorded key is absent from the slice", it passed with the list emptied --
        # every statement about the members of an empty list is true, so the record could stop
        # describing the projection entirely and this test would report success. That is the
        # green-gate-over-unexamined-output defect this repo keeps paying for, reproduced inside
        # the test written to prevent it; caught here by mutating the script rather than by
        # reading the assertion.
        really_dropped = set(plan) - {k for k in written if k != "plan_slice"}
        check("the recorded drop list is exactly what came out of the plan",
              set(record.get("dropped_top_level_keys") or []) == really_dropped,
              f"recorded {record.get('dropped_top_level_keys')}, actually missing "
              f"{sorted(really_dropped)}")
        check("this fixture really does lose blocks, so the check above is not vacuous",
              len(really_dropped) >= 2,
              f"only {sorted(really_dropped)} dropped -- if the fixture stops carrying blocks the "
              f"entry domain does not read, this whole section stops testing anything and needs a "
              f"fixture that does")
        check("the recorded kept list is the file's own keys",
              record.get("kept_top_level_keys") == [k for k in written if k != "plan_slice"],
              record.get("kept_top_level_keys"))
        check("the drop list is also printed, so a reader without the file can check it",
              all(key in result.stdout for key in record.get("dropped_top_level_keys", [])),
              result.stdout)

        import hashlib
        check("the record binds the slice to the exact plan bytes",
              record.get("source_plan_sha256") == hashlib.sha256(plan_path.read_bytes()).hexdigest()
              and record.get("source_plan_bytes") == len(plan_path.read_bytes()),
              record)

        # Deterministic on purpose: no timestamp. A slice that differs on every run cannot be
        # diffed against the plan, and two verifiers cannot be shown to have read the same file.
        again = tmp / "seasonality-again.json"
        run_cli([str(plan_path), "--domain", "seasonality", "--out", str(again)])
        check("two runs produce a byte-identical slice",
              again.read_bytes() == out.read_bytes(), "the output carries something non-repeatable")

        for auditor in ("consistency", "completeness"):
            refused = run_cli([str(plan_path), "--domain", auditor, "--out", str(tmp / "x.json")])
            check(f"the {auditor} auditor is refused by name",
                  refused.returncode == 2 and "AUDITOR" in refused.stderr
                  and "plan path" in refused.stderr,
                  refused.stderr)

        unknown = run_cli([str(plan_path), "--domain", "entry_rules", "--out", str(tmp / "x.json")])
        check("an unknown domain is refused and the five are named",
              unknown.returncode == 2
              and all(name in unknown.stderr for name in SLICE.DOMAINS),
              unknown.stderr)

        # Every refusal below is a wrong-file or destructive case that would otherwise produce a
        # plausible-looking artifact.
        broken_cases = {
            "a bare list": "[1, 2, 3]",
            "no days key": json.dumps({"trip": {}, "budget": {}}),
            "an empty days list": json.dumps({"trip": {}, "days": [], "budget": {}}),
            "days as an object": json.dumps({"trip": {}, "days": {"1": {}}, "budget": {}}),
            "not JSON at all": "{ this is not json",
        }
        for label, text in broken_cases.items():
            path = tmp / "broken.json"
            path.write_text(text, encoding="utf-8")
            refused = run_cli([str(path), "--domain", "entry", "--out", str(tmp / "x.json")])
            check(f"{label} is refused loudly",
                  refused.returncode == 2 and refused.stderr.startswith("ERROR:"),
                  f"exit {refused.returncode}: {refused.stdout}{refused.stderr}")

        missing = run_cli([str(tmp / "nope.json"), "--domain", "entry", "--out", str(tmp / "x.json")])
        check("a missing plan file is refused loudly",
              missing.returncode == 2 and "ERROR:" in missing.stderr, missing.stderr)

        resliced = run_cli([str(out), "--domain", "entry", "--out", str(tmp / "x.json")])
        check("a slice cannot be sliced again",
              resliced.returncode == 2 and "already carries" in resliced.stderr
              and str(plan_path) in resliced.stderr,
              resliced.stderr)

        before_bytes = plan_path.read_bytes()
        overwrite = run_cli([str(plan_path), "--domain", "entry", "--out", str(plan_path)])
        check("writing the slice over the plan is refused, and the plan survives",
              overwrite.returncode == 2 and plan_path.read_bytes() == before_bytes,
              overwrite.stderr)

        piped = run_cli([str(plan_path), "--domain", "transport", "--stdout"])
        parsed = None
        try:
            parsed = json.loads(piped.stdout)
        except Exception as exc:  # noqa: BLE001
            parsed = None
            check("--stdout emits parseable JSON on stdout", False, f"{exc}: {piped.stdout[:200]}")
        if parsed is not None:
            check("--stdout emits the slice on stdout and the summary on stderr",
                  "plan_slice" in parsed and "plan slice for domain" in piped.stderr
                  and "plan slice for domain" not in piped.stdout,
                  piped.stderr[:400])

        # ------------------------------------- a slice must not become a plan in someone's audit
        #
        # audit_workspace.py recognises a plan by SHAPE -- a dict with a `days` list and a `trip`
        # key -- over a non-recursive plans/*.json glob, and its filename filter is a prefix list
        # a slice does not match. So a slice written beside the plan is audited as an itinerary
        # and reported as one missing blocks it was never supposed to have, five times per trip.
        # The property asserted here is the integration one, not the filename.
        from audit_workspace import is_plan_file  # noqa: E402 - path set at module import

        plans_dir = tmp / "plans"
        plans_dir.mkdir()
        housed = plans_dir / "2027-02-12-somewhere.json"
        housed.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        for domain in SLICE.DOMAINS:
            defaulted = run_cli([str(housed), "--domain", domain])
            check(f"{domain}: the default output location works with no --out",
                  defaulted.returncode == 0, defaulted.stdout + defaulted.stderr)
        seen = [p.name for p in sorted(plans_dir.glob("*.json")) if is_plan_file(p)]
        check("five default slices leave the plans directory holding exactly one plan",
              seen == [housed.name],
              f"audit_workspace.is_plan_file would now audit {seen} as itineraries")
        check("the slices were written, just not where a plan scan looks",
              len(list((plans_dir / "slices").glob("*.json"))) == len(SLICE.DOMAINS),
              sorted(p.name for p in (plans_dir / "slices").glob("*.json")))

        beside = run_cli([str(housed), "--domain", "entry",
                          "--out", str(plans_dir / "beside.json")])
        check("--out into the plan's own directory is warned about, not silently obeyed",
              beside.returncode == 0 and "plan's own directory" in beside.stdout,
              beside.stdout[-500:])

        # ---------------------------------------------------- a schema that grew, and CJK text
        grown = copy.deepcopy(plan)
        grown["新增顶层区块"] = {"说明": "这是表里没有的键", "值": 1}
        grown_path = tmp / "grown.json"
        grown_path.write_text(json.dumps(grown, ensure_ascii=False, indent=2), encoding="utf-8")
        grown_out = tmp / "grown-slice.json"
        grew = run_cli([str(grown_path), "--domain", "seasonality", "--out", str(grown_out)])
        grown_slice = json.loads(grown_out.read_text(encoding="utf-8"))
        check("an unrecognised top-level key is KEPT",
              grew.returncode == 0 and "新增顶层区块" in grown_slice,
              "a deny list must keep what it has not classified; an allow-list is what starves a "
              "domain when the schema grows")
        check("an unrecognised top-level key is reported, in print and in the record",
              "新增顶层区块" in grew.stdout
              and grown_slice["plan_slice"]["unrecognised_keys_kept"] == ["新增顶层区块"],
              grew.stdout)
        check("CJK survives the round trip unescaped",
              "这是表里没有的键" in grown_out.read_text(encoding="utf-8"),
              "the slice was written with ensure_ascii=True and a Chinese plan is now unreadable "
              "as text, which is how a diff against the plan stops being possible")

        # ------------------------------------------- a projection that saves nothing says so
        thin = {"trip": plan["trip"], "days": plan["days"], "budget": plan["budget"]}
        thin_path = tmp / "thin.json"
        thin_path.write_text(json.dumps(thin, ensure_ascii=False, indent=2), encoding="utf-8")
        thin_run = run_cli([str(thin_path), "--domain", "entry", "--out", str(tmp / "thin-out.json")])
        check("a slice that is not smaller than the plan says so",
              thin_run.returncode == 0 and "NOT smaller" in thin_run.stdout,
              thin_run.stdout[-600:])
        check("the fat plan's slice does NOT carry that warning",
              "NOT smaller" not in result.stdout,
              "the warning fires on a real saving, so it means nothing when it fires on none")

    if failures:
        print(f"PLAN SLICE FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all plan-slice cases passed")
    return 0


def test_plan_slice() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
