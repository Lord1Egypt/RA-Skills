#!/usr/bin/env bash
# One command: links and/or local files -> a new notebook -> one Studio output, downloaded.
# Usage: studio.sh audio|video|slides "<title>" URL|FILE [URL|FILE ...] [-- key=value ...]
# Example: studio.sh slides "Apollo 11" https://en.wikipedia.org/wiki/Apollo_11 ./notes.pdf -- format=presenter length=short
# Arguments that are existing local files are uploaded; everything else is added as a URL.
# Prints progress on stderr and the saved file paths on stdout (OUT_DIR sets the folder).
DIR="$(dirname "$0")"
source "$DIR/_common.sh"
TYPE="${1:?Usage: studio.sh audio|video|slides \"<title>\" URL|FILE ... [-- key=value ...]}"
TITLE="${2:?Usage: studio.sh audio|video|slides \"<title>\" URL|FILE ... [-- key=value ...]}"
shift 2
URLS=() FILES=() OPTS=()
while [ $# -gt 0 ]; do
  if [ "$1" = "--" ]; then shift; OPTS=("$@"); break; fi
  if [ -f "$1" ]; then FILES+=("$1"); else URLS+=("$1"); fi
  shift
done
[ ${#URLS[@]} -gt 0 ] || [ ${#FILES[@]} -gt 0 ] || { echo "Give at least one URL or file" >&2; exit 1; }

NOTEBOOK=$(bash "$DIR/create-notebook.sh" "$TITLE")
log "notebook $NOTEBOOK"
if [ ${#URLS[@]} -gt 0 ]; then bash "$DIR/add-sources.sh" "$NOTEBOOK" "${URLS[@]}" >&2; fi
if [ ${#FILES[@]} -gt 0 ]; then
  for f in "${FILES[@]}"; do bash "$DIR/upload-file.sh" "$NOTEBOOK" "$f" >&2; done
fi
bash "$DIR/wait-sources.sh" "$NOTEBOOK" >&2
# generate.sh logs the job id (and how to resume with it) on stderr
JOBID=$(bash "$DIR/generate.sh" "$NOTEBOOK" "$TYPE" ${OPTS[@]+"${OPTS[@]}"})
JOB_FILE=$(mktemp)
trap 'rm -f "$JOB_FILE"' EXIT
bash "$DIR/wait-job.sh" "$JOBID" > "$JOB_FILE"
jq -r '"\"\(.result.title // "")\"" + (if .result.duration then ", \(.result.duration) s" else "" end)' "$JOB_FILE" >&2
bash "$DIR/download.sh" "$JOB_FILE" "${OUT_DIR:-.}"
