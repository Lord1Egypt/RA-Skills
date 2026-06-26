#!/usr/bin/env bash
# check.sh — Pre-flight diagnostics for the STT OpenClaw skill.
# Checks prerequisites and prints recommendations.
#
# Usage:
#   bash check.sh

set -euo pipefail

# ── Colors ───────────────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
info() { echo -e "${CYAN}→${NC} $1"; }

ERRORS=0
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  sergei-mikhailov-stt — Diagnostics"
echo "══════════════════════════════════════════════════════"
echo ""

# ── Step 1: Python ───────────────────────────────────────────────────────────

echo "── Python ──"

if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    PY_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 8 ]; then
        ok "Python $PY_VERSION"
    else
        fail "Python $PY_VERSION (need 3.8+)"
        info "Install Python 3.8 or newer"
        ERRORS=$((ERRORS + 1))
    fi
else
    fail "python3 not found"
    info "Install Python 3.8+: https://www.python.org/downloads/"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# ── Step 2: FFmpeg ───────────────────────────────────────────────────────────

echo "── FFmpeg ──"

if command -v ffmpeg &>/dev/null; then
    FF_VERSION=$(ffmpeg -version 2>&1 | head -1 | awk '{print $3}')
    ok "ffmpeg $FF_VERSION"
else
    fail "ffmpeg not found"
    info "Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# ── Step 3: Virtual Environment ──────────────────────────────────────────────

echo "── Virtual Environment ──"

VENV_DIR="$SCRIPT_DIR/.venv"

if [ -d "$VENV_DIR" ]; then
    ok ".venv exists"

    VENV_PYTHON="$VENV_DIR/bin/python"
    if [ -x "$VENV_PYTHON" ]; then
        # Check key dependencies
        MISSING_DEPS=0
        for pkg in dotenv requests; do
            if "$VENV_PYTHON" -c "import $pkg" 2>/dev/null; then
                ok "Python package: $pkg"
            else
                fail "Python package missing: $pkg"
                MISSING_DEPS=1
            fi
        done
        if [ "$MISSING_DEPS" -eq 1 ]; then
            info "Run: bash setup.sh"
            ERRORS=$((ERRORS + 1))
        fi
    else
        fail ".venv/bin/python not executable"
        info "Re-create venv: rm -rf .venv && bash setup.sh"
        ERRORS=$((ERRORS + 1))
    fi
else
    fail ".venv not found"
    info "Run: bash setup.sh"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# ── Step 4: Configuration Files ──────────────────────────────────────────────

echo "── Configuration ──"

if [ -f "$SCRIPT_DIR/config.json" ]; then
    ok "config.json exists"
else
    warn "config.json not found"
    info "Run: bash setup.sh"
fi

echo ""

# ── Step 5: API Keys ────────────────────────────────────────────────────────

echo "── API Keys ──"

KEYS_OK=0

# Check openclaw.json
OC_CONFIG="${HOME}/.openclaw/openclaw.json"
if [ -f "$OC_CONFIG" ]; then
    # Check for YANDEX_API_KEY in openclaw.json
    if python3 -c "
import json, sys
with open('$OC_CONFIG') as f:
    cfg = json.load(f)
env = cfg.get('skills',{}).get('entries',{}).get('sergei-mikhailov-stt',{}).get('env',{})
if env.get('YANDEX_API_KEY') and env.get('YANDEX_FOLDER_ID'):
    sys.exit(0)
sys.exit(1)
" 2>/dev/null; then
        ok "YANDEX_API_KEY and YANDEX_FOLDER_ID set in openclaw.json"
        KEYS_OK=1
    fi
fi

# Check .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    ENV_API_KEY=$(grep -E '^YANDEX_API_KEY=' "$SCRIPT_DIR/.env" 2>/dev/null | cut -d= -f2- || true)
    ENV_FOLDER_ID=$(grep -E '^YANDEX_FOLDER_ID=' "$SCRIPT_DIR/.env" 2>/dev/null | cut -d= -f2- || true)

    if [ -n "$ENV_API_KEY" ] && [ "$ENV_API_KEY" != "your_api_key_here" ] \
       && [ -n "$ENV_FOLDER_ID" ] && [ "$ENV_FOLDER_ID" != "your_folder_id_here" ]; then
        ok "YANDEX_API_KEY and YANDEX_FOLDER_ID set in .env"
        KEYS_OK=1
    elif [ "$KEYS_OK" -eq 0 ]; then
        warn ".env exists but keys are not filled in"
    fi
fi

# Check environment variables
if [ -n "${YANDEX_API_KEY:-}" ] && [ -n "${YANDEX_FOLDER_ID:-}" ]; then
    ok "YANDEX_API_KEY and YANDEX_FOLDER_ID set via environment"
    KEYS_OK=1
fi

