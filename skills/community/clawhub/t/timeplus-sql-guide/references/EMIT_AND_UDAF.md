# EMIT Clauses & UDAF Emit Control

Two underused Proton features that solve problems people commonly try to hand-roll:

1. **`EMIT AFTER SESSION CLOSE IDENTIFIED BY (ts_col, start_col, end_col)`** — a
   declarative event-terminated session window. Use it when an aggregation should
   start on one event and emit on another, rather than on a wall-clock window or
   inactivity gap.
2. **`has_customized_emit: true`** in a JS/Python UDAF — the UDAF itself decides how
   many rows to emit per flush by returning an integer from `process()`. Returning
   `0` means "engine skips emit entirely." This replaces fragile manual
   `this.emitted = false` flags.

This file covers the full EMIT vocabulary, the engine constraints around
`SESSION CLOSE` / `KEY EXPIRE`, and the UDAF emit-count contract. For the basic
`EMIT AFTER WATERMARK` / `ON UPDATE` window policies, see
`TRANSFORMATIONS.md → EMIT Policies`. For UDAF structure (`initialize` / `process` /
`finalize` / `serialize` / `merge`), see `UDFS.md → JavaScript UDAF`.

**When to reach for this file:**

- Writing a streaming MV that fires on a specific event, not on a time window.
- Writing a JS or Python UDAF that emits duplicate rows or stray `false` rows.
- About to add `WHERE event_time > now() - INTERVAL N MINUTE` just to bound state in
  a streaming `GROUP BY`.
- Hand-rolling `this.emitted = false` / `this.fired = true` inside a UDAF to prevent
  re-emit.
- Hitting install-time errors like
  `NOT_IMPLEMENTED: EMIT AFTER SESSION CLOSE`,
  `UNSUPPORTED: MAXSPAN only supports millisecond, second or minute interval`, or
  `TIMEOUT interval shall be great or equal to MAXSPAN interval`.

**Do NOT use** for: scalar UDFs (stateless per-row); ClickHouse-only deployments
(these features are Proton-specific); historical-only batch queries (use
`table(stream)` and a regular `GROUP BY`).

---

## Full EMIT clause vocabulary

```
EMIT [STREAM | CHANGELOG | DELTA]
EMIT STREAM AFTER WINDOW CLOSE [WITH DELAY <interval>] [AND TIMEOUT <interval>]
EMIT STREAM PERIODIC <interval> [REPEAT] [WITH DELAY <interval>] [AND TIMEOUT <interval>]
EMIT ON UPDATE [WITH BATCH <interval>] [WITH DELAY <interval>] [AND TIMEOUT <interval>]
EMIT PER EVENT [WITH DELAY <interval>] [AND TIMEOUT <interval>]
EMIT LAST <interval> [ON PROCTIME]
EMIT [STREAM] AFTER KEY EXPIRE   [IDENTIFIED BY <ts_col>]                            WITH [ONLY] MAXSPAN <interval> [AND TIMEOUT <interval>]
EMIT [STREAM] AFTER SESSION CLOSE [IDENTIFIED BY (<ts_col>, <start_col>, <end_col>)] WITH [ONLY] MAXSPAN <interval> [AND TIMEOUT <interval>]
```

**`AFTER KEY EXPIRE` and `AFTER SESSION CLOSE` are aliases.** They share the same
execution machinery. The conventional distinction is the `IDENTIFIED BY` tuple shape:

- 1-tuple `IDENTIFIED BY ts_col` — "KEY EXPIRE" idiom: inactivity-only, no
  start/end events.
- 3-tuple `IDENTIFIED BY (ts_col, start_col, end_col)` — "SESSION CLOSE" idiom:
  event-bounded.

