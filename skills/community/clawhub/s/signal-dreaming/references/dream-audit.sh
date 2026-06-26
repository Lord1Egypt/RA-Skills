#!/usr/bin/env bash
set -euo pipefail

# Lightweight post-write sanity check for signal-dreaming runs.
# Usage: references/dream-audit.sh <workspace-root> [touched-file ...]
# Prints filenames only for suspected secrets; never echoes matched values.
# This is NOT full DLP or exhaustive secret detection.

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <workspace-root> [touched-file ...]" >&2
  exit 2
fi

ROOT="$1"
shift || true

if [[ ! -d "$ROOT" ]]; then
  echo "ERROR: workspace root does not exist: $ROOT" >&2
  exit 2
fi

MEMORY="$ROOT/MEMORY.md"
DREAM_LOG="$ROOT/memory/dream-log.md"
status=0

if [[ ! -f "$MEMORY" ]]; then
  echo "ERROR: missing MEMORY.md" >&2
  status=1
else
  bytes=$(wc -c < "$MEMORY" | tr -d ' ')
  echo "MEMORY.md bytes=$bytes"
  if [[ "$bytes" -gt 8192 ]]; then
    echo "WARN: MEMORY.md exceeds 8KB target" >&2
    status=1
  fi
fi

if [[ ! -f "$DREAM_LOG" ]]; then
  echo "ERROR: missing memory/dream-log.md" >&2
  status=1
else
  dream_count=$(grep -c '^## 🌙 Dream #' "$DREAM_LOG" || true)
  echo "dream_log_entries=$dream_count"
fi

files=()
if [[ $# -gt 0 ]]; then
  for f in "$@"; do
    if [[ "$f" = /* ]]; then
      files+=("$f")
    else
      files+=("$ROOT/$f")
    fi
  done
else
  files+=("$MEMORY" "$DREAM_LOG")
fi

secret_re='(github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|[0-9]{8,12}:AA[A-Za-z0-9_-]{30,}|mfa\.[A-Za-z0-9_-]{20,}|[A-Za-z0-9_-]{24}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{25,}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|x-access-token:[A-Za-z0-9_-]{20,}@)'

suspects=()
for f in "${files[@]}"; do
  [[ -f "$f" ]] || continue
  if LC_ALL=C grep -Iq . "$f" && LC_ALL=C grep -qE "$secret_re" "$f"; then
    suspects+=("$f")
  fi
done

if [[ ${#suspects[@]} -gt 0 ]]; then
  echo "ERROR: suspected credential pattern in file(s):" >&2
  printf ' - %s\n' "${suspects[@]}" >&2
  status=1
else
  echo "secret_scan=ok"
fi

exit "$status"
