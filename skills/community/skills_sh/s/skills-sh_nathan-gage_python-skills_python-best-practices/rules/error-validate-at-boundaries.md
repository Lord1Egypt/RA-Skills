---
title: Validate Input at System Boundaries
impact: MEDIUM
impactDescription: fails fast and prevents bad data from spreading
tags: error, validation, boundaries
references: https://docs.pydantic.dev/latest/concepts/validators/
---

## Validate Input at System Boundaries

Validate once, at the edge — not repeatedly in every internal function. Sprinkling defensive checks throughout the call chain "in case something got through" bloats internals without catching anything a boundary check didn't. Push validation to the boundary (API handler, CLI entrypoint, deserialization), then trust the validated value.

**Incorrect (validation scattered through every internal function):**

```python
def process_order(order_id: str) -> None:
    if not order_id:
        raise ValueError("order_id required")
    order = load_order(order_id)
    fulfill(order)

def load_order(order_id: str) -> Order:
    if not order_id:  # checked again
        raise ValueError("order_id required")
    ...

def fulfill(order: Order) -> None:
    if not order.id:  # and again
        raise ValueError("order has no id")
    ...
```

Every internal function re-validates. If the validation rule changes (e.g., order IDs must match a pattern), every copy must change.

**Correct (validate at entry; trust internally):**

```python
# boundary: the API handler
def handle_fulfill_request(req: Request) -> Response:
    try:
        body = FulfillRequest.model_validate(req.json())  # Pydantic does the work
    except ValidationError as e:
        return error_response(400, str(e))

    process_order(body.order_id)
    return success_response()

# internal: takes a validated value, trusts it
def process_order(order_id: OrderId) -> None:
    order = load_order(order_id)
    fulfill(order)
```

One validation point. Internal code takes `OrderId` (a branded `NewType`) and trusts it — the validation already happened.

**Boundaries that need validation:**

- HTTP request parsing (headers, path params, query strings, body)
- CLI argument parsing
- Reading files or database rows that originated outside the system
- Message queue consumers
- Foreign API responses

**Heuristic:** data at a boundary is untrusted. Validate it into a typed model (Pydantic, dataclass with a validator, `NewType` + explicit check). Once validated, the typed model flows through internal code unchecked.

**Fail fast:** validate before expensive operations. Don't read a 10MB file, parse it, and *then* reject it for missing a required field — check the field first.
