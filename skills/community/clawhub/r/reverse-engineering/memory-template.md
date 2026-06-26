# Memory Template — Reverse Engineering Operator

Create `~/reverse-engineering/memory.md` with this structure:

```markdown
# Reverse Engineering Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Context
Use this for natural-language notes about how the user likes reverse engineering work framed, when the skill should activate, and what they normally analyze.

## Boundary Defaults
Use this for recurring constraints such as read-only preference, no production probing, or approval requirements for instrumentation.

## Typical Targets
Use this for repeated target types like mobile apps, legacy APIs, binary formats, firmware, or business workflows.

## Notes
Use this for short internal observations that improve future sessions without exposing config-style keys.

---
*Updated: YYYY-MM-DD*
```

Create `~/reverse-engineering/current-target.md` with this structure:

```markdown
# Current Target

## Target
- Name:
- Type:
- Goal:

## Allowed Actions
- Read-only:
- Instrumentation:
- Replay:
- Patching:

## Evidence
- Samples:
- Traces:
- Docs:

## Open Questions
- 

## Next Probe
- 
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning defaults | Keep gathering boundaries and target preferences naturally |
| `complete` | Enough context is known | Activate and work with minimal friction |
| `paused` | User wants less setup | Stop digging for preferences unless needed for safety |
| `never_ask` | User does not want this configured | Do not reopen setup questions unless they ask |

## Key Principles

- Learn from repeated behavior and explicit statements, not from silence.
- Keep durable memory focused on workflow preferences and safe boundaries.
- Store sensitive evidence in the workspace or target-specific files, not in global memory.
