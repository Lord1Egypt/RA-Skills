#!/bin/bash
# 配置预览与脱敏脚本
# 用法: ./preview.sh ~/.openclaw/openclaw.json

CONFIG_FILE="${1:-~/.openclaw/openclaw.json}"

echo "📋 配置文件预览（脱敏版）"
echo "================================"
echo ""

# 脱敏处理函数
sanitize() {
    sed -E 's/("apiKey"|"token"|"password"|"secret"|"botToken":[[:space:]]*")[^"]*"/\1***"/g'
}

# 基本信息
echo "🔧 基本信息"
echo "------------"
jq -r '
{
    "版本": .meta.lastTouchedVersion // "未知",
    "最后更新": .meta.lastTouchedAt // "未知",
    "主模型": .agents.defaults.model.primary // "未设置"
} | to_entries | "\(.key): \(.value)"
' "$CONFIG_FILE"
echo ""

# 模型提供商
echo "🔌 模型提供商"
echo "------------"
jq -r '.models.providers // {} | keys[]' "$CONFIG_FILE" 2>/dev/null | while read -r p; do
    echo "  - $p"
done
echo ""

# Channel 配置
echo "💬 Channel 状态"
echo "---------------"
jq -r '.channels | to_entries[] | "\(.key): enabled=\(.value.enabled)"' "$CONFIG_FILE" 2>/dev/null
echo ""

# 插件
echo "🔌 插件"
echo "-------"
jq -r '.plugins.entries // {} | to_entries[] | "\(.key): \(.value.enabled)"' "$CONFIG_FILE" 2>/dev/null
echo ""

# 完整配置（脱敏）
echo "📄 完整配置（脱敏）"
echo "-------------------"
jq '.' "$CONFIG_FILE" | sanitize
