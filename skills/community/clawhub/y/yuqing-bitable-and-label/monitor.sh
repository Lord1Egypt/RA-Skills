#!/bin/bash
# 舆情同步监控工具
# 用于手动检查状态、触发修复、查看统计

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS_FILE="$SCRIPT_DIR/.sync_status.json"
LOG_FILE="$SCRIPT_DIR/sync.log"
ERROR_LOG="$SCRIPT_DIR/error.log"

show_status() {
    echo "=========================================="
    echo "  舆情数据同步状态"
    echo "=========================================="
    
    if [ -f "$STATUS_FILE" ]; then
        echo ""
        echo "📊 最近一次同步状态："
        cat "$STATUS_FILE" | python3 -m json.tool 2>/dev/null || cat "$STATUS_FILE"
    else
        echo "⚠️  暂无状态文件"
    fi
    
    echo ""
    echo "📈 统计信息："
    
    if [ -f "$LOG_FILE" ]; then
        TOTAL_RUNS=$(grep -c "开始舆情数据同步任务" "$LOG_FILE" 2>/dev/null || echo 0)
        SUCCESS_RUNS=$(grep -c "同步成功" "$LOG_FILE" 2>/dev/null || echo 0)
        FAILED_RUNS=$(grep -c "同步失败" "$LOG_FILE" 2>/dev/null || echo 0)
        
        echo "  总执行次数：$TOTAL_RUNS"
        echo "  成功次数：$SUCCESS_RUNS"
        echo "  失败次数：$FAILED_RUNS"
        
        if [ $TOTAL_RUNS -gt 0 ]; then
            SUCCESS_RATE=$(echo "scale=2; $SUCCESS_RUNS * 100 / $TOTAL_RUNS" | bc 2>/dev/null || echo "N/A")
            echo "  成功率：${SUCCESS_RATE}%"
        fi
    fi
    
    echo ""
    echo "📁 文件信息："
    ls -lh "$SCRIPT_DIR"/*.log "$SCRIPT_DIR"/.sync_status.json 2>/dev/null | awk '{print "  " $9 ": " $5}'
    
    echo ""
    echo "=========================================="
}

show_recent_logs() {
    local lines=${1:-20}
    echo "=========================================="
    echo "  最近 $lines 条日志"
    echo "=========================================="
    tail -n $lines "$LOG_FILE"
}

show_errors() {
    local lines=${1:-50}
    echo "=========================================="
    echo "  最近 $lines 条错误"
    echo "=========================================="
    if [ -f "$ERROR_LOG" ]; then
        tail -n $lines "$ERROR_LOG"
    else
        echo "暂无错误日志"
    fi
}

run_health_check() {
    echo "=========================================="
    echo "  执行健康检查"
    echo "=========================================="
    . "$SCRIPT_DIR/.env"
    
    issues=0
    
    echo -n "  Python3 环境... "
    if command -v python3 &> /dev/null; then
        echo "✅"
    else
        echo "❌"
        ((issues++))
    fi
    
    echo -n "  .env 配置文件... "
    if [ -f "$SCRIPT_DIR/.env" ]; then
        echo "✅"
    else
        echo "❌"
        ((issues++))
    fi
    
    echo -n "  主脚本文件... "
    if [ -f "$SCRIPT_DIR/excel_to_feishu_bitable.py" ]; then
        echo "✅"
    else
        echo "❌"
        ((issues++))
    fi
    
    echo -n "  飞书 Token 缓存... "
    if [ -f "$SCRIPT_DIR/.cache/tenant_token.json" ]; then
        echo "✅"
    else
        echo "⚠️  无缓存（下次会重新获取）"
    fi
    
    echo -n "  唯一键缓存... "
    if [ -f "$SCRIPT_DIR/.cache/existing_keys.json" ]; then
        CACHE_AGE=$(( $(date +%s) - $(stat -c %Y "$SCRIPT_DIR/.cache/existing_keys.json" 2>/dev/null || echo 0) ))
        if [ $CACHE_AGE -lt 300 ]; then
            echo "✅ (有效)"
        else
            echo "⚠️  已过期 (${CACHE_AGE}s)"
        fi
    else
        echo "⚠️  无缓存"
    fi
    
    echo -n "  锁文件... "
    if [ -f "$SCRIPT_DIR/.sync.lock" ]; then
        LOCK_AGE=$(( $(date +%s) - $(stat -c %Y "$SCRIPT_DIR/.sync.lock" 2>/dev/null || echo 0) ))
        if [ $LOCK_AGE -gt 600 ]; then
            echo "⚠️  死锁 (${LOCK_AGE}s)，可清理"
        else
            echo "🔒 正常锁定中 (${LOCK_AGE}s)"
        fi
    else
        echo "✅"
    fi
    
    echo ""
    if [ $issues -gt 0 ]; then
        echo "❌ 发现 $issues 个问题"
    else
        echo "✅ 健康检查通过"
    fi
}

run_fix() {
    echo "=========================================="
    echo "  执行自动修复"
    echo "=========================================="
    
    fixed=0
    
    # 清理 Python 缓存
    if [ -d "$SCRIPT_DIR/__pycache__" ]; then
        echo -n "  清理 Python 缓存... "
        rm -rf "$SCRIPT_DIR/__pycache__"
        echo "✅"
        ((fixed++))
    fi
    
    # 清理死锁
    if [ -f "$SCRIPT_DIR/.sync.lock" ]; then
        LOCK_AGE=$(( $(date +%s) - $(stat -c %Y "$SCRIPT_DIR/.sync.lock" 2>/dev/null || echo 0) ))
        if [ $LOCK_AGE -gt 600 ]; then
            echo -n "  清理死锁文件... "
            rm -f "$SCRIPT_DIR/.sync.lock"
            echo "✅"
            ((fixed++))
        fi
    fi
    
    # 清理旧缓存
    if [ -d "$SCRIPT_DIR/.cache" ]; then
        echo -n "  清理过期缓存... "
        find "$SCRIPT_DIR/.cache" -type f -mmin +60 -delete 2>/dev/null
        echo "✅"
        ((fixed++))
    fi
    
    # 日志轮转
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(stat -c%s "$LOG_FILE" 2>/dev/null || echo 0)
        if [ $LOG_SIZE -gt 10485760 ]; then
            echo -n "  日志文件轮转... "
            mv "$LOG_FILE" "$LOG_FILE.$(date +%Y%m%d%H%M%S)"
            touch "$LOG_FILE"
            echo "✅"
            ((fixed++))
        fi
    fi
    
    echo ""
    if [ $fixed -gt 0 ]; then
        echo "✅ 完成 $fixed 项修复"
    else
        echo "ℹ️  无需修复"
    fi
}

run_sync_now() {
    echo "=========================================="
    echo "  手动执行同步"
    echo "=========================================="
    bash "$SCRIPT_DIR/sync.sh"
}

reset_status() {
    echo "=========================================="
    echo "  重置状态"
    echo "=========================================="
    rm -f "$STATUS_FILE" "$SCRIPT_DIR/.sync.lock"
    echo "✅ 状态已重置"
}

show_help() {
    echo "=========================================="
    echo "  舆情同步监控工具"
    echo "=========================================="
    echo ""
    echo "用法：$0 <命令>"
    echo ""
    echo "命令:"
    echo "  status      查看同步状态（默认）"
    echo "  logs [n]    查看最近 n 条日志（默认 20）"
    echo "  errors [n]  查看最近 n 条错误（默认 50）"
    echo "  health      执行健康检查"
    echo "  fix         执行自动修复"
    echo "  run         手动执行同步"
    echo "  reset       重置状态"
    echo "  help        显示帮助"
    echo ""
    echo "示例:"
    echo "  $0 status"
    echo "  $0 logs 50"
    echo "  $0 health"
    echo "  $0 fix && $0 run"
    echo ""
}

# 主逻辑
case "${1:-status}" in
    status)
        show_status
        ;;
    logs)
        show_recent_logs "${2:-20}"
        ;;
    errors)
        show_errors "${2:-50}"
        ;;
    health)
        run_health_check
        ;;
    fix)
        run_fix
        ;;
    run)
        run_sync_now
        ;;
    reset)
        reset_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令：$1"
        show_help
        exit 1
        ;;
esac
