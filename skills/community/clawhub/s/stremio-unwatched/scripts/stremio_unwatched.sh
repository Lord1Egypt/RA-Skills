#!/usr/bin/env bash
# Find unwatched episodes for series in Stremio library.
# Usage:
#   stremio_unwatched.sh                        # All unwatched across library
#   stremio_unwatched.sh --filter "show name"   # Specific show by name
#   stremio_unwatched.sh --id tt1234567         # Specific show by IMDB ID
#   stremio_unwatched.sh --season 2             # Only season 2
#   stremio_unwatched.sh --json                 # JSON output (default is table)
#   stremio_unwatched.sh --summary              # Just counts per show
# Output: table or JSON to stdout
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CINEMETA="https://v3-cinemeta.strem.io"
NODE_CMD="${NODE_CMD:-$(command -v bun 2>/dev/null || command -v node 2>/dev/null)}"

FILTER_NAME=""
FILTER_ID=""
FILTER_SEASON=""
JSON_OUTPUT=false
SUMMARY=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --filter) FILTER_NAME="$2"; shift 2 ;;
    --id) FILTER_ID="$2"; shift 2 ;;
    --season) FILTER_SEASON="$2"; shift 2 ;;
    --json) JSON_OUTPUT=true; shift ;;
    --summary) SUMMARY=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

[[ -n "$NODE_CMD" ]] || { echo "error: node or bun required for bitfield decoding" >&2; exit 1; }

# Build library args
lib_args=()
[[ -n "$FILTER_NAME" ]] && lib_args+=(--filter "$FILTER_NAME")
[[ -n "$FILTER_ID" ]] && lib_args+=(--id "$FILTER_ID")

# Fetch library
library=$("${SCRIPT_DIR}/stremio_library.sh" "${lib_args[@]}")
count=$(echo "$library" | jq 'length')

if [[ "$count" -eq 0 ]]; then
  echo "No series found in library" >&2
  echo "[]"
  exit 0
fi

all_unwatched="[]"

for i in $(seq 0 $((count - 1))); do
  item=$(echo "$library" | jq ".[$i]")
  show_id=$(echo "$item" | jq -r '.id')
  show_name=$(echo "$item" | jq -r '.name')
  bitfield=$(echo "$item" | jq -r '.watched_bitfield // ""')
  current_video=$(echo "$item" | jq -r '.video_id // ""')
  time_offset=$(echo "$item" | jq -r '.time_offset // 0')
  duration=$(echo "$item" | jq -r '.duration // 0')

  echo "Checking: ${show_name} (${show_id})..." >&2

  # Fetch full metadata from Cinemeta
  meta=$(curl -sfL "${CINEMETA}/meta/series/${show_id}.json" 2>/dev/null) || {
    echo "  warning: could not fetch meta for ${show_id}" >&2
    continue
  }

  # Extract and sort videos by season, episode, release date
  videos=$(echo "$meta" | jq '
    [.meta.videos // [] | .[]
      | select(.season and .episode and (.season | type) == "number" and (.episode | type) == "number")
      | {
          id: .id,
          title: (.title // .name // ""),
          season: .season,
          episode: .episode,
          released: .released,
          thumbnail: (.thumbnail // "")
        }
    ] | sort_by(.season, .episode, .released)')

  video_count=$(echo "$videos" | jq 'length')
  if [[ "$video_count" -eq 0 ]]; then
    echo "  no episodes found" >&2
    continue
  fi

  # Apply season filter
  if [[ -n "$FILTER_SEASON" ]]; then
    videos=$(echo "$videos" | jq --argjson s "$FILTER_SEASON" \
      '[.[] | select(.season == $s)]')
    video_count=$(echo "$videos" | jq 'length')
    if [[ "$video_count" -eq 0 ]]; then
      echo "  no episodes in season ${FILTER_SEASON}" >&2
      continue
    fi
  fi

  # Get sorted video IDs for bitfield decoding
  video_ids=$(echo "$videos" | jq '[.[].id]')

  # Decode watched bitfield
  watched="{}"
  if [[ -n "$bitfield" && "$bitfield" != "null" ]]; then
    # For bitfield decoding, we need ALL video IDs (not just filtered season)
    # since bitfield positions are based on the full sorted list
    all_videos=$(echo "$meta" | jq '
      [.meta.videos // [] | .[]
        | select(.season and .episode and (.season | type) == "number" and (.episode | type) == "number")
      ] | sort_by(.season, .episode, .released) | [.[].id]')
    watched=$("$NODE_CMD" "${SCRIPT_DIR}/bitfield_decode.mjs" "$bitfield" "$all_videos" 2>/dev/null) || watched="{}"
  fi

  now=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)

  # Find unwatched episodes (only those AFTER the last watched episode)
  show_unwatched=$(echo "$videos" | jq \
    --argjson watched "$watched" \
    --arg now "$now" \
    --arg current "$current_video" \
    --argjson offset "$time_offset" \
    --argjson dur "$duration" \
    --arg show "$show_name" \
    --arg show_id "$show_id" '

    # Find the index of the last watched/in-progress episode
    ([to_entries[] | select(
      ($watched[.value.id] // false) or .value.id == $current
    ) | .key] | if length > 0 then max else -1 end) as $last_idx |

    # Take only episodes after the last watched
    [.[$last_idx + 1:][] |
      select(.id) |
      (.id) as $vid |
      ($watched[$vid] // false) as $is_watched |
      (.released and (.released <= $now)) as $aired |
      ($vid == $current and $offset > 0 and $dur > 0) as $in_progress |
      (if $in_progress then (($offset / $dur) * 100 | floor) else 0 end) as $progress |
      select(
        $aired and
        ($is_watched | not) and
        (if $in_progress then $progress < 70 else true end)
      ) |
      {
        show: $show,
        show_id: $show_id,
        season: .season,
        episode: .episode,
        title: .title,
        video_id: .id,
        released: .released,
        status: (if $in_progress then "in_progress (\($progress)%)" else "unwatched" end)
      }
    ]')

  unwatched_count=$(echo "$show_unwatched" | jq 'length')
  echo "  ${unwatched_count} unwatched episode(s)" >&2

  all_unwatched=$(echo "$all_unwatched" | jq --argjson new "$show_unwatched" '. + $new')
done

total=$(echo "$all_unwatched" | jq 'length')
echo "---" >&2
echo "Total: ${total} unwatched episode(s)" >&2

if $SUMMARY; then
  echo "$all_unwatched" | jq '
    group_by(.show) | [.[] | {
      show: .[0].show,
      show_id: .[0].show_id,
      unwatched: length,
      seasons: ([.[].season] | unique)
    }]'
elif $JSON_OUTPUT; then
  echo "$all_unwatched"
else
  # Table output
  if [[ "$total" -eq 0 ]]; then
    echo "All caught up!"
    exit 0
  fi
  printf "%-30s %3s %3s  %-30s  %s\n" "SHOW" "S" "E" "TITLE" "STATUS"
  printf "%-30s %3s %3s  %-30s  %s\n" "----" "--" "--" "-----" "------"
  echo "$all_unwatched" | jq -r '.[] |
    [.show[:30], (.season|tostring), (.episode|tostring), .title[:30], .status] | @tsv' |
    while IFS=$'\t' read -r show s e title status; do
      printf "%-30s %3s %3s  %-30s  %s\n" "$show" "$s" "$e" "$title" "$status"
    done
fi
