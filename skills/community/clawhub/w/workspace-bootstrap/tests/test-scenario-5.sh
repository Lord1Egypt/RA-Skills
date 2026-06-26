#!/bin/bash

# 测试场景5：故障排查，坑点检查
# 目的：验证 check-pitfalls.sh 能否准确检测问题

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="/tmp/broken-workspace-$$"

echo "========================================="
echo "测试场景5：故障排查，坑点检查"
echo "========================================="

# 清理旧的测试目录
rm -rf "$WORKSPACE"

# 创建有问题的 workspace
echo "创建有问题的 workspace..."
mkdir -p "$WORKSPACE"
echo "# MEMORY.md" > "$WORKSPACE/MEMORY.md"

# 制造问题1：MEMORY.md 超过 100 行
echo ""
echo "制造问题1：MEMORY.md 超过 100 行..."
for i in {1..150}; do
    echo "Line $i" >> "$WORKSPACE/MEMORY.md"
done

# 运行坑点检查（预期会检测到多个问题）
echo ""
echo "运行坑点检查..."
OUTPUT=$(bash "$SKILL_ROOT/scripts/check-pitfalls.sh" "$WORKSPACE" 2>&1 || true)

echo "$OUTPUT"
echo ""

# 验证是否检测到 MEMORY.md 容量问题
echo "验证问题检测..."
DETECTED_ISSUES=0

if echo "$OUTPUT" | grep -q "容量爆炸\|超过 100 行\|MEMORY.md.*行"; then
    echo "✅ 检测到 MEMORY.md 容量问题"
    DETECTED_ISSUES=$((DETECTED_ISSUES + 1))
else
    echo "❌ 未检测到 MEMORY.md 容量问题"
fi

# 验证是否检测到缺少核心文件
if echo "$OUTPUT" | grep -q "缺少核心文件\|缺少文件\|SOUL.md\|AGENTS.md\|USER.md"; then
    echo "✅ 检测到缺少核心文件"
    DETECTED_ISSUES=$((DETECTED_ISSUES + 1))
else
    echo "❌ 未检测到缺少核心文件"
fi

# 验证是否检测到缺少目录
if echo "$OUTPUT" | grep -q "缺少目录\|目录不存在\|agents\|memory\|skills"; then
    echo "✅ 检测到缺少目录"
    DETECTED_ISSUES=$((DETECTED_ISSUES + 1))
else
    echo "❌ 未检测到缺少目录"
fi

# 验证至少检测到 2 个问题
if [ $DETECTED_ISSUES -lt 2 ]; then
    echo ""
    echo "❌ 测试失败：问题检测数量不足（检测到 $DETECTED_ISSUES 个，预期至少 2 个）"
    exit 1
fi

# 清理测试目录
rm -rf "$WORKSPACE"

echo ""
echo "========================================="
echo "✅ 场景5 测试通过"
echo "========================================="
