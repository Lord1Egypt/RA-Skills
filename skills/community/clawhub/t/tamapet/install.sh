#!/usr/bin/env bash
# Cross-platform install: OpenClaw + Hermes Agent.
# Symlinks this directory into both runtimes' skill paths.
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"

OPENCLAW_DIR="$HOME/.openclaw/workspace/skills/pet"
HERMES_DIR="$HOME/.hermes/skills/games/pet"

link() {
    local target="$1"
    local parent="$(dirname "$target")"
    if [[ "$SRC" == "$target" ]]; then
        echo "  ✓ already at $target (source)"
        return
    fi
    mkdir -p "$parent"
    if [[ -L "$target" ]]; then
        rm "$target"
    elif [[ -e "$target" ]]; then
        echo "  ⚠️  $target exists and is not a symlink — backup to ${target}.bak"
        mv "$target" "${target}.bak"
    fi
    ln -s "$SRC" "$target"
    echo "  ✓ linked → $target"
}

echo "🐣 Installing pet skill from $SRC"

if [[ -d "$HOME/.openclaw" ]]; then
    echo "OpenClaw detected"
    link "$OPENCLAW_DIR"
else
    echo "  (skipped) ~/.openclaw not found"
fi

if [[ -d "$HOME/.hermes" ]] || command -v hermes >/dev/null 2>&1; then
    echo "Hermes Agent detected"
    link "$HERMES_DIR"
else
    echo "  (skipped) ~/.hermes not found"
fi

if ! python3 -c "import PIL" 2>/dev/null; then
    echo
    echo "📦 Pillow needed for pet card PNG:"
    echo "   pip3 install pillow"
fi

echo
echo "✅ Done. Next steps:"
echo "   1. python3 $SRC/server.py"
echo "   2. cloudflared tunnel --url http://localhost:8080"
echo "   3. BotFather → /newapp → @Bombaligrim_bot → short name: pet → URL: <tunnel>"
