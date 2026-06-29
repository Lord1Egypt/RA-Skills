#!/bin/bash
#===============================================
# OpenClaw Server Guardian - Health Check
# 检测服务器健康状态 & Bot连接状态
#===============================================

set -uo pipefail

# --- 速率限制：每60秒最多运行1次 ---
RATE_LIMIT_FILE="/tmp/guardian_rate_limit.json"
RATE_WINDOW=60

check_rate_limit() {
    local now=$(date +%s)
    local cutoff=$((now - RATE_WINDOW))
    local timestamps=""
    if [[ -f "$RATE_LIMIT_FILE" ]]; then
        timestamps=$(cat "$RATE_LIMIT_FILE" 2>/dev/null | tr -d '[]' | tr ',' '\n' | grep -v '^$' | sort -n)
    fi
    # 过滤60秒内的记录
    local recent=$(echo "$timestamps" | awk -v c="$cutoff" '$1 > c' | wc -l)
    if [[ "$recent" -ge 40 ]]; then
        echo "⚠ 健康检测触发速率限制（每分钟最多40次），请稍后再试喵"
        exit 0
    fi
    # 写入当前时间戳
    echo "$now," >> "$RATE_LIMIT_FILE"
    # 清理过期记录
    if [[ -f "$RATE_LIMIT_FILE" ]]; then
        local tmp=$(mktemp)
        awk -v c="$cutoff" '$1 > c' "$RATE_LIMIT_FILE" > "$tmp" && mv "$tmp" "$RATE_LIMIT_FILE"
    fi
}

check_rate_limit

# --- 颜色 ---
RED='\033[0;31m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m'

report() {
  echo "[$(date '+%H:%M:%S')] $1"
}

# 获取实际 Gateway PID（匹配 node 进程，排除自身）
SCRIPT_PID=$$
get_gateway_pid() {
    pgrep -f "openclaw/dist/index.js" 2>/dev/null | grep -v "$SCRIPT_PID" | head -1 || true
}
GATEWAY_PID=$(get_gateway_pid)

# ========== 1. 系统基础指标 ==========
report "=== 系统基础指标 ==="

# CPU 负载
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
CPU_CORES=$(nproc)
LOAD_INT=$(echo "$LOAD" | cut -d. -f1)
if [ "$LOAD_INT" -gt $((CPU_CORES * 2)) ]; then
  echo -e "${RED}⚠ CPU过载: $LOAD (核心数: $CPU_CORES)${NC}"
  CPU_STATUS="CRITICAL"
elif [ "$LOAD_INT" -gt $CPU_CORES ]; then
  echo -e "${YELLOW}⚠ CPU较高: $LOAD${NC}"
  CPU_STATUS="WARN"
else
  echo -e "${GREEN}✓ CPU正常: $LOAD${NC}"
  CPU_STATUS="OK"
fi

# 内存使用
MEM_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
MEM_USED=$(free -m | awk '/^Mem:/ {print $3}')
MEM_PCT=$((MEM_USED * 100 / MEM_TOTAL))
if [ "$MEM_PCT" -gt 90 ]; then
  echo -e "${RED}⚠ 内存告警: 使用${MEM_PCT}% ($MEM_USED/${MEM_TOTAL}MB)${NC}"
  MEM_STATUS="CRITICAL"
elif [ "$MEM_PCT" -gt 75 ]; then
  echo -e "${YELLOW}⚠ 内存偏高: ${MEM_PCT}%${NC}"
  MEM_STATUS="WARN"
else
  echo -e "${GREEN}✓ 内存正常: ${MEM_PCT}%${NC}"
  MEM_STATUS="OK"
fi

# 磁盘使用
DISK_PCT=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_PCT" -gt 90 ]; then
  echo -e "${RED}⚠ 磁盘告警: 使用${DISK_PCT}%${NC}"
  DISK_STATUS="CRITICAL"
elif [ "$DISK_PCT" -gt 80 ]; then
  echo -e "${YELLOW}⚠ 磁盘偏高: ${DISK_PCT}%${NC}"
  DISK_STATUS="WARN"
else
  echo -e "${GREEN}✓ 磁盘正常: ${DISK_PCT}%${NC}"
  DISK_STATUS="OK"
fi

# ========== 2. OpenClaw 进程状态 ==========
report "=== OpenClaw 进程状态 ==="

if [ -n "$GATEWAY_PID" ] && [ "$GATEWAY_PID" -gt 0 ] 2>/dev/null; then
  GATEWAY_MEM=$(ps -o rss= -p "$GATEWAY_PID" 2>/dev/null || echo 0)
  GATEWAY_MEM_MB=$((GATEWAY_MEM / 1024))
  GATEWAY_CPU=$(ps -o %cpu= -p "$GATEWAY_PID" 2>/dev/null || echo 0)
  echo -e "${GREEN}✓ Gateway 运行中 (PID: $GATEWAY_PID, CPU: ${GATEWAY_CPU}%, MEM: ${GATEWAY_MEM_MB}MB)${NC}"
  GATEWAY_STATUS="OK"
else
  echo -e "${RED}✗ Gateway 未运行！${NC}"
  GATEWAY_STATUS="DOWN"
fi

