#!/usr/bin/env bash
# Upload a local file as a source: PDF, Word, PowerPoint, EPUB, Markdown, text, CSV, audio, video or an image.
# Usage: upload-file.sh <notebook> <path/to/file>
# The file is the raw request body; the API refuses files over 200 MB, and files over 100 MB are untested.
source "$(dirname "$0")/_common.sh"
NOTEBOOK="${1:?Usage: upload-file.sh <notebook> <file>}"
FILE="${2:?Usage: upload-file.sh <notebook> <file>}"

case "$(printf '%s' "$FILE" | tr '[:upper:]' '[:lower:]')" in
  *.pdf) TYPE=application/pdf ;;
  *.docx) TYPE=application/vnd.openxmlformats-officedocument.wordprocessingml.document ;;
  *.pptx) TYPE=application/vnd.openxmlformats-officedocument.presentationml.presentation ;;
  *.epub) TYPE=application/epub+zip ;;
  *.md) TYPE=text/markdown ;;
  *.txt) TYPE=text/plain ;;
  *.csv) TYPE=text/csv ;;
  *.mp3) TYPE=audio/mpeg ;;
  *.m4a) TYPE=audio/mp4 ;;
  *.wav) TYPE=audio/wav ;;
  *.mp4) TYPE=video/mp4 ;;
  *.jpg|*.jpeg) TYPE=image/jpeg ;;
  *.png) TYPE=image/png ;;
  *.webp) TYPE=image/webp ;;
  *) echo "Unsupported file type: $FILE (see https://useapi.net/docs/api-gemini-notebook-v1/post-gemini-notebook-sources-upload)" >&2; exit 1 ;;
esac

OUT=$(mktemp)
trap 'rm -f "$OUT"' EXIT
CODE=$(acurl -sS --max-time 600 -o "$OUT" -w '%{http_code}' -H "Content-Type: $TYPE" --data-binary "@$FILE" \
  "$API/sources/upload?notebook=$(enc "$NOTEBOOK")&name=$(enc "$(basename "$FILE")")") || true
if [ "${CODE:0:1}" != "2" ]; then
  echo "POST /sources/upload -> HTTP ${CODE:-000}: $(cat "$OUT")" >&2
  exit 1
fi
jq -r '"\(.kind // "file")\t\(.status)\t\(.title)"' "$OUT"
