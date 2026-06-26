#!/usr/bin/env bash
set -euo pipefail

CLI_URL="${TAPAUTH_CLI_URL:-https://tapauth.ai/cli/tapauth}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOCAL_SCRIPT="$SKILL_DIR/scripts/tapauth.sh"

tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

curl --fail --location --silent --show-error "$CLI_URL" --output "$tmp_file"

if cmp -s "$LOCAL_SCRIPT" "$tmp_file"; then
  echo "scripts/tapauth.sh matches $CLI_URL"
  exit 0
fi

echo "ERROR: scripts/tapauth.sh does not match $CLI_URL" >&2
echo "" >&2
echo "Local SHA-256:" >&2
shasum -a 256 "$LOCAL_SCRIPT" >&2
echo "Canonical SHA-256:" >&2
shasum -a 256 "$tmp_file" >&2
echo "" >&2
echo "Update it with:" >&2
echo "  curl -fsSL $CLI_URL -o scripts/tapauth.sh && chmod +x scripts/tapauth.sh" >&2

if command -v diff >/dev/null 2>&1; then
  echo "" >&2
  echo "Diff, canonical -> local:" >&2
  diff -u "$tmp_file" "$LOCAL_SCRIPT" >&2 || true
fi

exit 1
