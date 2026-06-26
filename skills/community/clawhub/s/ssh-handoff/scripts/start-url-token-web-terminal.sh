#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="${1:-ssh-handoff}"
REQUESTED_HOST="${HOST:-127.0.0.1}"
REQUESTED_PORT="${PORT:-48080}"
REQUESTED_CLIENT_IP="${CLIENT_IP:-}"
TTL_MINUTES="${TTL_MINUTES:-30}"
BIND_SCOPE="${BIND_SCOPE:-local}"
UPSTREAM_HOST="127.0.0.1"
REQUESTED_UPSTREAM_PORT="${UPSTREAM_PORT:-48081}"
COOKIE_SECURE="${COOKIE_SECURE:-}"
REQUESTED_EXPECTED_HOST="${EXPECTED_HOST:-${REQUESTED_HOST}:${REQUESTED_PORT}}"
REQUESTED_EXPECTED_ORIGIN="${EXPECTED_ORIGIN:-}"
FORBID_REUSE_IF_AUTHENTICATED="${FORBID_REUSE_IF_AUTHENTICATED:-0}"
REPLACE_EXISTING="${REPLACE_EXISTING:-0}"
AUTH_GUARD_REGEX="${AUTH_GUARD_REGEX:-(^|[^[:alnum:]_])(Last login:|[@][A-Za-z0-9._-]+:|Welcome to|Linux [A-Za-z0-9._-]+|[#$] $)}"
SESSION_NAME_SAFE="$(printf '%s' "$SESSION_NAME" | tr -c '[:alnum:]._:-' '_')"
STATE_FILE="/tmp/ssh-handoff-${SESSION_NAME_SAFE}.env"
HOST="$REQUESTED_HOST"
PORT="$REQUESTED_PORT"
CLIENT_IP="$REQUESTED_CLIENT_IP"
UPSTREAM_PORT="$REQUESTED_UPSTREAM_PORT"
EXPECTED_HOST="$REQUESTED_EXPECTED_HOST"
EXPECTED_ORIGIN="$REQUESTED_EXPECTED_ORIGIN"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing dependency: $1" >&2
    exit 1
  }
}

bool_true() {
  [[ "$1" == "1" || "$1" =~ ^([Tt][Rr][Uu][Ee]|[Yy][Ee][Ss]|[Oo][Nn])$ ]]
}

cleanup_existing_runtime() {
  local state_file="$1"
  if [[ ! -f "$state_file" ]]; then
    return 0
  fi

  # shellcheck disable=SC1090
  source "$state_file"
  if [[ -n "${CLEANUP_CMD:-}" ]]; then
    bash -lc "$CLEANUP_CMD" >/dev/null 2>&1 || true
  else
    if [[ -n "${PROXY_PID:-}" ]] && kill -0 "${PROXY_PID}" 2>/dev/null; then
      kill "${PROXY_PID}" 2>/dev/null || true
    fi
    if [[ -n "${TTYD_PID:-}" ]] && kill -0 "${TTYD_PID}" 2>/dev/null; then
      kill "${TTYD_PID}" 2>/dev/null || true
    fi
    if [[ -n "${RUNTIME_DIR:-}" ]] && [[ -d "${RUNTIME_DIR}" ]]; then
      rm -rf "${RUNTIME_DIR}" || true
    fi
  fi
  rm -f "$state_file"
}

existing_runtime_alive() {
  local state_file="$1"
  if [[ ! -f "$state_file" ]]; then
    return 1
  fi

  # shellcheck disable=SC1090
  source "$state_file"
  if [[ -n "${PROXY_PID:-}" ]] && kill -0 "${PROXY_PID}" 2>/dev/null; then
    return 0
  fi
  if [[ -n "${TTYD_PID:-}" ]] && kill -0 "${TTYD_PID}" 2>/dev/null; then
    return 0
  fi
  return 1
}

pane_snapshot_tail() {
  tmux capture-pane -t "$SESSION_NAME" -p -S -80 2>/dev/null | tail -20 || true
}

write_state_value() {
  local key="$1"
  local value="${2-}"
  printf '%s=%q\n' "$key" "$value"
}

