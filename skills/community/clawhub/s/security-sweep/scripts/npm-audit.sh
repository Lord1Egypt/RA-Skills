#!/usr/bin/env bash
#
# npm-audit.sh — Run npm audit on all workspace skills with package.json
# Part of security-sweep skill
#
# Usage:
#   bash npm-audit.sh --workspace ~/.openclaw/workspace/skills
#

set -euo pipefail

WORKSPACE_DIR=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --workspace) WORKSPACE_DIR="$2"; shift 2 ;;
        -h|--help) echo "Usage: npm-audit.sh --workspace DIR"; exit 0 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

[[ -z "$WORKSPACE_DIR" ]] && { echo "Error: --workspace required"; exit 1; }
[[ ! -d "$WORKSPACE_DIR" ]] && { echo "Error: $WORKSPACE_DIR not found"; exit 1; }

echo "Scanning workspace skills for npm vulnerabilities..."
echo ""

total_issues=0

for skill_path in "$WORKSPACE_DIR"/*/; do
    [[ ! -d "$skill_path" ]] && continue
    skill_name=$(basename "$skill_path")

    if [[ ! -f "$skill_path/package.json" ]]; then
        continue
    fi

    echo "Checking $skill_name..."

    if [[ ! -d "$skill_path/node_modules" ]]; then
        echo "  ⚠️  node_modules missing (run: npm install in $skill_path)"
        continue
    fi

    audit_output=$(cd "$skill_path" && npm audit --omit=dev --quiet 2>&1 || true)

    if echo "$audit_output" | grep -q "vulnerab"; then
        total_issues=$((total_issues + 1))
        echo "  🔴 Vulnerabilities found:"
        echo "$audit_output" | head -10 | sed 's/^/    /'
    else
        echo "  🟢 No vulnerabilities"
    fi
    echo ""
done

echo "── Summary ──────────────────────────────────────────────────────────────"
if [[ $total_issues -eq 0 ]]; then
    echo "  🟢 All workspace skills passed npm audit"
else
    echo "  🔴 $total_issues skill(s) have npm vulnerabilities — run npm audit manually to review"
fi
