# Contributing

## Guardrails

- Keep the public package V2-only.
- Keep host glue optional and the core skill host-neutral.
- Prefer config flags and traceability over hidden behavior.
- Preserve staged/tracked/closure semantics unless a bug fix clearly requires otherwise.
- Maintain both frontstage invariants together:
  - valid user-facing text must still deliver
  - internal/tool/fragment residue must not leak

## Before proposing changes

1. Check whether the change belongs in the portable skill core or an optional host addon.
2. If it changes follow-up semantics, explain the runtime effect on staging, tracking, closure, and frontstage delivery.
3. Prefer deterministic checks before live verification.

## Validation

- run a minimal smoke check
- run the targeted harness when a change touches the continuity/follow-up path
- do not rely on subjective frontstage feel as the only proof