print_existing_runtime_details() {
  local message="$1"
  local pane_tail
  pane_tail="$(pane_snapshot_tail)"
  cat <<EOF
READY=0
SESSION_NAME=$SESSION_NAME
EXISTING_SESSION=1
MESSAGE=$message
EXISTING_HOST=${EXISTING_HOST:-}
EXISTING_PORT=${EXISTING_PORT:-}
EXISTING_URL=${EXISTING_URL:-}
EXISTING_EXPIRES_AT=${EXISTING_EXPIRES_AT:-}
EXISTING_PROXY_PID=${EXISTING_PROXY_PID:-}
EXISTING_TTYD_PID=${EXISTING_TTYD_PID:-}
EXISTING_RUNTIME_DIR=${EXISTING_RUNTIME_DIR:-}
EXISTING_STATE_FILE=$STATE_FILE
EXISTING_CLEANUP_CMD=${EXISTING_CLEANUP_CMD:-}
EXISTING_PANE_TAIL<<'__SSH_HANDOFF_PANE__'
$pane_tail
__SSH_HANDOFF_PANE__
EOF
}

need tmux
need ttyd
need python3
need node

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if existing_runtime_alive "$STATE_FILE"; then
  EXISTING_HOST=''
  EXISTING_PORT=''
  EXISTING_URL=''
  EXISTING_EXPIRES_AT=''
  EXISTING_PROXY_PID=''
  EXISTING_TTYD_PID=''
  EXISTING_RUNTIME_DIR=''
  EXISTING_CLEANUP_CMD=''
  # shellcheck disable=SC1090
  source "$STATE_FILE"
  EXISTING_HOST="${HOST:-}"
  EXISTING_PORT="${PORT:-}"
  EXISTING_URL="${URL:-}"
  EXISTING_EXPIRES_AT="${EXPIRES_AT:-}"
  EXISTING_PROXY_PID="${PROXY_PID:-}"
  EXISTING_TTYD_PID="${TTYD_PID:-}"
  EXISTING_RUNTIME_DIR="${RUNTIME_DIR:-}"
  EXISTING_CLEANUP_CMD="${CLEANUP_CMD:-}"

  HOST="$REQUESTED_HOST"
  PORT="$REQUESTED_PORT"
  CLIENT_IP="$REQUESTED_CLIENT_IP"
  UPSTREAM_PORT="$REQUESTED_UPSTREAM_PORT"
  EXPECTED_HOST="$REQUESTED_EXPECTED_HOST"
  EXPECTED_ORIGIN="$REQUESTED_EXPECTED_ORIGIN"

  if ! bool_true "$REPLACE_EXISTING"; then
    print_existing_runtime_details "An active web handoff already exists for this tmux session. Ask the user whether to replace it. If they do not want that, relaunch on another port and update firewall rules if LAN access is needed."
    exit 0
  fi
  cleanup_existing_runtime "$STATE_FILE"
  HOST="$REQUESTED_HOST"
  PORT="$REQUESTED_PORT"
  CLIENT_IP="$REQUESTED_CLIENT_IP"
  UPSTREAM_PORT="$REQUESTED_UPSTREAM_PORT"
  EXPECTED_HOST="$REQUESTED_EXPECTED_HOST"
  EXPECTED_ORIGIN="$REQUESTED_EXPECTED_ORIGIN"
  sleep 0.2
else
  rm -f "$STATE_FILE"
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  tmux new-session -d -s "$SESSION_NAME"
fi

if bool_true "$FORBID_REUSE_IF_AUTHENTICATED"; then
  PANE_SNAPSHOT="$(tmux capture-pane -t "$SESSION_NAME" -p -S -200 2>/dev/null || true)"
  if printf '%s\n' "$PANE_SNAPSHOT" | grep -Eiq "$AUTH_GUARD_REGEX"; then
    echo "Refusing to launch: tmux session appears already authenticated. Set FORBID_REUSE_IF_AUTHENTICATED=0 to override." >&2
    exit 1
  fi
fi

if ss -ltn | awk '{print $4}' | grep -qE "(^|:)$UPSTREAM_PORT$"; then
  cat <<EOF
READY=0
SESSION_NAME=$SESSION_NAME
PORT_CONFLICT=1
CONFLICT_KIND=upstream
CONFLICT_PORT=$UPSTREAM_PORT
MESSAGE=The requested upstream port is already in use. Ask the user whether to free/replace the existing session. If they prefer not to, choose another UPSTREAM_PORT and relaunch. If LAN access is involved, remind them to update firewall rules when needed.
EOF
  exit 0
fi

if ss -ltn | awk '{print $4}' | grep -qE "(^|:)$PORT$"; then
  cat <<EOF
READY=0
SESSION_NAME=$SESSION_NAME
PORT_CONFLICT=1
CONFLICT_KIND=proxy
CONFLICT_PORT=$PORT
MESSAGE=The requested frontend port is already in use. Ask the user whether to free/replace the existing session. If they prefer not to, choose another PORT and relaunch. If LAN access is involved, remind them to update firewall rules when needed.
EOF
  exit 0
fi

ACCESS_TOKEN="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"

