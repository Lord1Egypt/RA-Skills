#!/usr/bin/env bash
set -euo pipefail

# editor.sh — Video editing operations via BlitzReels API.
# Wraps common timeline, transcription, caption, and export workflows.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BLITZREELS_SH="${SCRIPT_DIR}/blitzreels.sh"

BASE_URL="${BLITZREELS_API_BASE_URL:-https://www.blitzreels.com/api/v1}"
API_KEY="${BLITZREELS_API_KEY:-}"

usage() {
  cat <<'EOF'
Usage: editor.sh COMMAND [ARGS]

Commands:
  upload-url    <projectId> <url> [name]                Upload media from URL
  transcribe    <projectId> <mediaId>                   Transcribe media (polls until done)
  context       <projectId> [mode]                      Get project context (default: timeline)
  timeline-at   <projectId> <seconds>                   Get timeline items at timestamp
  trim          <projectId> <itemId> <startDelta> <endDelta>  Trim timeline item
  split         <projectId> <itemId> <atSeconds>        Split timeline item at time
  delete-item   <projectId> <itemId>                    Delete timeline item
  add-media     <projectId> <mediaId> [startSec]        Add media to timeline
  add-broll     <projectId> <JSON>                      Add B-roll from JSON body
  captions      <projectId> <presetId>                  Apply caption style preset
  words         <projectId> [limit] [offset]            List caption words
  transcript-corrections <projectId> <assetId> <JSON>   Apply single-word transcript replacements
  list-assets   [limit] [offset] [assetType]            List workspace media assets
  get-asset     <assetId>                               Get workspace media asset details
  workspace-settings [JSON_PATCH]                       Get or patch workspace settings
  export        <projectId> [--resolution R]            Export project (polls until done)

Arguments:
  <projectId>   BlitzReels project ID
  <mediaId>     Media asset ID
  <itemId>      Timeline item ID
  mode          Context mode: summary|assets|timeline|transcript|full (default: timeline)

Environment:
  BLITZREELS_API_KEY          Required. API key for authentication.
  BLITZREELS_API_BASE_URL     Optional. Override base URL.
  BLITZREELS_ALLOW_EXPENSIVE  Set to 1 to allow export calls.

Examples:
  editor.sh upload-url proj_abc https://example.com/video.mp4 "My Video"
  editor.sh transcribe proj_abc media_xyz
  editor.sh context proj_abc timeline
  editor.sh trim proj_abc item_123 0.5 -1.2
  editor.sh split proj_abc item_123 15.5
  editor.sh captions proj_abc viral-center
  editor.sh export proj_abc --resolution 1080p
EOF
  exit 0
}

poll_job() {
  local JOB_ID="$1"
  local LABEL="${2:-Job}"
  local MAX_POLLS=120
  local POLL_INTERVAL=5

  for i in $(seq 1 $MAX_POLLS); do
    STATUS_JSON=$(bash "$BLITZREELS_SH" GET "/jobs/${JOB_ID}")
    STATUS=$(echo "$STATUS_JSON" | jq -r '.status')

    case "$STATUS" in
      complete|completed|done|success)
        echo "  ${LABEL} complete!"
        echo "$STATUS_JSON"
        return 0
        ;;
      failed|error)
        echo "Error: ${LABEL} failed." >&2
        echo "$STATUS_JSON" | jq . >&2
        return 1
        ;;
      *)
        PROGRESS=$(echo "$STATUS_JSON" | jq -r '.progress // "unknown"')
        printf "\r  Status: %-12s Progress: %-6s (poll %d/%d)" "$STATUS" "$PROGRESS" "$i" "$MAX_POLLS"
        sleep "$POLL_INTERVAL"
        ;;
    esac
  done
  echo ""
  echo "Error: Timed out waiting for ${LABEL} (${MAX_POLLS} × ${POLL_INTERVAL}s)." >&2
  return 1
}

