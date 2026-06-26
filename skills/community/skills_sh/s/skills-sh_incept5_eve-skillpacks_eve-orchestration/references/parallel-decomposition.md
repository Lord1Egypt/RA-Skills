# Parallel Decomposition Reference

## Quick Decision Tree

1. Read context (`eve job current --json`).
2. If `current_depth >= target_depth`, execute directly.
3. If work can be split into independent deliverables, create children in parallel.
4. Add `waits_for` from parent to each child.
5. Return `json-result` with `eve.status = "waiting"`.

## Child Job Template

```
Target depth: 3 (EPIC). Current depth: 1.
If current depth < target, you may create child jobs and use waits_for relations to parallelize.
If current depth >= target, execute directly.

Scope: <concise child objective>
Deliverable: <clear outcome>
Dependencies: <list if any>
```

## Parallel Examples (Non-SWE)

### Research

- Child A: literature review
- Child B: data collection
- Child C: synthesis outline

Parent waits for all, then integrates.

### Writing

- Child A: outline
- Child B: draft section 1
- Child C: draft section 2

Parent waits for all, then consolidates and edits.

### Ops

- Child A: metrics snapshot
- Child B: logs scan
- Child C: incident timeline

Parent waits for all, then produces summary and next steps.

## Avoid These Patterns

- Creating children for tasks that are not independent
- Returning `waiting` before adding relations
- Chaining children with `blocks` when `waits_for` would suffice
