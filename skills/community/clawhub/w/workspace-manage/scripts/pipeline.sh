#!/usr/bin/env bash
# Workspace Pipeline - Master orchestrator for all 5 steps
# Part of workspace-manager skill
# Usage: pipeline.sh [step...] or pipeline.sh --all
# Steps: audit, organize, clean, archive, sync

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
SCRIPT_DIR="$SKILL_DIR/scripts"
STEP_LOG="$WORKSPACE/Workspace_Agent/logs/pipeline-$(date '+%Y-%m-%d').log"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"; }
pass() { echo -e "${GREEN}✅${NC} $1"; }
warn() { echo -e "${YELLOW}⚠️ ${NC} $1"; }
fail() { echo -e "${RED}❌${NC} $1"; }

usage() {
    echo "Usage: $0 [OPTIONS] [STEPS]"
    echo ""
    echo "Options:"
    echo "  --all       Run all steps (default)"
    echo "  --list      List available steps"
    echo "  --dry-run   Preview without executing"
    echo ""
    echo "Steps:"
    echo "  audit     1. Health check & scoring"
    echo "  organize  2. Sort files to proper locations"
    echo "  clean     3. Safe cleanup (dry-run first)"
    echo "  archive   4. Move old files to archive/"
    echo "  sync      5. Backup to Google Drive"
    echo ""
    echo "Examples:"
    echo "  $0 --all              Run full pipeline"
    echo "  $0 audit organize     Run only audit + organize"
    echo "  $0 --dry-run clean    Preview cleanup without executing"
}

# Parse arguments
DRY_RUN=false
STEPS=()
MODE="all"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all) MODE="all"; shift ;;
        --list)
            echo "Available steps: audit, organize, clean, archive, sync"
            exit 0 ;;
        --dry-run) DRY_RUN=true; shift ;;
        --*) usage; exit 1 ;;
        *) STEPS+=("$1"); shift ;;
    esac
done

# Set steps based on mode
if [ ${#STEPS[@]} -eq 0 ] || [ "$MODE" = "all" ]; then
    STEPS=("audit" "organize" "clean" "archive" "sync")
fi

# Ensure log directory exists
mkdir -p "$(dirname "$STEP_LOG")"

# Log pipeline start
echo "" | tee -a "$STEP_LOG"
echo "========================================" | tee -a "$STEP_LOG"
echo "🚀 Pipeline started: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$STEP_LOG"
echo "   Steps: ${STEPS[*]}" | tee -a "$STEP_LOG"
echo "   Dry-run: $DRY_RUN" | tee -a "$STEP_LOG"
echo "========================================" | tee -a "$STEP_LOG"

FAILED=0

for step in "${STEPS[@]}"; do
    echo "" | tee -a "$STEP_LOG"
    case "$step" in
        audit)
            log "🔍 Step 1/5: Running health check..."
            if bash "$SCRIPT_DIR/health-check.sh" 2>&1 | tee -a "$STEP_LOG"; then
                pass "Audit complete"
            else
                warn "Audit completed with warnings"
            fi
            ;;
        organize)
            log "📂 Step 2/5: Running file organizer..."
            if bash "$SCRIPT_DIR/organize.sh" 2>&1 | tee -a "$STEP_LOG"; then
                pass "Organize complete"
            else
                warn "Organize completed with warnings"
            fi
            ;;
        clean)
            log "🧹 Step 3/5: Running workspace cleaner..."
            CLEAN_CMD="python3 $SCRIPT_DIR/cleanup.py"
            if [ "$DRY_RUN" = "true" ]; then
                CLEAN_CMD="$CLEAN_CMD --json"
                log "(dry-run mode)"
            else
                CLEAN_CMD="$CLEAN_CMD --execute"
            fi
            if eval "$CLEAN_CMD" 2>&1 | tee -a "$STEP_LOG"; then
                pass "Clean complete"
            else
                warn "Clean completed with warnings"
            fi
            ;;
        archive)
            log "📦 Step 4/5: Running archiver..."
            if [ "$DRY_RUN" = "true" ]; then
                warn "Archive requires confirmation (skipped in dry-run)"
            else
                if bash "$SCRIPT_DIR/archive.sh" 2>&1 | tee -a "$STEP_LOG"; then
                    pass "Archive complete"
                else
                    warn "Archive completed with warnings"
                fi
            fi
            ;;
        sync)
            log "☁️  Step 5/5: Running cloud sync (optional)..."
            # Sync is optional - don't count as failure if skipped
            if bash "$SCRIPT_DIR/sync.sh" 2>&1 | tee -a "$STEP_LOG"; then
                pass "Sync complete"
            else
                SYNC_EXIT=${PIPESTATUS[0]}
                if [ $SYNC_EXIT -eq 0 ]; then
                    pass "Sync skipped (gog not configured)"
                else
                    warn "Sync completed with warnings"
                fi
            fi
            ;;
        *)
            fail "Unknown step: $step"
            FAILED=$((FAILED + 1))
            ;;
    esac
done

echo "" | tee -a "$STEP_LOG"
echo "========================================" | tee -a "$STEP_LOG"
echo "🏁 Pipeline finished: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$STEP_LOG"
echo "   Log: $STEP_LOG" | tee -a "$STEP_LOG"
echo "========================================" | tee -a "$STEP_LOG"

if [ $FAILED -gt 0 ]; then
    fail "$FAILED step(s) failed"
    exit 1
fi

pass "All steps completed successfully"
