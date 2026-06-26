#!/usr/bin/env bash
# Session Cleaner — keep main + group chat sessions, backup the rest.
# Usage: clean-sessions.sh [--dry-run]
set -euo pipefail

SESSIONS_DIR="$HOME/.openclaw/agents/main/sessions"
BACKUP_DIR="$SESSIONS_DIR/backup"
DRY_RUN=false

[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# Find the current active main session (most recently modified file with agent:main:main key)
find_current_main() {
  local latest=""
  local latest_mtime=0
  for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    if grep -q '"sessionKey":"agent:main:main"' "$f" 2>/dev/null; then
      local mtime
      mtime=$(stat -c '%Y' "$f" 2>/dev/null || stat -f '%m' "$f" 2>/dev/null)
      if (( mtime > latest_mtime )); then
        latest_mtime=$mtime
        latest="$f"
      fi
    fi
  done
  # Fallback: most recently modified .jsonl with "to":"user:" pattern
  if [ -z "$latest" ]; then
    latest=$(ls -t "$SESSIONS_DIR"/*.jsonl 2>/dev/null | head -1)
  fi
  echo "$latest"
}

is_group_session() {
  local f="$1"
  # Check if target address contains oc_ (group chat ID)
  local to
  to=$(grep -o '"to":"[^"]*"' "$f" 2>/dev/null | head -1 | cut -d'"' -f4)
  if echo "$to" | grep -q 'oc_'; then
    return 0
  fi
  # Check if session key contains feishu:group
  local key
  key=$(grep -o '"sessionKey":"[^"]*"' "$f" 2>/dev/null | head -1 | cut -d'"' -f4)
  if echo "$key" | grep -q 'feishu:group'; then
    return 0
  fi
  return 1
}

main() {
  if [ ! -d "$SESSIONS_DIR" ]; then
    echo "Sessions directory not found: $SESSIONS_DIR"
    exit 1
  fi

  local current_main
  current_main=$(find_current_main)
  local current_main_basename=""
  [ -n "$current_main" ] && current_main_basename=$(basename "$current_main")

  local keep=0 move=0 move_size=0

  for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    local basename
    basename=$(basename "$f")

    # Keep current main session
    if [ "$basename" = "$current_main_basename" ]; then
      keep=$((keep + 1))
      continue
    fi

    # Keep group chat sessions
    if is_group_session "$f"; then
      keep=$((keep + 1))
      continue
    fi

    # Move everything else
    move=$((move + 1))
    local fsize
    fsize=$(stat -c '%s' "$f" 2>/dev/null || stat -f '%z' "$f" 2>/dev/null)
    move_size=$((move_size + fsize))

    if $DRY_RUN; then
      echo "[dry-run] would move: $basename ($(numfmt --to=iec "$fsize" 2>/dev/null || echo "${fsize}B"))"
    else
      mkdir -p "$BACKUP_DIR"
      mv "$f" "$BACKUP_DIR/"
    fi
  done

  local size_human
  size_human=$(numfmt --to=iec "$move_size" 2>/dev/null || echo "${move_size}B")

  if $DRY_RUN; then
    echo "--- dry-run summary: keep=$keep, would_move=$move ($size_human)"
  else
    echo "--- done: keep=$keep, moved=$move ($size_human) → backup/"
  fi
}

main
