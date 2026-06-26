#!/usr/bin/env bash
# run.sh — wrapper to call runpod-media scripts without knowing the install path
# Usage: run.sh <generate_image|edit_image|image_to_video|text_to_video> [args...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 1 ]]; then
  echo "Usage: run.sh <command> [args...]"
  echo "Commands: generate_image, edit_image, image_to_video, text_to_video, call_endpoint, list_endpoints"
  exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
  generate_image|edit_image|image_to_video|text_to_video|call_endpoint|discover_endpoints)
    exec uv run "$SCRIPT_DIR/${COMMAND}.py" "$@"
    ;;
  list_endpoints)
    exec uv run "$SCRIPT_DIR/call_endpoint.py" --list
    ;;
  *)
    echo "Unknown command: $COMMAND"
    echo "Commands: generate_image, edit_image, image_to_video, text_to_video, call_endpoint, list_endpoints"
    exit 1
    ;;
esac
