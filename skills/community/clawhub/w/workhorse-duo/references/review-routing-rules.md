# Review Routing Rules

Use this reference when deciding whether a task must go through 小牛, may skip 小牛, or should be judged by the main session.

## Table of contents
- 1. Core routing rule
- 2. Must-review cases
- 3. Skippable-review cases
- 4. Main-session judgment cases
- 5. Examples

## 1. Core routing rule

Default for medium/large execution tasks:
- 小马 executes
- 小牛 reviews
- main session reports

Do not skip QA just because the execution result looks plausible.
Skip QA only when the task is clearly too small or too low-risk to justify the extra loop.

## 2. Must-review cases

Send to 小牛 by default if any of these are true:

- code was changed
- more than one file was modified
- a checklist or implementation milestone is being marked complete
- acceptance criteria were explicitly stated by the user
- the task has regression risk
- the task touches production-facing behavior, integration behavior, automation behavior, or environment setup
- the task includes debugging, refactor, migration, or fix verification
- the task result will be used as a basis for the next round of work

Rule of thumb:
If being wrong would create rework, confusion, or false confidence, route to 小牛.

## 3. Skippable-review cases

QA may be skipped if all of these are true:

- the task is tiny
- risk is low
- no meaningful state was changed
- the main session can verify the answer directly and quickly

Common examples:
- read-only analysis with no edits
- short clarification or recommendation
- tiny formatting/help text tweak with no downstream consequence
- fast factual lookup where dispatch overhead is clearly higher than the value of a second worker

Skipping QA is a performance optimization, not a shortcut habit.

## 4. Main-session judgment cases

Use main-session judgment when the task sits in the gray zone.
Examples:
- a small edit with moderate visibility
- a medium task with low technical risk but high communication importance
- a change that is easy to verify manually from the main session

In gray-zone cases, decide based on:
- blast radius
- reversibility
- acceptance sensitivity
- cost of being wrong
- dispatch overhead

## 5. Examples

### Example A — must review
Task: modify multiple frontend files and update copy/behavior.
Route: 小马 → 小牛.
Reason: multi-file change + visible behavior risk.

### Example B — must review
Task: mark a refactor checklist item as complete.
Route: 小马 → 小牛.
Reason: progress closure should not rely on self-certification.

### Example C — may skip review
Task: summarize a log snippet and explain likely cause.
Route: main session direct, or 小马 only if needed.
Reason: no state change.

### Example D — may skip review
Task: answer a tiny usage question that needs no file changes.
Route: main session direct.
Reason: dispatch overhead exceeds value.

### Example E — main-session judgment
Task: one-file documentation update with moderate importance.
Route: decide case by case.
Reason: low technical risk, but maybe worth QA if it affects a public workflow.
