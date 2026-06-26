---
title: Use raise ... from to Preserve Exception Causality
impact: LOW-MEDIUM
impactDescription: explicit `__cause__` chain vs implicit `__context__`; often invisible to end callers
tags: error, exceptions, traceback, chaining
---

## Use `raise ... from` to Preserve Exception Causality

When you catch one exception and raise another, include `from original` to preserve the chain. Without it, the traceback prints "During handling of the above exception, another exception occurred" — which is usually right, but the explicit form is clearer and survives `__cause__` suppression in some runtimes.

**Incorrect (original exception lost or implicit):**

```python
def load_config(path: Path) -> Config:
    try:
        raw = path.read_text()
    except FileNotFoundError:
        raise ConfigError(f"config missing: {path}")  # loses the original FileNotFoundError context
```

The traceback will still show both — Python implicitly sets `__context__` — but the intent isn't explicit, and `__cause__` is `None`, which some tools use to distinguish "we meant this chain" vs. "an error happened while handling."

**Correct (explicit `raise ... from`):**

```python
def load_config(path: Path) -> Config:
    try:
        raw = path.read_text()
    except FileNotFoundError as e:
        raise ConfigError(f"config missing: {path}") from e
```

The traceback prints "The above exception was the direct cause of the following exception" — a deliberate chain. `__cause__` is set, so programmatic handlers and logging can walk the chain cleanly.

**Use `from None` to suppress the context:**

When the original exception is genuinely internal and the caller shouldn't see it:

```python
def parse_timestamp(s: str) -> datetime:
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        raise ValueError(f"invalid timestamp: {s!r}") from None
```

The user-facing error is clean (`ValueError: invalid timestamp: 'abc'`) without the implementation's internal `ValueError: Invalid isoformat string:`.

**Three patterns:**

- `raise NewError() from original` — explicit chain; `__cause__` set
- `raise NewError()` inside `except` — implicit chain; `__context__` set
- `raise NewError() from None` — suppress the original context entirely

Default to `from original` when translating between exception types. Reach for `from None` when the internal cause is noise to the caller.
