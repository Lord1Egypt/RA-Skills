#!/usr/bin/env bash
# Wiki System Bootstrap Script
# One-command setup for any OpenClaw workspace.
# Works with builtin, QMD, or Honcho memory backends.
#
# Usage: bash skills/karpathy-wiki/scripts/wiki-setup.sh [OPTIONS]
#   --tz TIMEZONE     Timezone for cron jobs (default: UTC)
#   --with-cron       Create ingest and lint cron jobs (off by default)
#   --with-sync       Add wiki index to SuperMemory sync script (off by default)
#   --all             Enable --with-cron and --with-sync

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TZ="UTC"
WITH_CRON=0
WITH_SYNC=0

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --tz) TZ="${2:-UTC}"; shift 2 ;;
    --with-cron) WITH_CRON=1; shift ;;
    --with-sync) WITH_SYNC=1; shift ;;
    --all) WITH_CRON=1; WITH_SYNC=1; shift ;;
    *) shift ;;
  esac
done

echo "========================================"
echo "  Wiki System Setup"
echo "========================================"
echo "  Workspace: $WORKSPACE"
echo "  Timezone:  $TZ"
echo "  Cron jobs: $([ $WITH_CRON -eq 1 ] && echo 'yes' || echo 'no (pass --with-cron to enable)')"
echo "  SM sync:   $([ $WITH_SYNC -eq 1 ] && echo 'yes' || echo 'no (pass --with-sync to enable)')"
echo ""

# --- 1. Create directories ---
echo "[1/7] Creating directories..."
mkdir -p "$WORKSPACE/memory/wiki"
mkdir -p "$WORKSPACE/work/wiki-sources/pdfs"
mkdir -p "$WORKSPACE/work/wiki-sources/articles"
mkdir -p "$WORKSPACE/work/wiki-sources/papers"
echo "  Done."

# --- 2. Deploy schema and scaffold files ---
echo "[2/7] Deploying files..."

deploy_if_missing() {
  local src="$1" dst="$2" label="$3"
  if [[ ! -f "$dst" ]]; then
    cp "$src" "$dst"
    echo "  Deployed $label"
  else
    echo "  $label already exists, skipping."
  fi
}

deploy_if_missing "$SKILL_DIR/templates/WIKI-SCHEMA.md" "$WORKSPACE/WIKI-SCHEMA.md" "WIKI-SCHEMA.md"
deploy_if_missing "$SKILL_DIR/templates/index-template.md" "$WORKSPACE/memory/wiki/index.md" "memory/wiki/index.md"
deploy_if_missing "$SKILL_DIR/templates/queue-template.md" "$WORKSPACE/work/wiki-sources/ingestion-queue.md" "ingestion-queue.md"

if [[ ! -f "$WORKSPACE/memory/wiki/log.md" ]]; then
  cp "$SKILL_DIR/templates/log-template.md" "$WORKSPACE/memory/wiki/log.md"
  echo "$(date +"%Y-%m-%d %H:%M") | create | -- | Wiki system initialized" >> "$WORKSPACE/memory/wiki/log.md"
  echo "  Deployed memory/wiki/log.md"
else
  echo "  memory/wiki/log.md already exists, skipping."
fi

# --- 3. Update MEMORY.md (append wiki reference) ---
echo "[3/7] Updating MEMORY.md..."
WIKI_MARKER="memory/wiki/"
if [[ -f "$WORKSPACE/MEMORY.md" ]]; then
  if ! grep -q "$WIKI_MARKER" "$WORKSPACE/MEMORY.md" 2>/dev/null; then
    cat >> "$WORKSPACE/MEMORY.md" << 'WIKI_SECTION'

## Wiki
- `WIKI-SCHEMA.md` — Wiki rules and structure
- `memory/wiki/index.md` — Page catalog
- `memory/wiki/{slug}.md` — Individual wiki pages
- `work/wiki-sources/` — Raw source documents
- `work/wiki-sources/ingestion-queue.md` — Pending sources for ingestion
WIKI_SECTION
    echo "  Appended wiki reference section."
  else
    echo "  Wiki already in MEMORY.md, skipping."
  fi
else
  echo "  No MEMORY.md found (will be created by OpenClaw on first run)."
fi

# --- 4. Add memory/wiki to memorySearch.extraPaths (for builtin backend) ---
echo "[4/7] Configuring memorySearch..."
OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"
if [[ -f "$OPENCLAW_CONFIG" ]]; then
  if ! grep -q "memory/wiki" "$OPENCLAW_CONFIG" 2>/dev/null; then
    if grep -q '"memorySearch"' "$OPENCLAW_CONFIG"; then
      # memorySearch exists, check for extraPaths
      if grep -q '"extraPaths"' "$OPENCLAW_CONFIG"; then
        echo "  extraPaths exists but doesn't include memory/wiki. Add manually:"
        echo '    "memorySearch": { "extraPaths": ["memory/wiki"] }'
      else
        echo "  NOTE: Add memory/wiki to memorySearch.extraPaths in openclaw.json for builtin backend:"
        echo '    "memorySearch": { "extraPaths": ["memory/wiki"] }'
      fi
    else
      echo "  NOTE: For builtin memory backend, add to openclaw.json:"
      echo '    "memorySearch": { "extraPaths": ["memory/wiki"] }'
      echo "  (QMD users: not needed, QMD indexes memory/**/*.md recursively)"
    fi
  else
    echo "  memory/wiki already in config, skipping."
  fi
else
  echo "  No openclaw.json found."
fi

