#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <serve-dir> <relative-path> [port]" >&2
  exit 1
fi

SERVE_DIR="$1"
REL_PATH="$2"
PORT="${3:-8765}"

cd "$SERVE_DIR"
python3 -m http.server "$PORT" >/tmp/trycloudflare-file-server.log 2>&1 &
HTTP_PID=$!

cleanup() {
  kill "$HTTP_PID" 2>/dev/null || true
  [[ -n "${CF_PID:-}" ]] && kill "$CF_PID" 2>/dev/null || true
}
trap cleanup EXIT

cloudflared tunnel --url "http://127.0.0.1:$PORT" --no-autoupdate --protocol http2 >/tmp/trycloudflare-tunnel.log 2>&1 &
CF_PID=$!

PUBLIC_URL=""
for _ in $(seq 1 30); do
  if grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/trycloudflare-tunnel.log >/tmp/trycloudflare-url.txt 2>/dev/null; then
    PUBLIC_URL=$(tail -n 1 /tmp/trycloudflare-url.txt)
  fi
  if grep -q 'Registered tunnel connection' /tmp/trycloudflare-tunnel.log 2>/dev/null && [[ -n "$PUBLIC_URL" ]]; then
    break
  fi
  sleep 1
done

if [[ -z "$PUBLIC_URL" ]]; then
  echo "Failed to obtain verified public URL" >&2
  exit 2
fi

curl -I "$PUBLIC_URL/$REL_PATH" >/tmp/trycloudflare-final-head.txt

echo "$PUBLIC_URL/$REL_PATH"
wait
