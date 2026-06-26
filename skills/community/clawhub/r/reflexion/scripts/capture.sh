#!/usr/bin/env bash
# reflexion/scripts/capture.sh
# PostToolUse hook for Bash — auto-captures errors from command output.
#
# Claude Code PostToolUse hooks receive JSON on stdin:
#   { "tool_name": "Bash", "tool_input": { "command": "..." }, "tool_output": "..." }
#
# This script:
#   1. Reads the tool output from stdin JSON
#   2. Checks for error patterns
#   3. If error found: creates a .reflexion/entries/ JSON file + updates index
#   4. Outputs nothing on success (zero overhead), or a short reminder on error capture
set -euo pipefail

# --- Init on first run ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${CLAUDE_PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REFLEX_DIR="$PROJECT_ROOT/.reflexion"

if [ ! -d "$REFLEX_DIR/entries" ]; then
  bash "$SCRIPT_DIR/init.sh" 2>/dev/null || true
fi

# --- Read stdin (Claude Code passes JSON via stdin for PostToolUse hooks) ---
INPUT=""
if [ ! -t 0 ]; then
  INPUT="$(cat)"
fi

# If no input, exit silently
[ -z "$INPUT" ] && exit 0

# --- Extract fields from JSON ---
# Use lightweight parsing: avoid jq dependency for maximum portability
# Extract tool_output using python if available, otherwise grep/sed
extract_field() {
  local field="$1"
  local json="$2"
  # Try python3 first (most reliable)
  if command -v python3 &>/dev/null; then
    python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    # Handle nested fields like tool_input.command
    keys = '$field'.split('.')
    v = d
    for k in keys:
        v = v[k]
    print(v if isinstance(v, str) else json.dumps(v))
except:
    pass
" <<< "$json" 2>/dev/null
    return
  fi
  # Fallback: basic grep extraction (handles simple cases)
  echo "$json" | grep -oP "\"$field\"\s*:\s*\"[^\"]*\"" | head -1 | sed 's/.*: *"//;s/"$//'
}

TOOL_OUTPUT="$(extract_field 'tool_output' "$INPUT")"
TOOL_COMMAND="$(extract_field 'tool_input.command' "$INPUT")"
TOOL_NAME="$(extract_field 'tool_name' "$INPUT")"

# Only process Bash tool outputs
[ -z "$TOOL_OUTPUT" ] && exit 0

# --- Error Detection ---
# Pattern list adapted from OMC's error-detector but reading actual stdin, not a phantom env var
ERROR_PATTERNS=(
  'error:'
  'Error:'
  'ERROR:'
  'FAILED'
  'command not found'
  'No such file or directory'
  'Permission denied'
  'fatal:'
  'Exception'
  'Traceback'
  'npm ERR!'
  'ModuleNotFoundError'
  'SyntaxError'
  'TypeError'
  'ReferenceError'
  'ImportError'
  'FileNotFoundError'
  'ConnectionRefusedError'
  'ENOENT'
  'EACCES'
  'EPERM'
  'segmentation fault'
  'core dumped'
  'panic:'
  'cannot find module'
  'compilation failed'
  'build failed'
)

# Also detect non-zero exit codes mentioned in output
EXIT_CODE_ERROR=false
if echo "$TOOL_OUTPUT" | grep -qiP '(exit code [1-9]|exited with [1-9]|returned [1-9])'; then
  EXIT_CODE_ERROR=true
fi

MATCHED_PATTERN=""
for pattern in "${ERROR_PATTERNS[@]}"; do
  if echo "$TOOL_OUTPUT" | grep -qiF "$pattern"; then
    MATCHED_PATTERN="$pattern"
    break
  fi
done

# No error detected — exit silently (zero overhead)
if [ -z "$MATCHED_PATTERN" ] && [ "$EXIT_CODE_ERROR" = false ]; then
  exit 0
fi

# --- Redact Secrets ---
redact() {
  local text="$1"
  # Redact Bearer tokens, API keys, passwords, AWS keys, private keys
  echo "$text" \
    | sed -E 's/(Bearer\s+)[A-Za-z0-9._\-]+/\1[REDACTED]/gi' \
    | sed -E 's/(api[_-]?key["\s:=]+)[A-Za-z0-9._\-]{8,}/\1[REDACTED]/gi' \
    | sed -E 's/(password["\s:=]+)[^\s",}]+/\1[REDACTED]/gi' \
    | sed -E 's/(AKIA[A-Z0-9]{16})/[REDACTED_AWS_KEY]/g' \
    | sed -E 's/(-----BEGIN [A-Z ]+ KEY-----).*(-----END)/\1[REDACTED]\2/g' \
    | sed -E 's/(token["\s:=]+)[A-Za-z0-9._\-]{8,}/\1[REDACTED]/gi' \
    | sed -E 's/(secret["\s:=]+)[A-Za-z0-9._\-]{8,}/\1[REDACTED]/gi'
}

