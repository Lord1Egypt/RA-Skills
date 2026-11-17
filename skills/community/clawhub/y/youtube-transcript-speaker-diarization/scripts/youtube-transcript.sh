#!/usr/bin/env bash

set -euo pipefail

DEFAULT_BASE_URL="https://diarize.io"
DEFAULT_FORMAT="txt"
DEFAULT_TIMEOUT_SECONDS="180"
DEFAULT_POLL_INTERVAL_SECONDS="10"

CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/openclaw.json}"

print_usage() {
  cat <<'EOF'
Usage:
  youtube-transcript.sh submit <youtube-url>
  youtube-transcript.sh status <job-id>
  youtube-transcript.sh fetch <job-id> [txt|json|srt|vtt]
  youtube-transcript.sh run <youtube-url> [txt|json|srt|vtt] [timeout-seconds] [poll-interval-seconds]
EOF
}

read_skill_value() {
  local key="$1"

  if [[ -f "$CONFIG_PATH" ]] && command -v jq >/dev/null 2>&1; then
    jq -r --arg key "$key" '
      .skills.entries["youtube-transcript-speaker-diarization"][$key]
      // .skills.entries["youtube-transcript"][$key]
      // empty
    ' "$CONFIG_PATH" 2>/dev/null || true
    return
  fi

  printf ""
}

resolve_api_key() {
  local key=""
  key="${YOUTUBE_TRANSCRIPT_API_KEY:-}"
  if [[ -z "$key" ]]; then
    key="${DIARIZE_API_KEY:-}"
  fi
  if [[ -z "$key" ]]; then
    key="$(read_skill_value apiKey)"
  fi

  if [[ -z "$key" ]]; then
    echo "Missing API key. Set YOUTUBE_TRANSCRIPT_API_KEY, DIARIZE_API_KEY, or skills.entries[\"youtube-transcript-speaker-diarization\"].apiKey." >&2
    exit 1
  fi

  printf "%s" "$key"
}

resolve_base_url() {
  local base_url=""
  base_url="${YOUTUBE_TRANSCRIPT_BASE_URL:-}"
  if [[ -z "$base_url" ]]; then
    base_url="${DIARIZE_BASE_URL:-}"
  fi
  if [[ -z "$base_url" ]]; then
    base_url="$(read_skill_value baseUrl)"
  fi
  if [[ -z "$base_url" ]]; then
    base_url="$DEFAULT_BASE_URL"
  fi

  base_url="${base_url%/}"
  printf "%s" "$base_url"
}

api_json() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local api_key="$4"
  local base_url="$5"

  if [[ -n "$body" ]]; then
    curl -fsS -X "$method" \
      -H "Authorization: Bearer $api_key" \
      -H "Content-Type: application/json" \
      "${base_url}${path}" \
      -d "$body"
  else
    curl -fsS -X "$method" \
      -H "Authorization: Bearer $api_key" \
      "${base_url}${path}"
  fi
}

submit_job() {
  local youtube_url="$1"
  local api_key="$2"
  local base_url="$3"

  api_json "POST" "/api/v1/jobs" "{\"youtubeUrl\":$(jq -Rn --arg value "$youtube_url" '$value')}" "$api_key" "$base_url"
}

get_status() {
  local job_id="$1"
  local api_key="$2"
  local base_url="$3"

  api_json "GET" "/api/v1/jobs/${job_id}" "" "$api_key" "$base_url"
}

fetch_transcript() {
  local job_id="$1"
  local format="$2"
  local api_key="$3"
  local base_url="$4"

  curl -fsS \
    -H "Authorization: Bearer $api_key" \
    "${base_url}/api/v1/jobs/${job_id}/transcript/${format}"
}

require_format() {
  local format="${1:-$DEFAULT_FORMAT}"
  case "$format" in
    txt|json|srt|vtt) printf "%s" "$format" ;;
    *)
      echo "Unsupported format: $format" >&2
      exit 1
      ;;
  esac
}

run_job() {
  local youtube_url="$1"
  local format="$2"
  local timeout_seconds="$3"
  local poll_interval_seconds="$4"
  local api_key="$5"
  local base_url="$6"

  local create_response
  local job_id
  local status
  local started_at
  local now

  create_response="$(submit_job "$youtube_url" "$api_key" "$base_url")"
  job_id="$(printf "%s" "$create_response" | jq -r '.jobId // empty')"
  status="$(printf "%s" "$create_response" | jq -r '.status // empty')"

  if [[ -z "$job_id" ]]; then
    echo "Failed to create job. Response:" >&2
    printf "%s\n" "$create_response" >&2
    exit 1
  fi

  if [[ "$status" == "COMPLETED" ]]; then
    fetch_transcript "$job_id" "$format" "$api_key" "$base_url"
    return
  fi

  started_at="$(date +%s)"

  while true; do
    now="$(date +%s)"
    if (( now - started_at >= timeout_seconds )); then
      echo "Timed out waiting for job ${job_id}. Check it later with:" >&2
      echo "  $(basename "$0") status ${job_id}" >&2
      exit 2
    fi

    sleep "$poll_interval_seconds"

    local status_response
    status_response="$(get_status "$job_id" "$api_key" "$base_url")"
    status="$(printf "%s" "$status_response" | jq -r '.status // empty')"

    case "$status" in
      COMPLETED)
        fetch_transcript "$job_id" "$format" "$api_key" "$base_url"
        return
        ;;
      FAILED)
        echo "Job ${job_id} failed:" >&2
        printf "%s\n" "$status_response" | jq . >&2
        exit 1
        ;;
      *)
        ;;
    esac
  done
}

main() {
  if ! command -v curl >/dev/null 2>&1; then
    echo "curl is required." >&2
    exit 1
  fi
  if ! command -v jq >/dev/null 2>&1; then
    echo "jq is required." >&2
    exit 1
  fi

  local command="${1:-}"
  if [[ -z "$command" ]]; then
    print_usage
    exit 1
  fi
  shift

  local api_key
  local base_url
  api_key="$(resolve_api_key)"
  base_url="$(resolve_base_url)"

  case "$command" in
    submit)
      if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
      fi
      submit_job "$1" "$api_key" "$base_url" | jq .
      ;;
    status)
      if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
      fi
      get_status "$1" "$api_key" "$base_url" | jq .
      ;;
    fetch)
      if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
      fi
      local format
      format="$(require_format "${2:-$DEFAULT_FORMAT}")"
      fetch_transcript "$1" "$format" "$api_key" "$base_url"
      ;;
    run)
      if [[ $# -lt 1 ]]; then
        print_usage
        exit 1
      fi
      local format
      local timeout_seconds
      local poll_interval_seconds
      format="$(require_format "${2:-$DEFAULT_FORMAT}")"
      timeout_seconds="${3:-$DEFAULT_TIMEOUT_SECONDS}"
      poll_interval_seconds="${4:-$DEFAULT_POLL_INTERVAL_SECONDS}"
      run_job "$1" "$format" "$timeout_seconds" "$poll_interval_seconds" "$api_key" "$base_url"
      ;;
    *)
      print_usage
      exit 1
      ;;
  esac
}

main "$@"
