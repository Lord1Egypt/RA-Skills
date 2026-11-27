#!/usr/bin/env bash
# Upload a local image to PixVerse and print its upload path, for first_frame_path in generate.sh.
# Usage: upload.sh <file> [email]
#   Images: jpg, jpeg, png, webp, gif. PixVerse does not take images over about 2K (2048 px on a side): downscale first.
# The account is the second argument, else USEAPI_EMAIL, else the first connected account.
# Docs: https://useapi.net/docs/api-pixverse-v2/post-pixverse-files
source "$(dirname "$0")/_common.sh"
FILE="${1:?Usage: upload.sh <file> [email]}"
[ -f "$FILE" ] || { echo "No such file: $FILE" >&2; exit 1; }

EXT=$(tr '[:upper:]' '[:lower:]' <<< "${FILE##*.}")
case "$EXT" in
  jpg|jpeg) TYPE=image/jpeg ;;
  png) TYPE=image/png ;;
  webp) TYPE=image/webp ;;
  gif) TYPE=image/gif ;;
  *) echo "Unsupported file type .$EXT (use jpg, png, webp or gif)" >&2; exit 1 ;;
esac

EMAIL="${2:-}"
if [ -z "$EMAIL" ]; then EMAIL=$(account_email); fi
P="files?email=$(enc "$EMAIL")"
OUT=$(mktemp)
CODE=$(acurl -sS --max-time 300 -o "$OUT" -w '%{http_code}' -X POST -H "Content-Type: $TYPE" --data-binary "@$FILE" "$API/$P") || true
CODE="${CODE:-000}"
BODY=$(_finish POST "$P")
REF=$(jq -r '.result[0].path // empty' <<< "$BODY")
[ -n "$REF" ] || { echo "Upload answered without a path: $BODY" >&2; exit 1; }
log "uploaded $FILE to $EMAIL"
echo "$REF"
