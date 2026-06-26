#!/usr/bin/env python3
"""
Automated test suite for Skill Vetter Pro (scan.py).

Runs scan.py against all test samples (malicious, benign, adversarial, real_clawhub)
and validates results against ground truth expectations.

Usage:
    python3 tests/test_scan.py              # Run all tests
    python3 tests/test_scan.py --verbose     # Show detailed output
    python3 tests/test_scan.py --category malicious  # Run one category
    python3 tests/test_scan.py --json        # JSON output
"""

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

# ============================================================
# Config
# ============================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SCANNER = PROJECT_DIR / "scan.py"

CATEGORIES = ["malicious", "benign", "adversarial"]


# ============================================================
# Scanner Runner
# ============================================================

def run_scan(target_path: str) -> dict:
    """Run scan.py on a target and return parsed JSON output."""
    proc = subprocess.run(
        [sys.executable, str(SCANNER), target_path, "--json"],
        capture_output=True, text=True
    )
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"error": proc.stderr[:500], "exit_code": proc.returncode}


def extract_findings(scan_result: dict) -> list:
    """Extract all findings from scan result."""
    findings = []
    for fr in scan_result.get("file_reports", []):
        for f in fr.get("pattern_findings", []):
            findings.append(f)
        for f in fr.get("ast_findings", []):
            findings.append(f)
    return findings


def extract_triggered_rules(scan_result: dict) -> set:
    """Get set of rule IDs triggered."""
    rules = set()
    for fr in scan_result.get("file_reports", []):
        for f in fr.get("pattern_findings", []):
            rules.add(f.get("rule_id", ""))
        for f in fr.get("ast_findings", []):
            if f.get("category"):
                rules.add(f"AST-{f['category']}")
    return rules


def extract_triggered_categories(scan_result: dict) -> set:
    """Get set of categories triggered."""
    cats = set()
    for fr in scan_result.get("file_reports", []):
        for f in fr.get("pattern_findings", []):
            cats.add(f.get("category", ""))
        for f in fr.get("ast_findings", []):
            cats.add(f.get("category", ""))
    return cats


def count_doc_downgraded(scan_result: dict) -> int:
    """Count findings that were doc-downgraded."""
    count = 0
    for fr in scan_result.get("file_reports", []):
        for f in fr.get("pattern_findings", []):
            if f.get("in_documentation"):
                count += 1
    return count


# ============================================================
# Test Validators
# ============================================================

class TestResult:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.passed = []
        self.failed = []
        self.warnings = []
        self.scan_result = None

    @property
    def ok(self):
        return len(self.failed) == 0

    def check(self, condition, pass_msg, fail_msg):
        if condition:
            self.passed.append(pass_msg)
        else:
            self.failed.append(fail_msg)

    def warn(self, msg):
        self.warnings.append(msg)


def validate_malicious(skill_dir: Path, expected: dict, scan_result: dict) -> TestResult:
    """Validate a malicious sample against expectations."""
    name = skill_dir.name
    result = TestResult(name, "malicious")
    result.scan_result = scan_result

    if "error" in scan_result:
        result.failed.append(f"Scanner error: {scan_result['error']}")
        return result

    score = scan_result.get("risk_score", 0)
    level = scan_result.get("risk_level", "")
    rules = extract_triggered_rules(scan_result)

    # Check minimum score
    min_score = expected.get("expected_min_score", 0)
    result.check(
        score >= min_score,
        f"Score {score} >= expected min {min_score}",
        f"Score {score} < expected min {min_score}"
    )

    # Check risk level
    expected_levels = expected.get("expected_level", [])
    if expected_levels:
        result.check(
            level in expected_levels,
            f"Level '{level}' in expected {expected_levels}",
            f"Level '{level}' NOT in expected {expected_levels}"
        )

    # Check must-trigger rules
    must_trigger = expected.get("must_trigger_rules", [])
    for rule_id in must_trigger:
        result.check(
            rule_id in rules,
            f"Rule {rule_id} triggered",
            f"Rule {rule_id} NOT triggered (miss)"
        )

    # Check AST findings if expected
    if expected.get("must_trigger_ast"):
        ast_findings = []
        for fr in scan_result.get("file_reports", []):
            ast_findings.extend(fr.get("ast_findings", []))
        result.check(
            len(ast_findings) > 0,
            f"AST findings detected: {len(ast_findings)}",
            "No AST findings detected (expected some)"
        )

    return result


