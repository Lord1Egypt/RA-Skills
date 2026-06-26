# Writing Plans — Implementation Plan + WBS Ledger

## Overview

Transform approved design into bite-sized implementation tasks. Each task is 2-5 minutes of work with exact file paths, complete code, and verification commands. Simultaneously create the WBS task ledger with cold-start context briefs and model tier recommendations.

## Step 1: Scope Check

If the spec covers multiple independent subsystems, suggest splitting into separate plans.

## Step 2: Map File Structure

Before defining tasks, document which files will be created/modified and each file's responsibility.

## Step 3: Create Bite-Sized Tasks

Each step is one action (2-5 min):

```
Task 1: Write the failing test → Run → Implement → Run → Commit
Task 2: (same pattern)
```

Each task must contain:
- Exact file paths (Create/Modify/Test)
- Complete code blocks (no placeholders)
- Exact commands with expected output

### Assign Model Tier

为每个任务标注推荐模型层级：

| Tier | 适用场景 | 说明 |
|------|---------|------|
| **fast** | boilerplate、简单重构、配置变更、文件重命名 | 最快的模型即可 |
| **standard** | 常规功能实现、测试编写、中等复杂度重构 | 默认层级 |
| **strong** | 架构决策、跨文件不变式、根因分析、性能关键路径 | 最强模型 |

默认所有任务为 `standard`，仅在有明确理由时升降。

## Step 4: Create WBS Ledger with Context Briefs

为每个任务写 Context Brief（冷启动上下文摘要）。规则：

1. **自包含性**：新 agent 只读 Context Brief 就能开始执行，不需要读其他任务的详情
2. **前置产物**：如果有依赖，说明依赖任务完成后产出了什么（"Task 1 已创建 `src/models/user.ts`"）
3. **涉及文件**：本条任务要修改/创建的精确路径
4. **关键约束**：必须遵守的架构决策、命名约定、技术选型
5. **验收要点**：从 exit_criteria 中摘最关键的 1-2 条

```markdown
## WBS
| ID | Work Package | Dependencies | Context Brief | Exit Criteria | Evidence | Status |
|----|-------------|-----------|---------------|---------------|----------|--------|
| 1  | [Task name]  | -        | [self-contained brief] | [exit criteria] | - | todo |
```

参见 `references/task-ledger-template.md` 中的 Context Brief 编写示例。

## Step 5: Self-Review Plan

1. **Spec coverage:** Every spec requirement has at least one task
2. **Placeholder scan:** No "TBD", "TODO", "implement later"
3. **Type consistency:** Function signatures match across tasks
4. **Context Brief audit:** 每个 Context Brief 是否自包含？新 agent 读了能不能直接执行？

## Step 6: Adversarial Plan Review 🆕

**在给用户看之前**，派一个 reviewer subagent 做对抗性审查。

1. 构造 review prompt（使用 `subagents/plan-reviewer-prompt.md` 模板）
2. 传入：spec 文件 + plan 文件 + WBS ledger
3. Reviewer 按 5 个维度审查：完整性、依赖正确性、粒度假、Context Brief 质量、反模式
4. 收到审查结论后修复所有 Critical 问题
5. 然后将修复后的计划 + 审查报告一起呈现给用户

审查维度速查：

| 维度 | 关键问题 |
|------|---------|
| 完整性 | 每个 spec 需求都有对应 task？缺前置任务？缺测试任务？ |
| 依赖正确性 | 循环依赖？悬空依赖？串行化过度？依赖不足？ |
| 粒度假 | >30 分钟或 >5 文件的任务需拆分；过于琐碎的任务需合并 |
| Context Brief | 自包含吗？有前置产物描述吗？有文件路径吗？ |
| 反模式 | 独立任务串行化？测试放最后？God Task？范围蔓延？ |

**输出**：`docs/spm/reviews/YYYY-MM-DD-plan-review.md`

## Step 7: Execution Handoff

Present to user:
- Plan summary (task count, parallelism opportunities)
- Adversarial review result
- 2 execution mode options:
  1. **Subagent-Driven** (recommended) — fresh subagent per task + WBS binding + cold-start context
  2. **Inline Execution** — execute in this session

## Outputs

- `docs/spm/plans/YYYY-MM-DD-feature-plan.md` — detailed plan
- `docs/spm/ledger.md` — WBS ledger with all tasks + context briefs + model tiers
- `docs/spm/reviews/YYYY-MM-DD-plan-review.md` — adversarial review report
- User-approved execution mode
