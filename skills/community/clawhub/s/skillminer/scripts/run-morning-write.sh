#!/bin/bash
# skillminer morning writer wrapper — invoked by cron at 10:00
# OpenClaw edition: uses `openclaw agent --message` (or claude as fallback via FORGE_RUNNER).
# No su - forge: OC isolated session provides sandboxing.

set -euo pipefail

export CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORGE_DIR="$SKILL_DIR"
STATE_DIR="$FORGE_DIR/state"
STATE_FILE="$STATE_DIR/state.json"
WRITE_LOG_DIR="$STATE_DIR/write-log"
LOG_DIR="$STATE_DIR/logs"
mkdir -p "$LOG_DIR" "$WRITE_LOG_DIR"

# shellcheck source=/dev/null
source "$FORGE_DIR/scripts/lib/atomic-write.sh"
# shellcheck source=/dev/null
source "$FORGE_DIR/scripts/lib/secret-scrub.sh"
# shellcheck source=/dev/null
source "$FORGE_DIR/scripts/lib/slug-validate.sh"
if ! acquire_skillminer_lock; then
  exit 3
fi

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
TODAY="$(date -u +%Y-%m-%d)"
LOG="$LOG_DIR/write-${TODAY}T$(date -u +%H-%M-%SZ).log"

# Bug 6: remove stale tmps from any prior crashed run before creating a fresh backup
rm -f "$STATE_FILE.tmp" "$WRITE_LOG_DIR/$TODAY.md.tmp" \
      "$STATE_DIR/.last-success.tmp" "$STATE_DIR/.last-write.tmp"
# Remove any staging dir not scoped to this run's STAMP — mtime-based cleanup
# leaks crash dirs from within the last hour, which could shadow the new run.
if [[ -d "$CLAWD_DIR/skills/_pending/.staging" ]]; then
  find "$CLAWD_DIR/skills/_pending/.staging" -maxdepth 1 -mindepth 1 -type d ! -name "*-${STAMP}" 2>/dev/null | xargs -r rm -rf
fi

BACKUP_FILE="$(create_state_backup "$STATE_FILE" "$STAMP")"
rotate_state_backups "$STATE_FILE"

FORGE_RUNNER="${FORGE_RUNNER:-openclaw}"

# Read OC agent from config (prefer local override when present)
CONFIG_FILE="$FORGE_DIR/config/skill-miner.config.local.json"
if [ ! -f "$CONFIG_FILE" ]; then
  CONFIG_FILE="$FORGE_DIR/config/skill-miner.config.json"
fi
OC_AGENT="$(jq -r '.runner.openclaw_agent // "main"' "$CONFIG_FILE" 2>/dev/null || echo 'main')"
MAX_BUDGET_USD="$(jq -r '.scan.maxBudgetUsd // 3' "$CONFIG_FILE" 2>/dev/null || echo '3')"

while IFS= read -r candidate_slug; do
  if ! validate_slug "$candidate_slug" "accepted candidate id"; then
    echo "[skillminer] FATAL: state.json contains invalid accepted slug, aborting write" >&2
    exit 4
  fi
done < <(jq -r '.candidates[] | select(.status == "accepted") | .id' "$STATE_FILE")

# Write temp prompt file — inject CLAWD_DIR preamble (OC agent doesn't inherit env vars)
PROMPT_FILE="$(mktemp /tmp/forge-write-prompt.XXXXXX.md)"
{
  printf '> **Runtime preamble (injected by run-morning-write.sh):**\n'
  printf '> `CLAWD_DIR=%s` — use this as the authoritative CLAWD_DIR value throughout; skip Step 0 MISSING check (env var is not available in the agent session, but this path is confirmed valid).\n' \
    "$CLAWD_DIR"
  printf '> `FORGE_DIR=%s` — use this as the authoritative installed skill path throughout; do not derive it from `CLAWD_DIR`.\n' \
    "$FORGE_DIR"
  printf '> `scan.maxBudgetUsd=%s` — use this for any Claude fallback budget reference.\n' "$MAX_BUDGET_USD"
  printf '> `SKILLMINER_WRITE_STAMP=%s` — staging stamp for this run. Write each pending skill to `_pending/.staging/<slug>-%s/` instead of `_pending/<slug>/` directly. The wrapper will atomically rename staging dirs to final paths after state commits, or remove them on rollback.\n\n' \
    "$STAMP" "$STAMP"
  cat "$FORGE_DIR/prompts/skill-writer.md"
} > "$PROMPT_FILE"

