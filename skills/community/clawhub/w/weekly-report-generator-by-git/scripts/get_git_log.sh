#!/bin/zsh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="${SKILL_DIR}/config.conf"

# 读取配置文件
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "ERROR: 配置文件不存在: $CONFIG_FILE"
    echo "请复制 config.example.conf 为 config.conf 并填写项目路径："
    echo "  cp config.example.conf config.conf"
    exit 1
fi
source "$CONFIG_FILE"

# 校验项目目录
if [[ ${#PROJECT_DIRS[@]} -eq 0 ]]; then
    echo "ERROR: PROJECT_DIRS 为空，请在 config.conf 中配置至少一个项目路径"
    exit 1
fi

# 获取本周一日期（兼容 macOS 和 Linux）
MONDAY=$(date -v-monday +%Y-%m-%d 2>/dev/null || date -d "last monday" +%Y-%m-%d)
# 获取下周一日期
NEXT_MONDAY=$(date -v+7d -j -f "%Y-%m-%d" "$MONDAY" +%Y-%m-%d 2>/dev/null || date -d "$MONDAY + 7 days" +%Y-%m-%d)

# 遍历每个项目输出日志
for PROJECT_DIR in "${PROJECT_DIRS[@]}"; do
    if [[ ! -d "$PROJECT_DIR/.git" ]]; then
        echo "WARNING: 跳过非 git 目录: $PROJECT_DIR"
        continue
    fi

    PROJECT_NAME=$(basename "$PROJECT_DIR")
    GIT_AUTHOR="${AUTHOR:-$(cd "$PROJECT_DIR" && git config user.name)}"

    echo "===PROJECT: ${PROJECT_NAME}==="

    echo "===GIT_LOG_START==="
    cd "$PROJECT_DIR" && git log --author="$GIT_AUTHOR" --since="$MONDAY" --until="$NEXT_MONDAY" --pretty=format:"%h|%ad|%s" --date=short --no-merges
    echo ""
    echo "===GIT_LOG_END==="

    echo "===GIT_STAT_START==="
    cd "$PROJECT_DIR" && git log --author="$GIT_AUTHOR" --since="$MONDAY" --until="$NEXT_MONDAY" --pretty=format:"========== %h %ad %s ==========" --date=short --no-merges --stat
    echo ""
    echo "===GIT_STAT_END==="

    echo ""
done
