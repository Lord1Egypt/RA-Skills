#!/usr/bin/env bash
set -euo pipefail

SESSION_NAME="${1:-ssh-handoff}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-}"
TTL_MINUTES="${TTL_MINUTES:-30}"
BIND_SCOPE="${BIND_SCOPE:-local}"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing dependency: $1" >&2
    exit 1
  }
}

need tmux
need ttyd
need python3

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  tmux new-session -d -s "$SESSION_NAME"
fi

if [[ -z "$PORT" ]]; then
  PORT="$(HOST_FOR_PY="$HOST" python3 - <<'PY'
import os, socket
host = os.environ['HOST_FOR_PY']
s = socket.socket()
s.bind((host, 0))
print(s.getsockname()[1])
s.close()
PY
)"
fi

TOKEN="$(python3 - <<'PY'
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

CMD=(ttyd -W -o -i "$HOST" -p "$PORT" -c "$TOKEN:$TOKEN" tmux attach -t "$SESSION_NAME")
nohup "${CMD[@]}" >/tmp/ttyd-"$SESSION_NAME".log 2>&1 &
PID=$!

if [[ "$HOST" == "127.0.0.1" ]]; then
  NOTE="Local only. Writable one-shot terminal. It exits after the client disconnects. Do not expose this terminal via public tunnel or reverse proxy."
else
  NOTE="LAN-exposed on $HOST:$PORT with temporary credentials. Writable one-shot terminal. Keep it on trusted local network only; do not expose it publicly."
fi

CLIENT_IP="${CLIENT_IP:-}"
if [[ -n "$CLIENT_IP" && "$HOST" != "127.0.0.1" ]]; then
  UFW_ALLOW_CMD="sudo ufw allow from $CLIENT_IP to any port $PORT proto tcp"
  UFW_DELETE_CMD="sudo ufw delete allow from $CLIENT_IP to any port $PORT proto tcp"
else
  UFW_ALLOW_CMD=""
  UFW_DELETE_CMD=""
fi

cat <<EOF
READY=1
SESSION_NAME=$SESSION_NAME
PID=$PID
HOST=$HOST
PORT=$PORT
TOKEN=$TOKEN
URL=http://$HOST:$PORT/
USERNAME=$TOKEN
PASSWORD=$TOKEN
EXPIRES_AT=$EXPIRES_AT
LOG=/tmp/ttyd-$SESSION_NAME.log
STOP_CMD=kill $PID
BIND_SCOPE=$BIND_SCOPE
CLIENT_IP=$CLIENT_IP
UFW_ALLOW_CMD=$UFW_ALLOW_CMD
UFW_DELETE_CMD=$UFW_DELETE_CMD
NOTE=$NOTE
EOF
