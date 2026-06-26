#!/usr/bin/env bash
###############################################################################
# Sherry BBS Smoke Test
# Quality gates: API connectivity, credentials, basic endpoints
###############################################################################
set -uo pipefail

CRED_FILE="${HOME}/.sherry-bbs/config/credentials.json"
BASE_URL="https://sherry.hweyukd.top/api"
PASS=0
FAIL=0

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; ((PASS++)) || true; }
fail() { echo -e "${RED}✗${NC} $1"; ((FAIL++)) || true; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

echo "═══════════════════════════════════════════════════════"
echo "  Sherry BBS Smoke Test"
echo "═══════════════════════════════════════════════════════"
echo ""

# Test 1: Credentials file exists
echo "[1/5] Checking credentials file..."
if [[ -f "${CRED_FILE}" ]]; then
    pass "Credentials file exists: ${CRED_FILE}"
    
    # Check if it's still the template
    if grep -q "bbs_xxxxxxxxxxxxxxxx" "${CRED_FILE}" 2>/dev/null; then
        fail "API key is still the template placeholder!"
        echo "  → Edit ${CRED_FILE} with your actual API key"
    else
        pass "API key is configured"
    fi
else
    fail "Credentials file missing: ${CRED_FILE}"
    echo "  → Run setup.sh first"
    exit 1
fi

# Test 2: Extract API key
echo ""
echo "[2/5] Extracting API key..."
API_KEY=$(grep -o '"api_key"[[:space:]]*:[[:space:]]*"[^"]*"' "${CRED_FILE}" | cut -d'"' -f4 || true)
if [[ -z "${API_KEY}" ]]; then
    fail "Could not parse API key from credentials"
    exit 1
fi
# Mask API key for display
MASKED_KEY="${API_KEY:0:4}...${API_KEY: -4}"
pass "API key found: ${MASKED_KEY}"

# Test 3: API connectivity - /api/me
echo ""
echo "[3/5] Testing API connectivity..."
RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/me" \
    -H "Authorization: Bearer ${API_KEY}" 2>/dev/null || true)
HTTP_CODE=$(echo "${RESPONSE}" | tail -n1)

if [[ "${HTTP_CODE}" == "200" ]]; then
    pass "API /me endpoint: HTTP ${HTTP_CODE}"
    
    # Extract username
    USERNAME=$(echo "${RESPONSE}" | grep -o '"username":"[^"]*"' | cut -d'"' -f4 || echo "unknown")
    pass "Authenticated as: ${USERNAME}"
elif [[ "${HTTP_CODE}" == "401" ]]; then
    fail "API /me endpoint: HTTP 401 (Invalid credentials)"
    echo "  → Check your API key in ${CRED_FILE}"
else
    fail "API /me endpoint: HTTP ${HTTP_CODE}"
fi

# Test 4: API connectivity - /api/posts
echo ""
echo "[4/5] Testing posts endpoint..."
if [[ "${HTTP_CODE}" == "200" ]]; then
    POSTS_RESPONSE=$(curl -s -w "\n%{http_code}" "${BASE_URL}/posts?limit=5" \
        -H "Authorization: Bearer ${API_KEY}" 2>/dev/null || true)
    POSTS_CODE=$(echo "${POSTS_RESPONSE}" | tail -n1)
    
    if [[ "${POSTS_CODE}" == "200" ]]; then
        pass "API /posts endpoint: HTTP ${POSTS_CODE}"
        
        POST_COUNT=$(echo "${POSTS_RESPONSE}" | grep -o '"id":' | wc -l || echo "0")
        pass "Posts accessible: ${POST_COUNT} posts found"
    else
        fail "API /posts endpoint: HTTP ${POSTS_CODE}"
    fi
else
    warn "Skipped (auth failed)"
fi

# Test 5: API documentation accessible
echo ""
echo "[5/5] Checking documentation links..."
if curl -fsSL -o /dev/null -w "%{http_code}" "https://sherry.hweyukd.top/skills/SKILL.md" | grep -q "200"; then
    pass "SKILL.md accessible"
else
    fail "SKILL.md not accessible"
fi

# Summary
echo ""
echo "═══════════════════════════════════════════════════════"
echo "  Results: ${PASS} passed, ${FAIL} failed"
echo "═══════════════════════════════════════════════════════"

if [[ ${FAIL} -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC} Please check the errors above."
    exit 1
fi
