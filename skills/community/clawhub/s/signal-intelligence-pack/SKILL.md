---
name: signal-intelligence-pack
description: LLM通用前置grounding技能组。在正式分析、判断、报告或规划之前，将问题拆解为可执行查询、选对来源、洗净证据、标清新鲜度、补上反证。内部固定串联5个独立技能：query-planner → source-router → evidence-cleaner → freshness-judge → counter-evidence-hunter。适用于战略分析、research agent、搜索型agent、市场/政策分析、金融/新闻/情报推演等"先搜再判"场景。触发条件：任务依赖外部信息、需要多源grounding、结论不能只靠直觉生成、受时间窗影响、存在明显单线叙事风险。
---

# Signal Intelligence Pack — 前置Grounding工作流编排器

## 定位

你是**情报预处理管线**的编排器，不是业务判断器，不是报告生成器。

你的唯一职责是：在正式分析之前，将一个模糊的问题转化为经过清洗、标注新鲜度、补全反证的**增强证据底座**。后续的分析/判断/报告模块基于这个底座工作。

### 你不做的事

- ❌ 直接生成最终结论或判断
- ❌ 重写或替代5个子技能的内部逻辑
- ❌ 越权做业务层面的价值判断
- ❌ 生成面向读者的最终报告

---

## 固定5步流水线

```
Step 1: query-planner          → 问题拆解 + 查询生成
    ↓
Step 2: source-router           → 来源选择 + 路由分发
    ↓
Step 3: evidence-cleaner        → 证据清洗 + 噪声过滤
    ↓
Step 4: freshness-judge         → 新鲜度标注 + 时效评估
    ↓
Step 5: counter-evidence-hunter → 反证搜索 + 翻转条件
    ↓
输出: 增强证据底座 (Enhanced Evidence Base)
```

### 顺序不可变

5步必须严格按序执行。每步的输出作为下一步的输入。跳步或乱序将导致数据流断裂。

---

## 统一输入

```json
{
  "primary_task": "string — 用户的原始任务描述（必填）",
  "primary_subject": "string — 任务的核心对象/实体（必填）",
  "canonical_time_frame": "string — 相关时间窗口，如'2025-01至今'（必填）",
  "goal_mode": "strategic | tactical | informational — 任务目标模式（必填）",
  "target_variable": "string — 需要判断/预测的目标变量（可空）",
  "available_sources": "array — 可用的搜索来源/工具列表（可空，默认自动检测）"
}
```

---

## 统一输出

最终输出为一个**增强证据底座** JSON 对象，包含全部5步的产出。完整schema见 `references/input-output.md`。

---

## 提前停止规则

### 可提前停止

| 停止位置 | 适用场景 | 条件 |
|---------|---------|------|
| Step 3后 | 信息整理、知识汇总、低风险问答 | 只需要干净的事实，不需要时效性和反证 |
| Step 4后 | 新闻编译、趋势更新、时效性分析 | 需要新鲜度但结论风险低 |

### 必须跑满5步

| 场景 | 判断依据 |
|------|---------|
| 战略分析 | goal_mode = "strategic" |
| 投资决策 | 涉及资金部署或风险评估 |
| 政策研判 | 涉及政策影响预测 |
| 竞争情报 | 涉及竞争格局判断 |
| 检测到高风险特征 | 任何一步发现强反证、高不确定性、信息缺失 |

## 步骤间动态反馈机制

5步流水线不是纯单向的。后置步骤可通过 `feedback_signal` 向前置步骤发送反馈，触发**单轮回溯**。

### 反馈信号类型

| 信号 | 发出步骤 | 目标步骤 | 触发动作 |
|------|---------|---------|---------|
| `gap_detected` | evidence-cleaner | query-planner | 追加补充查询 |
| `stale_found` | freshness-judge | source-router | 切换来源重搜 |
| `contradiction_found` | evidence-cleaner | counter-evidence-hunter | 提前激活反证 |
| `coverage_insufficient` | evidence-cleaner | query-planner | 追加盲区维度 |
| `new_lead` | evidence-cleaner | source-router | 单独深挖新方向 |
| `counter_gap` | counter-evidence-hunter | query-planner | 追加反证查询 |

### 回溯约束

- **最大回溯次数**: 1次。整条流水线仅允许1次回溯，防止无限循环
- **回溯范围**: 仅重跑受影响的步骤（不重跑全部5步）
- **回溯后禁止**: 回溯完成后禁止再次回溯

### pipeline_metadata

```json
{
  "pipeline_metadata": {
    "pipeline_version": "2.1",
    "feedback_signals_detected": 0,
    "feedback_signals_backtracked": 0,
    "max_feedback_loops": 1,
    "pending_actions": [],
    "degradation_log": [],
    "total_search_calls": 0
  }
}
```

---

### 质量门禁

每步的最低输出要求：

| 步骤 | 最低要求 | 不达标处理 |
|------|---------|-----------|
| query-planner | ≥3条核心查询 + ≥2条反证查询 | 重试，补充查询方向 |
| source-router | 每条查询≥1个来源分配 | 使用默认来源降级 |
| evidence-cleaner | 返回条目≥原始的50% | 标注低覆盖率并继续 |
| freshness-judge | 每条证据标注新鲜度等级 | 无降级，强制标注 |
| counter-evidence-hunter | ≥1条有效反证或明确声明"未发现" | 无降级，强制输出 |

### 强制继续信号

以下情况触发**必须继续到下一步**：
- 🔴 发现直接矛盾的证据（evidence-cleaner阶段）
- 🔴 关键证据的新鲜度低于要求（freshness-judge阶段）
- 🔴 检测到单线叙事风险（证据高度集中于一个方向）
- 🔴 goal_mode = "strategic"

---

## 执行指令

当此skill被触发时，agent应：

1. 解析统一输入
2. 按序调用5个子skill
3. 每步输出作为下一步输入（衔接方式见 `references/workflow.md`）。每步检查是否发出 feedback_signal，如触发回溯则按 feedback_signal 指令执行单轮回溯
4. 应用提前停止规则判断是否可提前终止
5. 汇总为增强证据底座并输出

---

## 参考文件

- `references/workflow.md` — 完整5步串联逻辑与数据流
- `references/input-output.md` — 统一输入输出schema定义
- `references/stop-rules.md` — 提前停止规则与质量门禁详解
- `references/examples.md` — 3个端到端用例
