#!/bin/bash
# workspace-wizard - 交互式配置向导
# 版本: v0.3.0

set -e

WORKSPACE_ROOT=${1:-"."}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "═══════════════════════════════════════"
echo "🧙 Workspace Configuration Wizard"
echo "═══════════════════════════════════════"
echo ""

# 收集信息
read -p "1. 你的小龙虾叫什么名字？ (例如：小溪) " AGENT_NAME
read -p "2. 你的用户叫什么？ (例如：善人) " USER_NAME
read -p "3. 你的时区？ (例如：Asia/Shanghai) " USER_TIMEZONE
read -p "4. 你的小龙虾的身份是？ (例如：AI 思维教练) " AGENT_IDENTITY
read -p "5. 你的愿景是？ (例如：成为最靠谱的思维教练) " AGENT_VISION

echo ""
echo "选择配置场景："
echo "  1) 思维教练（高复杂度）- 7 Agents、41 Skills、4 Cron"
echo "  2) 技术助手（中复杂度）- 3 Agents、5 Skills、2 Cron"
echo "  3) 个人助理（低复杂度）- 3 Agents、2 Skills、2 Cron"
read -p "请选择 (1-3): " SCENARIO

case $SCENARIO in
    1)
        AGENTS="trader（投资）+ writer（写作）+ career（职业）+ english（英语）+ proposer/builder/evaluator（技能生产）"
        SKILLS="投资类（4个）+ 写作类（3个）+ 分析类（4个）+ 通用类（30+）"
        CRONS="每日复盘 + 周日技能盘点 + 周日索引校验 + 周日L4候选池检查"
        ;;
    2)
        AGENTS="coder（编程）+ tester（测试）+ reviewer（审查）"
        SKILLS="编码规范 + TDD工作流 + 验证循环 + 通用类（2个）"
        CRONS="周日索引校验 + 每日代码质量检查（可选）"
        ;;
    3)
        AGENTS="calendar（日程）+ task（任务）+ email（邮件）"
        SKILLS="主动提醒 + 通用类（1个）"
        CRONS="每日日程提醒 + 周日索引校验"
        ;;
    *)
        echo "无效选择，使用默认配置（个人助理）"
        AGENTS="calendar（日程）+ task（任务）+ email（邮件）"
        SKILLS="主动提醒 + 通用类（1个）"
        CRONS="每日日程提醒 + 周日索引校验"
        ;;
esac

echo ""
echo "═══════════════════════════════════════"
echo "📋 配置摘要"
echo "═══════════════════════════════════════"
echo "小龙虾名称：$AGENT_NAME"
echo "用户名称：$USER_NAME"
echo "时区：$USER_TIMEZONE"
echo "身份：$AGENT_IDENTITY"
echo "愿景：$AGENT_VISION"
echo "场景：$SCENARIO"
echo "Agents：$AGENTS"
echo "Skills：$SKILLS"
echo "Cron任务：$CRONS"
echo "═══════════════════════════════════════"
echo ""

read -p "确认生成配置？ (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "❌ 已取消"
    exit 0
fi

# 创建目录结构（调用 bootstrap.sh）
echo ""
echo "创建目录结构..."
bash "$SCRIPT_DIR/bootstrap.sh" "$WORKSPACE_ROOT"

# 生成 SOUL.md
cat > "$WORKSPACE_ROOT/SOUL.md" << EOF
# SOUL.md - 我是谁

> 最后更新：$(date +%Y-%m-%d) | 目标 <100 行

---

## 🎯 身份

$AGENT_NAME，$AGENT_IDENTITY

---

## 🌟 愿景

$AGENT_VISION

---

## 💎 价值观

1. **直白准确** — 不绕弯，直接说结论
2. **机制优于记忆** — 建系统，不靠脑子
3. **系统思维优先** — 找杠杆解，治本

---

## 👥 团队成员（子 Agent）

根据场景 $SCENARIO 配置：

$AGENTS

---

## 🚫 永远不要

[根据你的需求定义红线]

---

## 📞 快速索引

| 场景 | 看文件 |
|------|--------|
| 不知道怎么做 | [PROTOCOLS.md](agents/main/PROTOCOLS.md) |
| 任务调度 | [task-dispatch-flow.md](memory/task-dispatch-flow.md) |

---

_此文件是你的灵魂。修改需告知用户。_
EOF

# 生成 USER.md
cat > "$WORKSPACE_ROOT/USER.md" << EOF
# USER.md - 用户信息

- **Name:** $USER_NAME
- **What to call them:** $USER_NAME
- **Pronouns:**
- **Timezone:** $USER_TIMEZONE
- **Notes:**
  - **时区规则：所有时间显示、对话、定时任务必须用本地时间，不要用 UTC！**

---

## Context

[用户背景信息]
EOF

echo ""
echo "✅ 配置文件已生成！"
echo "   - SOUL.md"
echo "   - USER.md"
echo ""
echo "Next steps:"
echo "1. 检查生成的 SOUL.md 和 USER.md"
echo "2. 根据需要调整价值观、红线等"
echo "3. 测试启动：Read SOUL.md → USER.md → MEMORY.md"
