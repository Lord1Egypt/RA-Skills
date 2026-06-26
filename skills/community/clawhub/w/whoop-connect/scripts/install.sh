#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/.venv"

echo "Installing WHOOP Connect dependencies..."

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 is required but not found."
    exit 1
fi

# Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Install into venv
"${VENV_DIR}/bin/pip" install --quiet --upgrade requests flask

# Create a wrapper so scripts can be called directly with system python
# by using the venv's site-packages
ACTIVATE_WRAPPER="${SCRIPT_DIR}/python"
cat > "$ACTIVATE_WRAPPER" <<'WRAPPER'
#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "${SCRIPT_DIR}/.venv/bin/python3" "$@"
WRAPPER
chmod +x "$ACTIVATE_WRAPPER"

# Create data directory
mkdir -p ~/.whoop
chmod 700 ~/.whoop

echo "✓ Dependencies installed (venv at ${VENV_DIR})"
echo ""
echo "Next steps:"
echo "  1. Set environment variables:"
echo "     export WHOOP_CLIENT_ID='your_client_id'"
echo "     export WHOOP_CLIENT_SECRET='your_client_secret'"
echo ""
echo "  2. Run setup wizard:"
echo "     ${SCRIPT_DIR}/python ${SCRIPT_DIR}/setup.py"
echo ""
echo "  3. Authorize with WHOOP:"
echo "     ${SCRIPT_DIR}/python ${SCRIPT_DIR}/whoop_client.py auth"
