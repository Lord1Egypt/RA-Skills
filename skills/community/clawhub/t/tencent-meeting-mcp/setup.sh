#!/bin/bash
# Setup script for 腾讯会议 MCP Skill

set -e

echo "🚀 设置腾讯会议 MCP Skill..."
echo ""

# 检查 mcporter
if ! command -v mcporter &> /dev/null; then
    echo "⚠️  未找到 mcporter，正在安装..."
    npm install -g mcporter
    echo "✅ mcporter 安装完成"
fi

# 新增：检查 TENCENT_MEETING_TOKEN 环境变量
echo "🔍 检查腾讯会议 Token 环境变量..."
if [ -z "$TENCENT_MEETING_TOKEN" ]; then
    echo "❌ 错误：未检测到 TENCENT_MEETING_TOKEN 环境变量！"
    echo "请先执行以下命令设置环境变量（替换为真实 Token）："
    echo "  export TENCENT_MEETING_TOKEN=\"your_actual_token_here\""
    echo "或在执行脚本时直接传入："
    echo "  TENCENT_MEETING_TOKEN=\"your_actual_token_here\" bash this_script.sh"
    exit 1  # 退出脚本，避免后续无效操作
else
    echo "✅ TENCENT_MEETING_TOKEN 环境变量已配置"
fi
echo ""

# 添加 MCP 配置
echo "🔧 配置 mcporter..."

# 从环境变量中读取用户填写的 Token
mcporter config add tencent-meeting-mcp https://mcp.meeting.tencent.com/mcp/wemeet-open/v1 \
    --header "X-Tencent-Meeting-Token=$TENCENT_MEETING_TOKEN" \
    --header "X-Skill-Version=v1.0.1" \
    --scope project

echo "✅ 配置完成！"

# 验证配置
echo "🧪 验证配置..."
if mcporter list 2>&1 | grep -q "tencent-meeting-mcp"; then
    echo "✅ 配置验证成功！"
    echo ""
    mcporter list | grep -A 1 "tencent-meeting-mcp" || true
else
    echo "⚠️  配置验证失败，请检查网络或 Token 是否有效"
    echo ""
    echo "如有问题，请访问  获取 Token"
fi

echo ""
echo "─────────────────────────────────────"
echo "🎉 设置完成！"