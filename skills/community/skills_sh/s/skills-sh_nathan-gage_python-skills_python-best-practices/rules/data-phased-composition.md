---
title: Phase Related Optional Fields Into Nested Structs
impact: MEDIUM
impactDescription: one optional check instead of eight
tags: data, modeling, optional, dataclasses
---

## Phase Related Optional Fields Into Nested Structs

When fields are "all present or all absent" in practice, don't model them as eight independent optionals at the top level. The flattened alternative forces consumers to `profile.first_name or defaults.first_name` eight times, and the type says nothing about which fields co-occur.

**Incorrect (twelve independent optionals; co-occurrence invisible to the type):**

```python
@dataclass
class UserProfile:
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    company: str | None = None
    job_title: str | None = None
    billing_address: str | None = None
    billing_city: str | None = None
    billing_zip: str | None = None
    card_last4: str | None = None
    card_brand: str | None = None
    card_expires: str | None = None
```

**Correct (grouped into phases; one optional check per group):**

```python
@dataclass
class Identity:
    first_name: str
    last_name: str
    email: str
    phone: str | None = None

@dataclass
class Billing:
    address: str
    city: str
    zip_code: str
    card_last4: str
    card_brand: str
    card_expires: str

@dataclass
class UserProfile:
    identity: Identity | None = None
    billing: Billing | None = None
```

Consumers check one optional: `if profile.billing is not None: use profile.billing.card_last4`. Every billing field is guaranteed present when `billing` is. The type system enforces the co-occurrence that was always true in practice. Rule of thumb: three or more optionals that always set/unset together belong in a nested struct.
