#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "create_handoff.py"
FIXTURES = ROOT.parent / "tests" / "tool_presets.json"


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



def contains_all(text: str, parts: list[str]) -> bool:
    return all(part in text for part in parts)



def main():
    failed = 0
    for case in load_cases():
        result = run_case(case["args"])
        checks = case["checks"]
        ok = True

        if result.get("target_tool") != checks["target_tool"]:
            ok = False
        if result.get("target_tool_label") != checks["target_tool_label"]:
            ok = False
        if not contains_all(result.get("tool_instruction", ""), checks.get("tool_instruction_contains", [])):
            ok = False
        if not contains_all(result.get("handoff_text", ""), checks.get("handoff_text_contains", [])):
            ok = False

        print(f"{'OK' if ok else 'FAIL'} | {case['name']}")
        if not ok:
            failed += 1
            print(json.dumps({"checks": checks, "result": result}, ensure_ascii=False, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
