#!/usr/bin/env bash
#===============================================================================
# Notifier - Multi-channel Notification
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"

# === Send Feishu Notification ===
notify_feishu() {
    local title="$1"
    local message="$2"
    local webhook="${FEISHU_WEBHOOK_URL:-}"
    
    if [[ -z "$webhook" ]]; then
        log_warn "Feishu webhook not configured"
        return 1
    fi
    
    local payload=$(cat <<EOF
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "🤖 $title"},
      "color": "red"
    },
    "elements": [
      {
        "tag": "div",
        "text": {"tag": "lark_md", "content": "$message"}
      },
      {
        "tag": "hr"
      },
      {
        "tag": "note",
        "elements": [
          {"tag": "plain_text", "content": "来自 SysGuard 系统"}
        ]
      }
    ]
  }
}
EOF
)
    
    curl -s -X POST "$webhook" \
        -H "Content-Type: application/json" \
        -d "$payload" > /dev/null 2>&1
    
    log_info "Feishu notification sent: $title"
}

# === Send Wecom Notification ===
notify_wecom() {
    local title="$1"
    local message="$2"
    local webhook="${WECOM_WEBHOOK_URL:-}"
    
    if [[ -z "$webhook" ]]; then
        log_warn "Wecom webhook not configured"
        return 1
    fi
    
    local payload=$(cat <<EOF
{
  "msgtype": "markdown",
  "markdown": {
    "content": "**🤖 $title**\n> $message\n\n---\n> _来自 SysGuard 系统_"
  }
}
EOF
)
    
    curl -s -X POST "$webhook" \
        -H "Content-Type: application/json" \
        -d "$payload" > /dev/null 2>&1
    
    log_info "Wecom notification sent: $title"
}

# === Main Send Function ===
send_notification() {
    local title="${1:-SysGuard Alert}"
    local message="${2:-Test message from SysGuard}"
    
    case "$NOTIFY_CHANNEL" in
        feishu)
            notify_feishu "$title" "$message"
            ;;
        wecom)
            notify_wecom "$title" "$message"
            ;;
        both)
            notify_feishu "$title" "$message"
            notify_wecom "$title" "$message"
            ;;
        *)
            echo "[$NOTIFY_CHANNEL] $title: $message"
            ;;
    esac
}

export -f send_notification
