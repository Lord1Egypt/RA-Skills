#!/usr/bin/env bash
# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: .learnings/*.md
# Local files written: none
# Purpose: Audit learnings directory for format issues, sensitive data leaks, and consistency problems.

set -euo pipefail

LEARNINGS_DIR="${LEARNINGS_DIR:-.learnings}"
WARN_COUNT=0
ERROR_COUNT=0

echo "=== Safe Self-Improvement Audit ==="
echo "Directory: $LEARNINGS_DIR"
echo ""

# 1. Check if directory exists
if [ ! -d "$LEARNINGS_DIR" ]; then
    echo "⚠️  No .learnings/ directory found. Run initialization first."
    exit 0
fi

# 2. Check for sensitive data in all learnings files
echo "--- [1/5] Sensitive Data Scan ---"
SENSITIVE_PATTERNS=(
    "(ghp_|gho_|github_pat_|sk-|AKIA|xox[baprs])[a-zA-Z0-9]{10,}"
    "-----BEGIN (RSA |EC |DSA |OPENSSH )PRIVATE KEY-----"
    "1[3-9][0-9]{9}"
    "192\.168\.[0-9]+\.[0-9]+|10\.[0-9]+\.[0-9]+\.[0-9]+"
)

for file in "$LEARNINGS_DIR"/*.md; do
    [ -f "$file" ] || continue
    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
        if grep -HiE "$pattern" "$file" > /dev/null 2>&1; then
            echo "🚫 $file: sensitive pattern detected (redacted in output)"
            ERROR_COUNT=$((ERROR_COUNT + 1))
        fi
    done
done

if [ "$ERROR_COUNT" -eq 0 ]; then
    echo "✅ No sensitive data detected in learnings files."
fi
echo ""

# 3. Check format consistency (each entry should have Status, Priority, Logged)
echo "--- [2/5] Format Consistency ---"
for file in "$LEARNINGS_DIR"/*.md; do
    [ -f "$file" ] || continue
    BASENAME=$(basename "$file")
    if ! grep -q "^\*\*Status\*\*:" "$file" 2>/dev/null; then
        echo "⚠️  $BASENAME: missing Status field in some entries"
        WARN_COUNT=$((WARN_COUNT + 1))
    fi
    if ! grep -q "^\*\*Priority\*\*:" "$file" 2>/dev/null; then
        echo "⚠️  $BASENAME: missing Priority field in some entries"
        WARN_COUNT=$((WARN_COUNT + 1))
    fi
    if ! grep -q "^\*\*Logged\*\*:" "$file" 2>/dev/null; then
        echo "⚠️  $BASENAME: missing Logged field in some entries"
        WARN_COUNT=$((WARN_COUNT + 1))
    fi
done
[ "$WARN_COUNT" -eq 0 ] && echo "✅ Format fields present."
echo ""

# 4. Check for orphaned See Also links (point to non-existent entries)
echo "--- [3/5] Orphaned See Also Links ---"
ORPHANS=0
for file in "$LEARNINGS_DIR"/*.md; do
    [ -f "$file" ] || continue
    IDS=$(grep -h "^## \[" "$file" 2>/dev/null | sed 's/.*\[\(.*\)\].*/\1/' | tr -d ' ')
    LINKS=$(grep -oh "See Also: [A-Z]*-[0-9]*-[A-Z0-9]*" "$file" 2>/dev/null | sed 's/See Also: //' | tr -d ' ')
    for link in $LINKS; do
        if ! echo "$IDS" | grep -q "^${link}$"; then
            echo "⚠️  Orphaned link: $link (referenced but not found)"
            ORPHANS=$((ORPHANS + 1))
        fi
    done
done
[ "$ORPHANS" -eq 0 ] && echo "✅ All See Also links valid."
echo ""

# 5. Check file sizes (warn if any file is too large)
echo "--- [4/5] File Size Check ---"
for file in "$LEARNINGS_DIR"/*.md; do
    [ -f "$file" ] || continue
    LINES=$(wc -l < "$file")
    BASENAME=$(basename "$file")
    if [ "$LINES" -gt 500 ]; then
        echo "📄 $BASENAME: $LINES lines — consider running context compression."
        WARN_COUNT=$((WARN_COUNT + 1))
    else
        echo "✅ $BASENAME: $LINES lines (OK)"
    fi
done
echo ""

# 6. Summary
echo "=== Audit Summary ==="
echo "Errors: $ERROR_COUNT"
echo "Warnings: $WARN_COUNT"

if [ "$ERROR_COUNT" -gt 0 ]; then
    echo "Status: FAILED — fix errors before continuing."
    exit 1
elif [ "$WARN_COUNT" -gt 0 ]; then
    echo "Status: PASSED with warnings — review recommended."
    exit 0
else
    echo "Status: CLEAN — no issues found."
    exit 0
fi
