# Task Pilot — Task Decomposition & Execution Framework for Claude

> Breaks complex work into verified subtasks, plants context anchors to survive compaction, and never loses track of where you are.

[![clawhub](https://img.shields.io/badge/clawhub-task--pilot-blue)](https://clawhub.ai/skills/task-pilot)
[![thinkstack](https://img.shields.io/badge/ThinkStack-3%2F3-purple)](https://clawhub.ai/skills/task-pilot)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

Long tasks break in two ways. First, scope drift — execution slowly wanders away from the original goal. Second, context loss — compaction or a long session wipes the working state and Claude starts guessing where it was. Both cause rework.

Task Pilot solves both.

## What it does

**Plan first** — creates a numbered task plan before taking any action  
**Step checkpoints** — marks each step complete with what was produced and what's next  
**Context anchors** — periodic snapshots that survive compaction and let any session resume  
**Recovery protocol** — structured way to pick up exactly where things left off  
**Completion gate** — task is done only when success criteria are verified, not just "done"  
**Scope discipline** — scope expansions require an explicit plan update, not silent drift

## The Anchor Format

```
[Context Anchor]
Task: ...
Completed: steps 1–N ✓
Current: step N+1
Remaining: steps N+2 to end
Key decisions locked: ...
```

Planted every 8–12 exchanges. Short enough to be free, valuable enough to save hours.

## Installation

```bash
openclaw install task-pilot
```

## ThinkStack

Task Pilot is part of the **ThinkStack** — three skills that make Claude smarter at every stage:

```
clarity-first  →  deep-think  →  task-pilot
 understand        analyze        execute
```

```bash
openclaw install clarity-first
openclaw install deep-think
openclaw install task-pilot
```

## Keywords

task decomposition · task management · context management · multi-step tasks · execution framework · context compaction · checkpoint · subtask tracking · project management · agent framework · context loss recovery · long context · plan before execute · scope management · AI agent improvement · smarter Claude · 任务拆解 · 上下文管理 · 多步骤执行 · 防止上下文丢失

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/task-pilot)
