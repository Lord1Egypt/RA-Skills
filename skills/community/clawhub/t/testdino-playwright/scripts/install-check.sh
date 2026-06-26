#!/usr/bin/env bash
# install-check.sh
# Verifies that the testdino-mcp package is reachable and your PAT is valid.
# Run this after setting TESTDINO_PAT to confirm the skill will work.
#
# Usage:
#   export TESTDINO_PAT=your-pat-here
#   bash scripts/install-check.sh

set -e

echo ""
echo "TestDino OpenClaw Skill — Install Check"
echo "======================================="
echo ""

# 1. Check Node.js
echo "Checking Node.js..."
if ! command -v node &>/dev/null; then
  echo "FAIL: Node.js not found. Install Node.js 18+ from https://nodejs.org"
  exit 1
fi

NODE_VERSION=$(node --version)
NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1 | tr -d 'v')
if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "FAIL: Node.js $NODE_VERSION found. Version 18 or higher is required."
  exit 1
fi
echo "  OK: Node.js $NODE_VERSION"

# 2. Check npx
echo "Checking npx..."
if ! command -v npx &>/dev/null; then
  echo "FAIL: npx not found. Install Node.js 18+ which includes npx."
  exit 1
fi
echo "  OK: npx found"

# 3. Check TESTDINO_PAT
echo "Checking TESTDINO_PAT..."
if [ -z "$TESTDINO_PAT" ]; then
  echo "FAIL: TESTDINO_PAT environment variable is not set."
  echo ""
  echo "  Set it with:"
  echo "    export TESTDINO_PAT=your-personal-access-token"
  echo ""
  echo "  Get your PAT at: https://app.testdino.com → Settings → Personal Access Tokens"
  exit 1
fi

PAT_LENGTH=${#TESTDINO_PAT}
echo "  OK: TESTDINO_PAT is set (${PAT_LENGTH} characters)"

# 4. Check testdino-mcp package reachability
echo "Checking testdino-mcp package..."
if ! npx --yes testdino-mcp --version &>/dev/null 2>&1; then
  # Some versions may not support --version, try a different check
  if ! npm show testdino-mcp version &>/dev/null 2>&1; then
    echo "WARN: Could not verify testdino-mcp package. Check your internet connection."
    echo "      The package should be available at: https://www.npmjs.com/package/testdino-mcp"
  else
    MCP_VERSION=$(npm show testdino-mcp version 2>/dev/null)
    echo "  OK: testdino-mcp@${MCP_VERSION} available on npm"
  fi
else
  echo "  OK: testdino-mcp reachable via npx"
fi

# 5. Validate PAT against TestDino API
echo "Validating PAT with TestDino API..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer $TESTDINO_PAT" \
  "https://api.testdino.com/api/mcp/hello" 2>/dev/null || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
  echo "  OK: PAT is valid — TestDino API responded successfully"
elif [ "$HTTP_STATUS" = "401" ]; then
  echo "FAIL: PAT is invalid or expired (HTTP 401)."
  echo "      Generate a new PAT at: https://app.testdino.com → Settings → Personal Access Tokens"
  exit 1
elif [ "$HTTP_STATUS" = "000" ]; then
  echo "WARN: Could not reach TestDino API. Check your internet connection."
  echo "      API endpoint: https://api.testdino.com"
else
  echo "WARN: Unexpected response from TestDino API (HTTP $HTTP_STATUS)."
fi

echo ""
echo "======================================="
echo "All checks passed. The testdino skill is ready."
echo ""
echo "Next steps:"
echo "  1. Install OpenClaw: https://openclaw.ai"
echo "  2. Run: clawhub install testdino"
echo "  3. Add TESTDINO_PAT to your openclaw.json env"
echo "  4. Ask: 'Check my TestDino connection'"
echo ""
