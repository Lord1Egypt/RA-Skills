#!/usr/bin/env bash
# sigui-security/install.sh — Auto-install Sigui Protocol dependencies
#
# This script is called automatically by OpenClaw after skill installation.
# It ensures sigui-sdk and all required dependencies are available.
#
# Usage:
#   ./install.sh          — Install in current Python environment
#   ./install.sh --check  — Only check if already installed (no install)
set -e

SKILL_NAME="sigui-security"
SDK_PACKAGE="sigui-sdk"
SDK_MIN_VERSION="0.3.1"
RICH_PACKAGE="rich"

# ── Color helpers ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

ok()   { echo -e "${GREEN}✅ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
err()  { echo -e "${RED}❌ $1${NC}" >&2; }
info() { echo -e "${CYAN}ℹ️  $1${NC}"; }

echo ""
echo "🛡️  ${SKILL_NAME} — Dependency Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Python check ──────────────────────────────────────────────────────────────
PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" &>/dev/null; then
    PYTHON="python"
fi
if ! command -v "$PYTHON" &>/dev/null; then
    err "Python not found. Please install Python 3.10+ and try again."
    exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
info "Python: $PY_VERSION ($(command -v $PYTHON))"

# ── Check-only mode ───────────────────────────────────────────────────────────
if [[ "${1:-}" == "--check" ]]; then
    info "Check mode — not installing anything."
    
    SDK_OK=false
    if $PYTHON -c "from sigui import SiguiClient" &>/dev/null 2>&1; then
        SDK_VER=$($PYTHON -c "import sigui; print(getattr(sigui, '__version__', 'unknown'))" 2>/dev/null)
        ok "sigui-sdk is installed (version: ${SDK_VER})"
        SDK_OK=true
    else
        warn "sigui-sdk is NOT installed"
    fi

    if $PYTHON -c "import rich" &>/dev/null 2>&1; then
        ok "rich is installed"
    else
        warn "rich is NOT installed (optional, for pretty output)"
    fi

    if $SDK_OK; then
        ok "All required dependencies are available."
        exit 0
    else
        warn "Run './install.sh' to install missing dependencies."
        exit 1
    fi
fi

# ── Activate venv if present ──────────────────────────────────────────────────
if [ -f ".venv/bin/activate" ]; then
    info "Virtual environment found. Activating..."
    # shellcheck disable=SC1091
    source .venv/bin/activate
    ok "Virtual environment activated."
elif [ -f "venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    source venv/bin/activate
    ok "Virtual environment activated."
fi

# ── Install sigui-sdk ─────────────────────────────────────────────────────────
if $PYTHON -c "from sigui import SiguiClient" &>/dev/null 2>&1; then
    SDK_VER=$($PYTHON -c "import sigui; print(getattr(sigui, '__version__', 'unknown'))" 2>/dev/null)
    ok "sigui-sdk already installed (version: ${SDK_VER})"
else
    info "Installing ${SDK_PACKAGE}>=${SDK_MIN_VERSION}..."
    $PYTHON -m pip install "${SDK_PACKAGE}>=${SDK_MIN_VERSION}" --quiet

    if $PYTHON -c "from sigui import SiguiClient" &>/dev/null 2>&1; then
        ok "sigui-sdk installed successfully."
    else
        err "sigui-sdk installation failed. Check your network connection."
        exit 1
    fi
fi

# ── Install rich (optional, for pretty CLI output) ────────────────────────────
if $PYTHON -c "import rich" &>/dev/null 2>&1; then
    ok "rich already installed."
else
    info "Installing rich (for pretty output)..."
    $PYTHON -m pip install "${RICH_PACKAGE}" --quiet && ok "rich installed." || warn "rich install failed (optional, continuing)."
fi

# ── Final verification ────────────────────────────────────────────────────────
echo ""
echo "🔍 Running final verification..."

if ! $PYTHON -c "from sigui import SiguiClient; from sigui.models import Verdict" &>/dev/null 2>&1; then
    err "Sigui SDK import verification failed."
    err "Please report this issue: https://github.com/ibonon/Sigui/issues"
    exit 1
fi

ok "Sigui SDK import verified."

echo ""
ok "All dependencies are ready!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📌 Next step: Configure your Sigui endpoint"
echo ""
echo "   export SIGUI_API_URL=\"https://your-sigui-node.com\""
echo ""
echo "   Then test with:"
echo "   python evaluate.py --amount 100 --destination 0xYourAddress --demo"
echo ""
echo "   For real API use (required for production):"
echo "   python evaluate.py --amount 100 --destination 0xYourAddress"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
