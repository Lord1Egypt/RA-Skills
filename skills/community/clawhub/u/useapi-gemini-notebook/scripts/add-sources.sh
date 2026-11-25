#!/usr/bin/env bash
# Add web pages and YouTube videos (up to 50 per call) and/or pasted text to a notebook.
# Usage: add-sources.sh <notebook> [URL ...] [--text FILE|- [--title "<text title>"]]
# YouTube links become YouTube sources (read from captions), anything else a web page.
source "$(dirname "$0")/_common.sh"
NOTEBOOK="${1:?Usage: add-sources.sh <notebook> [URL ...] [--text FILE|- [--title TITLE]]}"
shift
URLS=() TEXT_FILE="" TITLE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --text) TEXT_FILE="$2"; shift 2 ;;
    --title) TITLE="$2"; shift 2 ;;
    *) URLS+=("$1"); shift ;;
  esac
done

BODY=$(jq -n --arg nb "$NOTEBOOK" '{notebook: $nb}')
if [ ${#URLS[@]} -gt 0 ]; then BODY=$(jq --args '.urls = $ARGS.positional' "${URLS[@]}" <<< "$BODY"); fi
if [ -n "$TEXT_FILE" ]; then
  # Pasted text, up to 500,000 characters
  # jq reads the body from stdin below, so pasted stdin text goes through a temp file first
  if [ "$TEXT_FILE" = "-" ]; then TEXT_FILE=$(mktemp); cat > "$TEXT_FILE"; trap 'rm -f "$TEXT_FILE"' EXIT; fi
  BODY=$(jq --rawfile t "$TEXT_FILE" '.text = $t' <<< "$BODY")
  if [ -n "$TITLE" ]; then BODY=$(jq --arg t "$TITLE" '.title = $t' <<< "$BODY"); fi
fi
api POST sources "$BODY" | jq -r '.sources[] | "\(.kind)\t\(.status)\t\(.title)"'
