---
name: uncagd
description: Validated CAG decision memory for OpenClaw tools, agents, and long-running project sessions.
---

# unCAGd Skill

Use this skill when the user is working on a repo, software project, agent workflow, plugin, MCP server, or multi-step implementation where decisions may matter later.

## When to retrieve memory

Before planning or editing code, call `cag.retrieve` when:
- The user references prior decisions.
- The task is part of an ongoing project.
- The user asks to continue, refine, implement, or fix something.
- The task involves architecture, naming, APIs, tests, security, or deployment.

Use `k=5` unless the user explicitly asks for a broader review.
Set `useEmbeddings=true` only as a secondary ranker when lexical retrieval is weak.

## When to capture a candidate

Call `cag.capture_candidate` when the conversation produces a durable decision such as:
- Architecture choice.
- Naming convention.
- API contract.
- Security constraint.
- Testing strategy.
- Deployment assumption.
- Project-specific behavior.

Captured candidates are not durable until validated.

## When to validate

Call `cag.validate_memory` only when:
- The user explicitly approves the decision.
- A test passes and the decision is tied to that test.
- A PR/commit/doc source is provided.
- The user says to remember the decision for the project.

## Important

Do not store raw assistant guesses as validated memory.
Do not use CAG memory as a replacement for reading the codebase.
Use retrieved decisions as constraints, not as proof of current code state.

## Contradiction workflow

When contradictions are detected:
- Use `cag.resolve_contradiction` with `keep_existing` if the prior decision stands.
- Use `supersede_existing` if policy changed and old validated memories should be deprecated.
- Use `create_candidate` if the new decision needs review first.

## Compression and portability

- Use `cag.compress_memory` to consolidate old validated decisions into one compact, validated summary.
- Use `cag.export_memory` with `format=memory_md` for portable handoff docs.
- Use `cag.import_memory` to rehydrate memory in another workspace.
