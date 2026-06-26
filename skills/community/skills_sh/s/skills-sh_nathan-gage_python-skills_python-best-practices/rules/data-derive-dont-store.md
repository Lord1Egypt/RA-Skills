---
title: Derive, Don't Store
impact: HIGH
impactDescription: eliminates flag-sync bugs and halves the state space
tags: data, state, derivation, architecture
---

## Derive, Don't Store

Every boolean you add doubles the theoretical state space. When a value can be computed from data you already have, do not store it. Cached derived values require multiple mutation sites to stay in sync — and they won't.

**Incorrect (four flags that must be kept in sync):**

```python
from dataclasses import dataclass

@dataclass
class ThreadState:
    was_interrupted: bool
    did_assistant_finish: bool
    did_assistant_error: bool
    was_tool_call_only: bool

def should_show_footer(state: ThreadState) -> bool:
    return (
        state.did_assistant_finish
        and not state.was_interrupted
        and not state.did_assistant_error
        and not state.was_tool_call_only
    )
```

Four fields to answer one question. Four mutation sites elsewhere that must keep them synchronized. One missed update and the footer lies.

**Correct (derive from the event log):**

```python
def should_show_footer(events: list[SessionEvent]) -> bool:
    latest = get_latest_assistant_message(events)
    if latest is None:
        return False
    return (
        latest.completed
        and not latest.error
        and latest.finish_reason != "tool_calls"
    )
```

The answer is now computed from evidence that already exists. No sync required — one source of truth.

**When NOT to derive:**

- The domain genuinely has a state machine with ordered transitions (a checkout step *is* the state, not a cached conclusion)
- Temporal or external data that cannot be re-derived (timestamps from async processes, API responses needed downstream)
- The derivation is meaningfully more expensive than the stored value *and* you've measured the cost

**The debugging payoff:** pure derivation means tests become data-in, answer-out. Load fixtures, call the function, assert the result. No mocks, no timing reproduction.
