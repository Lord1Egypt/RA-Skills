#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WenYan - Regression Test Framework

Commands:
  regression                Run all tests in tests/*.test.json
  score                     Read stdin, score
  drift        {style_id}  Read stdin, check drift
  baseline     {style_id}  Create baseline
  check-baseline {style_id} Compare with baseline
"""

import json
import os
import sys
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
TESTS_DIR = os.path.join(SKILL_DIR, "tests")
ASSETS_DIR = os.path.join(SKILL_DIR, "assets")

sys.path.insert(0, SCRIPT_DIR)
from style_engine import (
    load_style,
    validate_text,
    score_text,
    check_style_drift,
    count_chinese_chars,
)


def load_tests(style_id=None):
    cases = []
    if not os.path.exists(TESTS_DIR):
        return cases
    for fname in sorted(os.listdir(TESTS_DIR)):
        if not fname.endswith(".test.json"):
            continue
        if style_id and not fname.startswith(style_id):
            continue
        path = os.path.join(TESTS_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for case in data.get("cases", []):
            case["_file"] = fname
            cases.append(case)
    return cases


def run_single_test(case):
    result = {
        "name": case.get("name", "unnamed"),
        "input": case.get("input", ""),
        "style": case.get("style", ""),
        "intensity": case.get("intensity", 2),
        "checks": {},
        "pass": True,
        "errors": [],
    }

    if "expected_output" in case:
        score_result = score_text(case["expected_output"], case["style"])
        result["checks"]["score"] = score_result

        min_score = case.get("min_score", 70)
        if score_result["score"] < min_score:
            result["pass"] = False
            result["errors"].append(
                "Score too low: " + str(score_result["score"]) + " < " + str(min_score)
            )

        if "expect_contains" in case:
            for keyword in case["expect_contains"]:
                if keyword not in case["expected_output"]:
                    result["pass"] = False
                    result["errors"].append("Missing keyword: " + keyword)

        if "expect_not_contains" in case:
            for keyword in case["expect_not_contains"]:
                if keyword in case["expected_output"]:
                    result["pass"] = False
                    result["errors"].append("Contains forbidden word: " + keyword)

        max_len = case.get("max_length_per_sentence")
        if max_len:
            sentences = case["expected_output"].split("\u3002")
            for i, sent in enumerate(sentences):
                sent = sent.strip()
                if not sent:
                    continue
                chinese_len = count_chinese_chars(sent)
                if chinese_len > max_len:
                    result["pass"] = False
                    result["errors"].append(
                        "Sentence " + str(i+1) + " too long: " + str(chinese_len) + " > " + str(max_len)
                    )
    else:
        result["checks"]["note"] = "No expected output, case recorded only"

    return result


def run_regression(style_id=None):
    cases = load_tests(style_id)
    if not cases:
        return {"total": 0, "passed": 0, "failed": 0, "results": [], "summary": "No test cases"}

    results = []
    passed = 0
    failed = 0

    for case in cases:
        r = run_single_test(case)
        results.append(r)
        if r["pass"]:
            passed += 1
        else:
            failed += 1

    return {
        "total": len(cases),
        "passed": passed,
        "failed": failed,
        "pass_rate": "{:.1%}".format(passed / len(cases)),
        "results": results,
    }


def save_baseline(style_id, data):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, style_id + ".baseline.json")
    data["_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Baseline saved: " + path)


def load_baseline(style_id):
    path = os.path.join(ASSETS_DIR, style_id + ".baseline.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def check_baseline(style_id, current):
    baseline = load_baseline(style_id)
    if baseline is None:
        return {"changed": True, "reason": "No baseline, first run"}

    changes = []
    if current.get("score", 0) < baseline.get("score", 0) - 5:
        changes.append("Score dropped: " + str(baseline.get("score", 0)) + " -> " + str(current.get("score", 0)))

    if current.get("modern_ratio", 0) > baseline.get("modern_ratio", 0) + 0.02:
        changes.append(
            "Modern ratio increased: " + "{:.1%}".format(baseline.get("modern_ratio", 0)) +
            " -> " + "{:.1%}".format(current.get("modern_ratio", 0))
        )

    return {
        "changed": len(changes) > 0,
        "changes": changes,
        "baseline_time": baseline.get("_timestamp", "unknown"),
    }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "regression":
        style_id = sys.argv[2] if len(sys.argv) > 2 else None
        result = run_regression(style_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "score":
        text = sys.stdin.read()
        style_id = sys.argv[2] if len(sys.argv) > 2 else "ruya"
        result = score_text(text, style_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "drift":
        style_id = sys.argv[2] if len(sys.argv) > 2 else "ruya"
        text = sys.stdin.read()
        style = load_style(style_id)
        drift = check_style_drift(text, style)
        print(json.dumps({"drift_issues": drift}, ensure_ascii=False, indent=2))

    elif cmd == "baseline":
        style_id = sys.argv[2] if len(sys.argv) > 2 else "ruya"
        text = sys.stdin.read()
        result = score_text(text, style_id)
        save_baseline(style_id, result)

    elif cmd == "check-baseline":
        style_id = sys.argv[2] if len(sys.argv) > 2 else "ruya"
        text = sys.stdin.read()
        current = score_text(text, style_id)
        comparison = check_baseline(style_id, current)
        print(json.dumps(comparison, ensure_ascii=False, indent=2))

    else:
        print("Unknown command: " + cmd, file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
