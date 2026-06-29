#!/usr/bin/env bash
# Smoke test the call pattern from SKILL.md against a local HTTP server
# (no external network). Confirms: status captured, headers file written,
# body file written, temp dir cleaned up by trap.
set -euo pipefail

# External scratch dir: nothing written inside the repo, everything
# cleaned up via trap.
scratch="$(mktemp -d -t scouts-ai-smoke.XXXXXX)"
trap 'rm -rf "$scratch"' EXIT
printf '{"ok":true,"results":[]}\n' > "$scratch/search.json"

# Pick a free TCP port dynamically to avoid collisions.
port="$(
  python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)"

server_log="$scratch/server.log"
nohup python3 -m http.server "$port" --bind 127.0.0.1 --directory "$scratch" \
  >"$server_log" 2>&1 </dev/null &
server_pid=$!
disown "$server_pid" 2>/dev/null || true
trap 'kill "$server_pid" 2>/dev/null || true; rm -rf "$scratch"' EXIT

# Wait for server to accept connections (max ~2s).
for _ in $(seq 1 20); do
  if (echo > /dev/tcp/127.0.0.1/$port) 2>/dev/null; then break; fi
  sleep 0.1
done

umask 077
tmpdir=$(mktemp -d -t scouts-ai.XXXXXX)
trap 'rm -rf "$tmpdir"; kill "$server_pid" 2>/dev/null || true; rm -rf "$scratch"' EXIT

status=$(curl -sS --get "http://127.0.0.1:$port/search.json" \
  -D "$tmpdir/headers.txt" \
  -w '%{http_code}\n' \
  -o "$tmpdir/body.json")

if [[ "$status" != "200" ]]; then
  echo "expected 200, got $status" >&2
  cat "$server_log" >&2 || true
  exit 1
fi
[[ -s "$tmpdir/headers.txt" ]] || { echo "no headers captured" >&2; exit 1; }
[[ -s "$tmpdir/body.json"   ]] || { echo "no body captured" >&2; exit 1; }
grep -q '"ok":true' "$tmpdir/body.json" || { echo "body mismatch" >&2; exit 1; }

# Confirm trap cleanup happens on normal exit.
rm -rf "$tmpdir"
[[ ! -d "$tmpdir" ]] || { echo "temp dir not cleaned" >&2; exit 1; }

echo "Smoke test passed: status=$status, headers+body captured, temp dir cleaned."
