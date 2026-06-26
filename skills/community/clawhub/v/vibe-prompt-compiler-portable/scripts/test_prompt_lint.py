#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "prompt_lint.py"
FIXTURES = ROOT.parent / "tests" / "prompt_lint_cases.json"


def load_cases() -> list[dict]:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))



def run_case(args: list[str]) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)



def main():
    failed = 0
    for case in load_cases():
        result = run_case(case["args"])
        checks = case["checks"]
        issue_codes = [item["code"] for item in result.get("issues", [])]
        ok = True

        if result.get("task_type") != checks["task_type"]:
            ok = False
        if "min_issue_count" in checks and len(result.get("issues", [])) < checks["min_issue_count"]:
            ok = False
        if "max_issue_count" in checks and len(result.get("issues", [])) > checks["max_issue_count"]:
            ok = False
        if "issue_codes" in checks and not all(code in issue_codes for code in checks["issue_codes"]):
            ok = False

        print(f"{'OK' if ok else 'FAIL'} | {case['name']}")
        if not ok:
            failed += 1
            print(json.dumps({"checks": checks, "result": result}, ensure_ascii=False, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
