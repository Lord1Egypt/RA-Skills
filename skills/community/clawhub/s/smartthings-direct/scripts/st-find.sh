#!/usr/bin/env bash
# Fuzzy-find SmartThings devices by label substring (case-insensitive).
# Prints matching rows as: <deviceId>\t<label>\t<roomId>
#
# Usage:
#   st-find.sh <name-fragment>        # human-readable table
#   st-find.sh --json <name-fragment> # JSON array of matches
#   st-find.sh --id   <name-fragment> # deviceId(s) only, one per line
#
# Exits 1 if no matches.

set -euo pipefail

mode=table
if [[ "${1:-}" == --json ]]; then mode=json; shift; fi
if [[ "${1:-}" == --id   ]]; then mode=id;   shift; fi

query="${1:-}"
if [[ -z "$query" ]]; then
  echo "Usage: $0 [--json|--id] <name-fragment>" >&2
  exit 2
fi

# Escape regex metacharacters in the query for jq's test().
esc=$(printf '%s' "$query" | sed 's/[][(){}.^$|*+?\\]/\\&/g')

devices=$(smartthings devices --json)

matches=$(jq --arg q "$esc" '[.[] | select(.label | test($q; "i"))]' <<<"$devices")

count=$(jq 'length' <<<"$matches")
if [[ "$count" -eq 0 ]]; then
  echo "No SmartThings devices matched: $query" >&2
  exit 1
fi

case "$mode" in
  json)
    echo "$matches"
    ;;
  id)
    jq -r '.[].deviceId' <<<"$matches"
    ;;
  table)
    jq -r '.[] | [.deviceId, .label, (.roomId // "-")] | @tsv' <<<"$matches"
    ;;
esac
