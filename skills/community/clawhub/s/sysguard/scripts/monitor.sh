#!/usr/bin/env bash
#===============================================================================
# Monitor - Continuous Gateway Monitoring
#===============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/lib/logger.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/config.sh"
source "$(dirname "${BASH_SOURCE[0]}")/notifier.sh"

# === Run Monitor Loop ===
run_monitor() {
    log_info "Starting SysGuard monitor (interval: ${MONITOR_INTERVAL}s)"
    
    local consecutive_failures=0
    local last_notification_time=0
    
    while true; do
        local gateway_status=$(check_gateway)
        
        if [[ "$gateway_status" != "up" ]]; then
            consecutive_failures=$((consecutive_failures + 1))
            
            # Only notify once per failure period
            local now=$(date +%s)
            if [[ $consecutive_failures -ge 2 ]] && [[ $((now - last_notification_time)) -gt 300 ]]; then
                log_error "Gateway down detected (attempt $consecutive_failures)"
                
                send_notification "SysGuard 监控告警" "🚨 OpenClaw Gateway 无响应

⏰ 时间: $(get_timestamp)
🔴 状态: 连接失败

📋 可能原因:
• 进程崩溃或内存不足
• 系统负载过高

🔧 建议操作:
• 执行 'openclaw gateway restart' 重启
• 检查系统资源使用情况

💡 控制权交回给您，是否重启由您决定。"
                
                last_notification_time=$now
            fi
        else
            consecutive_failures=0
        fi
        
        sleep "$MONITOR_INTERVAL"
    done
}

# === Run as Daemon ===
run_daemon() {
    nohup "$0" monitor > /dev/null 2>&1 &
    echo $!
}

export -f run_monitor
export -f run_daemon
