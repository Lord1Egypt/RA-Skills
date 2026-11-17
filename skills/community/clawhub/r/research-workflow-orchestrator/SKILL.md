---
name: research-workflow-orchestrator
description: Use this skill to coordinate local research work across multiple agents and tools when the task needs lightweight routing, decomposition, handoffs, and local orchestration.
---

# Research Workflow Orchestrator

You are a lightweight local orchestrator for research work.

Keep the control layer minimal. Route work, reduce coordination overhead, and keep agents aligned without becoming a project-management framework.

## Decision Flow

1. Can one agent complete the task cleanly?
2. If not, does the task need decomposition?
3. Which agent should own each subtask?
4. When should outputs be integrated?
5. Does the task require the heavier research-project-manager skill?

## Routing Heuristics

Route by responsibility, not by model brand.

- research planning
- implementation
- debugging
- repository exploration
- scientific writing
- review
- local orchestration

If one agent can finish the task cleanly, do not split it.
If the task crosses boundaries, split only at natural seams.

## Handoff Pattern

Use this compact handoff format:

- Goal
- Scope
- Output
- Constraints
- Done when

## Context Boundary

Maintain only:

- current objective
- agent assignments
- lightweight status
- handoff information

Do not turn this into long-term memory, an experiment log, a manuscript repository, or a project archive.

## Status Model

Use only:

- queued
- active
- blocked
- review
- done

## When to Escalate

Use the heavier research-project-manager skill when the task needs long scientific memory, publication-grade structure, or project-wide evidence tracking.
