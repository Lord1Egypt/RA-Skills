#!/bin/bash
# Agent 自动更新脚本
# 在启动时检查并拉取远程更新

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$PROJECT_ROOT/config/auto_update.yaml"
MEMORY_FILE="$PROJECT_ROOT/memory/hot.md"

# 读取配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在: $CONFIG_FILE"
    exit 0
fi

# 解析 YAML 配置（简单实现）
ENABLED=$(grep "^enabled:" "$CONFIG_FILE" | awk '{print $2}')
REMOTE=$(grep "^remote:" "$CONFIG_FILE" | awk '{print $2}')
BRANCH=$(grep "^branch:" "$CONFIG_FILE" | awk '{print $2}')
SILENT=$(grep "^silent:" "$CONFIG_FILE" | awk '{print $2}')

# 检查是否启用
if [ "$ENABLED" != "true" ]; then
    [ "$SILENT" != "true" ] && echo "ℹ️  自动更新已禁用"
    exit 0
fi

# 进入项目目录
cd "$PROJECT_ROOT" || exit 1

# 检查是否是 git 仓库
if [ ! -d ".git" ]; then
    [ "$SILENT" != "true" ] && echo "⚠️  不是 git 仓库，跳过更新"
    exit 0
fi

# 获取当前 commit
LOCAL_COMMIT=$(git rev-parse HEAD)

# 静默 fetch 远程更新
git fetch "$REMOTE" "$BRANCH" 2>/dev/null || {
    [ "$SILENT" != "true" ] && echo "⚠️  无法连接远程仓库"
    exit 0
}

# 获取远程 commit
REMOTE_COMMIT=$(git rev-parse "$REMOTE/$BRANCH")

# 比对是否有更新
if [ "$LOCAL_COMMIT" = "$REMOTE_COMMIT" ]; then
    [ "$SILENT" != "true" ] && echo "✅ 已是最新版本"
    exit 0
fi

# 有更新，执行 pull
[ "$SILENT" != "true" ] && echo "🔄 发现更新，正在拉取..."

git pull "$REMOTE" "$BRANCH" || {
    echo "❌ 更新失败，请手动处理"
    exit 1
}

# 记录更新到 memory/hot.md
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
UPDATE_LOG="- [$TIMESTAMP] 自动更新: $LOCAL_COMMIT -> $REMOTE_COMMIT"

if [ -f "$MEMORY_FILE" ]; then
    echo "$UPDATE_LOG" >> "$MEMORY_FILE"
fi

[ "$SILENT" != "true" ] && echo "✅ 更新完成"
exit 0
