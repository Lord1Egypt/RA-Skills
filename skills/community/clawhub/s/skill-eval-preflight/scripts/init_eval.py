#!/usr/bin/env python3
"""Initialize eval scaffolding for an OpenClaw skill."""

from __future__ import annotations

import argparse
from pathlib import Path


EVALS_JSON_TEMPLATE = """[
  {{
    "id": "core-happy-path",
    "prompt": "[TODO: Add a realistic user request that should trigger {skill_name}]",
    "expected_artifacts": [
      "[TODO: Describe the main output, file, or behavior you expect]"
    ],
    "files": []
  }}
]
"""

TRIGGERS_JSON_TEMPLATE = """{{
  "should_trigger": [
    {{
      "id": "positive-basic",
      "prompt": "[TODO: Add a request that should clearly trigger {skill_name}]"
    }}
  ],
  "should_not_trigger": [
    {{
      "id": "negative-basic",
      "prompt": "[TODO: Add a request that should not trigger {skill_name}]"
    }}
  ]
}}
"""

README_TEMPLATE = """# Skill Eval Notes for {skill_title}

This folder is used by the `skill-eval` workflow.

Files:
- `evals.json`: realistic user requests for forward-testing the skill
- `triggers.json`: positive and negative trigger checks for the skill description

Before the first eval run:
1. Replace all `[TODO: ...]` placeholders.
2. Add at least one realistic eval case to `evals.json`.
3. Add at least one positive and one negative trigger case to `triggers.json`.
4. Make sure `SKILL.md` has a real `description` with concrete trigger scenarios.

Recommended commands:
- `python3 ~/.openclaw/skills/skill-eval/scripts/check_eval_readiness.py {skill_dir}`
- `python3 ~/.openclaw/skills/skill-eval/scripts/run_eval.py {skill_dir}`
"""


def title_case(name: str) -> str:
    return " ".join(part.capitalize() for part in name.split("-"))


def ensure_skill_dir(skill_dir: Path) -> str:
    if not skill_dir.is_dir():
        raise SystemExit(f"Error: skill directory not found: {skill_dir}")
    if not (skill_dir / "SKILL.md").is_file():
        raise SystemExit(f"Error: SKILL.md not found in {skill_dir}")
    return skill_dir.name


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return f"kept {path.name}"
    path.write_text(content)
    return f"created {path.name}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize eval files for a skill.")
    parser.add_argument("skill_dir", help="Path to the target skill directory")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    skill_name = ensure_skill_dir(skill_dir)
    evals_dir = skill_dir / "evals"
    evals_dir.mkdir(exist_ok=True)

    results = [
        write_if_missing(
            evals_dir / "evals.json",
            EVALS_JSON_TEMPLATE.format(skill_name=skill_name),
        ),
        write_if_missing(
            evals_dir / "triggers.json",
            TRIGGERS_JSON_TEMPLATE.format(skill_name=skill_name),
        ),
        write_if_missing(
            evals_dir / "README.md",
            README_TEMPLATE.format(skill_title=title_case(skill_name), skill_dir=skill_dir),
        ),
    ]

    for line in results:
        print(line)
    print(f"eval scaffold ready at {evals_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
