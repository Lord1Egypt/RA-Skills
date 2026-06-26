#!/bin/bash
# Check if all phases in task_plan.md are complete
# Always exits 0 — uses stdout for status reporting
# Used by Stop hook to report task completion status

# Support SPF directory by default
if [ -d ".superpower-with-files" ] && [ -f ".superpower-with-files/task_plan.md" ]; then
    DEFAULT_PLAN=".superpower-with-files/task_plan.md"
else
    DEFAULT_PLAN="task_plan.md"
fi

PLAN_FILE="${1:-$DEFAULT_PLAN}"

if [ ! -f "$PLAN_FILE" ]; then
    echo "[spf] No task_plan.md found — no active planning session."
    exit 0
fi

# Count total phases
TOTAL=$(grep -c "### Phase" "$PLAN_FILE" || true)

# Check for **Status:** format first
COMPLETE=$(grep -cF "**Status:** complete" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cF "**Status:** in_progress" "$PLAN_FILE" || true)
PENDING=$(grep -cF "**Status:** pending" "$PLAN_FILE" || true)

# Fallback: check for [complete] inline format if **Status:** not found
if [ "$COMPLETE" -eq 0 ] && [ "$IN_PROGRESS" -eq 0 ] && [ "$PENDING" -eq 0 ]; then
    COMPLETE=$(grep -c "\[complete\]" "$PLAN_FILE" || true)
    IN_PROGRESS=$(grep -c "\[in_progress\]" "$PLAN_FILE" || true)
    PENDING=$(grep -c "\[pending\]" "$PLAN_FILE" || true)
fi

# Default to 0 if empty
: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

# Report status (always exit 0 — incomplete task is a normal state)
if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "[spf] ALL PHASES COMPLETE ($COMPLETE/$TOTAL)"
else
    echo "[spf] Task in progress ($COMPLETE/$TOTAL phases complete)"
    
    # Git Pulse Check
    if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
        RECENT_COMMITS=$(git log --oneline --since="1 hour ago" | wc -l)
        echo "[spf] Git Pulse: $RECENT_COMMITS commit(s) in the last hour."
    fi

    if [ "$IN_PROGRESS" -gt 0 ]; then
        echo "[spf] $IN_PROGRESS phase(s) still in progress."
    fi
    if [ "$PENDING" -gt 0 ]; then
        echo "[spf] $PENDING phase(s) pending."
    fi
fi
exit 0
