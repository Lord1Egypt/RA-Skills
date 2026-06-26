#!/usr/bin/env bash
# VoxPact skill — shared helpers
# Source this file at the top of every script (except setup.sh):
#   source "$(dirname "$0")/lib.sh"

set -euo pipefail

VOXPACT_API="${VOXPACT_API_URL:-https://api.voxpact.com}"
VOXPACT_API="${VOXPACT_API%/}"

vox_api() {
  # Usage: vox_api METHOD PATH [JSON_BODY]
  local method="$1" path="$2" body="${3:-}"

  if [[ -z "${VOXPACT_API_KEY:-}" ]]; then
    echo "ERROR: VOXPACT_API_KEY not set. Run scripts/setup.sh first." >&2
    exit 1
  fi

  local args=(-s -S -f -X "$method" \
    -H "Authorization: ApiKey $VOXPACT_API_KEY" \
    -H "Content-Type: application/json")

  if [[ -n "$body" ]]; then
    args+=(-d "$body")
  fi

  local http_code response
  response=$(curl "${args[@]}" -w "\n%{http_code}" "${VOXPACT_API}${path}") || {
    echo "ERROR: Request failed — $method ${path}" >&2
    echo "$response" >&2
    exit 1
  }

  http_code=$(echo "$response" | tail -1)
  body_out=$(echo "$response" | sed '$d')

  if [[ "$http_code" -ge 400 ]]; then
    echo "ERROR: HTTP $http_code — $body_out" >&2
    exit 1
  fi

  echo "$body_out"
}

vox_api_raw() {
  # Usage: vox_api_raw METHOD PATH CONTENT_TYPE FILE_PATH
  local method="$1" path="$2" content_type="$3" file_path="$4"

  if [[ -z "${VOXPACT_API_KEY:-}" ]]; then
    echo "ERROR: VOXPACT_API_KEY not set." >&2
    exit 1
  fi

  local response http_code
  response=$(curl -s -S -f -X "$method" \
    -H "Authorization: ApiKey $VOXPACT_API_KEY" \
    -H "Content-Type: $content_type" \
    --data-binary "@${file_path}" \
    -w "\n%{http_code}" \
    "${VOXPACT_API}${path}") || {
    echo "ERROR: Upload failed — $method ${path}" >&2
    echo "$response" >&2
    exit 1
  }

  http_code=$(echo "$response" | tail -1)
  body_out=$(echo "$response" | sed '$d')

  if [[ "$http_code" -ge 400 ]]; then
    echo "ERROR: HTTP $http_code — $body_out" >&2
    exit 1
  fi

  echo "$body_out"
}

get_content_type() {
  # Usage: get_content_type FILE_PATH
  local ext="${1##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  case "$ext" in
    txt|md)  echo "text/plain" ;;
    json)    echo "application/json" ;;
    pdf)     echo "application/pdf" ;;
    png)     echo "image/png" ;;
    jpg|jpeg) echo "image/jpeg" ;;
    csv)     echo "text/csv" ;;
    html)    echo "text/html" ;;
    docx)    echo "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
    *)       echo "application/octet-stream" ;;
  esac
}

pretty_json() {
  # Try python, then jq, then cat
  if command -v python3 &>/dev/null; then
    python3 -m json.tool 2>/dev/null || cat
  elif command -v jq &>/dev/null; then
    jq . 2>/dev/null || cat
  else
    cat
  fi
}
