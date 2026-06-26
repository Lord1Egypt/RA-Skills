#!/bin/bash
# Git 统计工具 - 获取代码提交数据
# 用法: ./git-stats.sh /path/to/repo [days]

set -e

# 默认参数
DEFAULT_DAYS=7
DEFAULT_BRANCH="main"

# 帮助信息
usage() {
    echo "Git 统计工具"
    echo "用法: $0 <repo_path> [days] [branch]"
    echo ""
    echo "参数:"
    echo "  repo_path  Git 仓库路径"
    echo "  days       统计天数（默认: 7）"
    echo "  branch     分支名（默认: main）"
    echo ""
    echo "示例:"
    echo "  $0 /path/to/repo 7"
    echo "  $0 /path/to/repo 30 develop"
}

# 检查参数
if [ $# -lt 1 ]; then
    usage
    exit 1
fi

REPO_PATH=$1
DAYS=${2:-$DEFAULT_DAYS}
BRANCH=${3:-$DEFAULT_BRANCH}

# 验证仓库路径
if [ ! -d "$REPO_PATH" ]; then
    echo "错误: 仓库路径不存在: $REPO_PATH"
    exit 1
fi

if [ ! -d "$REPO_PATH/.git" ]; then
    echo "错误: 不是 Git 仓库: $REPO_PATH"
    exit 1
fi

# 进入仓库
cd "$REPO_PATH"

# 检查分支是否存在
if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "错误: 分支不存在: $BRANCH"
    echo "可用分支:"
    git branch -a
    exit 1
fi

# 切换到指定分支
git checkout $BRANCH > /dev/null 2>&1

# 获取统计数据
SINCE_DATE=$(date -d "$DAYS days ago" +%Y-%m-%d)

echo "# Git 代码统计"
echo "**日期范围:** $SINCE_DATE 至 $(date +%Y-%m-%d)"
echo "**分支:** $BRANCH"
echo ""

# 总提交数
TOTAL_COMMITS=$(git rev-list --count --since="$SINCE_DATE 00:00:00" $BRANCH)
echo "## 📊 总体统计"
echo "- **总提交数:** $TOTAL_COMMITS"
echo "- **活跃天数:** $(git log --since="$SINCE_DATE 00:00:00" --format=%ad --date=short $BRANCH | sort -u | wc -l)"
echo ""

# 按作者统计提交数
echo "## 👥 作者贡献"
echo "| 作者 | 提交数 | 最近一次提交 |"
echo "|------|--------|-------------|"

git log --since="$SINCE_DATE 00:00:00" --format='%an' $BRANCH | \
    sort | uniq -c | sort -rn | \
    while read count author; do
        last_commit=$(git log --author="$author" --since="$SINCE_DATE 00:00:00" --format='%ad' --date=short $BRANCH | head -n 1)
        echo "| $author | $count | $last_commit |"
    done

echo ""

# 代码行数变化
echo "## 📈 代码行数变化"
git diff --stat "HEAD@{$DAYS days ago}..HEAD" 2>/dev/null || echo "最近 $DAYS 天没有代码变化"

echo ""

# 最近 5 次提交
echo "## 🔥 最近提交"
git log --since="$SINCE_DATE 00:00:00" --format='%h - %an, %ar : %s' --date=relative $BRANCH | head -n 5

echo ""

# 按文件类型统计
echo "## 📁 文件类型统计"
git log --since="$SINCE_DATE 00:00:00" --name-only --pretty=format: $BRANCH | \
    grep -v '^$' | grep -v '^#' | \
    sed 's/.*\.//' | sort | uniq -c | sort -rn | \
    head -n 10 | \
    while read count ext; do
        if [ -n "$ext" ]; then
            echo "- .$ext: $count 个文件"
        fi
    done

echo ""
echo "---"
echo "*生成时间: $(date '+%Y-%m-%d %H:%M:%S')*"
