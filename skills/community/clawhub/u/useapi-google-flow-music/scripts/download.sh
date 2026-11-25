#!/usr/bin/env bash
# Download every clip of a finished song job or stem split and print the saved paths.
# Usage: download.sh <job.json|-> [OUT_DIR] [m4a|wav|mp3]
#   m4a (default) and wav come from the clip's own audio_url / wav_url links, which the API returns.
#   mp3 is served by the API itself (GET /music/download) with the same token.
# Files are named after the song title (letters and digits in any script) plus a short clip id.
source "$(dirname "$0")/_common.sh"
JOB=$(cat "${1:--}")
DEST="${2:-${OUT_DIR:-.}}"
FORMAT="${3:-m4a}"
case "$FORMAT" in m4a|wav|mp3) ;; *) echo "Format must be m4a, wav or mp3" >&2; exit 1 ;; esac
mkdir -p "$DEST"

N=0
while IFS=$'\t' read -r NAME CLIP URL; do
  FILE="$DEST/$NAME.$FORMAT"
  if [ "$FORMAT" = mp3 ]; then
    P="music/download?id=$(enc "$CLIP")&format=mp3"
    OUT="$FILE"
    CODE=$(acurl -sS --max-time 600 -o "$OUT" -w '%{http_code}' "$API/$P") || true
    CODE="${CODE:-000}"
    # an error answer is JSON: print it with a hint and stop (the file is removed)
    if [ "${CODE:0:1}" != "2" ]; then _finish GET "$P"; fi
  else
    case "$URL" in https://*) ;; *) echo "Clip $CLIP has no $FORMAT link, skipped" >&2; continue ;; esac
    curl -sS --fail --max-time 600 -o "$FILE" "$URL"
  fi
  N=$((N + 1))
  echo "$FILE"
done < <(jq -r --arg f "$FORMAT" '
  .clips[]?
  | ((.title // "") | gsub("[^\\p{L}\\p{M}\\p{N}_-]+"; "_") | .[:60] | sub("^_+"; "") | sub("_+$"; "")) as $t
  | ((.clip // "") | (capture("clip:(?<id>[0-9a-f]{8})").id // "")) as $id
  | ((if $t == "" then "google-flow-music" else $t end) + (if $id == "" then "" else "_" + $id end)) as $name
  | (if $f == "wav" then .wav_url elif $f == "m4a" then .audio_url else "-" end // "-") as $url
  | "\($name)\t\(.clip // "-")\t\($url)"' <<< "$JOB")
[ "$N" -gt 0 ] || { echo "Nothing saved, the record has no clips with a $FORMAT link: $(jq -c '{status, error}' <<< "$JOB")" >&2; exit 1; }
