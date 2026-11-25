#!/usr/bin/env bash
# Start one song (POST /music, async) and print its job id. It does not wait. Use wait-job.sh for that.
# Usage: generate.sh "<prompt>" [key=value ...]
#   model=lyria-3.5 (this script's default) | lyria-3-pro (the API's default)
#   instrumental=true|false (true forces an instrumental, false lets the model decide from the prompt)
#   lyrics=<text or a local .txt file> ([Verse] / [Chorus] tagged, up to 10,000 characters, the song sings these words)
#   ghostwriter=standard|pro (the lyrics writer when the model writes the lyrics, no effect with your own lyrics)
# The prompt (1 to 10,000 characters) describes style, mood, genre, instruments, BPM and any vocal direction.
# Every option: https://useapi.net/docs/api-flowmusic-v1/post-flowmusic-music
# This spends Google Flow Music credits. It never retries by itself: a retry after an unclear failure could pay twice.
source "$(dirname "$0")/_common.sh"
PROMPT="${1:?Usage: generate.sh \"<prompt>\" [key=value ...]}"
shift

BODY=$(jq -n --arg p "$PROMPT" '{prompt: $p, model: "lyria-3.5", mode: "async"}')
if [ -n "${USEAPI_EMAIL:-}" ]; then BODY=$(jq --arg e "$USEAPI_EMAIL" '.email = $e' <<< "$BODY"); fi
for KV in "$@"; do
  case "$KV" in *=*) ;; *) echo "Expected key=value, got: $KV" >&2; exit 1 ;; esac
  K="${KV%%=*}"
  V="${KV#*=}"
  case "$K" in
    instrumental)
      case "$V" in true|false) ;; *) echo "instrumental must be true or false" >&2; exit 1 ;; esac
      BODY=$(jq --argjson v "$V" '.instrumental = $v' <<< "$BODY") ;;
    lyrics)
      if [ -f "$V" ]; then V=$(cat "$V"); fi
      BODY=$(jq --arg v "$V" '.lyrics = $v' <<< "$BODY") ;;
    model|ghostwriter|email)
      BODY=$(jq --arg k "$K" --arg v "$V" '.[$k] = $v' <<< "$BODY") ;;
    *) echo "Unknown option $K (use model, instrumental, lyrics or ghostwriter)" >&2; exit 1 ;;
  esac
done

JOB=$(api POST music "$BODY")
ID=$(jq -r '.jobid // empty' <<< "$JOB")
[ -n "$ID" ] || { echo "No job id in the answer: $JOB" >&2; exit 1; }
log "job $ID"
echo "$ID"
