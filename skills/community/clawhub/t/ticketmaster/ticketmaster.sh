#!/usr/bin/env bash
# Security Manifest
# - Env: TM_API_KEY
# - Endpoints: https://app.ticketmaster.com/discovery/v2/*.json
# - Reads: TM_API_KEY from the environment
# - Writes: stdout and stderr only
# - Network: GET requests only to Ticketmaster Discovery API

set -euo pipefail

BASE_URL="https://app.ticketmaster.com/discovery/v2"

usage() {
  cat <<'EOF'
Usage:
  ./ticketmaster.sh events <keyword> [--city CITY] [--country CODE] [--classification NAME] [--start ISO] [--end ISO] [--size N] [--page N] [--locale LOCALE]
  ./ticketmaster.sh event <event_id> [--locale LOCALE]
  ./ticketmaster.sh venues <keyword> [--city CITY] [--country CODE] [--size N] [--page N] [--locale LOCALE]
  ./ticketmaster.sh venue <venue_id> [--locale LOCALE]
  ./ticketmaster.sh attractions <keyword> [--size N] [--page N] [--locale LOCALE]
  ./ticketmaster.sh attraction <attraction_id> [--locale LOCALE]
  ./ticketmaster.sh classifications [--locale LOCALE]

Environment:
  TM_API_KEY   Required Ticketmaster Discovery API key
EOF
}

need_env() {
  local name="$1"
  [[ -n "${!name:-}" ]] || {
    echo "Missing required environment variable: $name" >&2
    exit 1
  }
}

need_bin() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required binary: $1" >&2
    exit 1
  }
}

append_param() {
  local key="$1"
  local value="$2"
  [[ -n "$value" ]] || return 0
  CURL_ARGS+=(--data-urlencode "${key}=${value}")
}

emit() {
  if command -v jq >/dev/null 2>&1; then
    jq .
  else
    cat
  fi
}

parse_common_flags() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --city)
        CITY="${2:-}"
        shift 2
        ;;
      --country)
        COUNTRY="${2:-}"
        shift 2
        ;;
      --classification)
        CLASSIFICATION="${2:-}"
        shift 2
        ;;
      --start)
        START="${2:-}"
        shift 2
        ;;
      --end)
        END="${2:-}"
        shift 2
        ;;
      --size)
        SIZE="${2:-}"
        shift 2
        ;;
      --page)
        PAGE="${2:-}"
        shift 2
        ;;
      --locale)
        LOCALE="${2:-}"
        shift 2
        ;;
      *)
        echo "Unknown flag: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
  done
}

call_endpoint() {
  local path="$1"
  shift

  CURL_ARGS=(--silent --show-error --fail --get "${BASE_URL}${path}")
  append_param "apikey" "$TM_API_KEY"

  while [[ $# -gt 0 ]]; do
    CURL_ARGS+=(--data-urlencode "$1")
    shift
  done

  curl "${CURL_ARGS[@]}" | emit
}

main() {
  need_bin curl
  need_env TM_API_KEY

  [[ $# -gt 0 ]] || {
    usage >&2
    exit 1
  }

  local command="$1"
  shift

  CITY=""
  COUNTRY=""
  CLASSIFICATION=""
  START=""
  END=""
  SIZE=""
  PAGE=""
  LOCALE=""

  case "$command" in
    events)
      [[ $# -gt 0 ]] || {
        echo "events requires a keyword" >&2
        usage >&2
        exit 1
      }
      local keyword="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/events.json" \
        "keyword=${keyword}" \
        "city=${CITY}" \
        "countryCode=${COUNTRY}" \
        "classificationName=${CLASSIFICATION}" \
        "startDateTime=${START}" \
        "endDateTime=${END}" \
        "size=${SIZE}" \
        "page=${PAGE}" \
        "locale=${LOCALE}"
      ;;
    event)
      [[ $# -ge 1 ]] || {
        echo "event requires an event ID" >&2
        usage >&2
        exit 1
      }
      local event_id="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/events/${event_id}.json" "locale=${LOCALE}"
      ;;
    venues)
      [[ $# -gt 0 ]] || {
        echo "venues requires a keyword" >&2
        usage >&2
        exit 1
      }
      local venue_keyword="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/venues.json" \
        "keyword=${venue_keyword}" \
        "city=${CITY}" \
        "countryCode=${COUNTRY}" \
        "size=${SIZE}" \
        "page=${PAGE}" \
        "locale=${LOCALE}"
      ;;
    venue)
      [[ $# -ge 1 ]] || {
        echo "venue requires a venue ID" >&2
        usage >&2
        exit 1
      }
      local venue_id="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/venues/${venue_id}.json" "locale=${LOCALE}"
      ;;
    attractions)
      [[ $# -gt 0 ]] || {
        echo "attractions requires a keyword" >&2
        usage >&2
        exit 1
      }
      local attraction_keyword="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/attractions.json" \
        "keyword=${attraction_keyword}" \
        "size=${SIZE}" \
        "page=${PAGE}" \
        "locale=${LOCALE}"
      ;;
    attraction)
      [[ $# -ge 1 ]] || {
        echo "attraction requires an attraction ID" >&2
        usage >&2
        exit 1
      }
      local attraction_id="$1"
      shift
      parse_common_flags "$@"
      call_endpoint "/attractions/${attraction_id}.json" "locale=${LOCALE}"
      ;;
    classifications)
      parse_common_flags "$@"
      call_endpoint "/classifications.json" "locale=${LOCALE}"
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      echo "Unknown command: $command" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main "$@"
