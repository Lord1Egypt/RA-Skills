#!/usr/bin/env bash
# audit-logs.sh: F-007 pre-fix log audit for the VPS hosted-mcp surface.
#
# Read-only. No log mutation, no rotation, no clearing. Greps nginx and
# PM2 logs for bearer/ticket/api-key shaped values that may have leaked
# during the period when the WS upgrade accepted ?token=ck- and the
# phone app sent ck values in URLs.
#
# Output: per-source match count, plus up to N redacted sample lines per
# source so you can see which path / agent / time range is affected
# without ever printing the leaked secret in this terminal session.
#
# If any source shows a non-zero count, treat the matching ck values as
# already-leaked. Rotate them as part of the F-002 + F-005a deploy
# (see ai/product/bugs/security/2026-04-28--cc-mini--vps-hosted-mcp-audit.md).
#
# Usage on the VPS:
#   bash audit-logs.sh
#   bash audit-logs.sh --days 14            # widen log window for rotated logs
#   bash audit-logs.sh --samples 20         # show more redacted samples
#   bash audit-logs.sh --json               # machine-readable output (counts only)
#
# Source: src/hosted-mcp/scripts/audit-logs.sh

set -euo pipefail

# ── Defaults ────────────────────────────────────────────────────────

DAYS=7
SAMPLES=10
JSON=0
NGINX_LOG_DIR=/var/log/nginx
PM2_APP=mcp-server

# ── Args ────────────────────────────────────────────────────────────

while [ $# -gt 0 ]; do
  case "$1" in
    --days)    DAYS=$2;    shift 2 ;;
    --samples) SAMPLES=$2; shift 2 ;;
    --json)    JSON=1;     shift 1 ;;
    --nginx-log-dir) NGINX_LOG_DIR=$2; shift 2 ;;
    --pm2-app) PM2_APP=$2; shift 2 ;;
    -h|--help)
      sed -n '2,30p' "$0"
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

# ── Patterns ────────────────────────────────────────────────────────
#
# Three families of leak we are looking for. Each is a single ERE that
# `grep -E` will accept. We match conservatively (\b, exact prefixes)
# so we do not over-flag random bytes that happen to resemble a key.

PAT_QUERY_TOKEN='[?&](token|ticket|api_key|access_token)=[^[:space:]&"]+'
PAT_CK_KEY='\bck-[A-Za-z0-9_-]{6,}\b'
PAT_AUTH_BEARER='Authorization:[[:space:]]*Bearer[[:space:]]+ck-[A-Za-z0-9_-]{6,}'

# ── Redaction (for sample output only) ──────────────────────────────
#
# Replace the matched value with a marker before we print the sample
# line. This way the audit's own output never reproduces the leaked
# secret in the operator's terminal/scrollback.

redact() {
  sed -E \
    -e 's/([?&](token|ticket|api_key|access_token)=)[^&" \t]+/\1[REDACTED]/g' \
    -e 's/\bck-[A-Za-z0-9_-]+/[REDACTED ck-]/g'
}

# ── Source inventory ────────────────────────────────────────────────

declare -a SOURCES
declare -A SOURCE_LABEL

add_source() {
  local label=$1
  local path=$2
  if [ -e "$path" ] || compgen -G "$path" > /dev/null; then
    SOURCES+=("$path")
    SOURCE_LABEL["$path"]=$label
  fi
}

add_source "nginx access (current)"      "${NGINX_LOG_DIR}/access.log"
add_source "nginx error (current)"       "${NGINX_LOG_DIR}/error.log"
add_source "nginx wip.computer.access"   "${NGINX_LOG_DIR}/wip.computer.access.log"
add_source "nginx wip.computer.error"    "${NGINX_LOG_DIR}/wip.computer.error.log"

# ── Counters ────────────────────────────────────────────────────────

total_matches=0
declare -A counts

scan_one() {
  local path=$1
  local label=$2
  local count
  if [[ "$path" == *.gz ]]; then
    count=$(sudo zgrep -E "$PAT_QUERY_TOKEN|$PAT_CK_KEY|$PAT_AUTH_BEARER" "$path" 2>/dev/null | wc -l | tr -d ' ')
  else
    count=$(sudo grep -E "$PAT_QUERY_TOKEN|$PAT_CK_KEY|$PAT_AUTH_BEARER" "$path" 2>/dev/null | wc -l | tr -d ' ')
  fi
  counts["$path"]=$count
  total_matches=$(( total_matches + count ))
}

