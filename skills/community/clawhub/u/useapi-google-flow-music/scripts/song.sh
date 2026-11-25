#!/usr/bin/env bash
# Everything in one command: start a song, wait for it, download it. Prints the saved audio paths.
# Usage: song.sh "<prompt>" [key=value ...]
#   format=m4a (default) | wav | mp3, plus every option of generate.sh (model, instrumental, lyrics, ghostwriter).
# Example: song.sh "warm indie folk ballad, acoustic guitar, soft female vocals, 70 bpm, wistful and hopeful"
#          song.sh "energetic synthwave, driving bass, retro 80s, 120 bpm" instrumental=true format=wav
#          song.sh "soulful R&B, lush keys, 90 bpm" lyrics=./lyrics.txt
# One request gives one or two songs (an A/B pair). Each clip's title, length and clip id are logged on stderr
# (the clip id is what stems.sh takes). OUT_DIR sets the folder (default: the current one).
# If the run is interrupted after the job id was logged, resume with: wait-job.sh <jobid> > job.json && download.sh job.json
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
PROMPT="${1:?Usage: song.sh \"<prompt>\" [key=value ...]}"
shift

FORMAT=m4a
ARGS=()
for KV in "$@"; do
  case "$KV" in
    format=*) FORMAT="${KV#format=}" ;;
    *) ARGS+=("$KV") ;;
  esac
done
case "$FORMAT" in m4a|wav|mp3) ;; *) echo "format must be m4a, wav or mp3" >&2; exit 1 ;; esac

JOBID=$(bash "$DIR/generate.sh" "$PROMPT" ${ARGS[@]+"${ARGS[@]}"})
JOB=$(bash "$DIR/wait-job.sh" "$JOBID")
jq -r '.clips[]? | "\"\(.title // "untitled")\", \(.duration_s // "?") s, clip id \(.clip)"' <<< "$JOB" >&2
bash "$DIR/download.sh" - "${OUT_DIR:-.}" "$FORMAT" <<< "$JOB"
