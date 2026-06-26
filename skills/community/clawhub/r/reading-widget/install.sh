#!/bin/bash
set -e

# Reading Widget installer
# 1) Copies runtime files to ~/Desktop/reading-widget/
# 2) Runs update.py once to generate widget.html
# 3) Tells you how to open the card (local helper + frameless Chrome window)

SRC="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/Desktop/reading-widget"

echo "→ Installing runtime to $DEST"
mkdir -p "$DEST"
cp "$SRC/update.py" "$SRC/template.html" "$SRC/server.py" "$SRC/open-widget.sh" "$DEST/"
chmod +x "$DEST/open-widget.sh"
[ -f "$DEST/config.json" ] || cp "$SRC/config.default.json" "$DEST/config.json"

if [ -z "$WEREAD_API_KEY" ] && ! grep -qs WEREAD_API_KEY "$HOME/.claw/settings.json" "$HOME/.claude/settings.json"; then
  echo ""
  echo "⚠️  WEREAD_API_KEY not set."
  echo "   Apply for one via WeRead Agent Gateway (see SKILL.md)."
  echo "   Then add to ~/.claw/settings.json (Claude Code: ~/.claude/settings.json) env, or run:"
  echo "   export WEREAD_API_KEY=wrk-xxxxxxxx"
  echo ""
  exit 0
fi

echo "→ Generating widget.html for the first time"
python3 "$DEST/update.py"

echo ""
echo "✅ Installed."
echo "   Open the widget:  bash $DEST/open-widget.sh"
echo "   (starts the local helper on 127.0.0.1:47900 and opens a frameless Chrome window;"
echo "    on-card goal edits then persist and data auto-refreshes every 30 min)"
echo ""
echo "   Optional · keep the helper running at login — see SKILL.md Step 4 (launchd)."
echo "   Optional · Übersicht — copy ubersicht/reading.widget to"
echo "   ~/Library/Application Support/Übersicht/widgets/ and Refresh All Widgets."
