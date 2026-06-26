#!/bin/bash
# 系统监控脚本 - Linux 版本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISTORY_DIR="$SCRIPT_DIR/../history"
CONFIG_FILE="$HOME/.openclaw/skills/config/skill-system-monitor/config.json"

# 检查依赖
if ! command -v bc &> /dev/null; then
    echo "❌ 错误: 缺少依赖 'bc'，请安装: apt install bc -y"
    exit 1
fi
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M")
DATE=$(date "+%Y-%m-%d %H:%M:%S")
HOSTNAME=$(hostname)

# 默认配置
DISK_WARNING=70
DISK_CRITICAL=85
MEM_WARNING=70
MEM_CRITICAL=85
MONITOR_DISK=true
MONITOR_MEMORY=true
MONITOR_CPU=true
MONITOR_DOCKER=true
MONITOR_SERVICES=true
TOP_PROCESSES=5

# 读取配置（如果存在）
if [ -f "$CONFIG_FILE" ]; then
    # 简单解析 JSON 配置
    if grep -q '"disk"[[:space:]]*:[[:space:]]*false' "$CONFIG_FILE"; then MONITOR_DISK=false; fi
    if grep -q '"memory"[[:space:]]*:[[:space:]]*false' "$CONFIG_FILE"; then MONITOR_MEMORY=false; fi
    if grep -q '"cpu"[[:space:]]*:[[:space:]]*false' "$CONFIG_FILE"; then MONITOR_CPU=false; fi
    if grep -q '"docker"[[:space:]]*:[[:space:]]*false' "$CONFIG_FILE"; then MONITOR_DOCKER=false; fi
    if grep -q '"services"[[:space:]]*:[[:space:]]*false' "$CONFIG_FILE"; then MONITOR_SERVICES=false; fi
    
    # 读取阈值
    DW=$(grep -A1 '"disk"' "$CONFIG_FILE" | grep '"warning"' | grep -o '[0-9]*' | head -1)
    DC=$(grep -A1 '"disk"' "$CONFIG_FILE" | grep '"critical"' | grep -o '[0-9]*' | head -1)
    MW=$(grep -A1 '"memory"' "$CONFIG_FILE" | grep '"warning"' | grep -o '[0-9]*' | head -1)
    MC=$(grep -A1 '"memory"' "$CONFIG_FILE" | grep '"critical"' | grep -o '[0-9]*' | head -1)
    
    [ -n "$DW" ] && DISK_WARNING=$DW
    [ -n "$DC" ] && DISK_CRITICAL=$DC
    [ -n "$MW" ] && MEM_WARNING=$MW
    [ -n "$MC" ] && MEM_CRITICAL=$MC
fi

# 硬盘信息
DISK_INFO=$(df -h / | tail -1)
DISK_TOTAL=$(echo $DISK_INFO | awk '{print $2}')
DISK_USED=$(echo $DISK_INFO | awk '{print $3}')
DISK_AVAIL=$(echo $DISK_INFO | awk '{print $4}')
DISK_PERCENT=$(echo $DISK_INFO | awk '{print $5}' | tr -d '%')

# 内存信息
MEM_INFO=$(free -m | grep Mem)
MEM_TOTAL=$(echo $MEM_INFO | awk '{printf "%.0f", $2/1024}')
MEM_USED=$(echo $MEM_INFO | awk '{printf "%.0f", $3/1024}')
MEM_AVAIL=$(echo $MEM_INFO | awk '{printf "%.0f", $7/1024}')
MEM_PERCENT=$(echo $MEM_INFO | awk '{printf "%.0f", ($3/$2)*100}')

# Swap 信息
SWAP_INFO=$(free -m | grep Swap)
SWAP_TOTAL=$(echo $SWAP_INFO | awk '{printf "%.0f", $2/1024}')
SWAP_USED=$(echo $SWAP_INFO | awk '{printf "%.0f", $3/1024}')

# CPU 负载
LOAD_AVG=$(cat /proc/loadavg)
LOAD_1=$(echo $LOAD_AVG | awk '{print $1}')
LOAD_5=$(echo $LOAD_AVG | awk '{print $2}')
LOAD_15=$(echo $LOAD_AVG | awk '{print $3}')
CPU_CORES=$(nproc)