cd "$CLAWD_DIR"
{
  echo "=== skillminer morning-write ==="
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

PENDING_DIR="$CLAWD_DIR/skills/_pending"
STAGING_BASE="$PENDING_DIR/.staging"

rollback_pending_staging() {
  # Remove any staging dirs left by this run
  find "$STAGING_BASE" -maxdepth 1 -type d -name "*-${STAMP}" 2>/dev/null | xargs -r rm -rf
}

rollback_state_and_write_log() {
  local reason="$1"
  if [[ -f "$BACKUP_FILE" ]]; then
    cp -f "$BACKUP_FILE" "$STATE_FILE"
  fi
  rm -f "$WRITE_LOG_DIR/$TODAY.md" "$STATE_FILE.tmp"
  rollback_pending_staging
  echo "[skillminer] ROLLBACK: $reason" >> "$LOG"
}

commit_pending_staging() {
  # Atomically rename staging dirs to final _pending/<slug>/ paths
  while IFS= read -r staging_dir; do
    slug="$(basename "$staging_dir" "-${STAMP}")"
    if ! validate_slug "$slug" "staging dir"; then
      echo "[skillminer] ERROR: refusing to commit staging dir with invalid slug: $staging_dir" >> "$LOG"
      rm -rf "$staging_dir"
      continue
    fi
    final_dir="$PENDING_DIR/$slug"
    if [[ -d "$final_dir" ]]; then
      echo "[skillminer] WARN: staging rename skipped, _pending/$slug already exists (collision)" >> "$LOG"
    else
      mv "$staging_dir" "$final_dir"
      echo "[skillminer] staged _pending/$slug committed" >> "$LOG"
    fi
  done < <(find "$STAGING_BASE" -maxdepth 1 -type d -name "*-${STAMP}" 2>/dev/null)
}

VALIDATION_EXIT=0
FINAL_EXIT="$EXIT"
if [ "$EXIT" -eq 0 ]; then
  if ! atomic_text_write "$WRITE_LOG_DIR/$TODAY.md.tmp" "$WRITE_LOG_DIR/$TODAY.md"; then
    echo "[skillminer] ERROR: morning write-log tmp failed non-empty check, restored backup" >> "$LOG"
    cp "$BACKUP_FILE" "$STATE_FILE"
    rollback_pending_staging
    VALIDATION_EXIT=2
  elif ! { [ -f "$STATE_FILE.tmp" ] && scrub_file_in_place "$STATE_FILE.tmp"; true; } || ! atomic_json_write "$STATE_FILE.tmp" "$STATE_FILE" "$BACKUP_FILE"; then
    echo "[skillminer] ERROR: morning state tmp failed JSON validation, restored backup" >> "$LOG"
    rollback_state_and_write_log "state tmp failed JSON validation"
    VALIDATION_EXIT=2
  elif ! jq -e '.schema_version == "0.5"' "$STATE_FILE" >/dev/null 2>&1; then
    echo "[skillminer] ERROR: state.json schema_version not 0.5 — run scripts/migrate-state.sh" >&2
    echo "[skillminer] ERROR: state.json schema_version not 0.5 after write, restored backup" >> "$LOG"
    rollback_state_and_write_log "schema_version not 0.5 after write"
    VALIDATION_EXIT=2
  elif ! atomic_text_write "$STATE_DIR/.last-write.tmp" "$STATE_DIR/.last-write"; then
    echo "[skillminer] ERROR: morning .last-write tmp failed non-empty check, restored backup" >> "$LOG"
    rollback_state_and_write_log ".last-write tmp failed non-empty check"
    VALIDATION_EXIT=2
  elif ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
    echo "[skillminer] ERROR: morning state validation failed after rename, restored backup" >> "$LOG"
    rollback_state_and_write_log "final state validation failed after rename"
    VALIDATION_EXIT=2
  else
    commit_pending_staging
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
find "$LOG_DIR" -name 'write-*.log' -type f -printf '%T@ %p\n' | \
  sort -n | head -n -30 | cut -d' ' -f2- | xargs -r rm -f

exit "$FINAL_EXIT"
