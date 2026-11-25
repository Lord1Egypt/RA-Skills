#!/usr/bin/env bash
# Preflight self-check for the vision-fallback skill.
#
# Verifies, in order:
#   1. Required shell deps are present (curl, jq, file, base64).
#   2. API key can be resolved for the configured provider (ark|openai).
#   3. The configured endpoint is reachable (a quick TLS connect).
#
# Exits 0 only when all checks pass. On failure, prints a clear, actionable
# message to stderr and exits non-zero. Never prints the key value.
#
# By default output is minimal (one line per check).  Set VF_VERBOSE=1 for
# colored, detailed output.
#
# Usage:  ./scripts/check.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS=0
VERBOSE="${VF_VERBOSE:-0}"

# Minimal output: plain text, no ANSI colors (agents don't need colors).
# Verbose mode: colored, detailed (for human terminal use).
if [ "$VERBOSE" = "1" ]; then
  red()   { printf '\033[31m%s\033[0m\n' "$*"; }
  green() { printf '\033[32m%s\033[0m\n' "$*"; }
  yellow(){ printf '\033[33m%s\033[0m\n' "$*"; }
else
  red()   { printf '%s\n' "$*"; }
  green() { printf '%s\n' "$*"; }
  yellow(){ printf '%s\n' "$*"; }
fi

# --- Load provider config from dotenv (before defaults are applied) ---
# Explicit env vars always win. Dotenv values fill in unset vars so users
# can configure VISION_PROVIDER / VISION_BASE_URL / VISION_MODEL in
# ~/.env_vars without exporting them in the shell.
: "${VISION_ENV_FILE:=}"
for _vf_f in "$VISION_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
  [ -n "$_vf_f" ] && [ -f "$_vf_f" ] || continue
  for _vf_k in VISION_PROVIDER VISION_BASE_URL VISION_MODEL; do
    eval "_vf_cur=\${${_vf_k}:-}"
    [ -n "$_vf_cur" ] && continue
    _vf_val="$(grep -E "^\s*${_vf_k}=" "$_vf_f" 2>/dev/null | head -1 | sed -E "s/^\s*${_vf_k}=//; s/^\"(.*)\"$/\1/; s/^'(.*)'$/\1/")"
    if [ -n "$_vf_val" ]; then
      eval "export ${_vf_k}=\$_vf_val"
    fi
  done
done
unset _vf_f _vf_k _vf_cur _vf_val

: "${VISION_PROVIDER:=ark}"

# --- 1. Shell dependencies ---
MISSING=()
for c in curl jq file base64; do
  if ! command -v "$c" >/dev/null 2>&1; then
    MISSING+=("$c")
  fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
  red "FAIL: missing commands: ${MISSING[*]}"
  STATUS=1
else
  # Verify base64 supports stdin mode (macOS/BSD rejects positional file args)
  if ! echo "test" | base64 >/dev/null 2>&1; then
    red "FAIL: base64 does not support stdin input on this system"
    STATUS=1
  else
    [ "$VERBOSE" = "1" ] && green "OK:   deps (curl, jq, file, base64)"
  fi
fi

# --- 2. Provider config + API key resolution ---
case "$VISION_PROVIDER" in
  ark)
    BASE_URL="${VISION_BASE_URL:-https://ark.cn-beijing.volces.com/api/plan/v3}"
    MODEL="${VISION_MODEL:-doubao-seed-2.0-lite}"
    KEY_ENV="ARK_API_KEY"
    ;;
  openai)
    BASE_URL="${VISION_BASE_URL:-https://api.openai.com/v1}"
    MODEL="${VISION_MODEL:-gpt-4o-mini}"
    KEY_ENV="OPENAI_API_KEY"
    ;;
  *)
    red "FAIL: VISION_PROVIDER='$VISION_PROVIDER' is invalid. Use 'ark' or 'openai'."
    exit 1
    ;;
esac

# Helper: safely parse KEY=VALUE from a dotenv file (no sourcing/exec)
_parse_env() {
  local file="$1" key="$2"
  grep -E "^\s*${key}=" "$file" 2>/dev/null | \
    head -1 | \
    sed -E "s/^\s*${key}=//; s/^\"(.*)\"$/\1/; s/^'(.*)'$/\1/"
}

RESOLVED_KEY=""
KEY_SOURCE=""
if [ -n "${VISION_API_KEY:-}" ]; then
  RESOLVED_KEY="$VISION_API_KEY"
  KEY_SOURCE="VISION_API_KEY"
else
  eval "prov_key=\"\${${KEY_ENV}:-}\""
  if [ -n "$prov_key" ]; then
    RESOLVED_KEY="$prov_key"
    KEY_SOURCE="$KEY_ENV"
  else
    : "${VISION_ENV_FILE:=}"
    for f in "$VISION_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
      [ -n "$f" ] && [ -f "$f" ] || continue
      _val="$(_parse_env "$f" VISION_API_KEY)"
      if [ -n "$_val" ]; then
        RESOLVED_KEY="$_val"
        KEY_SOURCE="$f:VISION_API_KEY"
        break
      fi
      _val="$(_parse_env "$f" "$KEY_ENV")"
      if [ -n "$_val" ]; then
        RESOLVED_KEY="$_val"
        KEY_SOURCE="$f:$KEY_ENV"
        break
      fi
    done
  fi
fi
unset -f _parse_env

if [ -z "$RESOLVED_KEY" ]; then
  red "FAIL: no API key. Set VISION_API_KEY or ${KEY_ENV} (or store in ~/.env_vars)"
  STATUS=1
else
  [ "$VERBOSE" = "1" ] && green "OK:   provider=$VISION_PROVIDER model=$MODEL key=$KEY_SOURCE (len ${#RESOLVED_KEY})"
fi

# --- 3. Endpoint reachability (warning only, not fatal) ---
HOST="$(printf '%s' "$BASE_URL" | sed -E 's|https?://([^/:]+).*|\1|')"
SCHEME="$(printf '%s' "$BASE_URL" | sed -E 's|^(https?)://.*|\1|')"
[ -z "$SCHEME" ] && SCHEME="https"
if command -v curl >/dev/null 2>&1; then
  if curl -sS --connect-timeout 5 --max-time 8 \
        "${SCHEME}://${HOST}/" -o /dev/null 2>/dev/null; then
    [ "$VERBOSE" = "1" ] && green "OK:   endpoint reachable (${SCHEME}://${HOST})"
  else
    [ "$VERBOSE" = "1" ] && yellow "WARN: endpoint ${SCHEME}://${HOST} not reachable (may be transient/proxied)"
  fi
fi

# --- Summary ---
if [ "$STATUS" -ne 0 ]; then
  red "Preflight FAILED. Fix the above before calling call-api.sh."
  exit "$STATUS"
fi

[ "$VERBOSE" = "1" ] && green "Preflight OK."
true
