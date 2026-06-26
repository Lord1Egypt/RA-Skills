#!/usr/bin/env bash
# BYOB Workspace Bridge — one-command setup for an openclaw operator.
#
# Use case: you run openclaw locally for an agent (e.g. David). You want
# Mission Control to list/read/write the agent's actual MD files (MEMORY.md,
# memory/YYYY-MM-DD.md, DREAMS.md, AGENTS.md, SOUL.md) live from your laptop.
#
# Usage:
#   export SD_JWT='eyJhbGc...'                        # MC localStorage 'sd_token'
#   export SPACEDUCK_BEAK_KEY='bk_LIVE_...'           # MC Hatch panel
#   ./setup_byob_bridge.sh --duck-id <SPACEDUCK_ID> [--workspace <PATH>]
#
# Auth secrets MUST come via env to avoid leaking through `ps aux`.
#
# Prereqs:
#   - python3 ≥ 3.10
#   - cloudflared  (macOS: brew install cloudflare/cloudflare/cloudflared)
#   - openclaw installed locally; agent paired
#
# What it does:
#   1. Verifies prereqs + bridge files in place
#   2. Auto-discovers the workspace dir via Gateway-token (native openclaw path)
#   3. Picks a free local port (8086 by default, else next available)
#   4. Runs the bridge selftest with stderr captured for diagnosis
#   5. Starts the bridge in background; polls until it listens
#   6. Starts a cloudflared quick tunnel and captures the public URL
#   7. POSTs the URL to MC's flip endpoint with --fail so HTTP errors abort
#   8. Persists JWT + tunnel/bridge PIDs to /tmp/spaceduck-bridge-<SD>.state
#      (chmod 600) so the stop command works without re-prompting
#   9. Traps EXIT/INT/TERM so a Ctrl-C or partial-run doesn't orphan workers
#
# Note: cloudflared quick tunnels rate-limit aggressively and the URL rotates
# on every restart. Production deployments should use a stable tunnel (named
# tunnel, Tailscale, or upstream nginx + Let's Encrypt) — see README.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRIDGE_PY="$SCRIPT_DIR/workspace_bridge.py"
HMAC_PY="$SCRIPT_DIR/byob_hmac.py"
MC_API="${MC_API:-https://beak.spaceduckling.com}"
PORT_PREFERRED="${BIND_PORT:-8086}"

die() { echo "✗ $*" >&2; exit 1; }
ok()  { echo "✓ $*"; }
info(){ echo "→ $*"; }

# ─────────────────────────── args + secrets ───────────────────────────
SD=""; WS=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --duck-id)   SD="$2"; shift 2;;
    --workspace) WS="$2"; shift 2;;
    --help|-h)
      awk '/^# Usage:/,/^set/{ if ($0 ~ /^set/) exit; sub(/^# ?/, ""); print }' "$0"
      exit 0;;
    *) die "unknown arg: $1 (try --help)";;
  esac
done
[[ -z "$SD" ]] && die "--duck-id <SPACEDUCK_ID> is required"
[[ -z "${SD_JWT:-}" ]] && die "export SD_JWT='...' (your MC localStorage sd_token)"
[[ -z "${SPACEDUCK_BEAK_KEY:-}" ]] && die "export SPACEDUCK_BEAK_KEY='bk_LIVE_...'"

