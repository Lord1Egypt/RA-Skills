#!/bin/bash
# 清理测试数据脚本（对比测试前使用）

DATA_DIR=~/.openclaw/skills/fund-monitor/data
LOGS_DIR=~/.openclaw/skills/fund-monitor/logs

echo "=== 清理测试数据 ==="
echo ""

# 停止监控
echo "1. 停止监控进程..."
pkill -f "monitor.py start" 2>/dev/null && echo "   ✅ 进程已停止" || echo "   ⚠️ 无运行进程"
rm -f $DATA_DIR/monitor.pid

# 清理数据
echo ""
echo "2. 清理数据文件..."
rm -f $DATA_DIR/trades.json && echo "   ✅ 交易记录已清理"
rm -f $DATA_DIR/signals.json && echo "   ✅ 信号历史已清理"
rm -f $DATA_DIR/watchlist.json && echo "   ✅ 监控列表已清理"

# 清理日志
echo ""
echo "3. 清理日志..."
rm -f $LOGS_DIR/monitor.log && echo "   ✅ 日志已清理"

# 保留配置
echo ""
echo "4. 保留配置文件..."
echo "   ✅ config/default.yaml 未改动"

echo ""
echo "✅ 清理完成！可以开始对比测试"
echo ""
echo "下一步:"
echo "  1. 添加基金：python3 monitor.py add 512880,513050"
echo "  2. 启动监控：python3 monitor.py start"
echo "  3. 查看状态：python3 monitor.py status"
