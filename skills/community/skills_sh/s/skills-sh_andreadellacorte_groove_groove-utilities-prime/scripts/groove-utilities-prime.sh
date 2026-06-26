#!/usr/bin/env bash
# groove-utilities-prime — output full groove workflow context
# Called by SessionStart hooks and /groove-utilities-prime skill

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX=".groove/index.md"
JSON_MODE=false
if [ "${1:-}" = "--json" ]; then
  JSON_MODE=true
fi

if [ ! -f "$INDEX" ]; then
  if [ "$JSON_MODE" = true ]; then
    echo '{"additional_context": "groove: .groove/index.md not found — run /groove-admin-install to set up groove."}'
  else
    echo "groove: .groove/index.md not found — run /groove-admin-install to set up groove."
  fi
  exit 0
fi

# Extract frontmatter values
extract() {
  local key="$1"
  local default="${2:-}"
  local val
  val=$(sed -n '/^---$/,/^---$/p' "$INDEX" | grep "$key:" | head -1 | sed "s/.*${key}:[[:space:]]*//" | tr -d '[:space:]')
  echo "${val:-$default}"
}

tasks_backend=$(extract "backend" "none")
list_limit=$(extract "list_limit" "15")
analyse_limit=$(extract "analyse_limit" "30")
review_days=$(extract "review_days" "5")
git_memory=$(extract "memory" "commit-all" | head -1)
git_tasks=$(extract "tasks" "commit-all" | head -1)
git_hooks=$(extract "hooks" "commit-all" | head -1)
groovebook=$(extract "groovebook" "")

# Fix: git.* values come from the git: section, re-extract properly
git_memory=$(sed -n '/^git:/,/^[a-z]/p' "$INDEX" | grep 'memory:' | head -1 | sed 's/.*memory:[[:space:]]*//' | tr -d '[:space:]')
git_tasks=$(sed -n '/^git:/,/^[a-z]/p' "$INDEX" | grep 'tasks:' | head -1 | sed 's/.*tasks:[[:space:]]*//' | tr -d '[:space:]')
git_hooks=$(sed -n '/^git:/,/^[a-z]/p' "$INDEX" | grep 'hooks:' | head -1 | sed 's/.*hooks:[[:space:]]*//' | tr -d '[:space:]')

# In JSON mode, capture all output and wrap in additional_context
if [ "$JSON_MODE" = true ]; then
  _tmpfile=$(mktemp)
  trap 'rm -f "$_tmpfile"' EXIT
  _emit_output() {
    _do_output
  } > "$_tmpfile"
fi

_do_output() {

# Version check
bash "$SCRIPT_DIR/../../groove-utilities-check/scripts/check.sh" 2>/dev/null || true
echo ""

# Main context output
cat <<EOF
# Groove Workflow Context

groove is installed in this repo. Use \`/groove-*\` skills for all workflow commands.

## Config
tasks.backend:      ${tasks_backend}
tasks.list_limit:   ${list_limit}
tasks.analyse_limit:${analyse_limit}
memory.review_days: ${review_days}
memory path:        .groove/memory/ (hardcoded)
specs path:         .groove/memory/specs/ (hardcoded)
git.memory:         ${git_memory}
git.tasks:          ${git_tasks}
git.hooks:          ${git_hooks}

## Key commands
/groove-daily-start           — start the workday
/groove-daily-end             — end the workday
/groove-work-brainstorm       — clarify scope (YAGNI enforced)
/groove-work-plan             — research codebase, write implementation plan
/groove-work-exec             — execute the plan
/groove-work-review           — evaluate output, decide accept/rework
/groove-work-compound         — document lessons into existing project files
/groove-work-spec             — create outcome spec (what to build)
/groove-work-doc              — create reference doc (how it works)
/groove-utilities-task-list   — show active, ready tasks
/groove-utilities-task-create — create a task
/groove-utilities-task-analyse — summarise tasks by status
/groove-utilities-memory-log-daily — write daily end log
/groove-utilities-memory-promises       — capture or resolve deferred items
/groove-utilities-memory-mistakes        — log a mistake and resolve it
/groove-utilities-memory-retrospective  — analyse ratings, mistakes, and learnings over a period
/groove-utilities-memory-graduate       — promote a stable lesson to AGENTS.md permanently

## Conventions
- Stage tasks: "YYYY-MM-DD, <Stage>" (no numbers; e.g. 2026-02-28, Brainstorm; 2026-02-28, Compound — topic)
- Memory logs: .groove/memory/daily/, weekly/, monthly/, git/
- Task completion requires "Summary of Changes" in body before marking done
- Archive is always user-triggered — never automatic during end
- 80% of compound loop value is in plan and review — do not skip them

## Steering
- Fix root causes, not symptoms — if a workaround is needed, note the root cause anyway
- YAGNI — only make changes directly requested or clearly necessary; no unrequested refactors
- Verify before acting on shared state — confirm before push, PR creation, or destructive ops
- Smallest diff that solves the problem — prefer editing one file over touching five
- When blocked, ask rather than brute-force — retrying the same failing action wastes context
- Read before editing — understand existing code before proposing changes to it

## Constraints
- Do not edit files under \`.agents/skills/groove-*\` — managed by groove update, changes will be overwritten; to modify, propose PRs to andreadellacorte/groove; to update, run \`/groove-admin-update\`
- User zone: \`.groove/\` is yours — config, hooks, memory, and learned insights are all safe to edit
EOF

# Groovebook section
if [ -n "$groovebook" ]; then
  cat <<EOF

## Groovebook
groovebook: ${groovebook}
/groove-groovebook-publish — publish a learning to the shared commons
/groove-groovebook-review  — browse and review open learning PRs
EOF
fi

# Identity context
if [ -f ".groove/IDENTITY.md" ]; then
  echo ""
  echo "## Identity"
  cat ".groove/IDENTITY.md"
fi

# Pending capture (staged by the session-capture Stop hook)
if [ -s ".groove/.cache/pending-capture.md" ]; then
  cap_date=$(sed -n 's/^# Pending capture — //p' ".groove/.cache/pending-capture.md" | head -1)
  echo ""
  echo "## Pending capture"
  echo "📝 Unsaved session capture from ${cap_date:-a previous session} — run /groove-work-compound or /groove-utilities-memory-log-daily to review and save it (drafts from git activity are staged in .groove/.cache/pending-capture.md)."
fi

# Task prime
bash "$SCRIPT_DIR/groove-utilities-task-prime.sh" 2>/dev/null || true

# Memory prime
echo ""
bash "$SCRIPT_DIR/groove-utilities-memory-prime.sh" 2>/dev/null || true

}

if [ "$JSON_MODE" = true ]; then
  _do_output > "$_tmpfile" 2>/dev/null
  # Escape for JSON: backslashes, quotes, newlines, tabs
  escaped=$(sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/	/\\t/g' "$_tmpfile" | awk '{printf "%s\\n", $0}' | sed 's/\\n$//')
  printf '{"additional_context": "%s"}\n' "$escaped"
else
  _do_output
fi
