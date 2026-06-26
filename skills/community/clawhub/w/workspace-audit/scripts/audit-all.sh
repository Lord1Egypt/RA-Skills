#!/usr/bin/env bash
# Run all workspace audits
# Usage: bash scripts/audit-all.sh [--verbose]
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERBOSE="${1:-}"
FAIL=0

echo "╔══════════════════════════════════════╗"
echo "║       Workspace Audit Suite          ║"
echo "╚══════════════════════════════════════╝"
echo ""

run_audit() {
  local name="$1"
  local script="$2"
  echo "━━━ $name ━━━"
  if "$script" $VERBOSE; then
    echo ""
  else
    FAIL=$((FAIL + 1))
    echo ""
  fi
}

run_audit "Structure & Size" "$SCRIPT_DIR/audit-structure.sh"
run_audit "1Password Vault" "$SCRIPT_DIR/audit-1password.sh"
run_audit "Duplication" "$SCRIPT_DIR/audit-duplication.sh"
run_audit "Path References" "$SCRIPT_DIR/audit-paths.sh"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$FAIL" -gt 0 ]; then
  echo "⚠️  $FAIL audit(s) found issues"
  exit 1
else
  echo "✅ All audits passed"
  exit 0
fi
