#!/bin/bash

# 测试场景2：有经验用户，快速复刻
# 目的：验证有经验用户能否快速复刻现有 workspace

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="/tmp/test-workspace-2-$$"

echo "========================================="
echo "测试场景2：有经验用户，快速复刻"
echo "========================================="

# 清理旧的测试目录
rm -rf "$WORKSPACE"
mkdir -p "$(dirname "$WORKSPACE")"

# 记录开始时间
START_TIME=$(date +%s.%N)

# 运行 bootstrap
echo "运行 bootstrap.sh..."
bash "$SKILL_ROOT/scripts/bootstrap.sh" "$WORKSPACE"

# 记录结束时间
END_TIME=$(date +%s.%N)
DURATION=$(awk "BEGIN {printf \"%.2f\", $END_TIME - $START_TIME}")

echo ""
echo "执行时间：${DURATION}s"

# 验证目录结构
echo ""
echo "验证目录结构..."
REQUIRED_DIRS="agents memory skills user-data scripts shared reports temp .learnings wiki"
MISSING_DIRS=""

for dir in $REQUIRED_DIRS; do
    if [ ! -d "$WORKSPACE/$dir" ]; then
        MISSING_DIRS="$MISSING_DIRS $dir"
        echo "❌ 缺少目录: $dir"
    else
        echo "✅ 目录存在: $dir"
    fi
done

if [ -n "$MISSING_DIRS" ]; then
    echo "❌ 测试失败：缺少目录 - $MISSING_DIRS"
    exit 1
fi

# 验证模板文件
echo ""
echo "验证模板文件..."
TEMPLATE_FILES="SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md WORKSPACE-TEMPLATE.md"
MISSING_FILES=""

for file in $TEMPLATE_FILES; do
    if [ ! -f "$WORKSPACE/$file" ]; then
        MISSING_FILES="$MISSING_FILES $file"
        echo "❌ 缺少模板: $file"
    else
        echo "✅ 模板存在: $file"
    fi
done

if [ -n "$MISSING_FILES" ]; then
    echo "❌ 测试失败：缺少模板 - $MISSING_FILES"
    exit 1
fi

# 验证执行时间 < 1 秒
if (( $(awk "BEGIN {print ($DURATION > 1.0) ? 1 : 0}") )); then
    echo "❌ 执行时间过长：${DURATION}s（预期 < 1s）"
    exit 1
else
    echo "✅ 执行时间符合要求：${DURATION}s"
fi

# 运行坑点检查
echo ""
echo "运行坑点检查..."
bash "$SKILL_ROOT/scripts/check-pitfalls.sh" "$WORKSPACE"

# 清理测试目录
rm -rf "$WORKSPACE"

echo ""
echo "========================================="
echo "✅ 场景2 测试通过"
echo "========================================="
