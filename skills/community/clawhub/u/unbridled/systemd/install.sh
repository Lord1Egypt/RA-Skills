#!/usr/bin/env bash
# Install the clawd-beeper-sync systemd user service.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_DIR="$HOME/.config/systemd/user"

mkdir -p "$TARGET_DIR"

# Substitute the script path so the unit uses the actual checkout.
sed -e "s|%h/.openclaw/workspace/scripts/beeper/sync_daemon.py|$REPO_DIR/scripts/sync_daemon.py|" \
    "$SCRIPT_DIR/clawd-beeper-sync.service" > "$TARGET_DIR/clawd-beeper-sync.service"

systemctl --user daemon-reload

echo "✓ Installed clawd-beeper-sync.service"
echo ""
echo "Enable + start with:"
echo "  systemctl --user enable --now clawd-beeper-sync.service"
echo ""
echo "Watch logs:"
echo "  journalctl --user -u clawd-beeper-sync -f"
