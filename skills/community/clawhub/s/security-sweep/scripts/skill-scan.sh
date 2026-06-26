#!/usr/bin/env bash
#
# skill-scan.sh — Scan a single skill directory
# Part of security-sweep skill
#
# Usage:
#   bash skill-scan.sh --skill /path/to/skill
#

set -euo pipefail

SKILL_PATH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skill) SKILL_PATH="$2"; shift 2 ;;
        -h|--help) echo "Usage: skill-scan.sh --skill /path/to/skill"; exit 0 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

[[ -z "$SKILL_PATH" ]] && { echo "Error: --skill required"; exit 1; }
[[ ! -d "$SKILL_PATH" ]] && { echo "Error: $SKILL_PATH not found"; exit 1; }

skill_name=$(basename "$SKILL_PATH")
echo "Scanning skill: $skill_name"

# ── Secret patterns ─────────────────────────────────────────────────────────
echo ""
echo "── Secrets ─────────────────────────────────────────────────────────────"
secretFindings=$(grep -rEn \
    "api[_-]?key|token|password|secret|credential|Bearer" \
    "$SKILL_PATH" \
    --include="*.js" --include="*.ts" --include="*.sh" --include="*.py" \
    --include="*.json" \
    -l 2>/dev/null | grep -v node_modules | grep -v "\.git" || true)

if [[ -n "$secretFindings" ]]; then
    echo "  🔴 Found:"
    for f in $secretFindings; do echo "    $f"; done
else
    echo "  🟢 None found"
fi

# ── Dangerous exec ────────────────────────────────────────────────────────────
echo ""
echo "── Dangerous Exec ──────────────────────────────────────────────────────"
execFindings=$(grep -rEn \
    "exec\s*\(|spawn\s*\(|eval\s*\(|child_process|bash\s+-c|system\s*\(|shell\s*:\s*true" \
    "$SKILL_PATH" \
    --include="*.js" --include="*.ts" --include="*.sh" \
    -l 2>/dev/null | grep -v node_modules | grep -v "\.git" || true)

if [[ -n "$execFindings" ]]; then
    echo "  🟠 Found:"
    for f in $execFindings; do echo "    $f"; done
else
    echo "  🟢 None found"
fi

# ── Shell injection ──────────────────────────────────────────────────────────
echo ""
echo "── Shell Injection Surfaces ────────────────────────────────────────────"
injectionFindings=$(grep -rEn \
    '"\$.*"|`\$[^`]+`|\$\{[^}]+\}' \
    "$SKILL_PATH" \
    --include="*.js" --include="*.ts" --include="*.sh" \
    -l 2>/dev/null | grep -v node_modules | grep -v "\.git" || true)

if [[ -n "$injectionFindings" ]]; then
    echo "  🟡 Found (unverified):"
    for f in $injectionFindings; do echo "    $f"; done
else
    echo "  🟢 None found"
fi

# ── Network egress ────────────────────────────────────────────────────────────
echo ""
echo "── Network Egress ──────────────────────────────────────────────────────"
netFindings=$(grep -rEn \
    "https?://|curl |wget |fetch\(|axios\(" \
    "$SKILL_PATH" \
    --include="*.js" --include="*.ts" --include="*.sh" \
    -l 2>/dev/null | grep -v node_modules | grep -v "\.git" || true)

if [[ -n "$netFindings" ]]; then
    echo "  ℹ️  Found:"
    for f in $netFindings; do echo "    $f"; done
else
    echo "  🟢 None found"
fi

echo ""
echo "Done."
