#!/usr/bin/env python3
import re
import sys
from pathlib import Path

TEMPLATES = {
    "investigation": """Objective: {task}\n\nMode: Investigation only\nScope: {scope}\n\nInstructions:\n- Inspect only the files and modules relevant to this scope.\n- Trace behavior, dependencies, and likely fix points.\n- Do not modify files.\n- Keep the result concise and structured.\n\nReturn format:\n- Findings\n- Touched files\n- Risks or unknowns\n- Recommended next step\n""",
    "implementation": """Objective: {task}\n\nMode: Bounded implementation\nScope: {scope}\nVerification: {verification}\n\nInstructions:\n- Implement only the agreed change within scope.\n- Avoid unrelated refactors.\n- Keep the patch minimal and reversible.\n- Run the stated verification after editing.\n\nReturn format:\n- What changed\n- Touched files\n- Verification result\n- Remaining risks\n""",
    "test": """Objective: {task}\n\nMode: Test work\nScope: {scope}\nVerification target: {verification}\n\nInstructions:\n- Add or repair focused tests for the target behavior only.\n- Do not refactor unrelated tests.\n- Prefer the smallest test that proves the behavior.\n- Run the verification target after changes.\n\nReturn format:\n- Added or changed tests\n- Touched files\n- Verification result\n- Remaining gaps\n""",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "task"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: generate_subagent_brief.py <task-name> [scope] [verification] [base-dir]", file=sys.stderr)
        return 1

    task = sys.argv[1]
    scope = sys.argv[2] if len(sys.argv) > 2 else "relevant files and modules for this task"
    verification = sys.argv[3] if len(sys.argv) > 3 else "smallest meaningful verification command"
    base_dir = Path(sys.argv[4]) if len(sys.argv) > 4 else Path.cwd()

    out_dir = base_dir / "notes" / slugify(task) / "subagents"
    out_dir.mkdir(parents=True, exist_ok=True)

    for kind, template in TEMPLATES.items():
        path = out_dir / f"{kind}.brief.md"
        path.write_text(template.format(task=task, scope=scope, verification=verification), encoding="utf-8")
        print(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
