#!/usr/bin/env python3
"""
SPM Session Recovery Report
Analyzes WBS Ledger + Heartbeat Log to generate recovery guidance
Usage: python3 scripts/session-recovery.py [ledger_path]
"""
import os
import re
import sys

LEDGER = sys.argv[1] if len(sys.argv) > 1 else "docs/spm/ledger.md"

if not os.path.exists(LEDGER):
    print("❌ [SPM] WBS Ledger not found")
    sys.exit(1)

with open(LEDGER, encoding="utf-8") as f:
    content = f.read()

lines = content.split("\n")

# Extract Active State
active_state = {}
in_active = False
for line in lines:
    if "## Active State" in line:
        in_active = True
        continue
    if in_active and line.strip().startswith("-"):
        key_val = line.strip().lstrip("- ").split(":", 1)
        if len(key_val) == 2:
            active_state[key_val[0].strip()] = key_val[1].strip()
    elif in_active and line.strip().startswith("#"):
        break

# Extract heartbeat log
heartbeats = []
in_hb = False
for line in lines:
    if "## Heartbeat Log" in line:
        in_hb = True
        continue
    if in_hb:
        if line.strip().startswith("|") and "Time" not in line:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 5:
                heartbeats.append(cells)
        elif heartbeats and not line.strip().startswith("|"):
            break

# Find current doing tasks
doing_tasks = []
in_wbs = False
for line in lines:
    if "## WBS" in line or "| ID | Work Package" in line:
        in_wbs = True
        continue
    if in_wbs:
        if not line.strip().startswith("|"):
            break
        if "doing" in line.lower():
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                doing_tasks.append(cells)

# Generate report
print("")
print("╔══════════════════════════════════════════════════╗")
print("║     SPM Session Recovery Report                  ║")
print("╠══════════════════════════════════════════════════╣")

if active_state:
    current = active_state.get("Current item", "unknown")
    completed = active_state.get("Last completed", "none")
    resume = active_state.get("Resume from here", "")
    print(f"║  Current:  {current}")
    print(f"║  Completed: {completed}")
    if resume:
        print(f"║  Resume:    {resume}")
else:
    print("║  No Active State found in ledger")

if doing_tasks:
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  Active Tasks ({len(doing_tasks)}):")
    for task in doing_tasks[:5]:
        print(f"║    [{task[0]}] {task[1][:40]}")

if heartbeats:
    last_hb = heartbeats[-1]
    print(f"╠══════════════════════════════════════════════════╣")
    print(f"║  Last Heartbeat: {last_hb[0]}")
    print(f"║    Active:    {last_hb[1][:40]}")
    print(f"║    Completed: {last_hb[2][:40]}")
    if len(last_hb) >= 5:
        print(f"║    Resume:    {last_hb[4][:50]}")

print("╚══════════════════════════════════════════════════╝")
print("")

# Recommendation
if doing_tasks:
    print("▶️  Next Step: 继续 Task " + doing_tasks[0][0])
elif active_state:
    resume = active_state.get("Resume from here", "")
    if resume:
        print(f"▶️  Resume: {resume}")
