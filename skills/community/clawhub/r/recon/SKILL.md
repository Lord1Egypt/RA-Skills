---
name: recon
description: Research and proposal gate for non-trivial coding tasks. Inspects repository state, classifies task complexity, proposes 3-7 task-specific self-rules, produces a structured report (Task / What I found / Unknowns / Anticipated failure classes / Proposed self-rules / Awaiting confirmation), then stops for user confirmation before proceeding. Designed to prevent wasted effort on misaligned plans by surfacing constraints early. Not a substitute for domain expertise - flags unknowns instead of guessing.
license: MIT
---

# Recon

Research and proposal gate before any non-trivial task. This skill inspects your repository, proposes task-specific rules, and presents a structured report that you must confirm before any code is written or commands run. The stop is the point - without it, agents waste effort on misaligned plans.

## When this runs

This skill activates on ANY of these triggers:

- Start of any task that touches more than one file
- Any task involving network calls
- Any task involving data processing
- Any task involving writing to disk outside the current working directory
- Any task the user describes as "big", "long", or "risky"

State explicitly: do not skip this even for tasks that look simple, because simple-looking tasks are where the expensive mistakes come from.

## Procedure

### 1. Inspect

Read these files to understand context:
- README.md if present
- AGENTS.md if present  
- CLAUDE.md if present
- List of files relevant to the task
- Entry points for the application
- Configuration files (package.json, pyproject.toml, Cargo.toml, etc.)

Identify: language, framework, test setup, build system, deployment targets.

### 2. Classify

State the task type explicitly using one of these categories:

- bugfix
- feature
- refactor
- data-processing
- training
- deployment
- other

### 3. Propose self-rules

Write 3-7 numbered rules. Each rule must be specific, checkable, and scoped to THIS task only (not forever). Rules should be narrow enough to verify but broad enough to matter.

Good self-rules:

1. All database migrations must be backward compatible: new columns nullable, new tables empty on first deploy. Checkable via migration diff inspection; scoped to schema changes.
2. Every new API endpoint must include rate-limit headers and response-time SLA documentation. Checkable via header inspection; scoped to public APIs.
3. UI component commits must include an accessibility checklist: color contrast >= 4.5:1, keyboard navigation, screen reader labels. Checkable via automated audit plus manual review; scoped to UI layer.

Bad self-rules:

1. Always write good code. Uncheckable, subjective, not specific to this task.
2. Security is important. Universal truth, adds no actionable constraint, cannot be verified.
3. Don't break things. Vague, everyone agrees, no guidance on what "breaking" means.

### 4. Produce the report

Output exactly this template so the agent knows the format:

```markdown
## Reconnaissance Report

### Task
[one paragraph describing the task]

### What I found
- [bullet list of concrete facts from inspection]
- [more findings]

### Unknowns
- [things you could not determine; be honest about gaps]
- [missing information that blocks progress]

### Anticipated failure classes
1. [class of failure, e.g. "data shape mismatch"]
2. [class of failure, e.g. "empty input file"]
3. [class of failure, e.g. "API rate limit"]

### Proposed self-rules
1. [rule 1]
2. [rule 2]
3. [rule 3]

### Awaiting confirmation
Reply "confirmed" or "change: [what to change]".
```

### 5. Stop

Do not write any code. Do not run any command beyond inspection. Do not make a plan beyond the report. Wait for the user.

The purpose of this skill is to prevent wasted effort, not to complete work. Stopping is the job.

## Rules for this skill

- If the user replies "confirmed", proceed using the proposed self-rules as binding constraints.
- If the user replies "change: X", revise the report and stop again.
- If the user replies with anything else, treat it as a change request.
- Never skip the stop. The stop is the point.

## Common mistakes

- Writing code before the user confirms. The confirmation gate is the entire point of this skill.
- Proposing vague self-rules like "be careful" or "write good code." Every rule must be checkable.
- Skipping the inspection step and going straight to a report. The report must be grounded in what you actually read.
- Treating the report as a formality. If you have nothing useful to say in "Unknowns" or "Anticipated failure classes," you did not inspect carefully enough.
- Continuing after a "change: X" reply without revising and stopping again.
