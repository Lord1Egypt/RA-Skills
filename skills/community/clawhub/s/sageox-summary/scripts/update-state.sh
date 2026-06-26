#!/usr/bin/env bash
# update-state.sh — atomically merge a set of newly-summarized entry ids
# into the per-team included_ids list, prune stale entries, and write
# the result back via a temp-file rename.
#
# Usage: update-state.sh <state_file> <team_id>
#        (reads newline-separated entry ids from stdin)
#
# Arguments:
#   <state_file>  Absolute path to sageox-summary-state.json
#   <team_id>     Team id key to merge under
#
# Stdin: one entry id per line (may be empty). Lines not matching the
# distill-output id regex are silently dropped.
#
# Stdout: nothing on success.
# Stderr: single-line warnings (e.g. malformed prior state).
# Exit:
#   0 — success
#   2 — usage error
#   3 — internal error (required tool missing, write failed)

set -euo pipefail

if [ $# -ne 2 ]; then
  echo "usage: $(basename "$0") <state_file> <team_id>" >&2
  exit 2
fi

STATE_FILE="$1"
TEAM_ID="$2"

command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 3; }

ID_RE='^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9a-f-]+$'

# Prune cutoff: drop entries whose date prefix is strictly older than
# YESTERDAY_UTC. `ox distill history list --since 24h` auto-expands its
# window around the day boundary, so the candidate set spans at most
# today + yesterday UTC; keeping state at `>= yesterday` guarantees no
# id in range is ever dropped. BSD `date` uses `-v`; GNU uses `-d`.
CUTOFF_UTC="$(date -u -v-1d +%Y-%m-%d 2>/dev/null \
  || date -u -d 'yesterday' +%Y-%m-%d)"
NOW_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# Read and regex-filter added entry ids from stdin.
ADDED="$(grep -E "$ID_RE" || true)"

# Load existing state. Missing → {}. Malformed → {} + stderr warning.
if [ -f "$STATE_FILE" ]; then
  if ! EXISTING="$(jq -c . "$STATE_FILE" 2>/dev/null)"; then
    echo "warning: $STATE_FILE was unreadable, starting from empty state" >&2
    EXISTING='{}'
  fi
else
  EXISTING='{}'
fi

# Merge + prune + dedupe in a single jq pass. Preserves other teams'
# entries verbatim — only the target team's included_ids is rewritten.
NEW_STATE="$(
  jq -n \
    --argjson existing "$EXISTING" \
    --arg tid "$TEAM_ID" \
    --arg added "$ADDED" \
    --arg cutoff "$CUTOFF_UTC" \
    --arg now "$NOW_UTC" \
    --arg re "$ID_RE" \
    '
      ($existing // {}) as $e
    | ($e.teams // {}) as $teams
    | ($teams[$tid].included_ids // []) as $prior
    | ($added | split("\n") | map(select(. != ""))) as $new
    | (($prior + $new)
        | map(select(test($re)))
        | map(select(.[0:10] >= $cutoff))
        | unique
      ) as $merged
    | $e
      | .teams = ($teams | .[$tid] = {included_ids: $merged})
      | .updated_at = $now
    '
)"

# Atomic write: temp file in the same directory, then rename.
STATE_DIR="$(dirname "$STATE_FILE")"
mkdir -p "$STATE_DIR"
TMP_FILE="${STATE_FILE}.tmp.$$"
trap 'rm -f "$TMP_FILE" 2>/dev/null' EXIT
printf '%s\n' "$NEW_STATE" > "$TMP_FILE"
mv -f "$TMP_FILE" "$STATE_FILE"
