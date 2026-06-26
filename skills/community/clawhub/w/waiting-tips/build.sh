#!/usr/bin/env bash
# Build: generate tips.json from tips/*.txt
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIPS_DIR="$SCRIPT_DIR/tips"
OUT="$SCRIPT_DIR/tips.json"

tips=()
while IFS= read -r line; do
  [[ -z "$line" || "$line" == \#\#* ]] && continue
  escaped=$(echo "$line" | sed 's/\\/\\\\/g; s/"/\\"/g')
  tips+=("$escaped")
done < <(cat "$TIPS_DIR"/*.txt)

# build JSON
echo '{' > "$OUT"
echo '  "version": "1.0.0",' >> "$OUT"
echo "  \"count\": ${#tips[@]}," >> "$OUT"
echo '  "tips": [' >> "$OUT"

last=$((${#tips[@]} - 1))
for i in "${!tips[@]}"; do
  if (( i == last )); then
    echo "    \"${tips[$i]}\"" >> "$OUT"
  else
    echo "    \"${tips[$i]}\"," >> "$OUT"
  fi
done

echo '  ]' >> "$OUT"
echo '}' >> "$OUT"

echo "Built ${#tips[@]} tips -> $OUT"
