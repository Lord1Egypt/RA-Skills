---
title: Rule Title Here
impact: MEDIUM
impactDescription: brief phrase describing the payoff (e.g., "prevents drift between call sites")
tags: tag1, tag2
references: https://primary-source-1.example.com, https://primary-source-2.example.com
---

## Rule Title Here

Brief explanation — one or two sentences. Observational: describe the pattern and what it costs. Avoid "the impulse to avoid" or "the temptation of" framing.

**Incorrect:**

```python
# Bad code example
```

**Correct:**

```python
# Good code example
```

Optional one-paragraph note on nuance, edge cases, or version-specific behavior. Keep it short. Skip if the examples carry the point.

---

## Authoring notes

Target body length: 20–40 lines. One Incorrect block, one Correct block, optional note. Cut enumerated "use X when / use Y when" taxonomies — let the example speak.

### Impact

- `CRITICAL` — prevents a real bug class (data corruption, swallowed cancellations, insecure defaults)
- `HIGH` — meaningful correctness or maintainability win
- `MEDIUM-HIGH` — noticeable improvement worth enforcing
- `MEDIUM` — good practice; clarity or drift prevention
- `LOW-MEDIUM` / `LOW` — style; opportunistic

Reserve `CRITICAL` for bug classes you'd block a PR on. If in doubt, pick `MEDIUM`.

### References

`references` is required when the rule depends on:

- A specific Python version
- Stdlib behavior with versioned semantics
- Third-party library behavior (Pydantic, mypy, ruff)
- A PEP

Link to primary sources. Blog posts drift; PEPs don't.