# ─────────────────────────── prereqs ───────────────────────────
[[ -f "$BRIDGE_PY" ]] || die "workspace_bridge.py missing at $BRIDGE_PY"
[[ -f "$HMAC_PY" ]]   || die "byob_hmac.py missing at $HMAC_PY"
command -v python3 >/dev/null || die "python3 not in PATH"
PYVER=$(python3 -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')
PYMAJOR=$(python3 -c 'import sys; print(sys.version_info[0])')
PYMINOR=$(python3 -c 'import sys; print(sys.version_info[1])')
{ [[ "$PYMAJOR" -gt 3 ]] || [[ "$PYMAJOR" -eq 3 && "$PYMINOR" -ge 10 ]]; } \
  || die "python3 $PYVER too old; need ≥ 3.10"
ok "python3 $PYVER"

if ! command -v cloudflared >/dev/null; then
  echo "✗ cloudflared not installed."
  if command -v brew >/dev/null; then
    info "Install: brew install cloudflare/cloudflare/cloudflared"
  else
    info "Download: https://github.com/cloudflare/cloudflared/releases"
  fi
  exit 1
fi
ok "cloudflared $(cloudflared --version 2>&1 | head -1 | awk '{print $3}')"

# ─────────────────────────── workspace discovery ───────────────────────────
if [[ -z "$WS" ]]; then
  info "Resolving workspace via Gateway-token discovery..."
  # Parse with -F'= ' but split on first '= ' only — tolerates '=' in path
  WS_RAW=$(python3 "$BRIDGE_PY" introspect 2>&1) || die "introspect failed: $WS_RAW"
  WS=$(echo "$WS_RAW" | awk '/^workspace = /{sub(/^workspace = /, ""); print; exit}')
  [[ -z "$WS" || ! -d "$WS" ]] && die "Could not resolve workspace. Re-run with --workspace <PATH>"
fi
ok "workspace = $WS"

# Sanity — accept .md at root OR memory/ subdir (openclaw daily notes)
MD_COUNT=$(find "$WS" -maxdepth 2 -name '*.md' -type f 2>/dev/null | wc -l | tr -d ' ')
[[ "$MD_COUNT" -eq 0 ]] && die "no .md files in $WS (or memory/ subdir) — is this really an openclaw agent dir?"
ok "$MD_COUNT markdown file(s) detected"

# ─────────────────────────── selftest ───────────────────────────
info "Running bridge selftest..."
SELFTEST_LOG="/tmp/spaceduck-selftest-$SD.log"
if ! python3 "$BRIDGE_PY" selftest > "$SELFTEST_LOG" 2>&1; then
  echo "--- selftest output ---"
  cat "$SELFTEST_LOG"
  die "selftest failed — see above"
fi
ok "selftest passed"

# ─────────────────────────── pick free port ───────────────────────────
pick_free_port() {
  local p=$1
  for try in {0..15}; do
    if ! nc -z 127.0.0.1 "$p" 2>/dev/null; then echo "$p"; return; fi
    p=$((p + 1))
  done
  die "no free port near $1 — close something or set BIND_PORT"
}
PORT=$(pick_free_port "$PORT_PREFERRED")
[[ "$PORT" != "$PORT_PREFERRED" ]] && info "port $PORT_PREFERRED busy, using $PORT"
ok "bind = 127.0.0.1:$PORT"

# ─────────────────────────── state file (creds + pids) ───────────────────────────
STATE_FILE="/tmp/spaceduck-bridge-$SD.state"
umask 077
cat > "$STATE_FILE" <<EOM
# auto-generated by setup_byob_bridge.sh — do not commit
SD=$SD
JWT='$SD_JWT'
PORT=$PORT
MC_API='$MC_API'
EOM
ok "state file: $STATE_FILE (mode 600)"

# ─────────────────────────── teardown trap ───────────────────────────
SUCCESS=0
_teardown() {
  local rc=$?
  if [[ "$SUCCESS" -eq 0 ]]; then
    [[ -n "${BRIDGE_PID:-}" ]] && kill "$BRIDGE_PID" 2>/dev/null || true
    [[ -n "${TUNNEL_PID:-}" ]] && kill "$TUNNEL_PID" 2>/dev/null || true
    echo "↩ teardown on exit code $rc (bridge/tunnel killed; state file kept for inspection)"
  fi
  return $rc
}
trap _teardown EXIT INT TERM

# ─────────────────────────── start bridge ───────────────────────────
BRIDGE_LOG="/tmp/spaceduck-bridge-$SD.log"
: > "$BRIDGE_LOG"
info "Starting bridge on 127.0.0.1:$PORT..."
SPACEDUCK_BEAK_KEY="$SPACEDUCK_BEAK_KEY" nohup python3 "$BRIDGE_PY" run \
  --bind "127.0.0.1:$PORT" \
  --workspace "$WS" \
  > "$BRIDGE_LOG" 2>&1 &
BRIDGE_PID=$!
echo "BRIDGE_PID=$BRIDGE_PID" >> "$STATE_FILE"

# Poll until listening (replaces unreliable sleep-2)
LISTEN_OK=0
for i in {1..30}; do
  if nc -z 127.0.0.1 "$PORT" 2>/dev/null; then LISTEN_OK=1; break; fi
  sleep 0.5
done
[[ "$LISTEN_OK" -eq 0 ]] && { tail -20 "$BRIDGE_LOG"; die "bridge never started listening"; }
ok "bridge listening (pid $BRIDGE_PID, log $BRIDGE_LOG)"

# ─────────────────────────── tunnel ───────────────────────────
TUNNEL_LOG="/tmp/spaceduck-tunnel-$SD.log"
: > "$TUNNEL_LOG"
info "Starting cloudflared quick tunnel..."
nohup cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:$PORT" \
  > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!
echo "TUNNEL_PID=$TUNNEL_PID" >> "$STATE_FILE"

printf "  ⏳ waiting for tunnel URL "
TUNNEL_URL=""
for i in {1..40}; do
  TUNNEL_URL=$(grep -Eo 'https://[A-Za-z0-9.-]+\.trycloudflare\.com' "$TUNNEL_LOG" 2>/dev/null | head -1 || true)
  if [[ -n "$TUNNEL_URL" ]]; then echo; break; fi
  printf "."; sleep 1
done
[[ -z "$TUNNEL_URL" ]] && { echo; tail -20 "$TUNNEL_LOG"; die "tunnel never reported URL"; }

# Validate it actually proxies
info "Verifying tunnel is reachable..."
TS=$(date +%s)
SIG=$(python3 "$HMAC_PY" GET /v1/files "$TS" --key "$SPACEDUCK_BEAK_KEY")
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 8 \
  -H "Authorization: Bearer $SPACEDUCK_BEAK_KEY" \
  -H "X-Spaceduck-Timestamp: $TS" \
  -H "X-Spaceduck-Signature: $SIG" \
  "$TUNNEL_URL/v1/files" || echo "000")