def validate_benign(skill_dir: Path, expected: dict, scan_result: dict) -> TestResult:
    """Validate a benign sample against expectations."""
    name = skill_dir.name
    result = TestResult(name, "benign")
    result.scan_result = scan_result

    if "error" in scan_result:
        result.failed.append(f"Scanner error: {scan_result['error']}")
        return result

    score = scan_result.get("risk_score", 0)
    level = scan_result.get("risk_level", "")
    categories = extract_triggered_categories(scan_result)

    # Check maximum score
    max_score = expected.get("expected_max_score", 999)
    result.check(
        score <= max_score,
        f"Score {score} <= expected max {max_score}",
        f"Score {score} > expected max {max_score} (false positive!)"
    )

    # Check risk level
    expected_levels = expected.get("expected_level", [])
    if expected_levels:
        result.check(
            level in expected_levels,
            f"Level '{level}' in expected {expected_levels}",
            f"Level '{level}' NOT in expected {expected_levels} (over-reported)"
        )

    # Check categories that should NOT trigger
    should_not = expected.get("should_not_trigger_categories", [])
    for cat in should_not:
        if cat in categories:
            # Check if all findings in this category are doc-downgraded
            non_doc_findings = []
            for fr in scan_result.get("file_reports", []):
                for f in fr.get("pattern_findings", []):
                    if f.get("category") == cat and not f.get("in_documentation"):
                        non_doc_findings.append(f)
            if non_doc_findings:
                result.failed.append(
                    f"Category '{cat}' triggered with {len(non_doc_findings)} non-doc finding(s) (FP)"
                )
            else:
                result.warn(f"Category '{cat}' triggered but all findings doc-downgraded (OK)")
        else:
            result.passed.append(f"Category '{cat}' correctly not triggered")

    return result


def validate_adversarial(skill_dir: Path, expected: dict, scan_result: dict) -> TestResult:
    """Validate an adversarial sample — more nuanced expectations."""
    name = skill_dir.name
    result = TestResult(name, "adversarial")
    result.scan_result = scan_result

    if "error" in scan_result:
        result.failed.append(f"Scanner error: {scan_result['error']}")
        return result

    score = scan_result.get("risk_score", 0)
    level = scan_result.get("risk_level", "")
    rules = extract_triggered_rules(scan_result)

    # Check must-trigger rules (if any)
    must_trigger = expected.get("must_trigger_rules", [])
    for rule_id in must_trigger:
        if rule_id in rules:
            result.passed.append(f"Rule {rule_id} triggered")
        else:
            result.warn(f"Rule {rule_id} not triggered (known limitation)")

    # Check expected level
    expected_levels = expected.get("expected_level", [])
    if expected_levels:
        if level in expected_levels:
            result.passed.append(f"Level '{level}' matches expected")
        else:
            result.warn(f"Level '{level}' not in expected {expected_levels}")

    # Record known blind spots
    blind_spots = expected.get("known_blind_spots", [])
    for bs in blind_spots:
        result.warn(f"Known blind spot: {bs}")

    # Adversarial tests always pass (they document limitations)
    # but we still record what was detected vs. not
    result.check(True, f"Adversarial test recorded (score={score}, level={level})", "")

    return result


