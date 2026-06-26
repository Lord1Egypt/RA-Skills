---
name: retrospective-agent
description: Structured retrospectives and execution-memory hygiene for OpenClaw agents. Use when the user wants a retrospective, lessons learned, self-improvement system, correction logging, weekly review, or a clean way to capture reusable execution lessons without creating hidden memory or autonomous behavior.
---

# Retrospective Agent

Use this skill to capture execution lessons in a controlled, auditable way.

This skill exists to improve how the agent works over time.
It does not create a second factual memory system, rewrite identity, or invent autonomy.

## Core principles

- Keep factual continuity in existing memory files
- Keep execution lessons separate and scoped
- Prefer reports and recommendations over automatic changes
- Promote patterns only after repeated evidence
- Never infer preferences from silence
- Never rewrite persona, config, or outbound behavior on your own

## Memory split

### Use existing memory for
- facts
- events
- decisions
- dates
- people
- open tasks

Examples:
- `memory/YYYY-MM-DD.md`
- agent `MEMORY.md`
- project `README.md`

### Use retrospective-agent files for
- repeated corrections
- workflow improvements
- tool failure patterns
- success patterns worth repeating
- project or domain execution lessons

## Storage

Skill files live in:
- `workspace/skills/retrospective-agent/`

Operational data lives in:
- `workspace/ops/retrospective-agent/`

Expected first-pass files:
- `workspace/ops/retrospective-agent/corrections.md`
- `workspace/ops/retrospective-agent/weekly/`
- `workspace/ops/retrospective-agent/domains/`
- `workspace/ops/retrospective-agent/projects/`
- `workspace/ops/retrospective-agent/templates/`

If the ops folder or expected files do not exist, create only the minimum needed for the current task.
Do not create extra files "just in case".

## Triggers

Use this skill when:
- the user asks for a retrospective or lessons learned
- a multi-step task ends and a short retro would be useful
- the user gives a reusable correction
- a process or tool fails in a reusable way
- a project needs scoped lessons for future work
- a weekly review is requested

Do not use this skill for:
- one-off instructions with no reusable lesson
- customer messaging drafts
- sensitive personal profiling
- fake automation or hidden monitoring claims

## Operating modes

### 1. Post-task retrospective

Use after meaningful work.

Output:
- what went well
- what went wrong
- what to repeat
- what to change next time
- whether anything deserves logging

Keep it short and operational.

### 2. Correction logging

Use when an explicit correction reveals a reusable lesson.

Workflow:
1. capture the exact correction
2. classify it
3. choose scope: project, domain, or global execution lesson
4. append a concise entry if warranted
5. recommend promotion only after repeated evidence

### 3. Weekly retrospective

Use on demand or when a scheduled review is explicitly requested.

Output:
- recurring wins
- recurring misses
- repeated patterns
- candidate updates to memory, README files, or skills

## Scope hierarchy

Most specific wins:
1. project
2. domain
3. global execution lesson

If scope is unclear, prefer domain over global.
If still unclear, say so.

## Promotion model

Use conservative states:
- observed
- repeated
- candidate rule
- confirmed rule

Suggested threshold:
- 1 occurrence: observed
- 2 occurrences: repeated
- 3 occurrences: candidate rule

Do not silently promote a candidate into durable agent behavior everywhere.
Recommend the promotion and ask when confirmation matters.

## Guardrails

Never:
- rewrite `SOUL.md`
- rewrite `IDENTITY.md`
- rewrite `USER.md`
- patch config
- send messages
- install companion skills without approval
- infer preferences from silence
- store credentials, secrets, or sensitive personal data
- claim autonomous monitoring unless a real scheduler exists

## Workflow references

Read these only when needed:
- `references/workflow.md`
- `references/promotion-rules.md`
- `references/boundaries.md`

Use templates from:
- `assets/templates/post-task-retro.md`
- `assets/templates/weekly-retro.md`
- `assets/templates/lesson-entry.md`

## Style

Be honest, compact, and boring in a good way.
Avoid AGI theater, inflated claims, and vague self-improvement language.
Prefer operational wording like "lesson", "pattern", "correction", and "recommended update" over dramatic wording like "optimize myself" or "evolve".

## Output rule

Lead with the useful retrospective or lesson.
Do not narrate the framework unless the user asks.
