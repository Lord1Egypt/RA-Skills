# Requirement Card Template

Copy to `backlog/R-###.md`. id auto-increments, starting from R-001, never recycled.

````markdown
---
id: R-001
title: <one-line description of the requirement>
status: draft
priority: medium              # high / medium / low
depends_on: []                # dependency requirement ids, e.g. [R-002]
conflicts_with: []            # semantically conflicting requirement ids
created: YYYY-MM-DD           # written once at creation
updated: YYYY-MM-DD           # refreshed on every change
---

## Background / Goal
## Acceptance Criteria
## Design Doc        → link docs/superpowers/specs/<date>-<topic>-design.md
## Implementation Plan → plans/<id>.md (relative to the project's global root, generated at dispatch)
## Acceptance Record  → filled after merge: test results / review verdict
````
