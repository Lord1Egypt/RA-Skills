#!/usr/bin/env bash

atomic_json_write() {
  local tmp_file="$1"
  local final_file="$2"
  local backup_file="$3"

  if [ ! -f "$tmp_file" ]; then
    echo "[skillminer] ERROR: atomic_json_write expected tmp file but none exists: $tmp_file" >&2
    if [ -n "$backup_file" ] && [ -f "$backup_file" ]; then
      cp "$backup_file" "$final_file"
    fi
    return 2
  fi

  if jq -e . "$tmp_file" >/dev/null 2>&1; then
    mv "$tmp_file" "$final_file"
    return 0
  fi

  rm -f "$tmp_file"
  if [ -n "$backup_file" ] && [ -f "$backup_file" ]; then
    cp "$backup_file" "$final_file"
  fi
  return 1
}

atomic_text_write() {
  local tmp_file="$1"
  local final_file="$2"

  if [ ! -f "$tmp_file" ]; then
    echo "[skillminer] ERROR: atomic_text_write expected tmp file but none exists: $tmp_file" >&2
    return 2
  fi

  if [ -s "$tmp_file" ]; then
    mv "$tmp_file" "$final_file"
    return 0
  fi

  rm -f "$tmp_file"
  return 1
}

create_state_backup() {
  local state_file="$1"
  local stamp="$2"
  local backup_file="${state_file}.bak.${stamp}"

  cp "$state_file" "$backup_file"
  printf '%s\n' "$backup_file"
}

rotate_state_backups() {
  local state_file="$1"

  ls -t "${state_file}".bak.[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]T[0-9][0-9][0-9][0-9][0-9][0-9]Z 2>/dev/null \
    | tail -n +8 | xargs -r rm -f
}

acquire_skillminer_lock() {
  if [ "${SKILLMINER_LOCK_HELD:-0}" = "1" ]; then
    return 0
  fi

  local lock_file
  lock_file="/tmp/skillminer-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd | sha1sum | cut -c1-16).lock"
  exec 9>"$lock_file"
  if ! flock -n 9; then
    echo "[skillminer] another instance is running (lock: $lock_file) - aborting" >&2
    return 1
  fi

  export SKILLMINER_LOCK_HELD=1
  export SKILLMINER_LOCK_FILE="$lock_file"
}
