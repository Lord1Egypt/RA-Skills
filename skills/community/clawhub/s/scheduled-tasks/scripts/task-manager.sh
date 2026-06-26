#!/bin/bash
# 定时任务创建助手 - 交互式脚本
# 用法: bash create-task.sh
# 帮助 Agent 快速创建定时任务，避免踩坑

set -e

echo "========================================"
echo "  OpenClaw 定时任务创建助手"
echo "========================================"
echo ""

# 检查 openclaw 命令
if ! command -v openclaw &> /dev/null; then
    echo "❌ openclaw 命令未找到"
    echo "请确认 PATH 包含 openclaw 路径"
    exit 1
fi

# 参数
ACTION="${1:-help}"

case "$ACTION" in
    list)
        echo "📋 当前定时任务列表："
        echo ""
        openclaw cron list 2>&1
        echo ""
        echo "📋 系统 Crontab："
        crontab -l 2>/dev/null || echo "(无)"
        ;;

    test)
        JOB_ID="$2"
        if [ -z "$JOB_ID" ]; then
            echo "❌ 用法: $0 test <jobId>"
            exit 1
        fi
        echo "🧪 手动触发任务: $JOB_ID"
        openclaw cron run "$JOB_ID" 2>&1
        echo ""
        echo "📋 运行历史:"
        openclaw cron runs --id "$JOB_ID" --limit 5 2>&1
        ;;

    history)
        JOB_ID="$2"
        LIMIT="${3:-10}"
        if [ -z "$JOB_ID" ]; then
            echo "❌ 用法: $0 history <jobId> [limit]"
            exit 1
        fi
        echo "📋 任务 $JOB_ID 运行历史 (最近 $LIMIT 条):"
        openclaw cron runs --id "$JOB_ID" --limit "$LIMIT" 2>&1
        ;;

    check)
        echo "🔍 定时任务健康检查"
        echo ""
        
        # 检查 Gateway
        echo "1. Gateway 状态："
        openclaw gateway status 2>&1 || echo "⚠️ Gateway 未运行"
        echo ""
        
        # 检查 cron 服务
        echo "2. 系统 cron 服务："
        systemctl is-active cron 2>/dev/null && echo "✅ 运行中" || echo "⚠️ 未运行"
        echo ""
        
        # 检查时区
        echo "3. 系统时区："
        timedatectl 2>/dev/null | grep "Time zone" || date +%Z
        echo ""
        
        # 列出所有任务
        echo "4. OpenClaw Cron 任务："
        openclaw cron list 2>&1 || echo "(无)"
        echo ""
        
        echo "5. 系统 Crontab："
        crontab -l 2>/dev/null || echo "(无)"
        ;;

    help|*)
        echo "用法: $0 <command> [args]"
        echo ""
        echo "命令:"
        echo "  list              查看所有定时任务"
        echo "  test <jobId>      手动触发并查看结果"
        echo "  history <jobId>   查看运行历史"
        echo "  check             健康检查"
        echo "  help              显示帮助"
        ;;
esac
