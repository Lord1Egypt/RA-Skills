#!/usr/bin/env bash
# Split a song into four stems (drums, bass, vocals, other) with POST /music/edit operation=stems, then download them.
# Usage: stems.sh <clip id> [m4a|wav|mp3]
#   The clip id is logged by song.sh, or read it from a job record: jq -r '.clips[0].clip' job.json
# The split usually takes 15 to 60 seconds and runs on the account that holds the clip. If it is not done after
# 2 minutes the API answers 504 and keeps splitting, so this script asks again up to 3 times, 30 s apart:
# a clip that is already split answers with its stems at once. Stems spend credits from the same plan.
# Prints the saved paths. OUT_DIR sets the folder (default: the current one).
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
CLIP="${1:?Usage: stems.sh <clip id> [m4a|wav|mp3]}"
FORMAT="${2:-m4a}"
case "$FORMAT" in m4a|wav|mp3) ;; *) echo "Format must be m4a, wav or mp3" >&2; exit 1 ;; esac

BODY=$(jq -n --arg c "$CLIP" '{operation: "stems", clip: $c}')
TRY=1
while true; do
  _call POST music/edit "$BODY"
  if [ "$CODE" = 504 ] && [ "$TRY" -le 3 ]; then
    log "the split is still running, asking again in 30 s ($TRY of 3)"
    rm -f "$OUT"
    TRY=$((TRY + 1))
    sleep 30
    continue
  fi
  break
done
RESULT=$(_finish POST music/edit)
jq -r '.clips[]? | "\(.stem_type // "-"): \(.duration_s // "?") s"' <<< "$RESULT" >&2
bash "$DIR/download.sh" - "${OUT_DIR:-.}" "$FORMAT" <<< "$RESULT"
