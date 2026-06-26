---
name: usable-stability-loop
description: "Help agents ship usable, stable solutions faster for non-technical but goal-clear users, then improve them through real-world usage instead of over-engineering upfront. Use when the user wants fast development, efficient deployment, continuous evolution, an 80/20 build strategy, protection against over-engineering, or a reusable execution rule for usable first, stable first, iterate in real use delivery."
---

# Usable Stability Loop

A delivery principle for agents serving people who **do not have a programming background but do have clear goals**.

The promise is simple:
- help the user get to a working result quickly
- keep the result stable in real use
- avoid wasting time on over-built product layers
- let the system improve gradually through actual usage

Apply the **99/80 Loop**:
- **99 for usability**: the thing must work for the intended user.
- **99 for stability**: the thing should not feel fragile in normal use.
- **80 for polish**: once usable and stable, stop polishing by default.
- **Iterate from real use**: only spend the last 20 when actual usage exposes friction.

## What problem this skill solves

Many agent builds fail in one of two ways:
1. they stay in design mode too long and never become genuinely usable
2. they keep adding polish, interfaces, and architecture after the real need is already solved

This skill gives the agent a durable operating rule for:
- **fast development**
- **efficient deployment**
- **continuous evolution**

without drifting into over-engineering.

## Who this is for

Use this skill especially when the end user is someone like Mr.Soda:
- not a programmer
- clear about the outcome they want
- willing to accept an 80-point release if it is truly usable and stable
- prefers improvement through real use, not speculative design

## Product positioning

Think of this as a lightweight execution philosophy:
- **usable first**
- **stable first**
- **ship early**
- **evolve through use**

It is not a framework for maximum sophistication.
It is a rule for getting real work into users’ hands quickly and safely.

## High-conversion use cases

### 1. Ship an internal tool MVP for a non-technical user
Use this skill when an agent needs to deliver a working tool quickly without getting trapped in UI polish, framework choices, or speculative architecture.

### 2. Keep a knowledge base or workflow project from becoming over-productized
Use this skill when an agent is building a database, research workflow, or operating system and needs a scope governor: make the workflow usable first, delay dashboards and abstractions until usage proves the need.

### 3. Give a multi-agent system a shared execution rule
Use this skill as a system-level constraint so multiple agents optimize for usability and stability first, stop polishing after the solution is genuinely usable, and evolve only from recurring friction in real use.

## Core rules

1. Put **functional usability** first.
2. Put **operational stability** second, at the same priority level.
3. After both are good enough, **converge scope**.
4. Do not add layers for elegance, demos, or technical vanity.
5. Improve through **small, reversible, evidence-based** iterations.

## Decision test

Before adding work, ask:
1. Does this directly improve usability?
2. Does this directly improve stability?
3. Is there a real user pain point already observed?
4. If not, can this wait until actual use proves the need?

If the answer to 1-3 is mostly **no**, defer it.

## Delivery standard

### Must push toward ~99
- Core path works
- Basic errors are handled
- Normal use does not break easily
- Non-technical users can actually use it

### May stop around ~80
- Fancy interface layers
- Deep configuration flexibility
- Full abstraction/refactor passes
- Edge-case polish without observed demand
- “Professional-looking” packaging with no usage value

## Execution pattern

### Step 1: Define the minimum usable outcome
State the smallest version that solves the real problem.

### Step 2: Make it stable
Prefer boring, testable, recoverable choices.

### Step 3: Expose it in the easiest user-facing form
Prefer direct chat usage, simple files, CSVs, or existing tools before building new interfaces.

### Step 4: Stop deliberately
Once the main path is usable and stable, explicitly stop unless there is a concrete next pain point.

### Step 5: Evolve only from evidence
Use real usage, repeated friction, or failed tasks to decide the next improvement.

## Default recommendations

- Prefer **simple artifacts** over product shells.
- Prefer **plain files + stable structure** over heavy frameworks.
- Prefer **one obvious workflow** over many configurable paths.
- Prefer **human-friendly access** over technically impressive internals.
- Prefer **incremental fixes** over redesigns.

## Example triggers

If the user says things like:
- “先做个够用的版本”
- “别过度打磨”
- “没必要炫技”
- “普通用户能用就行”
- “先做到 80 分，后面边用边改”

then follow this skill.

## Anti-patterns

Avoid:
- building dashboards before the data workflow is proven
- adding abstraction layers before repeated reuse exists
- making a UI just to hide a system the user does not need to touch
- polishing low-value edges before the core path is trusted
- calling speculative future-proofing “architecture” when it mainly adds maintenance cost

## Output style when this skill is active

When proposing work, present it in this order:
1. **What is already enough**
2. **What is still required for usability/stability**
3. **What should wait**
4. **What can be learned from real usage later**

Be direct when the user is about to overbuild: say it is unnecessary and recommend the simpler path.
