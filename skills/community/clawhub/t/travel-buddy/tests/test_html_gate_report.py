#!/usr/bin/env python3
"""Regression tests for the machine-readable form of scripts/validate_trip_html.py.

`--json` exists so an iterating model does not re-read a delivered page to find out WHERE a
finding is. A delivered page in this workspace is around 130 kB and, because the renderer emits
the whole body on one line, "line 32" covers 93% of it -- so the pointer has to be a line AND a
column, and it has to be checked against the page rather than guessed.

Everything here is about the report, not about the rules: the findings themselves are unchanged,
and the property that keeps it that way is that a finding's message plus its rule's citation is
byte-for-byte the line the prose report prints.

Run:  python tests/test_html_gate_report.py
      python -m pytest tests/test_html_gate_report.py
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "scripts" / "validate_trip_html.py"

sys.path.insert(0, str(ROOT / "scripts"))
_spec = importlib.util.spec_from_file_location("_html_gate_under_test", GATE)
GATE_MODULE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(GATE_MODULE)

# Deliberately defective, and deliberately small. The provider name is CJK so a finding carrying
# it proves the report is not \u-escaped -- an escaped report is both bigger and unsearchable,
# which on a Chinese workspace is most of the value of having one.
PAGE = (
    '<html><body><h1>测试行程</h1>\n'
    '<section id="trip-plan" data-trip-plan="1">\n'
    '<article class="day-card" data-day="1">'
    '<a class="booking-link" data-booking-type="hotel" data-provider="携程 Ctrip" '
    'href="https://www.booking.com/x">open</a></article>\n'
    '</section></body></html>')

MANUAL_FLAGS = ("--expected-days", "1", "--require-booking-type", "hotel",
                "--transport-mode", "public-transit", "--require-unverified-banner")


def gate(path: Path, *extra: str) -> tuple[int, str, str]:
    proc = subprocess.run([sys.executable, str(GATE), str(path), *extra],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def pointer_cases() -> list[str]:
    """Every pointer names a real place on the page, and "no place" is said rather than faked."""
    failures: list[str] = []
    module = GATE_MODULE
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(PAGE, encoding="utf-8")
        code, out, _err = gate(page, *MANUAL_FLAGS, "--json")
        try:
            doc = json.loads(out)
        except ValueError as exc:
            return [f"json: a defective page did not print valid JSON ({exc}): {out[:200]}"]
        if code != 1 or doc["ok"] is not False:
            failures.append(f"json: a defective page must exit 1 and say ok false, got {code}")
        if "携程 Ctrip" not in out:
            failures.append("json: CJK was escaped or lost; the report has to stay searchable")

        lines = PAGE.split("\n")
        placed = 0
        for finding in doc["findings"]:
            if set(finding) != {"rule_id", "pointer", "message"}:
                failures.append(f"json: a finding carries {sorted(finding)}, not the three fields "
                                f"callers are told to expect")
                break
            pointer = finding["pointer"]
            if pointer is None:
                continue
            placed += 1
            # "line N col M", 1-based line and 0-based column, and it must land on a tag. A
            # pointer that lands in the middle of an attribute value is not a location, it is a
            # number that looks like one.
            parts = pointer.split()
            if len(parts) != 4 or parts[0] != "line" or parts[2] != "col":
                failures.append(f"json: pointer {pointer!r} is not 'line N col M'")
                continue
            row, column = int(parts[1]), int(parts[3])
            if not 1 <= row <= len(lines) or column >= len(lines[row - 1]):
                failures.append(f"json: pointer {pointer!r} is off the end of the page")
                continue
            if lines[row - 1][column] != "<":
                failures.append(f"json: pointer {pointer!r} lands on "
                                f"{lines[row - 1][column:column + 12]!r}, not on a tag")
        if not placed:
            failures.append("json: nothing on this page was placed, so nothing above was tested")
        if all(finding["pointer"] for finding in doc["findings"]):
            failures.append("json: every finding was placed, including the page-wide ones -- a "
                            "pointer that is always non-null is a guess, not a location")

        # Not every rule can be placed, and the field must SAY so rather than go missing: an
        # author who cannot tell "no pointer" from "pointer forgotten" reads the page anyway.
        if not any("pointer" in finding and finding["pointer"] is None
                   for finding in doc["findings"]):
            failures.append("json: no finding reported a null pointer, so 'nothing to point at' "
                            "is indistinguishable from an omitted field")

    # The fallbacks: an id the page declares is placed, an id it does not declare is not, and
    # neither raises on the shapes a caller can actually hand over.
    if module.finding_pointer("#trip-plan needs data-service-market.", None, PAGE) is None:
        failures.append("pointer: an id the page declares must be placed")
    if module.finding_pointer("Missing required region #nowhere-at-all.", None, PAGE) is not None:
        failures.append("pointer: an id the page does not declare must place nothing")
    for label, args in (
            ("no message", (None, None, PAGE)),
            ("no content", ("#trip-plan", None, None)),
            ("empty page", ("#trip-plan", None, "")),
            ("garbage position", ("anything", "line 4", PAGE)),
            ("short position", ("anything", (4,), PAGE))):
        try:
            got = module.finding_pointer(*args)
        except Exception as exc:  # noqa: BLE001 - the point is that nothing escapes
            failures.append(f"pointer: {label} raised {type(exc).__name__}: {exc}")
            continue
        if got is not None:
            failures.append(f"pointer: {label} produced {got!r} instead of nothing")
    return failures


def losslessness_cases() -> list[str]:
    """message + its rule rebuilds the prose finding exactly, so nothing was reworded or dropped.

    This is the whole defence against a machine-readable mode drifting into a summary. The
    reasoning in a finding is what lets a reader generalise to the case the rule never enumerated,
    so it has to be carried across, not compressed away.
    """
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(PAGE, encoding="utf-8")
        _code, prose_out, _err = gate(page, *MANUAL_FLAGS)
        _code, json_out, _err = gate(page, *MANUAL_FLAGS, "--json")
        prose = [line[2:] for line in prose_out.splitlines() if line.startswith("- ")]
        doc = json.loads(json_out)
        rebuilt = [f["message"] + doc["rules"][f["rule_id"]] for f in doc["findings"]]
        if rebuilt != prose:
            failures.append(f"json: rebuilding gave {len(rebuilt)} finding(s) against "
                            f"{len(prose)} prose line(s)")
            for built, original in zip(rebuilt, prose):
                if built != original:
                    failures.append(f"json: rebuilt {built[:80]!r} against {original[:80]!r}")
                    break
        for finding in doc["findings"]:
            if finding["rule_id"] not in doc["rules"]:
                failures.append(f"json: {finding['rule_id']} has no rules entry, so its citation "
                                f"is nowhere in the output")
                break
        # The ids are the ones cite() was called with, not something reconstructed from the
        # citation: several rules share a reference section, so the citation names the paragraph
        # and not the rule.
        if "link.provider_identity" not in doc["rules"]:
            failures.append(f"json: the provider-identity rule id is missing; got "
                            f"{sorted(doc['rules'])}")
        if "uncited" in doc["rules"]:
            failures.append("json: a finding came back with no rule id, which means a site "
                            "bypassed cite() or the registry lost it")

        clean = json.loads(GATE_MODULE.findings_json([], [], [], "", [], ok=True))
        if clean != {"ok": True, "findings": [], "rules": {}, "notes": []}:
            failures.append(f"json: a page with no findings must report an empty ok document, "
                            f"got {clean}")
    return failures


def refusal_cases() -> list[str]:
    """A wrapper that always passes --json must get JSON from every exit, refusals included."""
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(PAGE, encoding="utf-8")
        plan = Path(tmp) / "other-trip.json"
        plan.write_text(json.dumps({"trip": {"title": "另一趟行程"}}, ensure_ascii=False),
                        encoding="utf-8")
        for label, argv in (
                ("no --plan and no manual flags", (page, "--json")),
                ("unreadable page", (Path(tmp) / "nope.html", *MANUAL_FLAGS, "--json")),
                ("--plan beside a manual flag",
                 (page, "--plan", str(plan), "--expected-days", "1", "--json"))):
            code, out, err = gate(*argv)
            if code == 0:
                failures.append(f"refusal: {label} must not exit 0")
            try:
                doc = json.loads(out)
            except ValueError as exc:
                failures.append(f"refusal: {label} printed unparseable stdout ({exc}): {out[:120]}")
                continue
            if doc["ok"] is not False or not doc["findings"]:
                failures.append(f"refusal: {label} produced JSON that does not say what went wrong")
            if "ERROR" not in err:
                failures.append(f"refusal: {label} stopped explaining itself on stderr")

        # Without the flag the refusals must be exactly what they were: prose on stderr and
        # nothing on stdout, or every caller that greps this output starts seeing JSON.
        code, out, err = gate(page)
        if out.strip() or "ERROR" not in err:
            failures.append("refusal: the prose form must keep stderr-only refusals")

        # The success path has to be parseable too, and this is the case that was not.
        # `--assert-verified-without-plan` printed its disarm warning straight to stdout, ABOVE
        # the JSON body -- so `json.loads(stdout)` raised on exactly the run where the operator
        # had turned off the traveller-facing "not fact-checked" banner, which is the one run a
        # wrapper most needs to read. A wrapper that recovers by skipping unparseable lines drops
        # the warning instead, which is the worse of the two failures. Both halves are pinned:
        # stdout parses, AND the warning is still in the output rather than quietly relocated.
        # MANUAL_FLAGS carries --require-unverified-banner, which argparse refuses beside
        # --assert-verified-without-plan -- they are the two answers to one question.
        asserted_flags = tuple(f for f in MANUAL_FLAGS if f != "--require-unverified-banner")
        code, out, err = gate(page, *asserted_flags, "--assert-verified-without-plan", "--json")
        try:
            doc = json.loads(out)
        except ValueError as exc:
            failures.append(f"--assert-verified-without-plan leaked prose onto stdout under "
                            f"--json, so the body is unparseable ({exc}): {out[:160]}")
        else:
            if not any("ASSERTED, NOT READ" in note for note in doc.get("notes", [])):
                failures.append(
                    "--assert-verified-without-plan under --json no longer carries its disarm "
                    "warning anywhere a JSON consumer can see it; moving it to stderr to make the "
                    "body parse would hide the one thing this flag has to announce")
        code, out, err = gate(page, *asserted_flags, "--assert-verified-without-plan")
        if "ASSERTED, NOT READ" not in out + err:
            failures.append("the prose form stopped announcing --assert-verified-without-plan")
    return failures


def main() -> int:
    failures: list[str] = []
    failures += pointer_cases()
    failures += losslessness_cases()
    failures += refusal_cases()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all html gate report cases passed")
    return 0


def test_html_gate_report() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green -- the same false green the cases
    above exist to stop. Running the file directly is unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
