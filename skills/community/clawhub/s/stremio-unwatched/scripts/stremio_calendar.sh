#!/usr/bin/env bash
# Stremio calendar: show upcoming episodes and optionally sync to Google Calendar.
# Usage:
#   stremio_calendar.sh                     # Show upcoming episodes (next 30 days)
#   stremio_calendar.sh --days 7            # Next 7 days
#   stremio_calendar.sh --filter "name"     # Filter by show name
#   stremio_calendar.sh --json              # JSON output
#   stremio_calendar.sh --gcal-sync         # Sync to Google Calendar (requires gog)
#   stremio_calendar.sh --gcal-clear        # Remove all events from Stremio TV calendar
# Google Calendar sync creates a dedicated "Stremio TV" calendar, never the default.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CINEMETA="https://v3-cinemeta.strem.io"
STREMIO_API="https://api.strem.io/api"
GCAL_NAME="Stremio TV"
# Purple/grape color for episode events
GCAL_EVENT_COLOR="3"

DAYS=30
FILTER_NAME=""
JSON_OUTPUT=false
GCAL_SYNC=false
GCAL_CLEAR=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --days) DAYS="$2"; shift 2 ;;
    --filter) FILTER_NAME="$2"; shift 2 ;;
    --json) JSON_OUTPUT=true; shift ;;
    --gcal-sync) GCAL_SYNC=true; shift ;;
    --gcal-clear) GCAL_CLEAR=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Fetch library series IDs
lib_args=()
[[ -n "$FILTER_NAME" ]] && lib_args+=(--filter "$FILTER_NAME")
library=$("${SCRIPT_DIR}/stremio_library.sh" "${lib_args[@]}")
count=$(echo "$library" | jq 'length')

if [[ "$count" -eq 0 ]]; then
  echo "No series in library" >&2
  echo "[]"
  exit 0
fi

# Collect IMDB IDs (Cinemeta calendar endpoint accepts up to 100)
ids=$(echo "$library" | jq -r '.[].id' | head -100 | paste -sd, -)

echo "Fetching calendar for ${count} series..." >&2

# Call the Cinemeta calendar-videos endpoint
calendar_resp=$(curl -sfL "${CINEMETA}/catalog/series/calendar-videos/calendarVideosIds=${ids}.json" 2>/dev/null) || {
  echo "error: failed to fetch calendar data" >&2
  exit 1
}

# Build a name lookup from library
name_lookup=$(echo "$library" | jq 'map({key: .id, value: .name}) | from_entries')

# Parse date range
now=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)
if [[ "$(uname)" == "Darwin" ]]; then
  future=$(date -u -v+${DAYS}d +%Y-%m-%dT%H:%M:%S.000Z)
else
  future=$(date -u -d "+${DAYS} days" +%Y-%m-%dT%H:%M:%S.000Z)
fi

