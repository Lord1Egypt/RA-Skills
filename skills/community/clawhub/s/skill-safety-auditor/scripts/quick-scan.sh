#!/bin/bash
#
# quick-scan.sh - Quick security scan for skills
# Usage: ./quick-scan.sh <skill-path>
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

TARGET_SKILL="$1"

if [[ -z "$TARGET_SKILL" ]]; then
    echo "Usage: $0 <skill-path>"
    exit 1
fi

if [[ ! -d "$TARGET_SKILL" ]]; then
    echo "❌ Error: Skill directory not found: $TARGET_SKILL"
    exit 1
fi

echo "🔍 Quick Security Scan: $(basename "$TARGET_SKILL")"
echo "================================"

# Quick checks
echo "Checking for SKILL.md..."
if [[ -f "$TARGET_SKILL/SKILL.md" ]]; then
    echo "✅ SKILL.md exists"
else
    echo "❌ SKILL.md missing"
fi

echo ""
echo "Checking for secrets..."
SECRETS=$(grep -rn -E "api[_-]?key.*=.*['\"][a-zA-Z0-9]{16,}['\"]|password.*=.*['\"][^'\"]+['\"]|token.*=.*['\"][a-zA-Z0-9]{20,}['\"]" "$TARGET_SKILL" --include="*.js" --include="*.ts" --include="*.sh" 2>/dev/null | head -5 || true)
if [[ -n "$SECRETS" ]]; then
    echo "⚠️  Potential secrets found:"
    echo "$SECRETS"
else
    echo "✅ No obvious secrets detected"
fi

echo ""
echo "Checking for eval..."
EVAL=$(grep -rn "eval(" "$TARGET_SKILL" --include="*.js" --include="*.ts" 2>/dev/null | head -5 || true)
if [[ -n "$EVAL" ]]; then
    echo "⚠️  eval() found:"
    echo "$EVAL"
else
    echo "✅ No eval() detected"
fi

echo ""
echo "Checking for HTTP URLs..."
HTTP=$(grep -rn "http://" "$TARGET_SKILL" --include="*.js" --include="*.ts" --include="*.sh" 2>/dev/null | grep -v "localhost" | grep -v "127.0.0.1" | head -5 || true)
if [[ -n "$HTTP" ]]; then
    echo "⚠️  HTTP URLs found:"
    echo "$HTTP"
else
    echo "✅ No insecure HTTP URLs"
fi

echo ""
echo "================================"
echo "Quick scan complete"
