---
title: Use Timezone-Aware Datetimes at Boundaries
impact: HIGH
impactDescription: prevents off-by-hours bugs across timezones, daylight saving, and storage
tags: data, datetime, timezone, boundaries
references: https://docs.python.org/3/library/datetime.html#aware-and-naive-objects, https://docs.python.org/3/library/zoneinfo.html, https://peps.python.org/pep-0615/
---

## Use Timezone-Aware Datetimes at Boundaries

A `datetime` with no `tzinfo` is **naive**: two naive datetimes that look identical may refer to different absolute moments. Naive values leak into databases, JSON, logs, and inter-service messages, then surface as off-by-hours bugs during DST or when hosts differ. At any boundary the value crosses (HTTP, DB, queue, file, log, comparison), it must be timezone-aware. Store and transport in UTC; convert to local zones at display.

**Incorrect (`datetime.utcnow()` returns naive; deprecated in 3.12+):**

```python
from datetime import datetime

def stamp() -> datetime:
    return datetime.utcnow()              # naive — a serializer reading it as local time writes the wrong value
```

**Correct (UTC-aware at the boundary; local zone only for display):**

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

def stamp() -> datetime:
    return datetime.now(timezone.utc)     # aware; round-trips through isoformat() cleanly

stored = datetime.now(timezone.utc)
display = stored.astimezone(ZoneInfo("America/Los_Angeles"))  # named zone, DST handled
```

`zoneinfo` (3.9+, PEP 615) reads from system tzdata and handles DST and historical offsets. Use named zones (`"America/Los_Angeles"`), not raw offsets (`-08:00`).

**Parsing input:** if callers can send naive datetimes, decide once whether to reject or assume a fixed zone. Never *silently* treat naive as UTC. For Pydantic v2, `AwareDatetime` rejects naive values at the model boundary. For PostgreSQL, use `TIMESTAMPTZ`; for SQLite/MySQL, store ISO-8601 strings with `+00:00` or epoch milliseconds.

Naive is acceptable only inside a tight block where every value is naive and the timezone is documented in scope, or for pure date arithmetic (use `date`, not `datetime`). If the value outlives the function it's created in, it should be aware.
