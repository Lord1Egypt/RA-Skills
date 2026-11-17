#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run all weekend-pick-one release gates.")
    parser.add_argument("--agent-output-dir", type=Path, required=True)
    parser.add_argument("--live-evidence", type=Path, required=True)
    return parser.parse_args()


def run(name: str, command: list[str]) -> dict:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return {
        "name": name,
        "passed": completed.returncode == 0,
        "command": command,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def main() -> None:
    args = parse_args()
    python = sys.executable
    checks = [
        run("fixture_contract", [python, "scripts/run_forward_tests.py"]),
        run("structure", [python, "scripts/validate_escape_skill.py"]),
        run("independent_agent", [python, "scripts/evaluate_agent_outputs.py", "--outputs-dir", str(args.agent_output_dir)]),
        run("live_browser", [python, "scripts/validate_live_evidence.py", str(args.live_evidence)]),
    ]
    passed = all(check["passed"] for check in checks)
    print(json.dumps({"suite_type": "release_gates", "passed": passed, "checks": checks}, ensure_ascii=False, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
