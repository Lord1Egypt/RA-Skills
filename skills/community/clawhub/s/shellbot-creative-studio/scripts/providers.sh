#!/usr/bin/env bash
# shellbot-creative-studio — provider availability check
# Usage: providers
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"
source "${SCRIPT_DIR}/lib/provider_router.sh"

ALL_PROVIDERS="freepik fal nano-banana-2 openrouter elevenlabs"

log_info "Provider availability check"
log_info "==========================="

entries=""
for p in $ALL_PROVIDERS; do
  avail=false
  provider_available "$p" && avail=true

  caps=$(_provider_caps "$p")
  caps_json=$(echo "$caps" | tr ',' '\n' | jq -R . | jq -s .)
  env_var=$(_provider_env "$p")
  setup=$(_provider_setup "$p")

  # Human-readable
  caps_pretty=$(echo "$caps" | tr ',' ', ')
  if [[ "$avail" == "true" ]]; then
    if [[ "$p" == "nano-banana-2" ]]; then
      backend=$(get_nano_banana_backend)
      log_ok "${p}: READY via ${backend} (${caps_pretty})"
    else
      log_ok "${p}: READY (${caps_pretty})"
    fi
  else
    if [[ "$p" == "nano-banana-2" ]]; then
      log_warn "${p}: NOT CONFIGURED — set GOOGLE_API_KEY or OPENROUTER_API_KEY"
    else
      log_warn "${p}: NOT CONFIGURED — set ${env_var}"
    fi
  fi

  # JSON entry
  entry=$(printf '"%s":{"available":%s,"env_var":"%s","setup":"%s","capabilities":%s}' \
    "$p" "$avail" "$env_var" "$setup" "$caps_json")

  if [[ -n "$entries" ]]; then
    entries="${entries},${entry}"
  else
    entries="$entry"
  fi
done

# JSON to stdout
echo "{${entries}}" | jq .
