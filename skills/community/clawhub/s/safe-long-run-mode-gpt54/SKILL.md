---
name: safe-long-run-mode-gpt54
description: Operate long-running tasks safely when the environment is optimized for GPT-5.4 as the primary and often only model. Use when the user wants a low-cost, high-throughput long-run workflow, plans to keep everything on GPT-5.4, or asks how to run long coding, research, build, documentation, Azure, or multi-agent tasks safely without relying on Claude.
---

# Safe Long-Run Mode (GPT-5.4 Only)

Use this skill when GPT-5.4 is the default operating model for both orchestration and delegated work.

## Core rule
Use GPT-5.4 for long work by making tasks cheap, segmented, and resumable. Since the model layer is cost-efficient, the real risks are provider throttling, session interruption, and lack of checkpoints.

## When to use this mode
Use it when:
- the user wants to minimize model cost
- the task is implementation-heavy
- the task is file-heavy or repetitive
- multiple subagents may be involved
- external services may throttle
- quality depends more on process discipline than premium model nuance

## Operating procedure

### 1. Route to GPT-5.4 by default
Use GPT-5.4 for:
- coding
- docs
- research
- skills
- website work
- project tracker updates
- internal tooling
- multi-agent delegated work
- long build/test loops

Do not escalate to another model unless the user asks or the task clearly requires premium polish/judgment.

### 2. Split work aggressively
Break long tasks into explicit phases and write down the next step before moving on.

Preferred phases:
1. inspect
2. plan
3. execute
4. validate
5. report

### 3. Save progress continuously
Always leave artifacts that make recovery easy:
- notes
- drafts
- partial outputs
- checkpoint files
- project updates
- result summaries

### 4. Use subagents as workers
For large or parallel tasks, use subagents to keep the main thread clean.
Delegate when:
- tasks are independent
- multiple files or systems are involved
- work may take a while
- specialized roles improve throughput

### 5. Treat external APIs as the true bottleneck
In GPT-5.4-only mode, model cost is not the main concern. External limits are.
Be careful with:
- Azure / Microsoft Graph
- ClawHub / GitHub-backed operations
- Orgo runtime and VM usage
- websites / browser automation
- messaging providers

Use batching, backoff, and fewer larger writes.

### 6. Make every task resumable
If interrupted, resume from artifacts instead of recreating work. Always know:
- what is already done
- what file contains the latest state
- what exact next action should happen

## Ideal GPT-5.4-only use cases
- codebase changes
- documentation builds
- repeated content generation
- Azure script development
- internal automation
- multi-agent production work
- long back-office workflow creation

## What to tell the user
Explain that GPT-5.4-only safe mode works because:
- model cost stays low
- throughput stays high
- reliability comes from checkpoints, not from one giant run
- external APIs, not tokens, usually become the limiting factor

## Failure handling
If interrupted:
1. summarize completed work
2. cite the saved files
3. state the resume point
4. continue from the last checkpoint

## References
- Read `references/checklist.md` for the pre-flight checklist and GPT-5.4 operating pattern.
