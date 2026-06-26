#!/bin/bash
# Lightweight local pattern helper for Verified Humanizer
set -e
TEXT="${1:-}"
if [ -z "$TEXT" ]; then
  echo "Usage: scan-text.sh \"text to inspect\""
  exit 0
fi

count_matches() {
  local pattern="$1"
  printf '%s' "$TEXT" | grep -Eio "$pattern" | wc -l | tr -d ' '
}

echo "Potential pattern counts:"
echo "- filler phrases: $(count_matches 'in order to|due to the fact that|at this point in time')"
echo "- ai vocabulary: $(count_matches 'additionally|pivotal|underscor(e|es|ed)|showcase|landscape|testament|vibrant')"
echo "- chatbot residue: $(count_matches 'i hope this helps|great question|let me know if you\x27d like')"
echo "- em dashes: $(printf '%s' "$TEXT" | grep -o '—' | wc -l | tr -d ' ')"
