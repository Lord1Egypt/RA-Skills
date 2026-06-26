# Summary Examples

## Updates applied

```text
Update check complete.

Updated skills:
- skill-a: 1.0.0 → 1.0.1
- skill-b: 2.3.1 → 2.4.0

Already current:
- skill-c
- skill-d
```

## No changes

```text
Update check complete.

OpenClaw status is healthy.
All installed skills are already current.
```

## Partial failure

```text
Update check complete, with issues.

Updated skills:
- skill-a: 1.0.0 → 1.0.1

Failed:
- skill-b: network timeout while fetching package

Recommended next step:
- retry `clawhub update skill-b` later
```
