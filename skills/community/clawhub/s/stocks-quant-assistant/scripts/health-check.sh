#!/bin/bash
# 股票监控服务 - 健康检查

echo "🔍 股票监控服务健康检查"
echo "========================="
echo ""

# 1. 检查 LaunchAgent 状态
echo "1️⃣ LaunchAgent 状态："
LAUNCHCTL_OUTPUT=$(launchctl list | grep stock)
if [ -n "$LAUNCHCTL_OUTPUT" ]; then
    echo "   ✅ $LAUNCHCTL_OUTPUT"
else
    echo "   ❌ 未找到运行中的服务"
fi
echo ""

# 2. 检查进程状态
echo "2️⃣ 进程状态："
if pgrep -f "push_stock_report.py" > /dev/null; then
    PID=$(pgrep -f "push_stock_report.py")
    echo "   ✅ 进程运行中 (PID: $PID)"
else
    echo "   ❌ 进程未运行"
fi
echo ""

# 3. 检查日志文件
echo "3️⃣ 日志文件："
LOG_DIR="/Users/owen/.openclaw/workspace/skills/stocks-quant-assistant/logs"
if [ -d "$LOG_DIR" ]; then
    echo "   日志目录: $LOG_DIR"
    if [ -f "$LOG_DIR/launchd.log" ]; then
        LOG_SIZE=$(stat -f%z "$LOG_DIR/launchd.log" 2>/dev/null || stat -c%s "$LOG_DIR/launchd.log" 2>/dev/null)
        LOG_MTIME=$(stat -f%m "$LOG_DIR/launchd.log" 2>/dev/null || stat -c%Y "$LOG_DIR/launchd.log" 2>/dev/null)
        LOG_TIME=$(date -r "$LOG_MTIME" "+%Y-%m-%d %H:%M:%S" 2>/dev/null)
        echo "   📝 launchd.log: $(numfmt --to=iec-i --suffix=B --padding=7 $LOG_SIZE) (最后更新: $LOG_TIME)"
    else
        echo "   ⚠️  launchd.log 不存在"
    fi

    if [ -f "$LOG_DIR/launchd.err" ]; then
        ERR_SIZE=$(stat -f%z "$LOG_DIR/launchd.err" 2>/dev/null || stat -c%s "$LOG_DIR/launchd.err" 2>/dev/null)
        ERR_MTIME=$(stat -f%m "$LOG_DIR/launchd.err" 2>/dev/null || stat -c%Y "$LOG_DIR/launchd.err" 2>/dev/null)
        ERR_TIME=$(date -r "$ERR_MTIME" "+%Y-%m-%d %H:%M:%S" 2>/dev/null)
        echo "   📝 launchd.err: $(numfmt --to=iec-i --suffix=B --padding=7 $ERR_SIZE) (最后更新: $ERR_TIME)"
    else
        echo "   ⚠️  launchd.err 不存在"
    fi
else
    echo "   ❌ 日志目录不存在"
fi
echo ""

# 4. 检查配置文件
echo "4️⃣ 配置文件："
CONFIG_FILE="/Users/owen/.openclaw/workspace/skills/stocks-quant-assistant/config.local.yaml"
if [ -f "$CONFIG_FILE" ]; then
    STOCK_COUNT=$(grep -c '"code":' "$CONFIG_FILE" 2>/dev/null || echo "0")
    echo "   ✅ 配置文件存在 (使用 config.local.yaml)"
    echo "   📊 监控股票数量: $STOCK_COUNT 只"
else
    echo "   ⚠️  config.local.yaml 不存在，使用 config.yaml"
    CONFIG_FILE="/Users/owen/.openclaw/workspace/skills/stocks-quant-assistant/config.yaml"
    if [ -f "$CONFIG_FILE" ]; then
        STOCK_COUNT=$(grep -c 'code:' "$CONFIG_FILE" 2>/dev/null || echo "0")
        echo "   ✅ 配置文件存在"
        echo "   📊 监控股票数量: $STOCK_COUNT 只"
    else
        echo "   ❌ 配置文件不存在"
    fi
fi
echo ""

# 5. 检查飞书配置
echo "5️⃣ 飞书推送配置："
FEISHU_CONFIG=$(grep -A 2 "feishu:" "$CONFIG_FILE" | grep -E "app_id|app_secret|chat_id" | grep -v "^\s*#")
if [ -n "$FEISHU_CONFIG" ]; then
    echo "   ✅ 已配置飞书推送"
    echo "   📝 $FEISHU_CONFIG"
else
    echo "   ⚠️  飞书推送未配置"
    echo "   💡 运行 'python3 push_stock_report.py' 可以测试推送功能"
fi
echo ""

# 6. 下次运行时间
echo "6️⃣ 下次运行时间："
NEXT_RUN=$(launchctl list | grep stock | awk '{print $3}' | xargs launchctl print system/com.openclaw.stock-monitor 2>/dev/null)
if [ -n "$NEXT_RUN" ]; then
    echo "   ⏰ 下次运行: $NEXT_RUN"
else
    echo "   ℹ️  查看下次运行时间: launchctl print system/com.openclaw.stock-monitor"
fi
echo ""

echo "========================="
echo "✅ 健康检查完成"
