#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT.parent / "tests" / "rulesets.json"


def load_cases() -> list[dict]:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


def run_script(script_name: str, args: list[str]) -> dict:
    script_path = ROOT / script_name
    result = subprocess.run(
        [sys.executable, str(script_path), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def contains_all(items: list[str], required: list[str]) -> bool:
    return all(item in items for item in required)


def text_contains_all(text: str, required: list[str]) -> bool:
    return all(item in text for item in required)


def main():
    failed = 0
    for case in load_cases():
        result = run_script(case["script"], case["args"])
        checks = case["checks"]
        ok = True

        if result.get("ruleset") != checks["ruleset"]:
            ok = False
        for key in ["must_rules_contains", "must_not_rules_contains", "validation_rules_contains", "scope_guardrails_contains"]:
            if key in checks:
                source_key = key.replace("_contains", "")
                if not contains_all(result.get(source_key, []), checks[key]):
                    ok = False
        if "handoff_text_contains" in checks and not text_contains_all(result.get("handoff_text", ""), checks["handoff_text_contains"]):
            ok = False

        print(f"{'OK' if ok else 'FAIL'} | {case['name']}")
        if not ok:
            failed += 1
            print(json.dumps({"checks": checks, "result": result}, ensure_ascii=False, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
