#!/bin/bash

# 测试场景1：全新用户，第一次搭建
# 目的：验证零基础用户能否快速搭建 workspace

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="/tmp/test-workspace-1-$$"

echo "========================================="
echo "测试场景1：全新用户，第一次搭建"
echo "========================================="

# 清理旧的测试目录
rm -rf "$WORKSPACE"
mkdir -p "$(dirname "$WORKSPACE")"

# 运行向导（使用交互式输入）
bash "$SKILL_ROOT/scripts/wizard.sh" "$WORKSPACE" << EOF
小智
张三
Asia/Shanghai
AI 技术助手
成为最靠谱的编程助手
2
y
EOF

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

# 验证核心文件
echo ""
echo "验证核心文件..."
REQUIRED_FILES="SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md"
MISSING_FILES=""

for file in $REQUIRED_FILES; do
    if [ ! -f "$WORKSPACE/$file" ]; then
        MISSING_FILES="$MISSING_FILES $file"
        echo "❌ 缺少文件: $file"
    else
        echo "✅ 文件存在: $file"
    fi
done

if [ -n "$MISSING_FILES" ]; then
    echo "❌ 测试失败：缺少文件 - $MISSING_FILES"
    exit 1
fi

# 验证 SOUL.md 内容
echo ""
echo "验证 SOUL.md 内容..."
if ! grep -q "小智" "$WORKSPACE/SOUL.md"; then
    echo "❌ SOUL.md 缺少小龙虾名称"
    exit 1
else
    echo "✅ SOUL.md 包含小龙虾名称：小智"
fi

# 验证 USER.md 内容
echo ""
echo "验证 USER.md 内容..."
if ! grep -q "张三" "$WORKSPACE/USER.md"; then
    echo "❌ USER.md 缺少用户名称"
    exit 1
else
    echo "✅ USER.md 包含用户名称：张三"
fi

# 清理测试目录
rm -rf "$WORKSPACE"

echo ""
echo "========================================="
echo "✅ 场景1 测试通过"
echo "========================================="
