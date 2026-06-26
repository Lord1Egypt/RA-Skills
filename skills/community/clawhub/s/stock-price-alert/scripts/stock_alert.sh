#!/usr/bin/env bash
# stock_alert.sh — 股价异动实时提醒
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/config.json"
ONCE=false

# --- Args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --once)   ONCE=true; shift ;;
    --config) CONFIG_FILE="$2"; shift 2 ;;
    *)        echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# --- Deps ---
for cmd in curl jq; do
  command -v "$cmd" &>/dev/null || { echo "ERROR: $cmd not found"; exit 1; }
done

# --- Config ---
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "ERROR: config not found: $CONFIG_FILE"
  echo "Copy config.example.json to config.json and edit."
  exit 1
fi

POLL_INTERVAL=$(jq -r '.poll_interval_sec // 300' "$CONFIG_FILE")
EMAIL_ENABLED=$(jq -r '.notify.email // false' "$CONFIG_FILE")
SONOS_ENABLED=$(jq -r '.notify.sonos // false' "$CONFIG_FILE")
SONOS_SPEAKER=$(jq -r '.notify.sonos_speaker // "Kitchen"' "$CONFIG_FILE")
API_PROVIDER=$(jq -r '.api.provider // "alphavantage"' "$CONFIG_FILE")
API_KEY_ENV=$(jq -r '.api.apikey_env // "ALPHAVANTAGE_API_KEY"' "$CONFIG_FILE")
API_KEY="${!API_KEY_ENV:-}"

WATCH_COUNT=$(jq '.watchlist | length' "$CONFIG_FILE")

# --- Fetch quote (Alpha Vantage) ---
fetch_quote() {
  local symbol="$1"
  if [[ "$API_PROVIDER" == "alphavantage" ]]; then
    if [[ -z "$API_KEY" ]]; then
      echo "WARN: $API_KEY_ENV not set, skipping $symbol" >&2
      return 1
    fi
    local url="https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=${symbol}&apikey=${API_KEY}"
    local resp http_code
    for attempt in 1 2 3; do
      resp=$(curl -s -w '\n%{http_code}' "$url")
      http_code=$(echo "$resp" | tail -1)
      local body=$(echo "$resp" | sed '$d')
      if [[ "$http_code" == "200" ]]; then
        local price=$(echo "$body" | jq -r '."Global Quote"."05. price" // empty')
        local prev=$(echo "$body" | jq -r '."Global Quote"."08. previous close" // empty')
        local pct=$(echo "$body" | jq -r '."Global Quote"."10. change percent" // empty' | tr -d '%')
        if [[ -n "$price" && "$price" != "null" ]]; then
          echo "$price $prev $pct"
          return 0
        fi
      fi
      sleep 12  # Alpha Vantage rate limit
    done
    echo "WARN: failed to fetch $symbol after 3 attempts" >&2
    return 1
  else
    echo "ERROR: unsupported provider: $API_PROVIDER" >&2
    return 1
  fi
}

# --- Email ---
send_email() {
  local subject="$1" body="$2"
  if [[ "$EMAIL_ENABLED" != "true" ]]; then return 0; fi
  local smtp_host="${SMTP_HOST:-}" smtp_port="${SMTP_PORT:-587}"
  local smtp_user="${SMTP_USER:-}" smtp_pass="${SMTP_PASS:-}"
  local to="${ALERT_EMAIL_TO:-}"
  if [[ -z "$smtp_host" || -z "$to" ]]; then
    echo "  → 邮件跳过（SMTP 未配置）"
    return 0
  fi
  # Use curl SMTP
  if curl -s --ssl-reqd \
       --url "smtp://${smtp_host}:${smtp_port}" \
       --user "${smtp_user}:${smtp_pass}" \
       --mail-from "$smtp_user" \
       --mail-rcpt "$to" \
       -T <(cat <<EOF
From: ${smtp_user}
To: ${to}
Subject: ${subject}

${body}
EOF
  ) 2>/dev/null; then
    echo "  → 邮件已发送至 $to"
  else
    echo "  → 邮件发送失败，降级为控制台输出"
  fi
}

