#!/bin/bash
# Start Chrome with CDP for Weibo operations
# Usage: bash start_chrome.sh

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SRC="$HOME/Library/Application Support/Google/Chrome"
DST="/tmp/chrome-debug-profile"
PORT=19334

# Kill existing debug Chrome
pkill -f "chrome.*$PORT" 2>/dev/null
sleep 1

# Build clean profile from original Chrome data
rm -rf "$DST"
mkdir -p "$DST/Default"

cp "$SRC/Local State" "$DST/" 2>/dev/null

for f in Cookies Cookies-journal "Login Data" "Login Data-journal" \
    "Web Data" "Web Data-journal" Preferences "Secure Preferences" \
    Favicons "Favicons-journal" "Session Storage" "Session Storage-journal" \
    "Local Storage" "Local Storage-journal" IndexedDB Network \
    "Origin Bound Certs" "Origin Bound Certs-journal" \
    "Extension State" "Extension State-journal" \
    "Media Device Salts" "Trust Database" "Trust Database-journal" \
    Sessions; do
    cp -R "$SRC/Default/$f" "$DST/Default/" 2>/dev/null
done

echo "Profile ready ($(du -sh "$DST" | cut -f1))"

# Start Chrome with CDP
"$CHROME" \
    --remote-debugging-port=$PORT \
    --user-data-dir="$DST" \
    --no-first-run \
    --remote-allow-origins="*" \
    --disable-background-timer-throttling \
    &

sleep 3
if curl -s "http://127.0.0.1:$PORT/json/version" > /dev/null 2>&1; then
    echo "Chrome started on port $PORT ✓"
else
    echo "ERROR: Chrome failed to start"
    exit 1
fi
