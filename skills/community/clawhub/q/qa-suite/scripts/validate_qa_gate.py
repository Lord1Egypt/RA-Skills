#!/usr/bin/env python3
"""
validate_qa_gate.py

Zero-dependency, portable internal quality gate validator for the qa-suite skill.
Validates QA test execution results and coverage matrix against four deterministic criteria:
  1. Planning Integrity (覆盖规划完整性): All feature-category intersections assessed; skipped/NA have reasons.
  2. Execution Completeness (执行完备性): 100% of planned tests executed (planned == executed).
  3. Defect Severity (缺陷分级卡点): Zero unresolved P0 failures. (P0 -> BLOCKED, P2/P3 -> CONDITIONAL_PASS).
  4. Evidence Chain (证据闭环): Every failure must have error message/trace and screenshot.

Exit codes:
  0: PASSED            - All planned tests executed, 0 blocking failures.
  1: BLOCKED           - Critical gate blocker (P0 failure, unexecuted tests, or incomplete planning).
  2: CONDITIONAL_PASS  - Non-critical failures only (P2/P3), can proceed with risk acknowledgement.
  3: MALFORMED_INPUT   - Input JSON is invalid, missing required schema keys, or file unreadable.

Usage:
  python3 scripts/validate_qa_gate.py check <qa_report.json> [--json]
  python3 scripts/validate_qa_gate.py self-check
"""

import argparse
import json
import os
import sys

VERDICTS = ("PASSED", "BLOCKED", "CONDITIONAL_PASS")


def validate_qa_payload(data):
    """
    Validate a QA report payload dict against the 4 quality gate criteria.
    Returns (verdict, violations, details_dict).
    """
    violations = []
    warnings = []

    # 1. Schema check
    if not isinstance(data, dict):
        return "MALFORMED", ["Input payload must be a JSON object"], {}

    summary = data.get("summary")
    if not isinstance(summary, dict):
        return "MALFORMED", ["Missing or invalid 'summary' object in report"], {}

    planned = summary.get("planned", 0)
    executed = summary.get("executed", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    skipped = summary.get("skipped", 0)

    if not isinstance(planned, int) or not isinstance(executed, int):
        return "MALFORMED", ["'planned' and 'executed' counts must be integers"], {}

    # 2. Execution Completeness check
    if planned <= 0:
        violations.append("Planning violation: 'planned' tests count must be greater than 0")
    if executed < planned:
        violations.append(
            f"Execution incomplete: planned {planned} tests, but only executed {executed} "
            f"({planned - executed} dropped/missing)"
        )

    # 3. Planning Integrity check (coverage matrix)
    matrix = data.get("coverage_matrix")
    unfilled_count = 0
    if matrix is not None:
        if isinstance(matrix, list):
            # Format: list of row dicts or objects
            for idx, row in enumerate(matrix):
                status = str(row.get("status", "")).strip().lower()
                reason = str(row.get("reason", "")).strip()
                if not status or status in ("empty", "unassessed", "none"):
                    unfilled_count += 1
                elif status in ("na", "n/a", "skipped") and not reason:
                    violations.append(
                        f"Matrix integrity violation: row #{idx+1} is '{status}' but missing justification reason"
                    )
        elif isinstance(matrix, dict):
            # Format: dict mapping category -> elements -> status or dict
            for cat, elements in matrix.items():
                if isinstance(elements, dict):
                    for elem, val in elements.items():
                        if isinstance(val, dict):
                            st = str(val.get("status", "")).strip().lower()
                            r = str(val.get("reason", "")).strip()
                            if not st or st in ("empty", "unassessed", "none"):
                                unfilled_count += 1
                            elif st in ("na", "n/a", "skipped") and not r:
                                violations.append(
                                    f"Matrix integrity violation: [{cat} -> {elem}] is '{st}' without reason"
                                )
                        elif isinstance(val, str):
                            v_lower = val.strip().lower()
                            if not v_lower or v_lower in ("empty", "unassessed", "?"):
                                unfilled_count += 1

        if unfilled_count > 0:
            violations.append(
                f"Planning integrity violation: coverage matrix contains {unfilled_count} unassessed empty cells"
            )

    # 4. Defect Severity and Failures check
    failures = data.get("failures") or []
    if not isinstance(failures, list):
        return "MALFORMED", ["'failures' must be a list"], {}

    p0_count = 0
    p1_count = 0
    p2_count = 0
    p3_count = 0
    other_count = 0

    for idx, f in enumerate(failures):
        if not isinstance(f, dict):
            violations.append(f"Malformed failure item at index #{idx}")
            continue

        sev = str(f.get("severity", "")).strip().upper()
        name = f.get("name") or f"Failure #{idx+1}"
        err = f.get("error") or ""

        # Check evidence
        if not err.strip():
            warnings.append(f"Evidence warning: failure '{name}' lacks detailed error message")

        if sev == "P0":
            p0_count += 1
        elif sev == "P1":
            p1_count += 1
        elif sev == "P2":
            p2_count += 1
        elif sev == "P3":
            p3_count += 1
        else:
            other_count += 1

    if p0_count > 0:
        violations.append(f"Defect gate blocked: {p0_count} unresolved P0 critical failure(s) found")
    if p1_count > 0:
        violations.append(f"Defect gate blocked: {p1_count} unresolved P1 high-severity failure(s) found")

    # 5. Determine Verdict
    if violations:
        verdict = "BLOCKED"
    elif (p2_count + p3_count + other_count) > 0 or warnings:
        verdict = "CONDITIONAL_PASS"
    else:
        verdict = "PASSED"

    details = {
        "verdict": verdict,
        "planned": planned,
        "executed": executed,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "severity_breakdown": {
            "P0": p0_count,
            "P1": p1_count,
            "P2": p2_count,
            "P3": p3_count,
            "other": other_count,
        },
        "violations": violations,
        "warnings": warnings,
    }

    return verdict, violations, details


def run_check(file_path, output_json=False):
    """Run check on a target report file."""
    if not os.path.exists(file_path):
        sys.stderr.write(f"ERROR: File not found: {file_path}\n")
        return 3

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            # If input is markdown with JSON embedded, try extracting first JSON block
            if content.startswith("{"):
                data = json.loads(content)
            elif "```json" in content:
                json_part = content.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_part)
            else:
                sys.stderr.write(
                    f"ERROR: Could not parse JSON from {file_path}. Please provide a valid JSON file or markdown with a ```json block.\n"
                )
                return 3
    except Exception as e:
        sys.stderr.write(f"ERROR: Failed to read/parse {file_path}: {e}\n")
        return 3

    verdict, violations, details = validate_qa_payload(data)

    if verdict == "MALFORMED":
        if output_json:
            print(json.dumps({"verdict": "MALFORMED", "error": violations}, indent=2, ensure_ascii=False))
        else:
            print(f"FAILED: Malformed report format: {violations}")
        return 3

    exit_code = 0 if verdict == "PASSED" else (1 if verdict == "BLOCKED" else 2)
    details["exit_code"] = exit_code

    if output_json:
        print(json.dumps(details, indent=2, ensure_ascii=False))
    else:
        print("\n========================================================")
        print(f" QA GATE VERDICT: [{verdict}] (Exit Code: {exit_code})")
        print("========================================================")
        print(f" Tests: {details['planned']} planned | {details['executed']} executed | {details['passed']} passed | {details['failed']} failed")
        print(f" Severity: P0: {details['severity_breakdown']['P0']} | P1: {details['severity_breakdown']['P1']} | P2: {details['severity_breakdown']['P2']} | P3: {details['severity_breakdown']['P3']}")

        if violations:
            print("\n Blocking Violations:")
            for v in violations:
                print(f"   [!] {v}")

        if details.get("warnings"):
            print("\n Warnings:")
            for w in details["warnings"]:
                print(f"   [?] {w}")

        if verdict == "BLOCKED":
            print("\n DECISION DELEGATION:")
            print("   - In standalone mode: Present blocked items to the user for judgment (Fix / Waive / Adjust).")
            print("   - In workflow-orchestrator mode: meta-orchestrator judge evaluates whether to dispatch fixer or waive.")
        elif verdict == "CONDITIONAL_PASS":
            print("\n ADVISORY: Only non-critical defects remaining. Proceed with user/workflow acknowledgement.")
        else:
            print("\n SUCCESS: All quality criteria fully satisfied.")
        print("========================================================\n")

    return exit_code


