# Governance Guide

## Layer boundaries

### Durable memory
Use for:
- stable user preferences
- stable agent behavior rules
- long-term constraints
- lasting decisions

Do not use for:
- day-specific blockers
- temporary plans
- unstable hypotheses

### Daily memory
Use for:
- current context
- in-progress state
- temporary blockers
- unresolved ambiguity
- current execution notes

### Learnings archive
Use for:
- reusable debugging results
- tool behavior discoveries
- corrections that change future behavior
- reliable successful paths found after retries

## Promotion rules
Promote an item upward only when it is likely to remain true.

- daily → durable memory: when a task-level note becomes a long-term rule or preference
- daily → learnings: when a task-level result becomes reusable operational knowledge
- learnings → durable memory: only when the learning becomes a stable standing rule

## Demotion / cleanup rules
Move or remove items when:
- a durable rule turns out to be temporary
- a learning is too narrow to be reusable
- a daily note is obsolete after task completion

## Conflict handling
When two layers disagree:
1. trust explicit latest user instruction first
2. then durable memory
3. then latest daily memory
4. then learnings
5. then older history

Always record unresolved conflicts in daily memory.
