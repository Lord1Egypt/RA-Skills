# Conflict Resolution

## Conflict Types

1. context rule conflicts with global rule
2. two context rules conflict (different contexts)
3. duplicate statements with opposite meaning

## Precedence

1. active context rule wins for current task
2. global rule is fallback
3. if same scope conflict exists, latest user-confirmed rule wins
4. if still ambiguous, ask user

## Required Actions

When conflict is detected:
1. apply precedence for this turn
2. log conflict in active `corrections.md`
3. ask a short disambiguation question if behavior may change materially
4. on answer, mark losing rule as archived or scope-limited

## Conflict Log Template

```markdown
- id: CONFLICT-YYYYMMDD-XXX
  rule_a: <id/path>
  rule_b: <id/path>
  applied_rule: <id>
  reason: context_precedence | recency | user_override
  resolved_by_user: yes | no
  timestamp: <ISO-8601>
```

## Anti-Mixing Rule

Never automatically copy context rules into global scope.
Only promote to global via explicit confirmation or multi-context confirmation policy.
