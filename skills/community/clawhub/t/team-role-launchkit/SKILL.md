---
name: team-role-launchkit
description: Launch clone-like multi-agent workflows using explicit role prompts (researcher, builder, editor), strict handoff contracts, and shared behavior files for consistent long-running execution.
---

# Team Role Launchkit

Use this skill when a single task needs parallelization or role separation without losing coherence.

## What this skill provides

- 3 role modes: **Researcher**, **Builder**, **Editor**
- A required **handoff contract** to prevent role blur
- Launch prompts to start role sessions quickly
- Guardrails for memory hygiene and approval boundaries

## When to use

Use for:
- complex, multi-step tasks
- tasks crossing research + implementation + communication
- long-running tasks where consistency matters

Avoid for:
- tiny one-shot requests
- deterministic extraction tasks

## Role definitions

- **Researcher**: gather facts/options/constraints; no final outward messaging
- **Builder**: execute implementation and report exact outputs/diffs
- **Editor**: refine final user-facing output without changing core facts

## Orchestration sequence

1. Define objective and constraints.
2. Fill handoff contract from `references/handoff-contract.md`.
3. Run roles in order: Researcher → Builder → Editor.
4. Operator reviews and delivers final result.
5. Capture durable outcomes in memory.

## Non-negotiables

- Every role handoff must include done criteria.
- Receiver must restate scope before acting.
- External/public actions still require explicit approval policy.
- Temporary notes are not durable memory unless promoted.

## Output contract

Return:
- final deliverable
- what changed by role
- unresolved risks/questions
- next best action
