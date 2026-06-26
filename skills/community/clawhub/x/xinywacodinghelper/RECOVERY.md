# Recovery System

Triggered when BLOCKED

---

## Failure Types

* REPO_ACCESS_FAILURE
* INFRA_FAILURE
* MISSING_INFO
* NO_PROGRESS

---

## Strategy

### Repo failure

→ ask for path or fix access

### Infra failure

→ fail fast (no retry)

### Missing info

→ read more files

### No progress

→ change approach

---

## Retry Rules

* max 2 retries
* must change strategy

---

## Output

```
[Recovery]
Type: <type>
Action: <what done>
Next: <next step>
```

---

## Rule

Recovery ≠ blind retry
