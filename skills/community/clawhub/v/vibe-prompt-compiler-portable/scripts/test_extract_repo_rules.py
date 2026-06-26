#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "extract_repo_rules.py"
FIXTURES = ROOT.parent / "tests" / "repo_extract_cases.json"


def load_cases() -> list[dict]:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


def run_case(repo_root: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--repo-root", repo_root],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def contains_all(items: list[str], required: list[str]) -> bool:
    return all(item in items for item in required)


def main():
    failed = 0
    for case in load_cases():
        result = run_case(case["repo_root"])
        checks = case["checks"]
        ok = True
        for key in ["must_rules_contains", "must_not_rules_contains", "validation_rules_contains", "scope_guardrails_contains"]:
            source_key = key.replace("_contains", "")
            if not contains_all(result.get(source_key, []), checks.get(key, [])):
                ok = False
        print(f"{'OK' if ok else 'FAIL'} | {case['name']}")
        if not ok:
            failed += 1
            print(json.dumps({"checks": checks, "result": result}, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
