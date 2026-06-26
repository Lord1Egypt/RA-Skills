#!/bin/bash
# Installation Verification Script
# Research Analyst v1.4.0 (Minimal Bundle)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

echo "=========================================="
echo "Research Analyst Installation Verification"
echo "v1.4.0 (Minimal Bundle)"
echo "=========================================="
echo ""

# Check 1: Python environment
echo "1. Checking Python environment..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo -e "${GREEN}   ✓ Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}   ✗ Python 3 not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check 2: Verify requirements.txt
echo "2. Verifying requirements.txt..."
if [ -f requirements.txt ]; then
    echo -e "${GREEN}   ✓ requirements.txt found${NC}"
    DEP_COUNT=$(grep -c "==" requirements.txt || echo 0)
    if [ "$DEP_COUNT" -gt 0 ]; then
        echo -e "${GREEN}   ✓ Contains $DEP_COUNT pinned dependencies${NC}"
    else
        echo -e "${YELLOW}   ⚠ No pinned dependencies found${NC}"
        WARNINGS=$((WARNINGS + 1))
    fi
else
    echo -e "${RED}   ✗ requirements.txt not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

# Check 3: Verify key files
echo "3. Verifying key files..."
for file in "scripts/stock_analyzer.py" "scripts/portfolio_manager.py" \
            "scripts/dividend_analyzer.py" "scripts/cn_stock_quotes.py" \
            "scripts/cn_market_rankings.py" "skill.md" "README.md"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}   ✓ $file${NC}"
    else
        echo -e "${RED}   ✗ $file missing${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

# Check 4: Scan for suspicious patterns
echo "4. Scanning for suspicious patterns..."
SUSPICIOUS=0

if [ -d scripts/ ]; then
    # Check for eval/exec
    EVAL_COUNT=$(grep -r "eval(" scripts/ 2>/dev/null | grep -v ".pyc\|\.eval()" | wc -l)
    [ "$EVAL_COUNT" -gt 0 ] && SUSPICIOUS=$((SUSPICIOUS + 1))

    # Check for subprocess
    SUBPROCESS_COUNT=$(grep -r "subprocess\|os.system" scripts/ 2>/dev/null | grep -v ".pyc" | wc -l)
    [ "$SUBPROCESS_COUNT" -gt 0 ] && SUSPICIOUS=$((SUSPICIOUS + 1))

    # Check for POST requests
    POST_COUNT=$(grep -ri "requests.post\|method.*post" scripts/ 2>/dev/null | grep -v ".pyc" | wc -l)
    [ "$POST_COUNT" -gt 0 ] && SUSPICIOUS=$((SUSPICIOUS + 1))
fi

if [ "$SUSPICIOUS" -eq 0 ]; then
    echo -e "${GREEN}   ✓ No suspicious patterns${NC}"
else
    echo -e "${YELLOW}   ⚠ Found $SUSPICIOUS pattern types${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Check 5: Verify script count
echo "5. Verifying script count..."
SCRIPT_COUNT=$(find scripts/ -name "*.py" 2>/dev/null | wc -l)
if [ "$SCRIPT_COUNT" -eq 5 ]; then
    echo -e "${GREEN}   ✓ 5 core scripts present${NC}"
else
    echo -e "${YELLOW}   ⚠ Expected 5 scripts, found $SCRIPT_COUNT${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

# Summary
echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo "Errors:   $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ "$ERRORS" -eq 0 ]; then
    echo -e "${GREEN}✓ VERIFICATION PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ VERIFICATION FAILED${NC}"
    exit 1
fi