# --- Extract Keywords ---
# Pull meaningful words from the error output and command
extract_keywords() {
  local text="$1"
  # Lowercase, strip punctuation, extract unique words 3+ chars, skip common noise
  echo "$text" \
    | tr '[:upper:]' '[:lower:]' \
    | tr -cs '[:alnum:]_-' '\n' \
    | grep -E '^.{3,}$' \
    | grep -vxF -e 'the' -e 'and' -e 'for' -e 'not' -e 'that' -e 'with' -e 'this' -e 'from' -e 'was' -e 'are' -e 'but' -e 'has' -e 'had' -e 'have' -e 'been' -e 'will' -e 'can' -e 'could' -e 'would' -e 'should' -e 'may' -e 'might' -e 'shall' -e 'does' -e 'did' -e 'done' -e 'its' -e 'into' -e 'also' -e 'than' -e 'then' -e 'each' -e 'which' -e 'their' -e 'there' -e 'these' -e 'those' -e 'such' -e 'when' -e 'where' -e 'while' -e 'about' -e 'after' -e 'before' -e 'between' -e 'under' -e 'over' -e 'just' -e 'like' -e 'more' -e 'some' -e 'only' -e 'other' -e 'very' -e 'still' -e 'already' -e 'usr' -e 'bin' -e 'lib' -e 'etc' -e 'var' -e 'tmp' -e 'dev' -e 'null' -e 'true' -e 'false' -e 'line' -e 'file' -e 'exit' -e 'code' \
    | sort -u \
    | head -20 \
    | tr '\n' ',' \
    | sed 's/,$//'
}

# --- Generate Entry ID ---
DATE_STAMP="$(date +%Y%m%d)"
RANDOM_SUFFIX="$(head -c 32 /dev/urandom 2>/dev/null | od -An -tx1 | tr -d ' \n' | head -c 3)"
[ -z "$RANDOM_SUFFIX" ] && RANDOM_SUFFIX="$(printf '%03d' $((RANDOM % 1000)))"
ENTRY_ID="RFX-${DATE_STAMP}-${RANDOM_SUFFIX}"

# --- Truncate output for storage (max 500 chars) ---
TRUNCATED_OUTPUT="$(redact "$TOOL_OUTPUT" | head -c 500)"
REDACTED_COMMAND="$(redact "${TOOL_COMMAND:-unknown}")"

# --- Extract keywords ---
KEYWORDS="$(extract_keywords "$TRUNCATED_OUTPUT $REDACTED_COMMAND")"

# --- Build entry JSON ---
# Escape strings for JSON
json_escape() {
  echo "$1" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read().strip()))" 2>/dev/null \
    || echo "\"$(echo "$1" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\n/\\n/g' | tr '\n' ' ')\""
}

TRIGGER_JSON="$(json_escape "$TRUNCATED_OUTPUT")"
CONTEXT_JSON="$(json_escape "$REDACTED_COMMAND")"
TODAY="$(date +%Y-%m-%d)"

ENTRY_FILE="$REFLEX_DIR/entries/${ENTRY_ID}.json"

cat > "$ENTRY_FILE" << ENTRY_EOF
{
  "id": "$ENTRY_ID",
  "type": "error",
  "trigger": $TRIGGER_JSON,
  "context": $CONTEXT_JSON,
  "resolution": "",
  "keywords": "$(echo "$KEYWORDS" | sed 's/,/", "/g; s/^/"/; s/$/"/')",
  "occurrences": 1,
  "first_seen": "$TODAY",
  "last_seen": "$TODAY",
  "promoted": false
}
ENTRY_EOF

# --- Update keyword index ---
INDEX_FILE="$REFLEX_DIR/index.txt"
IFS=',' read -ra KW_ARRAY <<< "$KEYWORDS"
for kw in "${KW_ARRAY[@]}"; do
  kw="$(echo "$kw" | tr -d ' "')"
  [ -z "$kw" ] && continue
  if grep -q "^${kw}:" "$INDEX_FILE" 2>/dev/null; then
    # Append entry ID to existing keyword line
    sed -i "s/^${kw}:/${kw}:${ENTRY_ID},/" "$INDEX_FILE" 2>/dev/null || true
  else
    echo "${kw}:${ENTRY_ID}" >> "$INDEX_FILE"
  fi
done

# --- Update stats ---
STATS_FILE="$REFLEX_DIR/stats.json"
if [ -f "$STATS_FILE" ] && command -v python3 &>/dev/null; then
  python3 -c "
import json, sys
try:
    with open('$STATS_FILE', 'r') as f:
        s = json.load(f)
    s['total_captured'] = s.get('total_captured', 0) + 1
    s['last_capture'] = '$TODAY'
    with open('$STATS_FILE', 'w') as f:
        json.dump(s, f, indent=2)
except:
    pass
" 2>/dev/null || true
fi

# --- Output a minimal reminder (only when error captured) ---
cat << EOF
<reflexion-captured>
Error captured as $ENTRY_ID. After resolving this error, update the entry:
  File: .reflexion/entries/${ENTRY_ID}.json
  Field: "resolution" — describe what fixed it
</reflexion-captured>
EOF
