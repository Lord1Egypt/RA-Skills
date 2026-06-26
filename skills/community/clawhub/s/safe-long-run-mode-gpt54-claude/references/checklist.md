# Safe Long-Run Checklist

## Pre-flight checklist

Before starting a long task, answer:

1. What is the final deliverable?
2. Which tools/systems will be touched?
3. Which model should own this task first: GPT-5.4 or Claude?
4. Should this be delegated to a subagent?
5. What external systems may throttle?
6. What artifacts must be written after each phase?
7. If interrupted, where do we resume?

## Model routing matrix

| Task type | Preferred model |
|-----------|-----------------|
| Coding / implementation | GPT-5.4 |
| Documentation drafting | GPT-5.4 |
| Research / collection | GPT-5.4 |
| Multi-agent execution | GPT-5.4 |
| Strategic recommendations | Claude |
| Client-facing polish | Claude |
| Sensitive business judgment | Claude |
| Final review of high-stakes output | Claude |

## Phase template

### Phase 1 — Inspect
- gather context
- identify dependencies
- list risks

### Phase 2 — Prepare
- write plan/brief
- create working files
- note checkpoint path

### Phase 3 — Execute
- make changes in chunks
- save outputs continuously

### Phase 4 — Validate
- run checks
- verify outputs
- identify remaining issues

### Phase 5 — Report / Hand off
- summarize work completed
- link artifacts
- identify next step

## Resume note template

```markdown
## Resume Point
- Task:
- Completed phases:
- Artifacts saved:
- Blockers:
- Next exact step:
```
