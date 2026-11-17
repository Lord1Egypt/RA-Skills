
# Long-term trends

Use the connected telo account and answer in the user's language. Respect the user's chosen metrics and time range; for an open-ended request, start with the last 12 complete calendar months ending before the current local month and state that choice.

## Inspect and retrieve

Call `data_status` to inspect recorded date ranges and the latest received upload. Reuse its metric inventory or call `list_metrics` to discover exact metric names and units. Import progress and HealthKit read permissions are unknown, and a recent upload does not prove fresh or complete data. If `data_status` is unavailable, disclose that limitation and use available discovery tools. Never infer a confirmed sync failure from an old occasional measurement.

Use the user's current local date from context; ask if it is needed and unavailable. Do not shift requested periods to make stale records look current. If no records overlap the requested range, say so and identify available dates.

Call `query_daily` with explicit inclusive `from`/`to` dates and `granularity: "month"` for years or `"week"` for shorter trends. The response means:

- `value` uses `aggregation`: either the sum of recorded daily values or their unweighted average. These are not averages of all original sensor samples.
- `daily_min` and `daily_max` are extrema of stored daily values, not intraday extremes.
- `days_present` counts recorded dates; `days_expected` counts calendar dates in `period_start`–`period_end`, clipped to the query. Neither proves continuous sensor wear.
- A completely absent bucket or metric produces no row. Represent that interval as a gap, not zero. Keep units and aggregation methods separate across changes.
- Weekly `period` labels use SQLite `%Y-W%W`: Monday weeks split at New Year, not ISO weeks. Use `period_start` and `period_end` to interpret boundaries. Workout `sessions(granularity: "week")` uses Monday-date buckets with a different New Year convention; do not join the labels as if identical.

## Recover complete results

On `truncated: true`, discard the incomplete response before combining results. First request fewer metrics, then split into non-overlapping ranges at full bucket boundaries (month starts for monthly data, Mondays and January 1 for the existing weekly buckets). Keep the original outer bounds. Retry only the affected batches.

Prefer not to split a bucket. If it must be split, combine sums by addition, means weighted by `days_present`, minima/maxima with min/max, and coverage only across disjoint subranges. Never average averages equally or sum repeated buckets from overlapping retries. If a single bucket and metric still truncates, report that the full result could not be retrieved; do not loop indefinitely.

For a suspicious change, query daily values around that period. Use workout sessions or details only if needed to answer the user's question. Follow `workout_detail`'s independent cursors; historical summaries may exist after raw series expire.

## Interpret comparable periods

Identify the direction and dated changes the records support. Compare the latest three complete calendar months with the same months in the prior year only when both periods have usable observations; show coverage differences and avoid treating incomplete cumulative totals as behavioral changes. Distinguish a single year-over-year difference from established recurring seasonality. For a requested current month, label it partial and compare matching elapsed calendar days if useful.

For sum metrics, show recorded totals with covered days. A per-observed-day average may be useful but must be labeled and does not estimate missing days. For average metrics, weight multi-bucket comparisons by observed days and preserve units. Avoid percentage changes when the reference is zero. A device or recording-method change is a possible explanation, not a fact unless returned evidence supports it; daily aggregates do not identify the source device.

Present the range, granularity, coverage, a compact table or chart, and the changes with supporting numbers. Show gaps in charts. Separate observations from hypotheses; do not diagnose, infer causation or declare biological age/readiness from these trends. Explicitly state when coverage prevents a reliable comparison.
