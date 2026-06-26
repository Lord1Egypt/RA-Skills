#!/bin/bash
# manage_server.sh - Manage the Stock Invest Master reports web server
#
# Usage:
#   bash manage_server.sh start   - Start the server (if not already running)
#   bash manage_server.sh stop    - Stop the running server
#   bash manage_server.sh restart - Restart the server
#   bash manage_server.sh status  - Check if server is running
#   bash manage_server.sh ensure  - Check + auto-start if not running (used by skill)
#
# Port can be overridden: PORT=9999 bash manage_server.sh start

set -e

REPORTS_DIR="${HOME}/.stock-invest-master"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="${REPORTS_DIR}/.server.pid"
LOG_FILE="${REPORTS_DIR}/server.log"
PORT="${PORT:-8888}"

# Ensure reports directory exists
mkdir -p "${REPORTS_DIR}"

is_running() {
    if [ -f "${PID_FILE}" ]; then
        PID=$(cat "${PID_FILE}" 2>/dev/null)
        if [ -n "${PID}" ] && kill -0 "${PID}" 2>/dev/null; then
            return 0
        fi
    fi
    # Fallback: check by process name + port
    if pgrep -f "serve_reports.py.*${PORT}" > /dev/null 2>&1; then
        return 0
    fi
    return 1
}

do_start() {
    if is_running; then
        echo "Server is already running on port ${PORT}."
        return 0
    fi

    echo "Starting reports server on port ${PORT}..."
    nohup python3 "${SKILL_DIR}/serve_reports.py" "${PORT}" > "${LOG_FILE}" 2>&1 &
    SERVER_PID=$!
    echo "${SERVER_PID}" > "${PID_FILE}"

    # Wait up to 5 seconds for server to start
    for i in $(seq 1 10); do
        sleep 0.5
        if is_running; then
            echo "Server started successfully (PID: ${SERVER_PID})."
            echo "  URL: http://127.0.0.1:${PORT}"
            echo "  Health: http://127.0.0.1:${PORT}/health"
            return 0
        fi
    done

    echo "WARNING: Server may not have started. Check ${LOG_FILE} for details."
    return 1
}

do_stop() {
    if [ -f "${PID_FILE}" ]; then
        PID=$(cat "${PID_FILE}" 2>/dev/null)
        if [ -n "${PID}" ]; then
            kill "${PID}" 2>/dev/null || true
            echo "Sent SIGTERM to PID ${PID}."
        fi
    fi

    # Also kill any remaining serve_reports.py processes
    pkill -f "serve_reports.py.*${PORT}" 2>/dev/null || true

    rm -f "${PID_FILE}"
    echo "Server stopped."
}

do_status() {
    if is_running; then
        PID=""
        if [ -f "${PID_FILE}" ]; then
            PID=$(cat "${PID_FILE}" 2>/dev/null)
        fi
        echo "Server is RUNNING on port ${PORT} (PID: ${PID})."
        echo "  URL: http://127.0.0.1:${PORT}"
        echo "  Health: http://127.0.0.1:${PORT}/health"
        # Quick health check
        if command -v curl > /dev/null 2>&1; then
            HEALTH=$(curl -s --max-time 2 "http://127.0.0.1:${PORT}/health" 2>/dev/null || echo "unreachable")
            if [ "${HEALTH}" != "unreachable" ]; then
                echo "  Health check: ${HEALTH}"
            fi
        fi
        return 0
    else
        echo "Server is NOT running."
        return 1
    fi
}

do_ensure() {
    # This is the key function called by the skill after report generation.
    # It checks if the server is running, and starts it if not.
    if is_running; then
        echo "[server] Reports server is already running on port ${PORT}."
        return 0
    fi

    echo "[server] Reports server not detected. Starting on port ${PORT}..."
    do_start
}

case "${1}" in
    start)
        do_start
        ;;
    stop)
        do_stop
        ;;
    restart)
        do_stop
        sleep 1
        do_start
        ;;
    status)
        do_status
        ;;
    ensure)
        do_ensure
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|ensure}"
        echo ""
        echo "  start   - Start the server (if not already running)"
        echo "  stop    - Stop the running server"
        echo "  restart - Restart the server"
        echo "  status  - Check if server is running"
        echo "  ensure  - Check + auto-start if not running (for skill integration)"
        exit 1
        ;;
esac
