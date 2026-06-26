---
name: seven-step-rigor
description: Force a strict seven-step order of operations for improvement work: clarify outcome, constraints, and success test; delete before optimizing; simplify before accelerating; automate only after stability; prefer end-to-end validation; and keep human updates brief. Use when the user asks to improve, streamline, simplify, automate, harden, refactor, redesign, optimize, or rethink a workflow, prompt, process, architecture, or operating mode.
---

# Seven Step Rigor

Use this skill to keep improvement work in the right order. Do not jump to speed, automation, or extra checks before proving the thing should exist and is shaped correctly.

## Operating rule

Follow these stages in order:

1. Make the requirements less dumb.
2. Delete the part or process.
3. Simplify or optimize only what survives.
4. Accelerate cycle time.
5. Automate.
6. Prefer end-process testing when possible.
7. Keep the human briefed, briefly.

If the task is small, compress the write-up, but keep the ordering.

## Required working format

For substantial work, structure thinking and execution around these fields:

- **Outcome:** what success changes in the world
- **Constraints:** safety, scope, compatibility, reversibility, and time limits
- **Success test:** the smallest clear check that proves the job worked
- **Deletion candidates:** what can be removed entirely
- **Survivors to simplify:** what remains after deletion
- **Cycle-time move:** the feedback-loop improvement worth making
- **Automation decision:** what, if anything, is stable enough to automate
- **Test-placement decision:** why end-process checks are enough, or why an in-process guard must stay
- **Checkpoint:** what changed, why, evidence, next risk

## Stage instructions

### 1) Make the requirements less dumb

Rewrite the ask as outcome, constraints, and success test.

Challenge:

- inherited assumptions
- decorative requirements
- legacy habits
- work that exists only because "that is how it is done"

Ask at most one high-information question when a wrong assumption would be costly. Otherwise make the safest reasonable assumption and proceed.

### 2) Delete the part or process

Attempt subtraction before improvement.

Look for removable:

- steps
- prompts
- branches
- handoffs
- tests
- approvals
- wrappers
- dependencies
- duplicate status updates

Keep a short note of what was deleted and why. Apply deletion pressure hard enough that some things occasionally need to be restored later.

### 3) Simplify or optimize only what survives

Only now simplify structure, wording, state, interfaces, or dependencies.

Prefer:

- fewer branches
- fewer moving parts
- fewer state transitions
- tighter prompts
- simpler interfaces
- convergent logic over special cases

Do not optimize anything whose existence is still in doubt.

### 4) Accelerate cycle time

After the shape is right, shorten feedback loops.

Prefer:

- smaller batches
- earlier proof of correctness
- the smallest meaningful verification gate
- faster local checks before heavier validation

Speed is useful only after direction is credible.

### 5) Automate

Automate only stable, repetitive, well-understood work.

Automation must be:

- reversible
- inspectable
- scoped to a proven need

Do not automate ambiguity, churn, or waste.

### 6) Prefer end-process testing when possible

Default to the latest reliable test that catches the real failure.

Remove in-process checks that only add latency unless they prevent:

- expensive damage
- safety issues
- materially faster diagnosis

Every test or gate must earn its cost.

### 7) Keep the human briefed, briefly

Send concise checkpoints with:

- what changed
- why
- evidence
- next risk

Avoid narration spam. One solid update beats many fragments.

## Default execution checklist

Use this checklist for substantial work:

- requirement rewrite
- deletion candidates
- simplification decision
- cycle-time decision
- automation decision
- test-placement decision
- brief checkpoint with verification

## Quality bar

A good result from this skill usually shows these traits:

- at least one assumption was challenged or removed
- deletion was considered before optimization
- automation was deferred unless stability was demonstrated
- verification matched the real failure mode
- the final update was brief but evidence-backed
