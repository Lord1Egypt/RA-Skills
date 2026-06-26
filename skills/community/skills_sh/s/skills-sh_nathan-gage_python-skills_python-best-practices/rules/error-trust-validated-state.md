---
title: Trust Validated State Within the Same Trust Domain
impact: MEDIUM
impactDescription: removes clutter without losing real safety
tags: error, validation, defensive, trust-boundary
references: https://docs.pydantic.dev/latest/concepts/validators/, https://docs.python.org/3/library/dataclasses.html#frozen-instances
---

## Trust Validated State Within the Same Trust Domain

Once a value has been validated *and the validated object is immutable, locally constructed, and stays in the same trust domain*, internal helpers can skip re-checking it. The cousin of `types-trust-the-checker`: same principle, but state requires more care because state can change after validation.

**Incorrect (re-checking validated immutable state in the same module):**

```python
class ValidatedOrder(BaseModel):
    model_config = {"frozen": True}
    items: list[Item]
    total: int

    @model_validator(mode="after")
    def _check(self) -> "ValidatedOrder":
        if not self.items:
            raise ValueError("order must have items")
        if self.total < 0:
            raise ValueError("total must be non-negative")
        return self


def fulfill_order(order: ValidatedOrder) -> None:
    if not order.items:           # validator guarantees this
        raise ValueError("order must have items")
    if order.total < 0:           # validator guarantees this
        raise ValueError("total must be non-negative")
    for item in order.items:
        process(item)
```

**Correct (trust the invariant):**

```python
def fulfill_order(order: ValidatedOrder) -> None:
    for item in order.items:
        process(item)
```

**Keep the check when any of these fail:** (1) object is mutable, (2) constructed outside this process (rehydrated from cache, queue, DB), (3) an untyped or plugin caller could produce a bad instance, (4) the object has been exposed to code that might have mutated it. Rehydration is the most common miss — `ValidatedOrder.model_validate_json(...)` freshly out of the validator is fine; the same type pulled from a cache with no re-validation is not.

When you do trust the invariant, a single `assert order.items, "validator guarantees non-empty"` at the entry point documents the reasoning without sprinkling defensive `if` chains through the body.
