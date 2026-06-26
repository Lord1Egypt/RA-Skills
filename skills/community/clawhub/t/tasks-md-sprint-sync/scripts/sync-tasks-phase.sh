#!/usr/bin/env bash
set -euo pipefail

PLAN_FILE="${PLAN_FILE:-PLAN.md}"
TASKS_FILE="${TASKS_FILE:-TASKS.md}"
PROJECT_NAME="${PROJECT_NAME:-}"
SYNC_MODE="${SYNC_MODE:-report}" # report | apply

if [[ -z "$PROJECT_NAME" ]]; then
  echo "[tasks-md-sprint-sync] PROJECT_NAME is required (example: 'ClawHub Skills')" >&2
  exit 1
fi

if [[ ! -f "$PLAN_FILE" ]]; then
  echo "[tasks-md-sprint-sync] PLAN_FILE not found: $PLAN_FILE" >&2
  exit 1
fi

if [[ ! -f "$TASKS_FILE" ]]; then
  echo "[tasks-md-sprint-sync] TASKS_FILE not found: $TASKS_FILE" >&2
  exit 1
fi

if [[ "$SYNC_MODE" != "report" && "$SYNC_MODE" != "apply" ]]; then
  echo "[tasks-md-sprint-sync] SYNC_MODE must be report or apply (got: $SYNC_MODE)" >&2
  exit 1
fi

python3 - "$PLAN_FILE" "$TASKS_FILE" "$PROJECT_NAME" "$SYNC_MODE" <<'PY'
import re
import sys
from pathlib import Path

plan_path = Path(sys.argv[1])
tasks_path = Path(sys.argv[2])
project_name = sys.argv[3]
mode = sys.argv[4]

plan = plan_path.read_text(encoding="utf-8")
tasks = tasks_path.read_text(encoding="utf-8")

phase_header_re = re.compile(r"^##\s+Phase\s+(\d+):\s+(.+?)\s*$", re.MULTILINE)
status_re = re.compile(r"^\*\*Status:\s*(.+?)\*\*\s*$", re.MULTILINE)

current_phase = None
phase_work_items = []

for m in phase_header_re.finditer(plan):
    phase_num = m.group(1)
    phase_name = m.group(2).strip()
    start = m.end()
    next_match = phase_header_re.search(plan, start)
    end = next_match.start() if next_match else len(plan)
    block = plan[start:end]

    status_match = status_re.search(block)
    if not status_match:
        continue
    status = status_match.group(1).strip().upper()
    if "IN PROGRESS" not in status:
        continue

    current_phase = f"Phase {phase_num} — {phase_name}"

    work_section = re.search(r"^###\s+Work\s*$([\s\S]*?)(?:^###\s+|\Z)", block, re.MULTILINE)
    if work_section:
        work_text = work_section.group(1)
        phase_work_items = [
            re.sub(r"\s+", " ", item).strip()
            for item in re.findall(r"^\s*-\s+(.+?)\s*$", work_text, re.MULTILINE)
            if item.strip()
        ]
    break

if not current_phase:
    print("[tasks-md-sprint-sync] No phase marked IN PROGRESS in plan", file=sys.stderr)
    sys.exit(1)

project_heading_re = re.compile(rf"^##\s+{re.escape(project_name)}\s*$", re.MULTILINE)
project_match = project_heading_re.search(tasks)
if not project_match:
    print(f"[tasks-md-sprint-sync] Project section not found in TASKS.md: {project_name}", file=sys.stderr)
    sys.exit(1)

project_start = project_match.start()
next_project = re.search(r"^##\s+.+$", tasks[project_match.end():], re.MULTILINE)
project_end = project_match.end() + next_project.start() if next_project else len(tasks)
project_block = tasks[project_start:project_end]

phase_line_re = re.compile(r"^(\*\*Current phase:\*\*\s*).+$", re.MULTILINE)
if not phase_line_re.search(project_block):
    print(f"[tasks-md-sprint-sync] Current phase line missing in section: {project_name}", file=sys.stderr)
    sys.exit(1)

in_progress_re = re.compile(r"(^###\s+In progress\s*$)([\s\S]*?)(?=^###\s+|\Z)", re.MULTILINE)
in_progress_match = in_progress_re.search(project_block)
if not in_progress_match:
    print(f"[tasks-md-sprint-sync] In progress section missing in section: {project_name}", file=sys.stderr)
    sys.exit(1)

existing_items = [
    re.sub(r"\s+", " ", m).strip()
    for m in re.findall(r"^\s*-\s+\[.\]\s+(.+?)\s*$", in_progress_match.group(2), re.MULTILINE)
]
new_items = [f"- [ ] {item}" for item in phase_work_items]

print(f"[tasks-md-sprint-sync] Project: {project_name}")
print(f"[tasks-md-sprint-sync] Current phase from plan: {current_phase}")
print(f"[tasks-md-sprint-sync] Existing in-progress items: {len(existing_items)}")
print(f"[tasks-md-sprint-sync] Plan work items: {len(phase_work_items)}")

missing = [item for item in phase_work_items if item not in existing_items]
extra = [item for item in existing_items if item not in phase_work_items]

if missing:
    print("[tasks-md-sprint-sync] Missing in TASKS.md (from PLAN.md Work):")
    for item in missing:
        print(f"  + {item}")

if extra:
    print("[tasks-md-sprint-sync] Extra in TASKS.md (not in PLAN.md Work):")
    for item in extra:
        print(f"  - {item}")

if mode == "report":
    if not missing and not extra:
        print("[tasks-md-sprint-sync] In progress already aligned")
    print("[tasks-md-sprint-sync] Report mode complete (no file changes)")
    sys.exit(0)

updated_project = phase_line_re.sub(rf"\1{current_phase}", project_block)
updated_in_progress_match = in_progress_re.search(updated_project)
if not updated_in_progress_match:
    print(f"[tasks-md-sprint-sync] In progress section missing during apply: {project_name}", file=sys.stderr)
    sys.exit(1)

new_in_progress_block = "\n" + ("\n".join(new_items) if new_items else "- [ ] (No work items found in plan phase)") + "\n\n"
updated_project = (
    updated_project[:updated_in_progress_match.start(2)]
    + new_in_progress_block
    + updated_project[updated_in_progress_match.end(2):]
)

updated_tasks = tasks[:project_start] + updated_project + tasks[project_end:]
tasks_path.write_text(updated_tasks, encoding="utf-8")

print("[tasks-md-sprint-sync] Applied phase + In progress sync to TASKS.md")
PY
