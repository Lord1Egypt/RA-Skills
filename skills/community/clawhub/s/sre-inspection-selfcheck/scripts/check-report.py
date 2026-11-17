#!/usr/bin/env python3
"""Check falsification metadata in a JSON selfcheck summary, not business quality."""
import argparse
import json
from pathlib import Path
import sys


def inspect_report(report):
    if not isinstance(report, dict) or not isinstance(report.get("selfcheck"), dict):
        raise ValueError("Require a selfcheck object")
    summary = report["selfcheck"]
    requirement = summary.get("falsification_requirement", "unknown")
    if requirement not in ("required", "not_required", "unknown"):
        raise ValueError("Invalid falsification_requirement")
    attempts = summary.get("falsification_attempts", [])
    if not isinstance(attempts, list):
        raise ValueError("falsification_attempts must be an array")
    issues = []
    if requirement == "unknown":
        issues.append("否证适用性未说明")
    valid = 0
    for index, attempt in enumerate(attempts):
        if not isinstance(attempt, dict):
            issues.append(f"否证记录{index + 1}不是对象")
            continue
        fields = ("case_id", "attempt", "expected_counterevidence", "observed")
        has_text = all(isinstance(attempt.get(key), str) and attempt[key].strip()
                       for key in fields)
        refs = attempt.get("evidence_refs")
        has_refs = isinstance(refs, list) and bool(refs) and all(
            isinstance(ref, str) and ref.strip() for ref in refs)
        if has_text and has_refs:
            valid += 1
        else:
            issues.append(f"否证记录{index + 1}缺案例/动作/反证预期/观察/证据引用")
    reason = summary.get("falsification_not_required_reason")
    if requirement == "not_required" and not (isinstance(reason, str) and reason.strip()):
        issues.append("声明无需否证但未提供理由")
    if not attempts and requirement != "not_required":
        issues.append("否证尝试未记录")
    status = ("not_recorded" if not attempts and requirement != "not_required"
              else "incomplete" if issues else "recorded_unverified" if attempts
              else "not_required_declared")
    return {
        "schema_version": "selfcheck-report-review/0.1.0",
        "falsification_status": status,
        "complete_records": valid,
        "issues": issues,
        "metadata_complete": not issues,
        "business_verdict": "not_evaluated",
        "notice": "只检查记录完整性，不验证引用、否证有效性、适用性声明或业务正确性",
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        if args.report.stat().st_size > 2 * 1024 * 1024:
            raise ValueError("Summary exceeds 2 MiB")
        result = inspect_report(json.loads(args.report.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError) as error:
        print(json.dumps({"input_error": type(error).__name__,
                          "business_verdict": "not_evaluated"}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["metadata_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
