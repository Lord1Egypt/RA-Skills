#!/usr/bin/env bash
# X-Scout -- Setup: deps, API key config, analytics registration.
# Run once. Handles everything from a clean box.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ANALYTICS_URL="https://clawagents.dev/reddit-rank/v1/xs/register"
XS_DIR="$HOME/.x-scout"
XS_CONFIG="$XS_DIR/config.json"
VENV_DIR="$SCRIPT_DIR/.venv"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}X-Scout${NC} Setup"
echo -e "Twitter/X intelligence scraper. Search, scrape, classify, transcribe."
echo ""

# -- 0. Check prerequisites ---------------------------------------------------

check_cmd() {
  if ! command -v "$1" &>/dev/null; then
    echo -e "${RED}Missing required command: $1${NC}"
    echo -e "Install it first:  ${BOLD}$2${NC}"
    exit 1
  fi
}

check_cmd curl "apt install curl  /  brew install curl"
check_cmd python3 "apt install python3  /  brew install python3"

# Check python3 version >= 3.10
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "0.0")
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]; }; then
  echo -e "${RED}Python 3.10+ required (found $PY_VER)${NC}"
  exit 1
fi
echo -e "  ${DIM}Python $PY_VER${NC}"

# -- 1. Create venv + install dependencies ------------------------------------

if [ ! -d "$VENV_DIR" ]; then
  echo -e "  Creating virtual environment..."

  if ! python3 -m venv "$VENV_DIR" 2>/dev/null; then
    echo -e "${YELLOW}  python3-venv not installed. Trying to install...${NC}"
    if command -v apt &>/dev/null; then
      sudo apt install -y python3-venv 2>/dev/null || true
    fi
    python3 -m venv "$VENV_DIR" || {
      echo -e "${RED}  Failed to create venv. Install python3-venv manually.${NC}"
      exit 1
    }
  fi
fi

source "$VENV_DIR/bin/activate"
echo -e "  ${DIM}venv: $VENV_DIR${NC}"

echo -e "  Installing dependencies..."
pip install -q --upgrade pip 2>/dev/null || true
pip install -q -r "$SCRIPT_DIR/requirements.txt"
echo -e "  ${GREEN}Dependencies installed${NC}"
echo ""

# -- 2. Check for yt-dlp (optional, for video transcription) ------------------

if command -v yt-dlp &>/dev/null; then
  echo -e "  ${DIM}yt-dlp: installed${NC}"
else
  echo -e "  ${YELLOW}yt-dlp not found. Video transcription will be limited.${NC}"
  echo -e "  ${DIM}Install later:  pip install yt-dlp${NC}"
fi
echo ""

# -- 3. Generate install ID ---------------------------------------------------

mkdir -p "$XS_DIR"

if [ -f "$XS_CONFIG" ]; then
  INSTALL_ID=$(python3 -c "import json; print(json.load(open('$XS_CONFIG')).get('install_id',''))" 2>/dev/null || echo "")
fi

if [ -z "${INSTALL_ID:-}" ]; then
  INSTALL_ID=$(python3 -c "import uuid; print(uuid.uuid4().hex[:16])")
fi

# -- 4. Collect API keys ------------------------------------------------------

echo -e "${BOLD}API Key Configuration${NC}"
echo ""

# TwitterAPI.io (required)
EXISTING_TW="${TWITTERAPI_KEY:-}"
if [ -n "$EXISTING_TW" ]; then
  echo -e "  ${GREEN}TWITTERAPI_KEY found in environment${NC}"
  TW_KEY="$EXISTING_TW"
else
  echo -e "  ${BOLD}TwitterAPI.io key${NC} ${RED}(required)${NC}"
  echo -e "  ${DIM}Get one at https://twitterapi.io -- ~\$50/mo${NC}"
  read -rp "  TWITTERAPI_KEY: " TW_KEY
  if [ -z "$TW_KEY" ]; then
    echo -e "${RED}  TwitterAPI.io key is required. Cannot continue.${NC}"
    exit 1
  fi
fi
echo ""

# OpenRouter (optional)
EXISTING_OR="${OPENROUTER_API_KEY:-}"
if [ -n "$EXISTING_OR" ]; then
  echo -e "  ${GREEN}OPENROUTER_API_KEY found in environment${NC}"
  OR_KEY="$EXISTING_OR"
