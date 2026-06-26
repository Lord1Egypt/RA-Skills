#!/usr/bin/env bash
#
# Telnyx Embeddings - Test Script
#
# Validates that the embeddings tool is correctly installed and configured.
#
# Usage: ./test.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}+${NC} $1"; }
log_err()  { echo -e "${RED}x${NC} $1"; }
log_warn() { echo -e "${YELLOW}!${NC} $1"; }
log_info() { echo -e "${BLUE}i${NC} $1"; }

CHECKS_PASSED=0
CHECKS_FAILED=0

echo ""
echo "Telnyx Embeddings - Test"
echo "========================"
echo ""

# 1. Python 3 installed
log_info "Checking Python 3..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        log_ok "Python $python_version"
        ((CHECKS_PASSED++))
    else
        log_err "Python 3.8+ required, found $python_version"
        ((CHECKS_FAILED++))
    fi
else
    log_err "Python 3 not found"
    ((CHECKS_FAILED++))
fi

# 2. Scripts have valid syntax
log_info "Checking script syntax..."
syntax_ok=true
for py_file in "$SCRIPT_DIR"/*.py; do
    if [[ -f "$py_file" ]]; then
        if python3 -c "import py_compile; py_compile.compile('$py_file', doraise=True)" 2>/dev/null; then
            log_ok "$(basename "$py_file") syntax OK"
        else
            log_err "$(basename "$py_file") has syntax errors"
            syntax_ok=false
        fi
    fi
done
if $syntax_ok; then
    ((CHECKS_PASSED++))
else
    ((CHECKS_FAILED++))
fi

# 3. TELNYX_API_KEY accessible
log_info "Checking API key..."
API_KEY="${TELNYX_API_KEY:-}"
if [[ -z "$API_KEY" ]] && [[ -f "$SCRIPT_DIR/.env" ]]; then
    API_KEY=$(grep -E '^TELNYX_API_KEY=' "$SCRIPT_DIR/.env" 2>/dev/null | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'" || true)
fi

if [[ -n "$API_KEY" ]]; then
    log_ok "TELNYX_API_KEY found"
    ((CHECKS_PASSED++))
else
    log_err "TELNYX_API_KEY not found (set env var or create .env file)"
    ((CHECKS_FAILED++))
fi

# 4. Config file parseable
log_info "Checking config.json..."
if [[ -f "$SCRIPT_DIR/config.json" ]]; then
    if python3 -c "import json; json.load(open('$SCRIPT_DIR/config.json'))" 2>/dev/null; then
        log_ok "config.json valid"
        ((CHECKS_PASSED++))
    else
        log_err "config.json has invalid JSON"
        ((CHECKS_FAILED++))
    fi
else
    log_err "config.json not found"
    ((CHECKS_FAILED++))
fi

# 5. API connectivity test
if [[ -n "$API_KEY" ]]; then
    log_info "Testing API connectivity..."

    response=$(curl -s -w "%{http_code}" -o /dev/null \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        "https://api.telnyx.com/v2/ai/embeddings/similarity-search" \
        -d '{"bucket_name":"test-nonexistent-embeddings-check","query":"test","num_docs":1}' \
        2>/dev/null || echo "000")

    if [[ "$response" =~ ^[2-4][0-9][0-9]$ ]]; then
        log_ok "API responding (HTTP $response)"
        ((CHECKS_PASSED++))
    else
        log_err "API not reachable (HTTP $response)"
        ((CHECKS_FAILED++))
    fi
else
    log_warn "Skipping API test (no API key)"
fi

# Summary
echo ""
echo "========================"
echo ""
if [[ $CHECKS_FAILED -eq 0 ]]; then
    log_ok "All tests passed ($CHECKS_PASSED/$CHECKS_PASSED)"
    exit 0
else
    log_err "$CHECKS_FAILED test(s) failed, $CHECKS_PASSED passed"
    exit 1
fi
