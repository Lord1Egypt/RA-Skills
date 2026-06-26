#!/usr/bin/env bash
set -euo pipefail

SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"

echo "=== Sage COO heartbeat: $NOW ==="

if [ ! -d "$SAGE_HOME" ]; then
  echo "[MISSING] $SAGE_HOME does not exist. Run scripts/init_sage.sh first."
  exit 1
fi

REQUIRED=(
  "INDEX.md"
  "MANIFEST.yaml"
  "company_profile/basic_info.md"
  "team_and_roles/roster.csv"
  "operations_and_workflows/daily_operations.md"
  "memory_and_insights/open_loops.md"
  "memory_and_insights/recent_decisions.md"
  "inbox/capture.md"
  "inbox/unresolved.md"
)

ISSUES=0
for file in "${REQUIRED[@]}"; do
  if [ ! -f "$SAGE_HOME/$file" ]; then
    echo "[MISSING] $file"
    ISSUES=$((ISSUES + 1))
  fi
done

if grep -R "待填写" "$SAGE_HOME/INDEX.md" "$SAGE_HOME/company_profile/basic_info.md" >/dev/null 2>&1; then
  echo "[ONBOARDING] Core company profile still has placeholders."
  ISSUES=$((ISSUES + 1))
fi

CAPTURE_LINES=$(wc -l < "$SAGE_HOME/inbox/capture.md" 2>/dev/null || echo 0)
if [ "$CAPTURE_LINES" -gt 120 ]; then
  echo "[ATTENTION] inbox/capture.md is growing. Consider promoting confirmed facts."
  ISSUES=$((ISSUES + 1))
fi

if [ "$ISSUES" -eq 0 ]; then
  echo "[OK] Sage DNA looks healthy."
else
  echo "[ATTENTION] $ISSUES issue(s) need review."
fi

