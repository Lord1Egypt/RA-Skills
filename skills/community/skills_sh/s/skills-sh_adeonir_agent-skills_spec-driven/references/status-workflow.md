# Status Workflow

Status management for spec-driven features.

## When to Use

Auto-loaded as a reference for feature status transitions. Not a direct trigger.

## Status Values (EXACT)

Use ONLY these values in spec.md frontmatter:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `draft` | Initial state | After `specify` - spec created, may have open questions |
| `ready` | Ready for implementation | After `design` - spec complete, architecture defined |
| `in-progress` | Being implemented | After first `implement` task starts |
| `to-review` | Implementation complete, awaiting Goals/Success audit | After `implement` finishes all tasks and per-task verify passes |
| `done` | Complete | After `audit` confirms Goals and Success Criteria are met; the spec dir moves to `.artifacts/archive/` |

## Status Transitions

```text
draft --[design]→ ready --[implement]→ in-progress --[implement done]→ to-review --[audit]→ done
```

## Who Updates What

| Reference | Updates Status | From | To |
|-----------|---------------|------|-----|
| `specify.md` | Yes | - | `draft` |
| `design.md` | Yes | `draft` | `ready` |
| `tasks.md` | No | - | - |
| `implement.md` | Yes | `draft` or `ready` | `in-progress` |
| `implement.md` | Yes | (all tasks done + per-task verify passed) | `to-review` |
| `verify.md` | No (only marks AC `[x]` in spec.md body) | - | - |
| `audit.md` | Yes | `to-review` (+ tests green, + `uat: pass` if user-facing) | `done` |
| `validate.md` | No (sets `uat:`; may revert AC/Goal/Success `[x]` if UAT reproves) | - | - |

**Branch ownership:** `specify.md` records the intended branch name in spec.md frontmatter only; `implement.md` Step 3 creates/switches to the branch before any code is written. No other reference touches git refs.

## Critical Rules

1. **ONLY use the 5 values above** - never invent new status values
2. **Check current status before updating** - read spec.md frontmatter first
3. **Update at the END of the phase** - after completing all steps of that reference
4. **Never skip status** - follow the flow

## Status Field

The full spec.md frontmatter is canonical in [specify.md](specify.md) --
do not re-spell it here. This reference owns one field, `status`, whose
only valid values are:

```yaml
status: ready  # draft | ready | in-progress | to-review | done
```

The `review` field (`pending | pass | changes`) is a separate spec-quality gate
owned by specify.md Step 16 -- it does not transition with `status`.

The `uat` field (`pending | pass | changes`) is the UAT verdict owned by
validate.md; for `user-facing: true` features audit holds `done` until `uat: pass`.
Like `review`, it does not transition with `status`.

## Common Mistakes to AVOID

- `status: planned` -> Use `ready`
- `status: wip` -> Use `in-progress`
- `status: completed` -> Use `done`
- `status: finished` -> Use `done`
- `status: in_review` -> Use `to-review`
- `status: pending` -> Use `draft` or `ready`
- `status: archived` -> Use `done` (archiving is a file move at `done`, not a status: the dir moves to `.artifacts/archive/`)

## Quick Reference

- Just created feature? -> `draft`
- Design complete? -> `ready`
- Started coding? -> `in-progress`
- All tasks done, per-task verify passed? -> `to-review`
- Goals and Success Criteria audited and met? -> `done`
