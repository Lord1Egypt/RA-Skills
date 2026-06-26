#!/usr/bin/env bash
set -e

# Stop tesla-http-proxy.

# --- Resolve data dir/workspace robustly ---
find_workspace_from_pwd() {
    local d="${PWD:-$(pwd)}"
    while [ "$d" != "/" ]; do
        if [ -f "$d/AGENTS.md" ] || [ -f "$d/SOUL.md" ]; then
            printf '%s
' "$d"
            return 0
        fi
        d="$(dirname "$d")"
    done
    return 1
}

if [ -n "$OPENCLAW_WORKSPACE" ]; then
    WORKSPACE="$OPENCLAW_WORKSPACE"
elif WORKSPACE="$(find_workspace_from_pwd)"; then
    :
elif [ -f "$HOME/clawd/AGENTS.md" ] || [ -f "$HOME/clawd/SOUL.md" ]; then
    WORKSPACE="$HOME/clawd"
else
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    DATA_DIR="$(PYTHONPATH="$SCRIPT_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 -c 'from store import default_dir; print(default_dir())')"
    WORKSPACE="$(cd "$(dirname "$DATA_DIR")" && pwd)"
fi

DATA_DIR="${DATA_DIR:-${WORKSPACE}/tesla-fleet-api}"
PID_FILE="${DATA_DIR}/proxy/proxy.pid"

if [ ! -f "${PID_FILE}" ]; then
    echo "Proxy is not running (no PID file)"
    exit 0
fi

PROXY_PID=$(cat "${PID_FILE}")

if ! ps -p "${PROXY_PID}" > /dev/null 2>&1; then
    echo "Proxy is not running (stale PID file)"
    rm -f "${PID_FILE}"
    exit 0
fi

echo "Stopping tesla-http-proxy (PID: ${PROXY_PID})..."
kill "${PROXY_PID}"

for i in $(seq 1 10); do
    if ! ps -p "${PROXY_PID}" > /dev/null 2>&1; then
        rm -f "${PID_FILE}"
        echo "✓ Proxy stopped"
        exit 0
    fi
    sleep 0.5
done

kill -9 "${PROXY_PID}" 2>/dev/null
rm -f "${PID_FILE}"
echo "✓ Proxy stopped (forced)"
