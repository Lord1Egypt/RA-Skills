---
title: Encapsulate Mutable State in the Narrowest Clear Scope
impact: MEDIUM
impactDescription: keeps mutation scoped to the owning object
tags: data, state, encapsulation, scope
references: https://docs.python.org/3/reference/executionmodel.html#naming-and-binding
---

## Encapsulate Mutable State in the Narrowest Clear Scope

Give mutable state the narrowest scope where the surrounding code still reads clearly. A closure fits when the interface is one or two callables and nothing needs to inspect the state. A focused class fits when state has identity — multiple methods share it, or tests, logs, or subclasses need to see it. A wide-open class where every method can touch the state is how invariants rot.

**Incorrect (state visible to every method on the class — too wide):**

```python
class DebouncedWriter:
    def __init__(self, callback: Callable[[], None], delay_ms: int = 300):
        self._callback = callback
        self._delay_ms = delay_ms
        self._timeout_handle: TimerHandle | None = None  # touched by every method

    def queue_send(self, text: str) -> None: ...
    def flush_now(self) -> None: ...
    def something_else(self) -> None: ...  # nothing prevents a bug here
```

**Correct (focused class — state scoped to the methods that need it):**

```python
@dataclass
class DebouncedAction:
    callback: Callable[[], None]
    delay_ms: int = 300
    _timeout: TimerHandle | None = field(default=None, init=False, repr=False)

    def trigger(self) -> None:
        if self._timeout is not None:
            self._timeout.cancel()
        self._timeout = schedule_after(self.delay_ms, self._fire)

    def _fire(self) -> None:
        self._timeout = None
        self.callback()

    def clear(self) -> None:
        if self._timeout is not None:
            self._timeout.cancel()
            self._timeout = None
```

A closure returning `(trigger, clear)` is the right alternative when no one needs to inspect, type, serialize, or mock the state — the surface is just the two callables. Module-level globals deserve more pushback than either; prefer dependency injection.
