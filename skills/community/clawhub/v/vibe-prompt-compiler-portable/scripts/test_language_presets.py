#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT.parent / "tests" / "language_presets.json"


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



def contains_all_text(text: str, parts: list[str]) -> bool:
    return all(part in text for part in parts)



def contains_all_items(items: list[str], parts: list[str]) -> bool:
    return all(part in items for part in parts)



def main():
    failed = 0
    for case in load_cases():
        result = run_script(case["script"], case["args"])
        checks = case["checks"]
        ok = True

        for key in ["language_preset", "task_type", "target_tool", "target_tool_label"]:
            if key in checks and result.get(key) != checks[key]:
                ok = False
        if "compiled_prompt_contains" in checks and not contains_all_text(result.get("compiled_prompt", ""), checks["compiled_prompt_contains"]):
            ok = False
        if "handoff_text_contains" in checks and not contains_all_text(result.get("handoff_text", ""), checks["handoff_text_contains"]):
            ok = False
        if "tool_instruction_contains" in checks and not contains_all_text(result.get("tool_instruction", ""), checks["tool_instruction_contains"]):
            ok = False
        if "assumptions_contains" in checks and not contains_all_items(result.get("assumptions", []), checks["assumptions_contains"]):
            ok = False

        print(f"{'OK' if ok else 'FAIL'} | {case['name']}")
        if not ok:
            failed += 1
            print(json.dumps({"checks": checks, "result": result}, ensure_ascii=False, indent=2))

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
