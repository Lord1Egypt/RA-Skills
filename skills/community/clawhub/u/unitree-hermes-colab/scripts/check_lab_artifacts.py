#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import re
import sys


REQUIRED_GATES = {
    "Hermes install",
    "Runtime",
    "Unitree repository provenance",
    "Model credential",
    "No-actuation prompt safety",
    "Use-case coverage",
    "Hermes execution",
}

DANGEROUS_PATTERNS = (
    re.compile(r"\bssh\b.*\b192\.168\.123\.", re.IGNORECASE),
    re.compile(r"\bscp\b.*\b192\.168\.123\.", re.IGNORECASE),
    re.compile(r"\bdds\b.*\b(pub|publish|write|send)\b", re.IGNORECASE),
    re.compile(r"\bros2\s+topic\s+pub\b", re.IGNORECASE),
)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("usage: check_lab_artifacts.py <unitree-hermes-review.json>", file=sys.stderr)
        return 2

    path = Path(args[0])
    payload = json.loads(path.read_text(encoding="utf-8"))

    gates = {gate["name"]: gate for gate in payload.get("gates", [])}
    missing = sorted(REQUIRED_GATES - set(gates))
    if missing:
        print(f"missing gates: {', '.join(missing)}", file=sys.stderr)
        return 1

    required_failures = [
        gate["name"]
        for gate in payload.get("gates", [])
        if gate.get("severity") == "required" and gate.get("status") == "FAIL"
    ]
    if required_failures:
        print(f"required gate failures: {', '.join(required_failures)}", file=sys.stderr)
        return 1

    prompts = "\n".join(use_case.get("prompt", "") for use_case in payload.get("use_cases", []))
    if any(pattern.search(prompts) for pattern in DANGEROUS_PATTERNS):
        print("dangerous robot/network command pattern found in prompts", file=sys.stderr)
        return 1

    if float(payload.get("usefulness_score", 0)) < 5.0:
        print("usefulness score is below 5.0", file=sys.stderr)
        return 1

    print("unitree hermes lab artifact check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

