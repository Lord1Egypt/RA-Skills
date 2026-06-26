#!/bin/bash
# OpenClaw 一键备份脚本
# 用法: ./backup-openclaw.sh /Volumes/你的SSD/openclaw-backup.tar.gz

set -e

BACKUP_FILE="${1:-$HOME/Desktop/openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz}"
OPENCLAW_DIR="$HOME/.openclaw"

if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "❌ 错误: 找不到 OpenClaw 数据目录: $OPENCLAW_DIR"
    exit 1
fi

echo "📦 正在备份 OpenClaw 数据..."
echo "   源目录: $OPENCLAW_DIR"
echo "   目标: $BACKUP_FILE"
echo ""

# 创建临时清单
# 默认排除 skills（大且可重新下载）
# 如需完整备份，取消下面一行的注释：
# INCLUDE_SKILLS=1

cat > /tmp/openclaw-backup-list.txt << 'EOF'
.openclaw/workspace
.openclaw/agents
.openclaw/memory
.openclaw/credentials
.openclaw/cron
.openclaw/identity
.openclaw/extensions
.openclaw/devices
.openclaw/openclaw.json
.openclaw/openclaw.json.bak
.openclaw/openclaw.json.bak.1
.openclaw/openclaw.json.bak.2
.openclaw/openclaw.json.bak.3
.openclaw/exec-approvals.json
.openclaw/feishu
.openclaw/canvas
.openclaw/media
.openclaw/completions
.openclaw/delivery-queue
.openclaw/subagents
.openclaw/update-check.json
EOF

# 如果设置 INCLUDE_SKILLS，则添加 skills 目录
if [ "${INCLUDE_SKILLS:-0}" = "1" ]; then
    echo ".openclaw/skills" >> /tmp/openclaw-backup-list.txt
    echo "📦 包含 skills 目录（完整备份模式）"
fi

# 计算预计大小
echo "📊 正在计算备份大小..."
cd ~
ESTIMATED_SIZE=$(tar -czf /dev/null -T /tmp/openclaw-backup-list.txt 2>/dev/null | wc -c || echo "0")
ESTIMATED_MB=$((ESTIMATED_SIZE / 1024 / 1024))
echo "   预计大小: ~${ESTIMATED_MB}MB"
if [ "${INCLUDE_SKILLS:-0}" != "1" ]; then
    echo "   (skills 目录被排除，可在新机器上通过 'clawhub sync' 恢复)"
    echo "   如需完整备份，设置 INCLUDE_SKILLS=1"
fi
echo ""

# 执行备份
echo "🔄 开始压缩备份..."
cd ~
tar -czf "$BACKUP_FILE" -T /tmp/openclaw-backup-list.txt

# 清理临时文件
rm -f /tmp/openclaw-backup-list.txt

# 显示结果
ACTUAL_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo ""
echo "✅ 备份完成!"
echo "   文件: $BACKUP_FILE"
echo "   大小: $ACTUAL_SIZE"
echo ""
echo "💡 恢复命令 (在新机器上运行):"
echo "   ./restore-openclaw.sh $BACKUP_FILE"
