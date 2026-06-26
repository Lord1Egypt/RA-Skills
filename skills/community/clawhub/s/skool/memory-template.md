# Memory Template - Skool

Create `~/skool/memory.md` with this structure:

```markdown
# Skool Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Boundaries
<!-- When this skill should activate automatically and when it should stay quiet -->

## Group Profile
<!-- What the group sells or delivers, who it is for, and whether it is free, paid, or hybrid -->

## Funnel and Access
<!-- Membership questions, approval rules, invite logic, pricing notes, and course unlock boundaries -->

## Classroom and Calendar
<!-- Course structure, lesson sequencing, event cadence, and what members should do next -->

## Automation Surface
<!-- Approved Zapier flows, webhook hosts, AutoDM rules, and hard no-go automations -->

## Safety and Incidents
<!-- Confirmation policy, repeated failures, rollback moves, and trust boundaries -->

## Notes
<!-- Durable operating observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Group context is still evolving | Keep refining activation, access, and automation defaults |
| `complete` | Baseline is stable | Reuse defaults and focus on execution |
| `paused` | User wants less setup overhead | Save only critical changes |
| `never_ask` | User rejected persistence | Operate statelessly unless asked |

## Key Principles

- Store operating decisions, not full member histories or raw messages.
- Record exact group URLs, plan gates, and automation boundaries only when they change real behavior.
- Keep approval rules and rollback notes explicit whenever the workflow can affect live members.
- Update `last` on each meaningful Skool session.
