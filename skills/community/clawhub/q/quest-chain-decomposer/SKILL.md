---
name: quest-chain-decomposer
description: Break a fuzzy, high-friction goal into a sequenced quest chain with prerequisite nodes, parallel branches, waiting points, Definition of Done, and the first three actions. Use when the user knows the destination but cannot see the first move, keeps stalling mid-project, or needs a practical task map for study, home, admin, or personal projects.
version: v1.0.0
tags: productivity, task-management, gamification, project-planning
---

# Quest Chain Decomposer

Chinese name: 任务链分解器.

## Overview

Use this skill to turn a large or messy objective into a practical quest chain. It keeps the first step small, shows dependencies, and avoids fake progress such as endless research without a deliverable.

## When to use

Use this skill when the user wants to:
- break a goal into a realistic sequence
- identify prerequisite, parallel, and waiting nodes
- define what “done” means for each step
- start today instead of circling the task
- re-route after blockers appear

### Example prompts
- "Break this project into a quest chain"
- "I know what I want, but I cannot find the first step"
- "Map the dependencies for this admin task"

## Inputs

Useful inputs include:
- goal or deliverable
- deadline or time window
- success definition
- resources and constraints
- blockers, approvals, or handoffs

## Workflow

1. Clarify the finish line.
2. Sort work into main quest, prerequisite nodes, parallel branches, and waiting points.
3. Give each step a clear Definition of Done.
4. Make the first move small enough to start immediately.
5. Add reroute rules for common stalls.

## Output

Return markdown with:
- main quest objective
- quest chain map
- Definition of Done by step
- starter trio
- reroute rules

## Limits

- This skill does not replace full project management software.
- For large cross-team schedules, it should stay at the planning level.
- If the goal itself is unclear, define the mission first before decomposing it.

## Acceptance Criteria

- The first quest is small enough to start now.
- Dependencies are visible.
- Each step has an explicit done line.
- The plan points toward a real deliverable, not just thinking about the work.


## Usage Scenarios

| # | User Input | Expected Output |
|---|---|---|
| 1 | "Decompose 'Launch a podcast' into a quest chain with dependencies and effort estimates." | Quest tree: Main Quest → (A) Define niche & format [3h], (B) Procure equipment [4h] → (C) Record pilot [2h, depends on A+B], (D) Edit & mix [4h, depends on C], (E) Submit to directories [1h, depends on D]. Parallel paths marked. Total: 14h. |
| 2 | "I only have 30 minutes today. Which quest in my 'Write a novel' chain gives the highest forward progress?" | Recommends "Outline Chapter 3" (30 min, unblocks 4 downstream chapters) over "Polish dialogue in Chapter 1" (30 min, cosmetic only). Progress-impact score per quest. |
| 3 | "The 'Build a course' quest chain is stale (50% done, no activity in 3 weeks). Should I restart or pivot?" | Chain health assessment: 3 of 6 quests completed. The stuck quest ("Record lessons") is blocked by equipment not yet purchased. Suggests either purchasing equipment or rewriting the quest to use existing phone camera as a temporary path. |


### Scenario 2: 任务太大不知道从哪下手
**User input:** "老板让我做一个完整的年度营销方案，我一看就觉得好难好焦虑，拖了一个月了还没开始。怎么把这任务拆成能马上做的事？"
**Expected output:** 大任务拆解法——第一步：把最终成果拆成3-5个模块（年度营销方案=市场分析、竞品分析、目标用户、策略规划、执行计划、预算评估）；第二步：每个模块再拆成当天可完成的"最小行动"（如市场分析=打开百度/知乎查3篇行业报告+整理5个核心结论+写300字摘要，一天内必须完成这个最小行动）；第三步：每天只做1-2个最小行动，做完就下班不贪多；第四步：障碍识别（如果某个步骤卡住超过2天=拆得更小或换顺序做后面的）；第五步：给自己一个"日终结硬"——每天下班前发一条微信消息给自己：今天完成了什么+明天要做的第一件事。关键：最小行动是要在30分钟内能完成且做完后有明显进步感。
