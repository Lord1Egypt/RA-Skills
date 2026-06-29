#!/usr/bin/env python3
"""
run_script_tests.py — Execute script-layer tests, compare output against expectations.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--cases", required=True, help="Path to cases.json")
    p.add_argument("--skill-dir", required=True, help="Path to skill dir (used as cwd for script execution)")
    p.add_argument("--testres-dir", default="", help="Test resources dir (skill-regression-space/testres/<skill-name>)")
    p.add_argument("--work-dir", default="", help="Output dir for this run (skill-regression-space/output/<skill-name>/<timestamp>)")
    p.add_argument("--output", required=True, help="Output JSON path")
    p.add_argument("--script-timeout", type=int, default=30, help="Single-script timeout in seconds")
    p.add_argument("--cases-filter", default="", help="Comma-separated case IDs to run (used by --rerun)")
    return p.parse_args()


def match_output(actual: str, expected: str, mode: str) -> tuple[bool, str]:
    """Check if actual output matches expectation."""
    if not expected:
        return True, "no assertion (auto-pass)"

    actual_stripped = actual.strip()

    if mode == "contains":
        ok = expected in actual_stripped
        return ok, f"{'contains' if ok else 'missing'} keyword: {repr(expected)}"
    elif mode == "regex":
        try:
            ok = bool(re.search(expected, actual_stripped, re.IGNORECASE))
            return ok, f"{'matches' if ok else 'does not match'} regex: {repr(expected)}"
        except re.error as e:
            return False, f"regex error: {e}"
    elif mode == "exact":
        ok = actual_stripped == expected
        return ok, f"{'exact-matches' if ok else 'differs from'} expected output"
    else:
        return False, f"unknown match mode: {mode}"


def expand_placeholders(cmd: str, skill_dir: str, testres_dir: str, work_dir: str) -> str:
    """Substitute placeholders in script_cmd:
    {SKILL_DIR}    → target skill directory
    {TESTRES_DIR}  → skill-regression-space/testres/<skill-name> (fixtures, helper scripts)
    {WORK_DIR}     → skill-regression-space/output/<skill-name>/<timestamp> (this run output)
    """
    cmd = cmd.replace("{SKILL_DIR}", skill_dir)
    cmd = cmd.replace("{TESTRES_DIR}", testres_dir if testres_dir else "/tmp")
    cmd = cmd.replace("{WORK_DIR}", work_dir if work_dir else "/tmp")
    # Legacy placeholder support, mapped to TESTRES_DIR
    cmd = cmd.replace("{REGRESSION_DIR}", testres_dir if testres_dir else "/tmp")
    return cmd


def run_script_case(case: dict, skill_dir: str, timeout: int, testres_dir: str = "", work_dir: str = "") -> dict:
    """Execute a single script-layer test case."""
    result = {
        "id": case["id"],
        "name": case["name"],
        "type": case["type"],
        "status": "skip",
        "script_cmd": case.get("script_cmd", ""),
        "actual_output": "",
        "expected_output": case.get("expected_output", ""),
        "match_mode": case.get("expected_output_mode", "contains"),
        "match_reason": "",
        "duration_ms": 0,
        "error": "",
    }

    script_cmd = expand_placeholders(
        case.get("script_cmd", "").strip(), skill_dir, testres_dir, work_dir
    )
    result["script_cmd"] = script_cmd  # Update with expanded command for reporting
    if not script_cmd:
        result["status"] = "skip"
        result["match_reason"] = "no script command, skipped"
        print(f"    ⏭️  {case['name']} — skipped (no script cmd)")
        return result

    start = time.time()
    try:
        # ⚠️  Security: script_cmd comes from TEST.md and runs via shell=True,
        # meaning any command in TEST.md will execute. Only trust TEST.md from trusted sources.
        # ⚠️  Output merging: actual_output = stdout + stderr,
        # which is risky for exact-mode assertions (stderr warnings break match). Prefer contains/regex.
        proc = subprocess.run(
            script_cmd,
            shell=True,
            cwd=skill_dir,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        elapsed = int((time.time() - start) * 1000)
        actual_output = proc.stdout + proc.stderr
        result["actual_output"] = actual_output
        result["duration_ms"] = elapsed

        ok, reason = match_output(actual_output, result["expected_output"], result["match_mode"])
        result["status"] = "pass" if ok else "fail"
        result["match_reason"] = reason

        icon = "✅" if ok else "❌"
        print(f"    {icon} {case['name']} ({elapsed}ms) — {reason}")

    except subprocess.TimeoutExpired:
        result["status"] = "fail"
        result["error"] = f"script timeout (>{timeout}s)"
        result["duration_ms"] = timeout * 1000
        print(f"    ⏰ {case['name']} — timeout (>{timeout}s)")
    except Exception as e:
        result["status"] = "fail"
        result["error"] = str(e)
        print(f"    💥 {case['name']} — exception: {e}")

    return result


def main():
    args = parse_args()

    with open(args.cases, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data["cases"]
    skill_dir = data["skill_dir"]

    # --cases-filter: only run specified case IDs (used by --rerun)
    if args.cases_filter:
        filter_ids = set(args.cases_filter.split(","))
        cases = [c for c in cases if c["id"] in filter_ids]
        print(f"  [--cases-filter] only running {len(cases)} cases: {args.cases_filter}")

    print(f"  Running script-layer tests for {len(cases)} cases...")
    results = []
    for case in cases:
        result = run_script_case(case, skill_dir, args.script_timeout, args.testres_dir, args.work_dir)
        results.append(result)

    # Stats
    pass_count = sum(1 for r in results if r["status"] == "pass")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    skip_count = sum(1 for r in results if r["status"] == "skip")
    print(f"\n  Script layer summary: pass {pass_count} | fail {fail_count} | skipped {skip_count}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