# --- 5. Create cron jobs (opt-in) ---
echo "[5/7] Cron jobs..."
if [[ $WITH_CRON -eq 0 ]]; then
  echo "  Skipped (not requested). To create cron jobs, re-run with --with-cron or run manually:"
  echo '  openclaw cron create --name "Wiki Ingest" --cron "0 4 * * *" --tz "'"$TZ"'" --exact --session isolated --model "sonnet" --timeout-seconds 300 --message "Read skills/karpathy-wiki/scripts/wiki-ingest.md and execute it exactly. Process pending sources from the wiki ingestion queue. Output only the ingest report (or NO_REPLY if queue is empty)." --announce --best-effort-deliver'
  echo '  openclaw cron create --name "Wiki Lint (Weekly)" --cron "30 3 * * 0" --tz "'"$TZ"'" --exact --session isolated --model "haiku" --timeout-seconds 180 --message "Read skills/karpathy-wiki/scripts/wiki-lint.md and execute it exactly. Run the full wiki health check. Output only the lint report (or WIKI_LINT_OK if everything is clean)." --announce --best-effort-deliver'
elif ! command -v openclaw &>/dev/null; then
  echo "  WARNING: openclaw CLI not found. Create cron jobs manually (see commands above)."
else
  if openclaw cron list 2>/dev/null | grep -q "Wiki Ingest"; then
    echo "  Wiki Ingest cron already exists, skipping."
  else
    openclaw cron create \
      --name "Wiki Ingest" \
      --cron "0 4 * * *" \
      --tz "$TZ" \
      --exact \
      --session isolated \
      --model "sonnet" \
      --timeout-seconds 300 \
      --message "Read skills/karpathy-wiki/scripts/wiki-ingest.md and execute it exactly. Process pending sources from the wiki ingestion queue. Output only the ingest report (or NO_REPLY if queue is empty)." \
      --announce \
      --best-effort-deliver > /dev/null 2>&1 && \
    echo "  Created Wiki Ingest (daily 4:00 AM $TZ)." || \
    echo "  WARNING: Failed to create Wiki Ingest cron. Create manually or check gateway."
  fi

  if openclaw cron list 2>/dev/null | grep -q "Wiki Lint"; then
    echo "  Wiki Lint cron already exists, skipping."
  else
    openclaw cron create \
      --name "Wiki Lint (Weekly)" \
      --cron "30 3 * * 0" \
      --tz "$TZ" \
      --exact \
      --session isolated \
      --model "haiku" \
      --timeout-seconds 180 \
      --message "Read skills/karpathy-wiki/scripts/wiki-lint.md and execute it exactly. Run the full wiki health check. Output only the lint report (or WIKI_LINT_OK if everything is clean)." \
      --announce \
      --best-effort-deliver > /dev/null 2>&1 && \
    echo "  Created Wiki Lint (Sunday 3:30 AM $TZ)." || \
    echo "  WARNING: Failed to create Wiki Lint cron. Create manually or check gateway."
  fi
fi

# --- 6. SuperMemory sync (opt-in) ---
echo "[6/7] SuperMemory sync..."
if [[ $WITH_SYNC -eq 0 ]]; then
  echo "  Skipped (not requested). To add wiki index to SuperMemory sync, re-run with --with-sync."
else
  SYNC_SCRIPT="$WORKSPACE/scripts/supermemory-sync-workspace.sh"
  if [[ -f "$SYNC_SCRIPT" ]]; then
    if ! grep -q "memory/wiki/index.md" "$SYNC_SCRIPT" 2>/dev/null; then
      if grep -q "memory/workflows.md" "$SYNC_SCRIPT"; then
        sed -i '' '/"memory\/workflows.md"/a\
  "memory/wiki/index.md"
' "$SYNC_SCRIPT" 2>/dev/null || sed -i '/"memory\/workflows.md"/a\  "memory/wiki/index.md"' "$SYNC_SCRIPT" 2>/dev/null
        echo "  Added memory/wiki/index.md to sync script."
      else
        echo "  Could not find insertion point in sync script. Add manually:"
        echo '    "memory/wiki/index.md"'
      fi
    else
      echo "  Already in sync script, skipping."
    fi
  else
    echo "  No SuperMemory sync script found at $SYNC_SCRIPT."
  fi
fi

# --- 7. Verify ---
echo "[7/7] Verifying..."

check_exists() {
  if [[ -e "$1" ]]; then
    echo "  OK  $2"
  else
    echo "  FAIL $2"
  fi
}

check_exists "$WORKSPACE/memory/wiki" "memory/wiki/ directory"
check_exists "$WORKSPACE/memory/wiki/index.md" "memory/wiki/index.md"
check_exists "$WORKSPACE/memory/wiki/log.md" "memory/wiki/log.md"
check_exists "$WORKSPACE/WIKI-SCHEMA.md" "WIKI-SCHEMA.md"
check_exists "$WORKSPACE/work/wiki-sources/ingestion-queue.md" "ingestion-queue.md"

echo ""
echo "========================================"
echo "  Wiki system ready!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Drop source files into work/wiki-sources/"
echo "  2. Add them to work/wiki-sources/ingestion-queue.md"
echo "  3. Say 'wiki ingest' to the agent, or trigger via cron"
if [[ $WITH_CRON -eq 0 ]]; then
  echo ""
  echo "  To enable automated ingestion and lint:"
  echo "    bash skills/karpathy-wiki/scripts/wiki-setup.sh --with-cron --tz $TZ"
fi
echo ""