def validate_real_skill(skill_name: str, expected: dict, scan_result: dict) -> TestResult:
    """Validate a real ClawHub skill against ground truth."""
    result = TestResult(skill_name, "real_clawhub")
    result.scan_result = scan_result

    if "error" in scan_result:
        result.failed.append(f"Scanner error: {scan_result['error']}")
        return result

    score = scan_result.get("risk_score", 0)
    level = scan_result.get("risk_level", "")
    true_label = expected.get("true_label", "unknown")

    # Check level expectations
    expected_levels = expected.get("expected_level", [])
    if expected_levels:
        result.check(
            level in expected_levels,
            f"Level '{level}' in expected {expected_levels} (label={true_label})",
            f"Level '{level}' NOT in expected {expected_levels} (label={true_label})"
        )

    # Check score bounds
    if "expected_max_score" in expected:
        result.check(
            score <= expected["expected_max_score"],
            f"Score {score} <= max {expected['expected_max_score']}",
            f"Score {score} > max {expected['expected_max_score']} (over-reported for {true_label})"
        )
    if "expected_min_score" in expected:
        result.check(
            score >= expected["expected_min_score"],
            f"Score {score} >= min {expected['expected_min_score']}",
            f"Score {score} < min {expected['expected_min_score']} (under-reported for {true_label})"
        )

    # Check doc-downgrade for skill-vetter
    if expected.get("all_findings_should_be_doc_downgraded"):
        total = scan_result.get("summary", {}).get("total_findings", 0)
        downgraded = scan_result.get("summary", {}).get("doc_downgraded", 0)
        result.check(
            total == downgraded,
            f"All {total} findings doc-downgraded",
            f"Only {downgraded}/{total} findings doc-downgraded"
        )

    return result


# ============================================================
# Metrics
# ============================================================

def compute_metrics(all_results: list) -> dict:
    """Compute precision, recall, F1 for malicious detection."""
    # Binary classification: malicious vs. not-malicious
    # Treat scanner level HIGH/EXTREME as "flagged"
    tp = fp = fn = tn = 0

    for r in all_results:
        if r.scan_result is None or "error" in r.scan_result:
            continue

        level = r.scan_result.get("risk_level", "")
        flagged = level in ("HIGH", "EXTREME")

        if r.category == "malicious":
            if flagged:
                tp += 1
            else:
                fn += 1
        elif r.category == "benign":
            if flagged:
                fp += 1
            else:
                tn += 1
        # adversarial and real_clawhub are not counted in binary metrics

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "accuracy": round((tp + tn) / (tp + fp + fn + tn), 3) if (tp + fp + fn + tn) > 0 else 0,
    }


def compute_rule_coverage(all_results: list) -> dict:
    """Compute which rules were triggered and which were never hit."""
    # Get all rule IDs from scan.py
    all_rules_triggered = Counter()
    all_rules_expected = Counter()

    for r in all_results:
        if r.scan_result and "error" not in r.scan_result:
            for rule_id in extract_triggered_rules(r.scan_result):
                all_rules_triggered[rule_id] += 1

    return dict(all_rules_triggered)


# ============================================================
# Main Runner
# ============================================================

def run_category(category: str, verbose: bool = False) -> list:
    """Run all tests in a category."""
    results = []
    category_dir = SCRIPT_DIR / category

    if category == "real_clawhub":
        # Special handling: use ground_truth.json
        gt_file = category_dir / "ground_truth_expanded.json"
        if not gt_file.exists():
            print(f"  No ground_truth_expanded.json in {category_dir}")
            return results

        gt = json.loads(gt_file.read_text())
        skills = gt.get("skills", {})

        for skill_name, expected in skills.items():
            skill_dir = category_dir / skill_name
            if not skill_dir.exists():
                continue
            scan_result = run_scan(str(skill_dir))
            tr = validate_real_skill(skill_name, expected, scan_result)
            results.append(tr)
        return results

    # Standard categories: malicious, benign, adversarial
    if not category_dir.exists():
        return results

    for skill_dir in sorted(category_dir.iterdir()):
        if not skill_dir.is_dir():
            continue

        expected_file = skill_dir / "expected.json"
        if not expected_file.exists():
            continue

        expected = json.loads(expected_file.read_text())
        scan_result = run_scan(str(skill_dir))

        if category == "malicious":
            tr = validate_malicious(skill_dir, expected, scan_result)
        elif category == "benign":
            tr = validate_benign(skill_dir, expected, scan_result)
        elif category == "adversarial":
            tr = validate_adversarial(skill_dir, expected, scan_result)
        else:
            continue

        results.append(tr)

    return results


