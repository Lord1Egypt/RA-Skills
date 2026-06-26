---
name: sprint-plan
description: Use when the user asks to create, rewrite, or structure a concise one-week sprint plan, engineering sprint plan, focused project plan, or alignment doc with sprint goal, context, scope, workstreams, done criteria, metrics, and risks.
---

# Sprint Plan

Use this skill to produce a concise sprint planning document for engineering or product alignment.

## Workflow

1. Identify the sprint outcome in one sentence.
2. Add a concise bullet summary beneath the goal.
3. State why this work matters now, using one concrete example if available.
4. Separate current gaps from proposed work.
5. Keep scope explicit: `In Scope` and `Out Of Scope`.
6. Break work into 4-8 workstreams.
7. For each workstream, include `Goal`, `Deliverables`, and `Done when`.
8. Add decision principles only when they clarify tradeoffs.
9. End with definition of done, success metrics, and risks/open questions.

Avoid day-by-day plans unless the user explicitly asks for scheduling.

## Template

```md
# <Sprint Name>

## Sprint Goal

<One clear sentence describing the outcome.>

## Summary

- <Most important outcome or user-visible change.>
- <Main internal/process improvement.>
- <Key automation, quality, or measurement improvement.>

## Context

<Why this matters now. Include a canonical example if useful.>

## Current Gaps

- <What is broken or missing today.>

## In Scope

- <What this sprint will attempt to ship.>

## Out Of Scope

- <What this sprint will intentionally avoid.>

## Workstreams

### 1. <Workstream>

Goal: <Short outcome.>

Deliverables:

- <Concrete deliverable.>

Done when: <Observable completion criteria.>

### 2. <Workstream>

Goal: <Short outcome.>

Deliverables:

- <Concrete deliverable.>

Done when: <Observable completion criteria.>

## Decision Principles

- <Tradeoff or rule that should guide implementation decisions.>

## Definition Of Done

- <Sprint-level completion checklist.>

## Success Metrics

- <Observable outcome or metric.>

## Risks / Open Questions

- <Unresolved assumption, dependency, or risk.>
```

## Style

- Be direct and readable.
- Prefer concise bullets over long paragraphs.
- Keep the doc focused on alignment, not exhaustive execution detail.
- Avoid grand strategy unless the sprint depends on it.
- Preserve user-provided language when it is clearer than generic planning jargon.
