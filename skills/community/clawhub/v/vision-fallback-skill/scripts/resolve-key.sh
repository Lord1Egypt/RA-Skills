#!/usr/bin/env bash
# Resolve ARK_API_KEY from shell env or a dotenv file. Fails fast if missing.
# Sourced by call-api.sh; can also be run directly for a sanity check.
set -euo pipefail

: "${ARK_ENV_FILE:=}"
for f in "$ARK_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
  [ -n "$f" ] && [ -f "$f" ] || continue
  set -a; . "$f"; set +a
  break
done

if [ -z "${ARK_API_KEY:-}" ]; then
  echo "ERROR: ARK_API_KEY not found. Set ARK_API_KEY env var or store it in ~/.env_vars as ARK_API_KEY=..." >&2
  exit 1
fi

# Sanity check only — never print the value.
echo "ARK_API_KEY length: ${#ARK_API_KEY}" >&2
