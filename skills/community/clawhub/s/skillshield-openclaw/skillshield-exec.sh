#!/usr/bin/env bash

set -euo pipefail

COMMAND="${*:-}"
if [[ -z "$COMMAND" ]]; then
    echo "[SkillShield] Refused: missing command argument." >&2
    exit 1
fi

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "[SkillShield] Refused: this marketplace build currently requires Linux + bubblewrap." >&2
    exit 1
fi

for required in cargo curl python3 bwrap; do
    if ! command -v "$required" >/dev/null 2>&1; then
        echo "[SkillShield] Refused: missing required dependency '$required'." >&2
        exit 127
    fi
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAEMON_SRC_DIR="$SCRIPT_DIR/skillshieldd"
CACHE_ROOT="${XDG_CACHE_HOME:-$HOME/.cache}/skillshield-openclaw"
TARGET_DIR="$CACHE_ROOT/target"
SOCKET_PATH="$CACHE_ROOT/skillshieldd.sock"
PID_PATH="$CACHE_ROOT/skillshieldd.pid"
LOG_PATH="$CACHE_ROOT/skillshieldd.log"
MANIFEST_PATH="$DAEMON_SRC_DIR/Cargo.toml"
BIN_PATH="$TARGET_DIR/release/skillshieldd"

mkdir -p "$CACHE_ROOT"

needs_build=0
if [[ ! -x "$BIN_PATH" ]]; then
    needs_build=1
elif find "$DAEMON_SRC_DIR" -type f -newer "$BIN_PATH" | grep -q .; then
    needs_build=1
fi

stop_daemon() {
    if [[ -f "$PID_PATH" ]]; then
        pid="$(cat "$PID_PATH" 2>/dev/null || true)"
        if [[ -n "$pid" ]] && kill -0 "$pid" >/dev/null 2>&1; then
            kill "$pid" >/dev/null 2>&1 || true
        fi
        rm -f "$PID_PATH"
    fi
    rm -f "$SOCKET_PATH"
}

if [[ "$needs_build" -eq 1 ]]; then
    echo "[SkillShield] Building bundled Rust enforcement daemon..." >&2
    CARGO_TARGET_DIR="$TARGET_DIR" cargo build --release --manifest-path "$MANIFEST_PATH" >&2
    stop_daemon
fi

daemon_healthy() {
    curl -fsS --unix-socket "$SOCKET_PATH" http://localhost/health 2>/dev/null
}

start_daemon() {
    rm -f "$SOCKET_PATH"
    SKILLSHIELDD_BIND="unix:$SOCKET_PATH" "$BIN_PATH" >>"$LOG_PATH" 2>&1 &
    echo $! > "$PID_PATH"

    for _ in $(seq 1 40); do
        if daemon_healthy >/dev/null; then
            return 0
        fi
        sleep 0.25
    done

    echo "[SkillShield] Refused: bundled Rust daemon failed to start." >&2
    echo "[SkillShield] See log: $LOG_PATH" >&2
    exit 125
}

if ! daemon_healthy >/dev/null; then
    echo "[SkillShield] Starting bundled Rust enforcement daemon..." >&2
    start_daemon
fi

HEALTH_JSON="$(daemon_healthy)"
EXECUTOR_NAME="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("executor", ""))' <<<"$HEALTH_JSON")"
if [[ "$EXECUTOR_NAME" != "bubblewrap-linux" ]]; then
    echo "[SkillShield] Refused: daemon is not running with the bubblewrap executor." >&2
    exit 127
fi

REQUEST_JSON="$(python3 -c 'import json,os,sys; print(json.dumps({"command": sys.argv[1], "cwd": os.getcwd()}))' "$COMMAND")"
RESPONSE_JSON="$(curl -fsS --unix-socket "$SOCKET_PATH" -H 'Content-Type: application/json' -X POST http://localhost/v1/execute -d "$REQUEST_JSON")"

RESPONSE_JSON="$RESPONSE_JSON" python3 - <<'PY'
import json
import os
import sys

payload = json.loads(os.environ["RESPONSE_JSON"])
outcome = payload.get("outcome") or {}
stdout = outcome.get("stdout", "")
stderr = outcome.get("stderr", "")
code = int(outcome.get("exitCode", 125))

if stdout:
    sys.stdout.write(stdout)
if stderr:
    sys.stderr.write(stderr)
    if not stderr.endswith("\n"):
        sys.stderr.write("\n")

sys.exit(code)
PY
