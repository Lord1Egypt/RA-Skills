#!/bin/bash
# Update employees.json on GitHub
# Usage: update-employees.sh '<FULL_JSON_CONTENT>'
#    or: echo '<JSON>' | update-employees.sh
#    or: update-employees.sh /path/to/employees.json
# The script replaces the entire employees.json with the provided content.

set -e

JSON_CONTENT="$1"

# If $1 is a file path, read from it
if [ -n "$JSON_CONTENT" ] && [ -f "$JSON_CONTENT" ]; then
  JSON_CONTENT=$(cat "$JSON_CONTENT")
fi

# If no $1 and stdin is not a terminal, read from stdin
if [ -z "$JSON_CONTENT" ] && [ ! -t 0 ]; then
  JSON_CONTENT=$(cat)
fi

if [ -z "$JSON_CONTENT" ]; then
  echo "Usage: update-employees.sh '<FULL_EMPLOYEES_JSON>'"
  echo "   or: echo '<JSON>' | update-employees.sh"
  exit 1
fi

# Validate JSON before pushing
if ! echo "$JSON_CONTENT" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
  echo "ERROR: Content is NOT valid JSON. Refusing to push."
  echo "First 200 chars of content:"
  echo "$JSON_CONTENT" | head -c 200
  echo ""
  echo "Make sure to pass the actual JSON string, not a shell command."
  exit 1
fi

REPO="${ROSTER_REPO}"

if [ -z "$REPO" ]; then
  echo "ERROR: ROSTER_REPO environment variable is not set."
  echo "Set it to your GitHub repository in 'owner/repo' format."
  exit 1
fi
FILE_PATH="employees.json"

# Base64 encode via printf to avoid shell escaping issues
CONTENT_B64=$(printf '%s' "$JSON_CONTENT" | base64 -w 0)

# Get current file SHA (required for update)
RESPONSE=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/contents/$FILE_PATH?ref=main" 2>/dev/null || echo "{}")

EXISTING_SHA=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('sha',''))" 2>/dev/null || echo "")

if [ -z "$EXISTING_SHA" ]; then
  echo "ERROR: Could not get SHA of existing employees.json"
  exit 1
fi

# Build payload safely via python3 with sys.argv (no shell interpolation in JSON)
PAYLOAD=$(python3 -c "
import json, sys
sha = sys.argv[1]
b64 = sys.argv[2]
print(json.dumps({
    'message': 'feat: update employees.json',
    'content': b64,
    'sha': sha,
    'branch': 'main'
}))
" "$EXISTING_SHA" "$CONTENT_B64")

# Push to GitHub
RESULT=$(curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$REPO/contents/$FILE_PATH" \
  -d "$PAYLOAD")

# Check result
if echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); assert 'content' in d" 2>/dev/null; then
  COMMIT_SHA=$(echo "$RESULT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('commit',{}).get('sha','unknown'))")
  echo "SUCCESS: Updated employees.json on GitHub"
  echo "Commit: $COMMIT_SHA"
  echo "URL: https://github.com/$REPO/blob/main/$FILE_PATH"
else
  echo "ERROR: Failed to update employees.json"
  echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('message','Unknown error'))" 2>/dev/null || echo "$RESULT"
  exit 1
fi
