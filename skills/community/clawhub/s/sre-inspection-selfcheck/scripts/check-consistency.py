#!/usr/bin/env python3
"""Optional report consistency checks; never a business acceptance evaluator."""
import argparse
import json
import math
from pathlib import Path
import re
import sys


# All remaining registered metrics are simple count ratios. Composite metrics
# deliberately remain manual: do not invent a scalar unit for a vector/report.
NON_RATIO_IDS = set("""
E1-06b E1-06d E2-01a E2-03b E2-04a E3-03a E3-04b E4-03a
E5-03a E5-04a E6-01a E6-02a E6-02b E6-03a E6-04a E7-01a E7-01b
""".split())
CHECKS = ("metrics", "inventory", "reanalysis")
STATUSES = ("PASS", "FAIL", "UNKNOWN", "NOT_APPLICABLE")


def text(value):
    return isinstance(value, str) and bool(value.strip())


def count(value):
    return type(value) is int and value >= 0


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def registered_ids():
    reference = Path(__file__).resolve().parents[1] / "references/scope-and-metrics.md"
    return set(re.findall(r"^\| (E[1-7]-\d{2}[a-z]) \|", reference.read_text(encoding="utf-8"), re.M))


def id_list(value, label, issues):
    if not isinstance(value, list) or not all(text(item) for item in value):
        issues.append(f"{label}: require an array of nonempty IDs")
        return []
    if len(value) != len(set(value)):
        issues.append(f"{label}: duplicate IDs")
    return value


def check_metrics(summary, issues, manual):
    registry = registered_ids()
    expected = id_list(summary.get("expected_metric_ids"), "expected_metric_ids", issues)
    if not expected:
        issues.append("expected_metric_ids: selected metric inventory is missing or empty")
    for metric_id in expected:
        if metric_id not in registry:
            issues.append(f"expected_metric_ids: unregistered metric {metric_id}")
    metrics = summary.get("metrics")
    if not isinstance(metrics, list):
        issues.append("metrics: require an array")
        return
    seen = set()
    for index, metric in enumerate(metrics):
        label = f"metrics[{index}]"
        if not isinstance(metric, dict):
            issues.append(f"{label}: require an object")
            continue
        metric_id = metric.get("id")
        if not isinstance(metric_id, str) or metric_id not in registry:
            issues.append(f"{label}: unregistered metric ID")
            continue
        label = metric_id
        if metric_id in seen:
            issues.append(f"{label}: duplicate metric; split strata in an appendix")
        seen.add(metric_id)
        value, n = metric.get("value"), metric.get("n")
        if metric.get("verdict") == "satisfied" and not text(metric.get("criterion")):
            issues.append(f"{label}: satisfied requires a recorded criterion with its source")
        if metric_id in NON_RATIO_IDS:
            if value is not None and not text(metric.get("unit")):
                issues.append(f"{label}: measured value requires an explicit unit")
            manual.append(f"{label}: non-ratio unit, value and aggregation require manual review")
            continue
        if n is None and value is None and metric.get("numerator") is None:
            if not text(metric.get("caveat")) or metric.get("verdict") != "insufficient_evidence":
                issues.append(f"{label}: unmeasured ratio requires caveat and insufficient_evidence")
            continue
        numerator = metric.get("numerator")
        if not count(n) or not count(numerator) or numerator > n:
            issues.append(f"{label}: numerator/n must be integer counts with 0 <= numerator <= n")
            continue
        source = metric.get("denominator_source")
        if not isinstance(source, dict) or not all(text(source.get(k)) for k in ("kind", "reference")):
            issues.append(f"{label}: denominator_source requires kind and reference")
        elif metric_id == "E3-01a" and source["kind"] not in ("plan", "admission"):
            issues.append(f"{label}: denominator must declare plan/admission, not output-only records")
        if n == 0:
            if value is not None or metric.get("verdict") == "satisfied":
                issues.append(f"{label}: n=0 is N/A, not zero or satisfied")
            continue
        unit = metric.get("unit")
        if unit not in ("ratio", "percent"):
            issues.append(f"{label}: ratio metric unit must be ratio or percent (not elapsed time)")
            continue
        computed = numerator / n * (100 if unit == "percent" else 1)
        if not number(value) or not math.isclose(value, computed, rel_tol=1e-9, abs_tol=1e-9):
            issues.append(f"{label}: value does not equal numerator/n in declared unit")
    for missing in sorted(set(expected) - seen):
        issues.append(f"{missing}: selected metric missing; retain an unmeasured row with reason")
    manual.append("Denominator provenance, cohort eligibility, truth independence and criterion applicability are not verified")


