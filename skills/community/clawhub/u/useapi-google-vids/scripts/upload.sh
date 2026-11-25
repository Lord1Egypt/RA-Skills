#!/usr/bin/env bash
# Upload a local image (JPEG, PNG, WebP) or video (MP4), up to 50 MB, and print its assetId.
# Usage: upload.sh <file>
# The asset belongs to one Google account: USEAPI_EMAIL if set, otherwise the one the API assigns.
# Use the id as startImage or referenceImage_N (generate.sh), or as image or logo (avatar.sh).
# Uploads are temporary like every Google Vids file: upload shortly before the job that uses them.
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-assets
source "$(dirname "$0")/_common.sh"
FILE="${1:?Usage: upload.sh <file>}"
[ -f "$FILE" ] || { echo "No such file: $FILE" >&2; exit 1; }

EXT=$(tr '[:upper:]' '[:lower:]' <<< "${FILE##*.}")
case "$EXT" in
  png) TYPE=image/png ;;
  jpg|jpeg) TYPE=image/jpeg ;;
  webp) TYPE=image/webp ;;
  mp4) TYPE=video/mp4 ;;
  *) echo "Unsupported file type .$EXT (use png, jpg, jpeg, webp or mp4)" >&2; exit 1 ;;
esac

P="assets"
if [ -n "${USEAPI_EMAIL:-}" ]; then P="assets?email=$(enc "$USEAPI_EMAIL")"; fi
OUT=$(mktemp)
CODE=$(acurl -sS --max-time 320 -o "$OUT" -w '%{http_code}' -X POST -H "Content-Type: $TYPE" --data-binary "@$FILE" "$API/$P") || true
CODE="${CODE:-000}"
BODY=$(_finish POST "$P")
ID=$(jq -r '.assetId // empty' <<< "$BODY")
[ -n "$ID" ] || { echo "Upload answered without an assetId: $BODY" >&2; exit 1; }
log "uploaded $FILE to $(jq -r '.email // "?"' <<< "$BODY")"
echo "$ID"
