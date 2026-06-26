---
name: safe-long-run-mode-gpt54-claude
description: Operate long-running AI tasks safely across GPT-5.4 and Claude by using model selection rules, phased execution, checkpoints, resumable workflows, API throttling discipline, and subagent isolation. Use when a task may run for a while, touch multiple files/systems, involve external APIs, browser automation, Azure, Orgo, or multiple subagents, or when the user asks about long autonomous runs, rate limits, reliability, or safe operating mode.
---

# Safe Long-Run Mode (GPT-5.4 + Claude)

Use this skill for tasks that may run long, span multiple systems, or risk losing progress if interrupted.

## Core rule
Do not run long tasks as one monolithic attempt. Split into phases, write checkpoints, and keep the work resumable.

## Model selection

Use **GPT-5.4** for:
- coding
- docs
- research
- file-heavy transformations
- multi-agent delegated work
- repetitive build tasks
- long internal work where cost and throughput matter

Use **Claude** for:
- strategic judgment
- sensitive decisions
- nuanced synthesis
- client-facing polish
- brand voice refinement
- high-trust orchestration

Default to **GPT-5.4 first**. Escalate to Claude only when the task actually benefits from higher-quality judgment or tone.

## Operating procedure

### 1. Scope before acting
Before starting, decide:
- what the final deliverable is
- which systems/tools will be touched
- what can fail or throttle
- what must be saved after each phase

### 2. Break work into phases
Use phases such as:
1. gather / inspect
2. plan / write brief
3. execute / edit / build
4. validate
5. deploy or report

At the end of each phase, write artifacts to disk.

### 3. Always checkpoint
For long tasks, save progress in files:
- draft outputs
- notes
- reports
- partial results
- tracker entries
- checkpoint summaries

Prefer a resumable workspace state over a perfect one-shot run.

### 4. Isolate long work
Use subagents when:
- the task will take more than a few tool calls
- multiple files/systems are involved
- external APIs are involved
- failure should not pollute the main session
- specialized work can be delegated cleanly

### 5. Throttle external systems
When interacting with Azure, Graph, Orgo, messaging providers, registries, websites, or any external API:
- batch reads when possible
- avoid tight polling loops
- serialize risky writes
- respect retry/backoff
- avoid one-item burst loops when a bulk operation is possible

### 6. Prefer resumability over perfection
The goal is not "never fail." The goal is: if interrupted, resume with minimal loss.

## System-specific guidance

### Azure / cloud control planes
- validate auth first
- create foundational resources first
- verify after each layer
- log resource names/IDs
- do not chain long destructive commands blindly

### Browser / Orgo / GUI automation
- use explicit goals and stop conditions
- capture screenshots at checkpoints
- bound retry counts
- save artifacts locally
- prefer API/CLI over GUI when equivalent exists

### Coding / documentation work
- create a brief/spec first for complex tasks
- write files in chunks
- validate after each major change
- leave notes for resume if work is unfinished

## What to tell the user
When relevant, explain that safe long-run mode means:
- cheapest adequate model
- phased execution
- saved checkpoints
- subagent isolation
- controlled API usage
- resumable progress

## Failure handling
If a long task is interrupted:
1. summarize completed phases
2. point to saved artifacts
3. identify exact next step
4. resume from checkpoint rather than restarting

## References
- Read `references/checklist.md` for a reusable pre-flight checklist and model routing matrix.
