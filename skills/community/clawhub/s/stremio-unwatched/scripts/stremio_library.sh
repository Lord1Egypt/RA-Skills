#!/usr/bin/env bash
# Fetch Stremio library items (series by default).
# Usage:
#   stremio_library.sh                    # All series in library
#   stremio_library.sh --filter "name"    # Filter by show name (case-insensitive)
#   stremio_library.sh --id tt1234567     # Get specific show by IMDB ID
#   stremio_library.sh --type movie       # Get movies instead of series
#   stremio_library.sh --all              # All types, no filter
#   stremio_library.sh --raw              # Raw API output (no filtering)
# Output: JSON array to stdout
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STREMIO_API="https://api.strem.io/api"

FILTER_NAME=""
FILTER_ID=""
FILTER_TYPE="series"
RAW=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --filter) FILTER_NAME="$2"; shift 2 ;;
    --id) FILTER_ID="$2"; shift 2 ;;
    --type) FILTER_TYPE="$2"; shift 2 ;;
    --all) FILTER_TYPE=""; shift ;;
    --raw) RAW=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Get auth key
AUTH_KEY=$("${SCRIPT_DIR}/stremio_auth.sh" --key) || exit 1

# Fetch all library items
resp=$(curl -sf -X POST "${STREMIO_API}/datastoreGet" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg key "$AUTH_KEY" \
    '{authKey: $key, collection: "libraryItem", all: true}')")

if echo "$resp" | jq -e '.error' &>/dev/null; then
  echo "error: $(echo "$resp" | jq -r '.error.message')" >&2
  exit 1
fi

items=$(echo "$resp" | jq '.result // []')

if $RAW; then
  echo "$items"
  exit 0
fi

# Apply filters
filtered=$(echo "$items" | jq --arg type "$FILTER_TYPE" \
  --arg name "$FILTER_NAME" --arg id "$FILTER_ID" '
  [.[] | select(
    (.removed | not) and
    (.temp | not) and
    (if $type != "" then .type == $type else true end) and
    (if $name != "" then (.name | ascii_downcase | contains($name | ascii_downcase)) else true end) and
    (if $id != "" then ._id == $id else true end)
  )]
  | sort_by(.name)
  | [.[] | {
    id: ._id,
    name: .name,
    type: .type,
    poster: .poster,
    last_watched: .state.lastWatched,
    video_id: .state.video_id,
    watched_bitfield: .state.watched,
    time_offset: .state.timeOffset,
    duration: .state.duration,
    times_watched: .state.timesWatched,
    overall_time_watched: .state.overallTimeWatched,
    no_notif: .state.noNotif
  }]')

echo "$filtered"
