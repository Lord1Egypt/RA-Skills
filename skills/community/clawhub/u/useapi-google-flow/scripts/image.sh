#!/usr/bin/env bash
# Generate Nano Banana images with POST /images and save them. Prints the saved image paths.
# Usage: image.sh "<prompt>" [key=value ...]
#   model=nano-banana-2-lite (API default) | nano-banana-2 (Nano Banana 2.1) | nano-banana-pro
#   aspectRatio=16:9 | 4:3 | 1:1 | 3:4 | 9:16 | auto (auto needs at least one reference_N)
#   count=1..4 (this script sends 1 unless you pass count; the API's own default is 4)  seed=<int>
#   reference_1..10=<asset id or local image file>  character_1..7=<character id>
# Values that are existing local files (reference_N) are uploaded first with upload.sh.
# The call is synchronous and usually takes 10 to 20 seconds. OUT_DIR sets the folder (default: the current one).
# Every option: https://useapi.net/docs/api-google-flow-v1/post-google-flow-images
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: image.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p, count: 1}')
for KV in "$@"; do
  case "$KV" in *=*) ;; *) echo "Expected key=value, got: $KV" >&2; exit 1 ;; esac
  K="${KV%%=*}"
  V="${KV#*=}"
  if [ -f "$V" ]; then
    V=$("$DIR/upload.sh" "$V")
    # Keep every upload on the same Google account as the first one
    if [ -z "${USEAPI_EMAIL:-}" ]; then
      USEAPI_EMAIL=$(asset_email "$V")
      export USEAPI_EMAIL
    fi
  fi
  case "$K" in
    count|seed) BODY=$(jq --arg k "$K" --argjson v "$V" '.[$k] = $v' <<< "$BODY") ;;
    *) BODY=$(jq --arg k "$K" --arg v "$V" '.[$k] = $v' <<< "$BODY") ;;
  esac
done
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi

RESULT=$(api POST images "$BODY")
OUT="${OUT_DIR:-.}"
mkdir -p "$OUT"
STAMP=$(date +%Y%m%d-%H%M%S)
N=0
# fifeUrl is normally present (a signed link valid for about 6 hours). When it is absent the image
# arrived inline as base64 in encodedImage, so decode that instead.
while IFS=$'\t' read -r KIND VALUE; do
  N=$((N + 1))
  FILE="$OUT/nano-banana_${STAMP}_$N.jpg"
  if [ "$KIND" = url ]; then
    curl -sS --fail --max-time 300 -o "$FILE" "$VALUE"
  else
    printf '%s' "$VALUE" | base64 -d > "$FILE"
  fi
  echo "$FILE"
done < <(jq -r '.media[]?.image.generatedImage | if .fifeUrl then "url\t\(.fifeUrl)" else "b64\t\(.encodedImage // "")" end' <<< "$RESULT")
[ "$N" -gt 0 ] || { echo "The answer has no images: $(jq -c '{jobId, error}' <<< "$RESULT")" >&2; exit 1; }
log "saved $N image(s)"
