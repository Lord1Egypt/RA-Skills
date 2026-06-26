#!/usr/bin/env bash
# Shared helpers for key=value manifest files.

# manifest_read KEY FILE — print value for KEY, return 1 if absent
manifest_read() {
  grep "^$1=" "$2" 2>/dev/null | head -1 | cut -d= -f2-
}

# manifest_set FILE KEY VALUE [KEY VALUE ...] — atomic upsert
# Uses mkdir-based advisory locking (portable, no flock dependency) to
# serialize concurrent read-modify-write cycles from wrapper and monitor.
# Uses mktemp for per-call tmp paths so two concurrent writers cannot
# clobber each other's tmp file.
manifest_set() {
  local file="$1"; shift
  [ $# -ge 2 ] || return 0  # no pairs: no-op (prevents grep -Ev "" wipe)

  local lockdir="${file}.lock"
  local tmp exclude="" tries=0
  local -a pairs=()

  # Acquire lock via atomic mkdir. 5s max wait before proceeding
  # unlocked (best-effort for observability writes).
  while ! mkdir "$lockdir" 2>/dev/null; do
    tries=$(( tries + 1 ))
    if [ "$tries" -gt 50 ]; then
      break
    fi
    sleep 0.1
  done

  while [ $# -ge 2 ]; do
    exclude="${exclude:+$exclude|}^$1="
    pairs+=("$1=$2")
    shift 2
  done

  tmp=$(mktemp "${file}.XXXXXX" 2>/dev/null) || tmp="${file}.tmp.$$"
  { grep -Ev "$exclude" "$file" 2>/dev/null || true
    printf '%s\n' "${pairs[@]}"
  } > "$tmp"
  mv "$tmp" "$file"

  rmdir "$lockdir" 2>/dev/null || true
}
