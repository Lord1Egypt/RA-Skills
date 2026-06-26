#!/usr/bin/env python3
import re
import sys
from pathlib import Path

TEMPLATES = {
    'plan.md': """# Goal

# Constraints

# Current Understanding

# Likely Files / Modules
- 

# Steps
1. 
2. 
3. 

# Verification
- 
""",
    'todo.md': """- [ ] Inspect relevant files
- [ ] Confirm approach
- [ ] Make minimal change
- [ ] Verify result
- [ ] Update checkpoint
""",
    'checkpoint.md': """# Status

# What Changed

# Key Decisions

# Open Questions

# Next Step
""",
}


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "task"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: init_task.py <task-name> [base-dir]", file=sys.stderr)
        return 1

    task_name = sys.argv[1]
    base_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    task_dir = base_dir / "notes" / slugify(task_name)
    task_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for name, content in TEMPLATES.items():
        path = task_dir / name
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(path)

    print(f"Task directory: {task_dir}")
    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    else:
        print("No new files created; task notes already existed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
