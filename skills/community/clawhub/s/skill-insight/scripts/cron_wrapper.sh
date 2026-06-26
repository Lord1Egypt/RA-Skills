#!/bin/bash
# cron_wrapper.sh - Daily cron job wrapper for skill-insight
# Sets SKILL_USAGE_TRACKER_DIR so Python scripts resolve paths correctly.
#
# Add to crontab -e:
#   0 9 * * * cd ~/.openclaw/workspace/skills/skill-insight && bash scripts/cron_wrapper.sh >> ~/.local/log/skill-insight.log 2>&1

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export SKILL_USAGE_TRACKER_DIR="$SKILL_DIR"

LOG_DIR="${HOME}/.local/log"
mkdir -p "$LOG_DIR" 2>/dev/null || LOG_DIR="$HOME"
LOG_FILE="${LOG_DIR}/skill-insight.log"
SCRIPTS_DIR="${SKILL_DIR}/scripts"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "=== Skill Insight Cron Started ==="

log "Generating daily usage report..."
REPORT_OUTPUT=$(bash "${SCRIPTS_DIR}/report.sh" --period today 2>&1)
echo "$REPORT_OUTPUT" | head -20 >> "$LOG_FILE"

log "Running unused skill analysis..."
ANALYSIS_OUTPUT=$(bash "${SCRIPTS_DIR}/analyze.sh" --period 7 2>&1)
UNINSTALL_COUNT=$(echo "$ANALYSIS_OUTPUT" | grep -c "建议卸载")
if [ "$UNINSTALL_COUNT" -gt 0 ]; then
    echo "⚠️ Found $UNINSTALL_COUNT skills recommended for uninstall" >> "$LOG_FILE"
fi

log "=== Skill Insight Cron Finished ==="
echo "" >> "$LOG_FILE"
