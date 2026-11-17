# Dates and Times — Aware, UTC, and the DST Arithmetic Trap

One rule prevents most of the damage: every `datetime` that leaves a function is timezone-aware. Naive datetimes are only safe as a local, in-memory intermediate.

## Aware vs Naive

- `datetime.now()` is naive local time; `datetime.now(timezone.utc)` is aware. `datetime.utcnow()` returns a naive datetime holding UTC — the worst of both, deprecated in `python >=3.12`, and the single most common source of an eight-hour offset in production.
- Mixing them raises: `TypeError: can't compare offset-naive and offset-aware datetimes`. That error is your data model leaking; fix the boundary that produced the naive value, not the comparison.
- Named zones come from `zoneinfo` (`python >=3.9`): `ZoneInfo("Europe/Madrid")`. On Windows there is no system tz database — install the `tzdata` package or `ZoneInfoNotFoundError` appears only on that platform.
- Never use a fixed offset (`timezone(timedelta(hours=1))`) to mean a place. `+01:00` is Madrid in winter and wrong all summer.

## Store, Convert, Display

- Store instants in UTC (`timestamptz`, or an ISO-8601 string with an offset). Convert to a zone only for display.
- The exception that matters: a FUTURE local commitment ("the standup at 09:00 in Berlin next March") must be stored as local wall time + the zone NAME, not as UTC. Governments change offsets; a UTC instant frozen today drifts to the wrong local hour when the rules change.
- Dates without times (`date`) are not midnight-in-some-zone. A birthday is a `date`; a deadline is a `datetime`. Promoting a `date` to a `datetime` requires choosing a zone — make that choice visible.
- `datetime` is a subclass of `date`, so `isinstance(dt, date)` is True for both. When the distinction matters, test `type(x) is date` or check for a `.hour` attribute (`classes.md`).

## Arithmetic

- `dt + timedelta(days=1)` on an aware datetime is WALL-CLOCK arithmetic: the same local time the next day, which across a DST boundary is 23 or 25 real hours. For exact elapsed time, convert to UTC, add, convert back:

```python
later = (dt.astimezone(timezone.utc) + timedelta(hours=24)).astimezone(dt.tzinfo)
```

- Ambiguous local times (the hour that repeats when clocks go back) are disambiguated by `fold=0` (first occurrence) / `fold=1` (second). Nonexistent local times (the hour skipped in spring) have no correct answer — `zoneinfo` will hand you one silently, so validate user-entered times against the zone.
- "One month later" has no timedelta: `timedelta` has days, seconds, and microseconds only. Jan 31 + 1 month is a product decision — use `dateutil.relativedelta` and pick its behavior deliberately, or do the calendar math yourself with `calendar.monthrange`.
- Durations: `td.total_seconds()` is the only correct way to get a scalar (`td.seconds` is the sub-day remainder and drops whole days — a 25-hour timedelta reports 3600).
- POSIX time has no leap seconds, so a naive difference across one is off by a second; nothing in the stdlib fixes this and almost no application needs it to.

## Parsing and Formatting

- ISO-8601 in: `datetime.fromisoformat(s)`. In `python >=3.11` it accepts a trailing `Z` and most real-world ISO forms; before 3.11 it rejects `Z` and anything it did not itself produce.
- Anything else in: `datetime.strptime(s, fmt)` — and it is locale-dependent for `%b`, `%B`, `%a`, `%p`. A German-locale server cannot parse `"Jan"`. Pin the locale or parse numerically.
- Out: `dt.isoformat()` for machines, `strftime` for humans. `%-d`/`%-m` (no zero padding) is glibc-only — Windows spells it `%#d` and macOS is inconsistent. Compute the number and format it yourself if it must be portable.
- Unix timestamps: `dt.timestamp()` on a NAIVE datetime assumes local time, so the same code produces different epochs on your laptop and a UTC server. `datetime.fromtimestamp(ts)` is local; `datetime.fromtimestamp(ts, timezone.utc)` is explicit. Always pass the tz.
- Timestamps in milliseconds are the common wire format; dividing by 1000 into a float loses sub-millisecond precision above the year 2038-scale magnitudes — use integer division plus `timedelta(milliseconds=…)` when precision matters.

## Measuring Elapsed Time

- `time.monotonic()` for durations and timeouts — it cannot go backwards. `time.time()` can jump when NTP corrects the clock, which turns a duration negative and a rate-limiter into a bug.
- `time.perf_counter()` for benchmarks (highest resolution available, monotonic, `performance.md`).
- `time.time()` only when you need a real-world instant to store or display.
- Sleeping is not scheduling: `time.sleep(60)` in a loop drifts by however long the body takes. Schedule against a deadline: `next_run += 60; time.sleep(max(0, next_run - time.monotonic()))`.

## Boundaries With Other Systems

- Databases: a `timestamp without time zone` column returns naive datetimes no matter what you inserted. `timestamptz` (Postgres) round-trips aware values correctly; SQLite has no date type at all and stores whatever string you give it.
- JSON has no date type: serialize with `dt.isoformat()` and parse with `fromisoformat` (`files.md`).
- HTTP headers use RFC 7231 dates in GMT (`email.utils.parsedate_to_datetime` parses them correctly; `strptime` with a hand-written format does not).
- CSV/Excel: Excel serial dates are days since 1899-12-30 with a deliberate leap-year bug for 1900 — convert with a library, never by hand.
- Servers run UTC; your laptop does not. Any test that depends on the local zone must set it explicitly (`freezegun`, or `TZ=UTC` in the test environment) or it fails only for the colleague in another country (`testing.md`).
