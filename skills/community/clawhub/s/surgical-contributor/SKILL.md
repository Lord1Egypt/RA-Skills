---
name: surgical-contributor
description: Deliver small, high-signal contributions by finding and fixing one real pain point with the narrowest safe change, adding regression protection, and writing a maintainer-friendly PR summary. Use for bug fixes, workflow paper cuts, state/caching correctness issues, startup/config/platform edge cases, and UI-backend behavior drift where low review burden and low merge risk matter.
---

# Surgical Contributor

## Overview

Execute a disciplined contribution loop: reproduce, isolate, patch minimally, and protect against regressions.

Optimize for:
- Mergeability
- Trust
- Behavior stability

## Core Principles

These principles govern all decisions:

- Think before coding: do not assume; surface uncertainty early
- Simplicity first: prefer the smallest solution that fully solves the problem
- Surgical changes: touch only what is required for the fix
- Goal-driven execution: define success via reproduction and verification

If uncertain:
- state assumptions explicitly
- prefer clarification over guessing
- choose the safer, narrower change

## Contribution Doctrine

Apply this doctrine in every run:

- Regression-first
- Minimal-diff
- Maintainer-friendly

Refuse these by default unless explicitly requested:

- Broad refactors
- Speculative architecture shifts
- Opportunistic style rewrites
- Feature expansion beyond the bug or paper cut

## What “Surgical” Means in Practice

- Only modify the minimal set of files and lines required
- Do not change unrelated code, comments, or formatting
- Match existing patterns and conventions
- Do not introduce abstractions unless strictly necessary
- If a smaller patch works, prefer it

Every changed line must trace directly to the identified problem.

## Operating Modes

Choose exactly one mode at the start of work:

1. Bugfix mode  
Reproduce a correctness issue, isolate root cause, apply narrow patch, add regression protection.

2. Paper-cut mode  
Fix high-frequency UX friction in hot paths with minimal behavioral surface area.

3. Refactor-under-permission mode  
Only when explicitly requested; keep each change independently safe and reviewable.

4. Review-my-own-PR mode  
Perform a strict maintainer-style critique before final output (no code changes).

### Non-code repository fallback

If no executable bug exists, treat the repository as a specification system.

Fix exactly one deterministic weakness:
- ambiguity
- missing constraint
- contradiction
- scope leak
- unenforceable rule

Use the smallest reviewable documentation patch.

## Standard Workflow

### 1. Find one pain point

Select one issue that is:
- Reproducible
- Narrow in scope
- High-value

Prefer:
- State/caching bugs
- Edge-case crashes
- UI-backend drift
- Startup/config issues
- Hot-path UX friction

## Stack-Specific Focus

When working in UI-heavy or stateful codebases, prioritize issues where small state mistakes create disproportionate user impact.

Focus areas:

- State synchronization bugs
- Cache invalidation errors
- Selection / batch operation drift
- Undo/redo inconsistencies
- UI-backend contract mismatches
- Interaction edge cases (keyboard, focus, timing)

These bugs often:
- have small fixes
- but high user impact
- and low review resistance when isolated correctly

When available, consult:
- `references/risk-map.md`

Use it during:
- target selection
- self-review

### 2. Write a tiny change plan before editing

Document:

- Observed behavior
- Expected behavior
- Suspected root cause
- Safest seam to modify
- Risk surface

State assumptions explicitly if any uncertainty exists.

### 3. Reproduce first

Create a minimal repro:

- Existing test
- New focused test
- Small harness
- Manual repro if needed

Do not fix before proving the failure.

### 4. Implement the narrowest safe fix

Rules:

- No unrelated cleanup
- Preserve all non-bug behavior
- Prefer local fixes over rewrites
- Avoid new abstractions unless required
- Keep code as simple as possible

If two solutions exist, choose the simpler one.

### 5. Add regression protection

Add exactly one durable protection:

- Automated test (preferred)
- Focused harness
- Manual verification protocol

Tie directly to the reproduced issue.

### 6. Run self-review before finalizing

Checklist:

- Is behavior outside the bug unchanged?
- Are state and cache flows still consistent?
- Are edge cases still safe?
- Are UI/interaction flows intact?
- Is platform behavior safe (if relevant)?
- Is naming consistent with the repo?
- Is this the smallest viable patch?

### 7. Produce maintainer-language PR summary

Use this exact structure:

```markdown
## What broke
<one short paragraph>

## Root cause
<one short paragraph>

## Why this fix is minimal
<scope boundary + reasoning>

## What I tested
<tests / repro / verification>

## What I intentionally did not change
<explicit non-goals>