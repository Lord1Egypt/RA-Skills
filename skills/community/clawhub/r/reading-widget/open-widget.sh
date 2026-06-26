#!/bin/bash
# Open the reading widget as a frameless Chrome app window.
# Serves via the local helper (http://127.0.0.1:47900) so on-card goal edits
# persist to config.json and data auto-refreshes. Falls back to file:// if the
# helper can't be started.
ROOT="$HOME/Desktop/reading-widget"
PORT=47900
URL="http://127.0.0.1:$PORT/widget.html"
PY="$(command -v python3 || echo /usr/bin/python3)"

# Start the helper if it isn't already responding.
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/widget.html"; then
  "$PY" "$ROOT/server.py" >>"$ROOT/helper.log" 2>&1 &
  for i in $(seq 1 20); do
    curl -s -o /dev/null "http://127.0.0.1:$PORT/widget.html" && break
    sleep 1
  done
fi

# If the helper still isn't up, fall back to the static file.
if ! curl -s -o /dev/null "http://127.0.0.1:$PORT/widget.html"; then
  echo "helper not responding, falling back to file://" >&2
  URL="file://$ROOT/widget.html"
fi

if [ -d "/Applications/Google Chrome.app" ]; then
  open -na "Google Chrome" --args --app="$URL" --window-size=320,640
else
  echo "Chrome not found, opening in default browser." >&2
  open "$URL"
fi
