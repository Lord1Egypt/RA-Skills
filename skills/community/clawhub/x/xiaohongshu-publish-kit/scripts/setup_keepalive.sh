#!/bin/bash
# 小红书登录保活定时任务设置脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KEEPER_SCRIPT="$SCRIPT_DIR/login_keeper.py"

echo "🔧 设置小红书登录保活..."

# 检查脚本是否存在
if [ ! -f "$KEEPER_SCRIPT" ]; then
    echo "❌ login_keeper.py 脚本不存在: $KEEPER_SCRIPT"
    exit 1
fi

# 设置执行权限
chmod +x "$KEEPER_SCRIPT"

echo "📋 选择保活方式:"
echo "1. 添加到 crontab (推荐)"
echo "2. 启动守护进程"
echo "3. 手动测试一次"

read -p "请选择 (1-3): " choice

case $choice in
    1)
        echo "⏰ 设置 crontab 定时任务..."
        
        # 每30分钟检查一次登录状态
        CRON_CMD="*/30 * * * * cd $SCRIPT_DIR && python3 login_keeper.py --mode check >> /tmp/xiaohongshu_keepalive.log 2>&1"
        
        # 检查是否已存在相同任务
        if crontab -l 2>/dev/null | grep -q "login_keeper.py"; then
            echo "⚠️ 发现已存在的保活任务，是否替换？ (y/n)"
            read -p "> " replace
            if [ "$replace" = "y" ]; then
                # 删除旧任务，添加新任务
                (crontab -l 2>/dev/null | grep -v "login_keeper.py"; echo "$CRON_CMD") | crontab -
                echo "✅ 已更新 crontab 任务"
            else
                echo "⏭️ 跳过 crontab 设置"
            fi
        else
            # 添加新任务
            (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
            echo "✅ 已添加到 crontab"
        fi
        
        echo "📊 当前 crontab 任务:"
        crontab -l | grep login_keeper.py
        
        echo "📝 日志文件: /tmp/xiaohongshu_keepalive.log"
        ;;
        
    2)
        echo "🔄 启动守护进程模式..."
        read -p "检查间隔(分钟，默认30): " interval
        interval=${interval:-30}
        
        echo "启动守护进程，间隔 $interval 分钟..."
        python3 "$KEEPER_SCRIPT" --mode daemon --interval $interval
        ;;
        
    3)
        echo "🧪 执行一次保活测试..."
        python3 "$KEEPER_SCRIPT" --mode check
        
        echo "📋 测试完成，检查日志:"
        if [ -f "/tmp/xiaohongshu_login.log" ]; then
            tail -5 /tmp/xiaohongshu_login.log
        fi
        ;;
        
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "🎯 保活设置完成！"
echo ""
echo "💡 使用提示:"
echo "  • 查看日志: tail -f /tmp/xiaohongshu_keepalive.log"
echo "  • 手动检查: python3 $KEEPER_SCRIPT --mode check"
echo "  • 停止守护进程: pkill -f login_keeper.py"
echo "  • 删除 crontab: crontab -l | grep -v login_keeper.py | crontab -"