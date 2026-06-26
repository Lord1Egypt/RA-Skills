#!/bin/bash

# 测试场景3：团队协作，共享配置
# 目的：验证团队成员能否共享 workspace 配置

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
WORKSPACE_A="/tmp/team-workspace-$$"
WORKSPACE_B="/tmp/team-member-b-workspace-$$"

echo "========================================="
echo "测试场景3：团队协作，共享配置"
echo "========================================="

# 清理旧的测试目录
rm -rf "$WORKSPACE_A" "$WORKSPACE_B"

# 成员 A 创建 workspace
echo "团队成员 A 创建 workspace..."
bash "$SKILL_ROOT/scripts/wizard.sh" "$WORKSPACE_A" << EOF
小溪
善人
Asia/Shanghai
AI 思维教练
成为最靠谱的思维教练
1
y
EOF

# 成员 B 克隆（使用 cp 模拟 git clone）
echo ""
echo "团队成员 B 克隆 workspace..."
cp -r "$WORKSPACE_A" "$WORKSPACE_B"

# 验证配置一致性
echo ""
echo "验证配置一致性..."
CORE_FILES="SOUL.md AGENTS.md MEMORY.md USER.md HEARTBEAT.md"
INCONSISTENT_FILES=""

for file in $CORE_FILES; do
    if ! diff -q "$WORKSPACE_A/$file" "$WORKSPACE_B/$file" > /dev/null 2>&1; then
        INCONSISTENT_FILES="$INCONSISTENT_FILES $file"
        echo "❌ 配置不一致: $file"
    else
        echo "✅ 配置一致: $file"
    fi
done

if [ -n "$INCONSISTENT_FILES" ]; then
    echo "❌ 测试失败：配置不一致 - $INCONSISTENT_FILES"
    exit 1
fi

# 验证目录结构一致性
echo ""
echo "验证目录结构一致性..."
REQUIRED_DIRS="agents memory skills user-data scripts shared reports temp .learnings wiki"

for dir in $REQUIRED_DIRS; do
    if [ ! -d "$WORKSPACE_A/$dir" ] || [ ! -d "$WORKSPACE_B/$dir" ]; then
        echo "❌ 目录结构不一致: $dir"
        exit 1
    else
        echo "✅ 目录结构一致: $dir"
    fi
done

# 运行坑点检查（成员 A）
echo ""
echo "运行成员 A 的坑点检查..."
bash "$SKILL_ROOT/scripts/check-pitfalls.sh" "$WORKSPACE_A"

# 运行坑点检查（成员 B）
echo ""
echo "运行成员 B 的坑点检查..."
bash "$SKILL_ROOT/scripts/check-pitfalls.sh" "$WORKSPACE_B"

# 清理测试目录
rm -rf "$WORKSPACE_A" "$WORKSPACE_B"

echo ""
echo "========================================="
echo "✅ 场景3 测试通过"
echo "========================================="
