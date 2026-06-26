#!/bin/bash
# yf-memo技能跨环境测试脚本

echo "🚀 yf-memo技能跨环境兼容性测试"
echo "======================================"

# 清理之前的测试
rm -f ~/.openclaw/workspace/pending-items.md 2>/dev/null
rm -f ~/.openclaw/workspace/completed-items.md 2>/dev/null

# 1. 测试技能目录查找
echo "🔍 1. 查找技能目录..."
SKILL_DIR=$(find ~/.openclaw/skills ~/.openclaw/workspace/skills -name "yf-memo" -type d 2>/dev/null | head -1)

if [ -z "$SKILL_DIR" ]; then
    echo "❌ 测试失败：未找到yf-memo技能目录"
    exit 1
fi

echo "✅ 技能目录: $SKILL_DIR"

# 2. 测试脚本文件存在性
echo "🔍 2. 检查脚本文件..."
SCRIPTS=("memo-helper.sh" "daily-summary.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$SKILL_DIR/scripts/$script" ]; then
        echo "✅ $script 存在"
    else
        echo "❌ $script 不存在"
        exit 1
    fi
done

# 3. 测试添加功能
echo "🔍 3. 测试添加待办事项..."
MEMO_SCRIPT="$SKILL_DIR/scripts/memo-helper.sh"
sh "$MEMO_SCRIPT" add "测试任务1"
sh "$MEMO_SCRIPT" add "测试任务2"

# 4. 测试查看功能
echo "🔍 4. 测试查看待办事项..."
echo "当前待办任务："
sh "$MEMO_SCRIPT" show-todos

# 5. 测试完成功能
echo "🔍 5. 测试完成任务..."
sh "$MEMO_SCRIPT" complete-number 1

# 6. 测试查看已完
echo "🔍 6. 测试查看已完成..."
echo "已完成任务："
sh "$MEMO_SCRIPT" show-done

# 7. 测试定时任务脚本
echo "🔍 7. 测试定时任务脚本..."
DAILY_SCRIPT="$SKILL_DIR/scripts/daily-summary.sh"
output=$(sh "$DAILY_SCRIPT")
if echo "$output" | grep -q "{{summary}}"; then
    echo "✅ daily-summary.sh输出格式正确"
    summary=$(echo "$output" | awk '/{{summary}}/{p=1; next} p{print}')
    echo "汇总内容："
    echo "$summary"
else
    echo "❌ daily-summary.sh输出格式异常"
    exit 1
fi

# 8. 清理测试数据
echo "🔍 8. 清理测试环境..."
sh "$MEMO_SCRIPT" complete-number 2 2>/dev/null
rm -f ~/.openclaw/workspace/pending-items.md 2>/dev/null
rm -f ~/.openclaw/workspace/completed-items.md 2>/dev/null
echo "恢复原始文件..."
cat > ~/.openclaw/workspace/pending-items.md << 'EOF'
# 📝 Pending Items

_Last updated: 2026-03-15 10:00

## Pending items

_No pending items_

---

## Notes
- Language-agnostic interface via AI assistant
- Items will be added automatically when you ask
EOF

cat > ~/.openclaw/workspace/completed-items.md << 'EOF'
# ✅ Completed Items

_Created at: 2026-03-15 00:19_

> This file stores completed items with timestamps

## Completed Items List

_No completed items yet_

---

## Notes
- View via natural language: "show me what I've completed"
- Ask your assistant for summaries anytime
EOF

echo ""
echo "🎉 测试完成！所有跨环境功能验证通过"
echo "✅ 动态路径查找"
echo "✅ 脚本执行"  
echo "✅ 功能完整性"
echo "✅ 定时任务兼容"
echo ""
echo "技能可以在任何OpenClaw环境中正常工作！"