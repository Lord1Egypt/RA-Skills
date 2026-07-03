#!/bin/bash
# todos/scripts/pre_commit_check.sh
# 提交前隐私检查脚本
# 用法：./scripts/pre_commit_check.sh
# 版本：v1.0 | 日期：2026-06-11

set -e

echo "🔍 提交前隐私检查..."

# 检查隐私关键词
echo "=== 检查隐私信息 ==="
PRIVACY_PATTERNS=(
    "token"
    "secret"
    "api_key"
    "apikey"
    "client_id"
    "client_secret"
    "password"
    "本金"
    "持仓金额"
    "ding7ise8b0t8cyew2m2"
)

FOUND=false
for pattern in "${PRIVACY_PATTERNS[@]}"; do
    # 只检查代码文件（不含文档中的安全示例说明，不含检查脚本本身）
    RESULT=$(grep -rn "$pattern" . \
        --include="*.py" \
        --include="*.json" \
        --include="*.yaml" \
        2>/dev/null | grep -v ".git/" | grep -v ".gitignore" | grep -v "scripts/" || true)
    if [ -n "$RESULT" ]; then
        echo "⚠️  发现敏感词 '$pattern'："
        echo "$RESULT"
        FOUND=true
    fi
done

if [ "$FOUND" = true ]; then
    echo ""
    echo "❌ 检查失败：发现隐私信息"
    echo "请处理后再提交，或确认已在 .gitignore 中排除"
    exit 1
fi

echo "✅ 隐私检查通过：无敏感信息"

# 检查 .env 文件（不应存在）
if [ -f ".env" ]; then
    echo "⚠️  发现 .env 文件，确保已加入 .gitignore"
fi

# 检查 todos.db（不应存在）
if [ -f "todos.db" ]; then
    echo "⚠️  发现 todos.db，确保已加入 .gitignore"
fi

echo "✅ 提交前检查完成"
exit 0