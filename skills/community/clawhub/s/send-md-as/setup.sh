#!/bin/bash
# setup.sh - Install dependencies for send-md-as skill
# Idempotent: skips already-installed items
# Usage: setup.sh [--check-only]
set -e

CHECK_ONLY=false
[[ "$1" == "--check-only" ]] && CHECK_ONLY=true

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENDOR_DIR="$SKILL_DIR/vendor"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
fail()  { echo -e "${RED}[✗]${NC} $1"; }

# --- Ensure pip is available ---
if ! python3 -m pip --version &>/dev/null; then
    fail "python3 pip is not available. Install it first:"
    echo "  Debian/Ubuntu: apt install python3-pip"
    echo "  Fedora/RHEL:   dnf install python3-pip"
    echo "  macOS:         python3 -m ensurepip"
    exit 1
fi

# --- Ensure ~/.local/bin is in PATH ---
LOCAL_BIN="$HOME/.local/bin"
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    warn "$LOCAL_BIN is not in PATH. Adding for this session."
    export PATH="$LOCAL_BIN:$PATH"
    echo "  Consider adding to your shell profile:"
    echo "    echo 'export PATH=\"$LOCAL_BIN:\$PATH\"' >> ~/.zshrc"
fi

# --- Ensure vendor dir exists ---
mkdir -p "$VENDOR_DIR"

# --- playwright (required, the only renderer) ---
if python3 -c "from playwright.sync_api import sync_playwright" 2>/dev/null; then
    info "Playwright already installed"
else
    warn "Installing Playwright..."
    if $CHECK_ONLY; then
        fail "Playwright not installed (check-only mode)"
    else
        python3 -m pip install --user playwright 2>/dev/null && info "Playwright pip installed" || fail "Playwright pip install failed"
        # Use mirror if PLAYWRIGHT_DOWNLOAD_HOST is set (helps users in China)
        python3 -m playwright install chromium 2>/dev/null && info "Playwright chromium installed" || fail "Playwright chromium install failed (run: python3 -m playwright install chromium, or set PLAYWRIGHT_DOWNLOAD_HOST mirror)"
    fi
fi

# --- python3-pillow (required) ---
if python3 -c "from PIL import Image" 2>/dev/null; then
    info "Pillow already installed"
else
    warn "Installing Pillow..."
    if $CHECK_ONLY; then
        fail "Pillow not installed (check-only mode)"
    else
        python3 -m pip install --user pillow 2>/dev/null || fail "Pillow install failed (try: python3 -m pip install --user pillow)"
        python3 -c "from PIL import Image" 2>/dev/null && info "Pillow installed" || fail "Pillow installation failed"
    fi
fi

# --- python3-mistune (required) ---
if python3 -c "import mistune" 2>/dev/null; then
    info "Mistune already installed: $(python3 -c 'import mistune; print(mistune.__version__)')"
else
    warn "Installing mistune..."
    if $CHECK_ONLY; then
        fail "Mistune not installed (check-only mode)"
    else
        python3 -m pip install --user mistune 2>/dev/null || fail "Mistune install failed"
        python3 -c "import mistune" 2>/dev/null && info "Mistune installed" || fail "Mistune installation failed"
    fi
fi

# --- nh3 (required, HTML sanitization) ---
if python3 -c "import nh3" 2>/dev/null; then
    info "nh3 already installed"
else
    warn "Installing nh3..."
    if $CHECK_ONLY; then
        fail "nh3 not installed (check-only mode)"
    else
        python3 -m pip install --user 'nh3>=0.2.18' 2>/dev/null || fail "nh3 install failed"
        python3 -c "import nh3" 2>/dev/null && info "nh3 installed" || fail "nh3 installation failed"
    fi
fi

# --- Custom font (optional) ---
# To use a custom font (e.g., Maple Mono), place .woff2 files in skill's fonts/ dir:
#   fonts/custom-400.woff2  (regular weight)
#   fonts/custom-700.woff2  (bold weight)
# The script auto-detects these files. Falls back to system fonts if absent.

# --- mermaid-cli (optional, for diagrams) ---
export PATH="$VENDOR_DIR/bin:$PATH"
if command -v mmdc &>/dev/null; then
    info "Mermaid CLI already installed: $(mmdc --version 2>&1)"
else
    warn "Installing mermaid-cli (optional, to vendor/)..."
    npm install --prefix "$VENDOR_DIR" @mermaid-js/mermaid-cli 2>/dev/null && info "Mermaid CLI installed" || warn "Mermaid CLI install failed, diagrams will show as code"
fi

# --- pygments (optional, for syntax highlighting) ---
if python3 -c "import pygments" 2>/dev/null; then
    info "Pygments already installed"
else
    warn "Installing pygments (optional)..."
    python3 -m pip install --user pygments 2>/dev/null || true
    if python3 -c "import pygments" 2>/dev/null; then
        info "Pygments installed (syntax highlighting enabled)"
    else
        warn "Pygments not available, code blocks will use monochrome style"
    fi
fi

# --- katex (optional, for LaTeX, via npm) ---
if command -v katex &>/dev/null; then
    info "KaTeX CLI already installed: $(katex --version 2>&1)"
else
    warn "Installing katex (optional, to vendor/)..."
    npm install --prefix "$VENDOR_DIR" katex 2>/dev/null && info "KaTeX CLI installed" || warn "KaTeX CLI install failed, LaTeX will show as raw text"
fi

echo ""
info "Setup complete."
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    echo ""
    warn "Reminder: add $LOCAL_BIN to your PATH for pip --user scripts."
    echo "  echo 'export PATH=\"$LOCAL_BIN:\$PATH\"' >> ~/.zshrc"
fi