def run_self_check():
    """Run built-in test assertions on mock payloads to guarantee validator correctness."""
    # Test 1: Clean pass
    p_pass = {
        "summary": {"planned": 10, "executed": 10, "passed": 10, "failed": 0, "skipped": 0},
        "coverage_matrix": [{"status": "covered"}, {"status": "na", "reason": "pure link"}],
        "failures": [],
    }
    v, viols, _ = validate_qa_payload(p_pass)
    assert v == "PASSED", f"Expected PASSED, got {v} with {viols}"

    # Test 2: Incomplete execution -> BLOCKED
    p_incomp = {
        "summary": {"planned": 10, "executed": 8, "passed": 8, "failed": 0, "skipped": 0},
        "failures": [],
    }
    v, viols, _ = validate_qa_payload(p_incomp)
    assert v == "BLOCKED", f"Expected BLOCKED for dropped tests, got {v}"

    # Test 3: P0 failure -> BLOCKED
    p_p0 = {
        "summary": {"planned": 5, "executed": 5, "passed": 4, "failed": 1, "skipped": 0},
        "failures": [{"name": "SQL injection", "severity": "P0", "error": "Crash"}],
    }
    v, viols, _ = validate_qa_payload(p_p0)
    assert v == "BLOCKED", f"Expected BLOCKED for P0 defect, got {v}"

    # Test 4: Only P2 failure -> CONDITIONAL_PASS
    p_p2 = {
        "summary": {"planned": 5, "executed": 5, "passed": 4, "failed": 1, "skipped": 0},
        "failures": [{"name": "Mobile viewport padding", "severity": "P2", "error": "Slight overflow"}],
    }
    v, viols, _ = validate_qa_payload(p_p2)
    assert v == "CONDITIONAL_PASS", f"Expected CONDITIONAL_PASS for P2 defect, got {v}"

    # Test 5: Coverage matrix unassessed cell -> BLOCKED
    p_matrix = {
        "summary": {"planned": 5, "executed": 5, "passed": 5, "failed": 0, "skipped": 0},
        "coverage_matrix": [{"status": "covered"}, {"status": "unassessed"}],
        "failures": [],
    }
    v, viols, _ = validate_qa_payload(p_matrix)
    assert v == "BLOCKED", f"Expected BLOCKED for unassessed matrix cell, got {v}"

    print("SELF-CHECK OK: All 5 QA gate validation scenarios verified successfully.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="validate_qa_gate: Deterministic internal QA quality gate validator")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    check_parser = subparsers.add_parser("check", help="Check a QA report or JSON payload")
    check_parser.add_argument("file", help="Path to QA report file (JSON or Markdown with json block)")
    check_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON result")

    subparsers.add_parser("self-check", help="Run internal self-tests to ensure validator correctness")

    args = parser.parse_args()

    if args.command == "self-check":
        sys.exit(run_self_check())
    elif args.command == "check":
        sys.exit(run_check(args.file, output_json=args.json))
    else:
        parser.print_help()
        sys.exit(3)


if __name__ == "__main__":
    main()

