#!/bin/bash
# skillminer nightly scan wrapper — invoked by cron at 04:00
# OpenClaw edition: uses `openclaw agent --message` (or claude as fallback via FORGE_RUNNER).
# No su - forge: OC isolated session provides sandboxing.

set -euo pipefail

export CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORGE_DIR="$SKILL_DIR"
STATE_DIR="$FORGE_DIR/state"
STATE_FILE="$STATE_DIR/state.json"
REVIEW_DIR="$STATE_DIR/review"
LOG_DIR="$STATE_DIR/logs"
mkdir -p "$LOG_DIR" "$REVIEW_DIR"

# shellcheck source=/dev/null
source "$FORGE_DIR/scripts/lib/atomic-write.sh"
# shellcheck source=/dev/null
source "$FORGE_DIR/scripts/lib/secret-scrub.sh"
if ! acquire_skillminer_lock; then
  exit 3
fi

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TODAY="$(date -u +%Y-%m-%d)"
LOG="$LOG_DIR/scan-${TODAY}T$(date -u +%H-%M-%SZ).log"

# Bug 6: remove stale tmps from any prior crashed run before creating a fresh backup
rm -f "$STATE_FILE.tmp" "$REVIEW_DIR/$TODAY.md.tmp" \
      "$STATE_DIR/.last-success.tmp" "$STATE_DIR/.last-write.tmp"

BACKUP_FILE="$(create_state_backup "$STATE_FILE" "$STAMP")"
rotate_state_backups "$STATE_FILE"

FORGE_RUNNER="${FORGE_RUNNER:-openclaw}"

# Read config (prefer local override when present)
CONFIG_FILE="$FORGE_DIR/config/skill-miner.config.local.json"
if [ ! -f "$CONFIG_FILE" ]; then
  CONFIG_FILE="$FORGE_DIR/config/skill-miner.config.json"
fi
OC_AGENT="$(jq -r '.runner.openclaw_agent // "main"' "$CONFIG_FILE" 2>/dev/null || echo 'main')"
SCAN_WINDOW_DAYS="$(jq -r '.scan.windowDays // 10' "$CONFIG_FILE" 2>/dev/null || echo '10')"
SCAN_MIN_OCCURRENCES="$(jq -r '.scan.minOccurrences // 3' "$CONFIG_FILE" 2>/dev/null || echo '3')"
SCAN_MIN_DISTINCT_DAYS="$(jq -r '.scan.minDistinctDays // 2' "$CONFIG_FILE" 2>/dev/null || echo '2')"
SCAN_COOLDOWN_DAYS="$(jq -r '.scan.cooldownDays // 30' "$CONFIG_FILE" 2>/dev/null || echo '30')"
THRESHOLD_LOW="$(jq -r '.thresholds.low // .scan.minOccurrences // 3' "$CONFIG_FILE" 2>/dev/null || echo '3')"
THRESHOLD_MEDIUM="$(jq -r '.thresholds.medium // 4' "$CONFIG_FILE" 2>/dev/null || echo '4')"
THRESHOLD_HIGH="$(jq -r '.thresholds.high // 6' "$CONFIG_FILE" 2>/dev/null || echo '6')"
MAX_BUDGET_USD="$(jq -r '.scan.maxBudgetUsd // 3' "$CONFIG_FILE" 2>/dev/null || echo '3')"

# Write temp prompt file — inject runtime values (OC agent doesn't inherit env vars)
PROMPT_FILE="$(mktemp /tmp/forge-scan-prompt.XXXXXX.md)"
{
  printf '> **Runtime preamble (injected by run-nightly-scan.sh):**\n'
  printf '> `CLAWD_DIR=%s` — use this as the authoritative CLAWD_DIR value throughout; skip Step 0 MISSING check (env var is not available in the agent session, but this path is confirmed valid).\n' "$CLAWD_DIR"
  printf '> `FORGE_DIR=%s` — use this as the authoritative installed skill path throughout; do not derive it from `CLAWD_DIR`.\n' "$FORGE_DIR"
  printf '> `scan.windowDays=%s`, `scan.minOccurrences=%s`, `scan.minDistinctDays=%s`, `scan.cooldownDays=%s` — these are the active scan settings from `%s`; use them instead of prompt defaults wherever referenced below.\n' \
    "$SCAN_WINDOW_DAYS" "$SCAN_MIN_OCCURRENCES" "$SCAN_MIN_DISTINCT_DAYS" "$SCAN_COOLDOWN_DAYS" "$CONFIG_FILE"
  printf '> `thresholds.low=%s`, `thresholds.medium=%s`, `thresholds.high=%s` — use these configured confidence bands instead of hardcoded occurrence bands.\n' \
    "$THRESHOLD_LOW" "$THRESHOLD_MEDIUM" "$THRESHOLD_HIGH"
  printf '> `scan.maxBudgetUsd=%s` — use this for any Claude fallback budget reference.\n\n' "$MAX_BUDGET_USD"
  cat "$FORGE_DIR/prompts/nightly-scan.md"
} > "$PROMPT_FILE"

