#!/usr/bin/env bash
# setup-shell.sh ... Configure shell environment for LDM OS development.
# Run once on a new machine. Idempotent (safe to re-run).

set -euo pipefail

echo "LDM OS shell setup"
echo ""

# ── tmux: enable mouse scrolling ──

TMUX_CONF="$HOME/.tmux.conf"

if [ -f "$TMUX_CONF" ] && grep -q "set -g mouse on" "$TMUX_CONF"; then
  echo "[OK] tmux mouse scrolling already configured"
else
  echo "set -g mouse on" >> "$TMUX_CONF"
  echo "[OK] tmux mouse scrolling enabled ($TMUX_CONF)"
fi

# Reload if tmux is running
if command -v tmux &>/dev/null && tmux list-sessions &>/dev/null 2>&1; then
  tmux source-file "$TMUX_CONF" 2>/dev/null && echo "[OK] tmux config reloaded" || true
fi

echo ""
echo "Done. Shell environment configured."