[[ "$HTTP_CODE" != "200" ]] && die "tunnel verify failed: HTTP $HTTP_CODE on $TUNNEL_URL/v1/files"
ok "tunnel verified (200 from $TUNNEL_URL/v1/files)"
echo "TUNNEL_URL='$TUNNEL_URL'" >> "$STATE_FILE"

# ─────────────────────────── flip MC ───────────────────────────
info "Flipping MC workspace URL for duck $SD..."
FLIP_BODY="/tmp/spaceduck-flip-$SD.json"
FLIP_HTTP=$(curl -s -o "$FLIP_BODY" -w '%{http_code}' \
  -X POST "$MC_API/beak/me/duck/$SD/workspace-url" \
  -H "Authorization: Bearer $SD_JWT" -H 'Content-Type: application/json' \
  -d "{\"url\":\"$TUNNEL_URL\"}")
if [[ "$FLIP_HTTP" != "200" ]]; then
  echo "  HTTP $FLIP_HTTP"; cat "$FLIP_BODY"; echo
  die "flip endpoint rejected"
fi
PMW=$(python3 -c "import json,sys; d=json.load(open('$FLIP_BODY')); print(d.get('platform_managed_workspace',''))")
[[ "$PMW" != "False" ]] && { cat "$FLIP_BODY"; die "platform_managed_workspace did not flip to false"; }
ok "MC routes /beak/byob/workspace/* → $TUNNEL_URL"

SUCCESS=1

# ─────────────────────────── done ───────────────────────────
cat <<EOM

================ BYOB BRIDGE LIVE ================
  spaceduck_id : $SD
  workspace    : $WS
  bridge pid   : $BRIDGE_PID  (log: $BRIDGE_LOG)
  tunnel pid   : $TUNNEL_PID  (log: $TUNNEL_LOG)
  tunnel URL   : $TUNNEL_URL
  state file   : $STATE_FILE (chmod 600, JWT + PIDs)
==================================================

Open Mission Control → Files. The banner should now read:
    "✓ External BYOB — files shown are LIVE from the agent's workspace."

To stop the bridge + tunnel + flip back to platform-managed:
    bash $SCRIPT_DIR/teardown_byob_bridge.sh --duck-id $SD

Manual verify-curl (uses the persisted state file):
    source $STATE_FILE
    TS=\$(date +%s)
    SIG=\$(python3 $HMAC_PY GET /v1/files \$TS --key \$SPACEDUCK_BEAK_KEY)
    curl -s -H "Authorization: Bearer \$SPACEDUCK_BEAK_KEY" \\
         -H "X-Spaceduck-Timestamp: \$TS" -H "X-Spaceduck-Signature: \$SIG" \\
         \$TUNNEL_URL/v1/files | jq .

Heads-up: cloudflared quick tunnels are ephemeral and rate-limited. For
anything beyond a demo, use a named tunnel, Tailscale, or upstream nginx.

EOM
