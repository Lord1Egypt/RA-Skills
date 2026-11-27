# Sensor time series

Time series are the third data type alongside object properties and links: **many
measurement points over time** on one object. Typical cases: vehicle telemetry (position,
speed), water levels, temperature curves, fleet movement.

## The model in three sentences

- An **object** has one or more **series**. A series is a stream of points
  `(ts, value_float, value_str, lat, lng)`.
- A series has **no udid of its own**. Its identity is the pair `(object_udid, series_key)`.
- The `series_key` is **the same string** as the key of the associated property. The property
  is the **pointer** to the series (def field `computed = {"series": true}`) and carries no
  value of its own — the last value sits alongside it as `series_ts`/`series_lat`/`series_lng`.

## The two tools

| Tool | What for |
|---|---|
| `onto_series_range` | **History**: the points between two instants (curve, day's route) |
| `onto_series_last` | **Now**: the current values of several objects/series in ONE call |

Which series an object has is listed in `onto_object_show` in the field `series_keys`.

### `onto_series_range`

Required: `object_udid` + `series_key`.

**`resolution` is the trick.** `0` = every raw point. `>0` = grid in seconds (minimum 60).

- Day's route → `300` (5 minutes): a manageable number of points, the shape stays recognisable.
- Measurement curve → `900` or `3600`.
- Without a grid **all** raw points come back. At a fine resolution that quickly becomes very
  many, and the response is capped at `MAX_RANGE_POINTS` — a `count` smaller than expected means:
  shrink the window or use a coarser grid.

Response: `{count, resolution, points[{ts, value_float, value_str, lat, lng}]}`. For a
`geo` sensor, `lat`/`lng` carry the position, `value_*` is then `null`.

### `onto_series_last`

`objects` and `series` are **lists** (max 1000 objects). That serves an entire fleet in one
call — instead of N individual queries.

## Time: everything UTC

`points[].ts` and `series_ts` are **UTC in ISO 8601 with `Z`** — `2026-10-06T23:09:00Z`. `from`/`to`
are read as **UTC** even without a zone (measured 2026-11-25: naive vs `Z` = identical window).
**Do not convert yourself:** whoever first turns UTC into local time
in order to compare two values builds in exactly the error the conversion was meant to
avoid. Compare UTC with UTC.

The **web view**, by contrast, shows viewer time. `01:09` in the interface and `23:09` in the
API are the same instant (Europe/Berlin = UTC+2 in summer) — a two-hour zone difference,
not an error.

## Real use cases (measured)

### 1. "Where are all vehicles now?" — fleet in ONE call

**Measured** in a scope with **10 objects** (types `car`, `form`, `invoice`, `file`,
`trigger`, `damageReport`), telemetry series `location` (geo) and `speed`:

```json
{"objects": ["<udid1>", "…", "<udid10>"], "series": ["location", "speed"]}
```

Result: `count: 2`, i.e. **two values** — one object with two series:

```
location  ts=2026-10-06T23:09:00Z  lat=52.502494  value_float=null
speed     ts=2026-10-06T23:09:00Z  lat=null      value_float=26.2
```

**Lesson — the silent trap:** 10 objects asked for, 2 values returned. That is **not an
error**: nine objects simply have no point in these series. Whoever expects "number of
responses = number of objects" takes a correct answer for a broken one and looks in the wrong
place. The response is a list of *existing measurements*, not a list of objects.

Just as important: **an empty list is a valid result.** A vehicle that has just sent nothing
does not appear — it has not disappeared.

### 2. Day's route of a vehicle

1. `onto_series_range`, `series_key: "location"`, `from`/`to` set to the day, `resolution: 300`
2. The points carry `lat`/`lng` → straight into a map polygon
3. Use a coarser grid for longer periods (`900`, `3600`), otherwise `MAX_RANGE_POINTS` kicks in

As a yardstick: the same series had **22 points at `resolution: 300`** in a window of 2.5
hours — the history stays readable, the response stays small.

**Lesson:** `resolution` is the answer to "the response is too big" — not shrinking the window
further and further.

### 3. Thinning a measurement curve instead of truncating it

A sensor delivers once a minute, a chart needs an overview:
`resolution: 900` → 15-minute mean. The curve shows the trend, not the noise.
The grid is computed **server-side** — the thinning costs no additional transfer.

## What goes wrong (and why it is silent)

- **An empty response is not an error.** See use case 1 — the most common wrong conclusion.
- **`series_key` swapped.** The property key is the right one; whoever looks for the udid of the
  series finds nothing — a series has none.
- **Foreign scope → 403.** Visibility follows the scope of the **property**, not of the object.
  The tool is visible, execution is still refused (fail-closed).
- **Raw points over a long period.** Without `resolution` everything comes back — until the cap
  kicks in and `count` turns out smaller than expected.
- **`ts` misunderstood as local time.** The value ends in `Z`; it is UTC. Do not convert,
  only display — or have it displayed.
