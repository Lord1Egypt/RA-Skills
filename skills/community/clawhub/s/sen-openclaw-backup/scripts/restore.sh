#!/bin/bash
# OpenClaw 一键恢复脚本
# 用法: ./restore-openclaw.sh /Volumes/你的SSD/openclaw-backup.tar.gz

set -e

BACKUP_FILE="$1"

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ 用法: $0 <备份文件路径>"
    echo "   例如: $0 /Volumes/SSD/openclaw-backup-20250318.tar.gz"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ 错误: 找不到备份文件: $BACKUP_FILE"
    exit 1
fi

echo "📦 OpenClaw 恢复工具"
echo "   备份文件: $BACKUP_FILE"
echo ""

# 检查是否已安装 OpenClaw
if ! command -v openclaw &> /dev/null; then
    echo "⚠️  警告: 未检测到 OpenClaw 安装"
    echo "   建议先安装: npm install -g openclaw@latest"
    read -p "是否继续恢复? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查现有数据
if [ -d "$HOME/.openclaw" ]; then
    echo "⚠️  警告: 检测到现有 OpenClaw 数据"
    echo "   位置: $HOME/.openclaw"
    read -p "是否覆盖? 现有数据将被移动至 .openclaw.bak (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ 已取消"
        exit 1
    fi
    
    # 备份现有数据
    BAK_DIR="$HOME/.openclaw.bak.$(date +%Y%m%d-%H%M%S)"
    echo "   移动现有数据到: $BAK_DIR"
    mv "$HOME/.openclaw" "$BAK_DIR"
fi

echo ""
echo "🔄 正在解压备份..."
cd ~
tar -xzf "$BACKUP_FILE"

echo ""
echo "✅ 数据恢复完成!"
echo ""

# 恢复 skills（如果需要）
if command -v openclaw &> /dev/null; then
    echo "🔄 正在同步 skills..."
    clawhub sync 2>/dev/null || echo "   (clawhub sync 可选，可稍后手动运行)"
fi

echo ""
echo "🎉 恢复完成!"
echo ""
echo "📋 接下来:"
echo "   1. 检查配置: openclaw status"
echo "   2. 启动 Gateway: openclaw gateway start"
echo "   3. 验证数据完整性"
echo ""
echo "💡 提示:"
echo "   - 如果更换了机器，可能需要重新配置 API 密钥"
echo "   - Feishu/Telegram 等频道配置可能需要更新"
echo "   - 检查 ~/.openclaw/openclaw.json 中的路径设置"
