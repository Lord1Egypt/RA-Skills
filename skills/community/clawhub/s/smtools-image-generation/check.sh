#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
ERRORS=0

echo "=== SMTools Image Generation Skill - Diagnostics ==="
echo ""

# 1. Python
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")')
    echo "[OK] Python $PYTHON_VERSION"
else
    echo "[FAIL] python3 not found"
    ERRORS=$((ERRORS + 1))
fi

# 2. Virtual environment
if [ -d "$SKILL_DIR/.venv" ]; then
    echo "[OK] Virtual environment exists"
else
    echo "[FAIL] Virtual environment not found. Run: bash setup.sh"
    ERRORS=$((ERRORS + 1))
fi

# 3. Dependencies
if [ -d "$SKILL_DIR/.venv" ]; then
    MISSING_DEPS=""
    for pkg in requests dotenv; do
        if ! "$SKILL_DIR/.venv/bin/python3" -c "import $pkg" 2>/dev/null; then
            MISSING_DEPS="$MISSING_DEPS $pkg"
        fi
    done
    if [ -z "$MISSING_DEPS" ]; then
        echo "[OK] Dependencies installed"
    else
        echo "[FAIL] Missing packages:$MISSING_DEPS. Run: bash setup.sh"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 4. Config
if [ -f "$SKILL_DIR/config.json" ]; then
    echo "[OK] config.json exists"
else
    echo "[WARN] config.json not found (will use defaults)"
fi

# 5. API Keys
if [ -n "${OPENROUTER_API_KEY:-}" ]; then
    echo "[OK] OPENROUTER_API_KEY is set"
else
    # Check .env file
    if [ -f "$SKILL_DIR/.env" ] && grep -q "^OPENROUTER_API_KEY=" "$SKILL_DIR/.env" 2>/dev/null; then
        echo "[OK] OPENROUTER_API_KEY found in .env"
    else
        echo "[WARN] OPENROUTER_API_KEY not set"
    fi
fi

if [ -n "${KIE_API_KEY:-}" ]; then
    echo "[OK] KIE_API_KEY is set"
else
    if [ -f "$SKILL_DIR/.env" ] && grep -q "^KIE_API_KEY=" "$SKILL_DIR/.env" 2>/dev/null; then
        echo "[OK] KIE_API_KEY found in .env"
    else
        echo "[INFO] KIE_API_KEY not set (optional, needed for Kie.ai provider)"
    fi
fi

# 6. Output directory
if [ -d "$SKILL_DIR/output" ]; then
    echo "[OK] Output directory exists"
else
    echo "[WARN] Output directory missing (will be created on first run)"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "All checks passed."
else
    echo "$ERRORS error(s) found. Run 'bash setup.sh' to fix."
    exit 1
fi