if [ "$KEYS_OK" -eq 0 ]; then
    fail "No API keys found"
    info "Option 1 (recommended): add to ~/.openclaw/openclaw.json:"
    info '  "skills": { "entries": { "sergei-mikhailov-stt": { "env": {'
    info '    "YANDEX_API_KEY": "...", "YANDEX_FOLDER_ID": "..." } } } }'
    info "Option 2: edit .env in the skill folder"
    info "Get keys at https://console.yandex.cloud/"
    ERRORS=$((ERRORS + 1))
fi

echo ""

# ── Step 6: API Connectivity ───────────────────────────────────────────────

echo "── API Connectivity ──"

if [ "$KEYS_OK" -eq 1 ] && command -v curl &>/dev/null; then
    # Collect actual key values (priority: openclaw.json > .env > env vars)
    CHECK_API_KEY=""
    CHECK_FOLDER_ID=""

    # From environment variables
    if [ -n "${YANDEX_API_KEY:-}" ] && [ -n "${YANDEX_FOLDER_ID:-}" ]; then
        CHECK_API_KEY="${YANDEX_API_KEY}"
        CHECK_FOLDER_ID="${YANDEX_FOLDER_ID}"
    fi

    # From .env (overrides env vars)
    if [ -f "$SCRIPT_DIR/.env" ]; then
        _ekey=$(grep -E '^YANDEX_API_KEY=' "$SCRIPT_DIR/.env" 2>/dev/null | cut -d= -f2- || true)
        _efid=$(grep -E '^YANDEX_FOLDER_ID=' "$SCRIPT_DIR/.env" 2>/dev/null | cut -d= -f2- || true)
        if [ -n "$_ekey" ] && [ "$_ekey" != "your_api_key_here" ] \
           && [ -n "$_efid" ] && [ "$_efid" != "your_folder_id_here" ]; then
            CHECK_API_KEY="$_ekey"
            CHECK_FOLDER_ID="$_efid"
        fi
    fi

    # From openclaw.json (highest priority)
    if [ -f "$OC_CONFIG" ]; then
        _okeys=$(python3 -c "
import json, sys
with open('$OC_CONFIG') as f:
    cfg = json.load(f)
env = cfg.get('skills',{}).get('entries',{}).get('sergei-mikhailov-stt',{}).get('env',{})
ak = env.get('YANDEX_API_KEY','')
fi = env.get('YANDEX_FOLDER_ID','')
if ak and fi:
    print(ak + '\n' + fi)
" 2>/dev/null || true)
        if [ -n "$_okeys" ]; then
            CHECK_API_KEY=$(echo "$_okeys" | head -1)
            CHECK_FOLDER_ID=$(echo "$_okeys" | tail -1)
        fi
    fi

    if [ -n "$CHECK_API_KEY" ] && [ -n "$CHECK_FOLDER_ID" ]; then
        # Send an empty body to the SpeechKit API to validate credentials.
        # Expected responses:
        #   400 = auth OK (bad request because no audio)
        #   401 = invalid API key
        #   403 = access denied (check folder_id / service account role)
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
            -X POST "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId=${CHECK_FOLDER_ID}&lang=ru-RU" \
            -H "Authorization: Api-Key ${CHECK_API_KEY}" \
            --max-time 10 \
            2>/dev/null || echo "000")

        case "$HTTP_CODE" in
            400)
                ok "API credentials are valid (SpeechKit responded)"
                ;;
            401)
                fail "API key is invalid (HTTP 401)"
                info "Check YANDEX_API_KEY — it may be expired or mistyped"
                ERRORS=$((ERRORS + 1))
                ;;
            403)
                fail "Access denied (HTTP 403)"
                info "Check that the service account has the ai.speechkit.user role"
                info "and that YANDEX_FOLDER_ID is correct"
                ERRORS=$((ERRORS + 1))
                ;;
            000)
                warn "Could not reach Yandex SpeechKit API (network error or timeout)"
                info "Check your internet connection"
                ;;
            *)
                warn "Unexpected response from SpeechKit API (HTTP $HTTP_CODE)"
                ;;
        esac
    else
        warn "Could not extract key values for API check"
    fi
elif [ "$KEYS_OK" -eq 0 ]; then
    info "Skipping API check (no keys found)"
elif ! command -v curl &>/dev/null; then
    warn "curl not found, skipping API connectivity check"
fi

echo ""

# ── Summary ──────────────────────────────────────────────────────────────────

echo "══════════════════════════════════════════════════════"
if [ "$ERRORS" -eq 0 ]; then
    echo -e "  ${GREEN}All checks passed.${NC} STT skill is ready."
else
    echo -e "  ${RED}${ERRORS} issue(s) found.${NC} Fix them and re-run: bash check.sh"
fi
echo "══════════════════════════════════════════════════════"
echo ""

exit "$ERRORS"