SESSION_SECRET="$(python3 - <<'PY'
import secrets
print(secrets.token_urlsafe(24))
PY
)"

EXPIRES_AT="$(TTL_FOR_PY="$TTL_MINUTES" python3 - <<'PY'
import os
from datetime import datetime, timedelta, timezone
minutes = int(os.environ['TTL_FOR_PY'])
print((datetime.now(timezone.utc) + timedelta(minutes=minutes)).isoformat())
PY
)"

RUNTIME_DIR="$(mktemp -d -t ssh-handoff-${SESSION_NAME}-XXXXXX)"
PROXY_INFO_FILE="$RUNTIME_DIR/proxy-info.json"
PROXY_LOG_FILE="$RUNTIME_DIR/proxy.log"
TTYD_LOG_FILE="$RUNTIME_DIR/ttyd.log"
CLEANUP_SCRIPT="$RUNTIME_DIR/cleanup.sh"
METADATA_FILE="$RUNTIME_DIR/meta.env"
: > "$PROXY_INFO_FILE"

if [[ -z "$EXPECTED_ORIGIN" ]]; then
  if [[ -n "$COOKIE_SECURE" && "$COOKIE_SECURE" != "0" ]]; then
    EXPECTED_ORIGIN="https://$EXPECTED_HOST"
  else
    EXPECTED_ORIGIN="http://$EXPECTED_HOST"
  fi
fi

cat > "$CLEANUP_SCRIPT" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
TTYD_PID="${TTYD_PID:-}"
PROXY_PID="${PROXY_PID:-}"
RUNTIME_DIR="${RUNTIME_DIR:-}"
STATE_FILE="${STATE_FILE:-}"
if [[ -n "$PROXY_PID" ]] && kill -0 "$PROXY_PID" 2>/dev/null; then
  kill "$PROXY_PID" 2>/dev/null || true
fi
if [[ -n "$TTYD_PID" ]] && kill -0 "$TTYD_PID" 2>/dev/null; then
  kill "$TTYD_PID" 2>/dev/null || true
fi
sleep 0.2
if [[ -n "$PROXY_PID" ]] && kill -0 "$PROXY_PID" 2>/dev/null; then
  kill -9 "$PROXY_PID" 2>/dev/null || true
fi
if [[ -n "$TTYD_PID" ]] && kill -0 "$TTYD_PID" 2>/dev/null; then
  kill -9 "$TTYD_PID" 2>/dev/null || true
fi
if [[ -n "$RUNTIME_DIR" ]] && [[ -d "$RUNTIME_DIR" ]]; then
  rm -rf "$RUNTIME_DIR"
fi
if [[ -n "$STATE_FILE" ]]; then
  rm -f "$STATE_FILE"
fi
EOF
chmod 700 "$CLEANUP_SCRIPT"

nohup ttyd -W -i "$UPSTREAM_HOST" -p "$UPSTREAM_PORT" tmux attach -t "$SESSION_NAME" >"$TTYD_LOG_FILE" 2>&1 &
TTYD_PID=$!

nohup env \
  LISTEN_HOST="$HOST" \
  LISTEN_PORT="$PORT" \
  UPSTREAM_HOST="$UPSTREAM_HOST" \
  UPSTREAM_PORT="$UPSTREAM_PORT" \
  ACCESS_TOKEN="$ACCESS_TOKEN" \
  SESSION_SECRET="$SESSION_SECRET" \
  TTL_MS="$((TTL_MINUTES * 60 * 1000))" \
  COOKIE_SECURE="$COOKIE_SECURE" \
  EXPECTED_HOST="$EXPECTED_HOST" \
  EXPECTED_ORIGIN="$EXPECTED_ORIGIN" \
  ALLOWED_CLIENT_IP="$CLIENT_IP" \
  node "$SCRIPT_DIR/url-token-proxy.js" >"$PROXY_INFO_FILE" 2>"$PROXY_LOG_FILE" &
PROXY_PID=$!

{
  write_state_value STATE_FILE "$STATE_FILE"
  write_state_value RUNTIME_DIR "$RUNTIME_DIR"
  write_state_value TTYD_PID "$TTYD_PID"
  write_state_value PROXY_PID "$PROXY_PID"
  write_state_value SESSION_NAME "$SESSION_NAME"
  write_state_value HOST "$HOST"
  write_state_value PORT "$PORT"
  write_state_value UPSTREAM_PORT "$UPSTREAM_PORT"
  write_state_value CLIENT_IP "$CLIENT_IP"
  write_state_value EXPECTED_HOST "$EXPECTED_HOST"
  write_state_value EXPECTED_ORIGIN "$EXPECTED_ORIGIN"
  write_state_value EXPIRES_AT "$EXPIRES_AT"
} > "$METADATA_FILE"

