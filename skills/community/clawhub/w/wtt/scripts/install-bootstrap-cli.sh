#!/usr/bin/env bash
set -euo pipefail

# Install openclaw-wtt-bootstrap as a system-level command.
#
# Usage:
#   bash scripts/install-bootstrap-cli.sh
#   bash scripts/install-bootstrap-cli.sh --target /usr/local/bin/openclaw-wtt-bootstrap
#   bash scripts/install-bootstrap-cli.sh --uninstall

TARGET="/usr/local/bin/openclaw-wtt-bootstrap"
UNINSTALL="0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="$2"
      shift 2
      ;;
    --uninstall)
      UNINSTALL="1"
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$SCRIPT_DIR/.." && pwd)/bin/openclaw-wtt-bootstrap.mjs"

if [[ "$UNINSTALL" == "1" ]]; then
  if [[ -L "$TARGET" || -f "$TARGET" ]]; then
    rm -f "$TARGET"
    echo "Removed $TARGET"
  else
    echo "Nothing to remove: $TARGET"
  fi
  exit 0
fi

if [[ ! -f "$SRC" ]]; then
  echo "Source not found: $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$TARGET")"
ln -sf "$SRC" "$TARGET"
chmod +x "$SRC" "$TARGET"

echo "Installed: $TARGET -> $SRC"
echo "Try: openclaw-wtt-bootstrap --help"
