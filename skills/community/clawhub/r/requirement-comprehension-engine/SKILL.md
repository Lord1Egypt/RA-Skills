---
name: requirement-comprehension-engine
description: >
  Advanced requirement comprehension and skill orchestration engine.
  Analyzes complex/multi-step user requests, determines which skills to invoke
  and in what order, builds task decomposition trees.
  Delegates memory management to complex-memory-manager and self-iteration to
  self-iteration-engine for cross-skill consistency.
  Triggers: multi-intent requests, ambiguous instructions, requests spanning
  multiple skill domains, structured requirement analysis.
version: 1.2.0
metadata:
  openclaw:
    emoji: "🧠"
    homepage: https://clawhub.ai/BusTes01/requirement-comprehension-engine
    models:
      - gpt-4
      - deepseek-v4-flash
      - gemini-2.0-flash
      - claude-4-opus
    requires:
      skills:
        - complex-memory-manager
        - self-iteration-engine
---

# 🧠 Requirement Comprehension Engine

A metacognitive skill that equips agents with structured requirement analysis, skill selection & orchestration. Delegates memory management to **complex-memory-manager** and self-iteration to **self-iteration-engine** for cross-skill consistency.

## Core Capabilities

### 1. Requirement Analysis & Decomposition

When the agent receives a complex or ambiguous request:

**Step 1: Intent Classification**
- Parse incoming message for explicit intent signals (verbs, domain keywords, output expectations)
- Classify into: Direct Action / Information Request / Creative Generation / Analysis & Insight / Meta-Request / Multi-Step Workflow
- If ambiguous, flag as **Under-Specified** and use elicitation templates

**Step 2: Structured Decomposition**
Break the request into a tree:
```
Original Request
├── Intent A (primary)
│   ├── Sub-goal A1 → skill/action candidate
│   ├── Sub-goal A2 → skill/action candidate
│   └── Dependency check
├── Intent B (secondary)
│   └── ...
└── Cross-cutting concerns (privacy, cost, performance)
```

**Step 3: Skill Mapping**
For each sub-goal, select the best matching skill:
- Check `name` + `description` of all available skills (always in context as metadata)
- Rank matching skills by semantic relevance
- If no match → fallback to general knowledge
- If multiple → pick the most specific or orchestrate

### 2. Skill Orchestration Logic

| Situation | Action |
|-----------|--------|
| Single clear intent, single skill | Direct invocation |
| Multiple independent intents | Parallel execution |
| Multi-step pipeline (output A → input B) | Sequential orchestration with handoff |
| Full autonomy requested | Analyze, decide, execute, explain |
| Conflicting skill capabilities | Prefer skill with more specific description |

**Handoff Protocol:**
```
[ComprehensionEngine] Handoff: Skill-A → Skill-B
  Context: {user's original intent excerpt}
  Skill-A result: {summary}
  Skill-B requirement: {what Skill-B needs to continue}
```

### 3. Requirement Elicitation Templates

When a request is **under-specified**:

**Pattern A: Missing Output Format**
> "I need to confirm the output format — do you want a daily report, summary, table, chart, code, or something else?"

**Pattern B: Missing Scope**
> "This request seems broad. Could you narrow down the focus? For example: Option A, Option B, or Option C?"

**Pattern C: Ambiguous Intent**
> "I see two possible directions: do you want me to analyze existing data, or go out and collect new data?"

**Pattern D: Multi-Step Confirmation**
> "I plan to do this in three steps: ① collect latest market data ② analyze trends ③ generate a visualization. Does that work?"

### 4. Delegation to Shared Components

| Function | Delegated To | How |
|----------|-------------|-----|
| Persistent memory (T1/T2/T3) | `complex-memory-manager` | Use its encrypt/decrypt, storage conventions, and cleanup protocols |
| Usage logging & performance tracking | `self-iteration-engine` | Use its log format, review cycles, and update matrix |
| Self-iteration decisions | `self-iteration-engine` | Check triggers, run update decision matrix |
| New skill creation proposals | `self-iteration-engine` | Use its proposal template |

## Quick Reference: Skill Selection Flow

```
User speaks
  ↓
Parse & Classify Intent
  ↓
Is it clear? ──No──→ Use Elicitation Templates
  │                     ↓
  Yes←── User clarifies
  ↓
Decompose into sub-goals
  ↓
For each sub-goal:
  ├── Match skill by name+description
  ├── If match: check last-review-date; if >30d → quick scan SKILL.md
  ├── If no match: fallback to general knowledge
  └── If multi-skill: orchestrate (parallel or sequential)
  ↓
Execute & Deliver
  ↓
Log outcome → Delegate to self-iteration-engine
  ↓
[Periodic] Delegate review to self-iteration-engine + memory cleanup to complex-memory-manager
```

## Dependency Check

Before each orchestration run:
1. Verify `complex-memory-manager` metadata description is in context
2. Verify `self-iteration-engine` metadata description is in context
3. If either is missing, they may not be installed — fallback to built-in behavior

---

# 🧠 需求理解引擎

一个元认知技能，赋予Agent结构化的需求分析、技能选择与编排能力。将持久化记忆委托给 **complex-memory-manager**，将自迭代委托给 **self-iteration-engine**，实现跨技能一致性。

## 核心能力

### 1. 需求分析与分解

当Agent收到复杂或模糊请求时：

**第一步：意图分类**
- 解析输入信息的意图信号
- 分类：直接操作 / 信息查询 / 创意生成 / 分析洞察 / 元请求 / 多步工作流
- 若模棱两可，标记为"信息不足"并使用澄清模板

**第二步：结构化分解**
将请求拆解为树状结构

**第三步：Skill映射**
为每个子目标选择最佳匹配skill

### 2. 技能编排逻辑

| 场景 | 行动 |
|------|------|
| 单一明确意图 | 直接调用 |
| 多个独立意图 | 并行执行 |
| 多步流水线 | 顺序编排+交接记录 |
| 用户要求自主 | 分析→决策→执行→解释 |
| 技能冲突 | 选择描述更具体的 |

### 3. 需求澄清模板

在请求信息不足时使用四种追问模式（详见英文版）。

### 4. 委托给共享组件

| 功能 | 委托给 | 方式 |
|------|--------|------|
| 持久化记忆(T1/T2/T3) | `complex-memory-manager` | 使用其加密/解密、存储规范、清理协议 |
| 使用日志与性能追踪 | `self-iteration-engine` | 使用其日志格式、审查周期、更新矩阵 |
| 自迭代决策 | `self-iteration-engine` | 检查触发条件、运行更新决策矩阵 |
| 新技能创建建议 | `self-iteration-engine` | 使用其提案模板 |

## 依赖检查

每次编排运行前：
1. 检查 `complex-memory-manager` 的 metadata 是否在上下文中
2. 检查 `self-iteration-engine` 的 metadata 是否在上下文中
3. 若缺失，可能未安装——回退到内置基础行为

## 参考文件

- `references/orchestration-patterns.md` — 高级多skill编排示例
