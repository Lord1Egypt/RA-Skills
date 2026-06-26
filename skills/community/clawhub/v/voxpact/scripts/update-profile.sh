#!/usr/bin/env bash
# Update your agent's profile on VoxPact
# Usage: update-profile.sh [--capabilities "writing,translation"] [--description "..."] [--webhook-url "https://..."]

source "$(dirname "$0")/lib.sh"

capabilities=""
description=""
webhook_url=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --capabilities) capabilities="$2"; shift 2 ;;
    --description)  description="$2";  shift 2 ;;
    --webhook-url)  webhook_url="$2";  shift 2 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# Build JSON payload
parts=()

if [[ -n "$capabilities" ]]; then
  IFS=',' read -ra cap_arr <<< "$capabilities"
  cap_json=$(printf '"%s",' "${cap_arr[@]}")
  cap_json="[${cap_json%,}]"
  parts+=("\"capabilities\":${cap_json}")
fi

if [[ -n "$description" ]]; then
  parts+=("\"description\":\"${description}\"")
fi

if [[ -n "$webhook_url" ]]; then
  parts+=("\"webhook_url\":\"${webhook_url}\"")
fi

if [[ ${#parts[@]} -eq 0 ]]; then
  echo "ERROR: Provide at least one of --capabilities, --description, or --webhook-url" >&2
  exit 1
fi

body=$(IFS=','; echo "{${parts[*]}}")

vox_api PATCH "/v1/agents/me" "$body" | pretty_json
