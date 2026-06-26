---
name: skill-retrieval-gate
description: "Decide whether to run `memory_search` before following another skill or workflow, so the agent can reduce token usage without forcing retrieval on every task. Use when a task may depend on local knowledge, project history, prior decisions, user preferences, or existing notes, and you need a lightweight rule for when to retrieve, how to query, how much context to load, and when to fall back. Typical triggers include requests like: continue previous work, use project memory first, check what we already documented, base this on existing notes, or decide whether retrieval is worth it before following the skill."
---

# Skill Retrieval Gate

## Goal

Use this skill to decide whether the current task should query `memory_search` before following another skill or workflow.

This skill is for **retrieval judgment**, not mandatory retrieval.

## Core rule

Do **not** make every skill query memory first.

Instead:

1. Judge whether the task depends on local knowledge or history
2. Retrieve only when that dependency is real
3. Load only a few high-signal results
4. Fall back immediately if retrieval is weak, unavailable, or unnecessary

## Example triggers

This skill is especially useful for requests like:

- continue the previous work on this project
- check what we already documented before you proceed
- use project memory first if this depends on earlier decisions
- decide whether retrieval is worth it before following the skill
- base this on existing notes instead of asking me again

## Workflow

### 1. Decide whether retrieval is needed

Use [decision-flow](./references/decision-flow.md) when the request may depend on:

- project history
- prior decisions
- local knowledge bases
- user-specific preferences
- previously organized notes

### 2. Judge the skill tier

Use [skill-tiering](./references/skill-tiering.md) to classify the current skill or task into:

- retrieval-first
- retrieval-optional
- retrieval-usually-skip

### 3. Build the query

Use [query-construction](./references/query-construction.md) to build a compact query from:

- task object
- task type
- key module, symptom, or entity

### 4. Keep the result set small

Use [result-trimming](./references/result-trimming.md) to limit context expansion.

Default rule:

- fetch top 1-3 results first
- only expand deeper when clearly needed

### 5. Fall back fast

Use [fallback-rules](./references/fallback-rules.md) if retrieval is empty, noisy, low-confidence, unavailable, or unnecessary.

## Anti-patterns

Avoid these mistakes:

- forcing retrieval for every task
- copying the entire user prompt into `memory_search`
- expanding every hit just because it matched
- dragging weak or stale snippets into later reasoning
- treating retrieval failure as a blocker instead of falling back

## Output expectation

After using this skill, the agent should be able to answer:

- Should I call `memory_search` for this task?
- What query should I use?
- How many results should I keep?
- Should I fall back to the original skill flow immediately?
