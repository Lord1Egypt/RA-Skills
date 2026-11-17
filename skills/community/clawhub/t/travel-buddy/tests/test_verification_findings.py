#!/usr/bin/env python3
"""A wrong finding is closed by saying what changed, not by flipping a flag.

check_verification treated any truthy `resolved` as closed: `resolved: true` with no resolution,
even `resolved: "yes"`, made a `wrong` finding disappear, and `severity` was never read -- measured
2026-09-24 against v2.7.0, 0 errors where the control (`resolved: false`) produced 1. The replan
gate beside it had already learned this ("a bare true is the same claim as an unresolved entry,
made harder to see") and required both halves; the verification report did not. A critical
finding that vanishes takes the page's "not fact-checked" banner with it.

The report scaffold also wrote `low / medium / high` against a spec of `critical / major /
minor`, and the one real report built from it followed the scaffold. Severity is held to the spec
only where it means something -- on a wrong or misleading finding -- so that report's confirmed
findings stay valid.

Run:  python tests/test_verification_findings.py
      python -m pytest tests/test_verification_findings.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402
import new_verification_report as scaffold  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def fill(node: object) -> object:
    """Replace every scaffold placeholder with a concrete sentence, as an author would."""
    if isinstance(node, dict):
        out = {k: fill(v) for k, v in node.items()}
        if "verdict" in out:
            out["verdict"] = "confirmed"
            out["severity"] = "minor"
            out["evidence_url"] = "https://official-source.test/checked"
        return out
    if isinstance(node, list):
        return [fill(v) for v in node]
    if isinstance(node, str) and node.startswith("TODO:"):
        return "Opened the source page and read the rule for these dates."
    return node


PLAN = json.loads(FIXTURE.read_text(encoding="utf-8"))
REPORT = fill(scaffold.build(PLAN, Path("plan.json"))[0])


def errors_with(finding: dict) -> list[str]:
    """Errors the report produces with `finding` added, minus what the clean report produces."""
    def run(report: dict) -> list[str]:
        found: list[str] = []
        cpc.check_verification(report, found, [], plan=PLAN, plan_path="plan.json")
        return found
    baseline = run(REPORT)
    report = json.loads(json.dumps(REPORT))
    report["domains"][0]["findings"].append(finding)
    return [e for e in run(report) if e not in baseline]


def wrong(**over) -> dict:
    finding = {"claim": "the dinner venue is open on Mondays", "verdict": "wrong",
               "correction": "it is closed on Mondays", "severity": "major",
               "evidence_url": "https://venue.test/hours", "resolved": True,
               "resolution": "Moved the Monday dinner to Casa Nova, open Mondays until 23:00."}
    finding.update(over)
    return finding


def main() -> int:
    # The control: a finding closed properly, in the shape every legacy report uses.
    check("a resolved wrong finding with a resolution and a spec severity passes",
          not errors_with(wrong()), errors_with(wrong()))
    check("the control still fails when the finding is left open",
          errors_with(wrong(resolved=False)), "resolved: false produced no error")

    # (a) The bare flag.
    found = errors_with(wrong(resolution=None))
    check("resolved true with no resolution is still open",
          any("resolution" in e for e in found), found)
    # (b) A truthy string is not the JSON literal.
    found = errors_with(wrong(resolved="yes"))
    check("resolved 'yes' is not the literal true", any("'yes'" in e for e in found), found)
    # (c) The scaffold's own placeholder is not a resolution.
    found = errors_with(wrong(resolution="TODO: later"))
    check("a placeholder resolution is still open", any("placeholder" in e for e in found), found)
    # (d) Severity on a wrong finding is the spec's vocabulary.
    found = errors_with(wrong(severity="catastrophic-ish"))
    check("a wrong finding's severity is critical, major or minor",
          any("catastrophic-ish" in e for e in found), found)
    # (e) An audit block is held to the same rule as a domain.
    report = json.loads(json.dumps(REPORT))
    report["audits"][0]["findings"].append(wrong(resolution=""))
    found: list[str] = []
    cpc.check_verification(report, found, [], plan=PLAN, plan_path="plan.json")
    check("an audit's bare resolved flag is refused too",
          any("resolution" in e for e in found), found)
    # (f) A confirmed finding's severity carries no meaning and is left alone -- the newest real
    #     report, built from the old scaffold, has `high` on confirmed findings.
    check("a confirmed finding with the old scaffold's severity passes",
          not errors_with({"claim": "the museum opens at 10:00", "verdict": "confirmed",
                           "severity": "high", "evidence_url": "https://museum.test/",
                           "resolved": False, "resolution": None}))

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("verification finding cases passed")
    return 0


def test_verification_findings() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
