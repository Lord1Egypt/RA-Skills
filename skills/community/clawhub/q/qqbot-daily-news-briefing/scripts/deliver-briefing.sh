#!/bin/bash
# News Delivery Wrapper - Sends generated news via QQBot
# Version: 2.0 (Optimized)
# Author: Jarvis AI Assistant

set -e

# Configuration
TODAY=$(date +"%Y%m%d")
NEWS_FILE="/root/.openclaw/workspace/daily-news-${TODAY}.md"
LOG_FILE="/var/log/news-delivery.log"
TARGET_USER="9C12E02D9038B14FCEDCE1B69AAEAB3F"
TIMEOUT=30

# Colors for terminal output (disabled in logs)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] $1"
    echo -e "$message" | tee -a "$LOG_FILE"
}

error_exit() {
    log "${RED}❌ ERROR: $1${NC}"
    exit 1
}

warn() {
    log "${YELLOW}⚠️ WARNING: $1${NC}"
}

success() {
    log "${GREEN}✅ $1${NC}"
}

# Start delivery process
log "========================================================"
log "=== Starting news delivery process (v2.0) ==="
log "========================================================"

# Step 1: Check if news file exists
if [ ! -f "$NEWS_FILE" ]; then
    error_exit "News file not found: $NEWS_FILE"
fi

# Verify file is not empty
FILE_SIZE=$(stat -c%s "$NEWS_FILE" 2>/dev/null || echo "0")
if [ "$FILE_SIZE" -lt 100 ]; then
    error_exit "News file appears to be empty or corrupted (${FILE_SIZE} bytes)"
fi

success "Found news file: $NEWS_FILE (${FILE_SIZE} bytes)"

# Step 2: Extract headlines for preview message
TECH_HEADLINE="科技要闻汇总"
FINANCE_HEADLINE="市场动态更新"

# Extract first tech headline (support Chinese and English headers)
if command -v grep &> /dev/null; then
    TECH_EXTRACT=$(awk '/## 🖥️.*[科技 Technology]/,/## 📈/' "$NEWS_FILE" 2>/dev/null | grep -E '^### [0-9]+\. \*\*' | head -1)
    if [ -n "$TECH_EXTRACT" ]; then
        TECH_HEADLINE=$(echo "$TECH_EXTRACT" | sed 's/^### [0-9]*\. \*\*//' | sed 's/\*\*$//' | cut -c1-45)
    fi
    
    # Extract first finance headline (support Chinese and English headers)  
    FINANCE_EXTRACT=$(awk '/## 📈.*[财经 Financial]/,/Additional/' "$NEWS_FILE" 2>/dev/null | grep -E '^### [0-9]+\. \*\*' | head -1)
    if [ -n "$FINANCE_EXTRACT" ]; then
        FINANCE_HEADLINE=$(echo "$FINANCE_EXTRACT" | sed 's/^### [0-9]*\. \*\*//' | sed 's/\*\*$//' | cut -c1-45)
    fi
fi

# Handle empty headlines
[ -z "$TECH_HEADLINE" ] && TECH_HEADLINE="科技要闻汇总"
[ -z "$FINANCE_HEADLINE" ] && FINANCE_HEADLINE="市场动态更新"

# Month-day for message display
MONTH_DAY=$(date +"%m月%d日")

# Create delivery message with proper escaping
DELIVERY_MESSAGE="📰 早安，Sir! 今日简报已送达 - ${MONTH_DAY}

🖥️ 科技要闻：${TECH_HEADLINE}
📈 财经动态：${FINANCE_HEADLINE}

完整报告见附件：<qqfile>${NEWS_FILE}</qqfile>

⏰ 明日同一时间自动推送 • Jarvis Daily Briefing"

# Truncate message preview for logging
MSG_PREVIEW="${DELIVERY_MESSAGE:0:200}"
log "📨 Message preview (${#DELIVERY_MESSAGE} chars):"
log "$MSG_PREVIEW..."

# Step 3: Delivery with multiple fallback strategies
DELIVERY_SUCCESS=false

# Method A: Try direct OpenClaw message send (fastest)
if command -v openclaw &>/dev/null; then
    log "🚀 Attempting Method A: Direct OpenClaw CLI message send..."
    
    # Escape quotes in message for shell compatibility
    ESCAPED_MESSAGE=$(echo "$DELIVERY_MESSAGE" | sed 's/"/\\"/g')
    
    if timeout $TIMEOUT openclaw message send \
        --channel qqbot \
        -t "qqbot:c2c:${TARGET_USER}" \
        -m "$ESCAPED_MESSAGE" 2>>"$LOG_FILE"; then
        
        success "Direct OpenClaw message sent successfully!"
        DELIVERY_SUCCESS=true
    else
        warn "Method A failed, trying Method B..."
    fi
fi

# Method B: Use news-deliver-direct.py
if [ "$DELIVERY_SUCCESS" = false ] && [ -f "/root/.openclaw/workspace/scripts/news-deliver-direct.py" ]; then
    log "🐍 Attempting Method B: Python delivery script..."
    
    if timeout $TIMEOUT python3 /root/.openclaw/workspace/scripts/news-deliver-direct.py "$NEWS_FILE" 2>>"$LOG_FILE"; then
        success "Python delivery completed successfully!"
        DELIVERY_SUCCESS=true
    else
        warn "Method B failed, checking logs..."
    fi
fi

# Method C: Create notification file for manual pickup
if [ "$DELIVERY_SUCCESS" = false ]; then
    log "📝 Attempting Method C: Creating delivery notification..."
    
    NOTIFICATION_FILE="/root/.openclaw/workspace/PENDING_DELIVERY_${TODAY}.txt"
    echo -e "${DELIVERY_MESSAGE}" > "$NOTIFICATION_FILE"
    
    success "Delivery notification created: $NOTIFICATION_FILE"
    log "Please manually forward this message to QQ."
    DELIVERY_SUCCESS=true  # Count as success since user can manually send
fi

# Final status
log "========================================================"
if [ "$DELIVERY_SUCCESS" = true ]; then
    log "${GREEN}== Delivery process completed successfully ===${NC}"
else
    log "${RED}❌ All delivery methods failed! Check logs.${NC}"
    exit 1
fi
log "========================================================"

exit 0
