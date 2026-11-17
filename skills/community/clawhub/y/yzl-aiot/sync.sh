#!/bin/bash
# yzl-aiot 多平台同步脚本
# 用法: ./sync.sh [message]
# 自动推送到 Gitee + GitHub（可达时）
#
# 凭证优先从环境变量读取，其次读取 ../../.secure/gitee_token：
#   export GITEE_TOKEN=xxx
#   export GH_TOKEN=xxx        # 或已登录 gh CLI

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
TOKEN_FILE="$DIR/../../.secure/gitee_token"
COMMIT_MSG="${1:-自动同步 yzl-aiot 更新}"

cd "$DIR"

# 检查有没有未提交的更改
if git status --porcelain | grep -q .; then
    git add -A
    git commit -m "$COMMIT_MSG" --author="小虾米 <yzlkj@users.noreply.github.com>" 2>/dev/null || echo "  → 无新变更"
fi

# 推送到 Gitee（带 Token）
echo "📤 推送 Gitee..."
GITEE_TOKEN_VALUE="${GITEE_TOKEN:-}"
if [ -z "$GITEE_TOKEN_VALUE" ] && [ -f "$TOKEN_FILE" ]; then
    GITEE_TOKEN_VALUE="$(cat "$TOKEN_FILE")"
fi
if [ -n "$GITEE_TOKEN_VALUE" ]; then
    git push "https://dd1287963201:${GITEE_TOKEN_VALUE}@gitee.com/yzl-aiot/yzl-aiot.git" master
else
    echo "  ⚠️  未提供 Gitee token（GITEE_TOKEN 或 $TOKEN_FILE），跳过"
fi

# 推送到 GitHub
echo "📤 推送 GitHub..."
GH_TOKEN_VALUE="${GH_TOKEN:-}"
if [ -z "$GH_TOKEN_VALUE" ] && command -v gh &>/dev/null && gh auth status 2>/dev/null; then
    GH_TOKEN_VALUE="$(gh auth token)"
fi
if [ -n "$GH_TOKEN_VALUE" ]; then
    timeout 15 git push "https://x-access-token:${GH_TOKEN_VALUE}@github.com/yzlkj/yzl-aiot.git" master 2>/dev/null || \
        echo "  ⚠️  GitHub 不可达或超时，跳过（国内网络限制）"
else
    echo "  ⚠️  未提供 GitHub token，跳过"
fi

echo "✅ 同步完成"
