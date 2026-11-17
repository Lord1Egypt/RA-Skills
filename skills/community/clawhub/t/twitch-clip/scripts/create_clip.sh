#!/bin/bash
# Usage: create_clip.sh [duration_seconds]
# Duration defaults to 30, must be 5-60 (Twitch Helix clips API limit).

DURATION=${1:-30}
CLIENT_ID="${TWITCH_CLIENT_ID}"
TOKEN="${TWITCH_ACCESS_TOKEN}"
BROADCASTER_ID="${TWITCH_BROADCASTER_ID}"
COOLDOWN_SECONDS=30

# Validate duration before doing anything else. The Helix POST /clips endpoint
# accepts 5-60 seconds and silently falls back to its own default if the value
# is unusable, which would publish a clip of a different length than requested.
case "$DURATION" in
  ''|*[!0-9]*)
    echo "ERROR: duration must be an integer number of seconds (5-60)" >&2
    exit 1
    ;;
esac
if [ "$DURATION" -lt 5 ] || [ "$DURATION" -gt 60 ]; then
  echo "ERROR: duration must be between 5 and 60 seconds (got ${DURATION})" >&2
  exit 1
fi

# Cooldown state lives in a private per-user directory, not a shared /tmp path.
# A predictable file in /tmp can be pre-created or symlinked by another user on a
# multi-user machine, letting them read the timestamp or redirect the write.
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/twitch-clip"
LOCKFILE="${STATE_DIR}/cooldown"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

if [ -z "$TOKEN" ] || [ -z "$CLIENT_ID" ] || [ -z "$BROADCASTER_ID" ]; then
  echo "ERROR: Missing Twitch credentials in environment" >&2
  exit 1
fi

# Cooldown check - prevent spam clipping.
#
# The lock is acquired BEFORE the timestamp is read and before the API call.
# mkdir is atomic on POSIX, so a concurrent invocation cannot slip through the
# check while this one is still creating a clip. The timestamp is written
# before the request so a crash mid-request still consumes the cooldown slot.
LOCK_DIR="${STATE_DIR}/cooldown.lock"
LOCK_HELD=0

cleanup_lock() {
  if [ "$LOCK_HELD" -eq 1 ]; then
    rmdir "$LOCK_DIR" 2>/dev/null || true
  fi
}
trap cleanup_lock EXIT INT TERM

if mkdir "$LOCK_DIR" 2>/dev/null; then
  LOCK_HELD=1
else
  # Another invocation is mid-flight. Wait briefly for it to finish, then
  # report the cooldown rather than creating a second clip.
  WAITED=0
  while [ "$WAITED" -lt 5 ]; do
    sleep 1
    WAITED=$(( WAITED + 1 ))
    if mkdir "$LOCK_DIR" 2>/dev/null; then
      LOCK_HELD=1
      break
    fi
  done
  if [ "$LOCK_HELD" -ne 1 ]; then
    echo "COOLDOWN: Another clip request is already in flight. Wait ${COOLDOWN_SECONDS}s before clipping again." >&2
    exit 2
  fi
fi

if [ -f "$LOCKFILE" ] && [ ! -L "$LOCKFILE" ]; then
  LAST_CLIP=$(cat "$LOCKFILE" 2>/dev/null)
  # Ignore a non-numeric or tampered timestamp rather than failing the clip.
  case "$LAST_CLIP" in
    ''|*[!0-9]*)
      LAST_CLIP=0
      ;;
  esac
  NOW=$(date +%s)
  ELAPSED=$(( NOW - LAST_CLIP ))
  REMAINING=$(( COOLDOWN_SECONDS - ELAPSED ))

  if [ "$ELAPSED" -lt "$COOLDOWN_SECONDS" ]; then
    echo "COOLDOWN: Please wait ${REMAINING}s before clipping again." >&2
    exit 2
  fi
fi

# Consume the cooldown slot BEFORE the request. If the API call fails, the
# slot is still spent, which is the safe direction to err.
( umask 077; date +%s > "${LOCKFILE}.tmp.$$" ) && mv -f "${LOCKFILE}.tmp.$$" "$LOCKFILE"

RESPONSE=$(curl -s -X POST \
  "https://api.twitch.tv/helix/clips?broadcaster_id=${BROADCASTER_ID}&has_delay=false&duration=${DURATION}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Client-Id: ${CLIENT_ID}")

CLIP_ID=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['data'][0]['id'])" 2>/dev/null)
EDIT_URL=$(echo "$RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['data'][0]['edit_url'])" 2>/dev/null)

if [ -z "$CLIP_ID" ]; then
  echo "ERROR: Failed to create clip. Response: $RESPONSE" >&2
  exit 1
fi

# Cooldown timestamp was written before the request to prevent races.

echo "clip_id=$CLIP_ID"
echo "edit_url=$EDIT_URL"
echo "url=https://clips.twitch.tv/$CLIP_ID"