# Extract and filter upcoming episodes
upcoming=$(echo "$calendar_resp" | jq --arg now "$now" --arg future "$future" \
  --argjson names "$name_lookup" '
  [.metasDetailed // [] | .[] | .id as $show_id | .name as $show_name |
    (.videos // [])[] |
    select(.released != null and .released >= $now and .released <= $future) |
    {
      show: ($names[$show_id] // $show_name // $show_id),
      show_id: $show_id,
      season: (.season // 0),
      episode: (.episode // 0),
      title: (.title // .name // ""),
      video_id: .id,
      released: .released,
      thumbnail: (.thumbnail // "")
    }
  ] | sort_by(.released)')

total=$(echo "$upcoming" | jq 'length')
echo "${total} upcoming episode(s) in next ${DAYS} days" >&2

# Google Calendar sync
if $GCAL_SYNC || $GCAL_CLEAR; then
  if ! command -v gog &>/dev/null; then
    echo "error: gog (gogcli) is required for Google Calendar sync" >&2
    echo "Install: brew install steipete/tap/gogcli" >&2
    exit 1
  fi

  # Find or create the dedicated Stremio TV calendar
  echo "Looking for '${GCAL_NAME}' calendar..." >&2
  calendars=$(gog calendar calendars --json --no-input 2>/dev/null) || {
    echo "error: failed to list Google Calendars (is gog authenticated?)" >&2
    exit 1
  }

  cal_id=$(echo "$calendars" | jq -r \
    --arg name "$GCAL_NAME" \
    '.calendars[] | select(.summary == $name) | .id // empty' | head -1)

  if [[ -z "$cal_id" ]]; then
    if $GCAL_CLEAR; then
      echo "No '${GCAL_NAME}' calendar found, nothing to clear" >&2
      exit 0
    fi
    echo "Creating '${GCAL_NAME}' calendar..." >&2
    # Try gog calendar calendars create first
    create_resp=$(gog calendar calendars create --summary "$GCAL_NAME" --json --no-input 2>/dev/null) || {
      echo "error: could not create '${GCAL_NAME}' calendar via gog" >&2
      echo "Please create a calendar named '${GCAL_NAME}' manually in Google Calendar" >&2
      exit 1
    }
    cal_id=$(echo "$create_resp" | jq -r '.id // empty')
    [[ -n "$cal_id" ]] || {
      echo "error: calendar created but could not extract ID" >&2
      exit 1
    }
    echo "Created calendar: ${cal_id}" >&2
  fi

  if $GCAL_CLEAR; then
    echo "Clearing all events from '${GCAL_NAME}'..." >&2
    # List events in a wide window and delete them
    if [[ "$(uname)" == "Darwin" ]]; then
      from=$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ)
      to=$(date -u -v+365d +%Y-%m-%dT%H:%M:%SZ)
    else
      from=$(date -u -d "-30 days" +%Y-%m-%dT%H:%M:%SZ)
      to=$(date -u -d "+365 days" +%Y-%m-%dT%H:%M:%SZ)
    fi
    events=$(gog calendar events "$cal_id" --from "$from" --to "$to" --json --no-input 2>/dev/null) || events='{"events":[]}'
    event_ids=$(echo "$events" | jq -r '.events[].id // empty')
    del_count=0
    for eid in $event_ids; do
      gog calendar delete "$cal_id" "$eid" --no-input 2>/dev/null && ((del_count++)) || true
    done
    echo "Deleted ${del_count} event(s)" >&2
    exit 0
  fi

  # Sync upcoming episodes as events
  echo "Syncing ${total} episode(s) to '${GCAL_NAME}'..." >&2

  # Fetch existing events in the date range to avoid duplicates
  if [[ "$(uname)" == "Darwin" ]]; then
    from_gcal=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    to_gcal=$(date -u -v+${DAYS}d +%Y-%m-%dT%H:%M:%SZ)
  else
    from_gcal=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    to_gcal=$(date -u -d "+${DAYS} days" +%Y-%m-%dT%H:%M:%SZ)
  fi
  existing=$(gog calendar events "$cal_id" --from "$from_gcal" --to "$to_gcal" --json --no-input 2>/dev/null) || existing='{"events":[]}'
  existing_summaries=$(echo "$existing" | jq -r '[.events[].summary // ""] | .[]')

  synced=0
  skipped=0
  echo "$upcoming" | jq -c '.[]' | while IFS= read -r ep; do
    show=$(echo "$ep" | jq -r '.show')
    season=$(echo "$ep" | jq -r '.season')
    episode_num=$(echo "$ep" | jq -r '.episode')
    title=$(echo "$ep" | jq -r '.title')
    released=$(echo "$ep" | jq -r '.released')
    video_id=$(echo "$ep" | jq -r '.video_id')

    summary="${show} S$(printf '%02d' "$season")E$(printf '%02d' "$episode_num")"
    [[ -n "$title" && "$title" != "null" ]] && summary="${summary}: ${title}"

    # Skip if event already exists (by summary match)
    if echo "$existing_summaries" | grep -qF "$summary"; then
      ((skipped++)) || true
      continue
    fi

    # Parse released timestamp for event time (1-hour event at air time)
    event_start="$released"
    # Calculate end time (+1h) using date manipulation
    if [[ "$(uname)" == "Darwin" ]]; then
      start_epoch=$(date -jf "%Y-%m-%dT%H:%M:%S" "${released%%.*}" +%s 2>/dev/null || echo "")
      if [[ -n "$start_epoch" ]]; then
        end_epoch=$((start_epoch + 3600))
        event_end=$(date -u -r "$end_epoch" +%Y-%m-%dT%H:%M:%SZ)
      else
        event_end="$event_start"
      fi
    else
      event_end=$(date -u -d "${released} + 1 hour" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || echo "$event_start")
    fi

    description="Stremio: ${video_id}"

    gog calendar create "$cal_id" \
      --summary "$summary" \
      --description "$description" \
      --from "$event_start" --to "$event_end" \
      --event-color "$GCAL_EVENT_COLOR" \
      --no-input 2>/dev/null && {
        ((synced++)) || true
        echo "  + ${summary}" >&2
      } || {
        echo "  ! Failed: ${summary}" >&2
      }
  done

  echo "Sync complete (created: ${synced}, skipped: ${skipped})" >&2
fi

# Output
if $JSON_OUTPUT; then
  echo "$upcoming"
else
  if [[ "$total" -eq 0 ]]; then
    echo "No upcoming episodes in the next ${DAYS} days"
    exit 0
  fi
  printf "%-12s  %-28s %3s %3s  %-28s\n" "DATE" "SHOW" "S" "E" "TITLE"
  printf "%-12s  %-28s %3s %3s  %-28s\n" "----" "----" "--" "--" "-----"
  echo "$upcoming" | jq -r '.[] |
    [(.released[:10]), .show[:28], (.season|tostring), (.episode|tostring), .title[:28]] | @tsv' |
    while IFS=$'\t' read -r date show s e title; do
      printf "%-12s  %-28s %3s %3s  %-28s\n" "$date" "$show" "$s" "$e" "$title"
    done
fi
