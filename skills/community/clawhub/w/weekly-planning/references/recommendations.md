# Recommendation file

The shape each weekly-planning pull request writes, kept here so an adapter
can change headings without hunting through the system prompt. The prompt in
`infra/agents/planner.prompt.ts` is what the agent actually follows; if the
two drift, the prompt wins.

Zero active initiatives: one file, `cadence/plan/YYYY-Www.md`.
One or more: one file per initiative, `cadence/plan/YYYY-Www-<slug>.md`.

## Shape (that shape, not this content)

```
---
title: 2026-W36 Agent discoverability
description: The play is declared and idle; the criterion is 14 days overdue.
week: 2026-W36
target: 2026-08-agent-discoverability
---

## What it asked for

The initiative's own success criterion, in its words. Workspace file: what
the declared infra is for, if that can be read from it.

## What ran

Runs, usage, cadence logs, and infra that serve this target. Cite the
`cargo-ai` command that produced a number. Fleet volume is not news.

## The gap

The mismatch, or that the week was on track. Deployed is not running is a
gap. Green run counts are not.

## Recommendations

• Named owner: the action, with the evidence
```

## Rules

- At most three recommendation bullets. Skip the section when the week is
  on track rather than inventing work.
- Do not invent a number. A number returned by a `cargo-ai` read you actually
  ran is evidence; a number no command returned is not.
- Never edit `plan/` or `infra/`. A recommendation is markdown a human
  merges, not a deploy.
- One initiative per file. The workspace file exists only when there are
  zero active initiatives.