for _ in $(seq 1 50); do
  if [[ -s "$PROXY_INFO_FILE" ]]; then
    break
  fi
  sleep 0.1
done

if [[ ! -s "$PROXY_INFO_FILE" ]]; then
  TTYD_PID="$TTYD_PID" PROXY_PID="$PROXY_PID" RUNTIME_DIR="$RUNTIME_DIR" STATE_FILE="$STATE_FILE" "$CLEANUP_SCRIPT" || true
  echo "Proxy failed to start" >&2
  echo "See $PROXY_LOG_FILE" >&2
  exit 1
fi

PROXY_JSON="$(cat "$PROXY_INFO_FILE")"
PROXY_PORT="$(printf '%s' "$PROXY_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["port"])')"

if ! kill -0 "$TTYD_PID" 2>/dev/null; then
  PROXY_PID="$PROXY_PID" RUNTIME_DIR="$RUNTIME_DIR" STATE_FILE="$STATE_FILE" "$CLEANUP_SCRIPT" || true
  echo "ttyd exited unexpectedly" >&2
  exit 1
fi

if ! kill -0 "$PROXY_PID" 2>/dev/null; then
  TTYD_PID="$TTYD_PID" RUNTIME_DIR="$RUNTIME_DIR" STATE_FILE="$STATE_FILE" "$CLEANUP_SCRIPT" || true
  echo "proxy exited unexpectedly" >&2
  echo "See $PROXY_LOG_FILE" >&2
  exit 1
fi

TTL_SECONDS="$((TTL_MINUTES * 60))"
nohup bash -lc "sleep '$TTL_SECONDS'; TTYD_PID='$TTYD_PID' PROXY_PID='$PROXY_PID' RUNTIME_DIR='$RUNTIME_DIR' STATE_FILE='$STATE_FILE' '$CLEANUP_SCRIPT'" >/dev/null 2>&1 &
CLEANUP_WATCHER_PID=$!

URL="http://$HOST:$PROXY_PORT/?token=$ACCESS_TOKEN"
CLEANUP_CMD="TTYD_PID=$TTYD_PID PROXY_PID=$PROXY_PID RUNTIME_DIR=$RUNTIME_DIR STATE_FILE=$STATE_FILE $CLEANUP_SCRIPT"

write_state_value CLEANUP_WATCHER_PID "$CLEANUP_WATCHER_PID" >> "$METADATA_FILE"
write_state_value URL "$URL" >> "$METADATA_FILE"
write_state_value CLEANUP_CMD "$CLEANUP_CMD" >> "$METADATA_FILE"
cp "$METADATA_FILE" "$STATE_FILE"

if [[ -n "$CLIENT_IP" && "$HOST" != "127.0.0.1" ]]; then
  UFW_ALLOW_CMD="sudo ufw allow from $CLIENT_IP to any port $PROXY_PORT proto tcp"
  UFW_DELETE_CMD="sudo ufw delete allow from $CLIENT_IP to any port $PROXY_PORT proto tcp"
else
  UFW_ALLOW_CMD=""
  UFW_DELETE_CMD=""
fi

if [[ "$HOST" == "127.0.0.1" ]]; then
  NOTE="Local only. URL token is one-shot. Proxy enforces expected host/origin and TTL cleanup."
else
  NOTE="LAN-exposed on $HOST:$PROXY_PORT with one-shot URL token. Restrict firewall to the client IP only and do not expose publicly."
fi

cat <<EOF
READY=1
SESSION_NAME=$SESSION_NAME
HOST=$HOST
PORT=$PROXY_PORT
URL=$URL
EXPIRES_AT=$EXPIRES_AT
TTYD_PID=$TTYD_PID
TTYD_PORT=$UPSTREAM_PORT
PROXY_PID=$PROXY_PID
CLEANUP_WATCHER_PID=$CLEANUP_WATCHER_PID
RUNTIME_DIR=$RUNTIME_DIR
STATE_FILE=$STATE_FILE
CLEANUP_CMD=$CLEANUP_CMD
PROXY_JSON=$PROXY_JSON
BIND_SCOPE=$BIND_SCOPE
CLIENT_IP=$CLIENT_IP
EXPECTED_HOST=$EXPECTED_HOST
EXPECTED_ORIGIN=$EXPECTED_ORIGIN
COOKIE_SECURE=$COOKIE_SECURE
UFW_ALLOW_CMD=$UFW_ALLOW_CMD
UFW_DELETE_CMD=$UFW_DELETE_CMD
NOTE=$NOTE
EOF
