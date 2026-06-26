#!/usr/bin/env bash
# unformal-listen — real-time listener for Unformal conversation completions.
#
# Connects to the Unformal SSE stream and shows a macOS notification
# every time someone completes a conversation on the given Pulse.
# Also writes each event to ~/.unformal/inbox/<timestamp>.json so your
# Claude Code session can read it on demand.
#
# Usage:
#   unformal-listen                             # list your Pulses + show usage
#   unformal-listen <pulse_id>                  # listen to a specific Pulse
#
# Requires UNFORMAL_API_KEY env var (or pass via --key=<key>).
# Works on macOS (uses osascript for notifications). On Linux it falls
# back to notify-send if available, otherwise just logs to stdout.

set -euo pipefail

# ── Parse args ──────────────────────────────────────────────────────────
API_KEY="${UNFORMAL_API_KEY:-}"
PULSE_ID=""
for arg in "$@"; do
  case "$arg" in
    --key=*) API_KEY="${arg#--key=}" ;;
    --help|-h) grep -E '^# ' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) if [ -z "$PULSE_ID" ]; then PULSE_ID="$arg"; fi ;;
  esac
done

if [ -z "$API_KEY" ]; then
  echo "Error: no API key found."
  echo ""
  echo "Set UNFORMAL_API_KEY env var, or pass --key=<your_key>"
  echo "Get a key at https://unformal.ai/studio/settings"
  exit 1
fi

mkdir -p "$HOME/.unformal/inbox"

# ── No pulse ID → list Pulses ───────────────────────────────────────────
if [ -z "$PULSE_ID" ]; then
  echo "Your Pulses:"
  echo ""
  curl -fsS -H "Authorization: Bearer $API_KEY" \
    "https://unformal.ai/api/v1/pulses" | \
    python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    items = d.get("data", [])
    if not items:
        print("  (no pulses yet)")
    for p in items:
        pid = p.get("id", "")
        status = p.get("status", "?")
        slug = p.get("slug", "")
        intent = (p.get("intention") or "")[:55]
        print("  " + pid + "  [" + status.ljust(8) + "]  /" + slug.ljust(30) + "  " + intent)
except Exception as e:
    print("Error parsing pulses: " + str(e))
'
  echo ""
  echo "Usage:  unformal-listen <pulse_id>"
  exit 0
fi

# ── Connect to SSE stream ───────────────────────────────────────────────
NOTIFY_FN() {
  local title="$1"
  local msg="$2"
  if command -v osascript >/dev/null 2>&1; then
    # macOS
    osascript -e "display notification \"${msg//\"/\\\"}\" with title \"${title//\"/\\\"}\" sound name \"Glass\"" 2>/dev/null || true
  elif command -v notify-send >/dev/null 2>&1; then
    # Linux
    notify-send "$title" "$msg" || true
  fi
}

echo "🎧 Listening for new responses on pulse $PULSE_ID..."
echo "   Events saved to: ~/.unformal/inbox/"
echo "   Press Ctrl+C to stop. (auto-reconnects on disconnect)"
echo ""

# Catch Ctrl+C cleanly
trap 'echo; echo "Stopped."; exit 0' INT TERM

# Auto-reconnect loop. Serverless hosts (Vercel, Cloudflare, etc.) cap
# connection duration, so we reconnect whenever the stream closes.
while true; do
  event=""
  curl --no-buffer -fsS -N \
    -H "Authorization: Bearer $API_KEY" \
    -H "Accept: text/event-stream" \
    "https://unformal.ai/api/v1/pulses/$PULSE_ID/stream" 2>/dev/null | \
  while IFS= read -r line; do
    case "$line" in
      event:*)
        event="${line#event: }"
        event="${event## }"
        ;;
      data:*)
        data="${line#data: }"
        data="${data## }"

        case "$event" in
          connected)
            echo "✓ $(date +%H:%M:%S) connected"
            ;;
          conversation.completed)
            ts=$(date +%Y%m%d-%H%M%S)
            file="$HOME/.unformal/inbox/${ts}.json"
            printf '%s' "$data" > "$file"

            summary=$(printf '%s' "$data" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    echo = d.get("echo") or {}
    s = echo.get("summary") or d.get("summary") or "New response received"
    sys.stdout.write(s[:180])
except:
    sys.stdout.write("New response received")
' 2>/dev/null || echo "New response received")

            echo "✨ $(date +%H:%M:%S) $summary"
            NOTIFY_FN "Unformal — new response" "$summary"
            ;;
          ping)
            : # keepalive, ignore
            ;;
          timeout)
            : # server-requested reconnect, outer loop handles it
            ;;
        esac
        event=""
        ;;
      "")
        event=""
        ;;
    esac
  done

  # Connection closed — wait 2s then reconnect (unless killed)
  sleep 2
done
