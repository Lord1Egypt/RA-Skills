#!/usr/bin/env bash
# key-points.sh — Extract key points from URL or text

set -euo pipefail

INPUT="${1:-}"

if [[ -z "$INPUT" ]]; then
  echo "Usage: $0 <url or text>"
  echo "Usage: $0 -   # to read from stdin"
  exit 1
fi

# Check for stdin input
if [[ "$INPUT" == "-" ]]; then
  INPUT=$(cat)
fi

# Check if it looks like a URL
if [[ "$INPUT" =~ ^https?:// ]]; then
  CONTENT=$(curl -sL --max-time 30 -A "content-summarizer/1.0" "$INPUT" || true)
  if [[ -z "$CONTENT" ]]; then
    echo "ERROR: Failed to fetch URL: $INPUT"
    exit 1
  fi
  SOURCE="$INPUT (URL)"
else
  CONTENT="$INPUT"
  SOURCE="text input"
fi

if [[ ${#CONTENT} -lt 100 ]]; then
  echo "ERROR: Content too short to analyze"
  exit 1
fi

cat <<EOF
## Key Points — $SOURCE

### Main Insight
[One sentence capturing the core message]

### Supporting Points
- [Point 1: Key detail or argument]
- [Point 2: Additional context or evidence]
- [Point 3: Implication or call-to-action]

### Bottom Line
[One sentence: What should the reader do or think about this?]

---

*Note: This is a template. Run with OpenClaw agent for actual AI-powered extraction.*
EOF
