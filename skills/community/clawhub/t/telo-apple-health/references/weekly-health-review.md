
# Weekly health review

Use the connected telo account and answer in the user's language. This workflow reads records; it does not schedule future reports or change connections.

## Establish availability and dates

Call `data_status` before interpreting the records. Its `last_ingest` is a received upload batch, including empty uploads and re-sent records, not proof that sync finished. Collection ranges and per-metric dates describe stored records. `history_import.status` is the iPhone's own report of its import: trust `complete` or `details` as finished essentials, say older periods may still be arriving on `recent`, `history` or `failed`, and claim nothing when it is `unknown` or its `meaning` says the report is old. When `next_step` is present, relay its message to the user. `healthkit_read_permissions` is unknown: never claim permission was denied. An old workout alone does not prove stalled sync.

If there are no records, explain that no data has reached telo and direct the user to check sync in the telo iPhone app; do not invent a review. If a tool is unavailable in the installed version, state the limitation and use only available tools. Do not silently claim freshness was verified.

Use the user's local calendar date from conversation context, or ask when it is unavailable. Do not infer today's timezone from a historical workout offset. Unless the user specifies another period, use:

- Recent interval: today minus 7 days through yesterday, inclusive.
- Comparison interval: today minus 14 days through today minus 8 days, inclusive.

For 2026-10-24 these are 2026-10-17–2026-10-23 and 2026-10-10–2026-10-16. Both have seven days and no overlap. Honor explicit calendar-week requests; label a requested current, incomplete week as partial. Never silently move the window backward to hide missing recent data.

## Retrieve and compare

1. Discover exact names and units with `list_metrics` (or reuse the metric inventory just returned by `data_status`). Select available sleep-related daily metrics, resting heart rate, HRV, activity and body measurements relevant to the request; do not assume names from another provider.
2. Call `query_daily` with `granularity: "day"` over the two intervals. This avoids calendar-week buckets splitting the requested rolling weeks. Separate the returned dates into the two windows. Use `sessions(kind: "sleep")` for nights and `sessions(kind: "workout")` for workout counts, duration and distance. Query only the categories needed.
3. Track missing dates per metric. A missing row or null is unavailable, not zero. A recorded zero is valid. Days with body measurements need not occur every day; report the observation count. Multiple sleep sessions on one date are not multiple nights: distinguish naps if the records support it, otherwise describe sessions. Do not add overlapping session durations or time in bed to sleep stages. Sleep duration excludes awake stages; preserve local timestamp offsets.
4. For `aggregation: "sum"`, report the recorded total and its covered days. For `avg`, average the observed daily values. Keep different units or aggregation methods separate. Report workout totals as recorded workouts; absent workouts cannot by themselves establish rest days. Do not treat incomplete totals as evidence that activity fell. Do not extrapolate missing days.
5. If available and relevant, call `derived_metrics` for the recent window to contextualize HRV/resting-HR against preceding personal baselines. Respect `insufficient_data` and the reported baseline sample count. Training load is duration in minutes, not intensity-weighted TSS or a readiness score; its zero-workout days may include missing uploads.

If a response is truncated, discard it as an incomplete result and retrieve smaller non-overlapping date ranges or metric batches. For daily queries, splitting dates does not split daily buckets. Deduplicate overlapping retries by date/metric/unit/aggregation and sessions by UUID. If even a single day for a single metric or session kind is truncated, disclose the unresolved limit; do not fabricate a complete total or retry indefinitely. Use `workout_detail` only for a requested drilldown and follow its independent series and event cursors.

## Present the review

Name both date ranges. Show a compact comparison of values, units, observed days or sessions, and absolute changes; show percentage changes only with a nonzero, comparable prior value. State which comparisons have insufficient or unequal coverage. Even 7/7 recorded days does not prove full sensor wear.

Explain the few changes supported by the records, distinguishing factual differences from hypotheses. Avoid diagnosis, causal claims and prescriptive training decisions based only on these signals. If data is old or absent, report its dates and what cannot be concluded. Do not turn a missing-data review into a confident health assessment.