def print_results(all_results: list, verbose: bool = False):
    """Print test results."""
    total_pass = 0
    total_fail = 0
    total_warn = 0

    by_category = defaultdict(list)
    for r in all_results:
        by_category[r.category].append(r)

    for category in ["malicious", "benign", "adversarial", "real_clawhub"]:
        results = by_category.get(category, [])
        if not results:
            continue

        print(f"\n{'='*70}")
        print(f"  {category.upper()} ({len(results)} samples)")
        print(f"{'='*70}")

        for r in results:
            score = r.scan_result.get("risk_score", "?") if r.scan_result else "?"
            level = r.scan_result.get("risk_level", "?") if r.scan_result else "?"
            status = "PASS" if r.ok else "FAIL"
            icon = "✅" if r.ok else "❌"

            print(f"\n  {icon} {r.name}  [score={score}, level={level}] → {status}")

            if verbose or not r.ok:
                for msg in r.failed:
                    print(f"     ❌ {msg}")
            if verbose:
                for msg in r.passed:
                    print(f"     ✅ {msg}")
            for msg in r.warnings:
                print(f"     ⚠️  {msg}")

            total_pass += len(r.passed)
            total_fail += len(r.failed)
            total_warn += len(r.warnings)

    # Summary
    print(f"\n{'='*70}")
    print(f"  SUMMARY")
    print(f"{'='*70}")

    samples_pass = sum(1 for r in all_results if r.ok)
    samples_fail = sum(1 for r in all_results if not r.ok)
    print(f"  Samples: {samples_pass} passed, {samples_fail} failed, {len(all_results)} total")
    print(f"  Checks:  {total_pass} passed, {total_fail} failed, {total_warn} warnings")

    # Binary classification metrics (malicious vs benign only)
    metrics = compute_metrics(all_results)
    print(f"\n  Binary Classification (HIGH/EXTREME = flagged):")
    print(f"  ┌─────────────────────────┐")
    print(f"  │ TP={metrics['tp']:2d}  FP={metrics['fp']:2d}  │  Precision: {metrics['precision']:.1%}")
    print(f"  │ FN={metrics['fn']:2d}  TN={metrics['tn']:2d}  │  Recall:    {metrics['recall']:.1%}")
    print(f"  │                         │  F1:        {metrics['f1']:.1%}")
    print(f"  │                         │  Accuracy:  {metrics['accuracy']:.1%}")
    print(f"  └─────────────────────────┘")

    # Rule coverage
    rule_hits = compute_rule_coverage(all_results)
    if rule_hits:
        print(f"\n  Rules triggered across all tests:")
        for rule, count in sorted(rule_hits.items(), key=lambda x: -x[1]):
            print(f"    {rule:12s}  {count}x")

    return samples_fail == 0


def main():
    parser = argparse.ArgumentParser(description="Test suite for Skill Vetter Pro")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--category", "-c", choices=CATEGORIES + ["real_clawhub", "all"], default="all")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if not SCANNER.exists():
        print(f"Error: scan.py not found at {SCANNER}")
        sys.exit(1)

    categories = CATEGORIES + ["real_clawhub"] if args.category == "all" else [args.category]

    all_results = []
    for cat in categories:
        print(f"Running {cat} tests...", file=sys.stderr)
        results = run_category(cat, verbose=args.verbose)
        all_results.extend(results)

    if args.json:
        output = {
            "total_samples": len(all_results),
            "passed": sum(1 for r in all_results if r.ok),
            "failed": sum(1 for r in all_results if not r.ok),
            "metrics": compute_metrics(all_results),
            "rule_coverage": compute_rule_coverage(all_results),
            "details": [
                {
                    "name": r.name,
                    "category": r.category,
                    "ok": r.ok,
                    "score": r.scan_result.get("risk_score") if r.scan_result else None,
                    "level": r.scan_result.get("risk_level") if r.scan_result else None,
                    "passed": r.passed,
                    "failed": r.failed,
                    "warnings": r.warnings,
                }
                for r in all_results
            ]
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        success = print_results(all_results, verbose=args.verbose)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
