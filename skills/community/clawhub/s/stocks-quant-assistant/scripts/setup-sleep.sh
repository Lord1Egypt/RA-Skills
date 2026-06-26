#!/bin/bash
# 股票监控服务 - 系统睡眠配置
# 确保定时任务执行时系统不会进入睡眠

echo "🔧 配置系统睡眠设置..."

# 1. 禁用自动休眠（显示器关闭）
sudo pmset -a womp 0
echo "✅ 已禁用自动休眠"

# 2. 禁用电源节省
sudo pmset -a powersave 0
echo "✅ 已禁用电源节省"

# 3. 启用自动重启（系统崩溃时）
sudo pmset -a autorestart 1
echo "✅ 已启用自动重启"

# 4. 查看当前设置
echo ""
echo "📊 当前睡眠设置："
pmset -g assertions | grep -i "prevent sleep"
echo ""
echo "✅ 配置完成！"
echo ""
echo "💡 提示："
echo "- 如果需要恢复默认设置，运行: sudo pmset -a womp 1 && sudo pmset -a powersave 1"
echo "- 查看详细设置: pmset -g assertions"
