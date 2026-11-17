#!/usr/bin/env bash
# termux-compat-runner: validate a command against a safety allowlist, DRY-RUN only.
#
# This script NEVER executes the command. It only checks whether the command
# matches a category (READ-ONLY, MUTATING, or DENIED) and prints the result.
# Execution is left to the user.
#
# Categories:
#   READ-ONLY  — safe informational commands (ls, cat, ps, ss, git status, etc.)
#   MUTATING   — commands that change state (pkg install, git pull, apt, etc.)
#                These are flagged but not denied — user must confirm manually.
#   DENIED     — destructive commands (rm -rf, mkfs, dd, chmod -R, etc.)
#
# Shell operators (|, &&, ||, ;, $(), backticks, >, <) are always rejected
# unless the user explicitly passes --approve-operators.
#
# Usage:
#   bash scripts/run_safe.sh "ss -tulpen" --timeout 60
#   bash scripts/run_safe.sh "pkg update" --timeout 60
#   bash scripts/run_safe.sh "rm -rf /tmp/old"   # DENIED
set -uo pipefail

cmd="${1:-}"
shift || true
timeout_val=60
approve_operators=0

while [ $# -gt 0 ]; do
  case "$1" in
    --timeout) timeout_val="${2:-60}"; shift 2 ;;
    --approve-operators) approve_operators=1; shift ;;
    *) shift ;;
  esac
done

[ -z "$cmd" ] && { echo "usage: $0 <command> [--timeout N] [--approve-operators]" >&2; exit 2; }

# --- Shell operator detection ---
OPERATOR_PATTERN='[|&;<>`$()]'
if [ "$approve_operators" -eq 0 ]; then
  if echo "$cmd" | grep -Eq "$OPERATOR_PATTERN"; then
    echo "[run_safe] DENIED"
    echo "    reason: command contains shell operators (|, &, ;, <, >, \$, (), backtick)"
    echo "    operators require explicit --approve-operators flag"
    echo "[run_safe] no command was executed."
    exit 1
  fi
fi

# --- Destructive patterns (always denied) ---
DENY=(
  'rm[[:space:]].*-rf'
  'rm[[:space:]].*-fr'
  'mkfs'
  '(^|[[:space:]])dd[[:space:]]'
  'chmod[[:space:]].*-R'
  'chown[[:space:]].*-R'
  ':\(\)\{'
  '>[[:space:]]*/dev/'
  'shutdown'
  'reboot'
  'systemctl'
  'mkfs\.[a-z0-9]+'
  'fdisk'
  'parted'
)

# --- Read-only patterns ---
READONLY=(
  '^(ls|ll|cat|head|tail|wc|echo|printf|pwd|date|uname|whoami|id|env|printenv)[[:space:]]'
  '^(ss|netstat|ip|ifconfig|ping|getprop|dumpsys)[[:space:]]'
  '^(ps|top|free|df|du|mount|uptime|lscpu|lsof)[[:space:]]'
  '^git[[:space:]](status|log|diff|branch|show|blame|remote)[[:space:]]'
  '^command[[:space:]]-v[[:space:]]'
  '^which[[:space:]]'
  '^pkg[[:space:]](list-installed|search|show)[[:space:]]'
  '^dpkg[[:space:]]-l[[:space:]]'
  '^apt[[:space:]]list[[:space:]]'
)

# --- Mutating patterns (allowed but flagged) ---
MUTATING=(
  '^pkg[[:space:]](update|upgrade|install|remove)[[:space:]]'
  '^(apt|apt-get)[[:space:]](update|upgrade|install|remove)[[:space:]]'
  '^dpkg[[:space:]](-i|--install|--remove)[[:space:]]'
  '^git[[:space:]](fetch|pull|push|merge|rebase|checkout|reset|clean)[[:space:]]'
  '^termux-setup-storage'
  '^termux-change-repo'
  '^pip[[:space:]]install'
  '^npm[[:space:]]install'
  '^cargo[[:space:]]install'
)

# Check destructive first
reason=""
for d in "${DENY[@]}"; do
  if echo "$cmd" | grep -Eq "$d"; then
    reason="matches destructive pattern: $d"
    break
  fi
done

if [ -n "$reason" ]; then
  echo "[run_safe] DENIED"
  echo "    reason: $reason"
  echo "[run_safe] no command was executed."
  exit 1
fi

# Check read-only
for r in "${READONLY[@]}"; do
  if echo "$cmd" | grep -Eq "$r"; then
    echo "[run_safe] ALLOWED-READ"
    echo "    classification: READ-ONLY"
    echo "    would run with timeout ${timeout_val}s:"
    echo "    timeout ${timeout_val} ${cmd}"
    echo "[run_safe] review then run manually if you approve."
    exit 0
  fi
done

# Check mutating
for m in "${MUTATING[@]}"; do
  if echo "$cmd" | grep -Eq "$m"; then
    echo "[run_safe] ALLOWED-MUTATING"
    echo "    classification: MUTATING — requires explicit user confirmation"
    echo "    would run with timeout ${timeout_val}s:"
    echo "    timeout ${timeout_val} ${cmd}"
    echo "[run_safe] confirm with user before executing manually."
    exit 0
  fi
done

# Not on any list
echo "[run_safe] DENIED"
echo "    reason: command not on any allowlist (read-only or mutating)"
echo "    if this command is safe, add it to the appropriate pattern list."
echo "[run_safe] no command was executed."
exit 1
