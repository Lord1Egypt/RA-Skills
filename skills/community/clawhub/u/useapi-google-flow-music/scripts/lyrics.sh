#!/usr/bin/env bash
# Write song lyrics (POST /music/lyrics), no audio. Prints the [Verse] / [Chorus] tagged lyrics on stdout,
# and the title and a matching style prompt (sound_prompt) on stderr.
# Usage: lyrics.sh "<song idea>" [structure="Verse 1 / Chorus / Verse 2 / Chorus / Bridge / Outro"]
#   The idea is 1 to 2,000 characters, structure up to 2,000.
# Then sing them: lyrics.sh "..." > lyrics.txt && song.sh "<the sound_prompt or your own style>" lyrics=./lyrics.txt
# It renders no song but still uses a very small amount of Google Flow Music credit.
# Every option: https://useapi.net/docs/api-flowmusic-v1/post-flowmusic-music-lyrics
source "$(dirname "$0")/_common.sh"
PROMPT="${1:?Usage: lyrics.sh \"<song idea>\" [structure=\"...\"]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p}')
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
for KV in "$@"; do
  case "$KV" in
    structure=*) BODY=$(jq --arg v "${KV#structure=}" '.structure = $v' <<< "$BODY") ;;
    *) echo "Unknown option: $KV (only structure=...)" >&2; exit 1 ;;
  esac
done

RESULT=$(api POST music/lyrics "$BODY")
jq -r '"title: \(.title // "-")\nsound_prompt: \(.sound_prompt // "-")"' <<< "$RESULT" >&2
jq -r '.lyrics // empty' <<< "$RESULT"
