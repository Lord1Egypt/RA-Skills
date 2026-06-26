---
name: spec-first-dev
description: Spec-driven development workflow. Before writing any code, generates a comprehensive SPEC.md covering data models, user flows, API contracts, file structure, and edge cases. Forces the right order — spec first, code second. Prevents building the wrong thing. Use at the start of any non-trivial build task.
argument-hint: [project description or goal]
allowed-tools: Read, Write, Bash, Glob
metadata:
  version: "1.0.0"
  author: "clawsonnet"
  tags: ["development", "spec", "planning", "architecture", "workflow", "tdd"]
---

# Spec-First — Spec-Driven Development Workflow

## Why This Exists
80% of "Claude built the wrong thing" failures come from jumping into code before the spec is clear. This skill forces the right order: **spec → approval → implementation**.

## Trigger
Use at the start of ANY non-trivial build. If the task will touch >2 files or take >15 minutes, run this first.

Invoked as: `/spec-first-dev [brief description of what you want to build]`

Or auto-triggered by phrases like "build me", "create a", "implement a" when the scope is non-trivial.

## Process

### Step 1: Clarify Intent

Parse `$ARGUMENTS` for:
- What is being built (feature, service, script, component, etc.)
- Who uses it (end users, internal tooling, automated pipeline)
- Key constraints (stack, budget, timeline if mentioned)

If intent is ambiguous, ask ONE clarifying question before proceeding.

### Step 2: Explore Existing Codebase

Before speccing anything new, understand what already exists:
- Run Glob to find relevant existing files (configs, schemas, components)
- Run Grep to find related code patterns
- Identify: what can be reused, what must be new, what might conflict

### Step 3: Generate SPEC.md

Write `SPEC.md` to the project root (or current directory). Include:

```markdown
# SPEC: [Feature Name]

## Overview
[1-2 sentences. What this does and why.]

## Data Models
[All entities, fields, types, relationships]

## User Flows / API Contracts
[Numbered steps for each major flow. Include request/response shapes for APIs.]

## File Structure
[New files to create, existing files to modify, with brief reason for each]

## Edge Cases & Error Handling
[Specific scenarios to handle: empty states, failures, invalid input, concurrency]

## Out of Scope
[What we are explicitly NOT building in this task]

## Open Questions
[Any decisions that need input before coding starts]
```

### Step 4: Present and Gate

Output the SPEC.md contents to the user and explicitly pause:

```
SPEC complete. Review above and confirm before I write any code.
Reply 'go' to proceed, or tell me what to change.
```

**Do not write any implementation code until the user explicitly approves the spec.**

### Step 5: Implement Against Spec

Once approved:
- Work through the spec section by section
- Check off items as you complete them
- Flag any spec deviations immediately (don't quietly deviate)
- If a new edge case emerges, add it to the spec and note it

## Output Files

- `SPEC.md` — written in the project root before implementation starts
- (Optional) `SPEC_APPROVED.md` — copy of approved spec for audit trail

## Integration

Works well with:
- Task-tracking tools (prefix each coding session with this skill)
- Code review workflows (attach SPEC.md to PRs)
- Team handoffs (spec is the briefing document)
