---
name: token-optimizer
description: >
  AI Agent 项目的 Token 消耗审计与系统性优化。提供四层诊断框架、六步优化 SOP、
  自动化审计脚本。适用于任何使用 Rules + Memory + Knowledge + Skills 架构的
  AI Agent 项目（如 CodeBuddy、Cursor、Windsurf 等）。
  This skill should be used when users mention token optimization, context size reduction,
  prompt cost control, or AI agent operational efficiency.
  Triggers: token优化, token节约, token审计, 省token, 上下文膨胀, context太大,
  对话成本, rules瘦身, memory清理, 知识库精简, 降低开销, token consumption,
  optimize tokens, reduce context, context optimization, prompt cost.
---

# Token Optimizer

**Purpose:** 系统性审计并优化 AI Agent 项目的 Token 消耗，降低 30%+ 固定开销。

## Core Concept

每次 AI Agent 对话都有固定的"上下文税"——Rules、Memory、Knowledge 在每轮注入 prompt。固定开销 × 对话轮数 = 真正的消耗大头。

```
┌─────────────────────────────────────┐
│     用户可见的对话内容（~40%）        │  ← 你以为的消耗
├─────────────────────────────────────┤
│  Always-on Rules / Memory /         │
│  System Prompt / Knowledge /        │  ← 隐性固定税
│  Skill 指令                         │
└─────────────────────────────────────┘
```

## Four-Layer Diagnostic Framework

按 ROI 从高到低：

| 层级 | 审计对象 | 预期收益 |
|------|---------|---------|
| **L1 Rules** | `.codebuddy/rules/*.mdc` | ~800-2,000 tokens/轮 |
| **L2 Memory** | `update_memory` 条目 | ~500-1,500 tokens/轮 |
| **L3 Knowledge** | 知识库文件 | ~1,000-3,000 tokens/轮 |
| **L4 Behavior** | 运行时行为模式 | 变量，可省数万 tokens |

→ 各层详细策略与判断标准见 `references/optimization-strategies.md`

## Six-Step SOP

### Step 1: Inventory — 建立 Token 消耗基线

运行自动审计脚本建立基线：

```bash
python3 scripts/token_audit.py [项目根目录]
python3 scripts/token_audit.py [项目根目录] --json         # JSON 格式
python3 scripts/token_audit.py [项目根目录] --knowledge-dir /path/to/knowledge  # 自定义知识库路径
```

脚本自动扫描 Rules / Memory / Knowledge，输出每轮固定开销估算和分层诊断建议。

若需手动盘点，参考 `references/optimization-strategies.md` 中的基线计算公式。

### Step 2: Diagnose Rules (L1)

**核心原则：身份铁律 always-on，行为指南 on-demand。**

检查四类问题：重复规则 → 合并；过长规则 → 拆分；可降级规则 → 改 requestable；僵尸规则 → 删除。

→ 判断标准和降级操作清单见 `references/optimization-strategies.md` §L1

### Step 3: Diagnose Memory (L2)

清理三类冗余：已被 Rule 覆盖的 → 删除；一次性事件记录 → 删除；过时信息 → 删除。保留：行为红线、经验教训、仍有效的事实。

目标：Memory 控制在 ~15 条以内，每条不超过 3 行。

→ 清理决策树和格式规范见 `references/optimization-strategies.md` §L2

### Step 4: Diagnose Knowledge (L3)

拆分巨型文件为"精简路由表（~200行）+ 详细内容（按需加载）"。入口文件控制在 200 行以内。

→ 拆分模式和"两跳"加载策略见 `references/optimization-strategies.md` §L3

### Step 5: Optimize Runtime Behavior (L4)

五项行为优化：精准读取（offset/limit）、主动 /compact（>10轮）、subagent 分流、Skill 按需加载、知识两跳检索。

→ 具体操作对照表见 `references/optimization-strategies.md` §L4

### Step 6: Verify & Institutionalize

1. 量化对比优化前后的固定开销
2. 验证降级 Rule 的触发词能正确唤回
3. 将架构决策写入 MEMORY.md
4. 建立守护机制防止开销回弹

→ 守护机制清单见 `references/optimization-strategies.md` §守护机制

## Quick Decision Tree

```
Token 开销过高？
├── 固定开销高 → Step 2 (Rules) / Step 3 (Memory) / Step 4 (Knowledge)
├── 变量开销高 → Step 5 (精准读取 / subagent 分流 / Skill 按需加载)
└── 累计开销高 → Step 5 (主动 /compact)
```

## Tools & References

| 资源 | 路径 | 说明 |
|------|------|------|
| `token_audit.py` | `scripts/` | 自动扫描，输出分层诊断报告 |
| `optimization-strategies.md` | `references/` | 四层诊断的完整操作手册 |
| `real-world-cases.md` | `references/` | 实战优化案例（可选参考） |