Whichever keyword you write, the same engine constraints apply (see
[Engine constraints](#engine-constraints-for-session-close--key-expire)).

---

## Event-terminated session window

When the boundary of your aggregation is **an event** (not a clock interval or an
inactivity gap), use `EMIT AFTER SESSION CLOSE`:

```sql
-- Project the session-boundary predicates into boolean columns first.
-- IDENTIFIED BY only accepts column references and specific bool literals
-- (true for start_col, false for end_col) — inline predicates are rejected.
WITH typed_events AS (
    SELECT
        run_id,
        event_time,
        metric_name,
        metric_value,
        event_type = 'session_start' AS is_session_start,
        event_type = 'session_end'   AS is_session_end
    FROM event_stream
)
SELECT
    run_id,
    sum_if(metric_value, metric_name IN ('input_tokens', 'output_tokens')) AS tokens
FROM typed_events
GROUP BY run_id
EMIT AFTER SESSION CLOSE
  IDENTIFIED BY (event_time, is_session_start, is_session_end)
  WITH MAXSPAN 60m AND TIMEOUT 60m
HAVING tokens > 40000
SETTINGS default_hash_table = 'hybrid';
```

`IDENTIFIED BY` accepts a 1- or 3-tuple. The parser is **asymmetric** on the second
and third tuple positions:

- 1-tuple: `IDENTIFIED BY ts_col` — equivalent to the degenerate 3-tuple
  `(ts_col, true, false)`.
- 3-tuple: `(ts_col, start_col, end_col)`:
  - `ts_col` — column identifier (the event-time column).
  - `start_col` — a boolean column reference **OR** the `true` literal ("every row
    starts a session"). The `false` literal and inline predicates are rejected.
  - `end_col` — a boolean column reference **OR** the `false` literal ("no row ends;
    rely on KEY EXPIRE / TIMEOUT"). The `true` literal and inline predicates are
    rejected.

The four parser-accepted shapes:
`(ts, start_col, end_col)`, `(ts, start_col, false)`, `(ts, true, end_col)`,
`(ts, true, false)`.

To bound the aggregation on a value-derived predicate
(`event_type = 'session_end'`, `status IN (...)`, etc.), project the predicate into a
boolean column first via a CTE or subquery —
`IDENTIFIED BY (ts, event_type = 'start', event_type = 'end')` will **not** parse.

`MAXSPAN` caps the session duration so a malformed stream (start without end) cannot
grow state unbounded. `TIMEOUT` triggers emit if no terminator event arrives. The
engine **automatically releases the per-key state** when the session closes — no
manual cleanup.

---

## Engine constraints for SESSION CLOSE / KEY EXPIRE

These are enforced at install time. Violations produce install-time exceptions, not
silent misbehavior:

| Constraint | Failure mode |
|---|---|
| `MAXSPAN` accepts only `ms`, `s`, `m` units. `h`, `d`, `w` are rejected. | `UNSUPPORTED: MAXSPAN only supports millisecond, second or minute interval` |
| `MAXSPAN` interval must be greater than zero. | `INCORRECT_QUERY: MAXSPAN interval shall not be zero` |
| `TIMEOUT` interval must be greater than or equal to `MAXSPAN`. | `UNSUPPORTED: TIMEOUT interval shall be great or equal to MAXSPAN interval` |
| Requires the **hybrid** hash-table aggregator. The memory aggregator does not implement this emit mode. | `NOT_IMPLEMENTED: EMIT AFTER SESSION CLOSE is not supported by memory aggregator yet` |

Force hybrid with a query-level setting:

```sql
SELECT ...
FROM stream
GROUP BY ...
EMIT AFTER SESSION CLOSE
  IDENTIFIED BY (event_time, true, is_session_end)
  WITH MAXSPAN 15m AND TIMEOUT 15m
SETTINGS default_hash_table = 'hybrid';
```

### Practical implications

- **You cannot get "long state lifetime, short emit latency."** The `TIMEOUT ≥
  MAXSPAN` rule couples the two. The longest you can keep state without emitting is
  bounded by `MAXSPAN`, and you cannot fire faster on inactivity than `MAXSPAN`
  allows.
- **`MAXSPAN` truncates long sessions.** If your real session lasts longer than
  `MAXSPAN` and there is no `end_col=true` row to close it sooner, the engine emits
  at `MAXSPAN` and starts a new session for the same key. Aggregates over the full
  original session require either (a) an explicit `end_col` event or (b) downstream
  re-aggregation across the truncated emits.
- **`WITH ONLY MAXSPAN` gates emit on `MAXSPAN` only.** Emission requires the session
  to live until `MAXSPAN`. If an `end_col=true` row arrives earlier, the session
  state is still removed but **no row is emitted** — the session is silently dropped.
  Use only when discarding short sessions is acceptable.

### Worked example: the two constraints in practice

A common first attempt is "long state, fast inactivity emit": `MAXSPAN 120m AND
TIMEOUT 15m`. Both constraints fire:

1. The engine rejects `120m` MAXSPAN paired with `15m` TIMEOUT because
   `TIMEOUT < MAXSPAN`.
2. Switching MAXSPAN to hours (`2h`) would be rejected too — the unit constraint only
   permits `ms`/`s`/`m`.

The working shape is `MAXSPAN 15m AND TIMEOUT 15m` with a documented truncation
caveat: a session longer than 15 minutes with no `session_end` terminator is split
into multiple emits. Mitigation: have producers emit an explicit `session_end` event
at run boundaries, or post-aggregate downstream.

---

## UDAF emit control: `has_customized_emit`

### How the engine wires it

1. At UDAF registration, the engine reads the `has_customized_emit` property from
   your UDAF object.
2. If true, after each call to `process(...)`, the engine reads the function's
   **return value as `emit_times`** (a number).
3. If `emit_times == 0`, the engine **skips the `finalize()` flush entirely** — no
   row reaches the downstream stream.
4. If `emit_times == N`, `finalize()` is expected to return `N` results (typically as
   an array).

This means you never need a manual `emitted` flag. The engine owns the emit-count
contract.

### Correct pattern (engine-managed emit, JavaScript)

```js
{
  has_customized_emit: true,

  initialize: function() {
    this.pending = [];   // results waiting to be flushed
    // any FSM state lives here too
  },

  process: function(rowtime, col_a, col_b /*, ... */) {
    for (let i = 0; i < rowtime.length; i++) {
      // Run the FSM / pattern check; push to this.pending only when a match finalizes
      if (/* pattern matched */) {
        this.pending.push({ when: rowtime[i], evidence: col_a[i] });
      }
    }
    return this.pending.length;   // 0 => engine skips finalize; otherwise emit N rows
  },

  finalize: function() {
    const out = this.pending;
    this.pending = [];            // clear, ready for next batch
    return out;                   // array of length === last process() return
  },

  serialize:   function() { return JSON.stringify({ pending: this.pending /*, fsm state */ }); },
  deserialize: function(s)  { Object.assign(this, JSON.parse(s)); },
  merge:       function(s)  { /* combine FSM state + concat pending arrays */ }
}
```

### Python UDAF equivalent

Python UDAFs use the same `has_customized_emit` contract — set it as a class or
instance attribute. The Python UDAF DDL form is:

```sql
CREATE OR REPLACE AGGREGATE FUNCTION <name>(<args>)
RETURNS <type>
LANGUAGE PYTHON AS $$
class <name>:
    ...
$$;
```

```python
class detect_pattern:
    has_customized_emit = True            # class attribute — read once at registration

    def __init__(self):
        self.pending = []                  # results buffer
        # FSM state fields here

    def process(self, rowtime, col_a, col_b):
        for i in range(len(rowtime)):
            if self._pattern_matches(col_a[i], col_b[i]):
                self.pending.append({"when": rowtime[i], "evidence": col_a[i]})
        return len(self.pending)           # 0 -> engine skips finalize

    def finalize(self):
        out, self.pending = self.pending, []
        return out                         # list of length == process() return

    def serialize(self):   return json.dumps({"pending": self.pending})
    def deserialize(self, s): self.pending = json.loads(s)["pending"]
    def merge(self, other): self.pending.extend(other.pending)   # `other` is the other instance, NOT a string
```

**Important: Python's `merge()` signature differs from JavaScript's.** The Python
adapter passes the *other Python instance directly* and calls `merge(self, other)` —
it does NOT serialize first. The JS adapter serializes the other state via
`serialize()` and passes the resulting string to `merge(serialized_state)`. The two
adapters have opposite contracts; do not copy a JS `merge(s) { JSON.parse(s) ... }`
pattern into Python.

### Anti-pattern (manual emit-once flag — fragile)

```js
{
  // NO has_customized_emit declared → every finalize() call emits SOMETHING

  initialize: function() { this.matched = false; this.emitted = false; },

  process: function(...) { /* sets this.matched */ },

  finalize: function() {
    // Engine calls this on every checkpoint/batch and always emits the return value
    if (this.matched && !this.emitted) {
      this.emitted = true;
      return true;            // intended fire
    }
    return false;             // BUG: this still emits a "false" row downstream
  }
}
```

This pattern breaks in three ways:

- `finalize()` runs every flush, so `false` returns become noise rows downstream.
- The `emitted` flag must be hand-correctly handled in `serialize`/`deserialize`/
  `merge` — easy to get wrong across shard rebalance or MV restart.
- Multiple parallel partial aggregators each have their own `emitted = false`;
  `merge()` rarely OR's it correctly, leading to duplicate fires.

---

## `merge()` correctness for distributed UDAFs

Multi-shard or rebalanced execution combines partial aggregator states via `merge()`.
The function **must be associative and commutative** because Proton may merge partials
in any order. For each kind of state field:

| State kind | Correct merge | Why |
|---|---|---|
| Counter (`tokens_seen`, `call_count`) | `this.x += other.x` | additive — assoc + commut |
| Set membership flag (`saw_session_start`) | `this.x = this.x \|\| other.x` | OR is assoc + commut |
| Result buffer (`pending` array) | `this.pending = this.pending.concat(other.pending)` | concat — order-independent IF downstream doesn't rely on order; if it does, `finalize()` must sort |
| Latest-seen value (`last_event_time`) | `this.x = Math.max(this.x, other.x)` | max is assoc + commut |
| First-seen value (`first_match_ts`) | `this.x = (this.x === 0) ? other.x : Math.min(this.x, other.x)` | min with sentinel |
| Non-monotonic FSM state ("currently in state B") | **No general recipe** — redesign as monotonic state | non-commutative merges silently corrupt across shards |

**Rule of thumb:** if you can't reduce a state field to an associative + commutative
monoid (sum, max, OR, set-union, concat), it does not belong in a UDAF. Eliminating a
manual `emitted` flag via `has_customized_emit` also eliminates the merge-correctness
obligation for that field.

---

## `EMIT AFTER KEY EXPIRE` — the inactivity idiom of SESSION CLOSE

`AFTER KEY EXPIRE` is an alias for `AFTER SESSION CLOSE` (same execution path). The
keyword exists to signal **intent**: aggregate per key, fire when the key goes
inactive, with no explicit terminator event.

Convention:

- Use `AFTER KEY EXPIRE` with the **1-tuple** `IDENTIFIED BY ts_col`.
- Use `AFTER SESSION CLOSE` with the **3-tuple**
  `IDENTIFIED BY (ts_col, start_col, end_col)`.

The engine accepts either keyword with either tuple shape; the convention is for human
readers, not the parser.

```sql
-- Failed-login counter: fire when a user_id goes quiet
-- (there is no "session_end" event for failed logins).
-- Note: TIMEOUT >= MAXSPAN is enforced, so the "inactivity threshold"
-- is at minimum MAXSPAN. To fire after 10 min of inactivity, use 10m / 10m.
SELECT user_id, count(*) AS fails
FROM auth_events
WHERE outcome = 'failure'
GROUP BY user_id
EMIT AFTER KEY EXPIRE IDENTIFIED BY event_time
  WITH MAXSPAN 10m AND TIMEOUT 10m
HAVING fails > 5
SETTINGS default_hash_table = 'hybrid';
```

Both `MAXSPAN` and `TIMEOUT` participate in close detection:

- `MAXSPAN` is the upper bound on session duration regardless of activity.
- `TIMEOUT` is the inactivity threshold. Because `TIMEOUT ≥ MAXSPAN`, the effective
  inactivity threshold is also bounded below by `MAXSPAN`.
- The engine releases state when the session closes.

### When to use which keyword

| Use case | Keyword + IDENTIFIED BY shape |
|---|---|
| Aggregation has an **explicit terminator event** (`session_end`, `task_complete`, `is_session_end` column) | `AFTER SESSION CLOSE IDENTIFIED BY (ts, start_col, end_col)` |
| Aggregation should fire on **inactivity** per key, no terminator event | `AFTER KEY EXPIRE IDENTIFIED BY ts` |
| Periodic checkpointed aggregation over a fixed window | `AFTER WINDOW CLOSE` (with `tumble()` / `hop()`) |
| Continuous updates on every batch | `ON UPDATE [WITH BATCH ...]` |
| Emit one row per input event | `PER EVENT` |
| Emit at a fixed cadence | `PERIODIC <interval> [REPEAT]` |

---

## Other EMIT modes (reference)

One paragraph of semantics + one minimal example + the use case for each mode.

### EMIT STREAM (default for unwindowed `GROUP BY`)

The default emit mode. The aggregator updates state on every input row and emits the
current aggregate state row whenever a new row would change a visible aggregate. For
`GROUP BY` aggregations, this means a row per (group, change). Most queries that do not
declare an EMIT clause are implicitly `EMIT STREAM`.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id;
-- equivalent: ... EMIT STREAM
```

Use when downstream consumers want to see the latest aggregate as soon as it changes.

### EMIT CHANGELOG

Emits insert/retract pairs so downstream subscribers can maintain an exact
materialized view. When an aggregate changes from `x` to `y`, the engine emits a
retraction of `x` and an insert of `y`. Required for cascading materialized views that
pre-aggregate further: without retractions, the downstream view would double-count old
values.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT CHANGELOG;
```

Use when feeding the result into another streaming MV that aggregates again. Without
it, the downstream MV cannot tell "update" from "new row" and will over-count.

### EMIT DELTA

Emits only the *change* in aggregate state, not the full aggregate. Useful for
counters and gauges where downstream wants `+N since last emit` instead of `total so
far`. The canonical form pairs with `PERIODIC`:

```sql
SELECT id, sum(i) AS s FROM stream GROUP BY id EMIT DELTA PERIODIC 1s;
```

Use when downstream needs incremental rates rather than running totals — for example,
feeding a Prometheus-style counter.

### EMIT [STREAM] AFTER WINDOW CLOSE (alias: `AFTER WATERMARK`)

For aggregations over a *window function* (`tumble`, `hop`, `session`). Fires when the
window's watermark crosses the window-end. The aggregate for that window is final at
that point; no more rows in that window will arrive (within `WITH DELAY`).

```sql
SELECT window_start, count(*)
FROM tumble(events, event_time, 5m)
GROUP BY window_start
EMIT STREAM AFTER WINDOW CLOSE WITH DELAY 30s AND TIMEOUT 5s;
```

`WITH DELAY` is the late-arrival grace. `AND TIMEOUT` bounds how long the engine waits
for late events past the delay. Use whenever you have a windowed `FROM` and want one
row per window.

### EMIT PERIODIC `<interval>` [REPEAT]

Emit the current aggregate state at a fixed cadence. With `REPEAT`, the same aggregate
may be re-emitted across periods even when nothing changed; without `REPEAT`, the
engine emits only when state changed since the last emission.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT PERIODIC 1s;
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT STREAM PERIODIC 1s REPEAT WITH DELAY 1s AND TIMEOUT 5s;
```

Use when downstream wants a regular tick — dashboards, heartbeat tables, periodic
snapshots. The `PERIODIC <interval> ON UPDATE` form is equivalent to
`ON UPDATE WITH BATCH <interval>` (kept for backward compatibility).

### EMIT ON UPDATE [WITH BATCH `<interval>`]

Emit on every aggregate state change, with optional `WITH BATCH` debounce. `WITH BATCH
1s` means "coalesce all updates within 1s of the first change into a single emit."
Combine with `WITH TIMEOUT <interval>` to bound the delay even when no batch fills.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT ON UPDATE WITH BATCH 1s;
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT ON UPDATE WITH BATCH 1s WITH DELAY 1s AND TIMEOUT 5s;
```

If downstream cares about state freshness but not every individual mutation, `WITH
BATCH` is the right knob. The hybrid aggregator also honours the
`aggregate_state_ttl_sec` setting (see below) for `ON UPDATE WITH TIMEOUT`.

### EMIT PER EVENT

Emit one output row per *input* row, with the aggregate state observed *after*
incorporating that row. Different from `EMIT STREAM` in that `PER EVENT` always emits
even when the aggregate did not change, and even for keys with single-row groups.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT PER EVENT;
```

Use when downstream needs an "after each input event" projection of the state — for
example, an audit trail that records the running total after every event.

### EMIT LAST `<interval>` [ON PROCTIME]

Historical look-back: emit aggregates for the last `<interval>` of data from the
stream's current position. STREAM mode only (the parser throws `NOT_IMPLEMENTED` if
combined with `CHANGELOG`/`DELTA`). `ON PROCTIME` resolves the look-back against
wall-clock instead of event-time. This form is being deprecated in favour of explicit
table-window functions.

```sql
SELECT user_id, count(*) FROM events GROUP BY user_id EMIT LAST 1h ON PROCTIME;
```

Avoid in new queries; prefer `FROM tumble(stream, ts, 1h)` plus
`EMIT STREAM AFTER WINDOW CLOSE`.

### EMIT [STREAM] TIMEOUT `<interval>` (backward compatibility)

Standalone `TIMEOUT` without a preceding mode. The parser treats it as an implicit
`AFTER WINDOW CLOSE` (for windowed `FROM`) or implicit `PERIODIC` (for global
aggregation). Retained for older queries.

```sql
SELECT count(*) FROM stream EMIT STREAM TIMEOUT 30s;
```

Do not write new code in this shape; prefer the explicit `AFTER WINDOW CLOSE` or
`PERIODIC` form.

### Interaction with `aggregate_state_ttl_sec`

For hybrid hash aggregation, `SETTINGS aggregate_state_ttl_sec = N` puts an absolute
TTL on per-key aggregate state. This is the right knob when using `EMIT ON UPDATE WITH
TIMEOUT <interval>` — if the TTL is shorter than the TIMEOUT, the state is evicted
before the timeout fires and downstream sees no emit. Set `aggregate_state_ttl_sec >=`
the TIMEOUT to avoid silent eviction.

---

## Composition rules: EMIT clauses vs table-window functions

Two distinct ways to declare a window in Proton:

1. **Table-window functions** in `FROM`: `tumble(stream, ts, 5m)`,
   `hop(stream, ts, 1m, 5m)`, `session(stream, ts, gap)`. These produce
   `window_start` / `window_end` columns and **pair with `EMIT AFTER WINDOW CLOSE`**
   (often implicit).
2. **EMIT-clause windows** on an unwindowed `GROUP BY`: `EMIT AFTER SESSION CLOSE` or
   `EMIT AFTER KEY EXPIRE`. These do **not** use a windowing table function — they
   bound state via event predicates or inactivity instead.

**These two modes are mutually exclusive in a single SELECT:**

| FROM shape | EMIT clauses that fit | EMIT clauses that DO NOT fit |
|---|---|---|
| `FROM stream` (no window function) | `AFTER SESSION CLOSE`, `AFTER KEY EXPIRE`, `ON UPDATE`, `PER EVENT` | `AFTER WINDOW CLOSE` (no window to close) |
| `FROM tumble(stream, ...)` / `FROM hop(stream, ...)` | `AFTER WINDOW CLOSE` (often implicit), `PERIODIC` | `AFTER SESSION CLOSE`, `AFTER KEY EXPIRE` (redundant with the table-function window) |
| `FROM session(stream, ts, gap)` | `AFTER WINDOW CLOSE` | `AFTER SESSION CLOSE` (the gap-based `session()` already provides the close trigger) |

`HAVING` composes with any EMIT mode — it filters the emitted aggregate row regardless
of how it was triggered.

If you need event-bounded behavior, choose the unwindowed `FROM stream` +
`EMIT AFTER SESSION CLOSE` path. Do not mix the two — the parser may accept it, but the
semantics double-up and one of the windows will dominate.

---

## Anti-pattern: `WHERE event_time > now() - INTERVAL N MINUTE`

Often added not because the logic wants an N-minute window, but because **streaming
`GROUP BY` without a window clause keeps state forever** and the author wanted to bound
it. Symptoms:

- A run that spans longer than the interval gets split across two windows → false
  negative.
- Multiple unrelated runs that finish inside the same time slice get merged → false
  positive.
- Threshold semantics implicitly depend on wall-clock, not on the event boundary the
  logic actually cares about.

If the real boundary is an event (`session_end`, `run_complete`, etc.), use
`EMIT AFTER SESSION CLOSE IDENTIFIED BY (...)`. The engine then bounds state on the
actual event boundary instead of the clock.

---

## Quick reference

| Problem | Wrong approach | Right approach |
|---|---|---|
| Emit exactly once when a UDAF pattern matches | `this.emitted` flag, return `false` to suppress | `has_customized_emit: true`, return `0` from `process()` |
| Aggregate from `session_start` event to `session_end` event | `WHERE event_time > now() - INTERVAL N MINUTE` | `EMIT AFTER SESSION CLOSE IDENTIFIED BY (ts, start_col, end_col)` |
| Release state after a key is "done" | manual TTL in UDAF | `EMIT AFTER KEY EXPIRE IDENTIFIED BY ts_col` |
| Avoid downstream `false` rows from suppressed UDAF emits | filter with `HAVING result IS NOT NULL` (still emits and filters) | `has_customized_emit` so the engine never emits in the first place |
| One-shot emit at session close in pure SQL | hand-rolled `lag()` / `lead()` + dedup | `EMIT AFTER SESSION CLOSE` |
| Long state lifetime + short emit latency on the same key | `MAXSPAN 120m AND TIMEOUT 15m` (engine rejects) | Not possible — `TIMEOUT ≥ MAXSPAN` is enforced. Choose `MAXSPAN = TIMEOUT`, or post-aggregate downstream. |
| Hours-scale session window | `MAXSPAN 1h` (engine rejects) | Use compact `m`/`s`/`ms` units: `MAXSPAN 60m` |
| `EMIT AFTER SESSION CLOSE` install fails with `NOT_IMPLEMENTED` | Default cluster aggregator was memory | Add `SETTINGS default_hash_table = 'hybrid'` to the query |
| Downstream MV re-aggregates and double-counts | Default `EMIT STREAM` from upstream | Upstream emits `EMIT CHANGELOG` so downstream sees retractions |
| Downstream needs incremental rates, not running totals | Custom diff in SQL | `EMIT DELTA PERIODIC <interval>` |
| Hybrid aggregator silently evicts state before `EMIT ON UPDATE WITH TIMEOUT` fires | Default `aggregate_state_ttl_sec = 0` paired with long TIMEOUT | Set `SETTINGS aggregate_state_ttl_sec >= TIMEOUT` |

---

## Common mistakes

- Returning `false` (or `null`) from a UDAF `finalize()` to "suppress emit" — **does
  not suppress**, it just emits that value downstream. Use `has_customized_emit` +
  return `0` from `process()` instead.
- Assuming Proton's `session(stream, event_time, gap)` accepts an event predicate —
  **it does not**. `session()` is gap-based (inactivity). For event-bounded sessions
  use `EMIT AFTER SESSION CLOSE IDENTIFIED BY (...)`.
- Forgetting to set `MAXSPAN` on `EMIT AFTER SESSION CLOSE` — a malformed stream with
  no terminator event leaks state until `TIMEOUT` fires.
- Trying to mutate `has_customized_emit` after `initialize()` — it's read once at UDAF
  registration. Set it at the top level of the UDAF object literal (JS) or as a class
  attribute (Python).
- Putting per-shard state in `process()` without correct `merge()` semantics. Even
  with `has_customized_emit`, a non-associative or non-commutative `merge()` corrupts
  state on shard rebalance.
- Writing `MAXSPAN 1 HOUR` (or `1h`, `1d`, `1w`) on `AFTER SESSION CLOSE` /
  `AFTER KEY EXPIRE` — engine rejects at install time with `UNSUPPORTED: MAXSPAN only
  supports millisecond, second or minute interval`. Use `60m` etc.
- Writing `MAXSPAN 120m AND TIMEOUT 15m` to get "long state, fast inactivity emit" —
  engine rejects with `UNSUPPORTED: TIMEOUT interval shall be great or equal to MAXSPAN
  interval`. The two are coupled; you cannot decouple them.
- Installing an `AFTER SESSION CLOSE` rule without
  `SETTINGS default_hash_table = 'hybrid'` — the memory aggregator throws
  `NOT_IMPLEMENTED`. Pin the setting at the query level even if the cluster default is
  hybrid.
- Treating `AFTER KEY EXPIRE` and `AFTER SESSION CLOSE` as semantically distinct
  features — they are aliases for the same execution path. The same engine constraints
  apply.
- Using `MAXSPAN` to bound a long-lived session expecting "aggregate over the whole
  session, emit on terminator." `MAXSPAN` truncates: a 30-minute session with
  `MAXSPAN 15m` produces two emits, each over half the session. Either emit a real
  terminator event or post-aggregate downstream.
- Writing an inline predicate as `start_col` or `end_col`:
  `IDENTIFIED BY (ts, event_type = 'start', event_type = 'end')` — parser rejects with
  `expected be a column identifier or true/false literal`. Project the predicate into a
  boolean column via a CTE/subquery and reference the alias.
- Swapping the start/end literal positions: writing `false` for `start_col` or `true`
  for `end_col`. The parser is asymmetric — `start_col` accepts only `true`, `end_col`
  accepts only `false`. The valid literal-bearing shapes are `(ts, true, end_col)`,
  `(ts, start_col, false)`, and `(ts, true, false)`.
- Writing a Python UDAF `merge(self, s)` that calls `json.loads(s)` — the Python
  adapter passes the *other Python instance directly*, not a serialized string. The
  signature must be `merge(self, other)`, accessing `other.<field>` directly.
  JavaScript is the opposite: JS `merge(s)` does receive a string.
- Using `WITH ONLY MAXSPAN` with an `end_col` that fires often — sessions terminated by
  `end_col=true` before `MAXSPAN` are silently dropped with no emit. The mode is safe
  only when discarding short sessions is intentional.