# Bot 进程（排除 Gateway 和自身）
BOT_COUNT=$(pgrep -f "openclaw" 2>/dev/null | grep -v "$SCRIPT_PID" | grep -v "$GATEWAY_PID" | wc -l)
if [ "$BOT_COUNT" -gt 0 ]; then
  echo -e "${GREEN}✓ OpenClaw 子进程数: $BOT_COUNT${NC}"
  BOT_STATUS="OK"
else
  echo -e "${YELLOW}⚠ 未检测到 OpenClaw 子进程${NC}"
  BOT_STATUS="UNKNOWN"
fi

# ========== 3. 网络连接状态 ==========
report "=== 网络连接状态 ==="

# Gateway API 端口
GW_PORT="20447"
if curl -s --max-time 3 http://127.0.0.1:20447/health >/dev/null 2>&1; then
  echo -e "${GREEN}✓ Gateway API 端口 $GW_PORT 可达${NC}"
  API_STATUS="OK"
else
  echo -e "${RED}✗ Gateway API 端口 $GW_PORT 不通${NC}"
  API_STATUS="DOWN"
fi

# 频道插件连接状态
CHANNEL_PING=$(curl -s --max-time 3 http://127.0.0.1:20447/health 2>/dev/null || echo "offline")
if [ "$CHANNEL_PING" != "offline" ]; then
  echo -e "${GREEN}✓ Gateway HTTP 健康检查通过${NC}"
  HTTP_STATUS="OK"
else
  echo -e "${YELLOW}⚠ Gateway HTTP 健康检查失败${NC}"
  HTTP_STATUS="WARN"
fi

# ========== 4. 日志异常检测 ==========
report "=== 最近日志异常 ==="

LOG_FILE="${LOG_FILE:-$(find /tmp/openclaw /root/.openclaw/logs /var/log/openclaw -name "*.log" 2>/dev/null | head -1)}"
if [[ -n "$LOG_FILE" ]] && [[ -f "$LOG_FILE" ]]; then
  ERRORS=$(tail -n 500 "$LOG_FILE" 2>/dev/null | grep -cE "(ERROR|FATAL|CRITICAL)" || true)
  WARNS=$(tail -n 500 "$LOG_FILE" 2>/dev/null | grep -cE "(WARN|warning)" || true)
  if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}⚠ 日志中发现 $ERRORS 个 ERROR${NC}"
    echo -e "${RED}  最近错误示例:${NC}"
    tail -n 100 "$LOG_FILE" | grep -E "(ERROR|FATAL)" | tail -3 | sed 's/^/    /'
    LOG_STATUS="CRITICAL"
  elif [ "$WARNS" -gt 5 ]; then
    echo -e "${YELLOW}⚠ 日志中发现 $WARNS 个 WARN${NC}"
    LOG_STATUS="WARN"
  else
    echo -e "${GREEN}✓ 日志无明显异常${NC}"
    LOG_STATUS="OK"
  fi
else
  echo -e "${YELLOW}⚠ 未找到日志文件${NC}"
  LOG_STATUS="UNKNOWN"
fi
report "=== 崩溃/重启历史 ==="

CRASH_COUNT=$(journalctl -u openclaw --since "1 hour ago" 2>/dev/null | grep -cE "(SIGSEGV|SIGABRT|segfault|crash)" || true)
if [ "$CRASH_COUNT" -gt 0 ]; then
  echo -e "${RED}⚠ 最近1小时检测到 $CRASH_COUNT 次崩溃！${NC}"
  CRASH_STATUS="CRITICAL"
else
  echo -e "${GREEN}✓ 最近1小时无崩溃记录${NC}"
  CRASH_STATUS="OK"
fi

# ========== 汇总 ==========
report "=== 健康汇总 ==="

CRITICAL_COUNT=0
WARN_COUNT=0

[ "$CPU_STATUS" = "CRITICAL" ] && ((CRITICAL_COUNT++)) || true
[ "$MEM_STATUS" = "CRITICAL" ] && ((CRITICAL_COUNT++)) || true
[ "$DISK_STATUS" = "CRITICAL" ] && ((CRITICAL_COUNT++)) || true
[ "$GATEWAY_STATUS" = "DOWN" ] && ((CRITICAL_COUNT++)) || true
[ "$LOG_STATUS" = "CRITICAL" ] && ((CRITICAL_COUNT++)) || true
[ "$CRASH_STATUS" = "CRITICAL" ] && ((CRITICAL_COUNT++)) || true

[ "$CPU_STATUS" = "WARN" ] && ((WARN_COUNT++)) || true
[ "$MEM_STATUS" = "WARN" ] && ((WARN_COUNT++)) || true
[ "$DISK_STATUS" = "WARN" ] && ((WARN_COUNT++)) || true
[ "$API_STATUS" = "DOWN" ] && ((CRITICAL_COUNT++)) || true
[ "$HTTP_STATUS" = "WARN" ] && ((WARN_COUNT++)) || true
[ "$LOG_STATUS" = "WARN" ] && ((WARN_COUNT++)) || true
[ "$BOT_STATUS" = "DOWN" ] && ((CRITICAL_COUNT++)) || true

if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo -e "${RED}🚨 严重问题: $CRITICAL_COUNT 项 | 警告: $WARN_COUNT 项 → 需要干预${NC}"
  exit 2
elif [ "$WARN_COUNT" -gt 0 ]; then
  echo -e "${YELLOW}⚠ 需要关注: 警告 $WARN_COUNT 项${NC}"
  exit 1
else
  echo -e "${GREEN}✅ 服务器状态正常${NC}"
  exit 0
fi
