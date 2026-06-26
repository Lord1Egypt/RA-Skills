#!/bin/zsh
set -euo pipefail

SKILL_DIR="$(cd -- "$(dirname -- "$0")/.." && pwd)"

"$SKILL_DIR/scripts/bootstrap_env.sh"
"$SKILL_DIR/scripts/check_env.sh"

echo ""
echo "[sonos-install] Install complete."
echo "[sonos-install] Example playback commands:"
echo "  ./scripts/sonos_netease_play.sh --room 'Living Room' '至少还有你'"
echo "  ./scripts/sonos_qq_play.sh --room 'Living Room' '稻香'"
