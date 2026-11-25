#!/usr/bin/env bash
# Resolve vision-fallback provider configuration.
#
# Determines which vision API to call based on VISION_PROVIDER:
#   ark   (default) - Volcengine Ark / doubao
#   openai          - Any OpenAI-compatible endpoint
#
# Override everything with VISION_API_KEY / VISION_BASE_URL / VISION_MODEL.
#
# Sets these variables for the calling script:
#   VF_PROVIDER  VF_API_KEY  VF_ENDPOINT  VF_MODEL  VF_KEY_SOURCE
#
# Exits 1 if no API key can be resolved.
set -euo pipefail

# --- Load provider config from dotenv (before defaults are applied) ---
# Explicit env vars always win. Dotenv values fill in unset vars so users
# can configure VISION_PROVIDER / VISION_BASE_URL / VISION_MODEL in
# ~/.env_vars without exporting them in the shell.
# Must run BEFORE the case statement below, which applies := defaults.
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

# --- Provider defaults ---
# All endpoints are user-configurable via VISION_BASE_URL.
# No hardcoded runtime URL - defaults are assembled from provider name.
case "$VISION_PROVIDER" in
  ark)
    : "${VISION_BASE_URL:=https://ark.cn-beijing.volces.com/api/plan/v3}"
    : "${VISION_MODEL:=doubao-seed-2.0-lite}"
    KEY_ENV="ARK_API_KEY"
    ;;
  openai)
    : "${VISION_BASE_URL:=https://api.openai.com/v1}"
    : "${VISION_MODEL:=gpt-4o-mini}"
    KEY_ENV="OPENAI_API_KEY"
    ;;
  *)
    echo "ERROR: VISION_PROVIDER='$VISION_PROVIDER' is invalid. Use 'ark' or 'openai'." >&2
    exit 1
    ;;
esac

VF_PROVIDER="$VISION_PROVIDER"
VF_MODEL="$VISION_MODEL"
VF_ENDPOINT="${VISION_BASE_URL%/}/chat/completions"

# --- Resolve API key (precedence: explicit > provider-specific > dotenv) ---
# 1. VISION_API_KEY (explicit override, works for any provider)
# 2. Provider-specific env var (ARK_API_KEY / OPENAI_API_KEY)
# 3. Dotenv files (parsed safely with grep, NOT sourced)
VF_API_KEY=""
VF_KEY_SOURCE=""

if [ -n "${VISION_API_KEY:-}" ]; then
  VF_API_KEY="$VISION_API_KEY"
  VF_KEY_SOURCE="VISION_API_KEY"
else
  # Check provider-specific env var
  eval "prov_key=\"\${${KEY_ENV}:-}\""
  if [ -n "$prov_key" ]; then
    VF_API_KEY="$prov_key"
    VF_KEY_SOURCE="$KEY_ENV"
  else
    # Search dotenv files - parse with grep instead of sourcing
    # SECURITY: Sourcing a file executes its content as shell commands, which
    # is unsafe if the file is writable by another user.  We parse it as
    # KEY=VALUE lines instead.
    : "${VISION_ENV_FILE:=}"
    for f in "$VISION_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
      [ -n "$f" ] && [ -f "$f" ] || continue
      # Safe parse: extract KEY=VALUE lines, no execution
      _parse_env() {
        local file="$1" key="$2"
        # Match: optional whitespace, KEY, =, then value (strip surrounding quotes)
        grep -E "^\s*${key}=" "$file" 2>/dev/null | \
          head -1 | \
          sed -E "s/^\s*${key}=//; s/^\"(.*)\"$/\1/; s/^'(.*)'$/\1/"
      }
      # Check VISION_API_KEY first
      _val="$(_parse_env "$f" VISION_API_KEY)"
      if [ -n "$_val" ]; then
        VF_API_KEY="$_val"
        VF_KEY_SOURCE="$f:VISION_API_KEY"
        break
      fi
      # Then provider-specific
      _val="$(_parse_env "$f" "$KEY_ENV")"
      if [ -n "$_val" ]; then
        VF_API_KEY="$_val"
        VF_KEY_SOURCE="$f:$KEY_ENV"
        break
      fi
    done
    unset -f _parse_env
  fi
fi

# When sourced by call-api.sh, stay completely silent on stderr unless
# VF_VERBOSE=1 is set.  Errors (exit 1) still print to stderr.
# When run directly, always print the summary.
if [ "${BASH_SOURCE[0]}" = "${0:-}" ]; then
  _vf_verbose=1
else
  _vf_verbose="${VF_VERBOSE:-0}"
fi

if [ -z "$VF_API_KEY" ]; then
  cat >&2 <<EOF
ERROR: No API key resolved for provider '$VISION_PROVIDER'.
Tried (in order): VISION_API_KEY, $KEY_ENV, dotenv files (~/.env_vars).
Set one of:
  export VISION_API_KEY=...       # works for any provider
  export ${KEY_ENV}=...           # provider-specific
Or store in ~/.env_vars.
EOF
  exit 1
fi

# Sanity check only - never print the key value.
# NOTE: must end with a command that always returns 0, otherwise `set -e`
# in the sourcing script will abort on this last line when verbose is off.
if [ "$_vf_verbose" = "1" ]; then
  echo "Provider: $VF_PROVIDER | Model: $VF_MODEL | Key source: $VF_KEY_SOURCE (len ${#VF_API_KEY})" >&2
fi
true
