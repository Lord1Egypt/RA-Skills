#!/bin/bash
# stellar-trails dev server v7.2.2 — custom no-cache HTTP server + crash recovery
#
# Serves /home/z/my-project/.zscripts/ on port :3000 with Cache-Control: no-store
# headers (bypass browser heuristic caching).
#
# v7.2.2: Added `while true` crash recovery loop. If python3 process dies
# (OOM, signal, etc), dev.sh auto-restarts after 1 second. Previous v7.2.0
# had no loop → single python crash = popup preview down forever until
# session restart.
#
# Usage (Path B — non-ZAI standalone):
#   1. Copy this file to /home/z/my-project/.zscripts/dev.sh
#   2. chmod +x /home/z/my-project/.zscripts/dev.sh
#   3. bash /home/z/my-project/.zscripts/dev.sh
#
# On ZAI platform, /start.sh auto-launches /home/z/my-project/.zscripts/dev.sh
# at session start. This file is the source — copy to .zscripts/ to activate.
#
# No external dependencies. Pure Python 3 stdlib. No network. No git ops.
# No writes outside /home/z/my-project/.zscripts/.

set -e

ZSCRIPTS_DIR="${ZSCRIPTS_DIR:-/home/z/my-project/.zscripts}"
PORT="${PORT:-3000}"

mkdir -p "$ZSCRIPTS_DIR"
cd "$ZSCRIPTS_DIR"

# Port guard — exit gracefully if already in use
if command -v ss >/dev/null 2>&1 && ss -tlnp 2>/dev/null | grep -q ":$PORT "; then
  echo "[dev.sh] Port :$PORT already in use — not starting"
  exit 0
fi

echo "[dev.sh] Serving $ZSCRIPTS_DIR on :$PORT with Cache-Control: no-store (crash recovery enabled)"

# Crash recovery loop — if python3 exits, restart after 1 second
while true; do
  python3 -c "
import http.server, socketserver, os, signal, sys

class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, format, *args):
        pass  # suppress access logs

def shutdown(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

with ReuseTCPServer(('0.0.0.0', $PORT), NoCacheHandler) as httpd:
    httpd.serve_forever()
" 2>/dev/null || true
  echo "[dev.sh] python3 exited — restarting in 1s (crash recovery)"
  sleep 1
done
