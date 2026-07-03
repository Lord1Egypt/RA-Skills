#!/bin/bash
# sanitize.sh — Strip personal/security info from skill files
# Usage: sanitize.sh <input-dir> <output-dir>
#
# Reads replacement rules from sanitize-rules.conf (local, never published).
# Falls back to generic patterns (IPs, API keys, tokens) if no conf found.
set -euo pipefail

INPUT_DIR="$1"
OUTPUT_DIR="$2"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_FILE="$SCRIPT_DIR/sanitize-rules.conf"
SED_SCRIPT=$(mktemp /tmp/sanitize-sed-XXXXXX)

if [[ -z "$INPUT_DIR" || -z "$OUTPUT_DIR" ]]; then
  echo "Usage: sanitize.sh <input-dir> <output-dir>"
  exit 1
fi

# Copy everything first
cp -r "$INPUT_DIR"/. "$OUTPUT_DIR"/

# Remove any secrets files
find "$OUTPUT_DIR" -type f \( -name "*.key" -o -name "*.pem" -o -name "*.env" -o -name "*.secret" -o -name "*.credentials" \) -delete
find "$OUTPUT_DIR" -type d -name "secrets" -exec rm -rf {} + 2>/dev/null || true
find "$OUTPUT_DIR" -type f -name ".env*" -delete 2>/dev/null || true

# File extensions to sanitize
TEXT_EXTENSIONS="sh|mjs|js|ts|py|md|txt|json|yaml|yml|toml|cfg|conf|ini|html|css|jsx|tsx"

# Build sed script from rules file
cat > "$SED_SCRIPT" << 'GENERIC'
# Generic: Private/Tailscale IPs
s/100\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
s/192\.168\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
s/10\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
s/172\.1[6-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
s/172\.2[0-9]\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
s/172\.3[0-1]\.[0-9]\{1,3\}\.[0-9]\{1,3\}/<REDACTED_IP>/g
GENERIC

# Add rules from conf file
if [[ -f "$RULES_FILE" ]]; then
  while IFS='|' read -r type pattern replacement; do
    [[ "$type" =~ ^#.*$ || -z "$type" ]] && continue
    # Escape forward slashes for sed
    p_esc="${pattern//\//\\/}"
    r_esc="${replacement//\//\\/}"
    
    case "$type" in
      path)   echo "s|${pattern}|${replacement}|g" >> "$SED_SCRIPT" ;;
      email)  echo "s/${p_esc}/${r_esc}/g" >> "$SED_SCRIPT" ;;
      ssh)    echo "s/ssh ${pattern}@[^ ]*/ssh ${replacement}@<your-host>/g" >> "$SED_SCRIPT" ;;
      host)   echo "s/${p_esc}/${r_esc}/g" >> "$SED_SCRIPT" ;;
      ip)     echo "s/${p_esc}/${r_esc}/g" >> "$SED_SCRIPT" ;;
      github) echo "s/${p_esc}/${r_esc}/g" >> "$SED_SCRIPT" ;;
      secret) echo "s|${pattern}[^ \"']*|${replacement}|g" >> "$SED_SCRIPT" ;;
    esac
  done < "$RULES_FILE"
fi

# Add generic token patterns
cat >> "$SED_SCRIPT" << 'TOKENS'
# Port numbers on redacted IPs
s/<REDACTED_IP>:[0-9]\{1,5\}/<REDACTED_IP>:<PORT>/g
TOKENS

# Process each text file
find "$OUTPUT_DIR" -type f | while read -r file; do
  # Skip binary files (but not shell scripts marked "executable")
  if file "$file" | grep -q "binary\|image\|compressed" && ! file "$file" | grep -q "text\|script"; then
    continue
  fi
  
  ext="${file##*.}"
  if ! echo "$ext" | grep -qiE "^($TEXT_EXTENSIONS)$"; then
    if [[ "$ext" == "$file" ]] || file "$file" | grep -q "text"; then
      : # process it
    else
      continue
    fi
  fi

  # Apply sed script (all rules at once — much faster)
  sed -i -f "$SED_SCRIPT" "$file"
  
  # Extended regex patterns (API keys, tokens)
  sed -i -E \
    -e 's/(sk-[a-zA-Z0-9]{20,})/<REDACTED_API_KEY>/g' \
    -e 's/(xoxb-[a-zA-Z0-9-]+)/<REDACTED_TOKEN>/g' \
    -e 's/(xoxp-[a-zA-Z0-9-]+)/<REDACTED_TOKEN>/g' \
    -e 's/(ghp_[a-zA-Z0-9]{36,})/<REDACTED_TOKEN>/g' \
    -e 's/(gho_[a-zA-Z0-9]{36,})/<REDACTED_TOKEN>/g' \
    -e 's/(Bearer [a-zA-Z0-9_./-]{20,})/Bearer <REDACTED_TOKEN>/g' \
    -e 's|hooks\.slack\.com/[^ "]*|hooks.slack.com/<REDACTED> \
    -e 's|(HOOK_TOKEN[= ]+)[^ "'"'"']+|\1<REDACTED>|g' \
    "$file"
done

rm -f "$SED_SCRIPT"

TOTAL_FILES=$(find "$OUTPUT_DIR" -type f | wc -l)
echo "✅ Sanitized $TOTAL_FILES files in $OUTPUT_DIR"
