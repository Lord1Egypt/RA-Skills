#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "compile_prompt.py"
FIXTURES = ROOT.parent / "tests" / "web_cases.json"


def load_cases() -> list[dict]:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


def compile_request(request: str) -> dict:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--request", request, "--output", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)



def main():
    failed = 0
    cases = load_cases()
    for case in cases:
        result = compile_request(case["request"])
        ok = result["task_type"] == case["expected_task"]
        print(
            f"{'OK' if ok else 'FAIL'} | expected={case['expected_task']} got={result['task_type']} | {case['name']}"
        )
        if not ok:
            failed += 1
            print(f"  request: {case['request']}")

    print(f"Checked {len(cases)} realistic routing cases.")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
