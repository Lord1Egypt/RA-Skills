#!/usr/bin/env bash
# Start an Audio Overview (podcast), a Video Overview or a slide deck on a notebook and print the job id.
# Usage: generate.sh <notebook> audio|video|slides [key=value ...]
#   audio: format=deep_dive|brief|critique|debate  length=short|default|long  language=en|es|pt_BR|...  instructions="..."
#   video: format=explainer|brief|cinematic|short  style=auto|classic|whiteboard|anime|...  language=...  instructions="..."
#          style applies to explainer and brief only; cinematic takes no style, language or instructions
#   slides: format=detailed|presenter  length=short|default|long  language=...  instructions="..."
# Other Studio types (report, quiz, flashcards, infographic, mindmap ...) work too:
# https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-artifacts
# The job runs on Google for minutes; poll it with wait-job.sh. The job id is also logged on stderr.
source "$(dirname "$0")/_common.sh"
NOTEBOOK="${1:?Usage: generate.sh <notebook> audio|video|slides [key=value ...]}"
TYPE="${2:?Usage: generate.sh <notebook> audio|video|slides [key=value ...]}"
shift 2

BODY=$(jq -n --arg nb "$NOTEBOOK" --arg type "$TYPE" '{notebook: $nb, type: $type, mode: "async"}')
for kv in "$@"; do
  BODY=$(jq --arg k "${kv%%=*}" --arg v "${kv#*=}" '.[$k] = $v' <<< "$BODY")
done
JOBID=$(api POST artifacts "$BODY" | jq -r .jobid)
log "job $JOBID"
log "if this run is interrupted, do not generate again; resume with: $(dirname "$0")/wait-job.sh '$JOBID' > job.json && $(dirname "$0")/download.sh job.json"
echo "$JOBID"