for f in "$CLAWD_DIR"/memory/*.md; do
  [ -f "$f" ] || continue
  size="$(stat -c%s "$f")"
  if [ "$size" -gt 51200 ]; then
    echo "[skillminer] WARN: oversized memory file ($size bytes): $f" >&2
  fi
done

cd "$CLAWD_DIR"
{
  echo "=== skillminer nightly-scan ==="
  echo "started: $(date -u --iso-8601=seconds)"
  echo "CLAWD_DIR=$CLAWD_DIR"
  echo "FORGE_RUNNER=$FORGE_RUNNER"
  echo "user: $(id -un)"
  echo "---"
} > "$LOG"

set +e
if [ "$FORGE_RUNNER" = "openclaw" ]; then
  openclaw agent --agent "$OC_AGENT" --message "$(cat "$PROMPT_FILE")" >> "$LOG" 2>&1
  EXIT=$?
elif [ "$FORGE_RUNNER" = "claude" ]; then
  # Note: Claude Code blocks file-read permission bypass as root (security policy).
  # The claude runner requires running as a non-root user. As root, use FORGE_RUNNER=openclaw.
  if [ "$(id -u)" = "0" ]; then
    echo "WARNING: claude runner cannot bypass file permissions as root (Claude Code security policy)." >> "$LOG"
    echo "Use FORGE_RUNNER=openclaw (default) or run as a non-root user for the claude runner." >> "$LOG"
    rm -f "$PROMPT_FILE"
    exit 1
  fi
  claude --print \
    --model sonnet \
    --effort high \
    --permission-mode auto \
    --max-budget-usd "$MAX_BUDGET_USD" \
    < "$PROMPT_FILE" >> "$LOG" 2>&1
  EXIT=$?
else
  echo "ERROR: unknown FORGE_RUNNER=$FORGE_RUNNER (expected: openclaw | claude)" >> "$LOG"
  EXIT=1
fi
set -e

rm -f "$PROMPT_FILE"

rollback_state_and_review() {
  local reason="$1"
  if [[ -f "$BACKUP_FILE" ]]; then
    cp -f "$BACKUP_FILE" "$STATE_FILE"
  fi
  rm -f "$REVIEW_DIR/$TODAY.md"
  rm -f "$STATE_FILE.tmp"
  echo "[skillminer] ROLLBACK: $reason" >> "$LOG"
}

VALIDATION_EXIT=0
FINAL_EXIT="$EXIT"
if [ "$EXIT" -eq 0 ]; then
  if ! atomic_text_write "$REVIEW_DIR/$TODAY.md.tmp" "$REVIEW_DIR/$TODAY.md"; then
    echo "[skillminer] ERROR: nightly review tmp failed non-empty check, keeping previous state" >> "$LOG"
    rollback_state_and_review "review tmp failed non-empty check"
    VALIDATION_EXIT=2
  elif ! { [ -f "$STATE_FILE.tmp" ] && scrub_file_in_place "$STATE_FILE.tmp"; true; } || ! atomic_json_write "$STATE_FILE.tmp" "$STATE_FILE" "$BACKUP_FILE"; then
    echo "[skillminer] ERROR: nightly state tmp failed JSON validation, restored backup" >> "$LOG"
    rollback_state_and_review "state tmp failed JSON validation"
    VALIDATION_EXIT=2
  elif ! jq -e '.schema_version == "0.5"' "$STATE_FILE" >/dev/null 2>&1; then
    echo "[skillminer] ERROR: state.json schema_version not 0.5 — run scripts/migrate-state.sh" >&2
    echo "[skillminer] ERROR: state.json schema_version not 0.5 after write, restored backup" >> "$LOG"
    rollback_state_and_review "schema_version not 0.5 after write"
    VALIDATION_EXIT=2
  elif ! atomic_text_write "$STATE_DIR/.last-success.tmp" "$STATE_DIR/.last-success"; then
    echo "[skillminer] ERROR: nightly .last-success tmp failed non-empty check, restored backup" >> "$LOG"
    rollback_state_and_review ".last-success tmp failed non-empty check"
    VALIDATION_EXIT=2
  elif ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
    echo "[skillminer] ERROR: nightly state validation failed after rename, restored backup" >> "$LOG"
    rollback_state_and_review "final state validation failed after rename"
    VALIDATION_EXIT=2
  fi
fi
if [ "$VALIDATION_EXIT" -ne 0 ]; then
  FINAL_EXIT="$VALIDATION_EXIT"
fi
{
  echo "---"
  echo "exit: $FINAL_EXIT"
  echo "finished: $(date -u --iso-8601=seconds)"
} >> "$LOG"

# rotate logs — keep last 30
find "$LOG_DIR" -name 'scan-*.log' -type f -printf '%T@ %p\n' | \
  sort -n | head -n -30 | cut -d' ' -f2- | xargs -r rm -f

exit "$FINAL_EXIT"
