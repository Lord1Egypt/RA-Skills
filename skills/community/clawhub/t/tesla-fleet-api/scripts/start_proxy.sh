#!/usr/bin/env bash
set -e

# Start tesla-http-proxy in background.
# If the binary isn't installed, directs the user to SETUP.md.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

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
    DATA_DIR="$(PYTHONPATH="$SCRIPT_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 -c 'from store import default_dir; print(default_dir())')"
    WORKSPACE="$(cd "$(dirname "$DATA_DIR")" && pwd)"
fi

DATA_DIR="${DATA_DIR:-${WORKSPACE}/tesla-fleet-api}"

PROXY_DIR="${DATA_DIR}/proxy"
GO_BIN="${GOPATH:-$HOME/go}/bin"
PROXY_BIN="${GO_BIN}/tesla-http-proxy"
PID_FILE="${PROXY_DIR}/proxy.pid"
LOG_FILE="${PROXY_DIR}/proxy.log"
PRIVATE_KEY="${DATA_DIR}/private-key.pem"

# --- Check binary exists ---
if [ ! -f "${PROXY_BIN}" ]; then
    echo "Error: tesla-http-proxy not found at ${PROXY_BIN}" >&2
    echo "" >&2
    echo "See the Proxy Setup section in:" >&2
    echo "  ${SKILL_DIR}/SETUP.md" >&2
    exit 1
fi

# --- Check private key exists ---
if [ ! -f "${PRIVATE_KEY}" ]; then
    echo "Error: Tesla private key not found at ${PRIVATE_KEY}" >&2
    echo "" >&2
    echo "Place your EC private key at:" >&2
    echo "  ${PRIVATE_KEY}" >&2
    echo "" >&2
    echo "See SETUP.md for key generation instructions." >&2
    exit 1
fi

# --- Generate TLS certs if missing ---
mkdir -p "${PROXY_DIR}"
if [ ! -f "${PROXY_DIR}/tls-cert.pem" ] || [ ! -f "${PROXY_DIR}/tls-key.pem" ]; then
    echo "Generating self-signed TLS certificate for localhost..."
    openssl req -x509 -newkey rsa:4096 \
        -keyout "${PROXY_DIR}/tls-key.pem" \
        -out "${PROXY_DIR}/tls-cert.pem" \
        -days 365 -nodes -subj "/CN=localhost" > /dev/null 2>&1
    chmod 600 "${PROXY_DIR}/tls-key.pem"
    echo "✓ Generated TLS certificates in ${PROXY_DIR}"
fi

# --- Check if already running ---
if [ -f "${PID_FILE}" ]; then
    OLD_PID=$(cat "${PID_FILE}")
    if ps -p "${OLD_PID}" > /dev/null 2>&1; then
        echo "Proxy is already running (PID: ${OLD_PID})"
        exit 0
    else
        rm -f "${PID_FILE}"
    fi
fi

# --- Start ---
echo "Starting tesla-http-proxy..."

nohup "${PROXY_BIN}" \
    -key-file "${PRIVATE_KEY}" \
    -tls-key "${PROXY_DIR}/tls-key.pem" \
    -cert "${PROXY_DIR}/tls-cert.pem" \
    -host localhost \
    -port 4443 \
    >> "${LOG_FILE}" 2>&1 &

PROXY_PID=$!
echo "${PROXY_PID}" > "${PID_FILE}"

sleep 2
if ps -p "${PROXY_PID}" > /dev/null 2>&1; then
    echo "✓ Proxy started (PID: ${PROXY_PID})"
    echo "  Listening on: https://localhost:4443"
    echo "  Logs: ${LOG_FILE}"
else
    echo "Error: Proxy failed to start. Check logs: ${LOG_FILE}" >&2
    rm -f "${PID_FILE}"
    exit 1
fi
