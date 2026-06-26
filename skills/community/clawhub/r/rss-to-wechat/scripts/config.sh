#!/bin/bash
# RSS to WeChat - Configuration

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE="${WORKSPACE:-$SKILL_DIR}"
OUTPUT_DIR="${OUTPUT_DIR:-$WORKSPACE/output}"
DRAFTS_DIR="${DRAFTS_DIR:-$WORKSPACE/drafts}"

mkdir -p "$OUTPUT_DIR" "$DRAFTS_DIR"

if [ ${#RSS_SOURCES[@]} -eq 0 ]; then
  RSS_SOURCES=("simonwillison.net" "paulgraham.com")
fi

MIN_VIEWS_DAILY=${MIN_VIEWS_DAILY:-10000}
MAX_VIEWS_DAILY=${MAX_VIEWS_DAILY:-100000}
MIN_VIEWS_FEATURED=${MIN_VIEWS_FEATURED:-100000}

if [ ${#PRIORITY_KEYWORDS[@]} -eq 0 ]; then
  PRIORITY_KEYWORDS=("AI" "Artificial Intelligence" "Machine Learning")
fi

if [ ${#GENERAL_KEYWORDS[@]} -eq 0 ]; then
  GENERAL_KEYWORDS=("technology" "programming" "software")
fi

if [ ${#EXCLUDE_KEYWORDS[@]} -eq 0 ]; then
  EXCLUDE_KEYWORDS=("crypto" "blockchain")
fi

WECHAT_APPID="${WECHAT_APPID:-}"
WECHAT_APPSECRET="${WECHAT_APPSECRET:-}"
WECHAT_PUBLISH_SCRIPT="${WECHAT_PUBLISH_SCRIPT:-}"

COVER_WIDTH=${COVER_WIDTH:-1283}
COVER_HEIGHT=${COVER_HEIGHT:-383}
COVER_SKILL="${COVER_SKILL:-}"

BRAND_NAME="${BRAND_NAME:-AI News}"
BRAND_SLOGAN="${BRAND_SLOGAN:-All the AI News That is Fit to Read}"
BRAND_COLOR="${BRAND_COLOR:-#c41e3a}"

export TZ="${TZ:-Asia/Shanghai}"
DEBUG=${DEBUG:-0}

log() {
  echo "[$(date "+%Y-%m-%d %H:%M:%S")] $*"
}

debug() {
  [ "$DEBUG" = "1" ] && echo "[DEBUG] $*" >&2
}

error() {
  echo "[ERROR] $*" >&2
}

warn() {
  echo "[WARN] $*" >&2
}

LOCAL_CONFIG="$SKILL_DIR/config.local.sh"
[ -f "$LOCAL_CONFIG" ] && source "$LOCAL_CONFIG"

validate_config() {
  local errors=0
  for cmd in curl jq pandoc; do
    if ! command -v "$cmd" &> /dev/null; then
      error "Missing required tool: $cmd"
      errors=$((errors + 1))
    fi
  done
  if [ -n "$WECHAT_PUBLISH_SCRIPT" ]; then
    if [ -z "$WECHAT_APPID" ] || [ -z "$WECHAT_APPSECRET" ]; then
      warn "WeChat config incomplete, will skip publishing"
    fi
  fi
  return $errors
}

show_config_help() {
  echo "RSS to WeChat - Configuration Help"
  echo ""
  echo "1. Copy config.example.sh to config.local.sh"
  echo "2. Edit config.local.sh with your settings"
  echo "3. Run: bash rss-to-wechat.sh --check"
}
