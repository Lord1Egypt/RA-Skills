<div align="center">

[![中文](https://img.shields.io/badge/%E4%B8%AD%E6%96%87-GUIDE.md-111827?style=flat-square)](./GUIDE.md) · **English**

# token-efficient-task-router Guide

#### Public Usage Guide (English)

</div>

## What This Skill Does

`token-efficient-task-router` is a control skill that helps an agent decide how to work before it starts spending tokens, loading broad context, editing files, or entering risky execution paths.

It is designed to answer questions such as:

- Is this request clear enough to execute yet?
- Should the agent diagnose, plan, act, or escalate?
- Is the task risky enough to require confirmation?
- Does the user really need a full result, or just the next step, a sample, or staged execution?

## Why It Exists

Many agent failures are not caused by lack of capability, but by the wrong execution order:

- reading too much before understanding the real task
- writing too much before validating scope
- editing too early before confirming file boundaries
- expanding too broadly before proving full delivery is necessary

This skill adds a decision layer before those expensive actions happen.

## The Four Modes

### Ask Mode

Use for explanation, diagnosis, feasibility checks, risk analysis, and next-step advice.

### Plan Mode

Use for multi-step tasks, file-sensitive tasks, batch work, and expensive work where scope should be confirmed before execution.

### Craft Mode

Use for clear, low-risk tasks that can be completed safely in one pass.

### Expert Mode

Use when repeated attempts are failing, deeper specialization is needed, or more trial-and-error is no longer efficient.

## Interactive Routing

When a task is ambiguous, file-related, batch-oriented, or potentially expensive, this skill can ask the user to confirm:

- task complexity
- preferred handling mode
- output depth

This helps reduce wrong-scope execution and unnecessary token spend.

## Progressive Delivery

This skill does not treat “do everything now” as the default.

Preferred progression:

1. decide
2. sample
3. stage
4. fully execute

This makes it a better fit for real-world work, where the correct scope is often discovered as execution progresses.

## File Safety

The skill is deliberately conservative around:

- overwriting core files
- deletion
- batch rename or move operations
- deployment-affecting changes
- database-affecting changes

In these cases, confirmation gates are part of the design, not an optional add-on.

## Platform Behavior

### WorkBuddy

Better suited to read-only analysis, scope confirmation, and sample-batch execution before broad folder-level changes.

### iMA Copilot

Better suited to narrow retrieval, short evidence-based conclusions, and grouped material summaries before long-form expansion.

### CodeBuddy

Better suited to limiting code-reading scope, edit scope, and test scope instead of defaulting to full-repo scanning and broad refactors.

## Example Prompts

```text
Please decide whether this task should use Ask, Plan, Craft, or Expert mode.
```

```text
Use Plan Mode first and do not modify files yet.
```

```text
This is a clear small task. Use Craft Mode directly.
```

```text
Diagnose the issue first and avoid changing code immediately.
```

```text
Use the most token-efficient approach and only give me the next useful step.
```

## What This Skill Does Not Try To Do

It does not try to replace domain skills. It does not try to slow every task down. It does not default to maximum-length output.

Its purpose is narrower: make agent execution safer, cheaper, and more aligned with the user's real need.

---

For the Chinese version, see [GUIDE.md](./GUIDE.md).
