# Memory Template - Self-Criticism

Create `~/self-criticism/memory.md` with this structure:

```markdown
# Self-Criticism Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Context
- Situations where breakpoint critique helps most
- Risk signals that justify an interruption
- Preferred critique depth for low, medium, and high stakes
- Workflows where rework is especially expensive

## Notes
- Confirmed trigger rules worth keeping
- User feedback about too much or too little critique
- Candidate checkpoints to validate through future work

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Trigger map still evolving | Keep learning where critique helps |
| `complete` | Stable breakpoint behavior | Use existing trigger rules by default |
| `paused` | User wants less interruption | Critique only on explicit request or major risk |
| `never_ask` | User does not want setup prompts | Stop asking about integration and learn only from explicit feedback |

## Local Files to Initialize

```bash
mkdir -p ~/self-criticism/archive
touch ~/self-criticism/{memory.md,checkpoints.md,incidents.md}
```

## Templates for Other Files

`checkpoints.md`
```markdown
# Checkpoints

## Confirmed
- [Workflow phase] -> Trigger: [signal] | Depth: light|standard|deep | Ask: [hard question]

## Candidates
- [Possible checkpoint to validate]
```

`incidents.md`
```markdown
# Incidents

## YYYY-MM-DD
- Miss: [what slipped through]
  Late catch: [when it surfaced]
  Better breakpoint: [where critique should have interrupted]
  Promote: no | candidate | yes
```

## Key Principles

- Keep durable trigger rules in natural language, not hidden config jargon.
- Save reusable insertion points, not full narrative postmortems.
- If a lesson is still uncertain, keep it in Notes or mark it as a candidate checkpoint.
- Critique memory should stay small enough to read before important work.
