---
name: tesp
description: Enforce the Task Execution Signal Protocol for non-instant work so execution stays visible, staged, versioned, and auditable. Use when a task will take more than an immediate reply, spans multiple steps, needs async follow-through, involves cross-agent coordination, or requires active progress signaling, blocker escalation, queue hygiene, or result handoff. Trigger on requests about long tasks, execution tracking, task orchestration, status visibility, rollout audit, progress cadence, task boards, or reducing the need for the human to chase updates. 中文简介：用于非即时任务的任务执行信号协议。适用于长任务、多步骤任务、异步执行与多 agent 协作场景，要求快速接收确认、阶段进度广播、阻塞升级、任务看板与结果落位，并通过版本可见、数字进度、活跃板/归档板和低 token 巡检，避免人类反复追问状态。
---

# TESP

Apply TESP whenever silence would create coordination risk.

## 中文简介

TESP（Task Execution Signal Protocol / 任务执行信号协议）是一套面向非即时任务的执行治理协议。
它的核心不是“把任务做完”本身，而是让执行过程对协作者可见、可查、可监督。
适用于研究、迁移、排查、实施、跨 agent 协作、异步任务和任何需要持续推进但不能静默消失的工作。

## What this skill is for

TESP turns long or multi-step work into a visible execution flow.
It is for tasks that need acknowledgement, staged progress, blockers, active task tracking, and clean handoff discipline.

Typical triggers:
- “Do this and keep me posted.”
- “Break this big task down and supervise execution.”
- “Set a working protocol so I don’t need to chase status.”
- “Audit whether agents are actually following the execution standard.”
- “Clean up the task board so only current work stays visible.”

## Core operating sequence

Follow this order:
1. **Acknowledge fast** — send Layer 1 with visible TESP version, scene, and goal.
2. **Stage the work** — if the task is long, split it into numeric progress units like `2/5`.
3. **Broadcast by cadence** — update based on expected duration, not random chatter.
4. **Track active work** — keep current tasks in `TASK_QUEUE.md`.
5. **Archive finished work** — move completed items into `TASK_ARCHIVE.md`.
6. **Escalate blockers clearly** — say what is blocked and what decision is needed.
7. **Keep audits cheap** — prefer file checks, diffs, and samples over full replay.

## Minimum operating requirements

For any non-instant task:
- Use Layer 1 acknowledgement with visible TESP version.
- Use numeric progress for long tasks.
- Keep active and completed work separated.
- Do not make the human chase status.

## Multi-agent rule

When multiple agents are involved:
- update the task board first
- write the shared handoff second
- then transfer execution

## Model rule

Use `GLM` / `MiniMax` by default for lightweight governance, queue checks, and audits.
Upgrade only when stronger reasoning is actually needed.

## Read next

For the full protocol text and exact templates, read:
- `references/protocol.md`
- `references/templates.md`
