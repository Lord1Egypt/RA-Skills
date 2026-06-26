# Memory Template - Quizlet

Create `~/quizlet/memory.md` with this structure:

```markdown
# Quizlet Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation
- Auto-activate when:
- Activate only on explicit request for:
- Never activate for:

## Study Context
- Primary subjects:
- Target exam or deadline:
- Session length:
- Weekly study capacity:
- Preferred Quizlet modes:

## Set Quality Patterns
- Pattern:
  - Symptom:
  - Rewrite strategy:
  - Verified result:

## Weak Recall Log
- Set:
  - Topic:
  - Miss pattern:
  - Card fix applied:
  - Follow-up date:

## Session Playbook
- Scenario:
  - Objective:
  - Mode sequence:
  - Time split:

## Notes
- Decision:
- Follow-up:

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep capturing study constraints naturally |
| `complete` | Context is sufficient | Execute workflows without setup follow-ups |
| `paused` | User paused setup details | Keep working with existing context |
| `never_ask` | User rejected setup prompts | Do not ask setup follow-ups again |

## Principles

- Keep entries concise, factual, and easy to verify.
- Update `last` after each meaningful study workflow.
- Store patterns and decisions, not sensitive personal data.
- Prefer durable observations over temporary one-off notes.
