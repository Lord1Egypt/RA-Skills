---
name: task-pilot
version: 1.0.1
author: jiajiaoy
homepage: https://clawhub.ai/skills/task-pilot
description: "Task decomposition and execution framework for Claude — breaks complex work into verified subtasks, plants context anchors to survive compaction, and never loses track of where you are."
keywords:
  - task decomposition
  - task management
  - context management
  - multi-step tasks
  - execution framework
  - context compaction
  - checkpoint
  - subtask tracking
  - project management
  - agent framework
  - context loss recovery
  - long context
  - Claude loses context
  - AI forgets
  - AI goes off track
  - context window
  - Claude off track
  - AI planning
  - plan before execute
  - scope management
  - Claude improvement
  - make Claude better
  - improve AI
  - AI agent
  - agentic
  - AI workflow
  - Claude Code
  - LLM tasks
  - ThinkStack
  - 任务拆解
  - 上下文管理
  - 多步骤执行
  - AI跑偏
---

# Task Pilot

Never lose your place in a complex task. Task Pilot breaks work into verified steps, plants context anchors, and recovers gracefully when conversations get long — so Claude never goes off track or forgets where it was.

## The Core Problem

Long tasks break in two ways:
1. **Scope drift** — execution slowly wanders away from the original goal
2. **Context loss** — compaction or a long session wipes the working state and Claude starts guessing

Task Pilot solves both.

## When to Activate

Use Task Pilot when:
- A task has 3 or more distinct steps
- Execution will span many exchanges
- An error in one step would cascade to the next
- You need to hand back to the user at milestones

**Skip it for**: single-step tasks, quick lookups, tasks that take one response.

## The Protocol

### Before Starting: Plan First

Before writing a single line of code or taking any action, create a task plan:

```
[Task Plan]
Goal: ...
Steps:
  1. [ ] ...
  2. [ ] ...
  3. [ ] ...
Success criteria: ...
Risks / dependencies: ...
```

Wait for confirmation (or adjustment) before executing. Never skip the plan.

### During Execution: Step Checkpoints

After completing each step:
- Mark it done: `[✓ Step N — description]`
- State what was produced
- State what comes next
- Flag any deviation from the plan and explain why

If a step fails, say so immediately. Do not silently move to the next step.

### Context Anchors

Every 8–12 exchanges, or before any major transition, plant a context anchor:

```
[Context Anchor]
Task: ...
Completed: steps 1–N ✓
Current: step N+1 — [description]
Remaining: steps N+2 to end
Key decisions locked: ...
Blockers / open questions: ...
```

Anchors are short. They exist to let you — or a future session — resume from exactly this point.

### Recovery Protocol

If context appears lost or compacted:
1. Find the most recent Context Anchor
2. Read the task plan to identify completed steps
3. Resume from the last incomplete step
4. Never redo completed work unless the user explicitly asks

When recovering, announce it:
```
[Recovering from context loss]
Last anchor: step N complete
Resuming at: step N+1
```

### Completion Gate

A task is done when:
- All steps are marked ✓
- Success criteria are met
- Side effects (files changed, state modified, services restarted) are verified
- A brief completion summary is given

```
[Task Complete]
Completed: all N steps ✓
Result: ...
Verified: ...
```

## Scope Discipline

- Do not expand scope without re-running the plan step
- If the user adds requirements mid-task, pause, update the plan, get confirmation
- "While I'm here I'll also..." is a scope violation unless explicitly approved

## Pairs Well With

- **`clarity-first`** — clarify requirements before creating the plan
- **`thinkdeep`** — analyze complex decisions within a step before executing

Install the full ThinkStack for best results:
```bash
openclaw install clarity-first
openclaw install thinkdeep
openclaw install task-pilot
```
