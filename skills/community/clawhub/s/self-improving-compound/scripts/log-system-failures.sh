#!/usr/bin/env bash
set -euo pipefail
ROOT="${OPENCLAW_WORKSPACE:-$PWD}"
LEARNING_ROOT="${SELF_IMPROVING_LEARNING_ROOT:-${SELF_IMPROVING_LEARNING_DIR:-$ROOT/learning}}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="${SELF_IMPROVING_SKILL_DIR:-$(dirname "$SCRIPT_DIR")}"
LEARNINGS_CLI="${SELF_IMPROVING_LEARNINGS_CLI:-$SKILL_DIR/scripts/learnings.py}"
LOG="$LEARNING_ROOT/system-failure-audit.log"
mkdir -p "$LEARNING_ROOT"
{
  echo "# system failure audit $(date -Is)"
  if command -v openclaw >/dev/null 2>&1; then
    echo "## openclaw status"
    openclaw status 2>&1 || true
    echo "## gateway status"
    openclaw gateway status 2>&1 || true
    if openclaw help 2>/dev/null | grep -q '\bdoctor\b'; then
      echo "## openclaw doctor"
      openclaw doctor 2>&1 || true
    fi
  else
    echo "openclaw CLI not found"
  fi
} > "$LOG.tmp"
mv "$LOG.tmp" "$LOG"
if grep -Eiq '(^|[^a-z])(error|failed|failure|unhealthy|critical|panic|exception|traceback)([^a-z]|$)' "$LOG"; then
  SUMMARY=$(grep -Ei 'error|failed|failure|unhealthy|critical|panic|exception|traceback' "$LOG" | head -5 | tr '\n' '; ' | cut -c1-500)
  python3 "$LEARNINGS_CLI" --root "$ROOT" search "$SUMMARY" --limit 3 | grep -q 'No results' && \
  python3 "$LEARNINGS_CLI" --root "$ROOT" log-error \
    --summary "OpenClaw system audit detected failure signal" \
    --details "${SUMMARY}. Full audit log: $LOG" \
    --pattern "system:openclaw-audit-failure" \
    --area "domain:openclaw" \
    --force || true
fi
echo "[system-failure-audit] wrote $LOG"
