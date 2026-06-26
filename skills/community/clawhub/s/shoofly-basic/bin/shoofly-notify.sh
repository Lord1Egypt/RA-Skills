#!/usr/bin/env bash
# Usage: shoofly-notify <channel|"auto"> "<message>"
# Card 192: OpenClaw-native channel delivery with auto-discovery

set -euo pipefail

# Input validation
if [[ -z "${1:-}" ]] || [[ -z "${2:-}" ]]; then
  echo "Usage: shoofly-notify <channel|auto> <message>" >&2
  exit 1
fi

CHANNEL="$1"
MSG="$2"

# Strip leading/trailing whitespace and newlines
MSG="${MSG#"${MSG%%[![:space:]]*}"}"
MSG="${MSG%"${MSG##*[![:space:]]}"}"

# Sanitize MSG length
if [[ ${#MSG} -gt 500 ]]; then
  MSG="${MSG:0:497}..."
fi

CONFIG="$HOME/.shoofly/config.json"
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.shoofly/logs/alerts.log"

# Ensure log directory exists
mkdir -p "$HOME/.shoofly/logs"
chmod 700 "$HOME/.shoofly/logs"
[[ -L "$LOG_FILE" ]] && { echo "shoofly-notify: refusing to write to symlink $LOG_FILE" >&2; exit 1; }

# ---------- helper: log to alerts.log ----------
_log() {
  local ch="$1" extra="${2:-}"
  jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg ch "$ch" --arg msg "$MSG" \
    '{"ts":$ts,"channel":$ch,"msg":$msg}' >> "$LOG_FILE"
}

# ---------- helper: desktop notification (cross-platform) ----------
_desktop_notify() {
  case "$(uname -s)" in
    Darwin)
      # macOS — python3 json.dumps for safe osascript string
      local encoded
      encoded=$(printf "%s" "$MSG" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
      osascript -e "display notification ${encoded} with title \"Shoofly Basic 🪰\"" 2>/dev/null || true
      ;;
    Linux)
      if command -v notify-send >/dev/null 2>&1; then
        notify-send "Shoofly Basic 🪰" "$MSG" 2>/dev/null || true
      fi
      ;;
    *)
      # Windows (WSL / Git Bash) — check for powershell.exe
      if command -v powershell.exe >/dev/null 2>&1; then
        printf '%s' "$MSG" | powershell.exe -Command '
          $msg = [Console]::In.ReadToEnd().Trim()
          [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
          $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
          $template.GetElementsByTagName("text")[0].AppendChild($template.CreateTextNode("Shoofly Basic"))
          $template.GetElementsByTagName("text")[1].AppendChild($template.CreateTextNode($msg))
          [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Shoofly").Show($template)
        ' 2>/dev/null || true
      fi
      ;;
  esac
}

# ---------- helper: openclaw system event ----------
_openclaw_system_event() {
  if command -v openclaw >/dev/null 2>&1; then
    openclaw system event --mode now --text "$MSG" 2>/dev/null || true
  else
    jq -n --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg msg "openclaw not in PATH, skipping system event" \
      '{"ts":$ts,"channel":"auto","note":$msg}' >> "$LOG_FILE"
  fi
}

# ---------- helper: auto-discover openclaw channels ----------
_openclaw_channels() {
  if ! command -v openclaw >/dev/null 2>&1; then
    jq -n --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg msg "openclaw not in PATH, skipping channel discovery" \
      '{"ts":$ts,"channel":"auto","note":$msg}' >> "$LOG_FILE"
    return
  fi
  [[ ! -f "$OPENCLAW_CONFIG" ]] && return

  local channels
  channels=$(jq -r '.channels // {} | to_entries[] | select(.value.enabled == true) | .key' "$OPENCLAW_CONFIG" 2>/dev/null) || return

  for ch in $channels; do
    case "$ch" in
      telegram)
        local chat_id
        chat_id=$(jq -r '.channels.telegram.chat_id // empty' "$OPENCLAW_CONFIG" 2>/dev/null) || true
        [[ -z "$chat_id" ]] && chat_id=$(jq -r '.telegram.chat_id // empty' "$CONFIG" 2>/dev/null) || true
        [[ -z "$chat_id" ]] && continue
        if [[ ! "$chat_id" =~ ^-?[0-9]+$ ]]; then
          jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg val "$chat_id" \
            '{"ts":$ts,"channel":"telegram","warn":"invalid chat_id","value":$val}' >> "$LOG_FILE"
          continue
        fi
        openclaw message send --channel telegram --target "$chat_id" --message "$MSG" 2>/dev/null || true
        ;;
      whatsapp)
        local phone
        phone=$(jq -r '.channels.whatsapp.target // empty' "$OPENCLAW_CONFIG" 2>/dev/null) || true
        [[ -z "$phone" ]] && phone=$(jq -r '.whatsapp.target // empty' "$CONFIG" 2>/dev/null) || true
        [[ -z "$phone" ]] && continue
        if [[ ! "$phone" =~ ^\+?[0-9]{7,15}$ ]]; then
          jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg val "$phone" \
            '{"ts":$ts,"channel":"whatsapp","warn":"invalid phone","value":$val}' >> "$LOG_FILE"
          continue
        fi
        openclaw message send --channel whatsapp --target "$phone" --message "$MSG" 2>/dev/null || true
        ;;
      discord)
        local channel_id
        channel_id=$(jq -r '.channels.discord.channel_id // empty' "$OPENCLAW_CONFIG" 2>/dev/null) || true
        [[ -z "$channel_id" ]] && channel_id=$(jq -r '.discord.channel_id // empty' "$CONFIG" 2>/dev/null) || true
        [[ -z "$channel_id" ]] && continue
        if [[ ! "$channel_id" =~ ^[0-9]{15,20}$ ]]; then
          jq -nc --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg val "$channel_id" \
            '{"ts":$ts,"channel":"discord","warn":"invalid channel_id","value":$val}' >> "$LOG_FILE"
          continue
        fi
        openclaw message send --channel discord --target "$channel_id" --message "$MSG" 2>/dev/null || true
        ;;
    esac
  done
}

# ---------- legacy channel handlers ----------
_legacy_telegram() {
  local bot_token chat_id
  bot_token=$(jq -r '.telegram.bot_token // empty' "$CONFIG" 2>/dev/null) || true
  chat_id=$(jq -r '.telegram.chat_id // empty' "$CONFIG" 2>/dev/null) || true
  if [[ -z "$bot_token" ]] || [[ -z "$chat_id" ]]; then
    echo "shoofly-notify: telegram.bot_token and telegram.chat_id required in $CONFIG" >&2; exit 1
  fi
  curl -s -K - <<< "url = \"https://api.telegram.org/bot${bot_token}/sendMessage\"" \
    -d "chat_id=${chat_id}" \
    --data-urlencode "text=${MSG}" > /dev/null
}

_legacy_whatsapp() {
  if [[ ! -f "$CONFIG" ]]; then echo "shoofly-notify: config file not found: $CONFIG" >&2; exit 1; fi
  local target
  target=$(jq -r '.whatsapp_number // empty' "$CONFIG" 2>/dev/null) || true
  [[ -z "$target" ]] && { echo "shoofly-notify: whatsapp_number not set in $CONFIG" >&2; exit 1; }
  command -v wacli >/dev/null && wacli send --to "$target" --message "$MSG"
}

_legacy_terminal() {
  echo "$MSG" >&2
}

_legacy_macos() {
  local encoded
  encoded=$(printf "%s" "$MSG" | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")
  osascript -e "display notification ${encoded} with title \"Shoofly Basic 🪰\"" 2>/dev/null || true
}

# =====================================================================
# Main dispatch
# =====================================================================

case "$CHANNEL" in
  auto)
    # 1. Write to all active terminals for this user — works even when spawned from launchd
    _wrote_tty=false
    local _clean_msg
    _clean_msg=$(printf '%s' "$MSG" | tr -d '\000-\037\177')
    while IFS= read -r _tty; do
      [ -w "/dev/$_tty" ] && echo "🪰 $_clean_msg" > "/dev/$_tty" 2>/dev/null && _wrote_tty=true
    done < <(who | awk -v u="$(whoami)" '$1==u && $2~/^tty/{print $2}')
    # fallback: /dev/tty (works when process has a controlling terminal)
    if [ "$_wrote_tty" = false ] && [ -w /dev/tty ]; then
      echo "🪰 $_clean_msg" > /dev/tty
    fi

    # 2. OpenClaw system event → TUI/chat
    _openclaw_system_event

    # 3. Desktop notification (cross-platform)
    _desktop_notify

    # 4. Log to alerts.log
    _log "auto"

    # 5. Auto-discover and fire OpenClaw channels
    _openclaw_channels
    ;;

  # Legacy explicit channel support
  telegram)
    _legacy_telegram
    _log "telegram"
    ;;
  whatsapp)
    _legacy_whatsapp
    _log "whatsapp"
    ;;
  terminal)
    _legacy_terminal
    _log "terminal"
    ;;
  macos)
    _legacy_macos
    _log "macos"
    ;;
  *)
    echo "Invalid channel: $CHANNEL (use 'auto' or: telegram, whatsapp, terminal, macos)" >&2
    exit 1
    ;;
esac
