#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$SKILL_DIR/.venv"

SKILL_VERSION="$(cat "$SKILL_DIR/VERSION" 2>/dev/null || echo "unknown")"
echo "=== SMTools Image Generation Skill Setup (v$SKILL_VERSION) ==="
echo ""

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found. Please install Python 3.8+."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PYTHON_VERSION"

# Install dependencies into scripts/vendor/ (works with any system python3)
VENDOR_DIR="$SKILL_DIR/scripts/vendor"
echo "Installing dependencies into scripts/vendor/..."
python3 -m pip install -q --target "$VENDOR_DIR" -r "$SKILL_DIR/requirements.txt"

# Also install into venv as fallback
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists."
fi
"$VENV_DIR/bin/pip" install -q -r "$SKILL_DIR/requirements.txt"

# Copy config template
if [ ! -f "$SKILL_DIR/config.json" ]; then
    cp "$SKILL_DIR/assets/config.example.json" "$SKILL_DIR/config.json"
    echo "Created config.json from template."
else
    echo "config.json already exists, skipping."
fi

# Create .env template
if [ ! -f "$SKILL_DIR/.env" ]; then
    cat > "$SKILL_DIR/.env" <<'ENVEOF'
# Image Generation Skill - Environment Variables
# Uncomment and fill in the API keys you need.

# OpenRouter (primary provider)
# OPENROUTER_API_KEY=your_openrouter_api_key_here

# Kie.ai (alternative provider)
# KIE_API_KEY=your_kie_api_key_here
ENVEOF
    echo "Created .env template."
else
    echo ".env already exists, skipping."
fi

# Create output directory
mkdir -p "$SKILL_DIR/output"

echo ""
echo "=== Setup complete (v$SKILL_VERSION) ==="
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your API key(s)"
echo "  2. Test:     bash $SKILL_DIR/scripts/run.sh --list-models"
echo "  3. Generate: bash $SKILL_DIR/scripts/run.sh -p 'A cat in space'"
