#!/usr/bin/env bash
# Upload a local image, video or audio file to a Dreamina account and print its assetRef.
# Usage: upload.sh <file> [account]
#   Images: jpg, jpeg, png, webp (up to 10 MB). Videos: mp4, mov, webm (up to 50 MB, 1.8 to 30.2 s).
#   Audio: mp3, wav, m4a, aac (up to 15 MB, 1.8 to 30.2 s).
# The account is the second argument, else USEAPI_EMAIL, else the first connected account.
# An assetRef works only on the account it was uploaded to. Use it as firstFrameRef, endFrameRef or
# omni_N_imageRef / omni_N_videoRef / omni_N_audioRef in generate.sh.
# Docs: https://useapi.net/docs/api-dreamina-v1/post-dreamina-assets-account
source "$(dirname "$0")/_common.sh"
FILE="${1:?Usage: upload.sh <file> [account]}"
[ -f "$FILE" ] || { echo "No such file: $FILE" >&2; exit 1; }

EXT=$(tr '[:upper:]' '[:lower:]' <<< "${FILE##*.}")
case "$EXT" in
  jpg|jpeg) TYPE=image/jpeg ;;
  png) TYPE=image/png ;;
  webp) TYPE=image/webp ;;
  mp4) TYPE=video/mp4 ;;
  mov) TYPE=video/quicktime ;;
  webm) TYPE=video/webm ;;
  mp3) TYPE=audio/mpeg ;;
  wav) TYPE=audio/wav ;;
  m4a) TYPE=audio/mp4 ;;
  aac) TYPE=audio/aac ;;
  *) echo "Unsupported file type .$EXT (use jpg, png, webp, mp4, mov, webm, mp3, wav, m4a or aac)" >&2; exit 1 ;;
esac

ACCOUNT="${2:-}"
if [ -z "$ACCOUNT" ]; then ACCOUNT=$(account_id); fi
P="assets/$(enc "$ACCOUNT")"
OUT=$(mktemp)
CODE=$(acurl -sS --max-time 300 -o "$OUT" -w '%{http_code}' -X POST -H "Content-Type: $TYPE" --data-binary "@$FILE" "$API/$P") || true
CODE="${CODE:-000}"
BODY=$(_finish POST "$P")
REF=$(jq -r '.assetRef // empty' <<< "$BODY")
[ -n "$REF" ] || { echo "Upload answered without an assetRef: $BODY" >&2; exit 1; }
log "uploaded $FILE to $ACCOUNT"
echo "$REF"
