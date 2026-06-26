#!/usr/bin/env bash
# shellbot-creative-studio — provider selection logic
# Compatible with bash 3.2+ (no associative arrays)

# Get capabilities for a provider
_provider_caps() {
  case "$1" in
    freepik)       echo "image,edit,video,voice,music,sfx" ;;
    fal)           echo "image,edit,video" ;;
    nano-banana-2) echo "image,edit" ;;
    openrouter)    echo "image" ;;
    elevenlabs)    echo "voice,music,sfx" ;;
    *)             echo "" ;;
  esac
}

# Get the primary env var name for a provider
_provider_env() {
  case "$1" in
    freepik)       echo "FREEPIK_API_KEY" ;;
    fal)           echo "FAL_API_KEY" ;;
    nano-banana-2) echo "GOOGLE_API_KEY" ;;
    openrouter)    echo "OPENROUTER_API_KEY" ;;
    elevenlabs)    echo "ELEVENLABS_API_KEY" ;;
    *)             echo "" ;;
  esac
}

# Get setup URL for a provider
_provider_setup() {
  case "$1" in
    freepik)       echo "https://www.freepik.com/api/keys" ;;
    fal)           echo "https://fal.ai/dashboard/keys" ;;
    nano-banana-2) echo "https://aistudio.google.com/apikey" ;;
    openrouter)    echo "https://openrouter.ai/keys" ;;
    elevenlabs)    echo "https://elevenlabs.io/app/settings/api-keys" ;;
    *)             echo "" ;;
  esac
}

# Resolve which backend nano-banana-2 is using
get_nano_banana_backend() {
  if [[ -n "${GOOGLE_API_KEY:-}" ]]; then
    echo "google"
  elif [[ -n "${FAL_API_KEY:-}" ]]; then
    echo "fal"
  elif [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
    echo "openrouter"
  elif command -v infsh &>/dev/null; then
    echo "infsh"
  else
    echo "none"
  fi
}

# Check if a provider is available (env var set)
provider_available() {
  local provider="$1"

  # nano-banana-2 can use GOOGLE_API_KEY, FAL_API_KEY (fal-ai/nano-banana-2), or OPENROUTER_API_KEY
  if [[ "$provider" == "nano-banana-2" ]]; then
    [[ -n "${GOOGLE_API_KEY:-}" || -n "${FAL_API_KEY:-}" || -n "${OPENROUTER_API_KEY:-}" ]] && return 0
    command -v infsh &>/dev/null && return 0
    return 1
  fi

  local env_var
  env_var=$(_provider_env "$provider")
  [[ -n "$env_var" && -n "${!env_var:-}" ]]
}

# Check if a provider supports a task
provider_supports() {
  local provider="$1"
  local task="$2"
  local caps
  caps=$(_provider_caps "$provider")
  [[ ",$caps," == *",$task,"* ]]
}

# Select the best provider for a task
# Usage: select_provider <task> [--provider <override>]
select_provider() {
  local task="$1"
  shift
  local forced_provider=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --provider) forced_provider="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  # If provider is forced, validate it
  if [[ -n "$forced_provider" ]]; then
    if ! provider_supports "$forced_provider" "$task"; then
      log_error "Provider '${forced_provider}' does not support task '${task}'"
      json_error "Provider '${forced_provider}' does not support '${task}'"
    fi
    if ! provider_available "$forced_provider"; then
      local env_var setup
      env_var=$(_provider_env "$forced_provider")
      setup=$(_provider_setup "$forced_provider")
      log_error "Provider '${forced_provider}' requires ${env_var}. Setup: ${setup}"
      json_error "Missing ${env_var} for ${forced_provider}. Get it at: ${setup}"
    fi
    echo "$forced_provider"
    return
  fi

  # Auto-select based on priority per task
  local priority=""
  case "$task" in
    image)    priority="nano-banana-2 freepik fal openrouter" ;;
    edit)     priority="freepik fal nano-banana-2" ;;
    video)    priority="freepik fal" ;;
    voice)    priority="freepik elevenlabs" ;;
    music)    priority="freepik elevenlabs" ;;
    sfx)      priority="freepik elevenlabs" ;;
    *)        priority="freepik fal nano-banana-2 openrouter elevenlabs" ;;
  esac

  for provider in $priority; do
    if provider_available "$provider" && provider_supports "$provider" "$task"; then
      echo "$provider"
      return
    fi
  done

  # No provider available
  log_error "No provider available for task '${task}'"
  log_error "Set one of these environment variables:"
  for provider in $priority; do
    local env_var setup
    env_var=$(_provider_env "$provider")
    setup=$(_provider_setup "$provider")
    log_error "  ${env_var} — ${setup}"
  done
  json_error "No provider available for '${task}'. Run 'creative providers' to check setup."
}

# Require a provider's API key or exit
require_provider_key() {
  local provider="$1"

  if [[ "$provider" == "nano-banana-2" ]]; then
    if ! provider_available nano-banana-2; then
      log_error "Missing GOOGLE_API_KEY, FAL_API_KEY, or OPENROUTER_API_KEY"
      json_error "Missing GOOGLE_API_KEY, FAL_API_KEY, or OPENROUTER_API_KEY. See: https://aistudio.google.com/apikey"
    fi
    return
  fi

  local env_var setup
  env_var=$(_provider_env "$provider")
  if [[ -z "${!env_var:-}" ]]; then
    setup=$(_provider_setup "$provider")
    log_error "Missing ${env_var}. Setup: ${setup}"
    json_error "Missing ${env_var}. Get it at: ${setup}"
  fi
}

# Get provider API key value
get_provider_key() {
  local provider="$1"

  if [[ "$provider" == "nano-banana-2" ]]; then
    # Priority: GOOGLE_API_KEY > FAL_API_KEY > OPENROUTER_API_KEY
    if [[ -n "${GOOGLE_API_KEY:-}" ]]; then
      echo "${GOOGLE_API_KEY}"
    elif [[ -n "${FAL_API_KEY:-}" ]]; then
      echo "${FAL_API_KEY}"
    elif [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
      echo "${OPENROUTER_API_KEY}"
    else
      echo ""
    fi
    return
  fi

  local env_var
  env_var=$(_provider_env "$provider")
  echo "${!env_var:-}"
}

# Get default model for a provider+task combo
get_default_model() {
  local provider="$1"
  local task="$2"
  case "${provider}:${task}" in
    freepik:image)     echo "seedream-v5-lite" ;;
    freepik:video)     echo "kling-v3-omni-pro" ;;
    freepik:voice)     echo "elevenlabs-turbo-v2-5" ;;
    freepik:music)     echo "music-generation" ;;
    freepik:sfx)       echo "sound-effects" ;;
    fal:image)         echo "fal-ai/flux-2" ;;
    fal:video)         echo "fal-ai/kling-video/v2/image-to-video" ;;
    nano-banana-2:*)   echo "gemini-3.1-flash-image-preview" ;;
    openrouter:image)  echo "google/gemini-3.1-flash-image-preview" ;;
    elevenlabs:voice)  echo "eleven_turbo_v2_5" ;;
    elevenlabs:music)  echo "music-generation" ;;
    elevenlabs:sfx)    echo "sound-effects" ;;
    *)                 echo "" ;;
  esac
}
