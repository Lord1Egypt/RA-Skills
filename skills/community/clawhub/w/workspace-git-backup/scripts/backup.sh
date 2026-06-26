#!/bin/bash
# GitHub Backup - 通用自动备份脚本
# 从配置文件读取设置，检测变更并推送到远程仓库

set -e

# 配置文件路径
CONFIG_FILE="$HOME/.openclaw/workspace/.backup-config.json"
LOG_FILE="$HOME/.openclaw/logs/github-backup.log"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查配置文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    log "错误: 配置文件不存在: $CONFIG_FILE"
    echo "请先运行 install.sh 进行配置"
    exit 1
fi

# 读取配置
BACKUP_PATH=$(cat "$CONFIG_FILE" | grep -o '"backupPath"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/"backupPath"[[:space:]]*:[[:space:]]*"\([^"]*\)"/\1/' | sed "s|^~|$HOME|")
UPDATE_TIMESTAMP=$(cat "$CONFIG_FILE" | grep -o '"updateTimestamp"[[:space:]]*:[[:space:]]*[a-z]*' | sed 's/"updateTimestamp"[[:space:]]*:[[:space:]]*//' )

# 展开路径中的 ~
BACKUP_PATH="${BACKUP_PATH/#\~/$HOME}"

log "========== 开始备份 =========="
log "备份路径: $BACKUP_PATH"

# 检查目录是否存在
if [ ! -d "$BACKUP_PATH" ]; then
    log "错误: 备份路径不存在: $BACKUP_PATH"
    exit 1
fi

cd "$BACKUP_PATH"

# 检查是否是 git 仓库
if [ ! -d ".git" ]; then
    log "错误: 不是 git 仓库: $BACKUP_PATH"
    exit 1
fi

# 检查是否有变更
if git diff --quiet && git diff --staged --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
    log "没有变更，跳过备份"
    log "========== 备份结束 =========="
    exit 0
fi

# 获取变更文件列表
CHANGED_FILES=$(git status --porcelain)
log "检测到变更:\n$CHANGED_FILES"

# 更新 README 时间戳
if [ "$UPDATE_TIMESTAMP" = "true" ] && [ -f README.md ]; then
    TODAY=$(date '+%Y-%m-%d')
    # 支持中英文格式
    sed -i "s/\*最后更新: [0-9-]*\*/\*最后更新: $TODAY\*/g" README.md 2>/dev/null || \
    sed -i '' "s/\*最后更新: [0-9-]*\*/\*最后更新: $TODAY\*/g" README.md 2>/dev/null || true
    sed -i "s/\*Last updated: [0-9-]*\*/\*Last updated: $TODAY\*/g" README.md 2>/dev/null || \
    sed -i '' "s/\*Last updated: [0-9-]*\*/\*Last updated: $TODAY\*/g" README.md 2>/dev/null || true
fi

# 生成 commit 消息
COMMIT_MSG="chore: 自动备份 $(date '+%Y-%m-%d %H:%M')"
log "Commit 消息: $COMMIT_MSG"

# 添加所有变更并提交
git add .
git commit -m "$COMMIT_MSG"

# 推送
if git push; then
    log "备份完成，已推送到远程仓库"
else
    log "错误: 推送失败"
    exit 1
fi

log "========== 备份结束 =========="
