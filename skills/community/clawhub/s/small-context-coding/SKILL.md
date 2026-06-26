---
name: small-context-coding
description: Efficient coding workflow for small-context models working on medium or large codebases. Use when the user wants to develop, debug, refactor, or analyze code with limited context windows, when tasks should be split into smaller verified steps, when sub-agents may help isolate work, or when long coding sessions need plan files, checkpoints, and strict context discipline.
---

# Small Context Coding

Use this skill to keep coding work effective when the model context is limited.

## Core operating mode

Treat the model as a short-working-memory engineer.
Do not try to keep the whole project in chat context.
Store project state in files and retrieve only what is needed for the current step.

## Default workflow

1. Classify the task size.
2. Create or update a task plan file before broad changes.
3. Read only the minimum files needed to decide the next step.
4. Split the work into small closed loops: inspect -> change -> verify.
5. Use sub-agents only to isolate distinct subproblems.
6. Write checkpoints after each meaningful phase.

## Task size heuristic

### Small
- One file or one obvious fix
- No sub-agent
- No extra planning file unless requested

### Medium
- A few files or one subsystem
- Make a short plan
- Consider one sub-agent for investigation only

### Large
- Multiple modules, unclear root cause, or feature work across boundaries
- Create plan + todo + checkpoint files
- Delegate investigation or isolated implementation to sub-agents
- Keep main session focused on orchestration and decisions

## Required file-based state

For medium or large tasks, create these under a working notes folder such as `notes/<task-slug>/`:

- `plan.md` — goal, constraints, phases
- `todo.md` — actionable checklist
- `checkpoint.md` — current state, decisions, next step

Keep each file short and current.
Do not duplicate long chat history into these files.

## Planning rules

A plan should contain:
- task goal
- current understanding
- files/modules likely involved
- ordered steps
- verification method

If the task changes materially, update the plan before continuing broad edits.

## Context discipline rules

- Never read whole directories into context without a reason.
- Prefer targeted reads and searches.
- Summarize findings into notes instead of carrying raw outputs forward.
- After a phase is complete, compress it into a checkpoint and move on.
- Do not mix unrelated problem threads in one run when avoidable.

## Sub-agent rules

Use a sub-agent when one of these is true:
- investigation can be isolated from implementation
- one subsystem can be analyzed independently
- you need a clean context for an experiment
- the main session is becoming an overloaded coordinator

Do not use sub-agents for trivial single-file edits.
Do not spawn many sub-agents unless there are clearly separate workstreams.

### Good sub-agent tasks
- trace a call chain for one feature
- inspect one module and summarize risks
- draft a patch for one bounded component
- write or repair one test area

Generate brief files with:

```bash
python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/generate_subagent_brief.py "<task-name>" "<scope>" "<verification>" <repo-root>
```

Read `references/subagent-patterns.md` for prompt shapes and `references/usage-guide.md` for a concrete example.

### Main session responsibilities
- define task boundaries
- decide delegation
- merge findings
- choose final implementation direction
- verify final result

## Verification rules

After each implementation step, run the smallest meaningful check:
- targeted test
- lint/typecheck for changed area
- build of affected package
- direct inspection if no automated check exists

Read `references/verification-defaults.md` for stack-specific defaults before choosing a verification command.
Never claim completion without a verification step or explicit blocker.

A task is only done when these are true:
- the requested change is implemented or explicitly blocked
- the notes reflect the current state
- one meaningful verification step has run, or the blocker is named clearly
- the next follow-up is obvious from `checkpoint.md` if more work remains

## Recommended note templates

If notes do not exist, create them from the bundled templates in `references/templates.md`.
For a real task, prefer initializing them with `scripts/init_task.py`.
Read `references/usage-guide.md` when you want a concrete flow for medium or large tasks.
Read `references/verification-defaults.md` when selecting the smallest useful validation command for a stack.

## Anti-patterns

Avoid:
- giant upfront context dumps
- broad refactors without a written plan
- keeping important state only in chat
- asking one session to investigate, design, implement, and validate many unrelated things at once
- using sub-agents just because they exist

## Initialization

To set up a task workspace for medium or large work, run:

```bash
python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/init_task.py "<task-name>" <repo-root>
```

This creates `notes/<task-slug>/plan.md`, `todo.md`, and `checkpoint.md` if they do not already exist.

To verify the helper workflow end to end, run:

```bash
python3 /home/nick/.openclaw/workspace/skills/small-context-coding/scripts/smoke_test.py
```

## Iteration guidance

Keep the skill lean.
Improve it after real use by refining:
- task size thresholds
- sub-agent delegation patterns
- note templates
- verification defaults per language or framework
