#!/usr/bin/env bash
# qg-skill-sync - 卸载脚本
# 清理本地仓库缓存和配置（不删除已同步到 ~/.openclaw/skills/ 的技能文件）
# 用法: bash uninstall.sh

set -euo pipefail

SYNC_HOME="$HOME/.qg-skill-sync"

if [ -d "$SYNC_HOME" ]; then
    rm -rf "$SYNC_HOME"
    echo "已清理本地缓存: $SYNC_HOME"
else
    echo "未找到缓存目录，无需清理"
fi

echo ""
echo "注意: ~/.openclaw/skills/ 下已同步的技能文件未被删除。"
echo "      如需删除，请手动清理对应目录。"
echo ""
echo "请在 OpenClaw 中删除定时任务（openclaw cron list 查找 qg-skill-sync-1030 和 qg-skill-sync-1730）。"
