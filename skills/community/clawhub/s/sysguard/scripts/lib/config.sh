#!/usr/bin/env bash
#===============================================================================
# Config Library
#===============================================================================

CONFIG_FILE="${CONFIG_DIR:-/tmp}/sysguard.conf"

# === Default Config ===
OPENCLAW_ROOT="${OPENCLAW_ROOT:-/root/.openclaw}"
BACKUP_ROOT="${BACKUP_ROOT:-/mnt/vdc/backups}"
DATA_DISK="${DATA_DISK:-/mnt/vdc}"
MONITOR_INTERVAL="${MONITOR_INTERVAL:-30}"
NOTIFY_CHANNEL="${NOTIFY_CHANNEL:-feishu}"

# === Feishu Webhook ===
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"

# === Wecom Webhook ===
WECOM_WEBHOOK_URL="${WECOM_WEBHOOK_URL:-}"

# === Thresholds ===
TH_CPU_WARN="${TH_CPU_WARN:-70}"
TH_CPU_CRIT="${TH_CPU_CRIT:-85}"
TH_MEM_WARN="${TH_MEM_WARN:-70}"
TH_MEM_CRIT="${TH_MEM_CRIT:-85}"
TH_DISK_WARN="${TH_DISK_WARN:-80}"
TH_DISK_CRIT="${TH_DISK_CRIT:-90}"

# === History Retention ===
HISTORY_RETENTION_DAYS="${HISTORY_RETENTION_DAYS:-7}"

# === Load Config File ===
load_config() {
    if [[ -f "$CONFIG_FILE" ]]; then
        while IFS='=' read -r key value; do
            [[ "$key" =~ ^#.*$ ]] && continue
            [[ -z "$key" ]] && continue
            key=$(echo "$key" | tr -d ' ')
            value=$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
            export "$key"="$value"
        done < "$CONFIG_FILE"
    fi
}

save_config() {
    cat > "$CONFIG_FILE" <<EOF
# SysGuard Configuration

OPENCLAW_ROOT=$OPENCLAW_ROOT
BACKUP_ROOT=$BACKUP_ROOT
DATA_DISK=$DATA_DISK
MONITOR_INTERVAL=$MONITOR_INTERVAL
NOTIFY_CHANNEL=$NOTIFY_CHANNEL

FEISHU_WEBHOOK_URL=$FEISHU_WEBHOOK_URL
WECOM_WEBHOOK_URL=$WECOM_WEBHOOK_URL

TH_CPU_WARN=$TH_CPU_WARN
TH_CPU_CRIT=$TH_CPU_CRIT
TH_MEM_WARN=$TH_MEM_WARN
TH_MEM_CRIT=$TH_MEM_CRIT
TH_DISK_WARN=$TH_DISK_WARN
TH_DISK_CRIT=$TH_DISK_CRIT

HISTORY_RETENTION_DAYS=$HISTORY_RETENTION_DAYS
EOF
}

# Load on source
load_config
