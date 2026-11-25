#!/usr/bin/env bash
# Turn a finished seedance-2.5-draft video into the same video in full quality, wait, download. Prints the saved .mp4 path.
# Usage: full-quality.sh <draft jobid> [1080p|4k]
#   1080p is the default. 4k works on Canada (CA) accounts only. The draft must be at most 14 days old.
#   The video keeps the draft's prompt, references, length and aspect ratio, and is made on the draft's account.
#   It costs the same as making the video with seedance-2.5 at that resolution.
# Docs: https://useapi.net/docs/api-dreamina-v1/post-dreamina-videos-full-quality
# This spends Dreamina credits. If the run is interrupted after the job id was logged, resume with
# wait-job.sh <jobid> > job.json && download.sh job.json (do not run full-quality.sh again).
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
DRAFT="${1:?Usage: full-quality.sh <draft jobid> [1080p|4k]}"
RES="${2:-1080p}"
case "$RES" in 1080p|4k) ;; *) echo "Resolution must be 1080p or 4k, got: $RES" >&2; exit 1 ;; esac

BODY=$(jq -n --arg j "$DRAFT" --arg r "$RES" '{jobid: $j, resolution: $r}')
JOB=$(api POST videos/full-quality "$BODY")
JOBID=$(jq -r '.jobid // empty' <<< "$JOB")
[ -n "$JOBID" ] || { echo "No job id in the answer: $JOB" >&2; exit 1; }
log "job $JOBID"
JOB=$("$DIR/wait-job.sh" "$JOBID")
"$DIR/download.sh" - "${OUT_DIR:-.}" <<< "$JOB"
