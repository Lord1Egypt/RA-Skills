#!/usr/bin/env bash
# shellbot-creative-studio — output helpers
# JSON to stdout, colored logs to stderr. Never mix them.

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log_info()  { echo -e "${CYAN}[creative]${NC} $*" >&2; }
log_ok()    { echo -e "${GREEN}[creative]${NC} $*" >&2; }
log_warn()  { echo -e "${YELLOW}[creative]${NC} $*" >&2; }
log_error() { echo -e "${RED}[creative]${NC} $*" >&2; }

# Emit structured JSON success to stdout
# Usage: json_output '{"key":"value"}'
json_output() {
  echo "$1"
}

# Emit structured JSON error to stdout and exit
# Usage: json_error "message" [exit_code]
json_error() {
  local msg="$1"
  local code="${2:-1}"
  echo "{\"error\":true,\"message\":$(printf '%s' "$msg" | jq -Rs .)}"
  exit "$code"
}

# Build JSON object from key=value pairs
# Usage: json_build status=completed provider=freepik
json_build() {
  local pairs=()
  for arg in "$@"; do
    local key="${arg%%=*}"
    local val="${arg#*=}"
    # Auto-detect if value is already JSON (starts with { or [)
    if [[ "$val" =~ ^[\{\[] ]]; then
      pairs+=("$(printf '"%s":%s' "$key" "$val")")
    elif [[ "$val" =~ ^(true|false|null)$ ]] || [[ "$val" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
      pairs+=("$(printf '"%s":%s' "$key" "$val")")
    else
      pairs+=("$(printf '"%s":%s' "$key" "$(printf '%s' "$val" | jq -Rs .)")")
    fi
  done
  local IFS=','
  echo "{${pairs[*]}}"
}

# Download a URL to a local path, return the local path
download_to() {
  local url="$1"
  local output="$2"
  local dir
  dir="$(dirname "$output")"
  mkdir -p "$dir"
  if curl -sfL -o "$output" "$url"; then
    log_ok "Downloaded → ${output}"
    echo "$output"
  else
    log_error "Failed to download: ${url}"
    return 1
  fi
}
