#!/usr/bin/env bash
# Preflight self-check for the vision-fallback skill.
#
# Verifies, in order:
#   1. Required shell deps are present (curl, jq, file, base64).
#   2. ARK_API_KEY can be resolved (env -> dotenv).
#   3. The Volcengine Ark endpoint is reachable (a quick TLS connect).
#
# Exits 0 only when all checks pass. On failure, prints a clear, actionable
# message to stderr and exits non-zero. Never prints the key value.
#
# Usage:  ./scripts/check.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS=0

red()   { printf '\033[31m%s\033[0m\n' "$*"; }
green() { printf '\033[32m%s\033[0m\n' "$*"; }
yellow(){ printf '\033[33m%s\033[0m\n' "$*"; }

# --- 1. Shell dependencies ---
MISSING=()
for c in curl jq file base64; do
  if ! command -v "$c" >/dev/null 2>&1; then
    MISSING+=("$c")
  fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
  red "FAIL: missing required commands: ${MISSING[*]}"
  red "       Install them (e.g. via brew/installer) and re-run."
  STATUS=1
else
  green "OK:   dependencies present (curl, jq, file, base64)"
fi

# --- 2. ARK_API_KEY resolution ---
# Source resolve-key.sh's logic without aborting on failure.
ARK_KEY=""
if [ -n "${ARK_API_KEY:-}" ]; then
  ARK_KEY="$ARK_API_KEY"
else
  : "${ARK_ENV_FILE:=}"
  for f in "$ARK_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
    [ -n "$f" ] && [ -f "$f" ] || continue
    # shellcheck disable=SC1090
    ARK_KEY="$(set -a; . "$f" 2>/dev/null; printf '%s' "${ARK_API_KEY:-}")"
    [ -n "$ARK_KEY" ] && break
  done
fi

if [ -z "$ARK_KEY" ]; then
  red "FAIL: ARK_API_KEY not found."
  red "       Set the ARK_API_KEY env var, or store it in ~/.env_vars as:"
  red "         ARK_API_KEY=xxxxxxxxxxxxxxxx"
  red "       (issued by Volcengine / 火山引擎). See references/configuration.md."
  STATUS=1
else
  green "OK:   ARK_API_KEY resolved (length ${#ARK_KEY})"
fi

# --- 3. Endpoint reachability ---
HOST="ark.cn-beijing.volces.com"
PORT=443
if command -v curl >/dev/null 2>&1; then
  # Connect-only, 5s timeout, don't transfer anything.
  if curl -sS --connect-timeout 5 --max-time 8 \
        "https://${HOST}/" -o /dev/null 2>/dev/null; then
    green "OK:   endpoint reachable (https://${HOST})"
  else
    yellow "WARN: could not reach https://${HOST} within 5s."
    yellow "      Check network / region reachability. The API call may still fail."
    # Reachability is a warning, not a hard failure (could be transient / proxied).
  fi
fi

# --- Summary ---
if [ "$STATUS" -ne 0 ]; then
  red ""
  red "Preflight FAILED. Fix the issues above before calling ./scripts/call-api.sh."
  red "Do NOT substitute this skill with local OCR (tesseract) — it cannot do"
  red "visual/layout understanding. Configure the missing prerequisite instead."
  exit "$STATUS"
fi

green ""
green "Preflight OK. Ready to run ./scripts/call-api.sh"
