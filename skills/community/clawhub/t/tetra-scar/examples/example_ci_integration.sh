#!/usr/bin/env bash
# example_ci_integration.sh -- Add scar-code-review to your CI pipeline.
#
# Usage (in GitHub Actions, GitLab CI, etc.):
#   bash example_ci_integration.sh
#
# What it does:
#   1. Gets the list of changed files (git diff)
#   2. Runs scar_code_review.py on each changed file
#   3. If CRITICAL findings exist, fails the build
#   4. Records new findings as scars so future reviews catch them
#
# Requirements: python3, git
# ---------------------------------------------------------------------------

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REVIEW_SCRIPT="${SCRIPT_DIR}/../../tetra-scar-code-review/scar_code_review.py"
SCAR_FILE="${SCAR_FILE:-./review_scars.jsonl}"

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "============================================"
echo "  scar-code-review CI integration"
echo "============================================"
echo ""

# ---------------------------------------------------------------------------
# Step 1: Find changed files
# ---------------------------------------------------------------------------
echo "Step 1: Finding changed files..."

# In CI, compare against the base branch. Locally, compare against HEAD~1.
BASE_REF="${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-${GITHUB_BASE_REF:-HEAD~1}}"
CHANGED_FILES=$(git diff --name-only --diff-filter=ACMR "${BASE_REF}" -- '*.py' '*.js' '*.ts' '*.go' '*.rb' 2>/dev/null || echo "")

if [ -z "$CHANGED_FILES" ]; then
    echo -e "${GREEN}No changed source files to review.${NC}"
    exit 0
fi

FILE_COUNT=$(echo "$CHANGED_FILES" | wc -l | tr -d ' ')
echo "  Found ${FILE_COUNT} changed file(s)."
echo ""

# ---------------------------------------------------------------------------
# Step 2: Review each file
# ---------------------------------------------------------------------------
echo "Step 2: Running scar-code-review..."
echo ""

TOTAL_FINDINGS=0
CRITICAL_COUNT=0
FAILED_FILES=""

while IFS= read -r file; do
    [ -z "$file" ] && continue
    [ ! -f "$file" ] && continue

    echo "  Reviewing: ${file}"

    # Run review, capture output and exit code
    OUTPUT=$(python3 "$REVIEW_SCRIPT" --scar-file "$SCAR_FILE" review "$file" 2>&1) || true
    EXIT_CODE=${PIPESTATUS[0]:-0}

    if echo "$OUTPUT" | grep -q "No findings"; then
        echo -e "    ${GREEN}clean${NC}"
        continue
    fi

    # Count findings by severity
    CRITS=$(echo "$OUTPUT" | grep -c '^\[critical\]' || true)
    HIGHS=$(echo "$OUTPUT" | grep -c '^\[high\]' || true)
    WARNS=$(echo "$OUTPUT" | grep -c '^\[warning\]' || true)

    CRITICAL_COUNT=$((CRITICAL_COUNT + CRITS))
    TOTAL_FINDINGS=$((TOTAL_FINDINGS + CRITS + HIGHS + WARNS))

    if [ "$CRITS" -gt 0 ]; then
        echo -e "    ${RED}${CRITS} critical, ${HIGHS} high, ${WARNS} warning${NC}"
        FAILED_FILES="${FAILED_FILES}\n    - ${file} (${CRITS} critical)"
    elif [ "$HIGHS" -gt 0 ]; then
        echo -e "    ${YELLOW}${HIGHS} high, ${WARNS} warning${NC}"
    else
        echo -e "    ${YELLOW}${WARNS} warning(s)${NC}"
    fi

done <<< "$CHANGED_FILES"

echo ""

# ---------------------------------------------------------------------------
# Step 3: Record new findings as scars for next time
# ---------------------------------------------------------------------------
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "Step 3: Recording critical findings as scars..."

    # In a real pipeline you'd parse the specific findings.
    # This records a summary scar so the reflex arc catches similar code.
    python3 "$REVIEW_SCRIPT" --scar-file "$SCAR_FILE" record-miss \
        --what-missed "CI found ${CRITICAL_COUNT} critical issue(s) in PR" \
        --pattern "TODO_REPLACE_WITH_SPECIFIC_REGEX" \
        --severity critical \
        2>/dev/null || true

    echo "  Scar recorded. Future reviews will catch similar patterns."
    echo ""
fi

# ---------------------------------------------------------------------------
# Step 4: Verdict
# ---------------------------------------------------------------------------
echo "============================================"
echo "  RESULTS"
echo "============================================"
echo "  Total findings: ${TOTAL_FINDINGS}"
echo "  Critical:       ${CRITICAL_COUNT}"

if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo ""
    echo -e "  ${RED}BUILD FAILED${NC} -- ${CRITICAL_COUNT} critical finding(s):"
    echo -e "${FAILED_FILES}"
    echo ""
    echo "  Fix critical issues and push again."
    echo "  The scar file remembers -- these patterns will be caught faster next time."
    exit 1
else
    echo ""
    echo -e "  ${GREEN}BUILD PASSED${NC}"
    if [ "$TOTAL_FINDINGS" -gt 0 ]; then
        echo "  (${TOTAL_FINDINGS} non-critical findings -- consider fixing)"
    fi
    exit 0
fi
