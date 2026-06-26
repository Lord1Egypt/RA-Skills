#!/bin/bash
#
# ZenQuote - Daily inspirational quotes from ZenQuotes.io
# Free API only - no premium features
#

set -e

API_BASE="https://zenquotes.io/api"
CONFIG_FILE="${ZENQUOTE_CONFIG:-$HOME/.openclaw/skills/zenquote/config.json}"

# Ensure config directory exists
mkdir -p "$(dirname "$CONFIG_FILE")"

# Initialize default config if not exists
init_config() {
  if [[ ! -f "$CONFIG_FILE" ]]; then
    cat > "$CONFIG_FILE" << 'EOF'
{
  "mode": "free"
}
EOF
  fi
}

# Fetch quote from API
fetch_quote() {
  local mode="${1:-random}"
  local url=""
  
  case "$mode" in
    today|daily)
      url="${API_BASE}/today"
      ;;
    random)
      url="${API_BASE}/random"
      ;;
    quotes)
      url="${API_BASE}/quotes"
      ;;
    *)
      url="${API_BASE}/random"
      ;;
  esac
  
  # Fetch and parse response
  local response=$(curl -s "$url" 2>/dev/null || echo "[]")
  echo "$response"
}

# Fetch quote image and save to file
fetch_image() {
  local output_path="${1:-/tmp/zenquote_image.jpg}"
  local api_url="${API_BASE}/image"
  
  # Download image
  curl -s "$api_url" -o "$output_path" 2>/dev/null
  
  if [[ -f "$output_path" && -s "$output_path" ]]; then
    echo "$output_path"
  else
    echo ""
  fi
}

# Format quote for display
format_quote() {
  local json="$1"
  local idx="${2:-0}"
  
  local quote=$(echo "$json" | jq -r ".[$idx].q // empty")
  local author=$(echo "$json" | jq -r ".[$idx].a // empty")
  
  if [[ -z "$quote" ]]; then
    echo "No quote available"
    return 1
  fi
  
  cat << EOF
"${quote}"

— ${author}

━━━━━━━━━━━━━━━━━━
Provided by [ZenQuotes API](https://zenquotes.io/)
EOF
}

# Get daily quote
get_daily_quote() {
  local response=$(fetch_quote "today")
  local formatted=$(format_quote "$response" 0)
  echo "$formatted"
}

# Get random quote
get_random_quote() {
  local response=$(fetch_quote "random")
  local formatted=$(format_quote "$response" 0)
  echo "$formatted"
}

# Get multiple quotes
get_quotes() {
  local count="${1:-5}"
  local response=$(fetch_quote "quotes")
  
  echo "🌟 Inspirational Quotes"
  echo ""
  
  for i in $(seq 0 $((count - 1))); do
    local quote=$(echo "$response" | jq -r ".[$i].q // empty")
    local author=$(echo "$response" | jq -r ".[$i].a // empty")
    
    if [[ -n "$quote" ]]; then
      echo "$((i + 1)). \"${quote}\""
      echo "   — ${author}"
      echo ""
    fi
  done
  
  echo "━━━━━━━━━━━━━━━━━━"
  echo "Inspirational quotes provided by ZenQuotes API"
  echo "https://zenquotes.io/"
}

# Setup daily cron job
setup_daily_cron() {
  local chat_id="$1"
  local type="${2:-text}"
  local account_id="${3:-default}"
  
  if [[ -z "$chat_id" ]]; then
    echo '{"error": "Chat ID required"}'
    return 1
  fi
  
  # Validate type
  if [[ "$type" != "text" && "$type" != "image" ]]; then
    echo '{"error": "Type must be text or image"}'
    return 1
  fi
  
  local job_name="zenquote-daily-${type}"
  local cron_config="$HOME/.openclaw/cron/${job_name}.json"
  local message_cmd=""
  
  if [[ "$type" == "image" ]]; then
    message_cmd="/zenQuote image"
  else
    message_cmd="/zenQuote today"
  fi
  
  cat > "$cron_config" << EOF
{
  "name": "${job_name}",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Taipei"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Send daily inspirational ${type} from ZenQuotes API to telegram:${chat_id} using the zenquote skill. Use ${message_cmd} command.",
    "model": "opencode-go/kimi-k2.5"
  },
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "${chat_id}",
    "accountId": "${account_id}"
  }
}
EOF
  
  echo "{\"setup\": true, \"type\": \"${type}\", \"message\": \"Daily ${type} scheduled for 9:00 AM\", \"chat_id\": \"${chat_id}\"}"
}

# CLI Main
main() {
  init_config
  
  local cmd="${1:-help}"
  shift || true
  
  case "$cmd" in
    today|daily)
      get_daily_quote
      ;;
    random)
      get_random_quote
      ;;
    quotes)
      get_quotes "$1"
      ;;
    image)
      local img_path=$(fetch_image "/tmp/zenquote_image.jpg")
      if [[ -n "$img_path" && -f "$img_path" ]]; then
        echo "{\"image_path\": \"${img_path}\", \"caption\": \"Provided by ZenQuotes API https://zenquotes.io/\"}"
      else
        echo "{\"error\": \"Failed to fetch image\"}"
      fi
      ;;
    setup)
      local chat_id="$1"
      local type="${2:-text}"
      local account_id="${3:-default}"
      setup_daily_cron "$chat_id" "$type" "$account_id"
      ;;
    help|*)
      cat << 'HELP'
ZenQuote - Daily Inspirational Quotes

Usage: zenquote <command> [args]

Commands:
  today                    Get today's quote
  random                   Get random quote  
  quotes [count]           Get multiple quotes (default 5)
  image                    Get quote image URL
  setup <chat_id> [type] [account] Setup daily cron job at 9:00 AM
                                     type: text (default) or image

Free API Limits:
  - 5 requests per 30 seconds
  - Attribution required when displaying quotes

Examples:
  zenquote today
  zenquote random
  zenquote quotes 3
  zenquote setup <chat_id> text       # Daily text quote
  zenquote setup <chat_id> image      # Daily image quote

API: https://zenquotes.io/
HELP
      ;;
  esac
}

main "$@"