# 系统运行时间
UPTIME=$(uptime -p 2>/dev/null || uptime | awk -F'up ' '{print $2}' | awk -F',' '{print $1}')

# 网络流量
NET_INFO=$(cat /proc/net/dev | grep -E "eth0|ens" | head -1)
NET_RX=$(echo $NET_INFO | awk '{printf "%.1f", $2/1024/1024}')
NET_TX=$(echo $NET_INFO | awk '{printf "%.1f", $10/1024/1024}')

# 磁盘 I/O
if command -v iostat &> /dev/null; then
    DISK_IO=$(iostat -x 1 1 2>/dev/null | grep -A1 "Device" | tail -1 | awk '{printf "读: %.0f/s, 写: %.0f/s, 利用率: %.1f%%", $4, $8, $14}')
else
    DISK_IO="未安装 sysstat"
fi

# 判断状态
get_disk_status() {
    local percent=$1
    if [ $percent -lt $DISK_WARNING ]; then echo "✅正常"
    elif [ $percent -lt $DISK_CRITICAL ]; then echo "⚠️警告"
    else echo "🔴危险"; fi
}

get_mem_status() {
    local percent=$1
    if [ $percent -lt $MEM_WARNING ]; then echo "✅正常"
    elif [ $percent -lt $MEM_CRITICAL ]; then echo "⚠️警告"
    else echo "🔴危险"; fi
}

get_cpu_status() {
    local load=$1
    local cores=$CPU_CORES
    local double_cores=$(echo "$cores * 2" | bc)
    
    if (( $(echo "$load < $cores" | bc -l) )); then echo "✅正常"
    elif (( $(echo "$load < $double_cores" | bc -l) )); then echo "⚠️警告"
    else echo "🔴危险"; fi
}

DISK_STATUS=$(get_disk_status $DISK_PERCENT)
MEM_STATUS=$(get_mem_status $MEM_PERCENT)
CPU_STATUS=$(get_cpu_status $LOAD_1)

# TOP 5 内存进程
TOP_PROCESSES_OUTPUT=$(ps aux --sort=-%mem | head -6 | tail -5 | awk '{printf "%-25s %6s (%s%%)\n", substr($11,1,25), $6/1024"M", $4}')

# Docker 容器状态
if [ "$MONITOR_DOCKER" = "true" ] && command -v docker &> /dev/null; then
    DOCKER_RUNNING=$(docker ps -q 2>/dev/null | wc -l)
    DOCKER_STOPPED=$(docker ps -a --filter "status=exited" -q 2>/dev/null | wc -l)
    DOCKER_INFO="运行: $DOCKER_RUNNING, 停止: $DOCKER_STOPPED"
else
    DOCKER_INFO="未安装或已禁用"
fi

# 关键服务状态
check_service() {
    local name=$1
    local status=$(systemctl is-active $name 2>/dev/null)
    if [ "$status" = "active" ]; then echo "✅"
    elif [ "$status" = "inactive" ]; then echo "❌"
    else echo "❓"; fi
}

check_process() {
    local pattern=$1
    if pgrep -f "$pattern" > /dev/null 2>&1; then echo "✅"
    else echo "❌"; fi
}

SERVICES_STATUS=""
if [ "$MONITOR_SERVICES" = "true" ]; then
    SERVICE_MONGODB=$(check_service mongod)
    SERVICE_MYSQL=$(check_service mysql)
    SERVICE_POSTGRES=$(check_service postgresql)
    SERVICE_DOCKER=$(check_service docker)
    SERVICE_NGINX=$(check_service nginx)
    SERVICE_OPENCLAW=$(check_process "clawdbot-gateway")
    SERVICES_STATUS="MongoDB: $SERVICE_MONGODB | MySQL: $SERVICE_MYSQL | PostgreSQL: $SERVICE_POSTGRES
Docker: $SERVICE_DOCKER | Nginx: $SERVICE_NGINX | OpenClaw: $SERVICE_OPENCLAW"
fi

# 预警信息
WARNINGS=""
if [ $DISK_PERCENT -ge $DISK_CRITICAL ]; then
    WARNINGS="${WARNINGS}🔴 硬盘使用率过高 (${DISK_PERCENT}%)\n"
elif [ $DISK_PERCENT -ge $DISK_WARNING ]; then
    WARNINGS="${WARNINGS}⚠️ 硬盘使用率偏高 (${DISK_PERCENT}%)\n"
