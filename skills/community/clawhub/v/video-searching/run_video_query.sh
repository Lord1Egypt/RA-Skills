#!/usr/bin/env bash
# Video Searching API runner — calls Memories.ai SSE endpoint and emits NDJSON
set -euo pipefail

API_URL="https://mavi-backend.memories.ai/serve/api/v2/queries/stream"

# ── defaults ──
QUERY=""
MAX_RESULTS=10
MAX_STEPS=10
PLATFORMS=""
TIME_FRAME=""
ENABLE_CLARIFICATION="false"

# ── parse args ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)                QUERY="$2";                  shift 2;;
    --max-results)          MAX_RESULTS="$2";            shift 2;;
    --max-steps)            MAX_STEPS="$2";              shift 2;;
    --platforms)            PLATFORMS="$2";               shift 2;;
    --time-frame)           TIME_FRAME="$2";             shift 2;;
    --enable-clarification) ENABLE_CLARIFICATION="true"; shift;;
    *)                      shift;;                      # ignore unknown flags
  esac
done

# ── validate ──
if [[ -z "$QUERY" ]]; then
  echo '{"event":"error","data":{"message":"--query is required"}}'
  exit 1
fi

if [[ -z "${MEMORIES_API_KEY:-}" ]]; then
  echo '{"event":"error","data":{"message":"MEMORIES_API_KEY environment variable is not set. Get your key at https://api-tools.memories.ai"}}'
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo '{"event":"error","data":{"message":"curl is required but not found on PATH"}}'
  exit 2
fi

if ! command -v jq >/dev/null 2>&1; then
  echo '{"event":"error","data":{"message":"jq is required but not found on PATH"}}'
  exit 2
fi

# ── build JSON body ──
BODY=$(jq -n \
  --arg query "$QUERY" \
  --argjson max_results "$MAX_RESULTS" \
  --argjson max_steps "$MAX_STEPS" \
  --argjson enable_clarification "$ENABLE_CLARIFICATION" \
  '{query: $query, max_results: $max_results, max_steps: $max_steps, enable_clarification: $enable_clarification}')

# add optional platforms array (comma-separated → JSON array)
if [[ -n "$PLATFORMS" ]]; then
  PLATFORMS_JSON=$(echo "$PLATFORMS" | tr ',' '\n' | jq -R . | jq -s .)
  BODY=$(echo "$BODY" | jq --argjson p "$PLATFORMS_JSON" '. + {platforms: $p}')
fi

# add optional time_frame
if [[ -n "$TIME_FRAME" ]]; then
  BODY=$(echo "$BODY" | jq --arg tf "$TIME_FRAME" '. + {time_frame: $tf}')
fi

# ── call SSE endpoint, convert to NDJSON ──
EVENT_TYPE=""
HTTP_CODE_FILE=$(mktemp)

{
  curl -sS -N -w "%{http_code}" \
    -H "Content-Type: application/json" \
    -H "Authorization: ${MEMORIES_API_KEY}" \
    -d "$BODY" \
    "$API_URL" 2>/dev/null || true
} | {
  while IFS= read -r line; do
    # strip carriage return
    line="${line%$'\r'}"

    # capture HTTP status code (last line from -w)
    if [[ "$line" =~ ^[0-9]{3}$ ]]; then
      echo "$line" > "$HTTP_CODE_FILE"
      continue
    fi

    # parse SSE
    if [[ "$line" == event:* ]]; then
      EVENT_TYPE="${line#event:}"
      EVENT_TYPE="${EVENT_TYPE# }"  # trim leading space
    elif [[ "$line" == data:* ]]; then
      DATA="${line#data:}"
      DATA="${DATA# }"  # trim leading space
      if [[ -n "$EVENT_TYPE" && -n "$DATA" ]]; then
        # validate JSON before emitting
        if echo "$DATA" | jq empty 2>/dev/null; then
          echo "{\"event\":\"${EVENT_TYPE}\",\"data\":${DATA}}"
        fi
      fi
    fi
  done
}

# ── check for HTTP errors ──
if [[ -f "$HTTP_CODE_FILE" ]]; then
  HTTP_CODE=$(cat "$HTTP_CODE_FILE")
  rm -f "$HTTP_CODE_FILE"
  if [[ "$HTTP_CODE" =~ ^[45] ]]; then
    echo "{\"event\":\"error\",\"data\":{\"message\":\"API returned HTTP ${HTTP_CODE}\"}}"
    exit 1
  fi
else
  rm -f "$HTTP_CODE_FILE" 2>/dev/null || true
fi
