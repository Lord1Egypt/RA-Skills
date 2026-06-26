#!/bin/bash
# Obsidian Git 自动同步脚本 v1.0
# 核心原则：只增不减，安全推送

set -e

# 配置
OBSIDIAN_DIR="${OBSIDIAN_DIR:-$HOME/Obsidian}"
REMOTE_REPO="${REMOTE_REPO:-obsidian-vault}"
REMOTE_BRANCH="${REMOTE_BRANCH:-main}"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 进入 Obsidian 目录
cd "$OBSIDIAN_DIR" || {
    log_error "无法进入 Obsidian 目录: $OBSIDIAN_DIR"
    exit 1
}

# 检查是否有改动
if git diff-index --quiet HEAD --; then
    log_info "无改动，跳过推送"
    exit 0
fi

# 获取改动文件数
CHANGED_FILES=$(git diff-index --name-only HEAD -- | wc -l)
log_info "待推送文件数: $CHANGED_FILES"

# 拉取远程最新
log_info "拉取远程最新..."
git fetch origin "$REMOTE_BRANCH" || {
    log_warn "拉取失败，可能是首次推送"
}

# 只增不减原则：使用 rebase 而不是 merge
if git rev-parse --verify origin/$REMOTE_BRANCH >/dev/null 2>&1; then
    log_info "Rebase 远程分支..."
    git rebase origin/$REMOTE_BRANCH || {
        log_error "Rebase 失败，需要手动处理冲突"
        git rebase --abort
        exit 1
    }
fi

# 添加改动
git add -A

# 提交（带时间戳）
COMMIT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="记忆同步 @ $COMMIT_TIME

文件数: $CHANGED_FILES
来源: obsidian-brain-pro 自动推送
"

git commit -m "$COMMIT_MSG" || {
    log_warn "无改动可提交"
    exit 0
}

# 推送
log_info "推送到远程..."
git push origin "$REMOTE_BRANCH" || {
    log_error "推送失败，请检查网络或权限"
    exit 1
}

log_info "✅ Git 同步完成"
echo "文件数: $CHANGED_FILES"
echo "时间: $COMMIT_TIME"

# 清理僵尸进程（可选）
if command -v openclaw &>/dev/null; then
    openclaw doctor --fix-zombies &>/dev/null || true
fi

exit 0