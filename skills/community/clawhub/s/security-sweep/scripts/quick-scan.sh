#!/usr/bin/env bash
#
# quick-scan.sh — Fast security patterns scan for OpenClaw skills
# Part of security-sweep skill
#
# Usage:
#   bash quick-scan.sh --dir ~/.openclaw/workspace/skills
#

set -euo pipefail

SKILLS_DIR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir) SKILLS_DIR="$2"; shift 2 ;;
        -h|--help) echo "Usage: quick-scan.sh --dir DIR"; exit 0 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

[[ -z "$SKILLS_DIR" ]] && SKILLS_DIR="$HOME/.openclaw/workspace/skills"
[[ ! -d "$SKILLS_DIR" ]] && { echo "Error: $SKILLS_DIR not found"; exit 1; }

echo "Quick Scan — $SKILLS_DIR"
echo ""

total_critical=0
total_high=0

for skill_path in "$SKILLS_DIR"/*/; do
    [[ ! -d "$skill_path" ]] && continue
    skill_name=$(basename "$skill_path")

    critical=0
    high=0

    # ── Secret patterns (only key=value, skip tests and docs) ────────
    secret=$(grep -rEl \
        "(api[_-]?key|token|password|secret|credential)\s*[=:]\s*[\"'][^'\"]{8,}[\"']" \
        "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" --include="*.py" --include="*.json" \
        2>/dev/null | grep -v "/tests/" | grep -v "/node_modules/" || true)

    [[ -n "$secret" ]] && { critical=$((critical+1)); total_critical=$((total_critical+1)); }

    # ── Dangerous exec ───────────────────────────────────────────────
    exec_found=$(grep -rEl \
        "exec\s*\(|spawn\s*\(|eval\s*\(|child_process|bash\s+-c" \
        "$skill_path" \
        --include="*.js" --include="*.ts" --include="*.sh" \
        2>/dev/null | grep -v "/tests/" | grep -v "/node_modules/" || true)

    [[ -n "$exec_found" ]] && { high=$((high+1)); total_high=$((total_high+1)); }

    if [[ $critical -gt 0 || $high -gt 0 ]]; then
        echo "  $skill_name: 🔴 $critical 🟠 $high"
    else
        echo "  $skill_name: 🟢"
    fi
done

echo ""
echo "── Summary ──────────────────────────────────────────────"
echo "  🔴 CRITICAL: $total_critical"
echo "  🟠 HIGH:     $total_high"
echo ""
[[ $total_critical -eq 0 ]] && [[ $total_high -eq 0 ]] && echo "  🟢 All clear" || echo "  ⚠️  Review findings above"
