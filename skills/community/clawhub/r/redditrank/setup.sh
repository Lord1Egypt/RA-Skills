#!/usr/bin/env bash
# RedditRank — Setup: install Python deps and register for an API key.
# Run once after installing the skill.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_BASE="https://clawagents.dev/reddit-rank/v1"
RR_DIR="$HOME/.redditrank"
RR_CONFIG="$RR_DIR/config.json"
VENV_DIR="$SCRIPT_DIR/.venv"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}RedditRank${NC} Setup"
echo -e "Find Reddit threads ranking on Google. Draft AI replies. Get organic traffic."
echo ""

# ── 0. Check prerequisites ──────────────────────────────────────────────────

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    echo -e "${RED}Missing required command: $1${NC}"
    echo -e "Install it first:  ${BOLD}$2${NC}"
    exit 1
  fi
}

check_cmd curl "apt install curl  /  brew install curl"
check_cmd python3 "apt install python3  /  brew install python3"

PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
  echo -e "${RED}Python 3.10+ required (found $PY_VER)${NC}"
  exit 1
fi
echo -e "  ${DIM}Python $PY_VER${NC}"

# ── 1. Create venv + install dependencies ───────────────────────────────────

if [ ! -d "$VENV_DIR" ]; then
  echo -e "  Creating virtual environment..."
  python3 -m venv "$VENV_DIR" || {
    echo -e "${RED}  Failed to create venv. Install python3-venv manually.${NC}"
    exit 1
  }
fi

source "$VENV_DIR/bin/activate"
echo -e "  ${DIM}venv: $VENV_DIR${NC}"

echo -e "  Installing dependencies..."
pip install -q --upgrade pip 2>/dev/null || true
pip install -q -r "$SCRIPT_DIR/requirements.txt"
echo -e "  ${GREEN}Dependencies installed${NC}"
echo ""

# ── 2. Check for existing API key ───────────────────────────────────────────

HAS_JQ=false
command -v jq &>/dev/null && HAS_JQ=true

parse_json() {
  local json="$1" field="$2"
  if $HAS_JQ; then
    echo "$json" | jq -r ".$field // empty"
  else
    echo "$json" | grep -o "\"$field\":\"[^\"]*\"" | cut -d'"' -f4
  fi
}

EXISTING_KEY=""

if [ -n "${REDDITRANK_API_KEY:-}" ]; then
  EXISTING_KEY="$REDDITRANK_API_KEY"
fi

if [ -z "$EXISTING_KEY" ] && [ -f "$RR_CONFIG" ]; then
  if $HAS_JQ; then
    EXISTING_KEY=$(jq -r '.api_key // empty' "$RR_CONFIG" 2>/dev/null || true)
  else
    EXISTING_KEY=$(grep -o '"api_key":"[^"]*"' "$RR_CONFIG" 2>/dev/null | cut -d'"' -f4 || true)
  fi
fi

if [ -n "$EXISTING_KEY" ]; then
  echo -e "  Found existing API key. Validating..."
  VALIDATE=$(curl -s -X POST "$API_BASE/auth/validate" \
    -H "Content-Type: application/json" \
    -d "{\"token\": \"$EXISTING_KEY\"}" 2>/dev/null || echo "{}")

  if echo "$VALIDATE" | grep -q '"valid":true'; then
    TIER=$(parse_json "$VALIDATE" "tier")
    echo -e "  ${GREEN}Key is valid. Tier: ${BOLD}$TIER${NC}"
    echo ""
    echo -e "${GREEN}${BOLD}Setup complete.${NC}"
    echo -e "  Run:  ${CYAN}${BOLD}$SCRIPT_DIR/redditrank${NC}"
    echo ""
    exit 0
  else
    echo -e "${YELLOW}  Key is invalid. Registering a new one.${NC}"
    echo ""
  fi
fi

# ── 3. Register: email ──────────────────────────────────────────────────────

echo -e "${BOLD}Step 1/2:${NC} Enter your email to register"
echo -e "  ${DIM}(We'll send a 6-digit verification code)${NC}"
echo ""
read -rp "  Email: " EMAIL

if [ -z "$EMAIL" ]; then
  echo -e "${RED}No email provided. Exiting.${NC}"
  exit 1
fi

echo ""
echo -e "  Sending verification code to ${CYAN}$EMAIL${NC}..."

REGISTER_RESP=$(curl -s -X POST "$API_BASE/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\"}")

REG_ERROR=$(parse_json "$REGISTER_RESP" "error")
if [ -n "$REG_ERROR" ]; then
  REG_CODE=$(parse_json "$REGISTER_RESP" "code")
  if [ "$REG_CODE" = "EMAIL_ALREADY_REGISTERED" ]; then
    echo -e "${YELLOW}  This email already has an API key.${NC}"
    echo -e "  Check your inbox for your original key email, or contact support."
    exit 1
  fi
  echo -e "${RED}  Error: $REG_ERROR${NC}"
  exit 1
fi

echo -e "${GREEN}  Code sent.${NC} Check your inbox (and spam folder)."
echo ""

# ── 4. Register: verify code ────────────────────────────────────────────────

echo -e "${BOLD}Step 2/2:${NC} Enter the 6-digit code from your email"
echo ""
read -rp "  Code: " CODE

if [ -z "$CODE" ]; then
  echo -e "${RED}No code provided. Exiting.${NC}"
  exit 1
fi

echo ""
echo -e "  Verifying..."

VERIFY_RESP=$(curl -s -X POST "$API_BASE/auth/verify" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$EMAIL\", \"code\": \"$CODE\"}")

VER_ERROR=$(parse_json "$VERIFY_RESP" "error")
if [ -n "$VER_ERROR" ]; then
  echo -e "${RED}  Error: $VER_ERROR${NC}"
  echo -e "  Code may have expired. Run setup.sh again to get a new code."
  exit 1
fi

API_KEY=$(parse_json "$VERIFY_RESP" "api_key")
TIER=$(parse_json "$VERIFY_RESP" "tier")

if [ -z "$API_KEY" ]; then
  echo -e "${RED}  Failed to extract API key from response.${NC}"
  echo "  Raw response: $VERIFY_RESP"
  exit 1
fi

echo -e "${GREEN}${BOLD}  API key created.${NC}"
echo ""
echo -e "  Key:  ${CYAN}$API_KEY${NC}"
echo -e "  Tier: ${BOLD}${TIER:-free}${NC}"
echo ""

# ── 5. Save API key ─────────────────────────────────────────────────────────

mkdir -p "$RR_DIR"
if $HAS_JQ; then
  echo "{\"api_key\": \"$API_KEY\"}" | jq . > "$RR_CONFIG"
else
  echo "{\"api_key\": \"$API_KEY\"}" > "$RR_CONFIG"
fi
echo -e "  Saved to ${BOLD}$RR_CONFIG${NC}"
echo ""
echo -e "  ${DIM}You can also set it as an env var:${NC}"
echo -e "  ${DIM}export REDDITRANK_API_KEY=$API_KEY${NC}"

# ── Done ─────────────────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}${BOLD}Setup complete.${NC}"
echo ""
echo -e "  Run:  ${CYAN}${BOLD}$SCRIPT_DIR/redditrank${NC}"
echo ""
