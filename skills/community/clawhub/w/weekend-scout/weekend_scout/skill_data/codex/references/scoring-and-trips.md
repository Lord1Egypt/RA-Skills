# Scoring And Trips

Use this reference for Step 3 and Step 4. It defines the ranking, selection,
and trip-building contract after Python has already deduplicated and grouped
the saved weekend cache.

## Score each event 1-10

- Category match (festival/fair = high, generic = low): `0-3`
- Scale (city-wide = high, small local = low): `0-2`
- Uniqueness (annual = high, recurring = low): `0-2`
- Confidence (confirmed = 1, likely = 0.5, unverified = 0): `0-1`
- Free entry: `0-1`
- Source quality (official = 1, aggregator = 0.5): `0-1`

## Build the ranked pools

Before Step 3, `digest_input` must already contain the output of:

```bash
python -m weekend_scout prepare-digest --date "<saturday>"
```

Use:

- `home_city_pool = digest_input.home_city_candidates`
- `trip_city_pool = digest_input.trip_city_groups`

`trip_city_pool` is already grouped to one city bundle per city with:

- `city`
- `country`
- `tier`
- `event_count`
- `confirmed_count`
- `events` (all canonical events for that city, sorted best-first)

Objective dedupe and city grouping are already done by Python. Do **not** rebuild
duplicate collapse heuristics in-prompt unless the helper output is clearly wrong.

From those helper-provided pools:

- select up to `max_city_options` home-city events
- select up to `max_trip_options` trip-city bundles, preferring `tier1`, then `tier2`, then `tier3`
- do **not** under-fill the digest when eligible helper-provided candidates exist
- only discard a helper-provided trip city when there is explicit evidence that it is indoor, off-scope, off-date, or too weak to justify a trip option
- preserve each selected event's `source_url` when building the `city-events` payload for `format-message`
- keep that `source_url` when later verification did not improve the link

`score_summary.total_pool` must use `digest_input.summary.total_pool`, not an ad hoc
prompt-rebuilt count.

After selecting, compute:

```text
total_events = len(city_events_selected) + len(trip_options)
```

```bash
python -m weekend_scout score-summary --run-id "<run_id>" \
  --target-weekend "<saturday>" \
  --total-pool <N> \
  --city-events-selected <N> \
  --trip-options <N>
```

## Build trip options

Build trip options procedurally:

1. Use the pre-grouped `trip_city_pool` bundles directly.
2. Exclude `home_city` from trip building.
3. Keep only cities that have at least one confirmed or otherwise strong outdoor weekend event.
4. Build at most one trip option per city.
5. Rank candidate cities by tier order first, then event quality.
6. Build up to `max_trip_options`. If fewer credible trip cities exist, return the best smaller set without padding.
7. If one event clearly dominates for a city, use one event in the trip summary.
8. If multiple events materially improve the same city trip, combine at most `2-3` concise items from that city's `events` bundle.
9. Do **not** invent trip bundles from unrelated weak findings.
10. If the credible trip-city pool is smaller than `max_trip_options`, say so explicitly and build the best available smaller set without padding.

For road trips, use tier as a distance proxy:

- tier1 = largest / closest
- tier3 = smallest / farthest

Label trips `01` through `NN` in the final message only.

Trip payload contract:

```json
{
  "name": "Lodz Day Trip",
  "route": "Warsaw -> Lodz (130 km, ~1h45) -> Warsaw",
  "events": "Spring Fair | Main Square | Sat-Sun all day",
  "timing": "Leave by: 10:00 | Back by: ~20:00",
  "url": "https://example.com/event"
}
```

Use `home_city` as the route start/end label.
When a selected trip clearly centers on one kept event, copy that event's `source_url` into trip `url` when available.

"Leave by" timing means the latest departure that still arrives when the event is in full swing:

- formula: `event_start + 1h30 - drive_time`
- minimum departure: `09:00`
- if the event has no known start time, use `09:30`
