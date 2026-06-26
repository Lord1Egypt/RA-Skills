#!/usr/bin/env bash
# rtk-setup.sh — Install RTK and verify it works
# Run automatically when the rtk-integration skill is installed.
# Usage: bash skills/rtk-integration/scripts/rtk-setup.sh

set -e

RTK_BIN="$HOME/.local/bin"
export PATH="$RTK_BIN:$PATH"

echo "🔧 RTK Setup"
echo "============"

# Check if already installed
if command -v rtk &>/dev/null; then
  echo "✅ RTK already installed: $(rtk --version)"
  echo ""
  echo "📊 Current token savings:"
  rtk gain 2>/dev/null || echo "(no data yet — run some commands first)"
  exit 0
fi

echo "📦 Installing RTK..."

OS="$(uname -s)"

if [[ "$OS" == "Darwin" ]] && command -v brew &>/dev/null; then
  echo "   Using Homebrew..."
  brew install rtk
elif [[ "$OS" == "Linux" ]] || [[ "$OS" == "Darwin" ]]; then
  echo "   Using install script..."
  curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

  # Ensure PATH persists across sessions
  PROFILE=""
  if [[ -f "$HOME/.zshrc" ]]; then
    PROFILE="$HOME/.zshrc"
  elif [[ -f "$HOME/.bashrc" ]]; then
    PROFILE="$HOME/.bashrc"
  elif [[ -f "$HOME/.profile" ]]; then
    PROFILE="$HOME/.profile"
  fi

  PATH_LINE='export PATH="$HOME/.local/bin:$PATH"'
  if [[ -n "$PROFILE" ]] && ! grep -q '.local/bin' "$PROFILE" 2>/dev/null; then
    echo "$PATH_LINE" >> "$PROFILE"
    echo "   Added PATH to $PROFILE"
  fi
else
  echo "❌ Unsupported OS: $OS"
  echo "   Download manually: https://github.com/rtk-ai/rtk/releases"
  exit 1
fi

echo ""

# Verify
if command -v rtk &>/dev/null; then
  echo "✅ RTK installed successfully: $(rtk --version)"
  echo ""
  echo "📊 Initial stats:"
  rtk gain 2>/dev/null || echo "(no data yet — run some rtk commands first)"
  echo ""
  echo "🚀 Ready! The agent will now use rtk-prefixed commands automatically."
  echo "   Run 'rtk gain' anytime to see token savings."
else
  echo "❌ RTK binary not found after install. Try manually:"
  echo "   cargo install --git https://github.com/rtk-ai/rtk"
  echo "   Download: https://github.com/rtk-ai/rtk/releases"
  exit 1
fi
