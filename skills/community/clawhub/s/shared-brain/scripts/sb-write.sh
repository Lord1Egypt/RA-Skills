#!/usr/bin/env bash
# sb-write.sh — Append a validated fact to the shared-brain queue
# Usage: sb-write.sh SECTION "key = value"
# Sections: INFRA PROJECTS DECISIONS CAMPAIGNS SECURITY
# Example: sb-write.sh INFRA "deploy:frontends = Vercel (migrated 2026-03-21)"

set -euo pipefail

_CLAWD="${SB_WORKSPACE:-$HOME/clawd}"
QUEUE="${SB_QUEUE:-$_CLAWD/memory/shared-brain-queue.md}"
VALID_SECTIONS="INFRA PROJECTS DECISIONS CAMPAIGNS SECURITY"
MAX_VALUE_LEN=300

if [ $# -lt 2 ]; then
  echo "Usage: sb-write.sh SECTION \"key = value\"" >&2
  exit 1
fi

SECTION="${1^^}"
FACT="$2"
AGENT="${SB_AGENT:-$(basename "$0")}"
TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M UTC')

# Validate section
if ! echo "$VALID_SECTIONS" | grep -qw "$SECTION"; then
  echo "Invalid section: $SECTION. Valid: $VALID_SECTIONS" >&2
  exit 1
fi

# Validate key=value format
if ! echo "$FACT" | grep -q " = "; then
  echo "Fact must contain ' = ' separator. Got: $FACT" >&2
  exit 1
fi

KEY="${FACT%% = *}"
VALUE="${FACT#* = }"

# Validate key: alphanumeric, colons, hyphens only (no shell-special chars)
if ! echo "$KEY" | grep -qE '^[a-zA-Z0-9:._-]+$'; then
  echo "Invalid key format: '$KEY'. Use alphanumeric, colons, hyphens, dots only." >&2
  exit 1
fi

# Validate value length
if [ "${#VALUE}" -gt $MAX_VALUE_LEN ]; then
  echo "Value too long (${#VALUE} chars, max $MAX_VALUE_LEN). Truncate before writing." >&2
  exit 1
fi

# Reject prompt-injection vectors in value
if echo "$VALUE" | grep -qP '[`\$<>]|\$\(|<!--|\{\{|<script|ignore prev|disregard|new instructions' 2>/dev/null || \
   echo "$VALUE" | grep -q '$('; then
  echo "Value contains disallowed characters or patterns (injection risk). Rejected." >&2
  exit 1
fi

# Escape any pipe or newline chars that would break the line format
VALUE="${VALUE//|/\|}"
VALUE=$(echo "$VALUE" | tr -d '\n\r')

# Ensure queue file exists
mkdir -p "$(dirname "$QUEUE")"
touch "$QUEUE"

# Atomic append
echo "[$TIMESTAMP] [$SECTION] [$AGENT] $KEY = $VALUE" >> "$QUEUE"
echo "✓ Queued: [$SECTION] $KEY = $VALUE"
