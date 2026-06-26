# Phase 1: Discover

Parse the requirement and build a structured understanding of what the user wants. If the requirement itself is ambiguous, ask the user now.

## What to Communicate

After analyzing the requirement, present these points clearly:

- **Core intent** — what the user actually wants, in one sentence
- **Scope** — what's in, what's implicitly in, what's out
- **Acceptance criteria** — numbered, testable conditions for "done"
- **Constraints** — technical, business, compatibility, performance
- **Key terms** — definitions for any ambiguous or domain-specific terms

Write it naturally. The goal is clarity, not filling in a form.

## Context to Preserve

Before finishing, make sure the conversation retains: the core intent, key scope boundaries, how many acceptance criteria exist, and the most important constraints. A sentence or two is enough.

## Steps

1. TaskUpdate — set Phase 1 to `in_progress`.
2. Analyze the requirement across five dimensions: core intent, scope (in/implicit/out), acceptance criteria (numbered, testable), constraints (technical/business/compatibility/performance), key terms (definitions). Present the analysis clearly.
3. If the requirement has ambiguities that prevent clear scoping (e.g., "add payments" without specifying which methods, "improve performance" without saying for what), ask the user via AskUserQuestion before proceeding. Do not guess.
4. Preserve context for downstream phases.
5. TaskUpdate — set Phase 1 to `completed`.
