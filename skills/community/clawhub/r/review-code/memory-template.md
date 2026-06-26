# Memory Template - Review Code

Create `~/review-code/memory.md` with this structure:

```markdown
# Review Code Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Review Defaults
severity_threshold:
confidence_floor:
delivery_mode: quick | standard | deep

## Project Context
primary_stack:
critical_paths:
release_risk_profile:

## Known Constraints
test_limits:
environment_limits:
non_goals:

## Recent Patterns
- recurring defect class
- risky module
- fix strategy that worked

## Notes
- facts explicitly confirmed by user
- assumptions to revalidate in next review

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Active review support | Keep adapting findings style and risk focus |
| `complete` | Stable review baseline reached | Use lightweight updates |
| `paused` | User paused this skill | Keep context read-only until resumed |
| `never_ask` | User wants no setup prompts | Do not ask setup questions unless requested |

## Optional File Templates

Create `~/review-code/findings/YYYY-MM-DD.md`:

```markdown
# Findings - YYYY-MM-DD

## Scope
- branch:
- files reviewed:
- release context:

## Blocking Findings
- [P0/P1] file:line - issue - impact - fix summary

## Advisory Findings
- [P2/P3] file:line - issue - improvement

## Residual Risks
- remaining risk and monitoring note
```

## Key Principles

- Save only user-approved context.
- Keep logs short, factual, and reproducible.
- Update `last` whenever defaults or constraints change.
