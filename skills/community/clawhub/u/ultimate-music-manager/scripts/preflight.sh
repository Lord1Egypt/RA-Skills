#!/usr/bin/env bash
# =============================================================================
# Sonic Phoenix — Preflight Check
# =============================================================================
# Validates that the environment is correctly configured before any pipeline
# script is run. Exits 0 if everything is healthy, non-zero on first failure.
#
# Usage:
#   ./scripts/preflight.sh              # run from the skill directory
#   bash ultimate-music-manager/scripts/preflight.sh   # from repo root
#
# What it checks (in order):
#   1. Python 3.12 is available
#   2. Virtual environment is active
#   3. Required pip packages are installed
#   4. .env file exists in the repo root
#   5. MUSIC_ROOT is set and points to a real directory
#   6. config.py executes without error
#   7. FFmpeg is available (optional — warns but does not fail)
# =============================================================================

set -euo pipefail

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Colour

pass()  { printf "${GREEN}[PASS]${NC} %s\n" "$1"; }
fail()  { printf "${RED}[FAIL]${NC} %s\n" "$1"; exit 1; }
warn()  { printf "${YELLOW}[WARN]${NC} %s\n" "$1"; }
info()  { printf "       %s\n" "$1"; }

# ---------------------------------------------------------------------------
# Locate the repo root (config.py lives there)
# ---------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# scripts/ sits inside the skill folder which sits inside the repo
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

if [ ! -f "$REPO_ROOT/config.py" ]; then
    fail "Cannot find config.py. Expected repo root at: $REPO_ROOT"
fi

# ---------------------------------------------------------------------------
# 1. Python 3.12
# ---------------------------------------------------------------------------
PYTHON=""
for candidate in python3.12 python3 python; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>/dev/null || echo "")
        if [ "$ver" = "3.12" ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    fail "Python 3.12 not found. shazamio-core requires Python 3.10-3.12 (3.12 recommended)."
fi
pass "Python 3.12 found: $PYTHON ($($PYTHON --version 2>&1))"

# ---------------------------------------------------------------------------
# 2. Virtual environment active
# ---------------------------------------------------------------------------
if [ -z "${VIRTUAL_ENV:-}" ]; then
    warn "No virtual environment active."
    info "Activate one with:"
    info "  source .venv/bin/activate          # macOS / Linux"
    info "  .venv\\Scripts\\activate             # Windows PowerShell"
    info ""
    info "Or create one first:"
    info "  $PYTHON -m venv .venv"
    # Not a hard fail — the user might have installed globally intentionally.
else
    pass "Virtual environment active: $VIRTUAL_ENV"
fi

# ---------------------------------------------------------------------------
# 3. Required pip packages
# ---------------------------------------------------------------------------
REQUIRED_PACKAGES=(mutagen shazamio langdetect requests Pillow spotipy dotenv)
# dotenv is imported as "dotenv" but the pip name is "python-dotenv".
# We check import names here.
IMPORT_NAMES=(mutagen shazamio langdetect requests PIL spotipy dotenv)

MISSING=()
for i in "${!IMPORT_NAMES[@]}"; do
    if ! "$PYTHON" -c "import ${IMPORT_NAMES[$i]}" &>/dev/null; then
        MISSING+=("${REQUIRED_PACKAGES[$i]}")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    fail "Missing Python packages: ${MISSING[*]}. Run: pip install -r requirements.txt"
fi
pass "All required Python packages are installed."

# ---------------------------------------------------------------------------
# 4. .env file
# ---------------------------------------------------------------------------
ENV_FILE="$REPO_ROOT/.env"
if [ ! -f "$ENV_FILE" ]; then
    warn ".env file not found at $ENV_FILE"
    info "Copy the example and fill in MUSIC_ROOT:"
    info "  cp .env.example .env"
    # Not a hard fail — config.py falls back to env vars or auto-detection.
else
    pass ".env file found: $ENV_FILE"
fi

# ---------------------------------------------------------------------------
# 5. MUSIC_ROOT
# ---------------------------------------------------------------------------
# Source .env manually to read MUSIC_ROOT (config.py uses python-dotenv,
# but we need the value in bash).
if [ -f "$ENV_FILE" ]; then
    MUSIC_ROOT=$(grep -E '^MUSIC_ROOT=' "$ENV_FILE" | head -1 | cut -d'=' -f2- | tr -d '"' | tr -d "'" | xargs)
fi
MUSIC_ROOT="${MUSIC_ROOT:-${MUSIC_ROOT_ENV:-}}"
# Also check the process environment
MUSIC_ROOT="${MUSIC_ROOT:-$( printenv MUSIC_ROOT 2>/dev/null || echo "" )}"

if [ -z "$MUSIC_ROOT" ]; then
    fail "MUSIC_ROOT is not set. Set it in .env or your shell environment."
fi

if [ ! -d "$MUSIC_ROOT" ]; then
    fail "MUSIC_ROOT does not exist: $MUSIC_ROOT"
fi
pass "MUSIC_ROOT exists: $MUSIC_ROOT"

# ---------------------------------------------------------------------------
# 6. config.py executes cleanly
# ---------------------------------------------------------------------------
CONFIG_OUTPUT=$("$PYTHON" "$REPO_ROOT/config.py" 2>&1) || {
    fail "config.py failed to execute:\n$CONFIG_OUTPUT"
}
pass "config.py executes cleanly."
info "$(echo "$CONFIG_OUTPUT" | head -4)"

# ---------------------------------------------------------------------------
# 7. FFmpeg (optional)
# ---------------------------------------------------------------------------
if command -v ffmpeg &>/dev/null; then
    FFMPEG_VER=$(ffmpeg -version 2>&1 | head -1)
    pass "FFmpeg found: $FFMPEG_VER"
else
    # Check the portable location config.py might use
    FFMPEG_PORTABLE="$MUSIC_ROOT/ffmpeg/bin/ffmpeg"
    if [ -f "$FFMPEG_PORTABLE" ] || [ -f "${FFMPEG_PORTABLE}.exe" ]; then
        pass "Portable FFmpeg found at: $MUSIC_ROOT/ffmpeg/bin/"
    else
        warn "FFmpeg not found. Required only for non-MP3 formats (FLAC, OGG, WMA, etc.)."
        info "Install via your package manager or drop a portable build at:"
        info "  $MUSIC_ROOT/ffmpeg/bin/"
    fi
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
printf "${GREEN}Preflight complete. Environment is ready.${NC}\n"
exit 0
