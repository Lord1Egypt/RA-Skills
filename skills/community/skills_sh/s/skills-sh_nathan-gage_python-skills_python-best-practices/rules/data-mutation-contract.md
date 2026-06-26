---
title: Pick a Mutation Contract
impact: HIGH
impactDescription: prevents ambiguous caller expectations
tags: data, mutation, functions, contracts
---

## Pick a Mutation Contract

A function that mutates its input *and* returns the same reference gives callers no way to tell whether to use the return value or the original. Pick one: mutate and return `None`, or clone and return the new value. Never both.

**Incorrect (mutates and returns — callers can't tell which to use):**

```python
def with_pending_action(state: AppState, action: str) -> AppState:
    state.pending_action = action  # mutation
    return state                   # and return
```

A caller reading `new_state = with_pending_action(state, "confirm")` reasonably assumes `state` is unchanged. It isn't. Another caller reads `with_pending_action(state, "confirm")` (ignoring the return) and assumes that's fine. It is — but only because the mutation happened. Two callers, two wrong mental models.

**Correct (mutate, return None):**

```python
def apply_pending_action(state: AppState, action: str) -> None:
    state.pending_action = action
```

The `None` return and the imperative verb (`apply_`) signal that this is a command. Caller knows the input was modified.

**Also correct (clone, return new):**

```python
from dataclasses import replace

def with_pending_action(state: AppState, action: str) -> AppState:
    return replace(state, pending_action=action)
```

`with_` naming signals a functional transform. The input is untouched; the caller must use the returned value.

**Naming conventions:**
- `apply_*`, `set_*`, `update_*_inplace` — mutate, return `None`
- `with_*`, `update_*`, `derive_*` — return a new value, leave input alone

The contract should be obvious from the name and signature without reading the body.
