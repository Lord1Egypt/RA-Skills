#!/usr/bin/env bash
# secret-scrub.sh — regex-based redaction. Patterns loaded from secret-patterns.tsv.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERNS_FILE="$SCRIPT_DIR/secret-patterns.tsv"

SKILLMINER_SECRET_NAMES=()
SKILLMINER_SECRET_PATTERNS=()
if [[ -r "$PATTERNS_FILE" ]]; then
  while IFS=$'\t' read -r name regex; do
    [[ "$name" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$name" ]] && continue
    SKILLMINER_SECRET_NAMES+=("$name")
    SKILLMINER_SECRET_PATTERNS+=("$regex")
  done < "$PATTERNS_FILE"
fi

# Usage: scrub_stream < input > output   (stdin → stdout)
# Replaces PEM blocks with [REDACTED:pem] and single-line matches with [REDACTED:<name>].
scrub_stream() {
  local input
  input="$(cat)"
  # PEM block: multiline BEGIN..END range → single [REDACTED:pem]
  input="$(printf '%s' "$input" | sed -E '/-----BEGIN [A-Z ]+-----/,/-----END [A-Z ]+-----/c\
[REDACTED:pem]')"
  local i=0
  for pattern in "${SKILLMINER_SECRET_PATTERNS[@]}"; do
    local name="${SKILLMINER_SECRET_NAMES[$i]}"
    input="$(printf '%s' "$input" | sed -E "s#$pattern#[REDACTED:$name]#g")"
    i=$((i + 1))
  done
  printf '%s' "$input"
}

# Usage: scrub_file_in_place <file>
# Scrubs file content, writes back atomically (via mv).
scrub_file_in_place() {
  local file="$1"
  [[ -f "$file" ]] || return 0
  local tmp
  tmp="$(mktemp "${file}.scrub.XXXXXX")"
  scrub_stream < "$file" > "$tmp"
  mv "$tmp" "$file"
}
