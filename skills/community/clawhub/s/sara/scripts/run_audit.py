from __future__ import annotations

import json
import sys
from pathlib import Path


def find_project_root(start: Path) -> Path:
    """
    Search upward for a folder that contains sara_core/engine.py.
    Falls back to the previous fixed structure if not found.
    """
    current = start.parent
    for candidate in [current, *current.parents]:
        if (candidate / "sara_core" / "engine.py").exists():
            return candidate

    # Fallback to original expected layout
    return start.resolve().parents[2]


ROOT = find_project_root(Path(__file__).resolve())
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from sara_core.engine import SaraAuditor  # noqa: E402


def extract_tools(payload: dict) -> list[str]:
    if "tools" in payload and isinstance(payload["tools"], list):
        return [str(x) for x in payload["tools"]]

    if "steps" in payload and isinstance(payload["steps"], list):
        tools: list[str] = []
        for step in payload["steps"]:
            if isinstance(step, str):
                tools.append(step)
            elif isinstance(step, dict):
                name = step.get("name") or step.get("tool") or step.get("skill")
                if name:
                    tools.append(str(name))
            else:
                continue
        return tools

    return []


def main() -> None:
    raw = sys.stdin.read().strip()

    if not raw:
        print(
            json.dumps(
                {
                    "is_safe": True,
                    "risk_level": "low",
                    "warnings": [],
                    "violations": [],
                    "normalized_tools": [],
                    "suggested_order": None,
                    "note": "No input received.",
                },
                ensure_ascii=False,
            )
        )
        return

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(
            json.dumps(
                {
                    "is_safe": False,
                    "risk_level": "high",
                    "warnings": [f"Invalid JSON input: {exc}"],
                    "violations": [
                        {
                            "type": "input_error",
                            "severity": "high",
                            "message": "Sara could not parse the proposed tool plan.",
                        }
                    ],
                    "normalized_tools": [],
                    "suggested_order": None,
                },
                ensure_ascii=False,
            )
        )
        return

    proposed_tools = extract_tools(payload)

    auditor = SaraAuditor()
    result = auditor.audit_trajectory(proposed_tools)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
