#!/usr/bin/env bash
#===============================================================================
# Trend Chart Generator
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/util.sh"

DATA_DIR="$(dirname "${BASH_SOURCE[0]}")/../data"
HISTORY_DIR="$DATA_DIR/history"

# === Check jq availability ===
JQ_AVAILABLE=false
if command -v jq &>/dev/null; then
    JQ_AVAILABLE=true
fi

# === Generate Trend Chart ===
show_trend() {
    local hours="${1:-24}"
    local timestamp=$(get_timestamp)
    local date_key=$(get_date_key)
    
    local history_file="$HISTORY_DIR/${date_key}.json"
    
    echo "📈 SysGuard 趋势图表"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🕐 $timestamp | 范围: 最近 ${hours}h"
    echo ""
    
    if [[ ! -f "$history_file" ]]; then
        echo "⚠️ 暂无历史数据 (执行 'gs check' 初始化)"
        return
    fi
    
    # Use jq if available, otherwise warn
    if [[ "$JQ_AVAILABLE" == "false" ]]; then
        echo "⚠️ jq 未安装，趋势图表需要 jq 支持"
        echo "💡 安装 jq: apt install jq"
        return
    fi
    
    # Extract CPU values using jq
    echo "📊 CPU 使用率"
    local cpu_values=$(jq -r '.[].cpu.value' "$history_file" 2>/dev/null | tail -${hours})
    if [[ -z "$cpu_values" ]]; then
        echo " 暂无数据"
    else
        echo "$cpu_values" | while read -r val; do
            local bars=$((${val%%.*} / 10))
            local empty=$((10 - bars))
            printf "  %5s%% | " "$val"
            printf "█%.0s" $(seq 1 $bars 2>/dev/null) || true
            printf "░%.0s" $(seq 1 $empty 2>/dev/null) || true
            local int_val=${val%%.*}
            if [[ $int_val -ge $TH_CPU_CRIT ]]; then
                printf " 🔴\n"
            elif [[ $int_val -ge $TH_CPU_WARN ]]; then
                printf " ⚠️\n"
            else
                printf " ✅\n"
            fi
        done
    fi
    
    echo ""
    echo "📊 内存使用率"
    local mem_values=$(jq -r '.[].mem.value' "$history_file" 2>/dev/null | tail -${hours})
    if [[ -z "$mem_values" ]]; then
        echo " 暂无数据"
    else
        echo "$mem_values" | while read -r val; do
            local bars=$((${val%%.*} / 10))
            local empty=$((10 - bars))
            printf "  %5s%% | " "$val"
            printf "█%.0s" $(seq 1 $bars 2>/dev/null) || true
            printf "░%.0s" $(seq 1 $empty 2>/dev/null) || true
            if [[ $val -ge $TH_MEM_CRIT ]]; then
                printf " 🔴\n"
            elif [[ $val -ge $TH_MEM_WARN ]]; then
                printf " ⚠️\n"
            else
                printf " ✅\n"
            fi
        done
    fi
    
    echo ""
    echo "📊 Gateway 状态"
    echo "  $([ "$(check_gateway)" = "up" ] && echo '✅ 运行中' || echo '❌ 已停止') (PID: $(get_gateway_pid))"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💡 执行 'sgd' 查看详细诊断"
}

export -f show_trend