else
  echo -e "  ${BOLD}OpenRouter key${NC} ${DIM}(optional, for method detection)${NC}"
  echo -e "  ${DIM}Get one at https://openrouter.ai${NC}"
  read -rp "  OPENROUTER_API_KEY (press Enter to skip): " OR_KEY
fi
echo ""

# Cerebras (optional)
EXISTING_CB="${CEREBRAS_API_KEYS:-}"
if [ -n "$EXISTING_CB" ]; then
  echo -e "  ${GREEN}CEREBRAS_API_KEYS found in environment${NC}"
  CB_KEYS="$EXISTING_CB"
else
  echo -e "  ${BOLD}Cerebras key${NC} ${DIM}(optional, for query optimization)${NC}"
  echo -e "  ${DIM}Get one at https://cerebras.ai -- free tier available${NC}"
  read -rp "  CEREBRAS_API_KEYS (press Enter to skip): " CB_KEYS
fi
echo ""

# Deepgram (optional)
EXISTING_DG="${DEEPGRAM_API_KEY:-}"
if [ -n "$EXISTING_DG" ]; then
  echo -e "  ${GREEN}DEEPGRAM_API_KEY found in environment${NC}"
  DG_KEY="$EXISTING_DG"
else
  echo -e "  ${BOLD}Deepgram key${NC} ${DIM}(optional, for video transcription)${NC}"
  echo -e "  ${DIM}Get one at https://deepgram.com -- free tier available${NC}"
  read -rp "  DEEPGRAM_API_KEY (press Enter to skip): " DG_KEY
fi
echo ""

# -- 5. Write .env file -------------------------------------------------------

cat > "$SCRIPT_DIR/.env" <<ENVEOF
TWITTERAPI_KEY=$TW_KEY
OPENROUTER_API_KEY=${OR_KEY:-}
CEREBRAS_API_KEYS=${CB_KEYS:-}
DEEPGRAM_API_KEY=${DG_KEY:-}
XS_INSTALL_ID=$INSTALL_ID
ENVEOF

echo -e "  ${GREEN}Saved .env to $SCRIPT_DIR/.env${NC}"

# Save to ~/.x-scout/config.json
python3 -c "
import json
config = {
    'install_id': '$INSTALL_ID',
    'twitterapi_key': '$TW_KEY',
    'openrouter_key': '${OR_KEY:-}',
    'cerebras_keys': '${CB_KEYS:-}',
    'deepgram_key': '${DG_KEY:-}',
}
with open('$XS_CONFIG', 'w') as f:
    json.dump(config, f, indent=2)
"
echo -e "  ${GREEN}Saved config to $XS_CONFIG${NC}"

# -- 6. Register install (analytics) ------------------------------------------

echo ""
echo -e "  Registering install..."

# Collect optional email for analytics
read -rp "  Email (optional, for updates): " USER_EMAIL

REGISTER_PAYLOAD=$(python3 -c "
import json, platform
print(json.dumps({
    'tool': 'x-scout',
    'install_id': '$INSTALL_ID',
    'email': '${USER_EMAIL:-}',
    'platform': platform.system(),
    'python': '$PY_VER',
    'has_openrouter': bool('${OR_KEY:-}'),
    'has_cerebras': bool('${CB_KEYS:-}'),
    'has_deepgram': bool('${DG_KEY:-}'),
}))
")

# Silent registration -- don't fail setup if analytics server is down
curl -s -X POST "$ANALYTICS_URL" \
  -H "Content-Type: application/json" \
  -d "$REGISTER_PAYLOAD" \
  --connect-timeout 5 \
  --max-time 10 \
  >/dev/null 2>&1 || true

echo -e "  ${GREEN}Registered${NC}"

# -- Done ---------------------------------------------------------------------

echo ""
echo -e "${GREEN}${BOLD}Setup complete.${NC}"
echo ""
echo -e "  Usage examples:"
echo ""
echo -e "    ${CYAN}source .venv/bin/activate${NC}"
echo -e "    ${CYAN}python3 x_scout.py --search \"ai agents\" --limit 10${NC}"
echo -e "    ${CYAN}python3 x_scout.py --profile @elonmusk --limit 5${NC}"
echo -e "    ${CYAN}python3 x_scout.py --intel \"https://x.com/user/status/123\" ${NC}"
echo -e "    ${CYAN}python3 x_scout.py --search \"saas marketing\" --json${NC}"
echo ""
