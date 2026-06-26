#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_DIR="${VENV_DIR:-$SKILL_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "Error: '$PYTHON_BIN' not found." >&2
  echo "" >&2
  echo "Install Python 3 first:" >&2
  echo "  macOS:   brew install python3" >&2
  echo "  Ubuntu:  sudo apt install python3 python3-venv" >&2
  echo "" >&2
  echo "Or set PYTHON_BIN to point to your Python 3 installation:" >&2
  echo "  PYTHON_BIN=/path/to/python3 bash scripts/setup.sh" >&2
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r "$SKILL_DIR/requirements.txt"

ENV_FILE="$SKILL_DIR/.env"

echo
echo "Setup complete. Dependencies installed."
echo

if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<'EOF'
# Spotify API credentials
# Get these from https://developer.spotify.com/dashboard
# When creating your app, set the redirect URI to: http://127.0.0.1:8888/callback
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
EOF
  echo "Created .env at $ENV_FILE"
  echo ""
  echo "Next steps:"
  echo "  1. Go to https://developer.spotify.com/dashboard and create an app"
  echo "     Set the redirect URI to: http://127.0.0.1:8888/callback"
  echo "  2. Fill in your credentials in .env"
  echo "  3. Run: cd $SKILL_DIR && .venv/bin/python scripts/spotify_auth.py"
  echo ""
  echo "If your credentials are stored elsewhere, set SPOTIFY_ENV_PATH and re-run auth:"
  echo "  cd $SKILL_DIR && SPOTIFY_ENV_PATH=/path/to/creds.env .venv/bin/python scripts/spotify_auth.py"
elif grep -qE 'CLIENT_ID=your_client_id_here|CLIENT_SECRET=your_client_secret_here' "$ENV_FILE" 2>/dev/null; then
  echo "Fill in your credentials in .env, then authenticate:"
  echo "  cd $SKILL_DIR && .venv/bin/python scripts/spotify_auth.py"
elif ! grep -q 'CLIENT_ID' "$ENV_FILE" 2>/dev/null || ! grep -q 'CLIENT_SECRET' "$ENV_FILE" 2>/dev/null; then
  echo "Warning: .env exists but may be missing SPOTIPY_CLIENT_ID or SPOTIPY_CLIENT_SECRET."
  echo "Make sure both are set, then authenticate:"
  echo "  cd $SKILL_DIR && .venv/bin/python scripts/spotify_auth.py"
else
  TOKENS_FILE_SKILL="$SKILL_DIR/spotify_tokens.json"
  TOKENS_FILE_SCRIPT="$SCRIPT_DIR/spotify_tokens.json"
  TOKENS_FILE_CWD="$PWD/spotify_tokens.json"
  TOKENS_FILE_CWD_SECRETS="$PWD/secrets/spotify_tokens.json"
  if { [ -f "$TOKENS_FILE_SKILL" ] && grep -q 'access_token' "$TOKENS_FILE_SKILL" 2>/dev/null; } \
    || { [ -f "$TOKENS_FILE_SCRIPT" ] && grep -q 'access_token' "$TOKENS_FILE_SCRIPT" 2>/dev/null; } \
    || { [ -f "$TOKENS_FILE_CWD" ] && grep -q 'access_token' "$TOKENS_FILE_CWD" 2>/dev/null; } \
    || { [ -f "$TOKENS_FILE_CWD_SECRETS" ] && grep -q 'access_token' "$TOKENS_FILE_CWD_SECRETS" 2>/dev/null; }; then
    echo "Already set up. You're ready to go!"
  else
    echo "Credentials found in .env. Next step — authenticate:"
    echo "  cd $SKILL_DIR && .venv/bin/python scripts/spotify_auth.py"
  fi
fi
