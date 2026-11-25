#!/usr/bin/env bash
# Create, list or delete Google Vids avatars (a person's picture plus a fixed voice).
# Usage:
#   avatar.sh <name> <voice> appearance="<the person>" [outfit=...] [shot=close-up|upper-body|full-body] [expression=...] [details=...]
#   avatar.sh <name> <voice> image=<photo file, assetId or image mediaId> [refine="<change in words>"] [logo=<file or id>]
#   avatar.sh <name> <voice> avatar=<avatarId> [refine=...] [logo=...]     (start from another avatar's picture)
#   avatar.sh --list            one JSON line per avatar: avatarId, name, voice, email
#   avatar.sh --delete <avatarId>
#   avatar.sh --voices          the 30 voices: name, voice id, style
# Give exactly one of appearance, image and avatar. Local files (image=, logo=) are uploaded first.
# Create prints the avatarId on stdout and saves the new picture to OUT_DIR as avatar_<name>.jpg (path on stderr).
# Each picture Google makes (a drawing, a reframed photo, a refine/logo change) uses 1 Google Vids image;
# an account with no image allowance (a free one) still makes avatars at no cost. Voices are free.
# Google refuses photos of prominent people and of minors (422). Only use a photo of someone who agreed to it.
# The voice is a Google Vids voice name (Holt) or a Google voice id (Charon), see --voices.
# Avatars stay in the account's Google Vids document until deleted; reuse them by avatarId with talk.sh or as
# avatar_1..3 in video.sh. USEAPI_EMAIL picks the account (for --list, only that account is read).
# Docs: https://useapi.net/docs/api-google-vids-v1/post-google-vids-avatars
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
USAGE='Usage: avatar.sh <name> <voice> appearance="..." | image=<file or id> | avatar=<avatarId> [refine=...] [logo=...]  |  --list  |  --delete <avatarId>  |  --voices'

case "${1:-}" in
  "") echo "$USAGE" >&2; exit 1 ;;
  --voices)
    api_poll GET voices | jq -r '.voices[] | "\(.name)\t\(.voice)\t\(.style)"'
    exit 0 ;;
  --list)
    P=avatars
    if [ -n "${USEAPI_EMAIL:-}" ]; then P="avatars?email=$(enc "$USEAPI_EMAIL")"; fi
    R=$(api_poll GET "$P")
    jq -c '.avatars[] | {avatarId, name, voice, voiceStyle, email}' <<< "$R"
    jq -r '.errors[]? | "Could not read \(.email): \(.error)"' <<< "$R" >&2
    exit 0 ;;
  --delete)
    ID="${2:?Usage: avatar.sh --delete <avatarId>}"
    api DELETE "avatars/$(enc "$ID")" > /dev/null
    log "deleted avatar"
    exit 0 ;;
esac

NAME="$1"
VOICE="${2:?$USAGE}"
shift 2

# An id input pins the account it lives on, so uploads go there too
for KV in "$@"; do
  case "$KV" in
    image=*|avatar=*|logo=*)
      V="${KV#*=}"
      if [ ! -f "$V" ] && [ -z "${USEAPI_EMAIL:-}" ]; then USEAPI_EMAIL=$(id_email "$V"); export USEAPI_EMAIL; fi ;;
  esac
done
[ -n "${USEAPI_EMAIL:-}" ] || unset USEAPI_EMAIL

BODY=$(jq -n --arg n "$NAME" --arg v "$VOICE" '{name: $n, voice: $v}')
for KV in "$@"; do
  case "$KV" in
    image=*|logo=*) file_or_id "${KV#*=}"; KV="${KV%%=*}=$FID" ;;
  esac
  BODY=$(add_kv "$BODY" "$KV")
done
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
jq -e '[has("appearance"), has("image"), has("avatar")] | map(select(.)) | length == 1' <<< "$BODY" > /dev/null \
  || { echo "Give exactly one of appearance=\"<the person>\", image=<file or id> or avatar=<avatarId>. $USAGE" >&2; exit 1; }

# Sent once: drawing the picture uses a Google Vids image, so it is never retried automatically
R=$(api POST avatars "$BODY")
ID=$(jq -r '.avatarId // empty' <<< "$R")
[ -n "$ID" ] || { echo "No avatarId in the answer: $R" >&2; exit 1; }
log "avatar $(jq -r '"\(.name), voice \(.voice) (\(.voiceId), \(.voiceStyle)), on \(.email)"' <<< "$R")"
PREVIEW=$(jq -r '.previewMediaId // empty' <<< "$R")
if [ -n "$PREVIEW" ]; then
  SAFE=$(printf '%s' "$NAME" | tr -c 'A-Za-z0-9_-' '_')
  if FILE=$(bash "$DIR/download.sh" "$PREVIEW" "${OUT_DIR:-.}" "avatar_$SAFE"); then log "picture saved to $FILE"; else log "could not download the picture (the avatar is fine)"; fi
fi
echo "$ID"
