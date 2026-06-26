#!/usr/bin/env bash
# start_chrome.sh - Launch Chrome with remote debugging port for Playwright CDP connection
# Usage: ./start_chrome.sh [port]

set -euo pipefail

PORT="${1:-9222}"
GEMINI_URL="https://gemini.google.com"
USER_DATA_DIR="$HOME/.openclaw/workspace/chrome_profile"
LOCK_FILE="/tmp/openclaw-chrome.lock"
LOCK_TIMEOUT=30

# Function: Check if Chrome CDP is already available (cross-platform)
check_cdp_available() {
    curl -s --connect-timeout 2 "http://localhost:$PORT/json/version" > /dev/null 2>&1
}

# Function: Acquire lock (cross-platform, no flock needed)
acquire_lock() {
    local start_time=$(date +%s)
    while true; do
        # Try to create lock file atomically
        if (set -o noclobber; echo $$ > "$LOCK_FILE") 2>/dev/null; then
            trap 'rm -f "$LOCK_FILE"' EXIT
            return 0
        fi

        # Check if lock is stale (older than LOCK_TIMEOUT seconds)
        if [ -f "$LOCK_FILE" ]; then
            local lock_age=$(($(date +%s) - $(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE" 2>/dev/null || echo 0)))
            if [ "$lock_age" -gt "$LOCK_TIMEOUT" ]; then
                echo "[!] Removing stale lock file (age: ${lock_age}s)"
                rm -f "$LOCK_FILE"
                continue
            fi
        fi

        # Check if Chrome became available while waiting
        if check_cdp_available; then
            echo "[*] Chrome is now available (started by another process)"
            return 1  # Exit without lock, Chrome is ready
        fi

        local elapsed=$(($(date +%s) - start_time))
        if [ "$elapsed" -gt "$LOCK_TIMEOUT" ]; then
            echo "[!] Timeout waiting for lock. Another process may be stuck."
            return 2
        fi

        echo "[*] Another process is starting Chrome, waiting... (${elapsed}s)"
        sleep 1
    done
}

# Main logic
echo "[*] Checking if Chrome CDP is already available on port $PORT..."
if check_cdp_available; then
    echo "[*] Chrome is already running with CDP on port $PORT"
    echo "[*] CDP endpoint: http://localhost:$PORT"
    exit 0
fi

# Acquire lock before starting
acquire_lock
lock_result=$?
if [ $lock_result -eq 1 ]; then
    # Chrome became available while waiting
    exit 0
elif [ $lock_result -eq 2 ]; then
    exit 1
fi

# Double-check after acquiring lock (another process might have started it)
if check_cdp_available; then
    echo "[*] Chrome is already running (started by another process)"
    exit 0
fi

# Detect Chrome binary
CHROME_BIN=""
for candidate in \
    "google-chrome" \
    "google-chrome-stable" \
    "google-chrome-beta" \
    "google-chrome-canary" \
    "chromium" \
    "chromium-browser" \
    "/usr/bin/google-chrome" \
    "/usr/bin/chromium-browser" \
    "/snap/bin/chromium" \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta" \
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium"; do
    if command -v "$candidate" &>/dev/null || [ -x "$candidate" ]; then
        CHROME_BIN="$candidate"
        break
    fi
done

if [ -z "$CHROME_BIN" ]; then
    echo "ERROR: Chrome/Chromium not found. Please install Google Chrome."
    exit 1
fi

echo "[*] Starting Chrome with remote debugging on port $PORT..."
echo "[*] Chrome binary: $CHROME_BIN"
echo ""
echo "IMPORTANT:"
echo "  1. Log in to your Google account in the opened Chrome window"
echo "  2. Navigate to $GEMINI_URL to verify access"
echo "  3. Keep this Chrome window open while using the web-chat skill"
echo ""

mkdir -p "$USER_DATA_DIR"

"$CHROME_BIN" \
    --remote-debugging-port="$PORT" \
    --user-data-dir="$USER_DATA_DIR" \
    --no-first-run \
    --no-default-browser-check \
    "$GEMINI_URL" &

CHROME_PID=$!
echo "[*] Chrome started (PID: $CHROME_PID)"

# Wait for CDP to become available
echo "[*] Waiting for CDP endpoint..."
for i in {1..30}; do
    if check_cdp_available; then
        echo "[*] CDP endpoint ready: http://localhost:$PORT"
        exit 0
    fi
    sleep 1
done

echo "[!] Warning: CDP endpoint not responding after 30s"
echo "[*] Chrome may still be starting. Check http://localhost:$PORT/json/version"
exit 0
