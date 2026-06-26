#!/bin/bash
# ============================================================
# 闻其声耳轻松可视采耳 Skill · 客户侧自动更新脚本
# ============================================================
# 用法：
#   1. 将此脚本放在 skill 目录下
#   2. chmod +x auto_update.sh
#   3. 添加到 crontab（每天凌晨 3:07 检查更新）：
#      7 3 * * * cd ~/.openclaw/workspace/skills/wenqisheng-ear-care && bash auto_update.sh
# ============================================================

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_FILE="$SKILL_DIR/update.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

cd "$SKILL_DIR"

# 检查是否是 git 仓库
if [ ! -d ".git" ]; then
    log "ERROR: 不是 git 仓库，无法自动更新。请通过 git clone 安装。"
    exit 1
fi

# 获取远程仓库信息
REMOTE=$(git remote get-url origin 2>/dev/null || echo "")
if [ -z "$REMOTE" ]; then
    log "ERROR: 未配置 git remote，无法自动更新。"
    exit 1
fi

# 保存当前版本
OLD_VERSION=$(cat version.json 2>/dev/null | grep -o '"data_version": "[^"]*"' | cut -d'"' -f4 || echo "unknown")

# 拉取最新代码
log "正在检查更新..."
git fetch origin --quiet 2>&1 | tee -a "$LOG_FILE"

LOCAL=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse origin/master 2>/dev/null || git rev-parse origin/main 2>/dev/null)

if [ "$LOCAL" = "$REMOTE_HASH" ]; then
    log "已是最新版本 (data_version: $OLD_VERSION)"
    exit 0
fi

log "发现新版本，正在更新..."
git pull --ff-only origin master 2>&1 | tee -a "$LOG_FILE" || \
git pull --ff-only origin main 2>&1 | tee -a "$LOG_FILE"

NEW_VERSION=$(cat version.json 2>/dev/null | grep -o '"data_version": "[^"]*"' | cut -d'"' -f4 || echo "unknown")

log "更新完成！"
log "版本变更: $OLD_VERSION → $NEW_VERSION"

# 可选：运行测试验证
if [ -f "scripts/test_skill.py" ]; then
    python3 scripts/test_skill.py 2>&1 | tee -a "$LOG_FILE" || true
fi

log "自动更新流程结束"