def check_inventory(summary, issues, manual):
    initial_issue_count = len(issues)
    inventory = summary.get("check_inventory")
    if not isinstance(inventory, dict):
        issues.append("check_inventory: required for requested inventory check")
        return None
    expected = id_list(inventory.get("expected_unit_ids"), "expected_unit_ids", issues)
    if not text(inventory.get("source_ref")):
        issues.append("check_inventory: expected inventory needs source_ref")
    if "all_checks_passed" in inventory and type(inventory["all_checks_passed"]) is not bool:
        issues.append("check_inventory.all_checks_passed: require a boolean declaration")
    rows = inventory.get("observations")
    if not isinstance(rows, list):
        issues.append("check_inventory.observations: require an array")
        rows = []
    seen, counts = set(), dict.fromkeys(STATUSES, 0)
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not text(row.get("unit_id")) or row.get("status") not in STATUSES:
            issues.append(f"observations[{index}]: require unit_id and normalized status")
            continue
        unit_id = row["unit_id"]
        if unit_id in seen:
            issues.append(f"{unit_id}: duplicate observation; normalize versions before checking")
        seen.add(unit_id)
        counts[row["status"]] += 1
        if unit_id not in expected:
            issues.append(f"{unit_id}: observed unit outside expected inventory")
        if row["status"] == "NOT_APPLICABLE" and not text(row.get("reason")):
            issues.append(f"{unit_id}: NOT_APPLICABLE requires a reason; it is not PASS")
    missing = sorted(set(expected) - seen)
    for unit_id in missing:
        issues.append(f"{unit_id}: expected output missing (not removed from inventory)")
    all_pass = (bool(expected) and len(issues) == initial_issue_count and not missing
                and len(rows) == len(expected) and counts["PASS"] == len(expected))
    if inventory.get("all_checks_passed") is True and not all_pass:
        issues.append("all_checks_passed: declaration conflicts with inventory or observed statuses")
    manual.append("PASS/UNKNOWN/N/A labels are candidate outputs, not correctness labels; compare with independent expectations separately")
    return {"expected_count": len(expected), "status_counts": counts,
            "missing_unit_ids": missing, "all_expected_outputs_pass": all_pass}


def check_reanalysis(summary, issues, manual):
    lineage = summary.get("analysis_lineage")
    if not isinstance(lineage, dict):
        issues.append("analysis_lineage: required for requested reanalysis check")
        return
    for key in ("run_id", "run_status", "subject_ref", "raw_artifact_ref", "change_reason"):
        if not text(lineage.get(key)):
            issues.append(f"analysis_lineage.{key}: missing")
    for key in ("subject_sha256", "raw_artifact_sha256"):
        if not isinstance(lineage.get(key), str) or not re.fullmatch(r"[0-9a-fA-F]{64}", lineage[key]):
            issues.append(f"analysis_lineage.{key}: require a SHA-256 hex digest")
    versions = []
    for key in ("original", "current"):
        entry = lineage.get(key)
        if not isinstance(entry, dict):
            issues.append(f"analysis_lineage.{key}: missing original/current analysis")
            entry = {}
        for field in ("analysis_ref", "analysis_version", "recorded_status"):
            if not text(entry.get(field)):
                issues.append(f"analysis_lineage.{key}.{field}: missing")
        versions.append(entry)
    original, current = versions
    if original.get("analysis_ref") == current.get("analysis_ref"):
        issues.append("analysis_lineage: preserve distinct original and current analysis references")
    if original.get("analysis_version") == current.get("analysis_version"):
        issues.append("analysis_lineage: changed analysis requires a new version")
    manual.append("Hashes/references are recorded only, not fetched or authenticated; verify original retention and run status against raw artifacts")


def inspect_report(report, checks=("metrics",)):
    if not isinstance(report, dict) or not isinstance(report.get("selfcheck"), dict):
        raise ValueError("Require a selfcheck object")
    if not checks or any(check not in CHECKS for check in checks):
        raise ValueError("Unknown or empty checks")
    issues, manual, inventory = [], [], None
    summary = report["selfcheck"]
    for check in dict.fromkeys(checks):
        if check == "metrics":
            check_metrics(summary, issues, manual)
        elif check == "inventory":
            inventory = check_inventory(summary, issues, manual)
        else:
            check_reanalysis(summary, issues, manual)
    return {"schema_version": "selfcheck-consistency/0.1.0",
            "checks_requested": list(dict.fromkeys(checks)),
            "checks_not_requested": [check for check in CHECKS if check not in checks],
            "consistency_ok": not issues, "issues": issues, "inventory": inventory,
            "manual_review": manual, "business_verdict": "not_evaluated",
            "notice": "Only declared report consistency; no evidence authentication, safety proof or business acceptance"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--checks", nargs="+", choices=CHECKS, default=["metrics"])
    args = parser.parse_args()
    try:
        if args.report.stat().st_size > 2 * 1024 * 1024:
            raise ValueError("Summary exceeds 2 MiB")
        result = inspect_report(json.loads(args.report.read_text(encoding="utf-8-sig")), args.checks)
    except (OSError, ValueError, OverflowError) as error:
        print(json.dumps({"input_error": type(error).__name__, "business_verdict": "not_evaluated"}))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["consistency_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
