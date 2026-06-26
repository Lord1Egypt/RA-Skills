#!/usr/bin/env bash
# daily-memory.sh - Portable helper for a daily factual-memory digest.
#
# This script does not write the final note by itself. It validates the target
# date/root, optionally runs a user-provided context collector, and prints the
# contract the agent should follow when writing memory/YYYY-MM-DD.md.

set -euo pipefail

ROOT="${OPENCLAW_WORKSPACE:-$PWD}"
DATE=""
COLLECTOR="${SELF_IMPROVING_DAILY_COLLECTOR:-}"

usage() {
  cat <<'USAGE'
Usage: daily-memory.sh [--root PATH] [--date YYYY-MM-DD] [--collector COMMAND]

Prepare a Daily Memory Digest run. The agent should then gather/read context,
write memory/YYYY-MM-DD.md, and run the self-improvement capture pass.

Options:
  --root PATH          Workspace root (default: OPENCLAW_WORKSPACE or $PWD)
  --date DATE          Target date in YYYY-MM-DD format (default: today in Asia/Shanghai)
  --collector COMMAND  Optional command that collects/prints daily context.
                       Also configurable via SELF_IMPROVING_DAILY_COLLECTOR.

Collector contract:
  If provided, COMMAND is executed with DAILY_MEMORY_DATE and OPENCLAW_WORKSPACE
  in the environment. It may print a context file path or summary. The agent
  must inspect the output before writing the final note.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) ROOT="$2"; shift 2 ;;
    --date) DATE="$2"; shift 2 ;;
    --collector) COLLECTOR="$2"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if [[ -z "$DATE" ]]; then
  DATE="$(TZ=Asia/Shanghai date +%F)"
fi

if [[ ! "$DATE" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "ERROR: --date must be in YYYY-MM-DD format. Got: $DATE" >&2
  usage >&2
  exit 1
fi

mkdir -p "$ROOT/memory"

if [[ -n "$COLLECTOR" ]]; then
  echo "[daily-memory] Running collector: $COLLECTOR"
  DAILY_MEMORY_DATE="$DATE" OPENCLAW_WORKSPACE="$ROOT" bash -lc "$COLLECTOR"
else
  echo "[daily-memory] No collector configured. Gather context with runtime tools before writing the note."
fi

cat <<EOF

[daily-memory] Contract:
- Workspace root: $ROOT
- Target note:    $ROOT/memory/$DATE.md
- Date:           $DATE

Write a factual daily note with these sections when applicable:
1. Overview
2. Key workflows and actions
3. Important decisions
4. System/configuration changes
5. Files/projects changed
6. External integrations and automations
7. Problems, risks, and unfinished work
8. Items to promote into long-term memory/rules
9. Next-step suggestions
10. Source notes

After writing the note, run the self-improvement capture gate:
- corrections/preferences -> log-correction
- tool/API/schema failures -> log-error
- reusable workflow conventions -> log-learning
- missing capabilities/repeated friction -> log-feature
EOF
