# Templates

Adapt these examples to the indexed files and conventions of the current workspace.

## Lightweight memory capture

```markdown
## Learning Loop
- Correction: ...
- Error: ...
- Feature request: ...
- Better practice: ...
```

## Incident entry

```markdown
## [ERR-YYYYMMDD-XXX] short-name
- Logged: 2026-03-21T13:00:00Z
- Priority: medium
- Reproducible: unknown
- Status: pending
- Context: what failed
- Suspected cause: short note
- Suggested fix: short note
- Related files: path/to/file
```

## Feature request entry

```markdown
## [FEAT-YYYYMMDD-XXX] short-name
- Logged: 2026-03-21T13:00:00Z
- Requested by: user | operator | agent
- Priority: medium
- Scope: medium
- Status: pending
- Context: what capability was requested
- Suggested next step: short action
```

## Decision memo starter

```markdown
---
title: Short decision title
authority: authoritative
owner: system
date: 2026-03-21
topics: [topic1, topic2]
---

# Decision

## Decision

What was decided.

## Why

Why it was chosen.

## Consequences

What changes because of it.
```
