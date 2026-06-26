---
title: Use Discriminated Unions Over Optional Bags
impact: MEDIUM
impactDescription: tags variants explicitly in new designs; retrofit is expensive
tags: data, types, unions, modeling
references: https://docs.python.org/3/library/typing.html#typing.Literal, https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions
---

## Use Discriminated Unions Over Optional Bags

Every optional field is a question the rest of the codebase must answer every time it touches the data. Optional fields accumulate as features grow, producing models where half the combinations are semantically invalid. Use a tagged (discriminated) union so the type system enforces which fields travel together.

**Incorrect (optional fields create impossible state combinations):**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class PaymentState:
    status: Literal["idle", "processing", "settled"]
    gateway: Literal["stripe", "paypal"] | None = None
    transaction_id: str | None = None
    initiated_at: str | None = None
    settled_at: str | None = None
```

When `status == "idle"`, should `gateway` exist? The type says maybe. When `status == "settled"`, is `settled_at` guaranteed? The type says no. Every consumer defensively checks for `None` on fields that must be present, or forgets to check fields that might not be.

**Correct (each variant carries exactly the fields it needs):**

```python
from dataclasses import dataclass
from typing import Literal

@dataclass
class PaymentIdle:
    status: Literal["idle"] = "idle"

@dataclass
class PaymentProcessing:
    gateway: Literal["stripe", "paypal"]
    transaction_id: str
    initiated_at: str
    status: Literal["processing"] = "processing"

@dataclass
class PaymentSettled:
    gateway: Literal["stripe", "paypal"]
    transaction_id: str
    settled_at: str
    status: Literal["settled"] = "settled"

PaymentState = PaymentIdle | PaymentProcessing | PaymentSettled
```

Now `match payment.status:` narrows exactly, `transaction_id` is non-optional on the variants that have it, and impossible combinations (idle with a transaction ID, settled without a timestamp) are unrepresentable.

**With Pydantic** *(applicability: pydantic)*: use `Field(discriminator="status")` and a `status: Literal[...]` tag on each variant — Pydantic will validate and narrow automatically.

**Null over sentinels:** don't invent `"none"` action values. `pending_action: PendingAction | None` beats `pending_action: Literal["none", "confirm-address", "select-shipping"]`. Absence is not an action.

**Related:** `data-explicit-variants` applies the same idea at the behavior level — split a mode-flag class into one class per mode. Use discriminated unions when the variants are data; use explicit variants when the variants have meaningfully different methods.
