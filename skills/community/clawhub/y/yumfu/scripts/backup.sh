#!/bin/bash
# YumFu 自动备份脚本
# 每次游戏后调用此脚本备份存档

SAVE_DIR=~/clawd/memory/yumfu
cd "$SAVE_DIR" || exit 1

# Git提交
git add .
git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M:%S')" --quiet

# 清理30天前的commit（可选，保持仓库轻量）
# git gc --prune=30.days.ago

echo "✅ YumFu存档已备份到本地Git ($(git log -1 --format=%h))"
