#!/bin/bash

# 小红书自动互动技能安装测试脚本

echo "=== 小红书自动互动技能安装测试 ==="
echo "测试时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 检查脚本文件
echo "1. 检查脚本文件..."
if [ -f "scripts/xhs_interaction_simple_fixed.sh" ]; then
    echo "✅ 脚本文件存在"
    chmod +x "scripts/xhs_interaction_simple_fixed.sh"
    echo "✅ 脚本已赋予执行权限"
else
    echo "❌ 脚本文件不存在"
    exit 1
fi

# 2. 检查依赖工具
echo ""
echo "2. 检查依赖工具..."
for tool in curl jq; do
    if command -v $tool &> /dev/null; then
        echo "✅ $tool 已安装"
    else
        echo "❌ $tool 未安装"
    fi
done

# 3. 检查MCP服务
echo ""
echo "3. 检查MCP服务..."
if curl -s http://localhost:18060/mcp > /dev/null; then
    echo "✅ MCP服务正在运行"
else
    echo "⚠️  MCP服务未运行或无法访问"
    echo "   请确保小红书MCP服务已启动"
fi

# 4. 检查cron任务
echo ""
echo "4. 检查cron任务..."
CRON_COUNT=$(crontab -l | grep -c "xhs_interaction_simple_fixed.sh")
if [ "$CRON_COUNT" -gt 0 ]; then
    echo "✅ cron任务已配置 ($CRON_COUNT 个任务)"
    crontab -l | grep "xhs_interaction_simple_fixed.sh"
else
    echo "⚠️  cron任务未配置"
    echo "   请运行以下命令配置cron："
    echo "   crontab -e"
    echo "   添加：31 12,14,16,18,20 * * * bash /home/chan/.openclaw/workspace/xhs_interaction_simple_fixed.sh >> /home/chan/.openclaw/workspace/xhs_interaction.log 2>&1"
fi

# 5. 检查工作空间文件
echo ""
echo "5. 检查工作空间文件..."
WORKSPACE_SCRIPT="/home/chan/.openclaw/workspace/xhs_interaction_simple_fixed.sh"
if [ -f "$WORKSPACE_SCRIPT" ]; then
    echo "✅ 工作空间脚本已存在"
else
    echo "⚠️  工作空间脚本不存在"
    echo "   请运行：cp ../scripts/xhs_interaction_simple_fixed.sh /home/chan/.openclaw/workspace/"
fi

echo ""
echo "=== 安装测试完成 ==="
echo "如需手动测试，请运行："
echo "bash /home/chan/.openclaw/workspace/xhs_interaction_simple_fixed.sh"
echo ""
echo "查看日志："
echo "tail -f /home/chan/.openclaw/workspace/xhs_interaction_simple_fixed.log"