# --- Sonos ---
send_sonos() {
  local text="$1"
  if [[ "$SONOS_ENABLED" != "true" ]]; then return 0; fi
  if ! command -v sonos &>/dev/null; then
    echo "  → Sonos 跳过（sonos CLI 不可用）"
    return 0
  fi
  # Sonos TTS via say + clip — simplified: use sonos play with a notification approach
  # For now, use sonos volume + system notification as best-effort
  if sonos say --name "$SONOS_SPEAKER" "$text" 2>/dev/null; then
    echo "  → Sonos 播报: $SONOS_SPEAKER"
  else
    echo "  → Sonos 不可达，降级为控制台输出"
  fi
}

# --- Alert ---
check_and_alert() {
  local idx="$1"
  local symbol=$(jq -r ".watchlist[$idx].symbol" "$CONFIG_FILE")
  local name=$(jq -r ".watchlist[$idx].name // \"$symbol\"" "$CONFIG_FILE")
  local alert_pct=$(jq -r ".watchlist[$idx].alert_pct // 999" "$CONFIG_FILE")
  local price_above=$(jq -r ".watchlist[$idx].alert_price_above // null" "$CONFIG_FILE")
  local price_below=$(jq -r ".watchlist[$idx].alert_price_below // null" "$CONFIG_FILE")

  local quote
  if ! quote=$(fetch_quote "$symbol"); then
    return 0
  fi

  local price=$(echo "$quote" | awk '{print $1}')
  local prev_close=$(echo "$quote" | awk '{print $2}')
  local change_pct=$(echo "$quote" | awk '{print $3}')

  local ts=$(date '+%Y-%m-%d %H:%M:%S')
  local alerts=()

  # Pct alert
  if [[ -n "$change_pct" ]]; then
    local abs_pct
    abs_pct=$(echo "$change_pct" | tr -d '+' | awk '{if($1<0) $1=-$1; print $1}')
    if awk "BEGIN{exit !($abs_pct >= $alert_pct)}"; then
      local sign=""
      awk "BEGIN{if($change_pct>=0) exit 0; exit 1}" && sign="+" || sign=""
      alerts+=("涨幅${sign}${change_pct}%超阈值(${alert_pct}%)")
    fi
  fi

  # Price above
  if [[ "$price_above" != "null" && -n "$price_above" ]]; then
    if awk "BEGIN{exit !($price > $price_above)}"; then
      alerts+=("价格${price}上穿${price_above}")
    fi
  fi

  # Price below
  if [[ "$price_below" != "null" && -n "$price_below" ]]; then
    if awk "BEGIN{exit !($price < $price_below)}"; then
      alerts+=("价格${price}下穿${price_below}")
    fi
  fi

  if [[ ${#alerts[@]} -gt 0 ]]; then
    local alert_msg=$(IFS='，'; echo "${alerts[*]}")
    local sign=""
    awk "BEGIN{if($change_pct>=0) exit 0; exit 1}" && sign="+" || sign=""
    echo "[$ts] $symbol \$$price ${sign}${change_pct}% ⚠️ $alert_msg"

    local subject="[股价异动] $symbol ${sign}${change_pct}%"
    local body="$symbol ($name) 当前价格 \$$price，${sign}${change_pct}%，$alert_msg"
    send_email "$subject" "$body"
    send_sonos "$name 当前价格 $price 美元，${sign}${change_pct}%，$alert_msg"
  else
    local sign=""
    awk "BEGIN{if($change_pct>=0) exit 0; exit 1}" && sign="+" || sign=""
    echo "[$ts] $symbol \$$price ${sign}${change_pct}% ✅"
  fi
}

# --- Main loop ---
echo "Stock Price Alert started — watching $WATCH_COUNT symbol(s), interval ${POLL_INTERVAL}s"
while true; do
  for ((i=0; i<WATCH_COUNT; i++)); do
    check_and_alert "$i"
    sleep 12  # Rate limit between symbols
  done
  if $ONCE; then break; fi
  sleep "$POLL_INTERVAL"
done
