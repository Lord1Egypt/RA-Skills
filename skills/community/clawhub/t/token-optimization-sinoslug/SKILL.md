---
name: token-optimization
description: Reduce unnecessary token usage with the current production-proven workflow. Use when users ask to optimize token consumption, reduce prompt/context bloat, standardize concise replies, or align token-saving behavior across assistants. Includes only currently implemented practices (no future/experimental tactics).
---

# Token Optimization

Use this skill when the task is about reducing token usage while keeping answer quality stable.

## Workflow

1. Read the current baseline spec first:
   - `references/current-spec.md`
2. Apply only the already-implemented rules from that file.
3. Do not introduce speculative or not-yet-implemented optimization tactics.
4. If asked to change behavior, update the spec and version it.

## Scope guard

- In scope: concise reply behavior, log/tool-output trimming, current token-show usage flow, and currently active execution process.
- Out of scope: future ideas not yet implemented (auto-threshold switching, automatic split replies, weekly auto-reviews), unless user explicitly requests a new version update.

## Output expectation

When asked to explain or sync the optimization plan, provide the “current-state only” version and cite that it follows `references/current-spec.md`.