if [[ $# -lt 1 ]]; then
  usage
fi

COMMAND="$1"
shift

case "$COMMAND" in
  upload-url)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh upload-url <projectId> <url> [name]" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    URL="$2"
    NAME="${3:-}"
    BODY="{\"url\":$(echo "$URL" | jq -Rs .)}"
    if [[ -n "$NAME" ]]; then
      BODY="{\"url\":$(echo "$URL" | jq -Rs .),\"name\":$(echo "$NAME" | jq -Rs .)}"
    fi
    bash "$BLITZREELS_SH" POST "/projects/${PROJECT_ID}/media" "$BODY"
    ;;

  transcribe)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh transcribe <projectId> <mediaId>" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    MEDIA_ID="$2"
    echo "→ Starting transcription..."
    RESULT=$(bash "$BLITZREELS_SH" POST "/projects/${PROJECT_ID}/transcribe" \
      "{\"media_id\":\"${MEDIA_ID}\"}")
    JOB_ID=$(echo "$RESULT" | jq -r '.job_id // .jobId // .id')
    if [[ -z "$JOB_ID" || "$JOB_ID" == "null" ]]; then
      echo "Error: Failed to start transcription." >&2
      echo "$RESULT" >&2
      exit 1
    fi
    echo "  Job ID: ${JOB_ID}"
    poll_job "$JOB_ID" "Transcription"
    ;;

  context)
    if [[ $# -lt 1 ]]; then
      echo "Usage: editor.sh context <projectId> [mode]" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    MODE="${2:-timeline}"
    bash "$BLITZREELS_SH" GET "/projects/${PROJECT_ID}/context?mode=${MODE}"
    ;;

  timeline-at)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh timeline-at <projectId> <seconds>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" GET "/projects/$1/timeline/at?time_seconds=$2"
    ;;

  trim)
    if [[ $# -lt 4 ]]; then
      echo "Usage: editor.sh trim <projectId> <itemId> <startDelta> <endDelta>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" POST "/projects/$1/timeline/trim" \
      "{\"timeline_item_id\":\"$2\",\"trim_start_delta_seconds\":$3,\"trim_end_delta_seconds\":$4}"
    ;;

  split)
    if [[ $# -lt 3 ]]; then
      echo "Usage: editor.sh split <projectId> <itemId> <atSeconds>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" POST "/projects/$1/timeline/split" \
      "{\"timeline_item_id\":\"$2\",\"split_at_seconds\":$3}"
    ;;

  delete-item)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh delete-item <projectId> <itemId>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" DELETE "/projects/$1/timeline/items/$2"
    ;;

  add-media)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh add-media <projectId> <mediaId> [startSec]" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    MEDIA_ID="$2"
    START="${3:-0}"
    bash "$BLITZREELS_SH" POST "/projects/${PROJECT_ID}/timeline/media" \
      "{\"items\":[{\"asset_id\":\"${MEDIA_ID}\",\"start_seconds\":${START}}]}"
    ;;

  add-broll)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh add-broll <projectId> <JSON>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" POST "/projects/$1/broll" "$2"
    ;;

  captions)
    if [[ $# -lt 2 ]]; then
      echo "Usage: editor.sh captions <projectId> <presetId>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" POST "/projects/$1/captions" \
      "{\"style_id\":\"$2\"}"
    ;;

  words)
    if [[ $# -lt 1 ]]; then
      echo "Usage: editor.sh words <projectId> [limit] [offset]" >&2
      exit 1
    fi
    LIMIT="${2:-100}"
    OFFSET="${3:-0}"
    bash "$BLITZREELS_SH" GET "/projects/$1/captions/words?limit=${LIMIT}&offset=${OFFSET}"
    ;;

  transcript-corrections)
    if [[ $# -lt 3 ]]; then
      echo "Usage: editor.sh transcript-corrections <projectId> <assetId> <JSON>" >&2
      echo "JSON example: '{\"replacements\":[{\"from\":\"Cloud\",\"to\":\"Claude\"}]}'" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    ASSET_ID="$2"
    PATCH_JSON="$3"
    BODY=$(echo "$PATCH_JSON" | jq --arg media_asset_id "$ASSET_ID" '. + {media_asset_id: $media_asset_id}')
    bash "$BLITZREELS_SH" POST "/projects/${PROJECT_ID}/transcript/corrections" "$BODY"
    ;;

  list-assets)
    LIMIT="${1:-50}"
    OFFSET="${2:-0}"
    ASSET_TYPE="${3:-all}"
    bash "$BLITZREELS_SH" GET "/workspace/media/assets?limit=${LIMIT}&offset=${OFFSET}&asset_type=${ASSET_TYPE}"
    ;;

  get-asset)
    if [[ $# -lt 1 ]]; then
      echo "Usage: editor.sh get-asset <assetId>" >&2
      exit 1
    fi
    bash "$BLITZREELS_SH" GET "/workspace/media/assets/$1"
    ;;

  workspace-settings)
    if [[ $# -lt 1 ]]; then
      bash "$BLITZREELS_SH" GET "/workspace/settings"
    else
      bash "$BLITZREELS_SH" PATCH "/workspace/settings" "$1"
    fi
    ;;

  export)
    if [[ $# -lt 1 ]]; then
      echo "Usage: editor.sh export <projectId> [--resolution R]" >&2
      exit 1
    fi
    PROJECT_ID="$1"
    shift
    RESOLUTION="1080p"
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --resolution) RESOLUTION="$2"; shift 2 ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
      esac
    done

    export BLITZREELS_ALLOW_EXPENSIVE=1
    echo "→ Starting export (${RESOLUTION})..."
    EXPORT_JSON=$(bash "$BLITZREELS_SH" POST "/projects/${PROJECT_ID}/export" \
      "{\"resolution\":\"${RESOLUTION}\"}")
    EXPORT_ID=$(echo "$EXPORT_JSON" | jq -r '.export_id // .exportId // .id')
    if [[ -z "$EXPORT_ID" || "$EXPORT_ID" == "null" ]]; then
      echo "Error: Failed to start export." >&2
      echo "$EXPORT_JSON" >&2
      exit 1
    fi
    echo "  Export ID: ${EXPORT_ID}"

    # Poll export status
    for i in $(seq 1 60); do
      EXPORT_STATUS_JSON=$(bash "$BLITZREELS_SH" GET "/exports/${EXPORT_ID}")
      EXPORT_STATUS=$(echo "$EXPORT_STATUS_JSON" | jq -r '.status')

      case "$EXPORT_STATUS" in
        complete|completed|done|success)
          DOWNLOAD_URL=$(echo "$EXPORT_STATUS_JSON" | jq -r '.download_url // .downloadUrl // .url')
          echo "  Export complete!"
          echo "  Download: ${DOWNLOAD_URL}"
          echo "$EXPORT_STATUS_JSON"
          exit 0
          ;;
        failed|error)
          echo "Error: Export failed." >&2
          echo "$EXPORT_STATUS_JSON" | jq . >&2
          exit 1
          ;;
        *)
          printf "\r  Export status: %-12s (poll %d/60)" "$EXPORT_STATUS" "$i"
          sleep 5
          ;;
      esac
    done
    echo ""
    echo "Error: Timed out waiting for export." >&2
    exit 1
    ;;

  --help|-h|help)
    usage
    ;;

  *)
    echo "Unknown command: $COMMAND" >&2
    echo "Run 'editor.sh --help' for usage." >&2
    exit 1
    ;;
esac
