#!/usr/bin/env bash
# select-new-entries.sh — print ox distill history entry ids for a team
# that fall within the --since window and have NOT yet been included in a
# prior summary run.
#
# Usage: select-new-entries.sh <team_id> <since> <state_file>
#
# Arguments:
#   <team_id>     Team slug, id, or name. Passed verbatim to
#                 `ox distill history list --team`, and used as the key
#                 inside the state file's .teams map.
#   <since>       Window duration (e.g. 24h). Passed verbatim to
#                 `--since`. Anything ox's flag parser accepts works.
#                 ox auto-expands the window around the UTC day
#                 boundary, so `24h` is the pipeline's default.
#   <state_file>  Absolute path to sageox-summary-state.json (need not
#                 exist — a missing file is treated as empty state).
#
# Stdout: one entry id per line, sorted ascending. Empty if nothing new.
# Stderr: single-line warnings (malformed state, failed ox call).
# Exit:
#   0 — success (empty output is not a failure, including when the ox
#       call fails — the caller skips the team and continues)
#   2 — usage error
#   3 — internal error (required tool missing)

set -euo pipefail

if [ $# -ne 3 ]; then
  echo "usage: $(basename "$0") <team_id> <since> <state_file>" >&2
  exit 2
fi

TEAM_ID="$1"
SINCE="$2"
STATE_FILE="$3"

command -v jq >/dev/null 2>&1 || { echo "error: jq is required" >&2; exit 3; }
command -v ox >/dev/null 2>&1 || { echo "error: ox is required" >&2; exit 3; }

ID_RE='^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9a-f-]+$'

# Ask ox which distilled daily entries fall in the window. We pin the
# layer to `daily` because weekly/monthly roll-ups would double-count
# material the summary already synthesized from the daily layer.
CANDIDATES=""
if OX_OUT="$(ox distill history list \
  --team "$TEAM_ID" \
  --since "$SINCE" \
  --layer daily \
  --format json 2>/dev/null)"; then
  CANDIDATES="$(
    printf '%s' "$OX_OUT" \
      | jq -r '.data.entries[]?.id // empty' 2>/dev/null \
      | grep -E "$ID_RE" \
      | sort -u || true
  )"
else
  echo "warning: ox distill history list failed for team $TEAM_ID" >&2
fi

# Already-summarized set for this team. Missing state → empty
# (first run). Malformed → empty + stderr warning.
ALREADY_INCLUDED=""
if [ -f "$STATE_FILE" ]; then
  if ! jq -e . "$STATE_FILE" >/dev/null 2>&1; then
    echo "warning: $STATE_FILE was unreadable, starting from empty state" >&2
  else
    ALREADY_INCLUDED="$(
      jq -r --arg tid "$TEAM_ID" \
        '.teams[$tid].included_ids[]? // empty' "$STATE_FILE" \
      | grep -E "$ID_RE" \
      | sort -u || true
    )"
  fi
fi

# Set difference: CANDIDATES − ALREADY_INCLUDED. Both sides are already
# sorted and regex-validated; temp files avoid multi-line `awk -v`
# quirks on BSD.
CAND_TMP="$(mktemp)"
INCL_TMP="$(mktemp)"
trap 'rm -f "$CAND_TMP" "$INCL_TMP" 2>/dev/null' EXIT

printf '%s\n' "$CANDIDATES"       | grep -v '^$' > "$CAND_TMP" || true
printf '%s\n' "$ALREADY_INCLUDED" | grep -v '^$' > "$INCL_TMP" || true

comm -23 "$CAND_TMP" "$INCL_TMP"
