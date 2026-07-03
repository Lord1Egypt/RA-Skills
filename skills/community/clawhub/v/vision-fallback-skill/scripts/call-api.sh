#!/usr/bin/env bash
# Call the Volcengine Ark (doubao) vision fallback API.
#
# Usage:
#   ./call-api.sh <image> [ocr_text] [failure_reason] [primary_model_output]
#
# <image> may be a local file path, an http(s):// URL, or a data: URL.
# Prints the raw API JSON response to stdout.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# shellcheck source=resolve-key.sh
. "$SCRIPT_DIR/resolve-key.sh"

IMAGE="${1:?missing <image> arg}"
OCR_TEXT="${2:-}"
FAILURE_REASON="${3:-}"
PRIMARY_OUTPUT="${4:-}"

# --- Build the image URL ---
if [[ "$IMAGE" =~ ^https?:// ]] || [[ "$IMAGE" =~ ^data: ]]; then
  IMAGE_URL="$IMAGE"
else
  [ -f "$IMAGE" ] || { echo "ERROR: image file not found: $IMAGE" >&2; exit 1; }
  MIME="$(file -b --mime-type "$IMAGE")"
  # Portable base64: GNU wraps at 76 cols, macOS does not wrap. Strip all
  # newlines so the data URL is a single line regardless of platform.
  B64="$(base64 "$IMAGE" | tr -d '\n')"
  IMAGE_URL="data:${MIME};base64,${B64}"
fi

# --- Build JSON payload via a template + jq substitution ---
PAYLOAD_TEMPLATE="$SCRIPT_DIR/../assets/payload-template.json"
[ -f "$PAYLOAD_TEMPLATE" ] || { echo "ERROR: payload template missing" >&2; exit 1; }

PAYLOAD="$(jq -n \
  --arg image_url "$IMAGE_URL" \
  --arg ocr "$OCR_TEXT" \
  --arg fr "$FAILURE_REASON" \
  --arg pm "$PRIMARY_OUTPUT" \
  --rawfile tpl "$PAYLOAD_TEMPLATE" \
  '($tpl
    | gsub("\\{\\{IMAGE_URL\\}\\}"; $image_url)
    | gsub("\\{\\{ocr_text\\}\\}"; $ocr)
    | gsub("\\{\\{failure_reason\\}\\}"; $fr)
    | gsub("\\{\\{primary_model_output\\}\\}"; $pm)
  ) | fromjson')"

# --- POST ---
curl -sS https://ark.cn-beijing.volces.com/api/plan/v3/chat/completions \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
