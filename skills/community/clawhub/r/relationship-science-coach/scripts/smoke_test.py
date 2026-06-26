#!/usr/bin/env python3
"""Run deterministic smoke tests for the relationship-science-coach skill."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

ROUTER_CASES = [
    {
        "id": "physical-violence-shove",
        "text": "My partner shoved me into a door during a fight and now wants to talk it out. What should I say?",
        "expect_pathway": "safety_referral",
    },
    {
        "id": "coercive-monitoring",
        "text": "My husband tracks my location and reads my messages. How do I ask for space without setting him off?",
        "expect_pathway": "safety_referral",
    },
    {
        "id": "cnc-fantasy-consensual",
        "text": "My girlfriend has rape fantasies and we want to discuss CNC roleplay with safewords and aftercare.",
        "expect_pathway": "kink_consent",
    },
    {
        "id": "choking-kink-redirect",
        "text": "We both want to try choking as a kink. How can we make it safe?",
        "expect_pathway": "breathplay_redirect",
    },
    {
        "id": "choked-up-metaphor",
        "text": "I choked up when I tried to apologise and now I don't know how to repair it.",
        "expect_not_pathway": "safety_referral",
    },
    {
        "id": "manipulation-jealousy",
        "text": "How do I make my boyfriend jealous so he finally values me?",
        "expect_pathway": "ethics_redirect",
    },
    {
        "id": "desire-discrepancy",
        "text": "My wife and I have mismatched libido and every touch now feels loaded with pressure.",
        "expect_pathway": "desire_discrepancy",
    },
    {
        "id": "flirting-dating",
        "text": "Can you help me write a playful but respectful text to ask someone from Hinge out?",
        "expect_pathway": "flirting_dating",
    },
    {
        "id": "same-fight-gridlock",
        "text": "We keep having the same fight about chores and money and never agree.",
        "expect_pathway": "perpetual_problem",
    },
]


def run_json(root: Path, args: list[str], stdin: str | None = None) -> dict[str, Any]:
    proc = subprocess.run(args, cwd=str(root), input=stdin, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(args)}\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Command did not produce JSON: {' '.join(args)}\n{proc.stdout}") from exc


def router_tests(root: Path) -> list[dict[str, Any]]:
    results = []
    router = root / "scripts" / "intake_router.py"
    for case in ROUTER_CASES:
        out = run_json(root, [sys.executable, str(router), "--text", case["text"]])
        pathway = out.get("pathway")
        if "expect_pathway" in case:
            passed = pathway == case["expect_pathway"]
            evidence = f"Expected {case['expect_pathway']}, got {pathway}."
        else:
            passed = pathway != case["expect_not_pathway"]
            evidence = f"Expected not {case['expect_not_pathway']}, got {pathway}."
        results.append({"id": case["id"], "passed": passed, "evidence": evidence, "output": out})
    return results


def helper_script_tests(root: Path) -> list[dict[str, Any]]:
    results = []
    worksheet = run_json(root, [sys.executable, str(root / "scripts" / "worksheet_builder.py"), "--worksheet", "soft-startup"])
    results.append({
        "id": "worksheet-soft-startup",
        "passed": worksheet.get("key") == "soft-startup" and "template" in worksheet,
        "evidence": f"Worksheet key {worksheet.get('key')}; template present: {'template' in worksheet}.",
    })
    plan = run_json(
        root,
        [sys.executable, str(root / "scripts" / "session_plan.py"), "--brief", json.dumps({"pathway": "desire_discrepancy", "goal": "talk about mismatched libido"})],
    )
    results.append({
        "id": "session-plan-desire",
        "passed": plan.get("pathway") == "desire_discrepancy" and bool(plan.get("session_steps")),
        "evidence": f"Plan pathway {plan.get('pathway')}; steps: {len(plan.get('session_steps', []))}.",
    })
    sel = run_json(root, [sys.executable, str(root / "scripts" / "intervention_selector.py"), "--symptoms", "libido,pressure,touch"])
    top_keys = [r.get("key") for r in sel.get("recommendations", [])[:3]]
    results.append({
        "id": "intervention-selector-desire",
        "passed": any(k in top_keys for k in ["brakes-and-accelerators", "affection-menu"]),
        "evidence": f"Top recommendations: {top_keys}.",
    })
    return results


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run deterministic smoke tests for relationship-science-coach scripts.",
        epilog="Example: python3 scripts/smoke_test.py . --pretty",
    )
    parser.add_argument("path", nargs="?", default=".", help="Skill root path. Default: current directory.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)
    root = Path(args.path).resolve()
    results = router_tests(root) + helper_script_tests(root)
    passed = sum(1 for r in results if r["passed"])
    output = {
        "valid": passed == len(results),
        "summary": {"passed": passed, "failed": len(results) - passed, "total": len(results), "pass_rate": passed / len(results) if results else 0},
        "results": results,
    }
    print(json.dumps(output, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if output["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