print_samples() {
  local path=$1
  local label=$2
  local count=${counts["$path"]}
  [ "$count" -eq 0 ] && return
  echo
  echo "── $label ($path)"
  echo "   matches: $count"
  echo "   sample (redacted, up to $SAMPLES lines):"
  if [[ "$path" == *.gz ]]; then
    sudo zgrep -E "$PAT_QUERY_TOKEN|$PAT_CK_KEY|$PAT_AUTH_BEARER" "$path" 2>/dev/null \
      | head -n "$SAMPLES" | redact | sed 's/^/     /'
  else
    sudo grep -E "$PAT_QUERY_TOKEN|$PAT_CK_KEY|$PAT_AUTH_BEARER" "$path" 2>/dev/null \
      | head -n "$SAMPLES" | redact | sed 's/^/     /'
  fi
}

# ── Run nginx scan ──────────────────────────────────────────────────

if [ "$JSON" -ne 1 ]; then
  echo "F-007 log audit"
  echo "Days back (rotated): $DAYS"
  echo "Samples per source: $SAMPLES"
  echo "Nginx log dir: $NGINX_LOG_DIR"
  echo
fi

# Current logs
for path in "${SOURCES[@]}"; do
  scan_one "$path" "${SOURCE_LABEL[$path]}"
done

# Rotated logs within the window
shopt -s nullglob
declare -a ROTATED
for f in "${NGINX_LOG_DIR}"/*.gz "${NGINX_LOG_DIR}"/*.[0-9]*; do
  if [ -f "$f" ]; then
    if find "$f" -mtime "-${DAYS}" -print -quit | grep -q .; then
      ROTATED+=("$f")
    fi
  fi
done

for path in "${ROTATED[@]}"; do
  scan_one "$path" "rotated $(basename "$path")"
done

# ── PM2 ─────────────────────────────────────────────────────────────
#
# pm2 logs --nostream prints recent lines from the in-memory buffer.
# This is best-effort: it covers the current PM2 process lifetime, not
# rotated copies. PM2's persisted logs (if any) live under
# ~/.pm2/logs/<app>-out.log and ~/.pm2/logs/<app>-error.log.

PM2_OUT="$HOME/.pm2/logs/${PM2_APP}-out.log"
PM2_ERR="$HOME/.pm2/logs/${PM2_APP}-error.log"

if [ -e "$PM2_OUT" ]; then add_source "pm2 ${PM2_APP} out"   "$PM2_OUT"; scan_one "$PM2_OUT" "pm2 out"; fi
if [ -e "$PM2_ERR" ]; then add_source "pm2 ${PM2_APP} error" "$PM2_ERR"; scan_one "$PM2_ERR" "pm2 error"; fi

# ── Output ──────────────────────────────────────────────────────────

if [ "$JSON" -eq 1 ]; then
  printf '{"total_matches": %d, "by_source": {' "$total_matches"
  first=1
  for path in "${!counts[@]}"; do
    [ "$first" -eq 1 ] && first=0 || printf ','
    printf '"%s": %d' "$path" "${counts[$path]}"
  done
  printf '}}\n'
else
  echo "── Summary"
  for path in "${!counts[@]}"; do
    label=${SOURCE_LABEL[$path]:-${path}}
    printf "   %-40s %s matches\n" "$label" "${counts[$path]}"
  done
  echo
  echo "── Total matches: $total_matches"

  for path in "${!counts[@]}"; do
    print_samples "$path" "${SOURCE_LABEL[$path]:-${path}}"
  done

  echo
  if [ "$total_matches" -gt 0 ]; then
    echo "ACTION REQUIRED:"
    echo "  Treat any matched ck values as leaked. Rotate them as part of the"
    echo "  F-002 + F-005a deploy. After deploying redact-logs.conf, re-run"
    echo "  this script and confirm zero matches in the post-rotation window."
  else
    echo "OK: no leak signatures found in the scanned window."
    echo "  Re-run after every deploy that adds or moves auth surfaces."
  fi
fi
