#!/bin/bash
# screen-vision auto-setup: installs CLI binary + cliclick if missing
set -euo pipefail

ok() { echo "  ✓ $1"; }
install_step() { echo "  ⟳ $1..."; }

echo "screen-vision setup"
echo "==================="

# 1. screen-vision binary
if command -v screen-vision &>/dev/null; then
    ok "screen-vision $(screen-vision --help 2>&1 | head -1 | grep -oE 'v[0-9.]+' || echo 'installed')"
else
    if command -v brew &>/dev/null; then
        install_step "Installing screen-vision via Homebrew"
        brew install jackyun1024/tap/screen-vision
        ok "screen-vision installed via Homebrew"
    elif [[ "$(uname -m)" == "arm64" ]]; then
        install_step "Downloading pre-built binary (Apple Silicon)"
        curl -sL https://github.com/jackyun1024/mac-screen-vision/releases/download/v1.0.0/screen-vision-1.0.0-arm64-macos.tar.gz | tar xz -C /usr/local/bin/
        chmod +x /usr/local/bin/screen-vision
        ok "screen-vision installed to /usr/local/bin/"
    else
        install_step "Building screen-vision from source (Intel)"
        TMPDIR=$(mktemp -d)
        git clone --depth 1 https://github.com/jackyun1024/mac-screen-vision.git "$TMPDIR/sv"
        cd "$TMPDIR/sv" && swift build -c release
        cp .build/release/screen-vision /usr/local/bin/
        rm -rf "$TMPDIR"
        ok "screen-vision built and installed to /usr/local/bin/"
    fi
fi

# 2. cliclick (for tap command)
if command -v cliclick &>/dev/null; then
    ok "cliclick installed"
else
    if command -v brew &>/dev/null; then
        install_step "Installing cliclick via Homebrew"
        brew install cliclick
        ok "cliclick installed"
    else
        echo "  ⚠ cliclick not found. 'tap' command won't work."
        echo "    Install manually: https://github.com/BlueM/cliclick"
    fi
fi

# 3. Screen Recording permission check
echo ""
if screen-vision has "$(hostname -s)" 2>/dev/null || screen-vision list 2>/dev/null | head -1 | grep -q '\['; then
    ok "Screen Recording permission granted"
else
    echo "  ⚠ Screen Recording permission may be needed."
    echo "    System Settings > Privacy & Security > Screen Recording"
    echo "    Add your terminal app (Terminal, iTerm2, Warp, etc.)"
fi

echo ""
echo "Setup complete. Try: screen-vision list"
