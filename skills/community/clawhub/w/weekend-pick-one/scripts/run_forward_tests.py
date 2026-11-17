#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from eval_common import evaluate_text


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests" / "forward-cases.json"
OUTPUTS = ROOT / "tests" / "forward-outputs.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    cases = load_json(CASES)
    outputs = load_json(OUTPUTS)
    result = []
    failed = False

    for case in cases:
        output = outputs.get(case["id"], "")
        failures = evaluate_text(case, output)
        failed = failed or bool(failures)
        result.append({
            "id": case["id"],
            "mode": case["mode"],
            "passed": not failures,
            "failures": failures,
        })

    summary = {
        "suite_type": "fixture_contract",
        "proof_boundary": "Checks curated examples only; does not prove live agent behavior.",
        "case_count": len(cases),
        "passed_count": sum(1 for item in result if item["passed"]),
        "failed_count": sum(1 for item in result if not item["passed"]),
        "results": result,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
