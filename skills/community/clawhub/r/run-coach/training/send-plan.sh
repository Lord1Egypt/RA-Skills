#!/bin/bash
# send-plan.sh — Screenshot HTML(s) and send as Telegram photo(s)
#
# Usage: send-plan.sh <caption> <html1.html> [html2.html ...]
# Multiple HTMLs are screenshotted individually and sent as a photo album.
#
# Credentials: skill-root .credentials dotfile (chmod 600) read by
# send-album.mjs directly — this script never touches them.
#
# Example (split weekly plan):
#   send-plan.sh "Week 5 Plan" week-05-run.html week-05-cross.html
# Example (single plan):
#   send-plan.sh "Today's Session" today.html

set -e

CAPTION="$1"
shift
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$CAPTION" ] || [ $# -eq 0 ]; then
  echo "Usage: send-plan.sh <caption> <html1.html> [html2.html ...]"
  exit 1
fi

PNG_FILES=()
for HTML_FILE in "$@"; do
  BASENAME=$(basename "$HTML_FILE" .html)
  DIR=$(dirname "$HTML_FILE")
  PNG_FILE="${DIR}/${BASENAME}-hd.png"
  echo "Generating screenshot: $(basename $HTML_FILE) → $(basename $PNG_FILE)"
  node "${SCRIPT_DIR}/screenshot.mjs" "$HTML_FILE" "$PNG_FILE"
  PNG_FILES+=("$PNG_FILE")
done

echo "Sending ${#PNG_FILES[@]} image(s)..."
node "${SCRIPT_DIR}/send-album.mjs" "$CAPTION" "${PNG_FILES[@]}"
