#!/bin/bash

# 测试场景4：自定义配置，扩展模板
# 目的：验证用户能否基于模板自定义扩展

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE="/tmp/custom-workspace-$$"

echo "========================================="
echo "测试场景4：自定义配置，扩展模板"
echo "========================================="

# 清理旧的测试目录
rm -rf "$WORKSPACE"

# 创建基础 workspace
echo "创建基础 workspace..."
bash "$SKILL_ROOT/scripts/bootstrap.sh" "$WORKSPACE"

# 添加自定义扩展
echo ""
echo "添加自定义扩展..."
mkdir -p "$WORKSPACE/custom-plugins"
mkdir -p "$WORKSPACE/custom-templates"

echo "## 👥 自定义团队成员" >> "$WORKSPACE/SOUL.md"
echo "- **custom-agent** 自定义Agent 🎨 — 特殊任务" >> "$WORKSPACE/SOUL.md"

echo "# 自定义规则" > "$WORKSPACE/custom-rules.md"

# 验证自定义扩展
echo ""
echo "验证自定义扩展..."

if [ ! -d "$WORKSPACE/custom-plugins" ]; then
    echo "❌ 自定义目录创建失败: custom-plugins"
    exit 1
else
    echo "✅ 自定义目录创建成功: custom-plugins"
fi

if [ ! -d "$WORKSPACE/custom-templates" ]; then
    echo "❌ 自定义目录创建失败: custom-templates"
    exit 1
else
    echo "✅ 自定义目录创建成功: custom-templates"
fi

if [ ! -f "$WORKSPACE/custom-rules.md" ]; then
    echo "❌ 自定义文件创建失败: custom-rules.md"
    exit 1
else
    echo "✅ 自定义文件创建成功: custom-rules.md"
fi

if ! grep -q "自定义Agent" "$WORKSPACE/SOUL.md"; then
    echo "❌ SOUL.md 修改失败"
    exit 1
else
    echo "✅ SOUL.md 修改成功"
fi

# 验证核心结构未被破坏
echo ""
echo "验证核心结构未被破坏..."
CORE_FILES="SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md WORKSPACE-TEMPLATE.md"

for file in $CORE_FILES; do
    if [ ! -f "$WORKSPACE/$file" ]; then
        echo "❌ 核心文件丢失: $file"
        exit 1
    else
        echo "✅ 核心文件存在: $file"
    fi
done

# 运行坑点检查
echo ""
echo "运行坑点检查..."
bash "$SKILL_ROOT/scripts/check-pitfalls.sh" "$WORKSPACE"

# 清理测试目录
rm -rf "$WORKSPACE"

echo ""
echo "========================================="
echo "✅ 场景4 测试通过"
echo "========================================="
