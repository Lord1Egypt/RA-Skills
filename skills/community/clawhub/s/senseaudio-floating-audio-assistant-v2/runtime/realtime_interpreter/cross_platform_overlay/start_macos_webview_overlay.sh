#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST_SWIFT="$SCRIPT_DIR/overlay_webview_host.swift"
HOST_BIN="$SCRIPT_DIR/overlay_webview_host_app"
DIST_DIR="$SCRIPT_DIR/dist"

if [ ! -f "$DIST_DIR/index.html" ]; then
  echo "Missing built frontend. Run: npm run build" >&2
  exit 1
fi

if [ ! -x "$HOST_BIN" ] || [ "$HOST_SWIFT" -nt "$HOST_BIN" ]; then
  swiftc "$HOST_SWIFT" -o "$HOST_BIN" -framework AppKit -framework WebKit
fi

exec "$HOST_BIN" "$DIST_DIR"