fi

if [ $MEM_PERCENT -ge $MEM_CRITICAL ]; then
    WARNINGS="${WARNINGS}🔴 内存使用率过高 (${MEM_PERCENT}%)\n"
elif [ $MEM_PERCENT -ge $MEM_WARNING ]; then
    WARNINGS="${WARNINGS}⚠️ 内存使用率偏高 (${MEM_PERCENT}%)\n"
fi

DOUBLE_CORES=$(echo "$CPU_CORES * 2" | bc)
if (( $(echo "$LOAD_1 > $DOUBLE_CORES" | bc -l) )); then
    WARNINGS="${WARNINGS}🔴 CPU 负载过高 (${LOAD_1})\n"
fi

# 生成报告
REPORT="📊 系统监控报告 (Linux)
==================
主机: $HOSTNAME
时间: $DATE
运行时间: $UPTIME"

if [ "$MONITOR_DISK" = "true" ]; then
REPORT="$REPORT

💾 硬盘状态
总容量: ${DISK_TOTAL} | 已用: ${DISK_USED} (${DISK_PERCENT}%) | 可用: ${DISK_AVAIL}
状态: $DISK_STATUS"
fi

if [ "$MONITOR_MEMORY" = "true" ]; then
REPORT="$REPORT

🧠 内存状态
总内存: ${MEM_TOTAL}G | 已用: ${MEM_USED}G (${MEM_PERCENT}%) | 可用: ${MEM_AVAIL}G
Swap: ${SWAP_USED}G/${SWAP_TOTAL}G
状态: $MEM_STATUS"
fi

if [ "$MONITOR_CPU" = "true" ]; then
REPORT="$REPORT

⚙️ CPU 负载 (${CPU_CORES}核)
1分钟: $LOAD_1 | 5分钟: $LOAD_5 | 15分钟: $LOAD_15
状态: $CPU_STATUS"
fi

REPORT="$REPORT

🌐 网络流量
接收: ${NET_RX} MB | 发送: ${NET_TX} MB

💿 磁盘 I/O
$DISK_IO"

if [ "$MONITOR_DOCKER" = "true" ]; then
REPORT="$REPORT

🐳 Docker 容器
$DOCKER_INFO"
fi

if [ "$MONITOR_SERVICES" = "true" ] && [ -n "$SERVICES_STATUS" ]; then
REPORT="$REPORT

🔧 关键服务
$SERVICES_STATUS"
fi

if [ "$TOP_PROCESSES" -gt 0 ]; then
REPORT="$REPORT

🔴 资源占用 TOP $TOP_PROCESSES (内存)
$TOP_PROCESSES_OUTPUT"
fi

if [ -n "$WARNINGS" ]; then
REPORT="$REPORT

⚠️ 预警信息
$WARNINGS"
fi

# 保存历史记录
mkdir -p "$HISTORY_DIR"
echo "$REPORT" > "$HISTORY_DIR/${TIMESTAMP}.log"

# 保存 JSON
cat > "$HISTORY_DIR/${TIMESTAMP}.json" << EOF
{
  "timestamp": "$DATE",
  "system": "linux",
  "uptime": "$UPTIME",
  "disk": {
    "total": "$DISK_TOTAL",
    "used": "$DISK_USED",
    "available": "$DISK_AVAIL",
    "percent": $DISK_PERCENT
  },
  "memory": {
    "total_mb": $(echo $MEM_INFO | awk '{print $2}'),
    "used_mb": $(echo $MEM_INFO | awk '{print $3}'),
    "available_mb": $(echo $MEM_INFO | awk '{print $7}'),
    "percent": $MEM_PERCENT,
    "swap_used_mb": $(echo $SWAP_INFO | awk '{print $3}'),
    "swap_total_mb": $(echo $SWAP_INFO | awk '{print $2}')
  },
  "cpu": {
    "load_1": $LOAD_1,
    "load_5": $LOAD_5,
    "load_15": $LOAD_15,
    "cores": $CPU_CORES
  },
  "network": {
    "rx_mb": $NET_RX,
    "tx_mb": $NET_TX
  },
  "docker": {
    "running": $DOCKER_RUNNING,
    "stopped": $DOCKER_STOPPED
  }
}
EOF

echo "$REPORT"
